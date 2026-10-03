# -*- coding: utf-8 -*-
"""
scripts/ileri_tumor_genetigi/part4_slides.py
Slides 19 to 24 for 'learn-ileri-tumor-genetigi-metabolizmasi'
"""

slides_part4 = [
    {
        "slideNumber": 19,
        "title": "IDH Mutasyonlarının Klinik Spektrumu ve Hedefe Yönelik İnhibitörler",
        "subtitle": "DSÖ MSS sınıflaması, AML, kolanjiyokarsinom ve İvosidenib/Enasidenib ile diferansiyasyon tedavisi.",
        "badge": "Hassas Onkoloji",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "2021 DSÖ Beyin Tümörleri sınıflaması patolojide bir devrim yaptı: Artık glioblastom tanısı koyabilmek için tümörün IDH-yabani tip olması şarttır! IDH mutant gliomlar bambaşka bir antitedir, gençlerde görülür ve prognozu çok daha iyidir. Üstelik artık mutant IDH inhibitörlerimiz var!",
            "note": "İvosidenib mutant IDH1'i, Enasidenib ise mutant IDH2'yi hedefler. Vorasidenib kan-beyin bariyerini geçerek düşük dereceli gliomlarda sağkalımı uzatır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### IDH Mutasyonlarının Klinik Patolojisi ve Terapötik Devrim
IDH1 ve IDH2 mutasyonları modern onkolojide hem tanısal/prognostik bir biyobelirteç hem de doğrudan hedeflenebilen bir terapötik kırılganlıktır:

1. **Santral Sinir Sistemi Gliomları (DSÖ Sınıflamasının Temeli):**
   - 2021 DSÖ Merkezi Sinir Sistemi Tümörleri Sınıflaması, erişkin tipi diffüz gliomları moleküler temelde baştan tanımlamıştır:
     - **Astrositom, IDH-mutant:** Tipik olarak genç erişkinlerde (30-40 yaş) görülür, TP53 ve ATRX mutasyonları eşlik eder.
     - **Oligodendrogliom, IDH-mutant ve 1p/19q ko-delesyonlu:** Karakteristik bal peteği/kızarmış yumurta görünümüne ve kemosensitiviteye sahiptir.
     - **Glioblastom (GBM):** Artık tanımı gereği **IDH-yabani tip (wild-type)** agresif bir tümördür.
   - IDH-mutant gliomlar, IDH-yabani tip tümörlere kıyasla belirgin olarak daha uzun sağkalım ve iyi prognoz sergiler.

2. **Akut Miyeloid Lösemi (AML):**
   - Erişkin de novo AML vakalarının yaklaşık %20'sinde IDH1 (R132) veya IDH2 (R140/R172) mutasyonu saptanır.
   - İntrasellüler 2-HG birikimi miyeloblastların granülosite/monosite olgunlaşmasını kilitler.

3. **Diğer Maligniteler:**
   - İntrahepatik kolanjiyokarsinomların %15-20'sinde IDH1 mutasyonu görülür. Kıkırdak tümörlerinde (kondrosarkom, Ollier hastalığı ve Maffucci sendromu) IDH1/2 mutasyonları temel sürücüdür.

Hedefe Yönelik Tedavi (Precision Differentiation Therapy):
Geleneksel kemoterapiler hücreleri DNA hasarıyla öldürmeyi amaçlarken, IDH inhibitörleri hücreyi öldürmez; **farklılaşmasını sağlar**:
- **İvosidenib (AG-120):** Mutant IDH1 enziminin allosterik inhibitörüdür. AML ve kolanjiyokarsinomda onaylıdır.
- **Enasidenib (AG-221):** Mutant IDH2 enzim inhibitörüdür. Relaps/refrakter AML'de kullanılır.
- **Vorasidenib:** Kan-beyin bariyerini yüksek oranda geçen çift IDH1/IDH2 inhibitörüdür; rezidüel düşük dereceli gliomlarda tümör ilerlemesini dramatik olarak durdurur.
- **Etki Şekli:** İlaçlar 2-HG sentezini sıfırlar; TET2 üzerindeki baskı kalkar, DNA hipermetilasyonu çözülür. Kilitlenen lösemi blastları matür nötrofillere farklılaşarak apoptozla temizlenir.

> 🔴 **ÖNEMLİ:** Güncel DSÖ kriterlerine göre difüz bir gliomda IDH mutasyonu saptanması, hastanın IDH-yabani tip primer glioblastomlara kıyasla **çok daha iyi bir prognoza sahip olduğunu** gösterir.

> 🔵 **ÇIKMIŞ SORU:** Düşük ve orta dereceli diffüz gliomlarda ve AML'de saptanan, hücresel diferansiyasyonu engelleyen IDH1 mutasyonunu hedefleyerek 2-HG üretimini durduran hedefe yönelik ajan **İvosidenib**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: 2021 DSÖ MSS sınıflamasına göre Glioblastom tanısı için tümörün **IDH-yabani tip** olması zorunludur; IDH mutant gliomlar iyi prognozludur.",
            "🔵 ÇIKMIŞ SORU: Mutant IDH inhibitörleri (**İvosidenib ve Enasidenib**), 2-HG üretimini sıfırlayarak hücresel diferansiyasyon bloğunu çözer.",
            "⚡ Oligodendrogliom tanısı için **IDH mutasyonu + 1p/19q tam ko-delesyonu** birlikteliği şarttır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Gliom Sınıflaması", "text": "IDH-mutant astrositom ve oligodendrogliom; IDH-yabani tip glioblastom."},
                {"label": "AML ve Kolanjiyo Ca", "text": "Hematopoetik diferansiyasyon bloğu ve safra yolu karsinomunda IDH hedefi."},
                {"label": "Hedefe Yönelik İlaçlar", "text": "İvosidenib (IDH1), Enasidenib (IDH2), Vorasidenib (çift etkili beyin geçişli)."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-19-1",
                "front": "2021 DSÖ sınıflamasında erişkin tipi diffüz astrositom ile glioblastomu ayıran en temel moleküler belirteç nedir?",
                "back": "IDH mutasyon durumudur; glioblastom tanısı için tümör IDH-yabani tip olmalıdır. IDH-mutant olanlar astrositom kabul edilir.",
                "facultyNote": "Moleküler nöropatolojinin en güncel ve en çok sorulan kuralıdır."
            },
            {
                "id": "itg-fc-19-2",
                "front": "İvosidenib ve Enasidenib gibi mutant IDH inhibitörlerinin temel antitümöral etki mekanizması nedir?",
                "back": "2-HG düzeylerini düşürerek TET2 enzimini serbest bırakmak ve lösemi/gliom hücrelerinin diferansiyasyonunu sağlamaktır.",
                "facultyNote": "Sitotoksik değil, diferansiyasyon indükleyici tedavidir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-19",
            "question": "Kırk yaşında bir erkek hastaya yapılan kraniyotomi sonrası temporal lob kitlesi patolojisinde infiltratif astrositer tümör saptanmıştır. Moleküler analizde tümör hücrelerinde IDH1 R132H mutasyonu pozitif, 1p/19q ko-delesyonu ise negatif bulunmuştur. Bu hastanın patolojik sınıflaması ve klinik prognozu ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Tümör IDH-yabani tip klasik primer glioblastom olup prognozu son derece kötüdür",
                "B) Tümör oligodendrogliom olup 1p/19q kaybı olmadan da bu tanı kesinleşir",
                "C) Tümör IDH-mutant astrositomdur ve IDH-yabani tip glioblastomlara kıyasla belirgin şekilde daha iyi prognoza sahiptir",
                "D) IDH mutasyonu tümörde TET2'nin aşırı çalışarak küresel hipometilasyon yapmasına yol açmıştır",
                "E) Bu hastada hedefe yönelik anti-IDH tedavisi olarak Enasidenib tek seçenektir"
            ],
            "answer": "C",
            "explanation": "IDH1 mutasyonu pozitif ve 1p/19q ko-delesyonu negatif olan diffüz gliomlar güncel sınıflamada 'Astrositom, IDH-mutant' olarak adlandırılır. Bu hastalar IDH-yabani tip glioblastom olgularına göre belirgin olarak daha uzun sağkalım ve iyi prognoz gösterirler.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 20,
        "title": "Hücresel Otofaji: Kanserde İki Ucu Keskin Kılıç (Dual Role)",
        "subtitle": "Beclin-1 ve LC3 makinesi, pre-malign koruma vs tümör sağkalımı ve tedavi direnci.",
        "badge": "Hücresel Uyum",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Otofaji hücrenin kendi kendini yemesidir (self-eating). Erken evrede hasarlı mitokondrileri temizleyerek kanseri engeller. Ancak kanser oluştuktan sonra aynı otofaji, kemoterapi altında aç kalan tümör hücresine organellerini yakıt yaptırarak hayatta tutar!",
            "note": "Erken karsinojenezde otofaji tümör süpresördür; yerleşmiş tümörde ise mikroçevre stresine ve tedaviye direnç sağlayan bir kaçış mekanizmasıdır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Hücresel Otofajinin Karsinojenezdeki İkili Rolü (Dual Nature)
Otofaji ("kendi kendini yeme"), hücrenin besin yoksunluğu veya metabolik stres durumunda kendi yaşlanmış organellerini, kusurlu protein agregatlarını ve membranlarını çift zarlı veziküller (**otofagozom**) içine hapsedip lizozomla birleştirerek (**otofagolizozom**) aminoasit ve enerji elde ettiği temel geri dönüşüm sürecidir. Süreç **ATG genleri, Beclin-1 (ATG6)** ve **LC3 (LC3-I'in LC3-II'ye lipitasyonu)** ile yürütülür.

Kanser Biyolojisinde İki Ucu Keskin Kılıç:
1. **Erken Evrede Tümör Baskılayıcı Rol (Genomik Kalkan):**
   - Sağlıklı hücrelerde otofaji hasarlı mitokondrileri temizler (**mitofaji**).
   - Mitokondrilerden sızacak reaktif oksijen radikallerini (ROS) yok ederek DNA mutasyonlarını ve genomik instabiliteyi önler.
   - Otofaji geni **Beclin-1 (BECN1)** tek alel delesyonu insan meme, over ve prostat karsinomlarında sık saptanır. Otofaji kusurlu farelerde spontan maligniteler gelişir. Bu evrede otofaji tümör oluşumunu engelleyen koruyucu bir mekanizmadır.

2. **İleri Evre Tümörlerde Sağkalım ve Direnç Motoru (Kanser Desteği):**
   - Malign neoplazm oluştuktan sonra tümör kitlesinin merkezinde hızla avasküler, hipoksik ve glukozdan yoksun bir metabolik çöl oluşur.
   - Kanser hücreleri otofajiyi devreye sokarak kendi sitoplazmik rezervlerini yakar; açlık krizini atlatıp hayatta kalırlar.
   - **Kemoterapi ve Radyoterapi Direnci:** Sitotoksik ilaçlar ve radyasyon tümör hücresinde masif organel hasarı yaratır. Kanser hücreleri otofajiyi sonuna kadar açarak hasarlı kısımları temizler; metabolik olarak "uykuda" (**dormant**) kalarak tedaviyi atlatırlar. Tedavi bitip ortam sakinleştiğinde ise uyanarak relaps ve metastaz yaparlar.

Klinik Yansıma ve Farmakolojik Hedefleme:
Yerleşmiş tümörlerde otofajiyi bloke ederek tümör hücrelerini kemoterapiye duyarlı hale getirmek modern onkolojinin stratejisidir. Lizozom asidifikasyonunu engelleyen **Klorokin** ve **Hidroksiklorokin**, otofagozom-lizozom birleşmesini durdurarak tümör hücresini metabolik krize sokan otofaji inhibitörleri olarak klinik kombinasyon çalışmalarında kullanılmaktadır.

> 🔴 **ÖNEMLİ:** Otofaji karsinojenezde iki evreli çalışır: **Başlangıçta genomik hasarı temizleyerek tümör baskılayıcıdır**; **kurulmuş tümörde ise hipoksi ve kemoterapi stresinde tümöre yakıt sağlayarak sağkalım ve direnç motorudur**.

> 🔵 **ÇIKMIŞ SORU:** Şiddetli metabolik stres, iskemi ve kemoterapi altında kalan tümör hücrelerinin organellerini sindirerek metabolik yakıt sağladığı ve tedavi direncine katkıda bulunduğu süreç **Otofaji**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Otofajinin çift yönlü rolü: Prekanseröz evrede genomu korur (tümör süpresör); ileri evrede besinsizlik ve kemoterapiden kaçış yakıtıdır (onkoprotektif).",
            "🔵 ÇIKMIŞ SORU: Otofagozom membran oluşumunda sitoplazmik formdan lipitlenmiş forma dönerek otofajik akışın belirteci olan protein **LC3 (LC3-II)**dir.",
            "⚡ Klorokin ve hidroksiklorokin lizozom füzyonunu engelleyerek otofajiyi bloke eder ve kemoterapi duyarlılığını artırır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Erken Süpresyon", "text": "Hasarlı mitokondri ve ROS temizliğiyle DNA mutasyonlarını engeller."},
                {"label": "Geç Direnç", "text": "Hipoksi ve kemoterapide hücre rezervlerini yakarak uykuda sağkalım sağlar."},
                {"label": "Moleküler Belirteç", "text": "Beclin-1 ve LC3-II otofagozom oluşumunun ana aktörleridir."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-20-1",
                "front": "Otofajinin erken karsinojenezde tümör baskılayıcı etki göstermesinin temel mekanizması nedir?",
                "back": "Kusurlu mitokondrileri temizleyerek (mitofaji) mutajenik reaktif oksijen radikallerinin (ROS) DNA'ya hasar vermesini önlemesidir.",
                "facultyNote": "Beclin-1 delesyonu bu nedenle kanser yatkınlığı yaratır."
            },
            {
                "id": "itg-fc-20-2",
                "front": "İleri evre tümörlerde otofaji inhibisyonu (örneğin klorokin ile) kemoterapinin etkinliğini nasıl artırır?",
                "back": "Tümör hücresinin ilaç hasarına karşı organellerini geri dönüştürerek hayatta kalmasını engeller ve hücreyi metabolik krize sokup öldürür.",
                "facultyNote": "Klinik faz çalışmalarında kombine tedavi olarak incelenir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-20",
            "question": "Hücresel otofajinin kanser patogenezindeki ve tedavi direncindeki rolü ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Erken evrede hasarlı organelleri ve reaktif oksijen türlerini temizleyerek tümör baskılayıcı rol oynar",
                "B) Otofaji düzenleyicisi Beclin-1 geninin tek alel kaybı bazı meme ve over karsinomlarında saptanır",
                "C) İleri evre tümörlerde avasküler hipoksi ve besinsizlik stresinde tümör hücresinin canlı kalmasını destekler",
                "D) Sitotoksik kemoterapi alan tümör hücrelerinde otofajinin aktive olması tedaviye bağlı hücre ölümünü daima hızlandırır",
                "E) Hidroksiklorokin lizozom fonksiyonunu bozarak otofajik degradasyonu bloke eden bir ajandır"
            ],
            "answer": "D",
            "explanation": "Sitotoksik kemoterapi alan tümör hücrelerinde otofajinin aktive olması hücre ölümünü hızlandırmaz; tam aksine hasarlı organelleri geri dönüştürerek hücrenin hayatta kalmasını ve metabolik uykuya (dormancy) geçerek tedaviye direnç kazanmasını sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 21,
        "title": "Tümör Anjiyogenezi ve Hipoksi Yanıtı: VHL – HIF-1α – VEGF Ekseni",
        "subtitle": "1-2 mm difüzyon sınırı, prolil hidroksilazlar, VHL ubikitinasyonu ve VEGF/GLUT1 transkripsiyonu.",
        "badge": "Anjiyogenez",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bir tümör 1-2 milimetreden büyük olamaz; çünkü oksijen difüzyon limiti tükenir! Büyümek istiyorsa kendi damarlarını inşa etmek zorundadır. Normokside VHL proteini HIF-1α'yı çöpe atar. Hipoksi gelip VHL uyuduğunda HIF-1α nükleusa uçar ve ortalığı VEGF seline boğar!",
            "note": "Von Hippel-Lindau sendromu ve Berrak Hücreli Renal Karsinomda (ccRCC) VHL mutasyonu nedeniyle hücre ortamda bol oksijen olsa bile hipoksideymiş gibi sürekli VEGF ve GLUT1 salgılar.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Hipoksi Algılama Moleküler Sistemi ve Anjiyojenik Anahtar
Katı bir tümör dokusunun kan damarı desteği olmadan basit oksijen ve besin difüzyonu ile büyüyebileceği maksimum çap **1 ila 2 milimetredir**. Bu boyutu aşan tümörlerin merkezinde hipoksi ve nekroz başlar. Tümörün ilerleyebilmesi için yeni damar oluşumunu (**tümör anjiyogenezi**) tetiklemesi şarttır; bu olaya **anjiyojenik anahtarın açılması (angiogenic switch)** denir.

Hipoksi Algılama Moleküler Mekanizması:
Hücrenin oksijen sensörü nükleer transkripsiyon faktörü olan **HIF-1α (Hypoxia-Inducible Factor 1 alpha)**dır:
1. **Normoksi (Yeterli Oksijen Varlığı - HIF-1α Yıkımı):**
   - Oksijen bol olduğunda sitoplazmik **Prolil Hidroksilaz (PHD)** enzimleri aktifleşir (bu enzimler moleküler oksijen, demir ve 2-oksoglutarat kullanır).
   - PHD enzimleri HIF-1α'nın prolil kalıntılarını hidroksiller.
   - Hidroksillenmiş HIF-1α, bir tümör baskılayıcı protein olan **VHL (Von Hippel-Lindau)** tarafından tanınır.
   - VHL proteini bir E3 ubikitin ligaz kompleksinin substrat tanıma modülüdür. HIF-1α'yı poliubikitinler ve **26S proteazomda süratle parçalatır** (yarı ömrü 5 dakikadan azdır). Hücrede HIF-1α birikmez.

2. **Hipoksi veya VHL İnaktivasyonu (Anjiyogenez Patlaması):**
   - Dokuda oksijen tükendiğinde prolil hidroksilazlar çalışamaz veya **Von Hippel-Lindau sendromunda / Berrak Hücreli Renal Hücreli Karsinomda (ccRCC)** 3p25 lokusundaki VHL geni mutasyonla inaktive olur.
   - HIF-1α prolil kalıntılarından hidroksillenemez veya VHL yokluğunda ubikitinlenemez; proteazomal yıkımdan kaçar.
   - Sitoplazmada biriken HIF-1α çekirdeğe girer, **HIF-1β** alt birimiyle heterodimer kurar ve **Hipoksi Yanıt Elementlerine (HRE)** bağlanır.

HIF-1 Kompleksinin Transkripsiyonel Hedefleri:
- **Vasküler Endotelyal Büyüme Faktörü (VEGF-A):** Endotel proliferasyonunu ve damar filizlenmesini tetikleyen ana faktör.
- **Trombosit Kaynaklı Büyüme Faktörü (PDGF):** Perisit ve düz kas hücrelerini çeker.
- **Metabolik Adaptasyon:** Oksijen yokluğunda hayatta kalmak için **GLUT1** glukoz taşıyıcılarını ve tüm glikolitik enzimleri yukarı regüle eder.

> 🔴 **ÖNEMLİ:** Berrak hücreli renal karsinomların (ccRCC) %90'ından fazlasında **VHL gen inaktivasyonu** mevcuttur. Bu tümörler normoksik koşullarda bile VHL yokluğu nedeniyle sürekli HIF-1α biriktirir ve aşırı VEGF salgılayarak son derece vasküler (kanamalı) bir morfoloji sergiler.

> 🔵 **ÇIKMIŞ SORU:** Normoksik koşullarda HIF-1α'ya bağlanarak onun ubikitinlenmesini ve proteazomal yıkımını sağlayan, inaktivasyonunda böbrekte berrak hücreli karsinom ve serebellar hemanjiyoblastom gelişen tümör süpresör protein **VHL**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Normokside prolil hidroksilazlar HIF-1α'yı hidroksiller; VHL proteini (E3 ligaz) bağlayıp proteazomda yıkar.",
            "🔵 ÇIKMIŞ SORU: VHL gen mutasyonu veya hipokside biriken HIF-1α nükleusta **VEGF, PDGF ve GLUT1** genlerini transkribe ederek anjiyogenezi patlatır.",
            "⚡ Berrak hücreli renal karsinom (ccRCC) ve Von Hippel-Lindau hastalığında VHL kaybı aşırı vaskülarizasyonun temel nedenidir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Difüzyon Sınırı", "text": "1-2 mm üzerinde tümör anjiyojenik anahtarı açmak zorundadır."},
                {"label": "VHL Mekanizması", "text": "Normokside HIF-1α'yı yıkar; hipokside veya VHL kaybında HIF-1α birikir."},
                {"label": "HIF-1α Hedefleri", "text": "VEGF, PDGF ile anjiyogenez; GLUT1 ile glikolitik adaptasyon."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-21-1",
                "front": "Sağlıklı bir hücrede normoksi koşullarında HIF-1α'nın proteazomda yıkılabilmesi için hangi enzimatik modifikasyon şarttır?",
                "back": "Prolil hidroksilaz (PHD) enzimleri tarafından prolil aminoasit kalıntılarından hidroksillenmesi şarttır.",
                "facultyNote": "VHL sadece hidroksillenmiş HIF-1α'yı tanıyabilir."
            },
            {
                "id": "itg-fc-21-2",
                "front": "Berrak hücreli renal karsinomda (ccRCC) tümörlerin aşırı damarsal ve kanamalı olmasının moleküler sebebi nedir?",
                "back": "3p25'teki VHL gen inaktivasyonu sonucu HIF-1α'nın sürekli birikmesi ve kesintisiz VEGF salgılanmasıdır.",
                "facultyNote": "Anti-anjiyojenik tirozin kinaz inhibitörleri bu yüzden ilk tercihtir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-21",
            "question": "Von Hippel-Lindau sendromu bulunan ve böbreğinde berrak hücreli renal hücreli karsinom saptanan bir hastada tümör dokusunun aşırı damarsal olmasında rol oynayan moleküler patogenez basamakları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Hastada fonksiyonel VHL proteini sentezlenememektedir",
                "B) Prolil hidroksilazlar HIF-1α'yı hidroksillese bile VHL eksikliği nedeniyle ubikitinasyon gerçekleşemez",
                "C) Hücre içi HIF-1α düzeyleri normoksik koşullarda bile aşırı derecede yükselir",
                "D) Nükleusa geçen HIF-1α VEGF ve PDGF gibi anjiyojenik faktörlerin transkripsiyonunu uyarır",
                "E) HIF-1α birikimi tümör hücresinde GLUT1 ekspresyonunu baskılayarak glukoz tüketimini tamamen durdurur"
            ],
            "answer": "E",
            "explanation": "HIF-1α birikimi GLUT1 ekspresyonunu baskılamaz; tam aksine hipoksik adaptasyon gereği GLUT1 glukoz taşıyıcılarının ve tüm glikolitik enzimlerin transkripsiyonunu güçlü şekilde artırarak glukoz tüketimini hızlandırır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 22,
        "title": "Tümör Damarlarının Anormal Morfolojisi ve Anti-Anjiyojenik Tedaviler",
        "subtitle": "Kaotik sızıntılı neovaskülarizasyon, Bevacizumab farmakolojisi ve anjiyogenik kaçış direnci.",
        "badge": "Hedefe Yönelik",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör damarı normal damara hiç benzemez; kaotiktir, delik deşiktir, perisiti yoktur ve sızdırır! Bu sızıntı tümör içi basıncı artırarak damarları ezer ve kemoterapinin içeri girmesini engeller. Bevacizumab ile VEGF'yi kestiğinizde önce damarlar 'normalleşir', ama zamanla tümör başka anjiyojenik yollara kaçar!",
            "note": "Bevacizumab doğrudan VEGF-A ligandını nötralize eden monoklonal antikordur. Anti-anjiyojenik tedavi tümörü aç bırakmayı amaçlar ama tek başına küratif değildir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Tümör Neovaskülarizasyonunun Patolojisi ve Anti-VEGF Tedavi
Tümörün kontrolsüz VEGF salınımıyla kurduğu neovaskülarizasyon, normal doku damarlarından radikal biçimde farklıdır:

Tümör Damarlarının Morfolojik Kusurları:
- **Kaotik Mimari:** Damarlar düzenli arter-kapiller-ven hiyerarşisi göstermez; kıvrıntılı, genişlemiş, kör sonlanan kaotik bir labirent gibidir.
- **Sızıntılı Yapı (Hiperpermeabilite):** Endotelde geniş pencereler bulunur; damarları saran destekleyici **perisit kılıfı ve bazal membran eksiktir**.
- **Yüksek İnterstisyel Basınç ve Kemoterapi Bariyeri:** Damarlardan sürekli plazma sızması ve lenfatik drenaj yetersizliği tümör içi **interstisyel sıvı basıncını aşırı yükseltir**. Bu doku basıncı ince kapillerleri çökerterek hipoksiyi derinleştirir ve kemoterapötik ilaçların tümör derinliklerine difüzyonunu engeller.

Anti-Anjiyojenik Tedavi: **Bevacizumab**
- **Etki Mekanizması:** VEGF-A ligandına bağlanan monoklonal antikordur. Dolaşımdaki VEGF'yi nötralize eder.
- **Damar Normalizasyonu:** Bevacizumab erken evrede kaotik damarları budar; geçirgenliği azaltıp interstisyel basıncı düşürerek eş zamanlı verilen kemoterapinin tümöre ulaşmasını kolaylaştırır.
- **Kullanım:** Metastatik kolorektal karsinom, berrak hücreli renal karsinom ve glioblastom.

Tedaviye Direnç ve Anjiyogenik Kaçış:
Anti-anjiyojenik tedaviler tek başlarına küratif olamazlar:
1. **Faktör Değişimi (Switching):** Tümör hücreleri VEGF yerine alternatif anjiyojenik faktörleri devreye sokar: **Fibroblast Büyüme Faktörü (FGF) ve PDGF**.
2. **Vasküler Ko-opsiyon:** Tümör hücreleri çevre normal dokunun mevcut olgun kan damarlarını bir kılıf gibi sararak yayılır.
3. **İnvaziv Kaçış:** Anti-anjiyogenezin yarattığı derin hipoksi, tümör hücresinde EMT'yi tetikler; hücreler damar aramak için çevre dokuyu istila eder.

> 🔴 **ÖNEMLİ:** Tümör süpresör **TP53**, anti-anjiyojenik **Trombospondin-1 (TSP-1)** sentezini uyarırken VEGF'yi baskılar; TP53 mutasyonu bu dengeyi bozarak neovaskülarizasyonu tetikler.

> 🔵 **ÇIKMIŞ SORU:** Tümör anjiyogenezinde endotel hücre proliferasyonunu uyaran VEGF'ye karşı geliştirilen ve metastatik kolon karsinomunda kullanılan monoklonal antikor **Bevacizumab**dır.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Tümör damarları perisit desteğinden yoksun, pencereli ve sızıntılıdır; bu durum yüksek interstisyel doku basıncı yaratarak ilaç geçişini bozar.",
            "🔵 ÇIKMIŞ SORU: Dolaşımdaki VEGF-A ligandını bağlayarak nötralize eden ve metastatik kolorektal kanserde kullanılan monoklonal antikor **Bevacizumab**dır.",
            "⚡ Anti-VEGF tedaviye direnç; tümörün FGF ve PDGF gibi alternatif büyüme faktörlerine geçmesi ve damar ko-opsiyonu ile gelişir.",
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Damar Anomalisi", "text": "Perisitsiz, sızıntılı; yüksek interstisyel sıvı basıncı kemoterapi geçişini önler."},
                {"label": "Bevacizumab", "text": "Anti-VEGF monoklonal antikor; damarları normalleştirir ve budar."},
                {"label": "Direnç Yolları", "text": "FGF/PDGF anjiyojenik kaçışı, vasküler ko-opsiyon ve hipoksik invazyon."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-22-1",
                "front": "Tümör damarlarının perisit kılıfından yoksun ve sızıntılı olması kemoterapi uygulamasını nasıl olumsuz etkiler?",
                "back": "Tümör içi interstisyel sıvı basıncını aşırı yükseltir; yüksek doku basıncı kapillerleri ezerek intravenöz kemoterapinin tümöre difüzyonunu engeller.",
                "facultyNote": "Bevacizumab bu basıncı düşürerek kemoterapinin geçişini artırır."
            },
            {
                "id": "itg-fc-22-2",
                "front": "TP53 geninin tümör anjiyogenezini fizyolojik olarak baskılarken kullandığı temel anti-anjiyojenik protein nedir?",
                "back": "Trombospondin-1 (TSP-1) proteinidir; p53 TSP-1'i artırırken VEGF'yi baskılar.",
                "facultyNote": "p53 kaybı anjiyogenezi çift taraflı hızlandırır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-22",
            "question": "Metastatik kolorektal adenokarsinom tanısıyla kemoterapi rejimine anti-anjiyojenik monoklonal antikor Bevacizumab eklenen bir hastada tümör damarlanması ve tedaviye direnç mekanizmaları ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Bevacizumab doğrudan dolaşımdaki VEGF-A molekülüne bağlanarak reseptör aktivasyonunu engeller",
                "B) Tümör damarları normal doku damarlarına kıyasla belirgin perisit eksikliği ve yüksek vasküler geçirgenlik gösterir",
                "C) Tedavi başlangıcında tümör içi interstisyel sıvı basıncı düşerek kemoterapötik ilaç penetrasyonu artabilir",
                "D) Tümör hücreleri zamanla FGF ve PDGF gibi alternatif büyüme faktörleri salgılayarak anti-VEGF blokajından kaçabilir",
                "E) Bevacizumab monoterapisi tek başına tümör damarlarını kalıcı olarak kurutarak tam kür sağlar"
            ],
            "answer": "E",
            "explanation": "Bevacizumab tek başına tümör damarlarını kalıcı olarak yok edip tam kür sağlayamaz; sağkalımı genellikle aylar düzeyinde uzatır. Tümörler zamanla alternatif anjiyojenik faktörlere (FGF, PDGF) geçer, çevre damarları sarar (vasküler ko-opsiyon) veya hipoksi derinleştikçe daha invaziv bir fenotipe bürünürler.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 23,
        "title": "Kanser Epigenetiği: DNA Metilasyonu, Histon Kodu ve Non-Coding RNA'lar",
        "subtitle": "MLH1/BRCA1 promoter hipermetilasyonu, HDAC ve EZH2 susturması, onko-miR ve tümör süpresör mikroRNA'lar.",
        "badge": "Kanser Epigenetiği",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanserde DNA dizilimi değişmeden de genler susturulabilir; işte buna epigenetik diyoruz! Tümör baskılayıcı genlerin promoterlarına metil grupları asarak (MLH1, p16, BRCA1) onları kör ederler. Bir de mikroRNA'lar var: miR-21 onkogen gibi çalışıp PTEN'i yok ederken, let-7 RAS'ı dizginleyen bir kahramandır!",
            "note": "Kanserde lokal promoter hipermetilasyonu (tümör süpresörleri susturur) ile küresel genomik hipometilasyon (kromozomal kararsızlık yaratır) aynı anda bulunur.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kanser Epigenetiği: DNA Metilasyonu, Histon Kodu ve ncRNA'lar
Kanser gelişiminde DNA nükleotid diziliminde mutasyon olmaksızın gen ifadesinin kalıtılabilir şekilde değişmesi **kanser epigenetiği**dir:

1. **DNA Metilasyonu Paradoksu (Sitozin 5-Metilasyonu):**
   Kanser genomunda iki zıt metilasyon anormalliği bir arada bulunur:
   - **Lokal Promoter Hipermetilasyonu (Tümör Süpresörlerin Susturulması):** CpG adacıkları **DNA Metiltransferazlar (DNMT)** tarafından aşırı metillenir; transkripsiyon kilitlenir (**epigenetik susturma**).
     - **MLH1 Hipermetilasyonu:** Sporadik mikrosatellit instabiliteli (MSI-H) kolorektal ve endometriyal karsinomların temel nedenidir.
     - **CDKN2A (p16INK4A) Hipermetilasyonu:** RB frenini devre dışı bırakır.
     - **BRCA1 Hipermetilasyonu:** Sporadik meme/over karsinomlarında DNA tamirini kilitler.
     - **VHL Hipermetilasyonu:** Berrak hücreli renal karsinomda anjiyogenezi açar.
   - **Küresel Genomik Hipometilasyon:** Heterokromatinde ve retrotranspozonlarda metilasyon kaybı; kromozomal kırılmalara ve genomik instabiliteye yol açar.

2. **Histon Kodu ve Kromatin Düzenlemesi:**
   - **Histon Asetilasyonu vs Deasetilasyonu:** **Histon Deasetilazlar (HDAC)** asetil gruplarını kopararak kromatini kapatır ve tümör baskılayıcı genleri susturur. HDAC inhibitörleri (**Vorinostat**) T-hücreli lenfomada kullanılır.
   - **EZH2 ve PRC2 Kompleksi:** **EZH2**, Histon 3 Lizin 27'yi trimetiller (**H3K27me3**); genleri kalıcı susturur. EZH2 inhibitörü **Tazemetostat** sarkom ve lenfomada kullanılır.

3. **Kodlamayan MikroRNA'lar (miRNA):**
   - **Onko-miR'ler:** **miR-21** PTEN tümör baskılayıcısını parçalayarak PI3K/AKT yolağını kontrolsüzce açar.
   - **Tümör Baskılayıcı miRNA'lar:** **let-7** RAS onkogen mRNA'sını yıkarak hücreyi korur. **miR-34 ailesi** ise p53 tarafından doğrudan transkribe edilir; antiproliferatif komutları yürütür.

> 🔴 **ÖNEMLİ:** Sporadik kolorektal karsinomlarda mikrosatellit instabilitesinin (MSI) en sık sebebi **MLH1 gen promoterının bialelik hipermetilasyonudur**.

> 🔵 **ÇIKMIŞ SORU:** Tümör baskılayıcı genlerin promoter CpG adacıklarının metillenerek kapatılması **DNA hipermetilasyonu**dur; PTEN'i yıkan onkojenik mikroRNA **miR-21**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Sporadik MSI kolon kanserlerinin temeli **MLH1 promoter hipermetilasyonu**dur; DNA dizilimi değişmeden gen sessizleştirilir.",
            "🔵 ÇIKMIŞ SORU: Onkojenik mikroRNA **miR-21** PTEN'i baskılayarak PI3K/AKT'yi açar; tümör süpresör **let-7** ise RAS onkogenini yıkar.",
            "⚡ EZH2 enzimi H3K27 trimetilasyonu (H3K27me3) yaparak kromatini baskılar; Tazemetostat ile inhibe edilir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "DNA Metilasyonu", "text": "Promoter CpG hipermetilasyonu (MLH1, p16, BRCA1) genleri susturur."},
                {"label": "Histon Düzeyi", "text": "HDAC kapalı kromatin yapar; EZH2 H3K27me3 baskısı kurar."},
                {"label": "MikroRNA Rolü", "text": "Onko-miR miR-21 PTEN'i yıkar; let-7 RAS'ı susturur; miR-34 p53 efektörüdür."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-23-1",
                "front": "Sporadik kolon ve endometrium karsinomlarında mikrosatellit instabilitesine (MSI) yol açan en yaygın epigenetik defekt nedir?",
                "back": "MLH1 geni promoter bölgesindeki CpG adacıklarının hipermetilasyonu sonucu MLH1 proteininin susturulmasıdır.",
                "facultyNote": "Lynch sendromundaki germline mutasyondan bu özelliğiyle ayrılır."
            },
            {
                "id": "itg-fc-23-2",
                "front": "Tümör baskılayıcı p53 proteini tarafından transkripsiyonu doğrudan indüklenen ve p53'ün antiproliferatif komutlarını yürüten mikroRNA ailesi hangisidir?",
                "back": "miR-34 mikroRNA ailesidir.",
                "facultyNote": "p53 mutasyonunda miR-34 seviyeleri de çöker."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-23",
            "question": "Malign tümörlerin epigenetik mekanizmaları ve kodlamayan RNA düzenlemeleri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Tümör baskılayıcı genlerin promoter CpG adacıklarının hipermetilasyonu transkripsiyonu susturur",
                "B) Sporadik kolon kanserlerinde MLH1 gen susturulması sıklıkla promoter hipermetilasyonuna bağlıdır",
                "C) Onkojenik bir mikroRNA olan miR-21, PTEN tümör süpresörünü baskılayarak PI3K/AKT yolunu aktive eder",
                "D) Tümör süpresör let-7 mikroRNA'sı RAS onkogen ekspresyonunu dizginleyen koruyucu bir moleküldür",
                "E) Kanser hücrelerinde genomik heterokromatin bölgelerinde masif hipermetilasyon gelişerek genom aşırı stabilize olur"
            ],
            "answer": "E",
            "explanation": "Kanser hücrelerinde heterokromatin bölgelerinde ve retrotranspozonlarda hipermetilasyon değil, tam aksine 'küresel genomik hipometilasyon' gelişir. Bu hipometilasyon kromatinin gevşemesine, transpozonların aktifleşmesine ve masif genomik instabiliteye yol açar. Hipermetilasyon ise lokal olarak tümör baskılayıcı gen promoterlarında görülür.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 24,
        "title": "Replikatif Ölümsüzlük (Replicative Immortality): Telomeraz ve ALT Yolağı",
        "subtitle": "Hayflick limiti, telomer erozyonu, köprü-kırılma döngüleri ve TERT promoter mutasyonları.",
        "badge": "Ölümsüzlük",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Normal bir hücre sonsuza dek bölünemez; Hayflick limiti vardır. Her mitozda telomerler kısalır ve nihayetinde kriz patlar. Kanser hücresi ise telomerazı (TERT) yeniden uyandırarak veya ALT yolağını açarak kromozom uçlarını onarır ve sonsuz bölünme lisansı (ölümsüzlük) kazanır!",
            "note": "TERT promoter mutasyonları (C228T, C250T) glioblastom, melanom ve mesane karsinomlarında en sık saptanan non-coding mutasyonlardır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Replikatif Ölümsüzlük: Telomer Erozyonu ve Kaçış Yolları
Normal insan somatik hücreleri kültürde en fazla 50 ila 70 kez bölünebilir; ardından bölünmeyi durdururlar (**Hayflick Limiti**). Bu sayaç **telomerlerdir**.

Telomer Biyolojisi ve Kriz Evresi:
- Kromozom uçlarında **TTAGGG** tekrarları ve uçları koruyan **Shelterin** kompleksi bulunur.
- DNA polimeraz doğrusal DNA'nın uç primerini tamamlayamaz (**end-replication problem**). Her mitozda telomerlerden 50-100 baz çifti kaybolur.
1. **Senesens:** Telomerler kritik kısalığa indiğinde p53 ve RB sağlamsa hücre bölünmeme evresine (**senesens**) sokulur.
2. **Mitotik Felaket (Mitotic Catastrophe):** p53 ve RB inaktifse hücre bölünmeyi sürdürür. Çıplak kromozom uçları birbirine yapışarak disentrik kromozomlar kurar. Anafazda sentromerler zıt kutuplara çekilirken kromozomlar kopar (**köprü-kırılma-birleşme döngüsü**). Bu kaos hücrelerin topluca öldüğü **mitotik felakete** yol açar.

Kanser Hücresinin Ölümsüzlük Kazanması:
Kanser hücresinin ölümsüzleşmesi (immortalization) telomer boyunu korumasına bağlıdır:
1. **Telomeraz Enziminin Reaktivasyonu (%85-90):**
   - Telomeraz; RNA şablonu (**TERC**) ve ters transkriptaz alt biriminden (**TERT**) oluşan ribonükleoproteindir. Normal somatik hücrelerde TERT susturulmuştur.
   - İnsan kanserlerinin %90'ında **TERT gen promoterında aktive edici mutasyonlar (C228T ve C250T)** saptanır. Bu mutasyonlar yeni transkripsiyon faktörü bağlanma bölgeleri açarak TERT üretimini patlatır.
   - Glioblastomların %80'inde, melanomların %70'inde ve mesane karsinomlarının %65'inde TERT promoter mutasyonları ana sürücüdür.
2. **Alternatif Telomer Uzaması (ALT) (%10-15):**
   - Telomeraz negatif tümörlerde homolog rekombinasyonla telomer kopyalanır.
   - Sarkomlarda ve astrositomlarda görülür; **ATRX ve DAXX** mutasyonları eşlik eder.

> 🔴 **ÖNEMLİ:** Glioblastom, melanom ve mesane karsinomlarında en sık saptanan mutasyon tipi **TERT geni promoter bölgesindeki (C228T, C250T)** mutasyonlardır.

> 🔵 **ÇIKMIŞ SORU:** Kanser hücrelerinin sonsuz replikasyon potansiyeli kazanmasını sağlayan TERT gen aktivasyonunda en sık görülen mekanizma **TERT promoter mutasyonları**dır.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: TERT promoter mutasyonları (C228T/C250T) glioblastom, melanom ve mesane kanserinde en sık görülen telomeraz reaktivasyon nedenidir.",
            "🔵 ÇIKMIŞ SORU: Telomerlerin aşırı kısalması sonucu disentrik kromozomların oluştuğu ve kromozomal kaos yaratan döngü **köprü-kırılma-birleşme (bridge-breakage-fusion)** döngüsüdür.",
            "⚡ Telomeraz negatif tümörlerde alternatif telomer uzaması (ALT) yolağı kullanılır; ATRX/DAXX mutasyonları eşlik eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Hayflick Limiti", "text": "Telomer erozyonu normal hücrenin mitoz sayısını sınırlar."},
                {"label": "Mitotik Felaket", "text": "p53/RB yoksa köprü-kırılma-birleşme döngüsü ile kriz patlar."},
                {"label": "Ölümsüzlük Yolları", "text": "TERT promoter mutasyonu (%90) veya ALT mekanizması (%10)."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-24-1",
                "front": "Glioblastom ve mesane karsinomlarında telomeraz aktivitesini artıran en karakteristik genetik lezyon nedir?",
                "back": "TERT geni promoter bölgesindeki aktive edici mutasyonlardır (özellikle C228T ve C250T).",
                "facultyNote": "Kodlamayan DNA bölgesinde saptanan en sık kanser mutasyonudur."
            },
            {
                "id": "itg-fc-24-2",
                "front": "Telomeraz aktivitesi negatif olan sarkom ve gliomlarda telomer boyunu koruyan alternatif mekanizma hangisidir?",
                "back": "Alternatif Telomer Uzaması (ALT) yolağıdır; ATRX ve DAXX inaktivasyonu ile birliktedir.",
                "facultyNote": "Homolog rekombinasyon ile telomer uzatılır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-24",
            "question": "Malign neoplazmların sınırsız replikatif potansiyel (ölümsüzlük) kazanması ve telomer biyolojisi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Normal somatik hücrelerde her hücre bölünmesinde uç replikasyon problemi nedeniyle telomerler kısalır",
                "B) p53 ve RB yolları inaktif olan hücreler telomer erozyonuna rağmen bölünerek köprü-kırılma-birleşme döngülerine girerler",
                "C) İnsan kanserlerinin yaklaşık %90'ında telomer boyu telomeraz enziminin reaktivasyonu ile korunur",
                "D) Glioblastom ve melanomda en sık saptanan TERT mutasyonu proteinin katalitik bölgesindeki missense mutasyonudur",
                "E) Telomeraz negatif bazı sarkom ve astrositomlarda telomerler ALT (Alternatif Telomer Uzaması) yolağı ile korunur"
            ],
            "answer": "D",
            "explanation": "Glioblastom, melanom ve mesane karsinomunda saptanan TERT mutasyonları protein kodlayan katalitik bölgede değil; TERT geni promoter bölgesinde (C228T, C250T) yer alan non-coding transkripsiyonel mutasyonlardır. Bu mutasyonlar yeni bağlanma bölgeleri yaratarak TERT ekspresyonunu artırır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]
