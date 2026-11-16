# -*- coding: utf-8 -*-
"""
Part 2: Efektör İmmün Yanıt ve Hücreler (Slayt 7 - 10)
Robbins & Kumar Basic Pathology 11. Baskı ve Prof. Dr. Hikmet Keleş Ders Notu temelinde.
"""

slides_part2 = [
    # SLIDE 7
    {
        "slideNumber": 7,
        "title": "Dendritik Hücreler ve Çapraz Sunum (Cross-Presentation)",
        "subtitle": "MHC Sınıf I ile eksojen antijen yüklenmesi ve CD8+ CTL'lerin lisanslanması",
        "badge": "Antijen Sunumu",
        "badgeColor": "teal",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Dendritik hücreler immün sistemin en yetenekli istihbaratçılarıdır. Kural olarak eksojen antijenler MHC-II ile sunulur; ancak dendritik hücreler tümör döküntülerini fagositozla alıp MHC-I'e aktarır. İşte CD8+ ordusunu savaşa sokan bu mucizevi olaya 'Çapraz Sunum' diyoruz.",
            "note": "Prof. Dr. Hikmet Keleş, çapraz sunum ve kostimülasyon (B7-CD28) eksikliğinde T hücresinin aktivasyon yerine anerjiye girdiğini amfide önemle vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Dendritik Hücrelerin Rolü ve Antijen Yakalama\n"
            "Antitümöral bağışıklık yanıtının orkestrasyonunda en kritik basamak, profesyonel antijen sunan hücrelerin (APC), "
            "özellikle konvansiyonel tip 1 dendritik hücrelerin (**cDC1**) tümör yatağında oynadığı roldür. Apoptoza veya nekroza "
            "uğrayan tümör hücrelerinden dökülen debrisler ve tümöral ekzozomlar dendritik hücrelerce fagositozla yakalanır. "
            "Aktive olan DC'ler dokudan ayrılarak lenfatik yolla tümörü drene eden **lenf noduna** göç ederler.\n\n"
            "### Çapraz Sunum (Cross-Presentation) Mekanizması\n"
            "Klasik kurala göre eksojen antijenler MHC-II ile CD4+ T hücrelerine, endojen antijenler ise MHC-I ile CD8+ T hücrelerine "
            "sunulur. Ancak karsinom hücreleri doğrudan lenf noduna gidip naif T hücrelerine sunum yapamaz. Burada dendritik hücrelerin "
            "hayati yeteneği devreye girer: **Çapraz Sunum (Cross-Presentation)**. Dendritik hücreler, fagositozla aldıkları eksojen "
            "tümör antijenlerini sitoplazmaya kaçırır, proteazomda oligopeptitlere böler, TAP ile ER'ye aktarır ve **MHC Sınıf I "
            "molekülüne yükler!** Bu sayede lenf nodundaki naif CD8+ T lenfositleri eksojen tümör antijenleriyle uyarılır ve tümöre "
            "özgü sitotoksik T hücresi (CTL) klonları patlayıcı şekilde genişler.\n\n"
            "### Kostimülasyon ve DC Lisanslanması\n"
            "TCR'nin MHC-I ile bağlanması (1. sinyal) tek başına yetersizdir; aktivasyon için **Kostimülasyon (2. sinyal)** şarttır. "
            "DC yüzeyindeki **B7-1 (CD80)** ve **B7-2 (CD86)** molekülleri, T hücresindeki **CD28** reseptörüne bağlanmalıdır. "
            "İkinci sinyal olmadan antijenle karşılaşan T hücresi aktive olamaz ve **Anerjiye (Anergy)** girer. Ayrıca CD4+ Th1 hücreleri "
            "CD40L ile DC üzerindeki CD40'ı uyararak dendritik hücreyi 'lisanslar' ve tam aktivasyon sağlar.\n\n"
            "🔴 **ÖNEMLİ:** Dendritik hücrelerin eksojen tümör antijenlerini MHC Sınıf I üzerinde naif CD8+ T hücrelerine sunması "
            "olayına 'Çapraz Sunum' (Cross-presentation) denir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Naif CD8+ CTL aktivasyonunda dendritik hücre yüzeyindeki B7-1/B7-2 molekülleri, T hücresindeki "
            "CD28 reseptörüne bağlanarak zorunlu kostimülatör sinyali sağlar."
        ),
        "content": (
            "### Dendritik Hücrelerin Rolü ve Antijen Yakalama\n"
            "Antitümöral bağışıklık yanıtının orkestrasyonunda en kritik basamak, profesyonel antijen sunan hücrelerin (APC), "
            "özellikle konvansiyonel tip 1 dendritik hücrelerin (**cDC1**) tümör yatağında oynadığı roldür. Apoptoza veya nekroza "
            "uğrayan tümör hücrelerinden dökülen debrisler ve tümöral ekzozomlar dendritik hücrelerce fagositozla yakalanır. "
            "Aktive olan DC'ler dokudan ayrılarak lenfatik yolla tümörü drene eden **lenf noduna** göç ederler.\n\n"
            "### Çapraz Sunum (Cross-Presentation) Mekanizması\n"
            "Klasik kurala göre eksojen antijenler MHC-II ile CD4+ T hücrelerine, endojen antijenler ise MHC-I ile CD8+ T hücrelerine "
            "sunulur. Ancak karsinom hücreleri doğrudan lenf noduna gidip naif T hücrelerine sunum yapamaz. Burada dendritik hücrelerin "
            "hayati yeteneği devreye girer: **Çapraz Sunum (Cross-Presentation)**. Dendritik hücreler, fagositozla aldıkları eksojen "
            "tümör antijenlerini sitoplazmaya kaçırır, proteazomda oligopeptitlere böler, TAP ile ER'ye aktarır ve **MHC Sınıf I "
            "molekülüne yükler!** Bu sayede lenf nodundaki naif CD8+ T lenfositleri eksojen tümör antijenleriyle uyarılır ve tümöre "
            "özgü sitotoksik T hücresi (CTL) klonları patlayıcı şekilde genişler.\n\n"
            "### Kostimülasyon ve DC Lisanslanması\n"
            "TCR'nin MHC-I ile bağlanması (1. sinyal) tek başına yetersizdir; aktivasyon için **Kostimülasyon (2. sinyal)** şarttır. "
            "DC yüzeyindeki **B7-1 (CD80)** ve **B7-2 (CD86)** molekülleri, T hücresindeki **CD28** reseptörüne bağlanmalıdır. "
            "İkinci sinyal olmadan antijenle karşılaşan T hücresi aktive olamaz ve **Anerjiye (Anergy)** girer. Ayrıca CD4+ Th1 hücreleri "
            "CD40L ile DC üzerindeki CD40'ı uyararak dendritik hücreyi 'lisanslar' ve tam aktivasyon sağlar.\n\n"
            "🔴 **ÖNEMLİ:** Dendritik hücrelerin eksojen tümör antijenlerini MHC Sınıf I üzerinde naif CD8+ T hücrelerine sunması "
            "olayına 'Çapraz Sunum' (Cross-presentation) denir.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Naif CD8+ CTL aktivasyonunda dendritik hücre yüzeyindeki B7-1/B7-2 molekülleri, T hücresindeki "
            "CD28 reseptörüne bağlanarak zorunlu kostimülatör sinyali sağlar."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Çapraz sunum, eksojen tümör antijenlerinin MHC Sınıf I molekülüne yüklenerek naif CD8+ T hücrelerine sunulmasıdır.",
            "🔵 **ÇIKMIŞ SORU:** T lenfosit aktivasyonunda zorunlu kostimülatör sinyali APC üzerindeki B7-1/B7-2 ile T hücresi üzerindeki CD28 reseptörünün etkileşimi sağlar.",
            "⚡ **İMMÜNOLOJİ:** Kostimülasyon (B7-CD28) olmaksızın antijen sunumu gerçekleşirse T lenfosit aktive olamaz ve klonal anerjiye (fonksiyonel felç) girer."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** cDC1 alt grubu, lenf noduna göç ederek tümör spesifik CD8+ CTL klonlarını genişleten primer hücredir.",
            "🔵 **ÇIKMIŞ SORU:** CD4+ T yardımcı hücrelerinin CD40L molekülü ile dendritik hücredeki CD40'ı uyarması 'lisanslama' sağlayarak CD8+ yanıtını kuvvetlendirir.",
            "⚡ **İMMÜNOLOJİ:** Çapraz sunumda eksojen antijenler endozomdan sitozole sızarak proteazom ve TAP bağımlı olarak işlenir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Çapraz Sunum (Cross-Presentation)",
                    "desc": "Eksojen tümör debrislerinin MHC-I ile naif CD8+ T lenfositlerine sunulmasını sağlayan özel mekanizmadır.",
                    "isKey": True
                },
                {
                    "title": "B7-CD28 Kostimülasyonu",
                    "desc": "Aktivasyonun 2. sinyalidir; yokluğunda T lenfosit proliferasyon yerine klonal anerjiye girer.",
                    "isKey": True
                },
                {
                    "title": "cDC1 ve CD40 Lisanslaması",
                    "desc": "Th1 hücrelerinin CD40L uyarısı dendritik hücreyi tam yetkin hale getirerek sitotoksik yanıtı ateşler.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Klasik Antijen Sunumu vs Çapraz Sunum (Cross-Presentation)",
                "headers": ["Özellik", "Klasik Endojen Yol", "Klasik Eksojen Yol", "Çapraz Sunum (Cross-Presentation)"],
                "rows": [
                    ["Antijen Kaynağı", "Hücre içi viral/tümöral protein", "Hücre dışı bakteri/toksin", "Hücre dışı tümör hücresi döküntüsü"],
                    ["Sunan Hücre Tipi", "Tüm çekirdekli somatik hücreler", "Profesyonel APC (DC, Makrofaj, B)", "Özelleşmiş Dendritik Hücreler (cDC1)"],
                    ["Kullanılan MHC Tipi", "MHC Sınıf I", "MHC Sınıf II", "MHC Sınıf I"],
                    ["Uarılan T Lenfosit", "CD8+ Sitotoksik T Lenfosit (CTL)", "CD4+ T Yardımcı (Th) Lenfosit", "Naif CD8+ Sitotoksik T Lenfosit (CTL)"],
                    ["Biyolojik Sonuç", "Hedef hücrenin doğrudan lizisi", "Sitokin salınımı ve antikor üretimi", "Antitümöral CTL klonal genişlemesi"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-07-01",
                "category": "Antijen Sunumu",
                "front": "Dendritik hücrelerin eksojen tümör antijenlerini MHC Sınıf I ile CD8+ T hücrelerine sunması sürecine ne ad verilir?",
                "hint": "Normal immünolojik kuralları aşan çapraz yol.",
                "back": "**Çapraz Sunum (Cross-Presentation)**. Tümöre özgü naif CD8+ CTL'lerin uyarılmasında vazgeçilmez temel mekanizmadır.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu kavramın immünolojinin en kritik keşiflerinden biri olduğunu vurgulamıştır."
            },
            {
                "id": "imm-fc-07-02",
                "category": "Kostimülasyon",
                "front": "Bir dendritik hücre tümör antijenini naif T hücresine B7-CD28 kostimülasyonu olmaksızın sunarsa ne olur?",
                "hint": "T hücresinin aktivasyon yerine girdiği fonksiyonel durum.",
                "back": "T lenfosit aktive olamaz ve **Klonal Anerjiye (Anergy)** girer; yani antijene karşı yanıtsız, felçli hale gelir.",
                "facultyNote": "Komite ve TUS sınavlarında 'Kostimülasyon eksikliğinde T hücresinin akıbeti nedir?' kalıbı klasik bir sorudur."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-07",
            "question": "Primer meme karsinomu gelişen bir hastanın lenf nodunda tümör antijenlerine karşı spesifik sitotoksik T lenfosit (CD8+ CTL) yanıtının başlatılabilmesi için dendritik hücrelerin gerçekleştirdiği moleküler ve hücresel mekanizma ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) Dendritik hücreler tümör döküntülerini yalnızca MHC Sınıf II ile sunar; CD8+ T hücreleri tümörü doğrudan tanıyamaz.",
                "B) Eksojen tümör antijenleri dendritik hücre tarafından sitoplazmaya kaçırılıp proteazomda işlenir ve MHC Sınıf I üzerinde naif CD8+ T lenfositlerine çapraz sunulur.",
                "C) Dendritik hücreler aktivasyon için B7 molekülünü baskılayarak T hücresindeki CTLA-4 reseptörünü uyarmak zorundadır.",
                "D) CD8+ T hücrelerinin aktivasyonunda kostimülasyona ihtiyaç yoktur; sadece TCR-MHC teması tam aktivasyon için yeterlidir.",
                "E) Çapraz sunum yalnızca eritrositler ve trombositler tarafından yürütülen non-spesifik bir filtrasyon sürecidir."
            ],
            "answer": "B",
            "explanation": "Tümör antijenlerine karşı CD8+ CTL yanıtının başlatılması, dendritik hücrelerin gerçekleştirdiği 'Çapraz Sunum' (Cross-presentation) mekanizmasına dayanır. Fagositozla alınan eksojen tümör proteinleri sitozole aktarılır, proteazomda parçalanır ve TAP aracılığıyla ER'de MHC Sınıf I molekülüne yüklenir. Dendritik hücre bu peptit-MHC-I kompleksini B7-CD28 kostimülasyonu eşliğinde naif CD8+ T hücrelerine sunarak sitotoksik klonların çoğalmasını sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 8
    {
        "slideNumber": 8,
        "title": "Sitotoksik T Lenfositler (CD8+ CTL): Birincil Efektör Güç",
        "subtitle": "Perforin-granzim B porları, Fas/FasL apoptozu ve immünolojik sinaps",
        "badge": "Efektör İmmünite",
        "badgeColor": "rose",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör hücresini infaz eden birincil cellat CD8+ CTL'dir. İmmünolojik sinaps kurulduğunda perforin hedef zarda silindirik borular açar; içeri dalan granzim B kaspazları keserek tümörü dakikalar içinde apoptoza gömer.",
            "note": "Prof. Dr. Hikmet Keleş, CTL'lerin perforin-granzim ve Fas-FasL mekanizmalarının apoptoz indüksiyonundaki adımlarının sınavların vazgeçilmezi olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### İmmünolojik Sinaps ve Hedef Tanıma\n"
            "Drenaj lenf nodunda aktive olup klonal genişleme geçiren **CD8+ Sitotoksik T Lenfositleri (CTL)**, dolaşım yoluyla tümör "
            "mikroçevresine sızarlar. CTL'ler tümör parankiminde neoplastik hücrelerin yüzeyindeki peptid-MHC Sınıf I komplekslerini "
            "TCR ve CD8 ko-reseptörleri ile yüksek afiniteyle tanır. Hücreler arasında LFA-1 / ICAM-1 integrinleriyle izole bir "
            "temas alanı kurulur; buna **İmmünolojik Sinaps** adı verilir. Bu sinaps, sitolitik granüllerin çevreye dağılmadan "
            "doğrudan hedef tümör hücresine iletilmesini sağlar.\n\n"
            "### İnfaz Mekanizması 1: Perforin ve Granzim B Yolağı\n"
            "İmmünolojik sinaps kurulduktan sonra CTL litik granüllerini temas boşluğuna ekzositozla salgılar:\n"
            "1. **Perforin:** Kalsiyum bağımlı polimerizasyonla tümör membranına yerleşir ve 15-20 nm çapında silindirik, hidrofilik "
            "transmembran gözenekler (porlar) açar.\n"
            "2. **Granzim B:** Perforin porlarından tümör sitoplazmasına girer. Granzim B bir serin proteazdır; doğrudan **pro-kaspaz 3 "
            "ve 7**'yi kesip aktive eder. Ayrıca pro-apoptotik **Bid** proteinini keserek tBid haline getirir. tBid mitokondriden sitokrom c "
            "salınımını tetikleyerek intrensek apoptozu başlatır. Böylece çift koldan apoptoz kaskadı dakikalar içinde tümörü yok eder.\n\n"
            "### İnfaz Mekanizması 2: Fas / FasL (CD95 / CD95L) Yolağı\n"
            "Aktive CTL yüzeyinde **Fas Ligand (FasL / CD95L)** taşır. Tümör yüzeyindeki **Fas (CD95)** ölüm reseptörüne bağlanır. "
            "FADD adaptör proteini aracılığıyla **Kaspaz-8 ve 10** aktive edilir; ekstrensek apoptoz kaskadı tümör nükleusunu parçalar.\n\n"
            "### Sitokin Üretimi ve Anjiyostazis\n"
            "CTL'ler doğrudan sitotoksisitenin yanı sıra yoğun **İnterferon-gama (IFN-γ)** ve **TNF-alfa** salgılar. IFN-γ, tümörde "
            "MHC-I ekspresyonunu artırır, makrofajları M1 yönüne sevk eder ve neoplastik anjiyogenezi baskılar.\n\n"
            "🔴 **ÖNEMLİ:** CD8+ CTL'lerin tümör öldürmesindeki majör mekanizma Perforin ile zarda por açılması ve Granzim B'nin pro-kaspaz 3 "
            "ile Bid'i aktive ederek apoptoz başlatmasıdır.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Sitotoksik T lenfositlerinin hedef hücre membranında polimerize olarak por açan ve granzimlerin içeri "
            "girmesini sağlayan granül bileşeni Perforindir."
        ),
        "content": (
            "### İmmünolojik Sinaps ve Hedef Tanıma\n"
            "Drenaj lenf nodunda aktive olup klonal genişleme geçiren **CD8+ Sitotoksik T Lenfositleri (CTL)**, dolaşım yoluyla tümör "
            "mikroçevresine sızarlar. CTL'ler tümör parankiminde neoplastik hücrelerin yüzeyindeki peptid-MHC Sınıf I komplekslerini "
            "TCR ve CD8 ko-reseptörleri ile yüksek afiniteyle tanır. Hücreler arasında LFA-1 / ICAM-1 integrinleriyle izole bir "
            "temas alanı kurulur; buna **İmmünolojik Sinaps** adı verilir. Bu sinaps, sitolitik granüllerin çevreye dağılmadan "
            "doğrudan hedef tümör hücresine iletilmesini sağlar.\n\n"
            "### İnfaz Mekanizması 1: Perforin ve Granzim B Yolağı\n"
            "İmmünolojik sinaps kurulduktan sonra CTL litik granüllerini temas boşluğuna ekzositozla salgılar:\n"
            "1. **Perforin:** Kalsiyum bağımlı polimerizasyonla tümör membranına yerleşir ve 15-20 nm çapında silindirik, hidrofilik "
            "transmembran gözenekler (porlar) açar.\n"
            "2. **Granzim B:** Perforin porlarından tümör sitoplazmasına girer. Granzim B bir serin proteazdır; doğrudan **pro-kaspaz 3 "
            "ve 7**'yi kesip aktive eder. Ayrıca pro-apoptotik **Bid** proteinini keserek tBid haline getirir. tBid mitokondriden sitokrom c "
            "salınımını tetikleyerek intrensek apoptozu başlatır. Böylece çift koldan apoptoz kaskadı dakikalar içinde tümörü yok eder.\n\n"
            "### İnfaz Mekanizması 2: Fas / FasL (CD95 / CD95L) Yolağı\n"
            "Aktive CTL yüzeyinde **Fas Ligand (FasL / CD95L)** taşır. Tümör yüzeyindeki **Fas (CD95)** ölüm reseptörüne bağlanır. "
            "FADD adaptör proteini aracılığıyla **Kaspaz-8 ve 10** aktive edilir; ekstrensek apoptoz kaskadı tümör nükleusunu parçalar.\n\n"
            "### Sitokin Üretimi ve Anjiyostazis\n"
            "CTL'ler doğrudan sitotoksisitenin yanı sıra yoğun **İnterferon-gama (IFN-γ)** ve **TNF-alfa** salgılar. IFN-γ, tümörde "
            "MHC-I ekspresyonunu artırır, makrofajları M1 yönüne sevk eder ve neoplastik anjiyogenezi baskılar.\n\n"
            "🔴 **ÖNEMLİ:** CD8+ CTL'lerin tümör öldürmesindeki majör mekanizma Perforin ile zarda por açılması ve Granzim B'nin pro-kaspaz 3 "
            "ile Bid'i aktive ederek apoptoz başlatmasıdır.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Sitotoksik T lenfositlerinin hedef hücre membranında polimerize olarak por açan ve granzimlerin içeri "
            "girmesini sağlayan granül bileşeni Perforindir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** Granzim B, perforin porlarından girerek pro-kaspaz 3'ü doğrudan keser ve Bid proteini üzerinden mitokondriyal sitokrom c salınımını tetikler.",
            "🔵 **ÇIKMIŞ SORU:** Hedef hücrede Fas (CD95) ölüm reseptörüne bağlanarak FADD üzerinden kaspaz-8 aktivasyonuyla apoptoz başlatan molekül FasL'dir.",
            "⚡ **EFEKTÖR SİTOKİN:** CTL kaynaklı İnterferon-gama (IFN-γ), tümör hücrelerinde MHC-I ekspresyonunu artırarak antijen sunumunu güçlendirir."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** İmmünolojik sinaps, sitolitik granüllerin hedef tümör hücresine sızıntısız iletilmesini sağlayan izole temas bölgesidir.",
            "🔵 **ÇIKMIŞ SORU:** CTL aracılı tümör lizisinde birincil efektör enzim Granzim B serin proteazıdır.",
            "⚡ **EFEKTÖR SİTOKİN:** CTL ve Th1 kaynaklı IFN-γ, makrofajları M1 fenotipine polarize eder ve antianjiyogenik etki gösterir."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Perforin ve Membran Porları",
                    "desc": "Kalsiyum bağımlı polimerizasyonla tümör hücresi zarına delikler açarak sitolitik enzim geçişini sağlar.",
                    "isKey": True
                },
                {
                    "title": "Granzim B ve Kaspaz Kaskadı",
                    "desc": "Pro-kaspaz 3/7'yi doğrudan keser, Bid'i aktive ederek mitokondriyal intrensek apoptozu ateşler.",
                    "isKey": True
                },
                {
                    "title": "Fas/FasL Ölüm Reseptörü Yolağı",
                    "desc": "CD95/CD95L etkileşimiyle FADD ve kaspaz-8 üzerinden ekstrensek apoptoz kaskadını çalıştırır.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "CD8+ CTL'lerin Tümör Öldürme Mekanizmaları Karşılaştırması",
                "headers": ["Mekanizma", "Anahtar Moleküller", "İntrasellüler Biyokimyasal Yolak", "Hücre Ölümü Tipi"],
                "rows": [
                    ["Perforin / Granzim B", "Perforin, Granzim B serin proteazı", "Pro-kaspaz 3 kesilmesi + Bid aktivasyonu ile sitokrom c salınımı", "Hızlı Apoptoz (İntrensek + Ekstrensek)"],
                    ["Fas / FasL Yolağı", "FasL (CD95L) - Fas (CD95 reseptörü)", "FADD adaptörü -> Pro-kaspaz 8 kesilmesi -> Kaspaz 3 aktivasyonu", "Ekstrensek Apoptoz"],
                    ["Sitolitik Sitokinler", "TNF-alfa, İnterferon-gama (IFN-γ)", "TNFR1 aktivasyonu, kaspaz-8, iNOS indüksiyonu ve anjiyostazis", "Apoptoz ve Büyüme Tutukluğu (Nekroptoz)"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-08-01",
                "category": "CTL Sitotoksisitesi",
                "front": "Granzim B hedef tümör hücresine girdiğinde hangi iki kritik proteini keserek apoptozu başlatır?",
                "hint": "Bir yürütücü kaspaz ve bir pro-apoptotik Bcl-2 üyesi.",
                "back": "**Pro-kaspaz 3'ü** doğrudan kesip aktive eder ve **Bid proteinini** keserek tBid haline getirip mitokondriden sitokrom c salınımını tetikler.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide Granzim B'nin çift koldan apoptoz başlattığını vurgulamıştır."
            },
            {
                "id": "imm-fc-08-02",
                "category": "Ölüm Reseptörleri",
                "front": "CTL yüzeyindeki FasL (CD95L) tümör hücresindeki Fas reseptörüne bağlandığında aktive olan ilk başlatıcı kaspaz hangisidir?",
                "hint": "Ekstrensek apoptotik yolun başlatıcı enzimi.",
                "back": "**Kaspaz-8** (ve kaspaz-10). FADD adaptör proteini aracılığıyla ölüm indükleyici sinyal kompleksi (DISC) kurularak aktive edilir.",
                "facultyNote": "TUS Patoloji ve Biyokimya sınavlarında apoptoz kaspaz sıralaması sıkça sorgulanır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-08",
            "question": "Sitotoksik CD8+ T lenfositlerin bir malign melanom hücresini immünolojik sinaps aracılığıyla tanıdıktan sonra hedef hücrede perforin ve granzim B salgılayarak apoptoz indükleme süreci ile ilgili aşağıdaki ifadelerden hangisi BİYOKİMYASAL VE PATOLOJİK AÇIDAN DOĞRUDUR?",
            "options": [
                "A) Perforin lizozom membranını eriterek hidrolazların serbest kalmasını sağlar, plazma zarına etki etmez.",
                "B) Granzim B bir serin proteazdır; doğrudan pro-kaspaz 3'ü keserek aktive eder ve Bid proteini üzerinden mitokondriyal apoptozu tetikler.",
                "C) CTL sitotoksisitesi hedef hücrede hücresel şişme ve membran yırtılmasıyla giden primer lizis (nekroz) tablosu oluşturur.",
                "D) FasL-Fas etkileşimi mitokondriden bağımsız olarak hücre siklusunu zorla G2 fazında dondurur.",
                "E) Sitotoksik T hücreleri tümör hücresini öldürürken asla sitokin salgılamaz, sadece fiziksel temasla çalışır."
            ],
            "answer": "B",
            "explanation": "Sitotoksik T lenfositlerin (CD8+ CTL) temel öldürme silahı perforin ve granzim B granülleridir. Perforin plazma membranında transmembran hidrofilik porlar açar. Granzim B bu porlardan sitoplazmaya girerek: 1) Doğrudan yürütücü pro-kaspaz 3'ü kesip aktive eder, 2) Pro-apoptotik Bcl-2 üyesi olan Bid proteinini keserek tBid haline getirir; tBid mitokondriden sitokrom c salınımını ve kaspaz-9 aktivasyonunu tetikler. Böylece hedef hücre hızla apoptoza gider.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 9
    {
        "slideNumber": 9,
        "title": "Doğal Katil (NK) Hücreler ve 'Kayıp Benlik' (Missing Self) Prensibi",
        "subtitle": "KIR/NKG2A inhibisyonu, NKG2D aktivasyonu ve ADCC (CD16) sitotoksisitesi",
        "badge": "Doğal Bağışıklık",
        "badgeColor": "indigo",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser hücresi kurnazdır; CTL'den kaçmak için MHC Sınıf I molekülünü yok eder. Ama bağışıklık sistemi daha kurnazdır! MHC-I'ini kaybeden hücreyi Doğal Katil (NK) hücreler 'Kayıp Benlik' kuralıyla anında yakalar ve infaz eder.",
            "note": "Prof. Dr. Hikmet Keleş, NK hücrelerinin aktivasyon-inhibisyon dengesinin ve MHC-I kaybının TUS'ta en sık sorulan immünoloji mekanizmalarından biri olduğunu belirtmiştir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Doğal Katil (NK) Hücrelerin Doğuştan Savunma Gücü\n"
            "Doğal Katil (Natural Killer - NK) hücreler, doğuştan gelen (innate) bağışıklık sisteminin büyük granüler lenfositleridir. "
            "RAG bağımlı somatik rekombinasyon geçirmezler; klonal antijen reseptörleri yoktur. Hücre yüzeyinde CD3 bulunmaz; "
            "karakteristik olarak **CD56** ve bir Fc reseptörü olan **CD16 (FcγRIIIa)** taşırlar. Ön duyarlanmaya ihtiyaç duymaksızın "
            "tümör hücrelerini hızla öldürebilirler.\n\n"
            "### 'Kayıp Benlik' (Missing-Self) ve Reseptör Dengesi\n"
            "NK hücresinin hedefi öldürüp öldürmeyeceği, inhibitör ve aktive edici reseptörlerin net dengesiyle kararlaştırılır:\n"
            "1. **İnhibitör Reseptörler (Fren):** NK hücreleri yüzeyinde **KIR (Killer Cell Immunoglobulin-like Receptors)** ve **CD94/NKG2A** "
            "taşır. Bu reseptörler normal hücrelerdeki **MHC Sınıf I** moleküllerine bağlanır. Bağlanma, ITIM motifleri üzerinden SHP-1 "
            "fosfatazını uyararak NK hücresine güçlü bir **'DUR / ÖLDÜRME'** sinyali iletir.\n"
            "2. **Missing-Self (Kayıp Benlik):** Tümör hücreleri, CD8+ CTL'lerden kaçmak için MHC Sınıf I'i down-regüle ettiğinde NK "
            "hücresinin inhibitör reseptörü bağlanacak MHC-I bulamaz; **fren boşa çıkar!**\n"
            "3. **Aktive Edici Reseptörler:** Tümörde DNA hasarı ve onkojenik stresle artan **MICA, MICB ve ULBP** stres ligandları, "
            "NK hücresindeki **NKG2D** aktive edici reseptörüne bağlanır. Fren kalktığı için aktive edici sinyal galip gelir; NK hücresi "
            "perforin/granzim salarak MHC-I kaybetmiş tümör hücresini hızla parçalar.\n\n"
            "### Antikor Aracılı Hücresel Sitotoksisite (ADCC)\n"
            "NK hücreleri ayrıca yüzeylerindeki **CD16 (FcγRIIIa)** reseptörüyle tümör yüzeyine bağlanmış IgG antikorlarının (Trastuzumab, "
            "Rituksimab) Fc kuyruğunu tanır. Bu bağlanma litik granüllerin boşalmasını tetikler (ADCC).\n\n"
            "🔴 **ÖNEMLİ:** Tümör hücresi CTL'lerden kaçmak için MHC Sınıf I'i kaybettiğinde, KIR inhibitör sinyali kesilir ve tümör "
            "'Missing Self' kuralıyla NK hücrelerince öldürülür.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Hedef hücrede MHC Sınıf I molekülünün bulunmaması durumunda aktive olan ve MICA/MICB stres ligandlarını "
            "NKG2D reseptörüyle tanıyıp tümörü öldüren hücreler Doğal Katil (NK) hücrelerdir."
        ),
        "content": (
            "### Doğal Katil (NK) Hücrelerin Doğuştan Savunma Gücü\n"
            "Doğal Katil (Natural Killer - NK) hücreler, doğuştan gelen (innate) bağışıklık sisteminin büyük granüler lenfositleridir. "
            "RAG bağımlı somatik rekombinasyon geçirmezler; klonal antijen reseptörleri yoktur. Hücre yüzeyinde CD3 bulunmaz; "
            "karakteristik olarak **CD56** ve bir Fc reseptörü olan **CD16 (FcγRIIIa)** taşırlar. Ön duyarlanmaya ihtiyaç duymaksızın "
            "tümör hücrelerini hızla öldürebilirler.\n\n"
            "### 'Kayıp Benlik' (Missing-Self) ve Reseptör Dengesi\n"
            "NK hücresinin hedefi öldürüp öldürmeyeceği, inhibitör ve aktive edici reseptörlerin net dengesiyle kararlaştırılır:\n"
            "1. **İnhibitör Reseptörler (Fren):** NK hücreleri yüzeyinde **KIR (Killer Cell Immunoglobulin-like Receptors)** ve **CD94/NKG2A** "
            "taşır. Bu reseptörler normal hücrelerdeki **MHC Sınıf I** moleküllerine bağlanır. Bağlanma, ITIM motifleri üzerinden SHP-1 "
            "fosfatazını uyararak NK hücresine güçlü bir **'DUR / ÖLDÜRME'** sinyali iletir.\n"
            "2. **Missing-Self (Kayıp Benlik):** Tümör hücreleri, CD8+ CTL'lerden kaçmak için MHC Sınıf I'i down-regüle ettiğinde NK "
            "hücresinin inhibitör reseptörü bağlanacak MHC-I bulamaz; **fren boşa çıkar!**\n"
            "3. **Aktive Edici Reseptörler:** Tümörde DNA hasarı ve onkojenik stresle artan **MICA, MICB ve ULBP** stres ligandları, "
            "NK hücresindeki **NKG2D** aktive edici reseptörüne bağlanır. Fren kalktığı için aktive edici sinyal galip gelir; NK hücresi "
            "perforin/granzim salarak MHC-I kaybetmiş tümör hücresini hızla parçalar.\n\n"
            "### Antikor Aracılı Hücresel Sitotoksisite (ADCC)\n"
            "NK hücreleri ayrıca yüzeylerindeki **CD16 (FcγRIIIa)** reseptörüyle tümör yüzeyine bağlanmış IgG antikorlarının (Trastuzumab, "
            "Rituksimab) Fc kuyruğunu tanır. Bu bağlanma litik granüllerin boşalmasını tetikler (ADCC).\n\n"
            "🔴 **ÖNEMLİ:** Tümör hücresi CTL'lerden kaçmak için MHC Sınıf I'i kaybettiğinde, KIR inhibitör sinyali kesilir ve tümör "
            "'Missing Self' kuralıyla NK hücrelerince öldürülür.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Hedef hücrede MHC Sınıf I molekülünün bulunmaması durumunda aktive olan ve MICA/MICB stres ligandlarını "
            "NKG2D reseptörüyle tanıyıp tümörü öldüren hücreler Doğal Katil (NK) hücrelerdir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** NK hücreleri yüzeylerindeki KIR reseptörleri normal hücredeki MHC-I'e bağlandığında inhibe olur; tümörde MHC-I kaybı (missing-self) lizisi tetikler.",
            "🔵 **ÇIKMIŞ SORU:** DNA hasarı stresi altındaki tümör hücrelerinde ekspresyonu artan MICA/MICB ligandları, NK hücrelerindeki NKG2D aktive edici reseptörüne bağlanır.",
            "⚡ **ADCC:** NK hücrelerindeki CD16 (FcγRIIIa) reseptörü tümöre bağlı IgG antikorlarının Fc kuyruğunu tanıyarak hedefin degranülasyonla öldürülmesini sağlar."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** NK hücreleri CD3 taşımaz; periferik kanda CD16 ve CD56 ekspresyonu ile identifiye edilirler.",
            "🔵 **ÇIKMIŞ SORU:** RAG gen rekombinasyonu ve timik seleksiyon gerektirmeksizin tümör hücresini doğrudan öldürebilen hücre grubu Doğal Katil (NK) hücrelerdir.",
            "⚡ **ADCC:** Trastuzumab ve Rituksimab gibi monoklonal antikorların in vivo antitümöral etkisinin önemli bir kısmı NK aracılı ADCC'ye dayanır."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "Missing-Self Prensibi",
                    "desc": "MHC Sınıf I ekspresyonunu kaybeden tümör hücrelerinde inhibitör KIR sinyali kesilir ve hücre lize edilir.",
                    "isKey": True
                },
                {
                    "title": "NKG2D ve Stres Ligandları",
                    "desc": "MICA ve MICB stres proteinleri NKG2D aktivatör reseptörünü uyararak litik degranülasyonu tetikler.",
                    "isKey": True
                },
                {
                    "title": "CD16 Aracılı ADCC",
                    "desc": "Hedefe bağlanan IgG antikorlarının Fc kuyruğunu tanıyan CD16, monoklonal antikor tedavilerinin temel aracıdır.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "Sitotoksik CD8+ T Lenfositler vs Doğal Katil (NK) Hücreler",
                "headers": ["Özellik", "CD8+ Sitotoksik T Lenfosit (CTL)", "Doğal Katil (NK) Hücresi"],
                "rows": [
                    ["Bağışıklık Kolu", "Edinsel (Adaptif) Bağışıklık", "Doğuştan Gelen (İnnate) Bağışıklık"],
                    ["Antijen Reseptörü", "Klonal TCR (TCR alfa/beta, CD3+)", "Klonal reseptör YOK (Germline KIR, NKG2D)"],
                    ["Önceden Duyarlanma", "Zorunlu (Lenf nodunda DC ile aktivasyon)", "GEREKMEZ (Hemen öldürmeye hazır)"],
                    ["MHC Sınıf I ile İlişki", "MHC-I VARLIĞINDA uyarılır ve öldürür", "MHC-I VARLIĞINDA İNHİBE OLUR; YOKLUĞUNDA öldürür"],
                    ["Öldürme Medyatörleri", "Perforin, Granzim B, FasL, IFN-gama", "Perforin, Granzim B, FasL, TRAIL, IFN-gama"],
                    ["Karakteristik Belirteç", "CD3+, CD8+", "CD3-, CD56+, CD16+"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-09-01",
                "category": "NK Biyolojisi",
                "front": "Tümör hücresinin MHC Sınıf I molekülünü kaybetmesi CTL ve NK hücrelerini sırasıyla nasıl etkiler?",
                "hint": "Biri tanıyamazken diğeri freni kalktığı için saldırır.",
                "back": "CD8+ CTL'ler tümörü **tanıyamaz ve kaçışa uğrar**; ancak NK hücreleri inhibitör KIR sinyali kesildiği için **Missing-Self** mekanizmasıyla uyarılır ve tümörü öldürür.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide bu karşıtlığın immün dengenin en mükemmel örneği olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-09-02",
                "category": "NK Reseptörleri",
                "front": "NK hücrelerinin yüzeyindeki CD16 reseptörünün immünolojik fonksiyonu nedir?",
                "hint": "Monoklonal antikor tedavileriyle bağlantılı sitotoksisite.",
                "back": "Düşük afiniteli IgG Fc reseptörüdür (FcγRIIIa); antikor kaplı tümör hücrelerini tanıyarak **Antikor Aracılı Hücresel Sitotoksisiteyi (ADCC)** başlatır.",
                "facultyNote": "Trastuzumab ve Rituksimab mekanizma sorularında ADCC ve CD16 daima seçeneklerdedir."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-09",
            "question": "Bir akciğer karsinomu hücresinde Beta-2 mikroglobulin gen delesyonu sonucu hücre yüzeyinde Majör Histokompatibilite Kompleksi Sınıf I (MHC-I) ekspresyonunun tamamen kaybolduğu saptanıyor. Bu hücresel değişiklik sonrasında hastanın bağışıklık hücrelerinin tümöre vereceği yanıt ile ilgili hangisi DOĞRUDUR?",
            "options": [
                "A) CD8+ CTL'ler tümör hücresini daha kolay tanır ve perforin salınımını artırır.",
                "B) Tümör hücresi NK hücrelerinin inhibitör KIR reseptörlerini uyararak doğal katil lizisinden tamamen kurtulur.",
                "C) CD8+ CTL'lerin tanıma yeteneği kaybolurken; NK hücreleri üzerindeki inhibitör sinyal kalkar ('Missing-Self') ve tümör hücresi NK hücrelerince hedef alınır.",
                "D) Dendritik hücreler tümör hücresini doğrudan eritrosite dönüştürerek dalakta fagositozunu sağlar.",
                "E) MHC-I kaybı yalnızca B lenfositlerinin plazma hücresine dönüşmesini engeller, sitotoksisiteyi etkilemez."
            ],
            "answer": "C",
            "explanation": "MHC Sınıf I ekspresyonunun kaybı, tümör hücresini CD8+ CTL'lerin tanımasından kurtarır (immün kaçış). Ancak organizmanın bu kaçışa karşı geliştirdiği denge mekanizması Doğal Katil (NK) hücrelerdir. NK hücrelerinin yüzeyindeki KIR inhibitör reseptörleri normalde MHC-I'e bağlanarak NK hücresini frenler. MHC-I kaybolduğunda fren kalkar ('Missing-Self' prensibi); tümör hücresindeki stres molekülleri (MICA/B) NKG2D'yi uyararak NK hücresinin tümörü hızla parçalamasını sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    },

    # SLIDE 10
    {
        "slideNumber": 10,
        "title": "Makrofaj Polarizasyonu ve Tümör İlişkili Makrofajlar (TAM)",
        "subtitle": "M1 antitümöral fagositler vs M2 pro-tümöral anjiyogenik/immünsüpresif stroma",
        "badge": "Makrofaj Biyolojisi",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Makrofaj tümör mikroçevresinde iki yüzlü bir aktördür. Th1 sitokinleriyle uyarılan M1 makrofaj neoplaziyi yer bitirir; ama tümörün manipüle ettiği M2 makrofaj (TAM), VEGF salıp damar yapar, MMP salıp yolları açar ve tümörü besler!",
            "note": "Prof. Dr. Hikmet Keleş, solid tümörlerde M2 Tümör İlişkili Makrofaj (TAM) yoğunluğunun bağımsız kötü prognoz belirteci olduğunu amfide defalarca vurgulamıştır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": (
            "### Monositlerin Tümör Yatağına Göçü ve TAM Oluşumu\n"
            "Tümör dokusu ve stroma tarafından salgılanan **CCL2 (MCP-1)** ve **CSF-1 (M-CSF)** kemokinleri, kandaki monositleri tümör "
            "yatağına çeker. Buraya yerleşen hücrelere **Tümör İlişkili Makrofajlar (TAM)** denir. Makrofajlar mikroçevredeki yerel "
            "uyarılara göre iki zıt fenotipe polarize olurlar: **M1 (Klasik Aktivasyon)** ve **M2 (Alternatif Aktivasyon)**.\n\n"
            "### M1 Polarizasyonu: Klasik Antitümöral Aktivasyon\n"
            "M1 makrofajlar, Th1 kaynaklı **İnterferon-gama (IFN-γ)**, LPS veya TNF-alfa ile indüklenir:\n"
            "- İndüklenebilir Nitrik Oksit Sentaz (**iNOS**) enzimiyle L-arjininden sitotoksik **Nitrik Oksit (NO)** ve ROS üretirler.\n"
            "- NO ve serbest radikaller tümör hücresini doğrudan tahrip eder; ayrıca salgıladıkları **IL-12 ve TNF-alfa** ile CTL ve Th1 "
            "yanıtlarını kuvvetlendirirler. M1 infiltrasyonu güçlü bir antitümöral savunma yürütür ve iyi prognozla birliktedir.\n\n"
            "### M2 Polarizasyonu: Protümöral İşbirliği (TAM)\n"
            "Tümör mikroçevresindeki Th2 sitokinleri (**IL-4, IL-13**), **TGF-beta** ve **IL-10** makrofajları hızla **M2 fenotipine (TAM)** dönüştürür:\n"
            "1. **İmmünosüpresyon:** iNOS yerine **Arjinaz-1 (Arg-1)** eksprese ederek L-arjinini tüketirler; T lenfositlerin TCR zeta zinciri "
            "bozulur ve T hücreleri felç olur. Yüksek **IL-10 ve TGF-beta** ile CTL ve NK hücrelerini baskılarlar.\n"
            "2. **Anjiyogenez İndüksiyonu:** Yoğun **VEGF** ve bFGF salarak tümör içine yeni kılcal damarların filizlenmesini tetiklerler.\n"
            "3. **İnvazyon ve Metastaz Kolaylığı:** **Matriks Metalloproteinazlar (MMP-2, MMP-9)** salgılayarak bazal membranı eritirler; "
            "tümör hücrelerinin damar lümenine girmesine (intravazasyon) aracılık ederler. Bu nedenle solid tümörlerde yoğun M2 TAM "
            "infiltrasyonu bağımsız bir **KÖTÜ PROGNOZ** kriteridir.\n\n"
            "🔴 **ÖNEMLİ:** M1 makrofajlar iNOS ve NO ile antitümöral etki gösterirken; M2 makrofajlar (TAM) VEGF salarak anjiyogenezi, "
            "MMP salarak metastazı tetikler ve IL-10/TGF-beta ile immün sistemi felç eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Solid tümörlerde tümör stromasında yoğun M2 fenotipinde Tümör İlişkili Makrofaj (TAM) saptanması, "
            "anjiyogenez artışı ve metastaz kolaylaşması nedeniyle bağımsız bir KÖTÜ PROGNOZ göstergesidir."
        ),
        "content": (
            "### Monositlerin Tümör Yatağına Göçü ve TAM Oluşumu\n"
            "Tümör dokusu ve stroma tarafından salgılanan **CCL2 (MCP-1)** ve **CSF-1 (M-CSF)** kemokinleri, kandaki monositleri tümör "
            "yatağına çeker. Buraya yerleşen hücrelere **Tümör İlişkili Makrofajlar (TAM)** denir. Makrofajlar mikroçevredeki yerel "
            "uyarılara göre iki zıt fenotipe polarize olurlar: **M1 (Klasik Aktivasyon)** ve **M2 (Alternatif Aktivasyon)**.\n\n"
            "### M1 Polarizasyonu: Klasik Antitümöral Aktivasyon\n"
            "M1 makrofajlar, Th1 kaynaklı **İnterferon-gama (IFN-γ)**, LPS veya TNF-alfa ile indüklenir:\n"
            "- İndüklenebilir Nitrik Oksit Sentaz (**iNOS**) enzimiyle L-arjininden sitotoksik **Nitrik Oksit (NO)** ve ROS üretirler.\n"
            "- NO ve serbest radikaller tümör hücresini doğrudan tahrip eder; ayrıca salgıladıkları **IL-12 ve TNF-alfa** ile CTL ve Th1 "
            "yanıtlarını kuvvetlendirirler. M1 infiltrasyonu güçlü bir antitümöral savunma yürütür ve iyi prognozla birliktedir.\n\n"
            "### M2 Polarizasyonu: Protümöral İşbirliği (TAM)\n"
            "Tümör mikroçevresindeki Th2 sitokinleri (**IL-4, IL-13**), **TGF-beta** ve **IL-10** makrofajları hızla **M2 fenotipine (TAM)** dönüştürür:\n"
            "1. **İmmünosüpresyon:** iNOS yerine **Arjinaz-1 (Arg-1)** eksprese ederek L-arjinini tüketirler; T lenfositlerin TCR zeta zinciri "
            "bozulur ve T hücreleri felç olur. Yüksek **IL-10 ve TGF-beta** ile CTL ve NK hücrelerini baskılarlar.\n"
            "2. **Anjiyogenez İndüksiyonu:** Yoğun **VEGF** ve bFGF salarak tümör içine yeni kılcal damarların filizlenmesini tetiklerler.\n"
            "3. **İnvazyon ve Metastaz Kolaylığı:** **Matriks Metalloproteinazlar (MMP-2, MMP-9)** salgılayarak bazal membranı eritirler; "
            "tümör hücrelerinin damar lümenine girmesine (intravazasyon) aracılık ederler. Bu nedenle solid tümörlerde yoğun M2 TAM "
            "infiltrasyonu bağımsız bir **KÖTÜ PROGNOZ** kriteridir.\n\n"
            "🔴 **ÖNEMLİ:** M1 makrofajlar iNOS ve NO ile antitümöral etki gösterirken; M2 makrofajlar (TAM) VEGF salarak anjiyogenezi, "
            "MMP salarak metastazı tetikler ve IL-10/TGF-beta ile immün sistemi felç eder.\n\n"
            "🔵 **ÇIKMIŞ SORU:** Solid tümörlerde tümör stromasında yoğun M2 fenotipinde Tümör İlişkili Makrofaj (TAM) saptanması, "
            "anjiyogenez artışı ve metastaz kolaylaşması nedeniyle bağımsız bir KÖTÜ PROGNOZ göstergesidir."
        ),
        "spotPearls": [
            "🔴 **ÖNEMLİ:** M2 makrofajlar (TAM) VEGF salarak anjiyogenezi, MMP-2 ve MMP-9 salarak metastazı uyarır ve tümör büyümesine hizmet eder.",
            "🔵 **ÇIKMIŞ SORU:** L-arjinini kullanarak nitrik oksit (NO) üreten ve tümör hücresini öldüren klasik aktive makrofaj alt tipi M1 Makrofajlardır.",
            "⚡ **PROGNOZ:** Tümör parankiminde M1 infiltrasyonu iyi prognozla, M2 TAM infiltrasyonu ise agresif metastatik seyir ve kötü prognozla birliktedir."
        ],
        "spots": [
            "🔴 **ÖNEMLİ:** Th1 sitokini IFN-γ makrofajı M1'e yönlendirirken; Th2 sitokinleri (IL-4, IL-13) ve TGF-beta M2 polarizasyonu sağlar.",
            "🔵 **ÇIKMIŞ SORU:** Tümör dokusuna monositleri çeken en önemli kemokinler CCL2 (MCP-1) ve CSF-1'dir.",
            "⚡ **PROGNOZ:** M2 makrofajlardaki Arjinaz-1 (Arg-1) enzimi arjinini tüketerek T lenfositlerinin TCR zeta zincirini bozar."
        ],
        "coreContent": {
            "keyBullets": [
                {
                    "title": "M1 Klasik Aktivasyon",
                    "desc": "IFN-γ uyarısıyla iNOS, NO, ROS ve IL-12 üreterek tümörü tahrip eden anti-tümöral fenotiptir.",
                    "isKey": True
                },
                {
                    "title": "M2 Alternatif Aktivasyon (TAM)",
                    "desc": "IL-4/TGF-beta etkisiyle Arg-1, VEGF ve MMP üreterek tümörün büyümesini ve yayılımını besler.",
                    "isKey": True
                },
                {
                    "title": "Klinik Prognostik Değer",
                    "desc": "Tümör stromasındaki yüksek M2/TAM oranı anjiyogenezi hızlandırdığı için bağımsız kötü prognoz kriteridir.",
                    "isKey": True
                }
            ],
            "table": {
                "title": "M1 vs M2 Tümör İlişkili Makrofaj (TAM) Karşılaştırması",
                "headers": ["Özellik", "M1 Makrofaj (Klasik Aktivasyon)", "M2 Makrofaj (Alternatif Aktivasyon / TAM)"],
                "rows": [
                    ["İndükleyici Sitokinler", "İnterferon-gama (IFN-γ), LPS, TNF-alfa", "IL-4, IL-13, TGF-beta, IL-10, PGE2"],
                    ["Arjinin Metabolizması", "iNOS aktivasyonu -> Nitrik Oksit (NO) üretimi", "Arjinaz-1 (Arg-1) -> Ornitin ve poliamin üretimi"],
                    ["Efektör Medyatörler", "ROS, NO, TNF-alfa, IL-12", "VEGF, bFGF, TGF-beta, IL-10, MMP-2, MMP-9"],
                    ["Tümör Üzerine Etkisi", "Sitotoksik, tümör öldürücü (ANTİ-TÜMÖRAL)", "Anjiyojenik, invaziv, immünsüpresif (PRO-TÜMÖRAL)"],
                    ["T Hücreleri ile Etkileşim", "Th1 ve CTL aktivasyonunu güçlendirir", "T hücresini felç eder, Treg hücrelerini çeker"],
                    ["Klinik Prognostik Etki", "Yüksek oranda İYİ PROGNOZ", "Yüksek oranda KÖTÜ PROGNOZ"]
                ]
            }
        },
        "flashcards": [
            {
                "id": "imm-fc-10-01",
                "category": "Makrofaj Polarizasyonu",
                "front": "M1 ve M2 makrofajların L-arjinin aminoasidini metabolize ederken kullandıkları enzimler ve ürünleri nelerdir?",
                "hint": "Biri tümörü öldüren gaz, diğeri dokuyu besleyen poliamin üretir.",
                "back": "**M1 makrofajlar iNOS** kullanarak sitotoksik **Nitrik Oksit (NO)** üretir; **M2 makrofajlar Arjinaz-1 (Arg-1)** kullanarak ornitin üretir ve T hücrelerini arjininsiz bırakır.",
                "facultyNote": "Prof. Dr. Hikmet Keleş amfide iNOS vs Arg-1 ayrımının biyokimya ve patolojide çok sevilen bir soru olduğunu belirtmiştir."
            },
            {
                "id": "imm-fc-10-02",
                "category": "Tümör Mikroçevresi",
                "front": "Tümör İlişkili Makrofajların (M2 TAM) kanserin büyümesi ve yayılmasına yaptığı 3 temel katkı nedir?",
                "hint": "Damar yapımı, matriks yıkımı ve immün felç.",
                "back": "1) **VEGF salarak anjiyogenez**, 2) **MMP-2/9 salarak matriks invazyonu ve metastaz**, 3) **IL-10 ve TGF-beta ile T hücre baskılanması**.",
                "facultyNote": "Solid organ tümörlerinde TAM yoğunluğu metastaz riski ile doğrudan orantılıdır."
            }
        ],
        "practiceQuestion": {
            "id": "imm-pq-10",
            "question": "İnvaziv duktal meme karsinomu tanısı alan bir hastanın mastektomi materyali immünohistokimyasal analizinde, tümör stromasında yoğun CD163 ve CD206 pozitif M2 fenotipinde Tümör İlişkili Makrofaj (TAM) infiltrasyonu saptanıyor. Bu makrofaj popülasyonunun tümör mikroçevresindeki biyolojik aktiviteleri ve prognoz ile ilişkisi hakkında hangisi DOĞRUDUR?",
            "options": [
                "A) iNOS aracılığıyla bol miktarda nitrik oksit sentezleyerek tümör hücrelerini apoptoza sokarlar ve prognozu düzeltirler.",
                "B) IL-12 salgılayarak naif T lenfositlerini Th1 yönünde polarize edip tümör rejeksiyonunu sağlarlar.",
                "C) VEGF salarak anjiyogenezi uyarır, matriks metalloproteinazlar salarak invazyonu kolaylaştırır ve kötü prognozla ilişkilidirler.",
                "D) Tümör hücrelerindeki E-kaderin ekspresyonunu artırarak metastatik yayılımı tamamen durdururlar.",
                "E) Yalnızca viral enfeksiyonlarda aktive olurlar, primer epiteliyal meme tümörlerinde fonksiyonları yoktur."
            ],
            "answer": "C",
            "explanation": "M2 fenotipindeki Tümör İlişkili Makrofajlar (TAM - CD163+, CD206+), alternatif yoldan aktive olmuş hücrelerdir. M1 makrofajların aksine anti-tümöral değil PRO-TÜMÖRAL çalışırlar. Tümör mikroçevresinde VEGF salgılayarak yeni tümör damarlarının oluşmasını (anjiyogenez) indükler, MMP-2 ve MMP-9 salgılayarak ekstrasellüler matriksi eritip invazyon ve metastazı kolaylaştırır, IL-10 ve TGF-beta salarak sitotoksik T hücrelerini baskılarlar. Bu nedenle solid tümörlerde yoğun M2 TAM varlığı bağımsız bir KÖTÜ PROGNOZ kriteridir.",
            "isPracticeQuestion": True,
            "deckId": "learn-tumor-immunolojisi-metastaz",
            "discipline": "Tıbbi Patoloji"
        },
        "relatedQuestions": []
    }
]
