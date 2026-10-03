# -*- coding: utf-8 -*-
"""
scripts/ileri_tumor_genetigi/part2_slides.py
Slides 7 to 12 for 'learn-ileri-tumor-genetigi-metabolizmasi'
"""

slides_part2 = [
    {
        "slideNumber": 7,
        "title": "p53 Hücresel Yanıtları: Geçici Blokaj, Senesens ve Apoptoz Kararı",
        "subtitle": "p21 (CDKN1A) freni, GADD45 tamiri, geri döndürülemez senesens ve PUMA/BAX apoptozu.",
        "badge": "Genom Koruyucu",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "p53 hücrenin kaderini tayin eden en yüksek yargıçtır. DNA hasarı hafifse p21 ile hücreyi G1'de durdurup tamire fırsat tanır. Hasar onarılamayacak boyuttaysa tereddüt etmez; PUMA ve BAX'ı çağırıp mitokondriyi delerek hücreyi apoptozla idam eder!",
            "note": "p21 bir siklin bağımlı kinaz inhibitörüdür; hem Siklin D-CDK4 hem de Siklin E-CDK2'yi bloke ederek RB'nin hipofosforile (aktif) kalmasını sağlar.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### p53'ün Moleküler Karar Ağacı: Tamir mi, İntihar mı?
DNA hasarı veya onkojenik stresle aktive olup stabilize olan p53 proteini, hücreyi hasarlı genetik materyaliyle bölünmekten alıkoymak için üç temel savunma hattını yönetir:

1. **Geçici Hücre Döngüsü Duraklaması (Quiescence / G1 Arrest):**
   - p53'ün ilk tetiklediği gen **CDKN1A** (kodladığı protein: **p21CIP1**)'dır.
   - p21 geniş spektrumlu bir siklin bağımlı kinaz inhibitörüdür. Siklin D-CDK4/6 ve Siklin E-CDK2 komplekslerini güçlü biçimde inhibe eder.
   - Kinazlar bloke olunca RB proteini hiperfosforile edilemez; **hipofosforile (aktif)** formda kalır.
   - RB, E2F transkripsiyon faktörlerini tecrit etmeyi sürdürür ve hücre **G1/S kontrol noktasında durdurulur**.
   - Bu bekleme süresinde p53, **GADD45** (Growth Arrest and DNA Damage) gibi DNA onarım genlerini uyarır; hasar nükleotid eksizyon veya baz onarımı ile tamir edilir.
   - Tamir başarılı olursa, p53 kendi inhibitörü olan MDM2'yi uyararak düzeyini sıfırlar ve hücre sağ salim S fazına geçer.

2. **Kalıcı Hücre Döngüsü Duraklaması (Hücresel Senesens):**
   - DNA hasarı çok yaygınsa veya telomerler kritik düzeyde erozyona uğramışsa, hücre kalıcı heterokromatin odakları kurarak bir daha asla bölünemeyecek metabolik bir uyku evresine (**senesens**) kilitlenir.

3. **Programlanmış Hücre Ölümü (İntrinsik Apoptoz):**
   - Hasar onarılamaz boyutta olduğunda p53 nihai infaz kararını verir.
   - Pro-apoptotik BCL-2 ailesi üyelerinin transkripsiyonunu patlatır: Özellikle **PUMA (p53-Upregulated Modulator of Apoptosis)**, **NOXA** ve **BAX**.
   - Aynı anda anti-apoptotik BCL-2 ve BCL-XL'i baskılar.
   - PUMA ve NOXA, BAX ve BAK'ı allosterik olarak aktive eder. BAX/BAK oligomerleri mitokondri dış zarını geçirgenleştirir (MOMP).
   - Sitoplazmaya dökülen **sitokrom c**, Apaf-1 ve prokaspaz-9 ile apoptazom kurarak efektör Kaspaz-3'ü aktive eder ve tehlikeli hücre apoptoza gider.

> 🔴 **ÖNEMLİ:** TP53 mutasyonlu tümörlerde p21 indüklenemez, DNA tamiri yapılamaz ve BAX/PUMA kaynaklı apoptoz tetiklenemez. Hasarlı hücre kontrolsüzce çoğalarak ek mutasyonlar biriktirir.

> 🔵 **ÇIKMIŞ SORU:** p53'ün DNA hasarına yanıt olarak hücre döngüsünü G1/S kontrol noktasında geçici olarak durdurmasını sağlayan temel siklin bağımlı kinaz inhibitörü protein **p21CIP1 (CDKN1A)**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: p53 aracılı geçici G1 duraklamasını **p21CIP1** sağlar; p21 Siklin D/E-CDK komplekslerini bloke ederek RB'yi hipofosforile tutar.",
            "🔵 ÇIKMIŞ SORU: p53 onarılamayan DNA hasarında intrinsik apoptozu **BAX, BAK ve özellikle PUMA/NOXA** genlerini aktive ederek tetikler.",
            "⚡ p53 aracılı DNA tamir genleri arasında GADD45 yer alır; tamir tamamlanınca artan MDM2 p53'ü sıfırlayarak döngüyü yeniden başlatır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "p21CIP1 Etkisi", "text": "CDK inhibitörü; RB'yi hipofosforile tutarak G1 arresti oluşturur."},
                {"label": "GADD45 Rolü", "text": "p53 hedefi; DNA tamir mekanizmalarını aktive eder."},
                {"label": "PUMA ve BAX", "text": "Mitokondriyal zarı geçirgenleştirerek sitokrom c salınımı ve apoptoz sağlar."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-7-1",
                "front": "p53 aktive olduğunda G1/S kontrol noktasında geçici arresti hangi efektör protein üzerinden sağlar?",
                "back": "CDKN1A geninin ürünü olan p21 (p21CIP1) proteini üzerinden CDK4 ve CDK2 komplekslerini inhibe ederek.",
                "facultyNote": "p21 RB'nin fosforillenmesini önler."
            },
            {
                "id": "itg-fc-7-2",
                "front": "p53'ün onarılamaz DNA hasarında tetiklediği mitokondriyal apoptozun en kritik BH3-only efektörü nedir?",
                "back": "PUMA (ve NOXA) molekülüdür; BAX ve BAK'ı uyararak sitokrom c çıkışını sağlar.",
                "facultyNote": "TUS onkoloji sorularında PUMA anahtar kelimedir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-7",
            "question": "İyonizan radyasyona maruz kalan normal bir epitel hücresinde ATM kinaz tarafından aktive edilen p53'ün, hücreyi G1 evresinde durdurup DNA replikasyonuna geçişi engellemek için transkripsiyonunu doğrudan indüklediği temel siklin bağımlı kinaz inhibitörü protein aşağıdakilerden hangisidir?",
            "options": [
                "A) p16INK4A",
                "B) p21CIP1",
                "C) p27KIP1",
                "D) p57KIP2",
                "E) p15INK4B"
            ],
            "answer": "B",
            "explanation": "p53'ün doğrudan transkripsiyonunu başlattığı en temel CDK inhibitörü p21CIP1 (CDKN1A)'dir. p21, Siklin D-CDK4 ve Siklin E-CDK2'yi inhibe ederek RB'yi hipofosforile tutar ve G1/S geçişini bloke eder. p16 ve p15 ise p53 bağımsız yolaklarla uyarılır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 8,
        "title": "TP53 Somatik Mutasyonları ve Li-Fraumeni Sendromu",
        "subtitle": "Missense mutasyonlar, dominant-negatif etki, Li-Fraumeni sendromu spektrumu ve MDM2 amplifikasyonu.",
        "badge": "Kanser Sendromu",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Li-Fraumeni sendromu ailesel kanserlerin en trajik tablosudur. Hastalar tek bir mutant TP53 aleli ile doğarlar ve 30 yaşına gelmeden yumuşak doku sarkomu, meme karsinomu, beyin tümörü veya lösemi ile yüzleşirler. SBLA akronimini asla unutmayacaksınız!",
            "note": "TP53 mutasyonları çoğu tümör süpresördeki gibi delesyon değil, %75 oranında tek nükleotid missense mutasyonudur. Mutant protein yıkılamaz, hücrede aşırı birikir ve immünohistokimyada nükleusta koyu kahverengi boyanır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### TP53 Mutasyonlarının Biyolojisi ve Li-Fraumeni Sendromu
Çoğu tümör baskılayıcı gen karsinojenezde delesyon veya erken stop kodonuyla inaktive olurken, **TP53 mutasyonları istisnai bir biyolojiye sahiptir**:
- Olguların %75'inden fazlasında mutasyon, DNA bağlama alanında tek nükleotidlik **missense mutasyonu** şeklindedir.
- Mutant p53 proteini MDM2 tarafından tanınamaz ve proteazomal yıkımdan kaçar.
- Yıkılamayan p53 nükleusta aşırı miktarda birikir. Patolojide immünhistokimya (İHK) yapıldığında, tümör nükleuslarındaki homojen ve güçlü **p53 pozitifliği mutant fenotipin** göstergesidir.
- Dahası, p53 homotetramer olarak çalıştığından, tek bir mutant alt birim bile yabani tip p53 tetramerlerini bozar (**dominant-negatif etki**).

Li-Fraumeni Sendromu (Kalıtsal Kanser Yatkınlığı):
- Bireylerin germ hattında **tek bir mutant TP53 aleli** miras aldıkları, otozomal dominant geçişli sendromdur.
- Yaşam boyu kanser riski %90'a yaklaşır; kanserler erken yaşlarda başlar ve multipl primer tümörler sıktır.
- **Karakteristik Tümör Yelpazesi (SBLA Sendromu):**
  1. **S (Sarcoma):** Yumuşak doku sarkomları (rabdomyosarkom) ve osteosarkom.
  2. **B (Breast):** Çok genç yaşta (<30 yaş) premenopozal meme karsinomu.
  3. **L (Leukemia / Lymphoma):** Akut lösemi ve lenfomalar.
  4. **A (Adrenal cortex & Brain):** Çocukluk çağı adrenokortikal karsinomu ve beyin tümörleri (gliomlar).

MDM2 Gen Amplifikasyonu ile p53 Felci:
Bazı tümörlerde (özellikle iyi diferansiye ve dediferansiye liposarkomlarda) TP53 geni yabani tip olmasına rağmen 12q14-15 bölgesindeki **MDM2 geni devasa amplifiye** olmuştur. Aşırı üretilen MDM2, sağlam p53'ü yakalayıp proteazomda amansızca yıkar; p53 seviyesi sıfırlandığı için hücre kontrolsüzce prolifere olur.

> 🔴 **ÖNEMLİ:** Li-Fraumeni sendromunda çocukluk çağında saptanan **adrenokortikal karsinom** ve genç yaşta görülen **yumuşak doku sarkomları** TP53 germline mutasyonu için en güçlü klinik ipucudur.

> 🔵 **ÇIKMIŞ SORU:** TP53 geninde germ hattı mutasyonu bulunan bir hastada genç yaşta meme kanseri, osteosarkom, beyin tümörü ve adrenal korteks karsinomu gelişimi ile karakterize sendrom **Li-Fraumeni sendromu**dur.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Li-Fraumeni sendromu germline TP53 mutasyonudur; SBLA spektrumu: Sarkom, Meme, Lösemi/Lenfoma, Adrenal korteks karsinomu ve beyin tümörleri.",
            "🔵 ÇIKMIŞ SORU: p53 mutasyonlarının çoğu **missense** tipte olup dominant-negatif etki gösterir; mutant protein yıkılamadığı için İHK'da nükleer aşırı birikim izlenir.",
            "⚡ Liposarkomlarda TP53 sağlam olsa bile **MDM2 amplifikasyonu** p53 proteinini sürekli yıkarak aynı onkojenik sonuca yol açar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Li-Fraumeni", "text": "Germ hattı TP53 mutasyonu; sarkom, meme kanseri ve adrenal Ca birlikteliği."},
                {"label": "Missense Dominant", "text": "Tek nükleotid mutasyonu yabani tip tetrameri bozar ve nükleusta birikir."},
                {"label": "MDM2 Amplifikasyonu", "text": "Liposarkomda p53'ü proteazomda yok ederek işlevsiz kılar."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-8-1",
                "front": "Li-Fraumeni sendromunun altında yatan germ hattı mutasyonu ve en tipik 4 tümör grubu nedir?",
                "back": "TP53 germline mutasyonudur. Sarkomlar, genç yaş meme kanseri, lösemiler ve adrenal korteks/beyin tümörleri (SBLA).",
                "facultyNote": "Çocukta adrenal korteks karsinomu Li-Fraumeni için alarm zilidir."
            },
            {
                "id": "itg-fc-8-2",
                "front": "Dediferansiye liposarkomlarda p53 mutasyonu olmadan p53 yolağı nasıl devre dışı bırakılır?",
                "back": "12q15 kromozomundaki MDM2 gen amplifikasyonu ile aşırı MDM2 üretilerek p53 sürekli proteazomda parçalatılır.",
                "facultyNote": "İHK ve FISH ile MDM2 amplifikasyonu tanıda kullanılır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-8",
            "question": "Yirmi dört yaşında bir kadın hastada sağ memede invaziv duktal karsinom saptanmıştır. Aile öyküsü sorgulandığında erkek kardeşinin 7 yaşında rabdomyosarkomdan vefat ettiği, annesinin ise 32 yaşında adrenokortikal karsinom nedeniyle opere edildiği öğrenilmiştir. Bu hastada saptanması en olası kalıtsal genetik mutasyon aşağıdakilerden hangisidir?",
            "options": [
                "A) BRCA1 germline delesyonu",
                "B) TP53 germline mutasyonu",
                "C) APC germline mutasyonu",
                "D) PTEN germline mutasyonu",
                "E) RET germline mutasyonu"
            ],
            "answer": "B",
            "explanation": "Genç yaşta meme kanseri, rabdomyosarkom (yumuşak doku sarkomu) ve adrenal korteks karsinomu birlikteliği otozomal dominant geçişli Li-Fraumeni sendromunun klasik tablosudur. Altta yatan defekt germ hattı TP53 gen mutasyonudur.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 9,
        "title": "TGF-β Sinyal Yolağı: Normal Hücrede Güçlü Tümör Baskılayıcı Fren",
        "subtitle": "Serin/treonin kinaz reseptörleri, SMAD2/3/4 sinyal iletimi ve p15/p21 ile c-MYC baskılanması.",
        "badge": "Sinyal İletimi",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "TGF-β normal şartlarda epitel hücrelerinin en amansız düşmanıdır; bölünmeyi bıçak gibi keser! Hücre yüzeyindeki reseptörlerine bağlandığında SMAD trimeri çekirdeğe girer, p15 frenini çeker ve MYC onkogeninin boğazını sıkar.",
            "note": "SMAD2 ve SMAD3 reseptör tarafından doğrudan fosforillenir; ortak aracı olan SMAD4 ile birleşerek nükleusa göç eder.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### TGF-β Yolağının Fizyolojik ve Tümör Baskılayıcı Mimarisi
Transforme Edici Büyüme Faktörü-Beta (**TGF-β**), normal epitel, endotel ve hematopoetik hücrelerin proliferasyonunu güçlü şekilde baskılayan ana fizyolojik sitokindir. Sağlıklı dokularda epitelyal aşırı büyümeyi engelleyen temel parakrin ve otokrin güvenlik duvarıdır.

TGF-β Sinyal Kaskadının Moleküler Aşamaları:
1. **Reseptör Dimerizasyonu ve Aktivasyonu:**
   - Dolaşımdaki veya mikroçevredeki TGF-β ligandı, hücre zarında intrinsik serin/treonin kinaz aktivitesine sahip **Tip II reseptöre (TβRII)** bağlanır.
   - Bu bağlanma üzerine TβRII, komşu **Tip I reseptörü (TβRI)** fosforilleyerek onu enzimatik olarak aktif hale getirir.
2. **SMAD Proteinlerinin Fosforilasyonu:**
   - Aktif TβRI reseptör kinazı, sitoplazmada hazır bekleyen reseptörle ilişkili SMAD proteinlerini (**SMAD2 ve SMAD3**) spesifik serin kalıntılarından fosforiller.
3. **Heterotrimer Kompleks Oluşumu ve Nükleusa Göç:**
   - Fosforile olan SMAD2 ve SMAD3, ortak aracı (co-SMAD) olan **SMAD4** proteini ile bir araya gelerek stabil bir heterotrimerik transkripsiyon kompleksi oluşturur.
   - Bu SMAD2/3/4 kompleksi nükleer zara geçerek çekirdek içine transloke olur ve hedef DNA bölgelerine (SBE - SMAD Binding Elements) bağlanır.

Nükleustaki Çifte Antiproliferatif Darbe:
SMAD kompleksi nükleusa ulaştığında aynı anda iki yönlü bir transkripsiyonel program icra eder:
- **Frenlerin Güçlendirilmesi (CDK İnhibitörlerinin Aktivasyonu):**
  SMAD kompleksi **CDKN2B (p15INK4B)** ve **CDKN1A (p21CIP1)** genlerinin promoterlarını doğrudan uyarır. Aşırı üretilen p15, CDK4 ve CDK6'yı bloke eder; p21 ise Siklin E-CDK2'yi susturur. Böylece RB proteini hipofosforile kalarak hücreyi G1 evresinde kilitler.
- **Gaz Pedallarının Sökülmesi (Onkogenlerin Baskılanması):**
  Eş zamanlı olarak SMAD kompleksi, hücre büyümesinin ve metabolizmasının ana itici gücü olan **c-MYC** transkripsiyon faktörünün ve Siklin A/CDK4 genlerinin ifadesini doğrudan baskılar (transkripsiyonel represyon). Büyüme sinyali kesilen epitel hücresi bölünmeyi durdurur.

> 🔴 **ÖNEMLİ:** Normal bir epitel hücresinde TGF-β sinyali geldiğinde hem CDK inhibitörleri (p15, p21) artar hem de hücre döngüsünü kamçılayan **c-MYC geni doğrudan susturulur**. Bu çift yönlü kontrol G1/S geçişini tamamen kilitler.

> 🔵 **ÇIKMIŞ SORU:** TGF-β'nın epitel hücre proliferasyonunu durdurma mekanizmasında intraselüler sinyali çekirdeğe taşıyarak p15 ve p21 transkripsiyonunu artıran sitoplazmik aracı moleküller **SMAD proteinleri (özellikle SMAD4)**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: TGF-β Tip II ve Tip I serin/treonin kinaz reseptörleri üzerinden SMAD2/3'ü fosforiller; SMAD4 ile birleşen kompleks çekirdeğe girer.",
            "🔵 ÇIKMIŞ SORU: TGF-β nükleusta **p15 ve p21** CDK inhibitörlerini uyarırken, hücre büyümesini sağlayan **c-MYC** transkripsiyonunu doğrudan baskılar.",
            "⚡ Sağlıklı dokularda TGF-β en güçlü epitelyal büyüme frenidir; yokluğu kontrolsüz proliferasyona zemin hazırlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Reseptör Yapısı", "text": "TβRII ve TβRI intrinsik serin/treonin kinaz aktivitesine sahiptir."},
                {"label": "SMAD Kaskadı", "text": "SMAD2/3 fosforillenir, SMAD4 ile heterotrimer kurup nükleusa geçer."},
                {"label": "Transkripsiyonel Yanıt", "text": "p15 ve p21 transkripsiyonu artar, c-MYC susturulur, G1 arresti sağlanır."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-9-1",
                "front": "TGF-β sinyal yolunda SMAD2 ve SMAD3'ün çekirdeğe geçebilmek için birleştiği ortak ko-faktör protein hangisidir?",
                "back": "SMAD4 proteinidir. Oluşan heterotrimer nükleusta transkripsiyonu yönetir.",
                "facultyNote": "SMAD4 kaybı pankreas kanserinde neredeyse kuraldır."
            },
            {
                "id": "itg-fc-9-2",
                "front": "TGF-β normal epitel hücresinde hücre siklusunu durdurmak için hangi onkogenin ekspresyonunu doğrudan baskılar?",
                "back": "c-MYC onkogeninin transkripsiyonunu doğrudan baskılar.",
                "facultyNote": "Aynı zamanda p15INK4B ve p21'i uyarır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-9",
            "question": "Normal bağırsak epitelyumunda Transforme Edici Büyüme Faktörü-Beta (TGF-β) sinyal yolağının hücre proliferasyonunu G1 evresinde durdurma mekanizması ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) TGF-β Tip I ve Tip II reseptörleri serin/treonin kinaz aktivitesi gösterir",
                "B) Reseptör aktivasyonu sitoplazmik SMAD2 ve SMAD3 proteinlerini fosforiller",
                "C) Fosforile SMAD proteinleri ko-aracı SMAD4 ile birleşerek nükleusa transloke olur",
                "D) Nükleustaki SMAD kompleksi p15 ve p21 CDK inhibitörlerinin ekspresyonunu artırır",
                "E) SMAD kompleksi c-MYC onkogeninin transkripsiyonunu uyararak Siklin D sentezini hızlandırır"
            ],
            "answer": "E",
            "explanation": "SMAD kompleksi c-MYC onkogeninin transkripsiyonunu uyarmaz; tam aksine c-MYC genini güçlü şekilde baskılar (represyon). MYC'in baskılanması ve p15/p21'in uyarılması hücrenin bölünmesini durduran temel moleküler mekanizmadır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 10,
        "title": "TGF-β'nın İki Yüzü: İleri Evre Tümörlerde İnvazyon ve İmmünsüpresyon",
        "subtitle": "Tümör baskılayıcıdan metastaz destekleyicisine dönüşüm, EMT indüksiyonu ve immün körlük.",
        "badge": "Tümör Paradoksu",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Onkolojide buna 'TGF-β Paradoksu' diyoruz. Kanser hücresi başlangıçta TGF-β freninden kaçar (SMAD4 veya reseptörünü siler). İleri evrede ise aynı tümör devasa miktarda TGF-β salgılayarak bağışıklık hücrelerini uyutur ve metastaz yapar!",
            "note": "Pankreas adenokarsinomlarının yarısında SMAD4 (DPC4 - Deleted in Pancreatic Cancer 4) inaktive edilmiştir; bu kayıp tümörün TGF-β freninden tamamen kaçtığını kanıtlar.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### TGF-β Paradoksu: Koruyucu Melekten Şeytani İttifaka
TGF-β yolağı tümör evresine bağlı olarak taban tabana zıt iki rol üstlenir (**bağlam-bağımlı ikili doğa**):

1. **Erken Karsinojenezde Tümör Baskılayıcı Rol ve Kaçış:**
   - Erken evrede TGF-β epitel proliferasyonunu durduran güçlü bir frendir.
   - Malign neoplazmlar bu engeli aşmak için yolağı mutasyonla devre dışı bırakır:
     - **TβRII Reseptör İnaktivasyonu:** Mikrosatellit instabiliteli (MSI-H) kolorektal ve gastrik karsinomlarda TβRII genindeki mikrosatellit dizisinde mutasyon sıktır.
     - **SMAD4 Kaybı:** Pankreas adenokarsinomlarının %50'sinde **SMAD4 (DPC4)** homozigot delesyon veya mutasyonla yok edilir.
   - Sonuçta tümör hücresi TGF-β'nın büyüme durdurucu etkilerine karşı tamamen duyarsızlaşır.

2. **İleri Karsinojenezde Tümör Destekleyici Rol (Kötü Huylu Dönüşüm):**
   - Büyüme freninden kurtulan ileri evre kanser hücreleri, paradoksal olarak kendileri devasa miktarda TGF-β üretip çevreye salgılar.
   - Ortamdaki aşırı TGF-β tümörün büyümesini durduramaz; tam aksine invazyon ve yayılımı körükler:
     - **Epitelyal-Mezenkimal Geçiş (EMT):** TGF-β; **SNAIL, SLUG ve TWIST** transkripsiyon faktörlerini aktive eder. Bu faktörler **E-kadherini susturur**, vimentin ve matriks metalloproteinaz (MMP) üretimini artırır. Epitel hücresi polaritesini kaybederek motil, invaziv bir metastaz hücresine dönüşür.
     - **Güçlü İmmünosüpresyon:** TGF-β, tümör yatağındaki CD8+ sitotoksik T ve NK hücrelerini felç eder; naif T hücrelerini immün baskılayıcı **Regülatuvar T (Treg)** hücrelerine dönüştürür.
     - **Desmoplazi:** Kanserle ilişkili fibroblastları (CAF) uyararak tümörü saran yoğun, hipoksik fibröz stromayı (desmoplazi) kurar.

> 🔴 **ÖNEMLİ:** Pankreas karsinomunda **SMAD4/DPC4** gen kaybı TGF-β antiproliferatif frenini kırar; ileri evrede salgılanan TGF-β **SNAIL ve TWIST üzerinden E-kadherin kaybına ve EMT'ye** yol açarak masif invazyonu tetikler.

> 🔵 **ÇIKMIŞ SORU:** Kanser hücrelerinin epitelyal fenotipten mezenkimal fenotipe geçerek invazivite kazanmasında (EMT) ve immünsüpresif mikroçevre oluşumunda anahtar rol oynayan sitokin **TGF-β**dır.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Pankreas kanserlerinin %50'sinde **SMAD4 (DPC4)** kaybı saptanır; bu mutasyon TGF-β'nın büyüme frenini tamamen ortadan kaldırır.",
            "🔵 ÇIKMIŞ SORU: İleri evre tümörlerde TGF-β, **SNAIL ve TWIST** aktivasyonu ile E-kadherini baskılayarak **Epitelyal-Mezenkimal Geçişi (EMT)** ve metastazı tetikler.",
            "⚡ TGF-β aynı zamanda CD8+ sitotoksik T hücreleri baskılayıp Treg hücrelerini artırarak immün kaçış mikroçevresi oluşturur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "İkili Doğası", "text": "Erken evrede büyüme freni; ileri evrede metastaz ve immün kaçış sürücüsü."},
                {"label": "SMAD4 / DPC4", "text": "Pankreas karsinomunda inaktive olan kritik TGF-β aracı geni."},
                {"label": "EMT ve İmmün Felç", "text": "E-kadherini yıkar, motiliteyi artırır, T lenfositleri susturur."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-10-1",
                "front": "Pankreas adenokarsinomlarında 'DPC4' olarak da bilinen ve TGF-β sinyal yolunu bozan genetik inaktivasyon hangisidir?",
                "back": "SMAD4 gen delesyonu veya mutasyonudur (DPC4: Deleted in Pancreatic Carcinoma 4).",
                "facultyNote": "Tümör baskılayıcı SMAD yolağının kaybını gösterir."
            },
            {
                "id": "itg-fc-10-2",
                "front": "İleri evre kanserlerde salgılanan TGF-β'nın Epitelyal-Mezenkimal Geçişi (EMT) tetiklemesinde rol oynayan ana transkripsiyon faktörleri nelerdir?",
                "back": "SNAIL, SLUG ve TWIST faktörleridir; E-kadherin promoterını sustururlar.",
                "facultyNote": "E-kadherin kaybı tümör hücresine invaziv hareketlilik kazandırır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-10",
            "question": "İleri evre malign tümörlerde aşırı salgılanan TGF-β'nın tümör mikroçevresi ve neoplastik hücre davranışı üzerindeki biyolojik etkileri ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Sitotoksik CD8+ T lenfositlerin ve doğal katil (NK) hücrelerin antitümöral fonksiyonlarını baskılar",
                "B) Epitelyal-Mezenkimal Geçişi (EMT) tetikleyerek hücrelerin invazyon yeteneğini artırır",
                "C) SNAIL ve TWIST transkripsiyon faktörlerini aktive ederek E-kadherin ekspresyonunu baskılar",
                "D) Tümör hücrelerinde p15 ve p21 düzeylerini artırarak onları kalıcı apoptoza sürükler",
                "E) Fibroblastları aktive ederek desmoplastik stroma gelişimini kamçılar"
            ],
            "answer": "D",
            "explanation": "İleri evre tümör hücreleri TGF-β'nın büyüme baskılayıcı ve apoptotik etkilerine karşı direnç kazanmıştır (reseptör veya SMAD4 kaybı nedeniyle). Bu nedenle TGF-β artık tümör hücresinde p15/p21 aracılı apoptoz yapamaz; tam aksine tümörün lehine çalışarak EMT, invazyon ve immünosüpresyon sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 11,
        "title": "E-Kadherin, Kateninler, NF2 (Merlin) ve Temas İnhibisyonu",
        "subtitle": "Zonula adherens kompleksi, Hippo/YAP ekseni, NF2 mutasyonları ve lobüler meme/diffüz mide Ca modeli.",
        "badge": "Hücre Adezyonu",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "E-kadherin epitel hücrelerinin el ele tutuşmasını sağlayan moleküler çimentodur. Bu çimento çözüldüğünde hücreler birbirini bırakır ve tek tek dokuya sızar. İnvaziv lobüler meme karsinomundaki tek sıra 'kızılderili yürüyüşü' ve midedeki taşlı yüzük hücreleri işte bu CDH1 kaybının doğrudan morfolojik eseridir!",
            "note": "NF2 gen ürünü olan Merlin proteini, E-kadherinden gelen temas sinyallerini algılayarak hücreye 'dur' diyen temas inhibisyonu elçisidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Temas İnhibisyonu Mimarisi: E-Kadherin, Kateninler ve Merlin
Normal epitel hücreleri birbirleriyle fiziksel temas kurduklarında bölünmeyi durdururlar; bu olaya **temas inhibisyonu (kontak inhibisyon)** denir. Kanser hücreleri temas inhibisyonunu kaybederek üst üste yığılır ve çevre stromaya istila başlatır.

Temas İnhibisyonunun Moleküler Omurgası:
1. **E-Kadherin (CDH1 Geni):**
   - Epitel hücrelerinin en temel Ca-bağımlı adezyon glikoproteinidir. Hücreler arası **zonula adherens** kuşağında yer alır.
   - Hücre dışı bölgesiyle komşu hücrenin E-kadherinine tutunur.
   - Hücre içi kuyruğuyla doğrudan **β-katenin**e bağlanır; β-katenin de **α-katenin** aracılığıyla hücrenin **aktin hücre iskeletine** kenetlenir.
2. **NF2 ve 'Merlin' Proteini:**
   - 22q12 lokusundaki **NF2** tümör baskılayıcı geni **Merlin** proteinini kodlar.
   - Merlin, E-kadherin temas komplekslerinden gelen sinyalleri algılar ve **Hippo sinyal yolağını** aktive eder.
   - Aktif Hippo kaskadı onkojenik **YAP ve TAZ** transkripsiyon ko-aktivatörlerini fosforilleyip yıkar; proliferasyon durur.
   - **NF2 Gen İnaktivasyonu:** Nörofibromatozis Tip 2'ye yol açar; **iki taraflı akustik nörinom (schwannom)** ve meningiomlar gelişir.

E-Kadherin Kaybının Karakteristik Patolojileri:
- **Diffüz Tip Mide Adenokarsinomu:** **CDH1** germ hattı inaktivasyonunda kalıtsal diffüz mide kanseri gelişir. Sporadik diffüz karsinomlarda da CDH1 inaktiftir. Hücreler yapışamaz; tek tek yayılan hücreler sitoplazmalarında müsin biriktirip çekirdeği iter (**Taşlı Yüzük Hücreli Karsinom**).
- **İnvaziv Lobüler Meme Karsinomu:** Duktal karsinomdan farklı olarak, lobüler karsinomda CDH1 inaktivasyonu sonucu E-kadherin tamamen negatiftir. Hücreler tübül yapamaz; tek sıra halinde (**kızılderili yürüyüşü - Indian filing**) infiltre olurlar.

> 🔴 **ÖNEMLİ:** İnvaziv duktal ve **invaziv lobüler meme karsinomu** arasındaki en temel moleküler fark: Lobüler karsinomda **CDH1 kaybı sonucu E-kadherin immünhistokimyasal boyanmasının tamamen negatif** olmasıdır.

> 🔵 **ÇIKMIŞ SORU:** Hücreler arası temas inhibisyonunu sağlayan, intraselüler bölgede β-katenin ve aktin iskeletine bağlanan ve kaybında diffüz tip mide kanseri ile invaziv lobüler meme kanseri gelişen adezyon molekülü **E-kadherin**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: E-kadherin kaybı diffüz mide karsinomunda taşlı yüzük hücresi morfolojisine, invaziv lobüler meme karsinomunda 'kızılderili yürüyüşü' paterni oluşumuna yol açar.",
            "🔵 ÇIKMIŞ SORU: Nörofibromatozis Tip 2'de mutasyona uğrayan, E-kadherin temas inhibisyonunu Hippo/YAP yolağı üzerinden yöneten protein **Merlin (NF2)**dir.",
            "⚡ E-kadherinin sitoplazmik kuyruğu β-katenin ve α-katenin üzerinden aktin hücre iskeletine bağlanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "E-Kadherin (CDH1)", "text": "Ca-bağımlı adezyon molekülü; sitoplazmada kateninlerle aktine bağlanır."},
                {"label": "NF2 ve Merlin", "text": "Temas inhibisyonunu iletir, Hippo yolağını açar; kaybı bilateral schwannom yapar."},
                {"label": "Patolojik İmzalar", "text": "Taşlı yüzük hücreli mide Ca ve lobüler meme karsinomunda E-kadherin negatiftir."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-11-1",
                "front": "İnvaziv lobüler meme karsinomunda tümör hücrelerinin tek sıralı dizilim ('kızılderili yürüyüşü') göstermesinin moleküler nedeni nedir?",
                "back": "CDH1 gen mutasyonu veya susturulması sonucu E-kadherin proteininin tamamen kaybolmasıdır.",
                "facultyNote": "İmmünhistokimyada E-kadherin kaybı duktal ve lobüler ayrımında altın standarttır."
            },
            {
                "id": "itg-fc-11-2",
                "front": "NF2 (merlin) proteini temas inhibisyonunu sağlamak için hangi hücre içi yolağı aktive eder?",
                "back": "Hippo sinyal yolağını aktive ederek onkojenik YAP/TAZ transkripsiyon koaktivatörlerini baskılar.",
                "facultyNote": "Merlin inaktivasyonu nöral kılıf tümörlerine yol açar."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-11",
            "question": "Altmış yaşında bir kadın hastanın meme biyopsisinde tek sıra dizilim gösteren (Indian file paterni) ve tübüler yapı oluşturmayan kohezyonsuz malign hücre infiltrasyonu izlenmiştir. İmmünhistokimyasal incelemede bu hücrelerin membranöz E-kadherin boyanmasının tamamen negatif olduğu saptanmıştır. Bu tümörün histopatolojik tanısı ve patogenezinde rol oynayan temel genetik defekt aşağıdakilerden hangisidir?",
            "options": [
                "A) İnvaziv duktal karsinom — ERBB2 (HER2) amplifikasyonu",
                "B) Medüller karsinom — TP53 delesyonu",
                "C) İnvaziv lobüler karsinom — CDH1 inaktivasyonu",
                "D) Müsinöz karsinom — KRAS mutasyonu",
                "E) Metaplastik karsinom — APC gen inaktivasyonu"
            ],
            "answer": "C",
            "explanation": "Membranöz E-kadherin kaybı ve tek sıra halinde hücre infiltrasyonu (kızılderili yürüyüşü) invaziv lobüler meme karsinomunun patognomonik özelliğidir. Altta yatan temel moleküler olay CDH1 geninin mutasyon veya epigenetik susturulma ile fonksiyon kaybına uğramasıdır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 12,
        "title": "WNT / β-Katenin Yolağı ve APC Yıkım Kompleksi",
        "subtitle": "Aksin, GSK3β ve APC yıkım makinesi, WNT sinyali, nükleer translokasyon ve TCF/LEF aktivasyonu.",
        "badge": "Sinyal Yolağı",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Bağırsak epitelinde β-katenin iki efendiye birden hizmet eder: Hücre zarında E-kadherine tutunup adezyonu sağlar; sitoplazmada serbest kaldığında ise çekirdeğe koşup proliferasyon genlerini açar. APC proteini işte bu sitoplazmik β-katenini yakalayıp parçalayan canavar çarkın şefidir!",
            "note": "Dinlenme halindeki bir hücrede APC-Aksin-GSK3β kompleksi β-katenini fosforilleyip proteazomda parçalar; WNT uyarısı geldiğinde bu yıkım durur ve β-katenin nükleusa geçer.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### WNT / β-Katenin ve APC Yıkım Kompleksinin Dinamik Çalışma Prensibi
WNT sinyal yolağı, bağırsak kriptlerinde kök hücre yenilenmesini yöneten temel eksendir. Yolağın merkezinde çift fonksiyonlu bir molekül olan **β-katenin** yer alır: Zarda adezyonun parçasıyken, nükleusta proliferasyon aktörüdür.

Hücrenin WNT Durumuna Göre İki Temel Hali:
1. **Dinlenme Hali (WNT Yokken - β-Katenin Parçalanması):**
   - Ortamda WNT uyarısı yokken sitoplazmada serbest β-katenin birikmesi engellenmelidir.
   - Bu amaçla sitoplazmada **β-Katenin Yıkım Kompleksi (Destruction Complex)** kurulur.
   - Kompleksin iskeletini **APC** ve **Aksin (Axin)** oluşturur.
   - Kinaz enzimleri ise **Kazein Kinaz 1 (CK1)** ve **GSK3β** (Glikojen Sentaz Kinaz 3 Beta)'dır.
   - APC ve Aksin β-katenini yakalar; CK1 ve GSK3β enzimleri β-kateninin amino-ucunu fosforiller.
   - Bu fosforilasyon imha işaretidir: **β-TrCP** ubikitin ligazı fosforile β-katenini tanır ve **26S proteazoma yollayarak parçalatır**.
   - Sitoplazmik β-katenin düzeyi sıfırlanır; nükleusta **TCF/LEF** transkripsiyon faktörleri baskılı kalır.

2. **WNT Sinyali Geldiğinde (Kök Hücre Proliferasyonu):**
   - WNT ligandı hücre yüzeyindeki **Frizzled** reseptörüne ve **LRP5/6** ko-reseptörüne bağlanır.
   - Bu uyarı sitoplazmik **Dishevelled (Dvl)** proteinini aktive eder.
   - Dvl, Aksin proteinini hücre zarına çeker; böylece APC yıkım kompleksi inaktive olur ve dağılır.
   - GSK3β artık β-katenini fosforilleyemez; β-katenin yıkımdan kurtulur.
   - Sitoplazmada biriken serbest β-katenin nükleusa göç eder.
   - Nükleusta **TCF/LEF** transkripsiyon faktörlerine bağlanır ve hücre bölünmesini kamçılayan hedef genleri (**özellikle c-MYC ve Siklin D1**) aktive eder.

> 🔴 **ÖNEMLİ:** APC proteininin fizyolojik görevi bir reseptör olmak değildir; APC, **β-katenin yıkım kompleksinin yapısal parçasıdır** ve sitoplazmik β-katenini GSK3β fosforilasyonuna sunarak proteazomal yıkımını koordine eder.

> 🔵 **ÇIKMIŞ SORU:** WNT sinyal yolağında APC proteininin inaktivasyonunda gerçekleşen temel moleküler anormallik: **β-katenin yıkımının engellenmesi, nükleusa geçen β-katenin'in TCF transkripsiyon faktörünü kontrolsüz aktive etmesidir**.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: β-katenin yıkım kompleksi: APC, Aksin, CK1 ve GSK3β proteinlerinden oluşur; β-katenini fosforilleyip proteazoma yollar.",
            "🔵 ÇIKMIŞ SORU: WNT uyarısı veya APC kaybında yıkılamayan β-katenin nükleusa geçer ve **TCF/LEF** transkripsiyon faktörü ile birleşerek **c-MYC ve Siklin D1** genlerini aktive eder.",
            "⚡ APC bir tümör süpresör proteindir; inaktivasyonunda hücre sürekli WNT uyarısı alıyormuş gibi davranır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Yıkım Kompleksi", "text": "APC, Aksin, GSK3β, CK1; serbest β-katenini fosforilleyip yıkar."},
                {"label": "WNT Aktivasyonu", "text": "Frizzled ve Dvl aracılığıyla Aksin çekilir, kompleks dağılır."},
                {"label": "Nükleer Hedef", "text": "β-katenin nükleusta TCF/LEF ile birleşip c-MYC ve Siklin D1'i transkribe eder."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-12-1",
                "front": "β-katenin yıkım kompleksinde yer alan iki temel kinaz enzimi hangileridir?",
                "back": "Kazein Kinaz 1 (CK1) ve Glikojen Sentaz Kinaz 3 Beta (GSK3β) enzimleridir.",
                "facultyNote": "Bu kinazlar β-katenini fosforilleyerek ubikitinasyona hedefler."
            },
            {
                "id": "itg-fc-12-2",
                "front": "Nükleusa transloke olan serbest β-katenin hangi transkripsiyon faktörü ailesine bağlanarak proliferasyon genlerini uyarır?",
                "back": "TCF/LEF (T-cell factor / lymphoid enhancer factor) ailesine bağlanır.",
                "facultyNote": "Başta c-MYC ve Siklin D1 olmak üzere S fazı genlerini açar."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-12",
            "question": "WNT / β-katenin sinyal yolağının dinlenme halindeki ve aktif durumdaki regülasyonu ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) WNT uyarısı yokken sitoplazmik serbest β-katenin düzeyleri çok düşük tutulur",
                "B) β-katenin yıkım kompleksi APC, Aksin, CK1 ve GSK3β proteinlerini içerir",
                "C) GSK3β tarafından fosforillenen β-katenin doğrudan nükleusa geçerek TCF'yi inhibe eder",
                "D) WNT ligandı Frizzled ve LRP5/6 reseptörlerine bağlandığında Dishevelled (Dvl) aktive olur",
                "E) Nükleusta biriken β-katenin TCF/LEF ile birleşerek c-MYC ve Siklin D1 transkripsiyonunu uyarır"
            ],
            "answer": "C",
            "explanation": "GSK3β tarafından fosforillenen β-katenin nükleusa geçmez; tam aksine bu fosforilasyon β-TrCP tarafından tanınarak β-kateninin 26S proteazomda parçalanmasına yol açar. Nükleusa ancak fosforillenmemiş, yıkımdan kaçmış serbest β-katenin gidebilir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]
