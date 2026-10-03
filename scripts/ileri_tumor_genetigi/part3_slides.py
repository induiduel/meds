# -*- coding: utf-8 -*-
"""
scripts/ileri_tumor_genetigi/part3_slides.py
Slides 13 to 18 for 'learn-ileri-tumor-genetigi-metabolizmasi'
"""

slides_part3 = [
    {
        "slideNumber": 13,
        "title": "APC Kaybı, Ailesel Adenomatöz Polipozis (FAP) ve Kolorektal Karsinojenez",
        "subtitle": "Kromozom 5q21 gatekeeper geni, Gardner ve Turcot sendromları ve Vogelstein karsinom sekansı.",
        "badge": "Kolorektal Onkoloji",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kolon kanserinde APC kapı bekçisidir (gatekeeper). Bir hücrede APC kapısı kırıldığında adenom-karsinom sekansının ilk ve geri döndürülemez adımı atılmış olur. FAP hastaları bu ilk vuruşla doğarlar; ergenlikte kolonda binlerce polip fışkırır ve profilaktik kolektomi yapılmazsa 40 yaşına kadar karsinom kaçınılmazdır!",
            "note": "Sporadik kolon karsinomlarının %70-80'inde APC mutasyonu ilk basamaktır; APC mutasyonu olmayan nadir vakalarda ise doğrudan β-katenin geninde (CTNNB1) mutasyon saptanır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Kolon Karsinojenezinin Kapı Bekçisi: APC ve WNT Patolojisi
Kromozom 5'in uzun kolunda (**5q21**) yer alan **APC (Adenomatous Polyposis Coli)** geni, kolorektal epitelin en kritik tümör baskılayıcı kapı bekçisidir (**gatekeeper gen**). Bert Vogelstein'ın klasik "adenom-karsinom sekansı" modelinde, normal kolon mukozasından tübüler adenom gelişimini başlatan ilk genetik hasar APC inaktivasyonudur.

Ailesel Adenomatöz Polipozis (FAP) Sendromu:
- Hastalar germ hattında tek bir mutant APC aleli miras alırlar (**ilk vuruş**).
- Ergenlik döneminden itibaren kolonik kript epitelinde sağlam olan ikinci APC alelinde de somatik inaktivasyon gerçekleşir (**ikinci vuruş / LOH**).
- Kolonda yüzlerce ila binlerce adenomatöz polip (en az 100 polip tanı kriteridir) gelişir.
- **Klinik Seyir:** Eğer hastaya genç erişkinlikte profilaktik total kolektomi uygulanmazsa, 40 yaşına gelindiğinde bu poliplerin en az birinden **%100 oranında invaziv kolorektal adenokarsinom** gelişir.
- **FAP Varyantları:**
  - **Gardner Sendromu:** Kolonik poliplere ek olarak mandibulada osteomlar, desmoid tümörler, epidermal kistler ve konjenital retina pigment epitel hipertrofisi (CHRPE).
  - **Turcot Sendromu:** Kolonik adenomlara ek olarak santral sinir sistemi maligniteleri (özellikle medulloblastom).

Sporadik Kolorektal Karsinomlarda Moleküler Patogenez:
Tüm sporadik kolon kanserlerinin **%70-80'inde APC geninde bialelik somatik inaktivasyon** mevcuttur. APC proteini yok olduğunda β-katenin yıkım kompleksi kurulamaz. WNT sinyali olmasa dahi hücre içinde serbest β-katenin devasa konsantrasyonlara ulaşır. Nükleusa hücum eden β-katenin, **TCF** transkripsiyon faktörüyle birleşerek **c-MYC ve Siklin D1** genlerini sürekli transkribe eder. Böylece bağırsak kript epiteli temas inhibisyonunu ve matürasyonu terk ederek neoplastik adenom yapısına dönüşür. APC geni sağlam olan nadir sporadik kolon kanserlerinde ise doğrudan **CTNNB1 (β-katenin)** geninde mutasyon saptanır; bu mutasyon β-kateninin GSK3β tarafından fosforillenmesini önleyerek aynı onkojenik sonucu doğurur.

> 🔴 **ÖNEMLİ:** Kolorektal karsinojenezde APC geni **"gatekeeper (kapı bekçisi)"** iken, DNA uyumsuzluk onarım genleri (MSH2, MLH1) **"caretaker (bakımcı/onarıcı)"** genlerdir. FAP bir gatekeeper defekti örneğidir.

> 🔵 **ÇIKMIŞ SORU:** Ailesel Adenomatöz Polipozis (FAP) sendromunda mutasyona uğrayan, 5q21 lokusunda kodlanan ve β-katenin seviyelerini düzenleyerek kolon karsinojenezinde kapı bekçisi rolü üstlenen gen **APC**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: APC (5q21) gatekeeper gendir; bialelik kaybında β-katenin yıkılamaz ve nükleusta sürekli c-MYC/Siklin D1 transkripsiyonu başlar.",
            "🔵 ÇIKMIŞ SORU: Gardner sendromunda kolonik adenomatöz poliplere ek olarak **osteomlar, desmoid tümörler ve CHRPE** izlenir; sorumlu gen APC'dir.",
            "⚡ Sporadik kolon kanserlerinin %70-80'inde APC mutasyonu mevcuttur; APC normalse CTNNB1 (β-katenin) mutasyonu aranır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Lokus ve Görev", "text": "5q21, gatekeeper gen; kolon adenom-karsinom sekansının ilk basamağı."},
                {"label": "FAP ve Varyantlar", "text": "100'lerce polip, %100 Ca riski; Gardner'da osteom/desmoid, Turcot'ta beyin tümörü."},
                {"label": "β-Katenin İttifakı", "text": "APC yoksa β-katenin nükleusta TCF üzerinden c-MYC ve Siklin D1'i patlatır."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-13-1",
                "front": "Kolon karsinojenezinde APC gen inaktivasyonu neden adenom gelişimini başlatan ilk basamaktır?",
                "back": "APC yıkım kompleksini kurarak β-katenini frenleyen gatekeeper gendir; kaybında β-katenin nükleusta kontrolsüz kript proliferasyonunu başlatır.",
                "facultyNote": "Vogelstein adenom-karsinom sekansının 1 numaralı mutasyonudur."
            },
            {
                "id": "itg-fc-13-2",
                "front": "Gardner sendromunda APC mutasyonuna eşlik eden kolon dışı lezyonlar nelerdir?",
                "back": "Mandibula/kafatasında osteomlar, karın duvarında desmoid tümörler, epidermal kistler ve retinada CHRPE lezyonlarıdır.",
                "facultyNote": "Klinik sorularda osteom ve desmoid tümör FAP varyantını işaret eder."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-13",
            "question": "Yirmi yaşında asemptomatik bir erkek hastada yapılan tarama kolonoskopisinde tüm kolona yayılmış 500'den fazla tübüler adenom saptanmıştır. Çene radyografisinde multipl mandibuler osteomlar izlenmiştir. Bu hastanın genetik patogenezi ve kolon kanseri riski ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Hastada DNA uyumsuzluk onarım geni MSH2'de germ hattı mutasyonu mevcuttur",
                "B) Hastalık kromozom 5q21 lokusundaki APC gen mutasyonu sonucu gelişmiş olup kolektomi yapılmazsa kanser riski %100'dür",
                "C) Tümör oluşumu hücre içi serbest β-katenin düzeylerinin tamamen sıfırlanmasına bağlıdır",
                "D) Hastadaki lezyonlar Lynch sendromu tablosu olup ekstracolonik osteomlar rastlantısaldır",
                "E) WNT ligandları Frizzled reseptörlerine bağlanamadığı için hücreler diferansiye olamamıştır"
            ],
            "answer": "B",
            "explanation": "Yüzlerce adenom ve osteom birlikteliği FAP varyantı olan Gardner sendromudur. Kromozom 5q21'deki APC gen mutasyonundan kaynaklanır. Profilaktik kolektomi yapılmayan hastalarda 40 yaşına kadar %100 invaziv kolorektal adenokarsinom gelişir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 14,
        "title": "Onkojenik Metabolizma ve Warburg Etkisi (Aerobik Glikoliz)",
        "subtitle": "Kanser hücresinin metabolik tercihi, laktat fermantasyonu ve biyosentetik yapıtaşlarının temini.",
        "badge": "Tümör Metabolizması",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Otto Warburg 1920'lerde bir şey fark etti: Kanser hücresi bol oksijen varken bile mitokondrideki 36 ATP'lik verimli yolu bırakıp 2 ATP üreten glikolizi seçiyordu. Neden? Çünkü bölünen hücrenin derdi sadece enerji değil, iki yeni hücre yapacak karbon iskeletidir!",
            "note": "Warburg etkisi sadece tümöre özgü değildir; hızlı bölünen sağlıklı hücreler (örneğin aktive lenfositler ve embriyonik doku) de aerobik glikoliz kullanır.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Warburg Etkisi (Aerobik Glikoliz) ve Metabolik Mantığı
Normal diferansiye bir somatik hücre, yeterli oksijen varlığında glukozu sitoplazmada piruvata kadar yıkar; piruvat mitokondriye girerek Krebs döngüsü ve elektron taşıma zincirinde karbondioksite (CO2) kadar okside edilir. Bu süreç molekül başına yaklaşık **36 mol ATP** üreten son derece verimli bir metabolik yoldur (**oksidatif fosforilasyon**). Hücre ancak oksijensiz kaldığında (hipoksi) piruvattan laktat üretir (anaerobik glikoliz, net 2 ATP).

Nobel ödüllü Otto Warburg'un keşfettiği temel fenomen şudur: Kanser hücreleri ve hızla bölünen normal hücreler, **yeterli oksijen varlığında dahi** glukoz metabolizmasını oksidatif fosforilasyondan ziyade glikolize ve laktat üretimine kaydırırlar. Bu duruma **Aerobik Glikoliz (Warburg Etkisi)** denir.

Kanser Hücresi Neden Görünürde "Verimsiz" Bir Yolu Seçer?
Bir glukoz molekülünden sadece 2 ATP üreten bu yol ilk bakışta bir dezavantaj gibi görünür. Ancak hızla prolifere olan bir hücrenin en büyük biyolojik kısıtlaması enerji (ATP) değil, **biyosentetik yapıtaşlarının teminidir**:
- Bölünen bir tümör hücresi iki yeni yavru hücre oluşturmak için DNA, RNA, lipid, protein ve organellerini iki katına çıkarmak zorundadır.
- Eğer glukoz tamamen CO2 ve suya yakılsaydı, karbon atomları solunumla uçup giderdi; makromolekül sentezi için karbon iskeleti kalmazdı.
- Aerobik glikoliz glukoz akışını aşırı hızlandırır; böylece glikolitik ara metabolitler kritik biyosentetik kollara aktarılır:
  1. **Glukoz-6-Fosfat:** **Pentoz Fosfat Yolağına (PPP)** yönlendirilir. Burada nükleotid sentezinde kullanılan **riboz-5-fosfat** ile lipid biyosentezi ve antioksidan glutatyon rejenerasyonu için şart olan **NADPH** üretilir.
  2. **Gliserat-3-Fosfat:** Serin ve glisin gibi aminoasitlerin de novo sentezine yönlendirilir.
  3. **Dihidroksiaseton Fosfat (DHAP):** Hücre zarı inşası için gerekli fosfolipid ve triaçilgliserollerin omurgasını oluşturur.
  4. **Piruvat ve Laktat:** Üretilen laktat tümör dışına atılarak mikroçevre asitleştirilir; bu asidik ortam proteazları aktive edip tümör invazyonunu ve immün kaçışı kolaylaştırır.

> 🔴 **ÖNEMLİ:** Warburg etkisi (aerobik glikoliz) tümör hücresine sadece enerji sağlamakla kalmaz; asıl olarak hızlı bölünme için zorunlu olan **nükleotid, lipid ve aminoasit sentezinin karbon iskeletlerini ve NADPH havuzunu** temin eder.

> 🔵 **ÇIKMIŞ SORU:** Kanser hücrelerinin yeterli oksijen varlığında bile oksidatif fosforilasyon yerine glukozu laktata dönüştürerek hızlı hücre proliferasyonu için gerekli metabolik ara ürünleri üretmesi fenomeni **Warburg etkisi (Aerobik glikoliz)**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Warburg etkisi: Oksijen varlığında glukozun laktata çevrilmesi (aerobik glikoliz); temel amaç biyosentetik karbon iskeleti teminidir.",
            "🔵 ÇIKMIŞ SORU: Aerobik glikolizde glukoz-6-fosfat **Pentoz Fosfat Yolağına (PPP)** saparak nükleotid sentezi için **riboz-5-fosfat** ve redüksiyon için **NADPH** sağlar.",
            "⚡ Hızlı bölünen normal hücreler (aktif lenfositler) de Warburg metabolizmasını kullanır; ancak tümörlerde bu durum onkojenik mutasyonlarla kalıcı hale gelir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Tanım", "text": "Normokside bile glukozun glikoliz ve laktata kayması (aerobik glikoliz)."},
                {"label": "Biyosentetik Amaç", "text": "ATP'den ziyade nükleotid, lipid ve aminoasit yapıtaşlarını üretmek."},
                {"label": "Pentoz Fosfat Yolu", "text": "Riboz-5-fosfat (DNA/RNA) ve NADPH (lipid/antioksidan) temini."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-14-1",
                "front": "Warburg etkisinin (aerobik glikoliz) tümör hücrelerine sağladığı temel biyokimyasal avantaj nedir?",
                "back": "Hücre bölünmesi için gerekli nükleotid, aminoasit ve lipid sentezinde kullanılan glikolitik ara metabolitleri sağlamasıdır.",
                "facultyNote": "Sadece ATP üretmek değil, biyokütle (biomass) inşa etmek esastır."
            },
            {
                "id": "itg-fc-14-2",
                "front": "Glikolitik ara ürün glukoz-6-fosfatın pentoz fosfat yolağına aktarılması ile üretilen iki kritik molekül nedir?",
                "back": "Riboz-5-fosfat (nükleotid sentezi için) ve NADPH (lipid biyosentezi ve serbest radikal savunması için).",
                "facultyNote": "Metabolik soruların vazgeçilmez iki bileşenidir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-14",
            "question": "Malign tümör hücrelerinde yeterli oksijen varlığında dahi ATP üretiminin mitokondriyal oksidatif fosforilasyon yerine büyük oranda laktik asit fermantasyonuna kayması (Warburg etkisi) ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Glukoz başına net 2 mol ATP üretilmesine rağmen glukoz tüketim hızı dramatik olarak artmıştır",
                "B) Glikoliz ara ürünleri pentoz fosfat yolağına yönlendirilerek riboz-5-fosfat ve NADPH sentezlenir",
                "C) Temel biyolojik amaç hücrenin ihtiyacı olan nükleotid, lipid ve aminoasit karbon iskeletlerini temin etmektir",
                "D) Bu fenomen yalnızca kanser hücrelerine özgü olup hızlı bölünen hiçbir normal hücrede görülmez",
                "E) Üretilen laktatın mikroçevreye atılması asidik ortam yaratarak invazyonu kolaylaştırır"
            ],
            "answer": "D",
            "explanation": "Warburg etkisi sadece kansere özgü değildir; hızlı bölünen sağlıklı hücreler (örneğin antijenle uyarılmış prolifere olan lenfositler ve embriyonik dokular) de biyosentetik gereksinimleri nedeniyle aerobik glikoliz kullanır. Tümörlerde fark, bu programın onkogenik mutasyonlarla kalıcı ve kontrolsüz hale gelmesidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 15,
        "title": "Warburg Etkisinin Klinik Görüntülemesi: 18F-FDG PET Biyolojisi",
        "subtitle": "GLUT1 ve hekzokinaz oburluğu, metabolik tuzak prensibi ve onkolojik nükleer tıp uygulamaları.",
        "badge": "Klinik Görüntüleme",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "PET görüntüleme cihazı aslında bir Warburg dedektörüdür! Hastaya florla işaretli glukoz verirsiniz; kanser hücresi oburca glukozu çeker, hekzokinazla fosforiller ve içine hapseder. PET taramasında metastazların ampul gibi parlamasının moleküler sırrı metabolik tuzaktır.",
            "note": "18F-FDG 2. karbonunda hidroksil (-OH) grubu yerine flor-18 taşır; fosfoglukoz izomeraz bu yapıyı işleyemez ve defosforilasyon olmadığından hücre içinde kilitlenir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### 18F-FDG PET Nükleer Görüntülemesinin Moleküler Mekanizması
Warburg etkisinin klinik onkolojideki en başarılı uygulaması **18F-Florodeoksiglukoz Pozitron Emisyon Tomografisi (18F-FDG PET)** tekniğidir.

Biyokimyasal Zemin: GLUT ve Hekzokinaz Aşırılığı
Kanser hücreleri glukozu düşük ATP verimiyle (glukoz başına 2 ATP) kullandıklarından, normal dokulara kıyasla **20 ila 100 kat daha fazla glukoz** tüketmek zorundadırlar. Bu devasa iştahı doyurmak için:
- Hücre membranındaki glukoz taşıyıcılarını (özellikle **GLUT1** ve **GLUT3**) aşırı artırırlar.
- Glukozu tutan ilk enzim olan **Hekzokinazı (özellikle HK2)** yüksek düzeylerde eksprese ederler.

"Metabolik Tuzak (Metabolic Trapping)" Prensibi:
1. Hastaya enjekte edilen **18F-FDG**, bir glukoz analoğudur (2. karbondaki -OH grubu flor-18 ile değiştirilmiştir).
2. GLUT1 taşıyıcıları 18F-FDG'yi tümör hücresine taşır.
3. Hücre içinde hekzokinaz enzimi 18F-FDG'yi fosforilleyerek **18F-FDG-6-Fosfat** yapar.
4. 2. karbonda hidroksil grubu bulunmadığından bir sonraki enzim olan **Fosfoglukoz İzomeraz** bu molekülü tanıyamaz; glikoliz ilerleyemez.
5. Tümörde glukoz-6-fosfataz bulunmadığından, fosfatlı FDG hücre zarından dışarı geri sızamaz.
6. Sonuç: 18F-FDG tümör sitoplazmasında metabolik tuzağa düşer ve hapsolur. Bozunan 18F atomlarının yaydığı pozitronlar PET'te parlak hipermetabolik odaklar oluşturur.

Klinik Kullanım Alanları:
- **Primer Tümör ve Evreleme:** Okült primer tümör ve lenf nodu metastazlarının haritalanması.
- **Tedavi Yanıtı:** Kemoterapi sonrası boyutsal küçülmeden önce glukoz tutulumunun sönmesi en erken yanıt göstergesidir.
- **Nüks-Skar Ayrımı:** İnaktif fibröz skar glukoz tutmazken canlı nüks odakları yüksek FDG tutar.

> 🔴 **ÖNEMLİ:** 18F-FDG PET'te tümörün parlama mekanizması: **GLUT1 ve hekzokinaz aşırı ekspresyonu** ile alınan FDG'nin fosforillendikten sonra kilitlenmesidir (**metabolik tuzak**).

> 🔵 **ÇIKMIŞ SORU:** PET görüntülemede tümörde FDG birikmesini sağlayan temel değişiklikler: **GLUT1/GLUT3** taşıyıcıları ve **Hekzokinaz** enziminin aşırı artışıdır.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: 18F-FDG hücreye GLUT1 ile girer, hekzokinazla 18F-FDG-6-fosfata çevrilir; izomerize ve defosforile olamadığı için hücrede hapsolur (metabolik tuzak).",
            "🔵 ÇIKMIŞ SORU: Kanser hücrelerinde FDG tutulumunun yüksek olmasının nedeni **GLUT1/GLUT3** taşıyıcılarının ve **Hekzokinaz** enziminin aşırı ekspresyonudur.",
            "⚡ PET görüntüleme, kemoterapi yanıtında anatomik boyut küçülmesinden çok daha önce 'metabolik sönme' göstererek en erken yanıt kriterini sağlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "FDG Mekanizması", "text": "Glukoz analoğu; hekzokinaz ile fosforillenir ama glikolize devam edemez."},
                {"label": "Metabolik Tuzak", "text": "Fosfatlı FDG hücre zarından çıkamaz ve tümörde birikir."},
                {"label": "Klinik Güç", "text": "Metastaz taraması, tedavi yanıtı ve nüks-skar ayrımında altın standart."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-15-1",
                "front": "18F-FDG molekülünün hekzokinaz tarafından fosforillendikten sonra tümör hücresi içinde hapsolmasının nedeni nedir?",
                "back": "2. karbonunda flor atomu bulunduğundan fosfoglukoz izomeraz tarafından metabolize edilemez ve defosforile olamaz (metabolik tuzak).",
                "facultyNote": "Tıbbi nükleer onkolojinin temel biyokimyasal ilkesidir."
            },
            {
                "id": "itg-fc-15-2",
                "front": "FDG-PET'in onkolojik tedavi yanıtını değerlendirmede bilgisayarlı tomografiye (BT) en büyük üstünlüğü nedir?",
                "back": "Tümör kitlesi anatomik olarak henüz küçülmeden önce canlı hücrelerin metabolik glukoz tutulumunun sönmesini günler içinde gösterebilmesidir.",
                "facultyNote": "Prognozu ve yanıtı çok erken evrede tayin eder."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-15",
            "question": "Akciğer karsinomu tanısıyla kemoterapi alan bir hastanın tedavi yanıtını değerlendirmek amacıyla çekilen 18F-FDG PET/BT incelemesinde mediastinal lenf nodlarındaki glukoz tutulumunun tamamen kaybolduğu izlenmiştir. 18F-florodeoksiglukozun tümör hücrelerinde yüksek oranda tutulmasını ve hücre içinde birikerek metabolik tuzağa düşmesini sağlayan moleküler basamaklar ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) Kanser hücrelerinde glukoz alımı GLUT1 ve GLUT3 taşıyıcılarının artışı ile hızlandırılmıştır",
                "B) Sitoplazmaya giren FDG hekzokinaz enzimi tarafından FDG-6-fosfata dönüştürülür",
                "C) FDG-6-fosfat fosfoglukoz izomeraz enzimi tarafından kolayca fruktoz-6-fosfata çevrilerek Krebs döngüsüne girer",
                "D) Tümör hücrelerinde glukoz-6-fosfataz düzeyi çok düşük olduğundan FDG-6-fosfat hücre dışına kaçamaz",
                "E) PET incelemesi tümör kitlesinde boyut küçülmesi olmadan önce fonksiyonel metabolik yanıtı gösterebilir"
            ],
            "answer": "C",
            "explanation": "FDG molekülünün 2. karbonunda -OH grubu yerine flor bağlı olduğundan fosfoglukoz izomeraz enzimi bu molekülü tanıyamaz ve fruktoz-6-fosfata dönüştüremez. Bu nedenle FDG-6-fosfat glikolize devam edemez ve hücre içinde kilitlenir (metabolik tuzak).",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 16,
        "title": "Onkogenler ve Tümör Süpresörlerin Metabolik Düzenlemesi: MYC, PI3K/AKT/mTOR ve p53",
        "subtitle": "Glutamin bağımlılığı, anabolik lipid sentezi, TIGAR ve SCO2 ile p53 metabolik bekçiliği.",
        "badge": "Metabolik Düzenleyiciler",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Kanser metabolizmasını rastgele bir delilik sanmayın; arkasında onkogenler orkestrası vardır. MYC glutaminazı uyararak tümörü glutamin bağımlısı yapar. PI3K/AKT lipid fabrikalarını açar. Normalde p53 TIGAR ve SCO2 ile bu çılgınlığı frenlerdi; p53 ölünce metabolik fren tamamen boşalır!",
            "note": "p53'ün TIGAR geni glikolizi baskılarken, SCO2 geni mitokondriyal sitokrom c oksidazı destekler. TP53 mutasyonunda hücre hem glikoliz frenini kaybeder hem mitokondriyal solunumu terk eder.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Onkogen ve Tümör Baskılayıcıların Metabolik Programlaması
Warburg metabolizması izole bir biyokimyasal kusur değildir; klasik onkojenik sinyal yolaklarının hücre içi metabolizmayı doğrudan yönetmesinin doğal bir sonucudur:

1. **MYC Onkoproteini ve Glutamin Bağımlılığı (Glutamine Addiction):**
   - c-MYC, GLUT1 glukoz taşıyıcılarını ve glikolitik enzimleri (Hekzokinaz 2, PFK, Enolaz ve Laktat Dehidrogenaz A - LDHA) yukarı regüle eder.
   - En kritik metabolik eylemi: **Glutaminaz (GLS1)** enziminin transkripsiyonunu dramatik olarak artırmasıdır.
   - Kanser hücreleri glukoz kadar oburca glutamin tüketirler. Glutamin hücreye girip glutamat ve ardından **alfa-ketoglutarat (α-KG)** haline gelir.
   - Bu süreç Krebs döngüsünü ara ürünlerle besler (**anapleroz**) ve nükleotid ile aminoasit sentezinde kullanılan azot/amino gruplarını temin eder.

2. **PI3K / AKT / mTOR Yolağı (Anabolik Büyüme Motoru):**
   - Büyüme faktörü reseptörlerinden (RTK) gelen sinyaller PI3K ve AKT'yi aktive eder.
   - AKT, GLUT1 ve GLUT4'ün hücre membranına taşınmasını hızlandırır, Hekzokinazı fosforilleyerek glikolize bağlar.
   - Aktif **mTOR Kompleksi 1 (mTORC1)** ribozom biyogenezini ve protein translasyonunu tetikler; aynı zamanda **SREBP1** transkripsiyon faktörü üzerinden yağ asidi ve membran kolesterol sentezini (de novo lipogenez) sonuna kadar açar.

3. **TP53'ün Metabolik Frenleyici Rolü (Metabolik Muhafız):**
   Yabani tip p53, tümör metabolizmasını aerobik glikolizden uzaklaştırıp mitokondriyal solunuma yönlendiren ana fizyolojik bekçidir:
   - **TIGAR (TP53-Induced Glycolysis and Apoptosis Regulator):** p53 tarafından indüklenen TIGAR enzimi, hücre içi fruktoz-2,6-bisfosfat düzeylerini düşürür. Bu durum hız kısıtlayıcı enzim olan PFK-1'i inhibe ederek glikolitik akışı frenler; ara ürünleri Pentoz Fosfat Yolağına yönlendirerek antioksidan NADPH sentezini artırır.
   - **SCO2 (Synthesis of Cytochrome c Oxidase 2):** p53, mitokondriyal elektron taşıma zinciri Kompleks IV (sitokrom c oksidaz) montajı için zorunlu olan SCO2 proteininin transkripsiyonunu artırır. Böylece hücrenin oksidatif fosforilasyonu sürdürmesini sağlar.
   - **Sonuç:** TP53 mutasyona uğradığında TIGAR ve SCO2 kalkanı çöker; glikoliz freni kalkar, mitokondriyal solunum zayıflar ve hücre kaçınılmaz olarak Warburg aerobik glikolizine teslim olur!

> 🔴 **ÖNEMLİ:** TP53 mutasyonu taşıyan kanser hücrelerinde **TIGAR ekspresyonu kaybolur** (glikoliz baskısı kalkar) ve **SCO2 azalır** (mitokondriyal Kompleks IV montajı bozulur); bu çifte kayıp Warburg etkisini doğrudan tetikler.

> 🔵 **ÇIKMIŞ SORU:** Kanser hücrelerinde glutamin alımını ve glutaminaz (GLS) ekspresyonunu artırarak tümörün aminoasit ve nükleotid sentezinde glutamine bağımlı hale gelmesine yol açan onkogen **MYC**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: c-MYC onkoproteini **glutaminazı (GLS1)** indükleyerek tümörü glutamin bağımlısı yapar; Krebs döngüsünü anaplerotik olarak besler.",
            "🔵 ÇIKMIŞ SORU: p53 glikolizi **TIGAR** ile frenlerken, oksidatif fosforilasyonu mitokondriyal sitokrom c oksidaz montaj faktörü **SCO2** ile ayakta tutar.",
            "⚡ PI3K/AKT/mTOR ekseni SREBP aktivasyonu ile de novo lipid sentezini ve ribozomal protein yapımını kamçılayan ana anabolik motordur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "MYC ve Glutamin", "text": "Glutaminazı artırır, azot ve karbon iskeleti için glutamin bağımlılığı kurar."},
                {"label": "PI3K/AKT/mTOR", "text": "Glukoz alımını, protein translasyonunu ve lipid sentezini aktive eder."},
                {"label": "p53 Freni", "text": "TIGAR ile glikolizi yavaşlatır, SCO2 ile mitokondriyal solunumu korur."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-16-1",
                "front": "p53'ün glikolizi yavaşlatıp ara ürünleri pentoz fosfat yolağına yönlendiren metabolik hedef geni hangisidir?",
                "back": "TIGAR (TP53-Induced Glycolysis and Apoptosis Regulator) genidir.",
                "facultyNote": "Fruktoz-2,6-bisfosfatı düşürerek PFK-1'i baskılar."
            },
            {
                "id": "itg-fc-16-2",
                "front": "p53 mitokondriyal oksidatif fosforilasyonun Kompleks IV basamağını hangi protein üzerinden destekler?",
                "back": "SCO2 (Synthesis of Cytochrome c Oxidase 2) proteini üzerinden.",
                "facultyNote": "p53 mutasyonunda SCO2 düşer ve mitokondriyal solunum çöker."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-16",
            "question": "Kanser hücrelerinde metabolik yolakların onkogenler ve tümör süpresör genler tarafından kontrol edilmesi ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
            "options": [
                "A) c-MYC onkoproteini glutaminaz enzimini aktive ederek tümör hücresini glutamin bağımlısı haline getirir",
                "B) PI3K/AKT/mTOR yolağı glukoz taşıyıcılarını zarda artırır ve de novo lipid sentezini tetikler",
                "C) Yabani tip p53, TIGAR proteinini indükleyerek glikolitik akışı yavaşlatır",
                "D) p53 tarafından ekspresyonu artırılan SCO2, mitokondriyal elektron taşıma zinciri Kompleks IV montajını destekler",
                "E) TP53 gen inaktivasyonu durumunda SCO2 seviyeleri artarak mitokondriyal oksidatif fosforilasyon hızlanır"
            ],
            "answer": "E",
            "explanation": "TP53 gen inaktivasyonu durumunda SCO2 seviyeleri artmaz; tam aksine azalır. SCO2 desteği çöken mitokondride sitokrom c oksidaz (Kompleks IV) montajı bozulur ve hücre mitokondriyal solunumu terk ederek aerobik glikolize (Warburg etkisine) kayar.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 17,
        "title": "İzositrat Dehidrogenaz (IDH1/IDH2) Mutasyonları ve Neomorfik Enzim Aktivitesi",
        "subtitle": "Kodon R132 ve R172 mutasyonları, neomorfik fonksiyon ve alfa-ketoglutarattan 2-HG üretimi.",
        "badge": "Onkometabolitler",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Geleneksel olarak genetik mutasyonlar ya proteini susturur ya da hızlandırır sanırdık. IDH mutasyonu bu kuralı yıktı! Mutant IDH enzimi fonksiyon kaybetmez; yepyeni ve zehirli bir işlev kazanır (neomorfik aktivite). Normal ürünü alıp hücreyi kansere boğan '2-hidroksiglutarat' adlı onkometabolite çevirir!",
            "note": "IDH1 sitoplazma ve peroksizomda, IDH2 ise mitokondride görev yapar. Mutasyonlar aktif bölgedeki arjinin aminoasidini (R132 veya R172) değiştirir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### IDH1/IDH2 Mutasyonları ve Neomorfik Katalitik Aktivite
Metabolik enzim genlerindeki mutasyonların doğrudan karsinojenez başlattığının en sarsıcı kanıtı **İzositrat Dehidrogenaz (IDH)** enzim mutasyonlarının keşfidir.

Fizyolojik Krebs Döngüsünde IDH Rolü:
- **IDH1** (sitoplazma ve peroksizomlarda) ve **IDH2** (mitokondriyal matrikste) yerleşim gösterir.
- Normal fizyolojik reaksiyonda bu enzimler, Krebs döngüsü ara ürünü olan **izositratı** oksidatif dekarboksilasyon ile **alfa-ketoglutarata (α-KG)** dönüştürür.
- Bu sırada NADP+ molekülünü indirgeyerek hücrenin redoks dengesi için vazgeçilmez olan **NADPH** üretirler.

Onkojenik Mutasyonların Benzersiz Doğası: "Neomorfik (Yeni Fonksiyon Kazandırıcı) Aktivite"
Glioblastomlar, düşük dereceli gliomlar ve AML vakalarında IDH1 geninin 132. kodonunda (**IDH1 R132H**) veya IDH2 geninin 172/140. kodonlarında (**IDH2 R172, IDH2 R140**) heterozigot somatik missense mutasyonlar saptanmıştır:
1. **Basit Fonksiyon Kaybı Değildir:** Bu mutasyon enzimi işlevsiz bırakmaz.
2. **Neomorfik Reaksiyon:** Enzimin aktif bölgesindeki arjinin rezidüsünün değişmesi, substrat bağlama cebini yeniden şekillendirir. Mutant IDH enzimi artık normal substratı olan izositratı dönüştüremez.
3. Bunun yerine mutant enzim, normal reaksiyonun ürünü olan **alfa-ketoglutaratı (α-KG)** bağlar ve NADPH tüketerek onu doğrudan **D-2-Hidroksiglutarat (2-HG)** adı verilen anormal bir moleküle indirger!
4. **Onkometabolit Kavramı:** 2-Hidroksiglutarat normal fizyolojik hücrelerde ancak eser miktarlarda bulunan metabolik bir yan üründür. Ancak IDH mutant tümör hücrelerinde 2-HG konsantrasyonu 10 ila 100 kat artarak milimolar düzeylere ulaşır. Hücre içinde birikerek malign transformasyonu yöneten bu anormal metabolitlere **Onkometabolit (Oncometabolite)** adı verilir.

> 🔴 **ÖNEMLİ:** IDH1 ve IDH2 mutasyonları klasik bir "loss-of-function" veya basit "gain-of-function" değildir; enzime tamamen anormal yeni bir katalitik yetenek kazandıran **neomorfik mutasyondur**. Mutant enzim alfa-ketoglutaratı **2-hidroksiglutarata (2-HG)** çevirir.

> 🔵 **ÇIKMIŞ SORU:** İzositrat dehidrogenaz (IDH1/IDH2) mutasyonlarının karsinojenezdeki temel mekanizması: Enzimin neomorfik aktivite kazanarak alfa-ketoglutaratı bir onkometabolit olan **2-hidroksiglutarata (2-HG)** dönüştürmesidir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: IDH1/2 mutasyonları (R132/R172) **neomorfik enzimatik aktivite** yaratır; alfa-ketoglutaratı onkometabolit **2-hidroksiglutarata (2-HG)** indirger.",
            "🔵 ÇIKMIŞ SORU: Normalde izositratı alfa-ketoglutarata çeviren IDH enziminin mutant formu, hücrede anormal düzeyde **2-hidroksiglutarat** biriktirir.",
            "⚡ IDH1 sitoplazmada, IDH2 mitokondride çalışır; her ikisinde de mutasyon benzer onkometabolik sonuç doğurur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Fizyolojik Görev", "text": "İzositratı α-KG'ye dönüştürmek ve NADPH üretmek."},
                {"label": "Neomorfik Mutasyon", "text": "R132H mutasyonu ile α-KG'yi 2-hidroksiglutarata (2-HG) çevirme yeteneği kazanır."},
                {"label": "Onkometabolit", "text": "Hücrede biriken 2-HG malign transformasyonu başlatan kimyasal tetikleyicidir."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-17-1",
                "front": "IDH1 ve IDH2 mutasyonları neden basit bir fonksiyon kaybı (loss-of-function) olarak kabul edilmez?",
                "back": "Çünkü mutant enzim neomorfik aktivite kazanarak normalde yapmadığı bir reaksiyonla alfa-ketoglutaratı 2-hidroksiglutarata (2-HG) dönüştürür.",
                "facultyNote": "Tıpta neomorfik enzim mutasyonunun prototipidir."
            },
            {
                "id": "itg-fc-17-2",
                "front": "IDH1 mutasyonlarında en sık görülen spesifik aminoasit değişimi ve kodon hangisidir?",
                "back": "Kodon 132'de arjininin histidine dönüşmesidir (IDH1 R132H).",
                "facultyNote": "Nöropatolojide immünhistokimya ile R132H mutant proteini taranır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-17",
            "question": "Gliomlar ve akut miyeloid lösemide saptanan izositrat dehidrogenaz 1 (IDH1) gen mutasyonlarının enzimatik aktivite ve metabolik ürünler üzerindeki etkisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Enzim aktivitesi tamamen kaybolur ve hücrede izositrat birikerek apoptozu tetikler",
                "B) Enzim neomorfik aktivite kazanarak alfa-ketoglutaratı 2-hidroksiglutarata (2-HG) dönüştürür",
                "C) Enzim aşırı aktifleşerek hücre içi NADPH düzeylerini toksik boyutlara ulaştırır",
                "D) IDH1 mutasyonu sadece mitokondriyal DNA'da meydana gelen delesyonlardan kaynaklanır",
                "E) Mutant enzim laktatı glukoza çevirerek glikoneogenezi durdurur"
            ],
            "answer": "B",
            "explanation": "IDH1 mutasyonu neomorfik (yeni işlev kazandırıcı) bir mutasyondur. Enzim normal substratı olan izositrat yerine reaksiyon ürünü olan alfa-ketoglutaratı substrat olarak kullanır ve onu doğrudan '2-hidroksiglutarat (2-HG)' adlı onkometabolite indirger.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 18,
        "title": "Onkometabolit 2-Hidroksiglutarat (2-HG), TET2 İnhibisyonu ve CIMP Fenotipi",
        "subtitle": "Alfa-ketoglutarat bağımlı dioksijenazların kompetitif blokajı, masif DNA hipermetilasyonu ve diferansiyasyon engeli.",
        "badge": "Epigenetik Felaket",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "2-HG hücresel bir taklitçidir! Yapısı alfa-ketoglutarata o kadar benzer ki, α-KG kullanan tüm dioksijenaz enzimlerini aldatır. TET2 DNA demetilazını kilitler. TET2 felç olunca DNA demetile edilemez, tümör genomu baştan aşağı metillenir (CIMP) ve hücre kök hücre halinde kilitlenip çoğalır!",
            "note": "2-HG hem DNA demetilazı TET2'yi hem de histon lizin demetilazları (KDM) inhibe eder. Bu çifte epigenetik kilit kök hücre diferansiyasyonunu bloke eder.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### 2-Hidroksiglutaratın (2-HG) Epigenetik Felaketi Tetikleme Mekanizması
Mutant IDH enzimlerinin ürettiği **2-Hidroksiglutarat (2-HG)**, kimyasal yapısı itibarıyla Krebs döngüsü metaboliti olan **alfa-ketoglutaratın (α-KG)** yapısal ikizidir (antimetabolitidir). Hücrede kofaktör olarak α-KG ve Fe(II) kullanan 60'tan fazla "alfa-ketoglutarat bağımlı dioksijenaz" enzimi bulunur. Devasa miktarda biriken 2-HG, bu enzimlerin katalitik aktif bölgesine yarışmalı (**kompetitif**) olarak bağlanır ve onları felç eder!

2-HG'nin Bloke Ettiği İki Kritik Epigenetik Enzim Grubu:
1. **TET2 (Ten-Eleven Translocation 2) DNA Demetilazı:**
   - Fizyolojik görevi: DNA'daki 5-metilsitozini (5-mC) oksitleyerek 5-hidroksimetilsitozine (5-hmC) çevirmek ve DNA demetilasyonunu başlatmaktır.
   - 2-HG TET2'yi inhibe ettiğinde genomik DNA demetile edilemez!
   - Sonuç: Genom çapında, özellikle gen promoterlarındaki CpG adacıklarında masif bir DNA hipermetilasyonu gelişir.
   - Bu yaygın epigenetik susturma tablosuna **CpG Island Methylator Phenotype (CIMP)** adı verilir (gliomlardaki formu: **G-CIMP**).
2. **JmjC Alanı İçeren Histon Lizin Demetilazlar (KDM):**
   - Histon kuyruklarındaki metil gruplarını kopararak kromatini transkripsiyona açık tutan enzimlerdir.
   - 2-HG bu enzimleri de bloke eder; histon metilasyonu (H3K9me3, H3K27me3) artar ve kromatin kalıcı olarak baskılanır.

Diferansiyasyon Blokajı (Kök Hücre Tuzağı):
TET2 ve histon demetilazların felç olması sonucu ortaya çıkan yaygın hipermetilasyon, öncül kök hücrelerin matür doku hücrelerine (matür nöron/glia veya matür miyeloid hücreler) farklılaşmasını yöneten anahtar transkripsiyon faktörü genlerini transkripsiyonel olarak susturur.
- Diferansiye olamayan hücreler ilkel, kök hücre benzeri, diferansiyasyon yeteneğini kaybetmiş bir evrede kilitlenip kalır.
- Bu blokaj hücreye sınırsız çoğalma potansiyeli kazandırır ve malign transformasyon patlak verir.

> 🔴 **ÖNEMLİ:** Akut Miyeloid Lösemi (AML) vakalarında **IDH1/IDH2 mutasyonları ile TET2 mutasyonları birbirini karşılıklı dışlar (mutually exclusive)**! Çünkü TET2 mutasyonu ile IDH mutasyonunun ürettiği 2-HG aynı epigenetik yolu (DNA demetilasyonunun engellenmesini) felç eder.

> 🔵 **ÇIKMIŞ SORU:** IDH mutant gliomlarda ve lösemilerde 2-hidroksiglutaratın (2-HG) karsinojenezdeki temel rolü: **TET2 DNA demetilaz enzimini inhibe ederek genom çapında CpG adacık hipermetilasyonuna (CIMP) ve hücresel diferansiyasyon blokajına yol açmasıdır**.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: 2-HG, alfa-ketoglutarat bağımlı **TET2** DNA demetilazını inhibe ederek genomik **CpG adacığı hipermetilasyonuna (CIMP)** yol açar.",
            "🔵 ÇIKMIŞ SORU: AML'de **IDH mutasyonları ile TET2 mutasyonları birbirini karşılıklı dışlar**; çünkü her ikisi de aynı demetilasyon yolunu felç eder.",
            "⚡ 2-HG aynı zamanda histon demetilazları da bloke ederek kromatin kapanmasına ve kök hücre diferansiyasyonunun durmasına neden olur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Kompetitif İnhibisyon", "text": "2-HG, α-KG bağımlı dioksijenaz enzimlerini yarışmalı olarak bloke eder."},
                {"label": "TET2 ve CIMP", "text": "TET2 inhibisyonu sonucu yaygın DNA promoter hipermetilasyonu gelişir."},
                {"label": "Diferansiyasyon Engeli", "text": "Matürasyon genleri susar; hücre immatür bölünen kök hücrede kilitlenir."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-18-1",
                "front": "2-Hidroksiglutaratın (2-HG) inhibe ettiği ve CpG hipermetilasyonuna (CIMP) yol açan ana DNA demetilasyon enzimi hangisidir?",
                "back": "TET2 (Ten-Eleven Translocation 2) dioksijenaz enzimidir.",
                "facultyNote": "TET2 normalde 5-mC'yi 5-hmC'ye oksitler."
            },
            {
                "id": "itg-fc-18-2",
                "front": "AML'de IDH1/2 mutasyonları ile TET2 mutasyonlarının birbirini karşılıklı dışlamasının (mutually exclusive) biyolojik açıklaması nedir?",
                "back": "Çünkü her iki mutasyon da aynı biyokimyasal sonucu doğurur (TET2 fonksiyon kaybı ve DNA hipermetilasyonu); aynı hücrede ikisine birden gerek yoktur.",
                "facultyNote": "Moleküler onkolojinin en zarif yolak prensibidir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-18",
            "question": "İzositrat dehidrogenaz (IDH) mutasyonu taşıyan diffüz gliomlarda ve akut miyeloid lösemide biriken onkometabolit 2-hidroksiglutaratın (2-HG) hücresel diferansiyasyonu engelleyerek neoplastik transformasyonu tetikleme mekanizması ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) DNA metiltransferaz (DNMT) enzimlerini doğrudan parçalayarak küresel hipometilasyona yol açar",
                "B) Alfa-ketoglutarat bağımlı TET2 DNA demetilazını inhibe ederek yaygın CpG hipermetilasyonuna (CIMP) neden olur",
                "C) Histon asetiltransferazları aktive ederek kromatini sürekli açık ve gevşek tutar",
                "D) Sitoplazmada p53 proteinine bağlanıp onu doğrudan ubikitinleyerek apoptozu engeller",
                "E) Mitokondriyal elektron taşıma zincirini tamamen bloke ederek hücreyi laktik asidozla öldürür"
            ],
            "answer": "B",
            "explanation": "2-HG yapısal olarak alfa-ketoglutarata benzer ve α-KG bağımlı dioksijenaz olan TET2 DNA demetilaz enzimini kompetitif olarak inhibe eder. TET2 bloke olunca DNA demetile edilemez; genom çapında CpG hipermetilasyonu (CIMP fenotipi) gelişir ve matürasyon genleri susturularak diferansiyasyon kilitlenir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]
