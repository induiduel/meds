# -*- coding: utf-8 -*-
"""
scripts/ileri_tumor_genetigi/part1_slides.py
Slides 1 to 6 for 'learn-ileri-tumor-genetigi-metabolizmasi'
"""

slides_part1 = [
    {
        "slideNumber": 1,
        "title": "İleri Tümör Genetiği ve Moleküler Onkolojiye Bütüncül Giriş",
        "subtitle": "Hücre döngüsü bekçileri, onkometabolik ağlar ve non-lethal genetik hasarın klonal evrimi.",
        "badge": "Moleküler Giriş",
        "badgeColor": "accent",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Değerli meslektaşlarım, karsinojenez rastgele bir hücre çoğalması değildir. Hücrenin hem genomik frenlerini (RB, TP53) kırması hem de metabolizmasını (Warburg etkisi, IDH mutasyonları) bu kontrolsüz büyümeyi besleyecek şekilde yeniden organize etmesi gerekir.",
            "note": "İleri tümör genetiğinde odak noktamız genetik sinyal iletim yolları ile hücre metabolizmasının nasıl iç içe geçtiğidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Karsinojenezin Moleküler Temeli ve İleri Genetik Yaklaşım
Malign neoplazmların patogenezinde temel kural, hücrenin maruz kaldığı DNA hasarının ölümcül olmaması (**non-lethal genetik hasar**) ilkesidir. Eğer hücresel hasar öldürücü düzeyde olsaydı hücre lizise, nekroza veya akut apoptoza uğrar; neoplastik bir klon başlatamazdı. Karsinojenez, non-lethal hasara uğramış tek bir atasal hücrenin genetik transformasyonuyla başlar (monoklonalite) ve zamanla genomik instabilite zemininde ek mutasyonlar biriktirerek heterojen subklonlar meydana getirir.

Prof. Dr. Hikmet Keleş'in amfide üzerinde titizlikle durduğu üzere, modern moleküler patoloji kanseri yalnızca büyüme faktörü sinyallerinin kontrolsüz aktivasyonu olarak değil, hücresel enerji metabolizması, DNA tamir ağları, epigenetik programlama ve mikroçevre etkileşimlerinin oluşturduğu çok katmanlı bir sistem olarak ele almaktadır. Bu derste inceleyeceğimiz temel eksenler şunlardır:
1. **Hücre Döngüsü Fren Mekanizmaları:** Retinoblastom (RB) proteininin G1/S kontrol noktasındaki bekçiliği ve E2F regülasyonu.
2. **Genomun Baş Muhafızı:** TP53 geninin DNA hasarı, hipoksi ve onkojenik strese verdiği hücresel yanıtlar (durgunluk, senesens, apoptoz).
3. **Parakrin ve Adezyonel Frenler:** TGF-β yolağının ikili doğası (tümör baskılayıcıdan metastaz promotörüne dönüşüm), E-kadherin/katenin kompleksi ve APC/WNT yolağının β-katenin yıkım mekanizması.
4. **Metabolik Yeniden Programlanma:** Oksijen varlığında bile glikolizin seçildiği Warburg etkisi, onkojenlerin (MYC, PI3K/AKT/mTOR) metabolik kontrolü ve mutant IDH enzimlerinin ürettiği onkometabolit 2-hidroksiglutaratın (2-HG) epigenetik felaketi.
5. **Hipoksi ve Anjiyogenez:** VHL-HIF1α ekseni, kaotik tümör damarlanması ve anti-anjiyojenik tedaviye adaptif direnç.

> 🔴 **ÖNEMLİ:** Karsinojenez tek bir onkojenik olayla tamamlanamaz; malign fenotipin ortaya çıkabilmesi için hücrenin bağımsız sürücü (**driver**) mutasyonları basamaklı olarak biriktirmesi şarttır. Bu süreçte hücresel metabolizmanın anabolik yapıtaşlarını sentezleyecek şekilde yeniden organize edilmesi vazgeçilmez bir zorunluluktur.

> 🔵 **ÇIKMIŞ SORU:** Hücrelerin apoptoza gitmeksizin otonom ve sürekli çoğalma yeteneği kazanmasını sağlayan temel mekanizma, proto-onkogenlerin baskılanması değil, **non-lethal genetik mutasyonlar** yoluyla proto-onkogenlerin aktive olması ve tümör baskılayıcı genlerin inaktivasyonudur.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Karsinojenezin temelinde hücreyi öldürmeyen (**non-lethal**) genetik hasar yatar; hücre apoptozdan kaçarak transforme olur.",
            "🔵 ÇIKMIŞ SORU: Kanser hücrelerinin mikroçevre stresi altında hayatta kalmasını sağlayan temel adaptasyonlar metabolik yeniden programlanma ve immün kaçıştır.",
            "⚡ Tümörler başlangıçta monoklonaldir; büyüme ve metastaz sürecinde subklonal çeşitlilik (tümör heterojenitesi) kazanırlar."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Non-Lethal Hasar", "text": "Hücreyi öldürmeyen, yavru hücrelere aktarılan mutasyonel birikim."},
                {"label": "Genomik Bekçiler", "text": "RB ve TP53 eksenleri hücre siklusunu ve DNA bütünlüğünü denetler."},
                {"label": "Onkojenik Metabolizma", "text": "Warburg etkisi ve onkometabolitler tümörün biyosentez motorudur."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-1-1",
                "front": "Malign transformasyonu başlatan genetik hasarın temel niteliği nedir?",
                "back": "Non-lethal (ölümcül olmayan) mutasyondur; hücre nekroza gitmez, özerk büyüme kazanır.",
                "facultyNote": "Prof. Dr. Hikmet Keleş bu ilkenin karsinojenezin ilk adımı olduğunu vurgulamaktadır."
            },
            {
                "id": "itg-fc-1-2",
                "front": "Tümörlerin klonal başlangıcı ile ilerleyen evrelerdeki morfolojik/biyolojik çeşitliliği arasındaki ilişki nedir?",
                "back": "Başlangıçta monoklonal olan tümör, genetik instabilite sonucu subklonlar oluşturarak heterojenite kazanır.",
                "facultyNote": "Tedavi direnci geliştiren hücreler bu subklonlar arasından seleksiyona uğrar."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-1",
            "question": "Moleküler onkoloji prensiplerine göre, karsinojenez sürecini başlatan ve sürdüren hücresel genetik hasar tipiyle ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Hasar hücreyi hemen lizise ve koagülasyon nekrozuna götüren letal bir hasardır",
                "B) Hücreyi öldürmeyen (non-lethal) genetik hasar atasal hücrede klonal genişlemeyi başlatır",
                "C) Tümörler poliklonal kökenli olup her hücre bağımsız karsinojenik hasarla ortaya çıkar",
                "D) Malign transformasyon için tek bir sürücü mutasyon daima yeterlidir",
                "E) Genomik instabilite sadece benign neoplazmlarda görülen geçici bir adaptasyondur"
            ],
            "answer": "B",
            "explanation": "Karsinojenezin en temel ilkesi hasarın hücreyi öldürmeyen (non-lethal) olmasıdır. Hücre ölmez; mutasyonu taşıyarak klonal proliferasyona başlar ve monoklonal kökenden zamanla klonal heterojeniteye evrilir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 2,
        "title": "Retinoblastom (RB) Geni ve İki Vuruş (Two-Hit) Hipotezi",
        "subtitle": "Kromozom 13q14 lokusu, Knudson hipotezi, germline vs somatik inaktivasyon dinamikleri.",
        "badge": "Tümör Baskılayıcı",
        "badgeColor": "purple",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Retinoblastom sadece gözün nadir bir tümörü değildir; Knudson'ın 'iki vuruş' hipotezinin doğduğu ve tümör süpresör gen kavramının tıp literatürüne kazandırıldığı model hastalıktır.",
            "note": "Ailesel formda kalıtım soyağacında otozomal dominant gibi görünür; ancak hücresel düzeyde tümör oluşumu için iki alelin de kaybı gerektiğinden genetik etki resesiftir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Knudson'ın İki Vuruş (Two-Hit) Modeli ve RB1 Geni
Keşfedilen ilk tümör baskılayıcı gen, 13. kromozomun uzun kolunda (**13q14**) yer alan **RB1** genidir. Alfred Knudson 1971 yılında retinoblastom olgularının epidemiyolojik ve istatistiksel analizini yaparak tıp tarihine geçen "İki Vuruş (Two-Hit)" modelini formüle etmiştir. Bu kurala göre, tümör baskılayıcı bir genin koruyucu fonksiyonunun tamamen kaybolması ve malign transformasyonun tetiklenmesi için o genin **her iki fonksiyonel kopyasının (alelinin)** inaktive olması şarttır.

Hastalık iki farklı klinik ve genetik formda ortaya çıkar:
1. **Ailesel (Familyal / Kalıtsal) Retinoblastom (%40):**
   - Hastalar döllenme anında (zigotta) ebeveynlerinin birinden mutasyona uğramış veya delesif bir mutant RB1 alelini miras alırlar (**ilk vuruş germ hattındadır**).
   - Bu nedenle vücuttaki tüm somatik hücreler (tüm retina hücreleri dahil) tek bir fonksiyonel RB kopyasına sahiptir (heterozigottur).
   - Retinoblastom gelişimi için retina hücresinde sağlam olan ikinci alelin somatik olarak mutasyona uğraması veya delesyonu (**ikinci vuruş / heterozigosite kaybı - LOH**) yeterlidir.
   - **Klinik Yansıması:** Tümörler genellikle yaşamın ilk aylarında, **iki taraflı (bilateral)** ve **çok odaklı (multifokal)** olarak gelişir. En kritik nokta, bu çocukların ilerleyen yaşlarda başta **osteosarkom** olmak üzere yumuşak doku sarkomları ve melanom gibi sekonder maligniteler açısından devasa bir risk altında olmalarıdır.

2. **Sporadik Retinoblastom (%60):**
   - Çocuk anne ve babasından iki sağlam RB1 aleli miras alır; germ hattında mutasyon yoktur.
   - Tümörün gelişebilmesi için aynı retinal öncül hücrede iki bağımsız somatik mutasyonun peş peşe gerçekleşmesi gerekir.
   - İki bağımsız olayın aynı hücrede denk gelme olasılığı çok daha düşük olduğundan, tümörler genellikle daha geç yaşta, **tek taraflı (unilateral)** ve **tek odaklı (unifokal)** olarak ortaya çıkar. Sekonder osteosarkom riski bu grupta artmamıştır.

> 🔴 **ÖNEMLİ:** Ailesel retinoblastomda hastalığa yatkınlık aile ağacında **otozomal dominant** bir kalıtım paterni sergiler (çünkü vücuttaki milyonlarca retinal hücreden en az birinde ikinci vuruşun gerçekleşme olasılığı neredeyse %100'dür). Ancak hücresel ve moleküler düzeyde mutasyonun etkisi **resesiftir**; çünkü tek bir sağlam RB aleli bile hücreyi malign transformasyondan korumaya yeterlidir.

> 🔵 **ÇIKMIŞ SORU:** Retinoblastomlu bir çocukta ailesel formu sporadik formdan ayıran en güvenilir klinik/genetik özellikler: Tümörün **bilateral/multifokal** yerleşimi, erken yaşta ortaya çıkışı ve adolesan çağda **osteosarkom** gelişme riskinin yüksek olmasıdır.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Ailesel retinoblastomda birinci vuruş germ hattında olup tüm hücreler heterozigottur; ikinci vuruş retinal somatik mutasyondur (LOH).",
            "🔵 ÇIKMIŞ SORU: Ailesel retinoblastom hastalarında yaşamın ilerleyen dönemlerinde en sık görülen sekonder mezenkimal malignite **osteosarkom**dur.",
            "⚡ Kalıtım soyağacında yüksek penetranslı otozomal dominant görünür; fakat hücresel düzeyde tümör gelişimi alel kaybı gerektirdiğinden resesiftir."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Lokus", "text": "Kromozom 13q14, keşfedilen ilk tümör süpresör gen RB1."},
                {"label": "Two-Hit Kuralı", "text": "Tümör baskılayıcı fonksiyon kaybı için her iki alel inaktive olmalıdır."},
                {"label": "Klinik Dağılım", "text": "Ailesel tip bilateral/multifokal ve osteosarkom riski yüksek; sporadik tip unilateral."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-2-1",
                "front": "Knudson'ın iki vuruş hipotezine göre ailesel ve sporadik retinoblastom arasındaki temel mutasyonel fark nedir?",
                "back": "Aileselde ilk mutasyon germ hattındadır (tüm hücrelerde var), ikincisi somatiktir. Sporadikte her iki mutasyon da aynı retinal hücrede sonradan kazanılır.",
                "facultyNote": "Bu fark ailesel formun bilateralite ve sekonder tümör riskini açıklar."
            },
            {
                "id": "itg-fc-2-2",
                "front": "Ailesel retinoblastom genetik olarak neden 'pedigride dominant, hücresel düzeyde resesif' olarak tanımlanır?",
                "back": "Tek bir mutant alel hastalığı kuşaktan kuşağa taşır (dominant penetrans); fakat hücresel neoplastik transformasyon için sağlam ikinci kopyanın da kaybı (resesif mekanizma) şarttır.",
                "facultyNote": "TUS ve kurul sınavlarının klasik soru kalıbıdır."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-2",
            "question": "On sekiz aylık bir kız çocukta her iki gözde lökokori (beyaz refle) saptanmış ve yapılan incelemede bilateral retinoblastom teşhisi konulmuştur. Bu hastanın genetik patogenezi ve gelecekteki klinik riskleri ile ilgili aşağıdaki ifadelerden hangisi en doğrudur?",
            "options": [
                "A) Hastanın vücudundaki tüm somatik hücrelerde 13q14 lokusundaki her iki RB1 aleli de baştan beri mutasyonludur",
                "B) Tümör gelişimi için retina hücrelerinde sadece tek bir somatik mutasyon yeterli olmuştur",
                "C) Bu hastada adolesan dönemde osteosarkom gelişme riski genel popülasyondan farksızdır",
                "D) Hastalık ebeveynden otozomal resesif kalıtımla aktarılmış olup ikinci bir vuruşa ihtiyaç duyulmaz",
                "E) RB proteini sürekli hipofosforile kalarak E2F transkripsiyon faktörünü aşırı aktive etmiştir"
            ],
            "answer": "B",
            "explanation": "Bilateral retinoblastom ailesel formdur. Hasta germ hattında bir mutant alelle doğmuştur (tüm vücut hücreleri heterozigottur). Retina hücresinde tek bir ek somatik mutasyon (ikinci vuruş) meydana gelmesi iki alelin de kaybına ve tümör oluşumuna yeterlidir. Ayrıca bu hastalarda osteosarkom riski dramatik şekilde yüksektir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 3,
        "title": "RB Proteini, E2F Transkripsiyon Faktörleri ve G1/S Kontrol Noktası",
        "subtitle": "Hipofosforile aktif frenleme, kromatin modifikasyonu ve hiperfosforilasyonla E2F salınımı.",
        "badge": "Hücre Siklusu",
        "badgeColor": "blue",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Unutmayın: Fosforlanmamış veya hipofosforile RB aktif frendir! E2F'nin boğazına yapışır ve kromatini kilitler. Büyüme faktörleri gelip Siklin D/CDK4 ile RB'yi hiperfosforile ettiğinde fren boşalır, E2F serbest kalır ve hücre S fazına uçar.",
            "note": "Hipofosforile = Aktif fren (bölünmeyi durdurur). Hiperfosforile = İnaktif protein (bölünmeye izin verir). Bu kuralı asla karıştırmayın.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### RB Proteini ve G1/S Restriksiyon Noktası Moleküler Mekanizması
Hücre döngüsünün en kritik karar kapısı, hücrenin dış büyüme faktörlerine bağımlı olduğu G1 fazı ile DNA replikasyonunun başladığı ve otonom hale geldiği S fazı arasındaki geçiştir (**G1/S kontrol noktası / restriksiyon noktası**). Bu kapının ana nöbetçisi nükleer bir fosfoprotein olan **Retinoblastom (RB)** proteinidir.

RB proteininin moleküler aktivitesi doğrudan fosforilasyon durumuyla belirlenir:
1. **Hipofosforile RB (Aktif Form - Hücre Bölünmesini Durduran Fren):**
   - Durgun (G0) ve erken G1 fazındaki hücrelerde RB hipofosforile (az fosforlanmış) durumdadır.
   - Bu formda RB, **E2F ailesi** transkripsiyon faktörlerine sıkıca bağlanır ve onları fonksiyonel olarak tecrit eder (sekestre eder).
   - Yalnızca E2F'yi bağlamakla kalmaz; promoter bölgesine **Histon Deasetilaz (HDAC)** ve **Histon Metiltransferaz** enzimlerini davet eder. Bu enzimler histonlardaki asetil gruplarını koparıp kromatini sıkılaştırır (heterokromatin).
   - Sonuç: S fazına geçiş için şart olan genlerin (**Siklin E, Siklin A, DNA polimeraz, timidilat sentaz**) transkripsiyonu tam bir sessizliğe gömülür; hücre G1'de kilitlenir.

2. **Hiperfosforile RB (İnaktif Form - Hücre Bölünmesine İzin Veren Durum):**
   - Hücre büyüme faktörleri (EGF, PDGF vb.) ile uyarıldığında hücre içi sinyal yolakları (RAS-MAPK) **Siklin D** sentezini artırır.
   - Siklin D, **CDK4 ve CDK6** kinazları ile birleşerek aktif kompleksler kurar. Bu kompleksler RB proteinini fosforillemeye başlar.
   - Ardından devreye giren **Siklin E - CDK2** kompleksi RB'yi ileri derecede fosforilasyona uğratarak **hiperfosforile** hale getirir.
   - Hiperfosforilasyon RB proteininde konformasyonel değişikliğe yol açar; E2F transkripsiyon faktörü serbest kalır.
   - HDAC kompleksleri dağılır; serbest E2F hedef genlerin promoterlarına bağlanarak S fazı enzimlerinin ve Siklin E'nin transkripsiyonunu patlatır. Hücre geri dönüşümsüz olarak DNA replikasyonuna (S fazı) girer.

> 🔴 **ÖNEMLİ:** Kanser hücrelerinde RB ya doğrudan mutasyonla kaybolur ya da Siklin D/CDK4 aşırı aktivasyonu veya p16 kaybı nedeniyle **sürekli hiperfosforile ve inaktif** tutulur. Böylece G1/S kontrolü kalıcı olarak bypass edilir.

> 🔵 **ÇIKMIŞ SORU:** Hipofosforile RB'nin gen transkripsiyonunu baskılama mekanizması: **E2F transkripsiyon faktörlerini bağlayarak inaktive etmesi** ve kromatin yeniden şekillendirici histon deasetilazları (HDAC) bölgeye çekmesidir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Hipofosforile RB aktiftir; E2F'yi bağlayıp kromatini HDAC ile kapatarak G1/S geçişini bloke eder.",
            "🔵 ÇIKMIŞ SORU: RB'nin inaktivasyonu ve E2F'nin serbest kalması, **Siklin D-CDK4/6** ve **Siklin E-CDK2** komplekslerinin RB'yi hiperfosforile etmesiyle gerçekleşir.",
            "⚡ Hiperfosforile RB inaktiftir; fren kalktığı için hücre S fazına ve DNA sentezine engelsiz ilerler."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Hipofosforile Form", "text": "Aktif fren; E2F'yi hapseder, HDAC toplayarak S fazı genlerini kilitler."},
                {"label": "Hiperfosforile Form", "text": "İnaktif form; E2F serbest kalır, Siklin E ve DNA sentez genleri açılır."},
                {"label": "Kinaz Kompleksleri", "text": "Siklin D-CDK4/6 ve Siklin E-CDK2 fosforilasyonu gerçekleştiren motorlardır."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-3-1",
                "front": "RB proteininin aktif formu hangisidir ve hücre döngüsünü nasıl durdurur?",
                "back": "Hipofosforile formdur. E2F'yi bağlayarak transkripsiyonu engeller ve HDAC enzimlerini toplayarak kromatini kapatır.",
                "facultyNote": "Sınavlarda 'hiperfosforile aktif' yanıltmacası çok sık kurulur."
            },
            {
                "id": "itg-fc-3-2",
                "front": "RB proteininin hiperfosforilasyonunu başlatarak E2F'yi serbest bırakan ilk siklin-CDK kompleksi hangisidir?",
                "back": "Siklin D - CDK4/6 kompleksidir. Süreci Siklin E - CDK2 tamamlar.",
                "facultyNote": "Bu kompleksin aşırı çalışması kanserlerde temel hedeftir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-3",
            "question": "Hücre döngüsünün G1/S kontrol noktasında Retinoblastom (RB) proteininin fonksiyonel durumu ve moleküler etkileşimleri ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
            "options": [
                "A) Hipofosforile RB inaktif olup E2F'nin S fazı genlerini uyarmasına izin verir",
                "B) Hiperfosforile RB histon deasetilazları (HDAC) toplayarak kromatini transkripsiyona kapatır",
                "C) Hipofosforile RB E2F faktörlerini bağlayarak tecrit eder ve hücre döngüsünü G1'de durdurur",
                "D) Siklin D-CDK4/6 kompleksi RB'yi defosforile ederek aktif hale getirir",
                "E) E2F faktörlerinin serbest kalması için RB proteininin proteazomda tamamen parçalanması şarttır"
            ],
            "answer": "C",
            "explanation": "RB proteini hipofosforile iken aktiftir; E2F transkripsiyon faktörlerine bağlanarak onları inaktif tutar ve HDAC toplayarak S fazı genlerinin ifadesini kilitler. Siklin-CDK kompleksleri tarafından hiperfosforile edildiğinde ise inaktive olur ve E2F serbest kalır.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 4,
        "title": "Siklin D – CDK4/6 – p16 (CDKN2A) – RB Ekseni ve Onkojenik Bozulmalar",
        "subtitle": "G1/S regülasyonunun 4 kilit oyuncusu, p16 inaktivasyonu ve CDK4/6 inhibitörlerinin onkolojik başarısı.",
        "badge": "Hedefe Yönelik",
        "badgeColor": "emerald",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Amfide altını çizdiğim altın kural şudur: Kanser hücresi G1/S kapısını kırmak zorundadır. Bunu ya RB genini silerek yapar, ya Siklin D'yi çoğaltır, ya CDK4'ü azdırır ya da p16 frenini söker. Bu dört mekanizma birbirini dışlar ama sonuç aynıdır: RB'nin felç olması!",
            "note": "CDKN2A lokusu hem p16INK4A (CDK inhibitörü) hem de p14ARF (MDM2 inhibitörü) proteinlerini alternatif okuma çerçeveleriyle kodlayan istisnai bir gen bölgesidir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### G1/S Kontrol Ekseninin Onkojenik Düzensizliği
İnsan malignitelerinin neredeyse tamamında G1/S kontrol noktasının regülasyonu bozulmuştur. Bu kontrol mekanizması dört ana moleküler aktörün dengesi üzerine kuruludur: **Siklin D, CDK4/6, p16 (CDKN2A) ve RB**. Kanser hücresi bu dört faktörden birini mutasyona uğratarak RB'yi kalıcı olarak devre dışı bırakır. Genellikle bu mutasyonlar birbirini dışlayıcıdır (örneğin RB geni doğrudan inaktive olmuş bir küçük hücreli akciğer karsinomunda p16 kaybına veya Siklin D artışına ihtiyaç kalmaz).

Bu ekseni bozan temel onkojenik mekanizmalar şunlardır:
1. **Siklin D Aşırı Ekspresyonu ve Amplifikasyonu:**
   - **CCND1** geni amplifikasyonu meme karsinomlarının yaklaşık %15-20'sinde saptanır.
   - Mantle hücreli lenfomada **t(11;14)** translokasyonu sonucu Siklin D1 geni immünglobülin ağır zincir (IgH) enhancerı altına girerek aşırı üretilir.
2. **CDK4 Aktivasyonu ve Amplifikasyonu:**
   - Glioblastom, melanom ve sarkomlarda CDK4 gen amplifikasyonu veya p16'ya bağlanmayı engelleyen aktive edici missense mutasyonlar görülür.
3. **p16INK4A (CDKN2A) Gen İnaktivasyonu:**
   - p16, CDK4 ve CDK6 kinazlarına spesifik olarak bağlanıp onları inhibe eden doğal tümör baskılayıcı bir proteindir.
   - 9p21 lokusundaki **CDKN2A** geni; homozigot delesyon, mutasyon veya promoter CpG hipermetilasyonu yoluyla inaktive edilir.
   - Pankreas adenokarsinomlarının %75'inde, glioblastomların %50'sinde, melanom ve baş-boyun skuamöz hücreli karsinomlarında CDKN2A kaybı en sık rastlanan genetik defekttir.

Klinik ve Terapötik Devrim: **CDK4/6 İnhibitörleri**
Bu moleküler biyolojinin kliniğe en büyük armağanı, RB geni sağlam olan tümörlerde (özellikle Hormon Reseptörü pozitif, HER2 negatif metastatik meme kanseri) geliştirilen oral selektif CDK4/6 inhibitörleridir (**Palbosiklib, Ribosiklib, Abemasiklib**). Bu ilaçlar CDK4/6 kinaz aktivitesini bloke ederek RB'nin hiperfosforile olmasını engeller; RB hipofosforile (aktif) durumda kalarak tümör hücresini G1 fazında dondurur ve proliferasyonu durdurur.

> 🔴 **ÖNEMLİ:** CDKN2A lokusu tek bir genden iki farklı tümör baskılayıcı protein üretir: **p16INK4A** (CDK4/6'yı inhibe ederek RB yolunu korur) ve **p14ARF** (MDM2'yi inhibe ederek p53'ü korur). CDKN2A delesyonu her iki ana bekçiyi (RB ve p53) aynı anda sakatlar!

> 🔵 **ÇIKMIŞ SORU:** Mantle hücreli lenfomada t(11;14)(q13;q32) translokasyonu sonucu aşırı üretilerek RB fosforilasyonunu ve G1/S geçişini hızlandıran protein **Siklin D1**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: CDKN2A lokusu p16INK4A (RB yolu) ve p14ARF (p53 yolu) olmak üzere iki kritik tümör süpresör proteini birden kodlar.",
            "🔵 ÇIKMIŞ SORU: Mantle hücreli lenfomada t(11;14) translokasyonu ile regülasyonu bozulan ve RB hiperfosforilasyonuna yol açan siklin tipi **Siklin D1**dir.",
            "⚡ CDK4/6 inhibitörleri (Palbosiklib vb.) RB'nin hipofosforile aktif kalmasını sağlayarak tümör hücrelerini G1 fazında durdurur."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Dörtlü Eksen", "text": "Siklin D, CDK4, p16, RB dengesi karsinojenezde mutlaka bozulur."},
                {"label": "CDKN2A Önemi", "text": "p16 kaybı pankreas karsinomu, melanom ve glioblastomda çok yaygındır."},
                {"label": "Farmakolojik Hedef", "text": "Palbosiklib/Ribosiklib CDK4/6'yı inhibe ederek RB frenini devrede tutar."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-4-1",
                "front": "CDKN2A gen delesyonu neden hem RB hem de p53 yollarını aynı anda çökertir?",
                "back": "Çünkü bu lokus alternatif okuma çerçevesiyle hem p16INK4A'yı (RB koruyucusu) hem de p14ARF'yi (MDM2'yi baskılayıp p53'ü koruyan protein) kodlar.",
                "facultyNote": "Tıbbi patolojide en zarif ve tehlikeli iki yönlü genetik kayıptır."
            },
            {
                "id": "itg-fc-4-2",
                "front": "Metastatik meme kanserinde kullanılan CDK4/6 inhibitörlerinin etki gösterebilmesi için tümörde hangi proteinin sağlam olması zorunludur?",
                "back": "Fonksiyonel RB proteininin bulunması şarttır; çünkü ilaç RB'yi hipofosforile tutarak etki eder.",
                "facultyNote": "RB mutant bir tümörde CDK4/6 inhibitörü tamamen etkisizdir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-4",
            "question": "Pankreas adenokarsinomu ve kutanöz malign melanomda çok yüksek oranda inaktive olan, 9p21 kromozom lokusunda kodlanan ve CDK4/6 komplekslerini fizyolojik olarak inhibe ederek RB proteininin hipofosforile kalmasını sağlayan tümör baskılayıcı molekül aşağıdakilerden hangisidir?",
            "options": [
                "A) p21CIP1 (CDKN1A)",
                "B) p16INK4A (CDKN2A)",
                "C) p27KIP1 (CDKN1B)",
                "D) Siklin E1",
                "E) MDM2"
            ],
            "answer": "B",
            "explanation": "CDKN2A geninin ürünü olan p16INK4A, CDK4 ve CDK6 kinazlarına bağlanarak onların Siklin D ile birleşip RB'yi fosforillemesini engeller. Bu genin delesyon veya metilasyonu pankreas kanseri ve melanomda RB inaktivasyonunun en sık nedenidir.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 5,
        "title": "Onkojenik DNA Virüsleri ve RB / p53 İnaktivasyonu",
        "subtitle": "HPV E6 ve E7 onkoproteinleri, viral onkogenez stratejileri ve hücresel bekçilerin gaspı.",
        "badge": "Viral Onkogenez",
        "badgeColor": "red",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Onkojenik DNA virüsleri evrimin en kurnaz parazitleridir. Hücreyi kendi genomlarını çoğaltmaya zorlamak için tek bir hamleyle hücrenin iki ana bekçisini yok ederler: HPV E7 proteini RB'yi felç eder, E6 ise p53'ü çöpe yollar!",
            "note": "Yüksek riskli HPV tiplerinde (Tip 16 ve 18) E6 ve E7'nin hücresel hedeflere afinitesi düşük riskli siğil tiplerine kıyasla katbekat yüksektir.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### Onkojenik DNA Virüslerinin Hücre Döngüsü Kontrol Mekanizmalarını Gasbetmesi
Bazı DNA tümör virüsleri konak hücreyi transforme etmek ve kendi viral genom replikasyonlarını başlatabilmek için doğrudan hücre döngüsü bekçilerini hedefleyen onkoproteinler üretirler. Virüsün bölünmeyen (G0 evresindeki) bir epitel hücresinde çoğalabilmesi için hücreyi zorla S fazına sokması ve bu sırada tetiklenecek apoptozu engellemesi gerekir.

Bu stratejinin prototipi **Human Papillomavirus (HPV)** yüksek riskli tipleridir (Tip 16, 18, 31, 33 - Serviks karsinomu, anogenital ve orofaringeal kanser etkenleri):
1. **HPV E7 Onkoproteini (RB Yolunun Çökertilmesi):**
   - E7 proteini, hücredeki hipofosforile (aktif) RB proteinine son derece yüksek bir afiniteyle bağlanır.
   - RB-E2F kompleksini parçalayarak **E2F transkripsiyon faktörünü zorla serbest bırakır**.
   - Ayrıca E7; p21CIP1 ve p27KIP1 gibi siklin bağımlı kinaz inhibitörlerine de bağlanarak onları inaktive eder.
   - Sonuç: Hücre dış büyüme faktörü uyarısına ihtiyaç duymadan, G1/S kontrol noktasını atlayarak hızla S fazına ve DNA sentezine geçer.

2. **HPV E6 Onkoproteini (p53 Yolunun ve Apoptozun Yok Edilmesi):**
   - Normal bir hücrede RB inaktive edilip E2F aniden serbest kaldığında, p14ARF aktive olur ve p53 düzeyleri fırlar; kontrolsüz replikasyon stresine giren hücre hızla apoptoza gönderilir.
   - İşte HPV bu koruyucu intihar mekanizmasını **E6 proteini** ile bertaraf eder.
   - E6, hücresel bir E3 ubikitin ligaz olan **E6AP (E6-Associated Protein)** ile birleşir.
   - Bu kompleks doğrudan p53 proteinine bağlanarak onu poliubikitinler ve **26S proteazomda süratle parçalatır**.
   - p53 düzeyleri sıfırlandığı için hücre ne apoptoza gidebilir ne de DNA tamiri yapabilir. Ek olarak E6, **TERT (telomeraz)** ekspresyonunu aktive ederek hücreye ölümsüzlük kazandırır.

Diğer Onkojenik DNA Virüslerinin Paralel Mekanizmaları:
- **Adenovirüs:** **E1A** proteini RB'ye bağlanıp inaktive ederken; **E1B** proteini p53'e bağlanıp onu etkisiz hale getirir.
- **Simian Virus 40 (SV40):** Tek bir viral protein olan **Large T antijeni**, hem RB'ye hem de p53'e eş zamanlı bağlanarak her iki bekçiyi tek başına nötralize eder.

> 🔴 **ÖNEMLİ:** Yüksek riskli HPV tiplerinde viral genom konakçı DNA'sına entegre olur. Entegrasyon sırasında viral E2 represör geni kırılır; E2 baskısı kalkan **E6 ve E7 onkoproteinleri aşırı ve kontrolsüz şekilde transkribe edilmeye başlar**.

> 🔵 **ÇIKMIŞ SORU:** Yüksek riskli HPV enfeksiyonlarında serviks karsinogenezinde rol oynayan viral onkoproteinlerin etkileri: **E7 hipofosforile RB'ye bağlanıp E2F'yi serbest bırakır**; **E6 ise p53'ü ubikitin-proteazom yolağı ile parçalanmaya yönlendirir**.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: Yüksek riskli HPV E7 proteini hipofosforile RB'ye bağlanıp E2F'yi serbest bırakır; ayrıca p21 ve p27'yi inhibe eder.",
            "🔵 ÇIKMIŞ SORU: HPV E6 proteini konakçı hücresinde p53'e bağlanarak onu **ubikitin-proteazom** sistemi üzerinden yıkıma gönderir ve apoptozu engeller.",
            "⚡ Adenovirüste E1A RB'yi, E1B p53'ü bağlar; SV40 Large T antijeni ise her iki proteini tek başına inaktive eder."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "HPV E7 Etkisi", "text": "Hipofosforile RB'yi bağlar, E2F'yi serbest bırakır, G1/S'yi bypass eder."},
                {"label": "HPV E6 Etkisi", "text": "E6AP ile p53'ü proteazomal yıkıma gönderir, TERT'i aktive eder."},
                {"label": "Entegrasyon Sonucu", "text": "E2 geni kopunca E6 ve E7'nin kontrolsüz transkripsiyonu başlar."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-5-1",
                "front": "HPV E7 onkoproteininin konak hücre siklusundaki birincil moleküler hedefi ve eylemi nedir?",
                "back": "Hipofosforile RB'ye bağlanarak E2F transkripsiyon faktörünü serbest bırakmak ve p21/p27'yi baskılamaktır.",
                "facultyNote": "Böylece hücre kontrolsüz biçimde S fazına sürüklenir."
            },
            {
                "id": "itg-fc-5-2",
                "front": "HPV E6 proteini p53'ü hangi hücresel mekanizmayı kullanarak ortadan kaldırır?",
                "back": "E6AP ubikitin ligazını kullanarak p53'ü ubikitinler ve 26S proteazomunda parçalatır.",
                "facultyNote": "Bunun sonucunda p53 aracılı apoptoz tamamen engellenir."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-5",
            "question": "Serviks skuamöz hücreli karsinomu patogenezinde yüksek riskli Human Papillomavirus (HPV) tip 16 onkoproteinlerinin konak hücre siklus bekçileri üzerindeki etkileri ile ilgili aşağıdaki eşleştirmelerden hangisi doğrudur?",
            "options": [
                "A) E6: RB'yi defosforile eder — E7: p53'ü fosforilleyerek stabilize eder",
                "B) E7: Hipofosforile RB'ye bağlanıp E2F'yi serbest bırakır — E6: p53'ü proteazomal yıkıma hedefler",
                "C) E6: CDK4'ü inhibe eder — E7: MDM2'yi parçalayarak p53'ü artırır",
                "D) E7: E-kadherin sentezini artırır — E6: Telomeraz aktivitesini tamamen susturur",
                "E) E7: Siklin D yıkımını uyarır — E6: Kaspaz-3 aktivasyonunu doğrudan tetikler"
            ],
            "answer": "B",
            "explanation": "HPV'nin yüksek riskli tiplerinde E7 onkoproteini hipofosforile RB'ye bağlanıp E2F'yi serbest bırakarak hücreyi S fazına sokar; E6 onkoproteini ise p53'ü E6AP aracılığıyla ubikitinleyip proteazomda yıkarak apoptozdan kaçışı sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    },
    {
        "slideNumber": 6,
        "title": "TP53: Genomun Baş Muhafızı (Guardian of the Genome)",
        "subtitle": "Kromozom 17p13.1, stres sensör kinazları (ATM/ATR) ve MDM2 ubikitin ligaz döngüsü.",
        "badge": "Genom Koruyucu",
        "badgeColor": "amber",
        "discipline": "Tıbbi Patoloji",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "professorAudioHighlight": {
            "quote": "Tümör patolojisinin tartışmasız kralı TP53'tür. İnsan kanserlerinin yarısından fazlasında doğrudan mutasyona uğramıştır; geri kalanında ise MDM2 gibi ortakları üzerinden susturulmuştur. O hücrenin vicdanıdır; DNA tamir edilemiyorsa hücreyi gözünü kırpmadan ölüme yollar!",
            "note": "Normal hücrede p53 sürekli üretilir ama MDM2 tarafından derhal parçalanır; yarı ömrü sadece 20 dakikadır. Stres anında fosforillenerek MDM2'nin pençesinden kurtulur.",
            "emphasisType": "high_yield"
        },
        "synthesisNarrative": """### TP53 Geni ve Moleküler Stres Sensör Ağı
Kromozom 17'nin kısa kolunda (**17p13.1**) haritalanan **TP53** geni, tıp literatüründe haklı olarak "Genomun Baş Muhafızı (Guardian of the Genome)" unvanını taşır. İnsan malign tümörlerinin %50'sinden fazlasında TP53 geninde somatik inaktive edici mutasyonlar veya delesyonlar mevcuttur; bu oran TP53'ü kanserde en sık bozulan tekil gen yapmaktadır.

Stres Altında Olmayan Sağlıklı Hücrede p53 Dinamiği:
- Normal fizyolojik koşullarda hücrede yüksek düzeyde p53 bulunması toksiktir; çünkü hücre döngüsünü durdurabilir veya apoptozu tetikleyebilir.
- Bu nedenle p53 proteini sürekli sentezlenmesine rağmen yarı ömrü son derece kısadır (~20 dakika).
- Düzeyin düşük tutulmasını sağlayan ana molekül, bir E3 ubikitin ligaz olan **MDM2** proteinidir.
- MDM2, p53'ün transaktivasyon alanına bağlanır; onu nükleustan sitoplazmaya ihraç eder ve üzerine ubikitin zincirleri ekleyerek 26S proteazomda parçalanmaya yönlendirir.

Stres Uyarısı ve p53'ün Kurtuluşu:
Hücre iyonizan radyasyon (çift zincir DNA kırıkları), ultraviyole ışık (timin dimerleri), karsinojenik kimyasallar, hipoksi veya onkojenlerin aşırı sinyalleriyle karşılaştığında devasa bir alarm ağı devreye girer:
1. **Kinaz Sensörlerinin Aktivasyonu:** Çift zincir DNA kırıklarında **ATM (Ataxia Telangiectasia Mutated)**, tek zincir kırıkları ve replikasyon stresinde **ATR (ATM-and-Rad3-related)** kinazları derhal aktive olur.
2. **Fosforilasyon Kalkanı:** ATM ve efektör kinazlar (Chk1, Chk2), p53 proteinini amino-terminalindeki kritik serin ve treonin kalıntılarından (özellikle Ser15 ve Ser20) hızla fosforiller.
3. **MDM2'den Kopuş ve Stabilizasyon:** Fosforilasyon p53'ün MDM2 ile etkileşen yüzeyinde elektrostatik itme yaratır; MDM2 artık p53'e bağlanamaz!
4. **Birikim ve Tetramerleşme:** Yıkımdan kurtulan p53 hızla stabilize olur, nükleusta seviyesi dramatik biçimde yükselir. p53 homotetramerler oluşturarak spesifik DNA promotör dizilerine bağlanır ve yüzlerce hedef genin transkripsiyonunu başlatır.

> 🔴 **ÖNEMLİ:** p53 aynı zamanda kendi inhibitörü olan **MDM2 geninin transkripsiyonunu da uyarır**. Bu zarif negatif geri bildirim (oto-regülasyon) döngüsü sayesinde, DNA hasarı tamir edildikten sonra yükselen MDM2 p53'ü tekrar yıkarak hücre döngüsünün yeniden başlamasını sağlar.

> 🔵 **ÇIKMIŞ SORU:** Hücre içi p53 düzeyini düşük seviyelerde tutan, p53'e bağlanarak onu ubikitinleyen ve proteazomal yıkımını sağlayan temel negatif düzenleyici molekül **MDM2**dir.""",
        "spotPearls": [
            "🔴 ÖNEMLİ: TP53 (17p13.1) insan kanserlerinde en sık mutasyona uğrayan gendir; stres yokken MDM2 tarafından sürekli proteazomda yıkılır.",
            "🔵 ÇIKMIŞ SORU: DNA hasarında ATM/ATR kinazları p53'ü fosforilleyerek **MDM2'den ayrılmasını** ve nükleusta birikerek stabilize olmasını sağlar.",
            "⚡ p53 aktif bir transkripsiyon faktörü olarak homotetramer yapısında DNA promoterlarına bağlanır."
        ],
        "coreContent": {
            "keyBullets": [
                {"label": "Lokus ve Önemi", "text": "17p13.1, insan kanserlerinin %50'sinden fazlasında mutasyona uğrar."},
                {"label": "MDM2 Rolü", "text": "E3 ubikitin ligaz; p53'ü bağlayıp 26S proteazomal yıkıma gönderir."},
                {"label": "Stres Sensörleri", "text": "ATM/ATR ve Chk1/Chk2 p53'ü fosforilleyerek MDM2'den kurtarır."}
            ]
        },
        "flashcards": [
            {
                "id": "itg-fc-6-1",
                "front": "Sağlıklı bir hücrede p53 proteininin yarı ömrünü ~20 dakikada tutan temel enzim hangisidir?",
                "back": "MDM2 (E3 ubikitin ligaz) enzimidir; p53'ü ubikitinleyerek proteazomda parçalatır.",
                "facultyNote": "MDM2 geni aşırı amplifiye olduğunda p53 yabani tip olsa bile işlevsiz kalır."
            },
            {
                "id": "itg-fc-6-2",
                "front": "DNA çift zincir kırığı algılandığında p53'ü stabilize eden sinyal kaskadı nasıl çalışır?",
                "back": "ATM kinazı aktive olur, Chk2 ile birlikte p53'ün N-ucunu fosforiller; MDM2 bağlanamaz ve p53 nükleusta birikir.",
                "facultyNote": "Ataksi telenjiektazide ATM mutasyonu bu nedenle kanser yatkınlığı yapar."
            }
        ],
        "practiceQuestion": {
            "id": "itg-pq-6",
            "question": "Normal hücresel koşullarda p53 düzeylerinin son derece düşük tutulmasını sağlayan, stres anında ise ATM kinaz aracılı fosforilasyon nedeniyle p53'e bağlanamayarak onun nükleer birikimine izin veren moleküler düzenleyici aşağıdakilerden hangisidir?",
            "options": [
                "A) MDM2",
                "B) E2F1",
                "C) p21CIP1",
                "D) BAX",
                "E) GADD45"
            ],
            "answer": "A",
            "explanation": "MDM2 bir E3 ubikitin ligaz olup p53'e bağlanarak onu proteazomal yıkıma hedefler. Hücre DNA hasarına uğradığında ATM/ATR kinazları p53'ü fosforiller; bu fosforilasyon p53'ün MDM2'den ayrılmasını ve hücrede birikerek tetramer oluşturmasını sağlar.",
            "isPracticeQuestion": True,
            "deckId": "learn-ileri-tumor-genetigi-metabolizmasi",
            "discipline": "Tıbbi Patoloji"
        }
    }
]
