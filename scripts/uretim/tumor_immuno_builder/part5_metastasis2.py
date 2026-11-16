# -*- coding: utf-8 -*-
"""
Part 5: Metastaz Kaskadı II (Slayt 21 - 24)
Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde.
"""

slides_part5 = [
    # SLIDE 21
    {
        "slideNumber": 21,
        "title": "Dolaşımda Hayatta Kalma: Trombosit Zırhı ve Anoikis Direnci",
        "subtitle": "Tümör embolisi, shear stress, NK lizisinden korunma ve TrkB sinyali",
        "badge": "Dolaşımda Sağkalım",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanda tek başına yüzen bir tümör hücresi ölü bir hücredir! Kalbin hidrolik basıncı onu parçalar, NK hücreleri deler, matriksten koptuğu için de anoikisle intihar eder. Ama zeki tümör doku faktörü salıp trombositleri üstüne çeker; oluşturduğu trombosit zırhıyla adeta bir denizaltı gibi hedefe süzülür.",
            "note": "Prof. Dr. Hikmet Keleş, tümör hücresi-trombosit agregatlarının shear stress ve NK hücrelerinden koruyucu rolünün ve Anoikis mekanizmasının TUS'ta klasik soru olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Dolaşım Sistemindeki Ölümcül Tehditler\n"
            "Damar lümenine giren Dolaşan Tümör Hücreleri (CTC) için kan dolaşımı son derece acımasız ve düşmanca bir ortamdır. "
            "Tek başına serbest yüzen bir kanser hücresi dakikalar içinde şu üç ölümcül engelle karşılaşır:\n"
            "1. **Hemodinamik Kayma Stresi (Shear Stress):** Kalbin yüksek atım gücü ve dar kapillerlerdeki sürtünme kuvveti hücre zarını "
            "mekanik olarak parçalar.\n"
            "2. **İmmün Hücre Saldırısı:** Kanda devriye gezen Doğal Katil (NK) hücreleri ve sitotoksik mononükleer hücreler tümör hücresini "
            "hızla tanıyarak litik granüllerle lize eder.\n"
            "3. **Anoikis (Ayrılma Apoptozu):** Normal epitelyal hücreler yaşayabilmek için integrinler aracılığıyla ekstrasellüler matrikse "
            "bağlı olmak zorundadır. Matriks bağı koptuğunda hücrede **BIM** ve **BMF** gibi pro-apoptotik proteinler tetiklenir ve hücre "
            "programlı intihara gider; bu özel apoptoz türüne **Anoikis** denir.\n\n"
            "### Trombosit Kalkanı (Tümör Embolisi Oluşumu)\n"
            "Metastaz yapmayı başaran saldırgan klonlar dolaşımda tek başlarına kalmazlar. Yüzeylerinde yüksek düzeyde **Doku Faktörü (TF)** "
            "eksprese ederek pıhtılaşma kaskadını tetikler ve lokal olarak trombin üretirler. Trombin dolaşımdaki trombositleri hızla aktive "
            "eder. Aktive olan trombositler tümör hücresinin yüzeyine yapışarak etrafını yoğun bir fibrin-trombosit zırhıyla kaplar; buna "
            "**Tümör Hücresi-Trombosit Embolisi** denir. Bu zırh tümöre üç hayati avantaj sağlar:\n"
            "- Tümör hücresini hemodinamik kayma stresine karşı mekanik bir yastık gibi korur.\n"
            "- Tümörün yüzeyindeki stres ligandlarını (MICA/MICB) fiziksel olarak örterek **NK hücrelerinin temasını ve lizisini engeller**.\n"
            "- Trombositlerden salgılanan TGF-beta ve PDGF tümör hücresinin EMT fenotipini ve canlılığını destekler.\n\n"
            "### Anoikis Direnci Mekanizmaları\n"
            "Metastatik hücreler, nörotrofik reseptör tirozin kinaz olan **TrkB** ekspresyonunu artırarak veya FAK ve Akt yolaklarını "
            "ligand bağımsız olarak sürekli aktif tutarak matriksten kopmuş olsalar bile kaspaz aktivasyonunu bloke eder ve anoikise direnç kazanırlar.\n\n"
            "🔴 **ÖNEMLİ:** Tümör hücreleri doku faktörü eksprese ederek trombosit agregasyonu başlatır; oluşan fibrin-trombosit zırhı "
            "tümörü hemodinamik kayma stresinden ve NK hücre lizisinden korur.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Epitelyal hücrelerin ekstrasellüler matriks ile temasını kaybetmesi durumunda integrin sinyalinin "
            "kesilmesine bağlı olarak tetiklenen programlı hücre ölümüne Anoikis adı verilir."
        ),
        "content": (
            "### Dolaşım Sistemindeki Ölümcül Tehditler\n"
            "Damar lümenine giren Dolaşan Tümör Hücreleri (CTC) için kan dolaşımı son derece acımasız ve düşmanca bir ortamdır. "
            "Tek başına serbest yüzen bir kanser hücresi dakikalar içinde şu üç ölümcül engelle karşılaşır:\n"
            "1. **Hemodinamik Kayma Stresi (Shear Stress):** Kalbin yüksek atım gücü ve dar kapillerlerdeki sürtünme kuvveti hücre zarını "
            "mekanik olarak parçalar.\n"
            "2. **İmmün Hücre Saldırısı:** Kanda devriye gezen Doğal Katil (NK) hücreleri ve sitotoksik mononükleer hücreler tümör hücresini "
            "hızla tanıyarak litik granüllerle lize eder.\n"
            "3. **Anoikis (Ayrılma Apoptozu):** Normal epitelyal hücreler yaşayabilmek için integrinler aracılığıyla ekstrasellüler matrikse "
            "bağlı olmak zorundadır. Matriks bağı koptuğunda hücrede **BIM** ve **BMF** gibi pro-apoptotik proteinler tetiklenir ve hücre "
            "programlı intihara gider; bu özel apoptoz türüne **Anoikis** denir.\n\n"
            "### Trombosit Kalkanı (Tümör Embolisi Oluşumu)\n"
            "Metastaz yapmayı başaran saldırgan klonlar dolaşımda tek başlarına kalmazlar. Yüzeylerinde yüksek düzeyde **Doku Faktörü (TF)** "
            "eksprese ederek pıhtılaşma kaskadını tetikler ve lokal olarak trombin üretirler. Trombin dolaşımdaki trombositleri hızla aktive "
            "eder. Aktive olan trombositler tümör hücresinin yüzeyine yapışarak etrafını yoğun bir fibrin-trombosit zırhıyla kaplar; buna "
            "**Tümör Hücresi-Trombosit Embolisi** denir. Bu zırh tümöre üç hayati avantaj sağlar:\n"
            "- Tümör hücresini hemodinamik kayma stresine karşı mekanik bir yastık gibi korur.\n"
            "- Tümörün yüzeyindeki stres ligandlarını (MICA/MICB) fiziksel olarak örterek **NK hücrelerinin temasını ve lizisini engeller**.\n"
            "- Trombositlerden salgılanan TGF-beta ve PDGF tümör hücresinin EMT fenotipini ve canlılığını destekler.\n\n"
            "### Anoikis Direnci Mekanizmaları\n"
            "Metastatik hücreler, nörotrofik reseptör tirozin kinaz olan **TrkB** ekspresyonunu artırarak veya FAK ve Akt yolaklarını "
            "ligand bağımsız olarak sürekli aktif tutarak matriksten kopmuş olsalar bile kaspaz aktivasyonunu bloke eder ve anoikise direnç kazanırlar.\n\n"
            "🔴 **ÖNEMLİ:** Tümör hücreleri doku faktörü eksprese ederek trombosit agregasyonu başlatır; oluşan fibrin-trombosit zırhı "
            "tümörü hemodinamik kayma stresinden ve NK hücre lizisinden korur.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Epitelyal hücrelerin ekstrasellüler matriks ile temasını kaybetmesi durumunda integrin sinyalinin "
            "kesilmesine bağlı olarak tetiklenen programlı hücre ölümüne Anoikis adı verilir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Tümör embolileri, tümör hücresinin doku faktörü salarak trombositleri etrafına toplamasıyla oluşur; NK hücrelerinden kaçışı sağlar.",
            "🔵 **ÇIKMIŞ SORU:** Normal epitel hücrelerinin matriksten ayrıldığında apoptoza gitmesi olayına Anoikis denir; metastatik subklonlar anoikis direnci kazanmıştır.",
            "⚡ **TROMBÜS:** Kanser hastalarında görülen yaygın migratuar tromboflebit (Trousseau sendromu), tümör kaynaklı doku faktörü ve müsinlerin sistemik pıhtılaşmayı tetiklemesiyle gelişir."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Trombosit zırhı, tümör yüzeyindeki MICA/MICB antijenlerini kapatarak NK hücrelerinin NKG2D reseptörünü körleştirir.",
            "🔵 **ÇIKMIŞ SORU:** TrkB reseptör tirozin kinaz ekspresyonu tümör hücrelerine anoikis direnci ve agresif metastatik karakter kazandırır.",
            "⚡ **TROMBÜS:** Dolaşan tümör hücrelerinin (CTC) tespiti 'sıvı biyopsi' yöntemleriyle erken metastaz takibinde kullanılır."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Trombosit Zırhı ile Korunma",
                    "desc": "Tümör doku faktörü salarak etrafında trombosit kalkanı kurar; kayma stresi ve NK lizisini engeller.",
                    "isKey": True
                },
                {
                    "title": "Anoikis Direnci Biyolojisi",
                    "desc": "Matriksten kopan normal hücre BIM ile ölürken, metastatik hücre Akt ve TrkB ile hayatta kalır.",
                    "isKey": True
                },
                {
                    "title": "NK Hücre Maskelemesi",
                    "desc": "Fibrin kılıf tümör stres ligandlarını örterek Doğal Katil hücrelerin missing-self saldırısını önler.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Dolaşımdaki Tehditler ve Tümörün Geliştirdiği Savunma Mekanizmaları",
                "headers": ["Dolaşımdaki Tehdit", "Fizyopatolojik Hasar Mekanizması", "Tümörün Karşı Savunma Mekanizması", "Hücresel Sonuç"],
                "rows": [
                    ["Hemodinamik Kayma Stresi", "Yüksek akım ve kapiller daralma ile zarda yırtılma", "Trombosit ve fibrin agregasyonu (tümör embolisi)", "Mekanik sürtünmeye karşı fiziksel yastıklama"],
                    ["NK Hücre Sitotoksisitesi", "Perforin/granzim ile tümör lizisi", "Trombosit zırhı ile stres antijenlerinin maskelenmesi", "NK hücresi teması engellenir, lizisten kaçış"],
                    ["Anoikis (Ayrılma Apoptozu)", "İntegrin sinyal kaybı -> BIM aktivasyonu -> Apoptoz", "TrkB aşırı ekspresyonu, kaspaz inhibisyonu, konstitütif Akt", "Matriksten bağımsız hücre sağkalımı"],
                    ["Monosit / Makrofaj İnfazı", "Fagositoz ve serbest oksijen radikalleri", "CD47 'Don't eat me' sinyalinin aşırı ekspresyonu", "Fagositozdan kaçış ve kanda uzun süre kalabilme"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-21-01",
                "category": "Dolaşımda Sağkalım",
                "front": "Tümör hücrelerinin dolaşımda trombositlerle agregatlar oluşturarak (tümör embolisi) elde ettiği en kritik iki avantaj nedir?",
                "hint": "Fiziksel basınç ve bir bağışıklık hücresinden saklanma.",
                "back": "1) **Hemodinamik kayma stresine (shear stress)** karşı korunma, 2) Yüzey antijenlerini örterek **Doğal Katil (NK) hücre lizisinden kaçış**.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide trombosit agregasyonunun metastazın can simidi olduğunu söylemiştir."
            },
            {
                "id": "imm-fc-21-02",
                "category": "Hücre Ölümü Tipleri",
                "front": "Epitel hücrelerinin ekstrasellüler matriks bağlantısını kaybettiklerinde apoptoza gitmesi sürecine ne ad verilir?",
                "hint": "Yunanca 'evsiz kalma / ayrılma' kökünden gelen terim.",
                "back": "**Anoikis**. İntegrin uyarısının kesilmesi sonucu BIM gibi pro-apoptotik proteinlerin indüklenmesiyle gerçekleşir.",
                "facultyNote": "TUS ve Dönem 3 sınavlarında anoikis tanımı patolojinin vazgeçilmez sorularındandır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-21",
            "question": "İntravazasyon yaparak kan dolaşımına katılan bir meme adenokarsinomu hücresinin dolaşımda canlı kalabilmesi, anoikisten kurtulması ve hedef organa ulaşabilmesi sürecinde gerçekleşen hücresel ve biyokimyasal mekanizmalar ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) Dolaşıma çıkan tümör hücreleri daima tek tek dolaşır; trombositlerle temas ettiklerinde anında ölürler.",
                "B) Tümör hücreleri doku faktörü eksprese ederek etraflarında koruyucu fibrin-trombosit zırhı kurar; bu yapı onları hemodinamik kayma stresinden ve NK hücre lizisinden korur.",
                "C) Anoikis, tümör hücrelerinin damar endoteline yapışmasını hızlandıran pro-metastatik bir adezyon molekülüdür.",
                "D) Kan dolaşımındaki yüksek hidrostatik basınç tümör hücrelerinde DNA tamir enzimlerini uyararak proliferasyonu artırır.",
                "E) Trombositler salgıladıkları perforin enzimi ile tümör hücrelerini dolaşımda tamamen temizler."
            ],
            "answer": "B",
            "explanation": "Dolaşıma katılan tümör hücrelerinin hayatta kalabilmesindeki en hayati strateji trombositlerle kümeleşerek 'Tümör Hücresi-Trombosit Embolisi' oluşturmaktır. Tümör yüzeyindeki doku faktörü trombin üretimini tetikler ve trombositleri aktive eder. Oluşan fibrin-trombosit zırhı tümör hücresini hem hemodinamik kayma stresinin (shear stress) mekanik parçalayıcı etkisinden korur hem de hücre yüzeyindeki stres ligandlarını örterek Doğal Katil (NK) hücrelerinin öldürücü temasını engeller.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 22
    {
        "slideNumber": 22,
        "title": "Ekstravazasyon, Organ Tropizmi ve 'Tohum ve Toprak' Hipotezi",
        "subtitle": "Stephen Paget teorisi, CXCR4/CXCL12 aksı, prostatın osteoblastik tropizmi",
        "badge": "Organ Tropizmi",
        "badgeColor": "indigo",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Neden kolon karaciğere, prostat kemiğe, akciğer böbrek üstü bezine gider? Ewing 'kan nereye akarsa oraya gider' dedi ama Paget 1889'da gerçeği gördü: Tohum (kanser hücresi) ancak uygun Toprakta (organ mikroçevresi) yeşerir! CXCR4 taşıyan meme kanseri, CXCL12 salan kemik iliğine koşar.",
            "note": "Prof. Dr. Hikmet Keleş, Stephen Paget'nin 'Seed and Soil' hipotezinin ve prostatın osteoblastik kemik metastazı mekanizmasının sınavların en klasik patoloji soruları olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Ekstravazasyon Basamağı\n"
            "Dolaşan tümör embolisi hedef organın mikrosirkülasyonuna ulaştığında lümen çapı daralır ve mekanik olarak kılcal damara takılır. "
            "Ekstravazasyon lökosit diapedezine benzer aşamalarla gerçekleşir: Tümör yüzeyindeki karbohidrat ligandları endoteldeki "
            "**E-selektin** ve **P-selektin**'e bağlanarak hücreyi yavaşlatır (yuvarlanma / rolling). Ardından tümör integrinleri (**VLA-4 / alfa-4-beta-1**) "
            "endoteldeki **VCAM-1**'e kilitlenir. Hücre endotel kavşaklarından damar dışına çıkarak organ parankimine sızar (**Ekstravazasyon**).\n\n"
            "### Organ Tropizmi Paradoksu: Ewing vs Paget Hipotezi\n"
            "Kan akımı vücudun her yerine ulaşırken neden belirli kanserler ısrarla belirli organlara metastaz yapar?\n"
            "1. **James Ewing Hipotezi (Anatomik / Hemodinamik Teori):** Metastaz lokalizasyonu tamamen vasküler ve lenfatik drenaj yollarına "
            "bağlıdır. Örneğin kolorektal karsinomların venöz kanı portal venle karaciğere boşaldığı için ilk metastaz karaciğerde görülür. "
            "Benzer şekilde alt ekstremite osteosarkomu vena kava yoluyla ilk kapiller filtre olan akciğere gider.\n"
            "2. **Stephen Paget Hipotezi ('Seed and Soil' - Tohum ve Toprak, 1889):** Ewing teorisi birçok metastazı açıklayamaz! Paget'e "
            "göre tümör hücreleri **'Tohum' (Seed)**, hedef organ dokusu ise **'Toprak'tır (Soil)**. Bir tohum vücudun her yerine dağılabilir "
            "ancak sadece uygun besin, büyüme faktörü ve adezyon ortamı sunan spesifik 'topraklarda' filizlenebilir.\n\n"
            "### Moleküler Organ Tropizmi Örnekleri\n"
            "- **Meme Karsinomu ve Kemik/Akciğer:** Meme kanseri hücreleri yüzeylerinde yüksek oranda **CXCR4** ve **CCR7** kemokin reseptörleri "
            "taşırlar. Bu reseptörlerin ligantları olan **CXCL12 (SDF-1)** ve **CCL21** ise kemik iliği, akciğer ve lenf nodu stromasında çok yüksek "
            "konsantrasyonda sentezlenir. Meme kanseri bu kemokin gradientini takip ederek seçici olarak kemik ve akciğere göç eder.\n"
            "- **Prostat Karsinomu ve Osteoblastik Metastaz:** Prostat kanseri kemik iliğine olağanüstü afinite gösterir. Kemik iliğinde "
            "salınan **Endotelin-1 (ET-1)** ve TGF-beta prostat hücrelerini çeker. Prostat hücreleri osteoblastları aşırı uyararak radyoopak, "
            "sklerotik **Osteoblastik Kemik Metastazları** meydana getirir (diğer çoğu kanser osteolitik kemik yıkımı yapar).\n"
            "- **Akciğer Karsinomu:** Karakteristik olarak **Sürrenal (Adrenal) Bezlere** ve **Beyne** seçici organotropizm gösterir.\n\n"
            "🔴 **ÖNEMLİ:** Paget'nin 'Tohum ve Toprak' teorisine göre tümör hücreleri (tohum) sadece uygun kemokin reseptörlerine (CXCR4-CXCL12) "
            "ve büyüme ortamına sahip spesifik organ mikroçevresinde (toprak) kolonize olabilir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** İleri yaştaki bir erkekte direkt grafide veya sintigrafide vertebra kemiklerinde sklerotik (osteoblastik) "
            "metastatik lezyonlar izlendiğinde öncelikle araştırılması gereken primer odak Prostat Adenokarsinomudur."
        ),
        "content": (
            "### Ekstravazasyon Basamağı\n"
            "Dolaşan tümör embolisi hedef organın mikrosirkülasyonuna ulaştığında lümen çapı daralır ve mekanik olarak kılcal damara takılır. "
            "Ekstravazasyon lökosit diapedezine benzer aşamalarla gerçekleşir: Tümör yüzeyindeki karbohidrat ligandları endoteldeki "
            "**E-selektin** ve **P-selektin**'e bağlanarak hücreyi yavaşlatır (yuvarlanma / rolling). Ardından tümör integrinleri (**VLA-4 / alfa-4-beta-1**) "
            "endoteldeki **VCAM-1**'e kilitlenir. Hücre endotel kavşaklarından damar dışına çıkarak organ parankimine sızar (**Ekstravazasyon**).\n\n"
            "### Organ Tropizmi Paradoksu: Ewing vs Paget Hipotezi\n"
            "Kan akımı vücudun her yerine ulaşırken neden belirli kanserler ısrarla belirli organlara metastaz yapar?\n"
            "1. **James Ewing Hipotezi (Anatomik / Hemodinamik Teori):** Metastaz lokalizasyonu tamamen vasküler ve lenfatik drenaj yollarına "
            "bağlıdır. Örneğin kolorektal karsinomların venöz kanı portal venle karaciğere boşaldığı için ilk metastaz karaciğerde görülür. "
            "Benzer şekilde alt ekstremite osteosarkomu vena kava yoluyla ilk kapiller filtre olan akciğere gider.\n"
            "2. **Stephen Paget Hipotezi ('Seed and Soil' - Tohum ve Toprak, 1889):** Ewing teorisi birçok metastazı açıklayamaz! Paget'e "
            "göre tümör hücreleri **'Tohum' (Seed)**, hedef organ dokusu ise **'Toprak'tır (Soil)**. Bir tohum vücudun her yerine dağılabilir "
            "ancak sadece uygun besin, büyüme faktörü ve adezyon ortamı sunan spesifik 'topraklarda' filizlenebilir.\n\n"
            "### Moleküler Organ Tropizmi Örnekleri\n"
            "- **Meme Karsinomu ve Kemik/Akciğer:** Meme kanseri hücreleri yüzeylerinde yüksek oranda **CXCR4** ve **CCR7** kemokin reseptörleri "
            "taşırlar. Bu reseptörlerin ligantları olan **CXCL12 (SDF-1)** ve **CCL21** ise kemik iliği, akciğer ve lenf nodu stromasında çok yüksek "
            "konsantrasyonda sentezlenir. Meme kanseri bu kemokin gradientini takip ederek seçici olarak kemik ve akciğere göç eder.\n"
            "- **Prostat Karsinomu ve Osteoblastik Metastaz:** Prostat kanseri kemik iliğine olağanüstü afinite gösterir. Kemik iliğinde "
            "salınan **Endotelin-1 (ET-1)** ve TGF-beta prostat hücrelerini çeker. Prostat hücreleri osteoblastları aşırı uyararak radyoopak, "
            "sklerotik **Osteoblastik Kemik Metastazları** meydana getirir (diğer çoğu kanser osteolitik kemik yıkımı yapar).\n"
            "- **Akciğer Karsinomu:** Karakteristik olarak **Sürrenal (Adrenal) Bezlere** ve **Beyne** seçici organotropizm gösterir.\n\n"
            "🔴 **ÖNEMLİ:** Paget'nin 'Tohum ve Toprak' teorisine göre tümör hücreleri (tohum) sadece uygun kemokin reseptörlerine (CXCR4-CXCL12) "
            "ve büyüme ortamına sahip spesifik organ mikroçevresinde (toprak) kolonize olabilir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** İleri yaştaki bir erkekte direkt grafide veya sintigrafide vertebra kemiklerinde sklerotik (osteoblastik) "
            "metastatik lezyonlar izlendiğinde öncelikle araştırılması gereken primer odak Prostat Adenokarsinomudur."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Stephen Paget'nin 'Tohum ve Toprak' hipotezi, tümör hücrelerinin organ spesifik metastaz paternlerini mikroçevresel uyumla açıklar.",
            "🔵 **ÇIKMIŞ SORU:** Meme karsinomunun kemik iliğine ve akciğere yönelmesinde tümör yüzeyindeki CXCR4 reseptörü ile hedef stromadaki CXCL12 kemokin aksı rol oynar.",
            "⚡ **PROSTAT METASTAZI:** Prostat adenokarsinomu osteoblastları uyararak karakteristik osteoblastik (sklerotik/kemik yapıcı) metastazlar yapar."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Ewing'in anatomik hipotezi kolon kanserinin karaciğere (portal drenaj) metastazını başarıyla açıklar.",
            "🔵 **ÇIKMIŞ SORU:** Akciğer kanserleri sürrenal (adrenal) bezlere ve beyne yüksek oranda seçici tropizm gösterir.",
            "⚡ **PROSTAT METASTAZI:** Meme kanseri ve böbrek hücreli karsinom ise kemikte kemik erimesiyle giden osteolitik lezyonlar oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Tohum ve Toprak Hipotezi",
                    "desc": "Tümör hücresi (tohum) yalnızca biyokimyasal olarak elverişli organ stromasında (toprak) koloni kurabilir.",
                    "isKey": True
                },
                {
                    "title": "CXCR4 - CXCL12 Kemokin Aksı",
                    "desc": "Meme kanseri hücreleri CXCL12 gradientini izleyerek kemik iliği ve akciğer kılcallarına ekstravaze olur.",
                    "isKey": True
                },
                {
                    "title": "Prostatın Osteoblastik Tropizmi",
                    "desc": "Endotelin-1 ve büyüme faktörleri ile osteoblastları uyararak sklerotik kemik lezyonları meydana getirir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Primer Tümörler ve Seçici Organ Metastaz Paternleri",
                "headers": ["Primer Tümör Türü", "En Sık Metastaz Hedefi", "Tropizm Mekanizması / Yolak", "Karakteristik Lezyon Tipi"],
                "rows": [
                    ["Kolorektal Adenokarsinom", "Karaciğer", "Portal venöz anatomik drenaj (Ewing teorisi)", "Çok odaklı nodüler metastazlar"],
                    ["Meme Adenokarsinomu", "Kemik iliği, akciğer, beyin", "CXCR4 / CXCL12 kemokin aksı ve RANKL", "Ağırlıklı osteolitik kemik lezyonları"],
                    ["Prostat Adenokarsinomu", "Aksiyel iskelet (Vertebra)", "Endotelin-1 (ET-1), osteoblast aktivasyonu", "Osteoblastik (sklerotik/radyoopak) lezyonlar"],
                    ["Bronkojenik Akciğer Ca", "Sürrenal (Adrenal) bezler, beyin", "Organotropik vasküler adezyon molekülleri", "Bilateral sürrenal kitleleri, nörolojik defisitler"],
                    ["Malign Melanom", "Karaciğer, beyin, GIS, dalak", "Geniş tropizm (neredeyse tüm organlar)", "Hiperpigmente multipl organ metastazları"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-22-01",
                "category": "Organ Tropizmi",
                "front": "Meme kanseri hücrelerinin kemik iliği ve akciğere seçici olarak göç etmesini sağlayan kemokin reseptörü ve ligantı hangisidir?",
                "hint": "Reseptör 4, ligant 12.",
                "back": "Tümör hücresindeki **CXCR4 reseptörü** ile hedef organ stromasındaki **CXCL12 (SDF-1)** kemokinidir.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide CXCR4-CXCL12 aksının farmakolojik hedef olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-22-02",
                "category": "Kemik Patolojisi",
                "front": "Kemik metastazlarında osteolitik yıkım yerine osteoblastik (kemik yapıcı/sklerotik) lezyon oluşturan en tipik malignite hangisidir?",
                "hint": "İleri yaş erkeklerde sık görülen adenokarsinom.",
                "back": "**Prostat Adenokarsinomu**. Endotelin-1 salarak osteoblastları uyarır ve sklerotik kemik oluşturur.",
                "facultyNote": "TUS Radyoloji ve Patoloji ortak sorularında sklerotik kemik metastazı daima prostatı işaret eder."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-22",
            "question": "71 yaşındaki bir erkek hasta son 3 aydır giderek artan bel ağrısı şikayetiyle başvuruyor. Çekilen lomber vertebra direkt grafisinde L2-L4 vertebralarda kemik dansitesinde belirgin artışla karakterize multipl radyoopak, sklerotik (osteoblastik) lezyonlar saptanıyor. Bu hastada kemik metastazına yol açan en olası primer neoplazi ve organ tropizmi mekanizması hangisidir?",
            "options": [
                "A) Renal hücreli karsinom; osteoklastları aşırı uyararak kemik rezorpsiyonu yapmasıyla bilinir.",
                "B) Prostat adenokarsinomu; endotelin-1 salınımı ve osteoblast uyarısıyla karakteristik osteoblastik metastaz oluşturur.",
                "C) Kolon karsinomu; portal ven yoluyla omurgaya doğrudan kaval reflü ile yerleşir.",
                "D) Malign melanom; melanositlerin kemik iliğinde kalsiyum biriktirmesi sonucu skleroz yapar.",
                "E) Mide taşlı yüzük hücreli karsinomu; yalnızca over stromasına metastaz (Krukenberg) yapar, kemiğe gitmez."
            ],
            "answer": "B",
            "explanation": "Kemik metastazları genellikle osteoklast aktivasyonuyla kemiği eriten osteolitik lezyonlar şeklinde görülür (örn. meme kanseri, akciğer kanseri, böbrek kanseri). Ancak Prostat Adenokarsinomu osteoblastları güçlü şekilde uyararak radyoopak, sklerotik 'Osteoblastik Kemik Metastazları' oluşturur. Prostat hücrelerinin salgıladığı Endotelin-1 (ET-1), TGF-beta ve BMP'ler osteoblastik kemik yapımını tetikler. Bu tablo Stephen Paget'nin 'Tohum ve Toprak' teorisinin klasik bir örneğidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 23
    {
        "slideNumber": 23,
        "title": "Premetastatik Niş ve Kolonizasyon (Anjiyogenik Anahtar)",
        "subtitle": "VEGFR1+ kemik iliği hücreleri, MET geri dönüşümü ve anjiyogenez eşiği",
        "badge": "Kolonizasyon & Niş",
        "badgeColor": "cyan",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser hücresi hedef organa varmadan önce oraya ajanlarını yollar! Primer tümör ekzozomlar salar, kemik iliğinden VEGFR1+ öncüleri kaldırıp hedef organda iniş pisti kurdurur; buna Premetastatik Niş diyoruz. Hücre indiğinde ise damar yapmadan (anjiyogenik anahtar) 1 milimetreyi geçemez!",
            "note": "Prof. Dr. Hikmet Keleş, premetastatik niş hazırlığı ve mikrometastazın 1-2 mm difüzyon sınırını aşmasını sağlayan anjiyogenik anahtarın önemini amfide vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Premetastatik Niş (Pre-metastatic Niche) Kavramı\n"
            "Geleneksel görüşe göre metastaz, hücrenin rastgele bir organa ulaşıp yerleşmesi olarak kabul edilirdi. Oysa modern tümör "
            "biyolojisi göstermiştir ki: **Tümör hücreleri henüz hedef organa varmadan önce, primer tümör uzak hedef organı kolonizasyona "
            "uygun hale getirmek üzere sistemik olarak hazırlar!** Bu hazırlanmış ortama **Premetastatik Niş** adı verilir.\n\n"
            "### İniş Pistinin Hazırlanması:\n"
            "1. **Tümöral Ekzozomlar ve Sitokinler:** Primer tümör tarafından kana salgılanan mikroveziküller (tümör ekzozomları), VEGF, "
            "TGF-beta ve TNF-alfa; hedef organdaki (örn. akciğer) endotel hücrelerini aktive eder ve geçirgenliği artırır.\n"
            "2. **VEGFR1+ Kemik İliği Progenitörleri:** Primer tümörün sistemik sinyalleri kemik iliğinden **VEGFR1+ (Flt-1+) myeloid progenitör "
            "hücreleri** mobilize eder. Bu hücreler hedef organ stromasına göç ederek yuvalanır.\n"
            "3. **Fibronektin Birikimi:** Bu hücreler hedef organda yoğun **Fibronektin** birikimini ve **MMP-9** salınımını tetikler; böylece "
            "dolaşımdan gelecek olan tümör hücreleri için güvenli, besleyici bir 'iniş pisti ve yuva (niş)' kurulmuş olur.\n\n"
            "### Mezenkimal-Epitelyal Geçiş (MET): Aslına Geri Dönüş\n"
            "İnvazyon ve dolaşımda hareket edebilmek için epitel karakterini bırakıp mezenkimal fenotip (EMT) kazanan tümör hücresi, "
            "hedef dokuya ulaştığında tersine bir biyolojik dönüşüm geçirir: **Mezenkimal-Epitelyal Geçiş (MET)**. Vimentin azalır, "
            "**E-kaderin** yeniden hücre zarına döner. Hücreler tekrar birbirine kenetlenerek primer tümörün histopatolojik mimarisini "
            "(glandüler asinuslar, tubuller veya kordonlar) sekonder organda yeniden inşa ederler.\n\n"
            "### Anjiyogenik Anahtar (Angiogenic Switch) ve Makrometastaz\n"
            "Hedef dokuda kurulan ilk odak birkaç yüz hücreden oluşan klinik olarak sessiz bir **Mikrometastaz**dır. Oksijen ve besinlerin "
            "doku içindeki difüzyon sınırı **1 ila 2 mm**'dir. Yeni damarlanma sağlayamayan bir mikrometastatik odak 1-2 mm'den daha büyük "
            "bir kitleye dönüşemez; hipoksi ve nekroza girer. Bu aşamada tümör hücreleri hipoksiyle indüklenen faktör-1alfa (**HIF-1α**) "
            "aracılığıyla ortama yoğun **VEGF** ve bFGF salarak **'Anjiyogenik Anahtarı' (Angiogenic Switch)** açarlar. Yeni kapillerlerin "
            "filizlenmesiyle (sprouting) beslenen mikrometastaz kontrolsüzce büyüyerek klinik olarak saptanan ölümcül **Makrometastaza** dönüşür.\n\n"
            "🔴 **ÖNEMLİ:** Primer tümörün saldığı ekzozomlar ve sitokinler hedef organda VEGFR1+ kemik iliği progenitörlerini toplayıp "
            "fibronektin zengini 'Premetastatik Niş' (iniş pisti) hazırlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Mikrometastazların difüzyon sınırını (1-2 mm) aşarak makroskopik makrometastaza dönüşebilmesi için "
            "zorunlu olan ve VEGF salınımıyla tetiklenen biyolojik adım 'Anjiyogenik Anahtarın' (Angiogenic switch) devreye girmesidir."
        ),
        "content": (
            "### Premetastatik Niş (Pre-metastatic Niche) Kavramı\n"
            "Geleneksel görüşe göre metastaz, hücrenin rastgele bir organa ulaşıp yerleşmesi olarak kabul edilirdi. Oysa modern tümör "
            "biyolojisi göstermiştir ki: **Tümör hücreleri henüz hedef organa varmadan önce, primer tümör uzak hedef organı kolonizasyona "
            "uygun hale getirmek üzere sistemik olarak hazırlar!** Bu hazırlanmış ortama **Premetastatik Niş** adı verilir.\n\n"
            "### İniş Pistinin Hazırlanması:\n"
            "1. **Tümöral Ekzozomlar ve Sitokinler:** Primer tümör tarafından kana salgılanan mikroveziküller (tümör ekzozomları), VEGF, "
            "TGF-beta ve TNF-alfa; hedef organdaki (örn. akciğer) endotel hücrelerini aktive eder ve geçirgenliği artırır.\n"
            "2. **VEGFR1+ Kemik İliği Progenitörleri:** Primer tümörün sistemik sinyalleri kemik iliğinden **VEGFR1+ (Flt-1+) myeloid progenitör "
            "hücreleri** mobilize eder. Bu hücreler hedef organ stromasına göç ederek yuvalanır.\n"
            "3. **Fibronektin Birikimi:** Bu hücreler hedef organda yoğun **Fibronektin** birikimini ve **MMP-9** salınımını tetikler; böylece "
            "dolaşımdan gelecek olan tümör hücreleri için güvenli, besleyici bir 'iniş pisti ve yuva (niş)' kurulmuş olur.\n\n"
            "### Mezenkimal-Epitelyal Geçiş (MET): Aslına Geri Dönüş\n"
            "İnvazyon ve dolaşımda hareket edebilmek için epitel karakterini bırakıp mezenkimal fenotip (EMT) kazanan tümör hücresi, "
            "hedef dokuya ulaştığında tersine bir biyolojik dönüşüm geçirir: **Mezenkimal-Epitelyal Geçiş (MET)**. Vimentin azalır, "
            "**E-kaderin** yeniden hücre zarına döner. Hücreler tekrar birbirine kenetlenerek primer tümörün histopatolojik mimarisini "
            "(glandüler asinuslar, tubuller veya kordonlar) sekonder organda yeniden inşa ederler.\n\n"
            "### Anjiyogenik Anahtar (Angiogenic Switch) ve Makrometastaz\n"
            "Hedef dokuda kurulan ilk odak birkaç yüz hücreden oluşan klinik olarak sessiz bir **Mikrometastaz**dır. Oksijen ve besinlerin "
            "doku içindeki difüzyon sınırı **1 ila 2 mm**'dir. Yeni damarlanma sağlayamayan bir mikrometastatik odak 1-2 mm'den daha büyük "
            "bir kitleye dönüşemez; hipoksi ve nekroza girer. Bu aşamada tümör hücreleri hipoksiyle indüklenen faktör-1alfa (**HIF-1α**) "
            "aracılığıyla ortama yoğun **VEGF** ve bFGF salarak **'Anjiyogenik Anahtarı' (Angiogenic Switch)** açarlar. Yeni kapillerlerin "
            "filizlenmesiyle (sprouting) beslenen mikrometastaz kontrolsüzce büyüyerek klinik olarak saptanan ölümcül **Makrometastaza** dönüşür.\n\n"
            "🔴 **ÖNEMLİ:** Primer tümörün saldığı ekzozomlar ve sitokinler hedef organda VEGFR1+ kemik iliği progenitörlerini toplayıp "
            "fibronektin zengini 'Premetastatik Niş' (iniş pisti) hazırlar.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Mikrometastazların difüzyon sınırını (1-2 mm) aşarak makroskopik makrometastaza dönüşebilmesi için "
            "zorunlu olan ve VEGF salınımıyla tetiklenen biyolojik adım 'Anjiyogenik Anahtarın' (Angiogenic switch) devreye girmesidir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Premetastatik niş hazırlığında VEGFR1+ kemik iliği kökenli myeloid progenitörler hedef organda fibronektin biriktirerek yuva açar.",
            "🔵 **ÇIKMIŞ SORU:** Mikrometastazların 1-2 mm'lik difüzyon sınırını aşarak makrometastaza büyümesi için zorunlu olan adım 'Anjiyogenik Anahtarın' (VEGF) devreye girmesidir.",
            "⚡ **MET:** Hedef organda kolonize olan hücreler mezenkimal-epitelyal geçiş (MET) geçirerek E-kaderini yeniden kazanır ve primer tümör morfolojisini taklit eder."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Tümöral ekzozomlar taşıdıkları mikroRNA ve proteinlerle uzak organdaki stromal hücreleri önceden reprogramlar.",
            "🔵 **ÇIKMIŞ SORU:** Oksijen difüzyon sınırı (1-2 mm) aşılamadığında mikrometastatik odaklar anjiyogenez olmaksızın büyüyemez.",
            "⚡ **MET:** EMT invazyon için, MET ise hedef organda kolonizasyon ve doku mimarisi kurmak için zorunludur."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Premetastatik Niş Hazırlığı",
                    "desc": "Ekzozomlar ve VEGFR1+ hücreler hedef organda fibronektin biriktirerek tümör için iniş pisti kurar.",
                    "isKey": True
                },
                {
                    "title": "MET ile Yeniden Epitelyalleşme",
                    "desc": "Hedefe varan hücre E-kaderini yeniden aktive ederek primer tümörün glandüler yapısını taklit eder.",
                    "isKey": True
                },
                {
                    "title": "Anjiyogenik Anahtar (1-2 mm Sınırı)",
                    "desc": "VEGF ile neovaskülarizasyon sağlanmadan mikrometastaz klinik makrometastaza dönüşemez.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Premetastatik Niş, Mikrometastaz ve Makrometastaz Dinamikleri",
                "headers": ["Evre", "Biyolojik Süreç", "Kritik Moleküler Aktörler", "Klinik / Radyolojik Durum"],
                "rows": [
                    ["Premetastatik Niş", "Hedef organda iniş pisti kurulması", "Tümör ekzozomları, VEGFR1+ öncüller, Fibronektin", "Organ tamamen normal görünür (asemptomatik)"],
                    ["Mikrometastaz", "Ekstravazasyon ve dokuya yerleşim", "MET süreci, E-kaderin re-ekspresyonu", "Klinik ve radyolojik olarak saptanamaz (<1 mm)"],
                    ["Anjiyogenik Anahtar", "Neovaskülarizasyonun tetiklenmesi", "HIF-1alfa, VEGF, bFGF salınımı", "Difüzyon sınırının (1-2 mm) aşılması eşiği"],
                    ["Makrometastaz", "Kontrolsüz büyüme ve organ destrüksiyonu", "Devam eden anjiyogenez, stromal destek", "Görüntülemede kitle (BT/PET pozitif, semptomatik)"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-23-01",
                "category": "Premetastatik Niş",
                "front": "Primer tümörün saldığı faktörlerle hedef organda toplanarak fibronektin biriktiren kemik iliği kökenli hücreler hangileridir?",
                "hint": "Bir reseptör tirozin kinaz taşıyan myeloid öncüller.",
                "back": "**VEGFR1+ (Flt-1+) myeloid progenitör hücreler**. Hedef organda tümör için 'Premetastatik Niş' (iniş pisti) kurarlar.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide VEGFR1+ hücrelerin metastaz öncüsü olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-23-02",
                "category": "Kolonizasyon",
                "front": "Bir mikrometastatik odağın 1-2 mm çaptan daha büyük bir kitleye dönüşebilmesi için mutlaka devreye girmesi gereken biyolojik mekanizma nedir?",
                "hint": "Damar yapımıyla ilişkili şalter.",
                "back": "**Anjiyogenik Anahtar (Angiogenic Switch)**. VEGF salınımıyla yeni damar filizlenmesi sağlanmazsa difüzyon sınırı aşılamaz.",
                "facultyNote": "TUS Patolojide tümörün 1-2 mm büyüme sınırı ve VEGF ilişkisi sıkça sorulan bir kuraldır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-23",
            "question": "Metastaz sürecinde primer tümörün uzak organlarda 'Premetastatik Niş' hazırlaması, hedef dokuda kolonizasyon kurması ve anjiyogenik anahtarın devreye girmesi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Premetastatik niş hazırlığı hedef organda tümör hücreleri oluştuktan aylar sonra başlayan geç bir reaksiyondur.",
                "B) Primer tümörün salgıladığı ekzozomlar ve sitokinler hedef organda VEGFR1+ kemik iliği öncüllerini toplayarak fibronektin zengini iniş pisti kurar; mikrometastazlar VEGF ile anjiyogenik anahtarı açmadan 1-2 mm'den büyük makrometastaz olamaz.",
                "C) Tümör hücreleri hedef organda E-kaderin ekspresyonunu tamamen sıfırlayarak tek tek hücreler halinde kalır.",
                "D) Mikrometastatik odaklar anjiyogeneze ihtiyaç duymadan sadece laktik asit difüzyonuyla 10 cm kitlelere ulaşabilir.",
                "E) Fibronektin tümör hücrelerini lize eden bir doğal katil hücresi proteazıdır."
            ],
            "answer": "B",
            "explanation": "Primer tümör uzak hedef organı henüz hücreler ulaşmadan önce sistemik sinyaller ve ekzozomlarla hazırlar; buna 'Premetastatik Niş' denir. Bu süreçte kemik iliğinden mobilize olan VEGFR1+ myeloid progenitör hücreler hedef dokuda toplanır, fibronektin birikimi sağlar ve iniş pisti oluşturur. Hedefe ulaşan hücreler Mezenkimal-Epitelyal Geçiş (MET) ile yeniden E-kaderin kazanıp kolonize olurlar. Ancak difüzyon sınırı 1-2 mm olduğu için, VEGF ile 'Anjiyogenik Anahtar' açılmadan bu odaklar makroskopik makrometastaza büyüyemez.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 24
    {
        "slideNumber": 24,
        "title": "Tümör Dormansisi, Geç Nüksler ve Metastazın Tedavi Rasyoneli",
        "subtitle": "Hücresel ve anjiyogenik uyku hali, tetikleyiciler ve multimodal onkoloji",
        "badge": "Dormansi & Tedavi",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Meme kanseri ameliyatından 15 yıl sonra hasta tertemizken birden kemikte metastaz çıkar! Neredeydi bu hücreler? G0 fazında uyuyorlardı. Hücre bölünmüyorsa kemoterapi ona dokunamaz. İmmün sistem yaşlanıp stroma sarsılınca canavar uyanır; bu yüzden onkoloji ömür boyu teyakkuzdur.",
            "note": "Prof. Dr. Hikmet Keleş, tümör dormansisinin özellikle hormon reseptörü pozitif meme kanseri ve melanomdaki klinik önemini ve M evresinin tedavi stratejisini belirlediğini vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Tümör Dormansisi (Uyku Hali) Kavramı\n"
            "Onkolojik cerrahi ve kemoradyoterapi sonrası tümörden tamamen arındığı düşünülen hastalarda 5, 10, hatta 20 yıl sonra aniden "
            "viseral organ veya kemik metastazlarının belirmesi onkolojinin en çarpıcı gerçeklerinden biridir. Bu durum **Tümör Dormansisi "
            "(Tumor Dormancy)** kavramı ile açıklanır. Dormansi iki temel biyolojik formda gerçekleşir:\n"
            "1. **Hücresel Dormansi (G0/G1 Tutukluğu):** Uzak organ nişine yerleşen soliter kanser kök hücreleri mitozu tamamen durdurur, "
            "metabolizmalarını bazal seviyeye indirir ve hücre siklusunun **G0 fazında** adeta kış uykusuna yatar. Klasik sitotoksik "
            "kemoterapiler ve radyoterapi hızla bölünen hücreleri hedeflediği için, G0 fazındaki dorman hücrelere **asla etki edemez!**\n"
            "2. **Tümör Kütlesi Dormansisi (Anjiyogenik / İmmün Denge):** Mikrometastatik odaktaki hücreler yavaşça bölünür; ancak yeni "
            "damarlanma (anjiyogenez) yetersiz olduğu için veya konak CTL/NK hücreleri bölünen hücreleri aynı hızda lize ettiği için kitle "
            "1 mm'yi aşamaz (**Proliferasyon Hızı = Apoptoz Hızı**).\n\n"
            "### Karakteristik Kanser Türleri ve Uyanma Tetikleyicileri\n"
            "- **En Tipik Kanserler:** **Östrojen Reseptörü Pozitif (ER+) Meme Karsinomu**, Kutanöz Malign Melanom, Berrak Hücreli Böbrek "
            "Karsinomu (RCC) ve Prostat Adenokarsinomu uzun süreli dormansiyle yıllar sonra nüks yapma eğilimindedir.\n"
            "- **Uyanmayı Tetikleyen Faktörler:** Şiddetli sistemik enfeksiyon veya cerrahi travma (nötrofil NET'lerinin salınımı), konak "
            "bağışıklığının yaşlanmayla zayıflaması (immünosenesans), kemik iliğinde osteoklastik kemik yıkımıyla matriksten serbest kalan "
            "TGF-beta ve IGF-1 uyuyan kök hücreleri aniden G0'dan çıkarıp fulminan metastatik büyümeyi ateşler.\n\n"
            "### Metastazın Klinik Yönetim İlkeleri ve Tedavi Rasyoneli\n"
            "TNM evreleme sisteminde uzak metastaz saptanması (**M1 durumu**) hastayı doğrudan **Evre IV (en ileri evre)** kategorisine sokar:\n"
            "- Metastatik hastalık varlığında lokal tedaviler (cerrahi, radyoterapi) primer kür sağlamaz; yalnızca palyatif amaçla veya "
            "soliter oligometastazlarda (örn. kolorektal Ca tek karaciğer metastazı) anlamlıdır.\n"
            "- Esas tedavi stratejisi daima **SİSTEMİK TEDAVİDİR**: Sitotoksik kemoterapi, hedefe yönelik tirozin kinaz inhibitörleri "
            "ve immün gözetimi yeniden canlandıran **İmmün Kontrol Noktası Blokajı (Anti-PD-1 / Anti-CTLA-4)** multimodal olarak uygulanır.\n\n"
            "🔴 **ÖNEMLİ:** Tümör dormansisinde hücreler G0 evresinde bölünmeyi durdurur; bu nedenle hücre siklusuna bağımlı klasik kemoterapi "
            "ve radyoterapiye tamamen dirençlidirler.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Primer tümörün cerrahi tedavisinden 10-15 yıl sonra kemik veya organlarda metastatik nüks yapabilen, uzun "
            "süreli tümör dormansisi ile en karakteristik malignite Östrojen Reseptörü Pozitif (ER+) Meme Karsinomudur."
        ),
        "content": (
            "### Tümör Dormansisi (Uyku Hali) Kavramı\n"
            "Onkolojik cerrahi ve kemoradyoterapi sonrası tümörden tamamen arındığı düşünülen hastalarda 5, 10, hatta 20 yıl sonra aniden "
            "viseral organ veya kemik metastazlarının belirmesi onkolojinin en çarpıcı gerçeklerinden biridir. Bu durum **Tümör Dormansisi "
            "(Tumor Dormancy)** kavramı ile açıklanır. Dormansi iki temel biyolojik formda gerçekleşir:\n"
            "1. **Hücresel Dormansi (G0/G1 Tutukluğu):** Uzak organ nişine yerleşen soliter kanser kök hücreleri mitozu tamamen durdurur, "
            "metabolizmalarını bazal seviyeye indirir ve hücre siklusunun **G0 fazında** adeta kış uykusuna yatar. Klasik sitotoksik "
            "kemoterapiler ve radyoterapi hızla bölünen hücreleri hedeflediği için, G0 fazındaki dorman hücrelere **asla etki edemez!**\n"
            "2. **Tümör Kütlesi Dormansisi (Anjiyogenik / İmmün Denge):** Mikrometastatik odaktaki hücreler yavaşça bölünür; ancak yeni "
            "damarlanma (anjiyogenez) yetersiz olduğu için veya konak CTL/NK hücreleri bölünen hücreleri aynı hızda lize ettiği için kitle "
            "1 mm'yi aşamaz (**Proliferasyon Hızı = Apoptoz Hızı**).\n\n"
            "### Karakteristik Kanser Türleri ve Uyanma Tetikleyicileri\n"
            "- **En Tipik Kanserler:** **Östrojen Reseptörü Pozitif (ER+) Meme Karsinomu**, Kutanöz Malign Melanom, Berrak Hücreli Böbrek "
            "Karsinomu (RCC) ve Prostat Adenokarsinomu uzun süreli dormansiyle yıllar sonra nüks yapma eğilimindedir.\n"
            "- **Uyanmayı Tetikleyen Faktörler:** Şiddetli sistemik enfeksiyon veya cerrahi travma (nötrofil NET'lerinin salınımı), konak "
            "bağışıklığının yaşlanmayla zayıflaması (immünosenesans), kemik iliğinde osteoklastik kemik yıkımıyla matriksten serbest kalan "
            "TGF-beta ve IGF-1 uyuyan kök hücreleri aniden G0'dan çıkarıp fulminan metastatik büyümeyi ateşler.\n\n"
            "### Metastazın Klinik Yönetim İlkeleri ve Tedavi Rasyoneli\n"
            "TNM evreleme sisteminde uzak metastaz saptanması (**M1 durumu**) hastayı doğrudan **Evre IV (en ileri evre)** kategorisine sokar:\n"
            "- Metastatik hastalık varlığında lokal tedaviler (cerrahi, radyoterapi) primer kür sağlamaz; yalnızca palyatif amaçla veya "
            "soliter oligometastazlarda (örn. kolorektal Ca tek karaciğer metastazı) anlamlıdır.\n"
            "- Esas tedavi stratejisi daima **SİSTEMİK TEDAVİDİR**: Sitotoksik kemoterapi, hedefe yönelik tirozin kinaz inhibitörleri "
            "ve immün gözetimi yeniden canlandıran **İmmün Kontrol Noktası Blokajı (Anti-PD-1 / Anti-CTLA-4)** multimodal olarak uygulanır.\n\n"
            "🔴 **ÖNEMLİ:** Tümör dormansisinde hücreler G0 evresinde bölünmeyi durdurur; bu nedenle hücre siklusuna bağımlı klasik kemoterapi "
            "ve radyoterapiye tamamen dirençlidirler.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Primer tümörün cerrahi tedavisinden 10-15 yıl sonra kemik veya organlarda metastatik nüks yapabilen, uzun "
            "süreli tümör dormansisi ile en karakteristik malignite Östrojen Reseptörü Pozitif (ER+) Meme Karsinomudur."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Hücresel dormansideki kanser kök hücreleri G0 fazında metabolik uykuda oldukları için kemoterapi ve radyoterapiye tamamen dirençlidir.",
            "🔵 **ÇIKMIŞ SORU:** Primer operasyondan 10-20 yıl sonra geç metastatik nüks yapabilen en tipik tümör grubu Östrojen Reseptörü Pozitif (ER+) Meme Karsinomudur.",
            "⚡ **KLİNİK EVRELEME:** Uzak organ metastazı (M1) daima Evre IV'tür ve tedavide lokal cerrahiden ziyade sistemik multimodal tedaviler (kemoterapi + immünoterapi) esastır."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Tümör kütlesi dormansisinde anjiyogenez yokluğu nedeniyle proliferasyon hızı apoptoz hızına eşittir ve kitle mikroskopik kalır.",
            "🔵 **ÇIKMIŞ SORU:** Sistemik inflamasyon, cerrahi travma ve kemik rezorpsiyonu dorman kanser hücrelerini uyandırarak fulminan nükse yol açabilir.",
            "⚡ **KLİNİK EVRELEME:** Berrak hücreli böbrek karsinomu ve melanom da 10 yıldan sonra geç metastaz yapabilen diğer tümörlerdir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Hücresel Dormansi (G0 Tutukluğu)",
                    "desc": "Kanser kök hücreleri G0 evresinde metabolik uykuya geçer ve hücre siklusuna bağımlı kemoterapiden kaçar.",
                    "isKey": True
                },
                {
                    "title": "ER+ Meme Kanseri ve Geç Nüks",
                    "desc": "Cerrahi rezeksiyondan 10-15 yıl sonra bile kemik iliğinde uyuyan hücrelerin uyanmasıyla nüks görülebilir.",
                    "isKey": True
                },
                {
                    "title": "Sistemik Multimodal Tedavi",
                    "desc": "Uzak metastaz evre IV demektir; tedavi kemoterapi, hedefe yönelik ajanlar ve immünoterapinin birlikteliğidir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Hücresel Dormansi vs Anjiyogenik / İmmün Kütle Dormansisi",
                "headers": ["Biyolojik Parametre", "Hücresel Dormansi (Soliter Hücre)", "Tümör Kütlesi Dormansisi (Mikrometastaz)"],
                "rows": [
                    ["Hücre Siklusu Evresi", "G0 evresinde tam bölünme tutukluğu", "Hücreler bölünür (S ve M fazına girer)"],
                    ["Kitle Boyutu", "Tek hücre veya birkaç hücrelik mikroniş", "Mikrometastatik nodül (1-2 mm)"],
                    ["Dormansi Nedeni", "İntrensek kinaz inhibisyonu, p27 artışı", "Yetersiz anjiyogenez veya CTL/NK immün dengesi"],
                    ["Kemoterapiye Duyarlılık", "Tamamen DİRENÇLİDİR (bölünmez)", "Kısmen duyarlıdır (ancak eradike edilemez)"],
                    ["Tipik Klinik Örnek", "Meme Ca kemik iliği mikrometastazı", "Tiroit papiller Ca mikroskopik akciğer odağı"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-24-01",
                "category": "Tümör Dormansisi",
                "front": "Hücresel dormansideki kanser hücrelerinin klasik sitotoksik kemoterapilerden hiç etkilenmemesinin sebebi nedir?",
                "hint": "Hücre siklusu evresi.",
                "back": "Hücrelerin bölünmeyi durdurup **G0 fazında metabolik uykuya** yatmış olmalarıdır; kemoterapiler yalnızca hızla bölünen hücreleri vurabilir.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide kemoterapi direncinin temel nedenlerinden birinin bu uyku hali olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-24-02",
                "category": "Klinik Onkoloji",
                "front": "Küratif cerrahiden 15 yıl sonra kemikte dormansi çıkışı geç nüks yapmasıyla meşhur olan karsinom hangisidir?",
                "hint": "Hormon reseptörü pozitif kadın kanseri.",
                "back": "**Östrojen Reseptörü Pozitif (ER+) Meme Karsinomu** (ayrıca malign melanom ve böbrek hücreli karsinom).",
                "facultyNote": "TUS Onkoloji sorularında '15 yıl sonra geç nüks' kalıbı ER+ meme kanserini sorgular."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-24",
            "question": "14 yıl önce erken evre ER-pozitif meme karsinomu nedeniyle meme koruyucu cerrahi ve adjuvan hormonal tedavi alan ve o tarihten bu yana remisyonda olan 66 yaşındaki bir kadın hastada, geçirdiği ağır pnömoni ve sepsis tablosundan 2 ay sonra sırt ağrısı gelişiyor. Çekilen MRG'de torakal vertebralarda litik metastatik lezyonlar saptanıyor. Bu klinik nüks tablosu ve 'Tümör Dormansisi' biyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Meme kanseri hücreleri vücutta 1 yıldan uzun süre asla canlı kalamaz; lezyonlar kesinlikle yeni bir primer multipl miyelomdur.",
                "B) Kanser hücreleri kemik iliği nişinde G0 fazında hücresel dormanside uykuya yatmıştır; sepsis sırasında salınan sistemik inflamatuar sitokinler dormansiyi bozarak hücreleri replikasyona sokmuştur.",
                "C) Dorman tümör hücreleri haftalık kemoterapi ile kolaylıkla yok edilebilir, çünkü metabolizmaları çok hızlıdır.",
                "D) Tümör dormansisi yalnızca primer santral sinir sistemi tümörlerinde görülen bir tablodur.",
                "E) ER-pozitif meme karsinomlarında geç nüks beklenmez; geç nüks yalnızca üçlü negatif tümörlerin özelliğidir."
            ],
            "answer": "B",
            "explanation": "Östrojen Reseptörü Pozitif (ER+) meme karsinomu, tümör dormansisinin ve geç metastatik nükslerin en klasik örneğidir. Primer cerrahi sonrası mikrometastatik kanser kök hücreleri kemik iliğinde G0 fazında canlı kalır (hücresel dormansi). Bölünmedikleri için kemoterapiden etkilenmezler. Ağır sepsis, cerrahi travma veya immünsüpresyon gibi şiddetli sistemik inflamatuar süreçler (nötrofil NET'leri, sitokinler) bu uyuyan kök hücreleri uyararak yıllar sonra fulminan metastatik nükslere yol açabilir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    }
]
