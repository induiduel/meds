from meds.scripts.deck_generators.builder_helper import make_slide, make_cloze, make_table, make_chain, make_recall, make_spot_lie, make_quiz

def get_sec4():
    slides = []

    # Slide 31
    slides.append(make_slide(
        title="Latent Sifiliz Tanımı ve Asemptomatik Dönemin Başlangıcı",
        narrative="""Sekonder sifiliz belirtilerinin kendiliğinden (tedavisiz) gerilemesiyle birlikte hastalık **Latent Sifiliz** (Gizli Sifiliz) evresine girer. Latent evre, klinik olarak hastanın tamamen sağlıklı göründüğü ancak enfeksiyonun vücutta hala varlığını sürdürdüğü bir 'sessizlik' dönemidir.

Latent sifilizin temel kriterleri:
* **Klinik Belirti Yokluğu:** Döküntü, LAP, şankr veya herhangi bir organ disfonksiyonu yoktur. Hastanın hiçbir şikayeti bulunmaz.
* **Serolojik Pozitiflik:** Hastalık sadece laboratuvar testleriyle saptanabilir. Hem treponemal (örn. TPHA, FTA-ABS) hem de non-treponemal (örn. VDRL, RPR) testler pozitiftir.
* **Normal BOS Bulguları:** Merkezi sinir sistemi (SSS) tutulumu (nörosifiliz) veya kardiyovasküler sifiliz bulgusu yoktur.

> Latent sifiliz, klinik olarak tanınması imkansız olan bir evredir. Bu hastalar ancak rutin kan taramaları (gebelik, kan bağışı, ameliyat öncesi) veya temaslı taraması sırasında tesadüfen saptanırlar.""",
        elements=[
            make_cloze("Sekonder bulguların sönmesiyle başlayan, hastanın asemptomatik olduğu ancak serolojik testlerin reaktif (pozitif) kaldığı evreye {{Latent}} sifiliz denir."),
            make_cloze("Latent sifiliz evresinde nörosifiliz dışlandığı için Beyin Omurilik Sıvısı (BOS) bulguları tamamen {{normaldir}}."),
            make_table(
                headers=["Değerlendirme Parametresi", "Latent Sifilizdeki Durumu"],
                rows=[
                    ["Klinik Belirtiler (Şikayetler)", "Yok (Asemptomatik)"],
                    ["Fizik Muayene Bulguları", "Tamamen normal (Lezyon veya LAP yok)"],
                    ["Serolojik Testler (Kan)", "Pozitif (Reaktif)"],
                    ["BOS Analizi", "Normal (Nörosifiliz bulgusu yok)"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Latent Sifiliz Tanımı",
                [
                    {"text": "Latent sifiliz, klinik bulguların olmadığı ancak serolojik testlerin pozitif olduğu asemptomatik bir evredir.", "isLie": False, "explanation": "Doğru, bu evre tamamen laboratuvar ile saptanır."},
                    {"text": "Bu evredeki hastalar genellikle rutin kan bağışı veya gebelik taramalarında tesadüfen teşhis edilirler.", "isLie": False, "explanation": "Doğru, klinik bir şikayet olmadığı için taramalarla bulunur."},
                    {"text": "Latent sifiliz diyebilmek için hastada hafif de olsa makülopapüler döküntülerin devam etmesi şarttır.", "isLie": True, "explanation": "Yanlış! Latent evrenin en temel özelliği HİÇBİR klinik bulgunun olmamasıdır. Döküntü varsa sekonder evrededir."}
                ]
            ),
            make_quiz(
                question="Bir hastaya 'Latent Sifiliz' tanısı konulabilmesi için aşağıdakilerden hangisinin BİR ARADA bulunması gerekir?",
                options=[
                    "Şankr varlığı + VDRL pozitifliği",
                    "Yaygın döküntü + BOS'ta pleositoz",
                    "Klinik semptom yokluğu + Serolojik pozitiflik + Normal BOS bulguları",
                    "Aort anevrizması + TPHA pozitifliği",
                    "Epitroklear LAP + VDRL negatifliği"
                ],
                answer="Klinik semptom yokluğu + Serolojik pozitiflik + Normal BOS bulguları",
                explanation="Latent sifilizin üç saç ayağı vardır: Klinik olarak asemptomatik olmak, kanda sifiliz testlerinin (seroloji) pozitif olması ve SSS/kardiyovasküler tutulumun (normal BOS vb.) dışlanması."
            )
        ]
    ))

    # Slide 32
    slides.append(make_slide(
        title="Erken Latent Sifiliz (İlk 1 Yıl) ve Epidemiyolojik Önemi",
        narrative="""Latent sifiliz, hastalığın bulaşıcılık potansiyeline ve relaps (nüks) riskine göre zamansal olarak ikiye ayrılır: Erken ve Geç. **Erken Latent Sifiliz**, enfeksiyonun bulaşmasından itibaren geçen sürenin **1 yıldan daha az** (bazı kılavuzlara göre ilk 1 yıl) olduğu dönemdir.

Erken Latent Evrenin Kritik Özellikleri:
* **Yüksek Bulaşıcılık (İnfektivite):** Erken latent dönemdeki hastalar, klinik olarak hiçbir lezyonları olmamasına rağmen cinsel partnerlerine enfeksiyonu bulaştırabilirler. Spiroketemi atakları dönem dönem devam eder.
* **Mukokutanöz Relaps Riski:** Hastaların büyük çoğunluğunda sekonder sifiliz bulguları (döküntüler, kondiloma lata vb.) bu ilk 1 yıl içinde aniden tekrarlayabilir (relaps).
* **Epidemiyolojik Öncelik:** Bulaş riski nedeniyle halk sağlığı açısından temaslı takibi ve acil tedavisi en elzem gruplardan biridir.

> Bir hasta asemptomatik olsa bile, enfeksiyonu son 1 yıl içinde almışsa 'Erken Latent' kabul edilir ve cinsel yolla bulaştırma potansiyeli yüksektir. Erken ve geç evre ayrımı, bulaşıcılık ve tedavi süresi açısından çok önemlidir.""",
        elements=[
            make_cloze("Enfeksiyonun bulaşından itibaren 1 yıldan daha kısa süre geçmiş asemptomatik döneme {{Erken Latent}} sifiliz denir."),
            make_cloze("Erken latent dönemdeki hastalar klinik olarak sağlıklı görünseler de cinsel yolla enfeksiyonu {{bulaştırabilirler}} (yüksek infektivite)."),
            make_table(
                headers=["Latent Sifiliz Özelliği", "Erken Latent Dönemdeki Durumu"],
                rows=[
                    ["Zaman Dilimi", "Enfeksiyondan sonraki İlk 1 Yıl"],
                    ["Klinik Görünüm", "Asemptomatik (şikayet yok)"],
                    ["Bulaştırıcılık (Cinsel Yolla)", "Var (Spiroketemi atakları nedeniyle bulaşıcıdır)"],
                    ["Sekonder Bulgu Relaps Riski", "Çok yüksek"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken Latent Sifiliz",
                [
                    {"text": "Erken latent sifiliz, primer enfeksiyondan sonraki ilk 1 yılı kapsayan asemptomatik dönemdir.", "isLie": False, "explanation": "Doğru, erken latent tanımı ilk 1 yılı kapsar."},
                    {"text": "Erken latent dönemde mukokutanöz sekonder sifiliz bulgularının tekrarlama (relaps) riski mevcuttur.", "isLie": False, "explanation": "Doğru, relapsların büyük kısmı bu dönemde yaşanır."},
                    {"text": "Erken latent evredeki bir hasta, derisinde lezyon olmadığı için cinsel partnerine kesinlikle hastalık bulaştıramaz.", "isLie": True, "explanation": "Yanlış! Erken latent evredeki hastalar, gözle görülür lezyonları olmasa bile dönem dönem spiroketemi (kana mikrop karışması) yaşadıkları için bulaştırıcıdırlar."}
                ]
            ),
            make_quiz(
                question="Asemptomatik bir hastanın kan tahlillerinde VDRL ve TPHA pozitif saptanmıştır. Yapılan derinleşmiş anamnezde, hastanın 6 ay önce şüpheli cinsel temas öyküsü ve sonrasında kaybolan ağrısız bir genital ülseri olduğu öğrenilmiştir. Bu hastanın evresi aşağıdakilerden hangisidir?",
                options=[
                    "Primer sifiliz",
                    "Sekonder sifiliz",
                    "Erken latent sifiliz",
                    "Geç latent sifiliz",
                    "Tersiyer sifiliz"
                ],
                answer="Erken latent sifiliz",
                explanation="Hasta asemptomatik ve serolojisi pozitif olduğu için 'latent' evrededir. Enfeksiyon süresi 1 yıldan kısa (6 ay) olduğu için spesifik olarak 'Erken Latent' sifiliz tanısı alır."
            )
        ]
    ))

    # Slide 33
    slides.append(make_slide(
        title="Geç Latent Sifiliz (>1 Yıl) ve Klinik Özellikleri",
        narrative="""Enfeksiyonun bulaşmasından itibaren **1 yıldan daha uzun** süre geçmiş (veya enfeksiyon süresi tam olarak bilinmeyen) asemptomatik döneme **Geç Latent Sifiliz** denir. Bu evre, enfeksiyon dinamiklerinin değiştiği, bağışıklık sisteminin spiroketleri dokulara hapsettiği daha stabil bir dönemdir.

Geç Latent Evrenin Kritik Özellikleri:
* **Düşük Cinsel Bulaşıcılık:** İlk 1 yıldan sonra spiroketemi atakları son derece nadir hale gelir. Bu nedenle geç latent sifilizli bireylerin cinsel partnerlerine enfeksiyonu bulaştırma ihtimali oldukça düşüktür (pratikte bulaştırıcı kabul edilmezler).
* **Bağışıklık (Direnç):** Bu evredeki hastalar, yeni T. pallidum suşlarıyla tekrar enfekte olmaya (süperenfeksiyon) karşı büyük oranda dirençlidir.
* **Gelecek Riski (Tersiyer):** Bulaştırıcılık azalsa da, spiroketler vasküler ve sinir dokularında sessizce bekler. Geç latent evre, yıkıcı tersiyer sifiliz (kardiyovasküler ve nörosifiliz) tablosunun gelişimi için öncü dönemdir.

> Süresi bilinmeyen (latent sifiliz - süresi belirsiz) vakalar her zaman 'Geç Latent' gibi kabul edilip buna göre (daha uzun) tedavi edilir. Geç latent evrede bulaştırıcılık azdır ancak organ hasarı riski (tersiyer dönem için) birikmektedir.""",
        elements=[
            make_cloze("Enfeksiyonun bulaşmasından itibaren 1 yıldan daha uzun süre geçmiş asemptomatik döneme {{Geç Latent}} sifiliz denir."),
            make_cloze("Geç latent dönemde spiroketemi atakları nadirleştiği için cinsel yolla enfeksiyon {{bulaştırıcılığı}} oldukça düşüktür."),
            make_table(
                headers=["Özellik", "Erken Latent (<1 Yıl)", "Geç Latent (>1 Yıl)"],
                rows=[
                    ["Cinsel Bulaştırıcılık", "Yüksek", "Çok düşük / Pratik olarak yok"],
                    ["Relaps Riski (Sekonder Bulgular)", "Yüksek (%25 civarı)", "Yok denecek kadar az"],
                    ["Yeni Enfeksiyona Direnç", "Kısmi", "Yüksek (Süperenfeksiyona dirençli)"],
                    ["Tedavi Süresi (Penisilin G)", "Tek doz genellikle yeterli", "Uzun süreli (3 hafta haftada bir doz) gerekir"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Geç Latent Sifiliz",
                [
                    {"text": "Geç latent sifiliz, bulaştan itibaren 1 yıldan daha uzun süre geçmiş asemptomatik vakaları tanımlar.", "isLie": False, "explanation": "Doğru, zaman sınırı genellikle 1 yıldır (DSÖ'ye göre 2 yıl olabilse de çoğu kılavuz 1 yıl alır)."},
                    {"text": "Geç latent dönemdeki hastalar, yeni Treponema pallidum enfeksiyonlarına (süperenfeksiyon) büyük oranda dirençlidir.", "isLie": False, "explanation": "Doğru, immünite stabilleşmiştir."},
                    {"text": "Geç latent sifilizli hastalar, erken latentlere göre cinsel partnerlerine çok daha yüksek oranda enfeksiyon bulaştırırlar.", "isLie": True, "explanation": "Yanlış! Geç latent evrede spiroketemi olmadığı için cinsel yolla bulaştırıcılık oldukça düşüktür, asıl bulaştırıcı olan erken latenttir."}
                ]
            ),
            make_quiz(
                question="Rutin taramada sifiliz testleri pozitif çıkan 45 yaşında bir hastanın, klinik hiçbir bulgusu yoktur ve son 5 yıldır hiçbir cinsel teması olmamıştır. Bu hasta için en uygun tanım aşağıdakilerden hangisidir?",
                options=[
                    "Sekonder sifiliz",
                    "Erken latent sifiliz",
                    "Geç latent sifiliz",
                    "Asemptomatik nörosifiliz",
                    "Sifilitik aortit"
                ],
                answer="Geç latent sifiliz",
                explanation="Hastanın asemptomatik olması ve son 5 yıldır temasının olmaması (enfeksiyonun >1 yıl önce alındığını gösterir) durumu 'Geç Latent Sifiliz' ile uyumludur."
            )
        ]
    ))

    # Slide 34
    slides.append(make_slide(
        title="Latent Dönemde Mukokutanöz Relaps Dinamiği (İlk Yılda %75-90 Relaps Riski)",
        narrative="""Tedavi edilmeyen sifilizin doğal seyrinde bağışıklık sistemi ile spiroketler arasındaki denge tam oturana kadar dalgalanmalar yaşanır. Latent evreye geçen bir hastada klinik belirtiler aniden tekrar ortaya çıkabilir; bu duruma **relaps (nüks)** denir.

Relaps dinamikleri hakkında kritik bilgiler:
* **Relaps Oranı:** Tedavisiz hastaların yaklaşık dörtte birinde (%25) latent dönemde en az bir kez klinik relaps görülür.
* **Klinik Görünüm:** Relapslar hemen her zaman **sekonder sifiliz bulguları** (makülopapüler döküntü, kondiloma lata, mukozal plaklar vb.) şeklinde ortaya çıkar. Şankr (primer) relapsı olmaz.
* **Zamanlamanın Önemi:** Tüm relaps ataklarının %75 ila %90'ı, enfeksiyonun **ilk 1 yılı içinde** (yani Erken Latent dönemde) meydana gelir. Birinci yıldan sonra relaps riski hızla düşer.

> Relaps, enfeksiyonun 'erken' dönem özelliklerine (spiroketemi, yüksek bulaşıcılık) kısa süreli bir geri dönüştür. Bu nedenle erken latent hastalar, aniden ortaya çıkan döküntüler nedeniyle tekrar yüksek bulaştırıcı hale gelebilirler.""",
        elements=[
            make_cloze("Latent evreye geçmiş tedavisiz bir hastada klinik bulguların yeniden ortaya çıkmasına {{relaps}} (nüks) adı verilir."),
            make_cloze("Sifilizdeki klinik relapsların büyük çoğunluğu (%75-90'ı) enfeksiyonun ilk {{bir}} yılı içinde (erken latent evrede) görülür."),
            make_chain(
                "Sifilizde Relaps",
                "Latent dönemde relaps geliştiğinde, hastada hangi evrenin lezyonları tekrar ortaya çıkar?",
                "Sekonder sifiliz lezyonları (döküntüler, kondilomlar)",
                "Tüm relaps ataklarının yaklaşık %90'ı hangi zaman diliminde gerçekleşir?",
                "İlk 1 yıl içinde (Erken Latent dönemde)"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilizde Relaps",
                [
                    {"text": "Latent sifilizi olan tedavisiz bir hastada hastalık tekrar klinik belirti vererek relaps yapabilir.", "isLie": False, "explanation": "Doğru, hastaların %25'inde sekonder relapslar görülür."},
                    {"text": "Relaps ataklarının büyük kısmı enfeksiyonun ilk 1 yılı içinde (erken latent evrede) meydana gelir.", "isLie": False, "explanation": "Doğru, bu nedenle ilk yıl dalgalı seyreder."},
                    {"text": "Latent dönemde görülen relapslar her zaman primer şankrın genital bölgede yeniden açılması şeklinde ortaya çıkar.", "isLie": True, "explanation": "Yanlış! Relapslar primer şankr şeklinde değil, sekonder sifiliz bulguları (yaygın döküntü, LAP, kondilom) şeklinde ortaya çıkar."}
                ]
            ),
            make_quiz(
                question="Tedavi edilmemiş sifiliz vakalarında latent dönemde ortaya çıkabilen 'relaps' atakları ile ilgili olarak hangisi doğrudur?",
                options=[
                    "Genellikle ilk 1 yıldan sonra, 10. yılda ortaya çıkar",
                    "Hastaların %90'ında görülür, kaçınılmazdır",
                    "Ataklarda sekonder sifiliz bulguları (döküntüler) yeniden ortaya çıkar",
                    "Relaps sırasında spiroketemi olmadığı için hastalık başkasına bulaşmaz",
                    "Relaps geçiren hasta otomatik olarak tersiyer sifilize girmiş sayılır"
                ],
                answer="Ataklarda sekonder sifiliz bulguları (döküntüler) yeniden ortaya çıkar",
                explanation="Relapslar, sekonder sifiliz semptomlarının (spiroketemiye bağlı olarak) kısa süreli olarak yeniden belirmesidir. En sık ilk 1 yıl içinde görülür."
            )
        ]
    ))

    # Slide 35
    slides.append(make_slide(
        title="Latent Sifilizin Zamansal Seyri (3 ila 30 Yıl Arası Süreç)",
        narrative="""Geç latent sifiliz evresi, hastalığın en uzun ve en belirsiz dönemidir. Bakteri ve konak bağışıklık sistemi arasında bir tür 'ateşkes' (denge) vardır ve bu denge on yıllar boyunca devam edebilir.

Latent evrenin zamansal özellikleri:
* **Değişken Süre:** Geç latent evre, kişiden kişiye büyük farklılıklar gösterir. Kimi hastada 3-5 yıl sürerken, kimisinde 15, 20 hatta 30 yıl boyunca hiçbir klinik belirti vermeden devam edebilir.
* **Organ Hasarının Birikimi:** Bu uzun sessizlik döneminde, klinik bir şikayet olmasa da, spiroketlerin küçük damarlara (vasa vasorum) veya sinir sistemine verdiği yavaş inflamatuar hasar (endarteritis obliterans) yıllar içinde birikir.
* **Kırılma Noktası:** Hastaların yaklaşık üçte birinde (%30) bilinmeyen bir tetikleyiciyle immün kontrol bozulur ve hastalık **Tersiyer Sifiliz** evresine (klinik yıkım dönemi) geçer.

> Bir hastanın 20 yıldır hiçbir sifiliz belirtisi yaşamamış olması (latent kalması), onun iyileştiği anlamına gelmez. Sifilizde zaman, sessizce işleyen bir bomba gibi organ hasarını hazırlayabilir.""",
        elements=[
            make_cloze("Geç latent sifiliz evresi çok değişkendir, klinik olarak sessiz geçen süre 3 ila {{30}} yıl arasında değişebilir."),
            make_cloze("Latent evre boyunca spiroketlerin yavaş yavaş oluşturduğu endarterit, hastaların üçte birinde nihayetinde {{Tersiyer}} sifiliz adı verilen yıkıcı evreye yol açar."),
            make_table(
                headers=["Hastalık Evresi", "Zaman Çizelgesi (Tedavisiz)"],
                rows=[
                    ["Primer Şankr", "Bulaştan 3-4 hafta sonra"],
                    ["Sekonder Bulgular", "Şankrdan haftalar sonra (3-12 hafta sürer)"],
                    ["Erken Latent", "İlk 1 yıl içinde (relapslar sık)"],
                    ["Geç Latent", "1 yıldan sonra, 3 ila 30 yıl (veya ömür boyu) sürer"],
                    ["Tersiyer Sifiliz", "Bulaştan 10-30 yıl sonra ortaya çıkar"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Geç Latent Sifilizin Seyri",
                [
                    {"text": "Geç latent evre, 3 ila 30 yıl gibi çok uzun ve değişken bir süre boyunca asemptomatik devam edebilir.", "isLie": False, "explanation": "Doğru, sifilizin en uzun ve belirsiz evresidir."},
                    {"text": "Bu sessiz evre boyunca hastaların bir kısmında yavaş ilerleyen vasküler ve nörolojik hasar birikmektedir.", "isLie": False, "explanation": "Doğru, bu hasar birikimi tersiyer sifilize zemin hazırlar."},
                    {"text": "Latent sifiliz en fazla 5 yıl sürebilir, 5. yılın sonunda hasta mutlaka hayatını kaybeder.", "isLie": True, "explanation": "Yanlış! Latent evre 30 yıla kadar sürebilir ve hastaların önemli bir kısmı bu süreci tamamen semptomsuz atlatır, 5 yılda ölüm gibi kesin bir kural yoktur."}
                ]
            ),
            make_quiz(
                question="Sifilizin doğal seyri düşünüldüğünde, 'Geç Latent' evre ile ilgili en doğru ifade aşağıdakilerden hangisidir?",
                options=[
                    "Maksimum 6 ay sürer, sonra hemen nörosifilize döner",
                    "Zaman dilimi değişkendir, 3 ile 30 yıl arası sessiz devam edebilir",
                    "Bu evrede hastalar şiddetli kemik ağrıları çekerler",
                    "Geç latent evredeki herkes mutlaka ama mutlaka aort anevrizması geliştirir",
                    "Hastalık bu evrede yüksek derecede bulaşıcıdır"
                ],
                answer="Zaman dilimi değişkendir, 3 ile 30 yıl arası sessiz devam edebilir",
                explanation="Geç latent evre çok uzundur (on yıllar alabilir) ve bireyden bireye değişen bir sessizlik dönemi sunar."
            )
        ]
    ))

    # Slide 36
    slides.append(make_slide(
        title="Latent Sifilizin Doğal Seyrinde Ömür Boyu Asemptomatik Kalma Oranı (%60-70)",
        narrative="""Sifilizin ('Büyük Taklitçi') doğal seyriyle ilgili en çarpıcı istatistiklerden biri, Oslo ve Tuskegee gibi tarihi (ve etik dışı) çalışmalarla elde edilen uzun dönem verileridir. Bu verilere göre, penisilin öncesi dönemde tedavi edilmeyen hastaların çoğu hastalığın yıkıcı (tersiyer) etkilerini yaşamaz.

Doğal Seyrin İstatistikleri:
* **Tersiyer Sifilize Geçiş (3'te 1 Kuralı):** Tedavisiz hastaların yaklaşık %30-35'inde on yıllar sonra Tersiyer Sifiliz (gomatöz, kardiyovasküler veya nörosifiliz) gelişir ve mortalite/morbiditeye neden olur.
* **Ömür Boyu Asemptomatik Kalma (3'te 2 Kuralı):** Kalan hastaların yaklaşık %60-70'i ömür boyu **Latent** evrede kalır. Bu kişiler hastalık nedeniyle herhangi bir semptom yaşamaz veya ölmezler.
* **Serolojik Düzelme:** Çok nadir bir grupta, tedavi edilmese bile yıllar içinde serolojik testler (VDRL vb.) kendiliğinden negatife dönebilir (biyolojik şifa).

> Hastaların çoğunda (%60-70) sifiliz, bağışıklık sistemi tarafından bir ömür boyu zararsız bir şekilde hapsedilmiş halde kalabilir. Ancak hangi hastanın tersiyer yıkıma gideceği, hangisinin latent kalacağı önceden bilinemediği için, saptanan her latent sifiliz mutlak surette tedavi edilmelidir.""",
        elements=[
            make_cloze("Tedavi edilmeyen sifiliz vakalarının %60-70'i ömür boyu hiçbir semptom geliştirmeden {{latent}} evrede kalır."),
            make_cloze("Tedavisiz hastaların yalnızca yaklaşık üçte biri (%30'u) geç dönem komplikasyonu olan {{tersiyer}} sifilize ilerler."),
            make_chain(
                "Doğal Seyir Kuralı",
                "Tedavisiz sifiliz hastalarında tersiyer evre (organ yıkımı) gelişme riski kabaca yüzde kaçtır?",
                "%30-35 (Üçte bir)",
                "Geriye kalan %60-70 hastanın ömür boyu seyri nasıldır?",
                "Latent (asemptomatik) olarak kalırlar"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Sifilizin Tedavisiz Uzun Dönem Seyri",
                [
                    {"text": "Tedavi edilmeyen hastaların yaklaşık %30-35'i tersiyer sifiliz (KVS, nörolojik vb. komplikasyonlar) geliştirir.", "isLie": False, "explanation": "Doğru, bu ünlü 'üçte bir' kuralıdır."},
                    {"text": "Hastaların büyük çoğunluğu (%60-70), hastalığı hiçbir zaman klinik bir sorun yaratmadan ömür boyu latent evrede taşır.", "isLie": False, "explanation": "Doğru, bağışıklık sistemi çoğu hastada hastalığı hapsetmeyi başarır."},
                    {"text": "Tersiyer sifilize geçmeyen %70'lik kesimde bağışıklık sistemi çökerek hastalar mutlaka AIDS tablosu ile vefat eder.", "isLie": True, "explanation": "Yanlış! Sifiliz tek başına AIDS tablosuna yol açmaz. Asemptomatik kalan bu %70'lik grup, sifilizden kaynaklı bir sorun yaşamaz ve başka (doğal) nedenlerle ölürler."}
                ]
            ),
            make_quiz(
                question="Penisilin öncesi döneme ait uzun vadeli sifiliz izlem kohortlarına (Örn. Oslo çalışması) göre, hastalık hayat boyu tedavi edilmezse beklenen en olası (en sık görülen) klinik sonuç aşağıdakilerden hangisidir?",
                options=[
                    "Her hastanın sonunda nörosifilizden ölmesi",
                    "Hastaların %95'inde kardiyovasküler sifiliz (aortit) gelişmesi",
                    "Hastaların çoğunluğunun (%60-70) ömür boyu semptomsuz (latent) kalması",
                    "Tüm hastaların 5 yıl içinde kendiliğinden şifa bulması",
                    "Her hastada devasa gom'lar çıkması"
                ],
                answer="Hastaların çoğunluğunun (%60-70) ömür boyu semptomsuz (latent) kalması",
                explanation="İlginç bir şekilde, tedavi edilmeyen hastaların yaklaşık %60-70'i hastalığı sessiz (latent) evrede, semptom geliştirmeden bir ömür taşırlar. Sadece üçte biri tersiyer faza geçer."
            )
        ]
    ))

    # Slide 37
    slides.append(make_slide(
        title="Latent Sifilizde Serolojik Reaktivite ve Tarama",
        narrative="""Latent sifilizin tanımlayıcı tek özelliği serolojik (kan) testlerinin pozitif olmasıdır, çünkü hastanın hiçbir şikayeti veya muayene bulgusu yoktur. Bu evrede seroloji, hem tanıyı hem de hastalık aktivitesini belirlemede hayati bir rol oynar.

Latent evredeki serolojik paternler:
* **Treponemal Testler (TPHA, FTA-ABS, CIA vb.):** Bu testler vücudun bakteriye karşı ürettiği spesifik antikorları ölçer. Latent evrede (ve genellikle ömür boyu) **kuvvetli pozitiftir**.
* **Non-Treponemal Testler (VDRL, RPR):** Hastalık aktivitesini yansıtan titre bazlı testlerdir. Erken latent evrede titreler genellikle yüksektir (örn. >1:8 veya >1:16).
* **Zamanla Titre Düşüşü:** Geç latent evrede, enfeksiyonun stabil olması nedeniyle VDRL/RPR titreleri zamanla spontan olarak düşük seviyelere inebilir (örn. 1:4, 1:2) veya bazen tamamen negatifleşebilir, ancak treponemal testler her zaman pozitif kalır.

> Latent sifiliz taramasında yüksek VDRL titreleri hastalığın daha yeni (erken) veya aktif olduğunu düşündürürken, çok düşük titreler eski bir enfeksiyon (geç latent) veya geçirilmiş ve tedavi edilmiş bir hastalıkla uyumlu olabilir.""",
        elements=[
            make_cloze("Latent sifilizde tanı, hastanın klinik bulgusu olmadığı için tamamen {{serolojik}} (kan) testlerinin pozitifliğine dayanır."),
            make_cloze("Geç latent sifilizde, hastalık aktivitesini gösteren VDRL veya RPR {{titreleri}} zamanla düşük seviyelere inebilir."),
            make_table(
                headers=["Test Türü", "Latent Evredeki Beklenen Durumu"],
                rows=[
                    ["Treponemal (TPHA, FTA-ABS vb.)", "Kuvvetli Pozitif (Genellikle ömür boyu pozitif kalır)"],
                    ["Non-Treponemal (VDRL, RPR)", "Pozitif, ancak titre üzerinden değerlendirilir"],
                    ["Erken Latent'te VDRL Titresi", "Genellikle Yüksek (>1:8 veya daha fazla)"],
                    ["Geç Latent'te VDRL Titresi", "Genellikle Düşük (1:4, 1:2 veya negatif olabilir)"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Latent Sifiliz Serolojisi",
                [
                    {"text": "Latent sifilizde TPHA veya FTA-ABS gibi treponemal testler pozitiftir.", "isLie": False, "explanation": "Doğru, bu testler spesifik antikorları saptar ve pozitiftir."},
                    {"text": "Erken latent evrede VDRL/RPR titreleri genellikle yüksektir, geç latent evrede ise zamanla titreler düşebilir.", "isLie": False, "explanation": "Doğru, titre hastalığın aktivite/zamanıyla ilişkilidir."},
                    {"text": "Geç latent evrede VDRL titresi düşük (örn. 1:2) ise, bu hasta kesinlikle sahte pozitiftir ve sifiliz olamaz.", "isLie": True, "explanation": "Yanlış! Geç latent evrede (eski enfeksiyonlarda) VDRL/RPR titrelerinin 1:2 veya 1:4 gibi çok düşük seviyelerde kalması ('serofast' durum veya düşük aktivite) oldukça beklenen ve klasik bir tablodur, sahte pozitiflik anlamına gelmez."}
                ]
            ),
            make_quiz(
                question="Herhangi bir şikayeti olmayan ve fizik muayenesi tamamen normal olan 50 yaşındaki bir hastada rutin taramada TPHA (+), VDRL ise düşük titrede (1:2) pozitif saptanmıştır. Hasta geçmişte sifiliz tedavisi aldığını hatırlamamaktadır. Bu tablo aşağıdakilerden hangisi ile en uyumludur?",
                options=[
                    "Tamamen aktif primer şankr dönemi",
                    "Geç latent sifiliz",
                    "Sekonder sifiliz",
                    "Tedavi sonrası serolojik başarısızlık",
                    "Kesin biyolojik yanlış pozitiflik"
                ],
                answer="Geç latent sifiliz",
                explanation="Klinik bulgusu olmayan, treponemal testi pozitif ve düşük VDRL titresi olan bir erişkin (tedavi öyküsü yoksa) 'Geç latent sifiliz' olarak değerlendirilir."
            )
        ]
    ))

    # Slide 38
    slides.append(make_slide(
        title="Latent Dönemde Gebelik ve Konjenital Bulaş Riski",
        narrative="""Sifilizin gebelikte fetüse bulaşması (Konjenital Sifiliz), hastalığın her evresinde mümkündür, ancak evrelere göre geçiş riski farklılık gösterir. Latent evredeki gebelerin yönetimi bebek sağlığı açısından kritik bir konudur.

Gebelikte Latent Sifiliz ve Bulaş:
* **Erken Latent Gebelik:** İlk 1 yıl içindeki gebeliklerde spiroketemi atakları yoğun olduğu için fetüse bulaş riski (transplasental geçiş) **%40 ila %80** gibi çok yüksek bir orandadır. Ölü doğum, abortus veya şiddetli konjenital sifiliz riski yüksektir.
* **Geç Latent Gebelik:** Enfeksiyon 1 yıldan eski ise spiroketemi nadirdir. Bulaş riski belirgin şekilde azalarak **%10 civarına** düşer, ancak fetüsü enfekte etme potansiyeli hiçbir zaman tam sıfırlanmaz.
* **Taramanın Önemi:** Bu nedenle tüm gebeler ilk trimesterde ve yüksek riskli bölgelerde üçüncü trimesterde mutlaka VDRL/RPR ile rutin sifiliz taramasından geçirilmelidir.

> Latent sifilizdeki bir kadın cinsel partnerine hastalık bulaştırmayacak durumda (geç latent) olsa bile, **fetüsüne (plasenta yoluyla)** enfeksiyonu bulaştırabilir. Fetüs için 'tamamen güvenli' bir tedavisiz sifiliz evresi yoktur.""",
        elements=[
            make_cloze("Erken latent sifiliz olan bir gebede, spiroketemi nedeniyle enfeksiyonun fetüse geçme riski (%40-80) oldukça {{yüksektir}}."),
            make_cloze("Geç latent dönemde cinsel yolla bulaş pratik olarak olmasa da, gebelikte {{plasenta}} yoluyla fetüse geçiş (konjenital sifiliz) riski devam eder."),
            make_table(
                headers=["Annedeki Evre", "Fetüse (Konjenital) Bulaş Riski"],
                rows=[
                    ["Primer / Sekonder Sifiliz", "Çok yüksek (%60-100)"],
                    ["Erken Latent Sifiliz (<1 Yıl)", "Yüksek (%40-80)"],
                    ["Geç Latent Sifiliz (>1 Yıl)", "Düşük ancak var (%10 civarı)"],
                    ["Tersiyer Sifiliz", "Oldukça düşük / nadir"]
                ]
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Gebelik ve Latent Sifiliz",
                [
                    {"text": "Erken latent sifilizli gebelerde enfeksiyonun fetüse geçme ve düşüğe neden olma riski oldukça yüksektir.", "isLie": False, "explanation": "Doğru, erken evrede spiroketemi olduğu için risk fazladır."},
                    {"text": "Geç latent evrede cinsel yolla bulaş nadir olsa da, fetüse transplasental bulaş (konjenital sifiliz) ihtimali az da olsa devam eder.", "isLie": False, "explanation": "Doğru, fetüs için tamamen güvenli değildir."},
                    {"text": "Sifiliz sadece şankr varken (primer evrede) fetüse bulaşır; latent evredeki bir anneden bebeğe asla sifiliz geçmez.", "isLie": True, "explanation": "Yanlış! Sifiliz latent evrede de (özellikle erken latentte %40-80 oranında, geç latentte %10) fetüse bulaşabilir ve konjenital sifilize neden olabilir."}
                ]
            ),
            make_quiz(
                question="Asemptomatik olan ancak sifiliz serolojisi pozitif gelen ve enfeksiyonu 3 yıl önce aldığı (Geç Latent) saptanan hamile bir hasta değerlendirilmektedir. Hastalığın bu aşamasında bulaştırıcılıkla ilgili aşağıdakilerden hangisi doğrudur?",
                options=[
                    "Bebek %100 oranında şiddetli konjenital sifiliz doğacaktır",
                    "Cinsel partnerine bulaştırma riski yok denecek kadar az olsa da, bebeğe bulaşma riski (%10) hala mevcuttur",
                    "Hastalık artık kana karışmadığı için bebeğe bulaşması imkansızdır",
                    "Annede organ hasarı (tersiyer) olmadığı sürece bebeğe geçmez",
                    "Sadece normal doğum sırasında bebek şankra temas ederse bulaşır"
                ],
                answer="Cinsel partnerine bulaştırma riski yok denecek kadar az olsa da, bebeğe bulaşma riski (%10) hala mevcuttur",
                explanation="Geç latent evrede cinsel yolla bulaştırıcılık büyük oranda bitmiştir, ancak transplasental (bebeğe) geçiş riski (%10 civarı) devam ettiği için gebe mutlaka tedavi edilmelidir."
            )
        ]
    ))

    # Slide 39
    slides.append(make_slide(
        title="Erken Latent ile Geç Latent Sifiliz Arasındaki Ayırıcı Kriterler",
        narrative="""Latent sifilizi saptadığımızda (asemptomatik, seropozitif hasta), tedavi süresini (tek doz vs. 3 doz penisilin) belirlemek için bunun **Erken (<1 yıl)** mi yoksa **Geç (>1 yıl / Bilinmeyen süre)** mi olduğunu anlamak hayati önem taşır.

Kılavuzlara göre 'Erken Latent' diyebilmek için hastanın şu kriterlerden en az birini karşılaması gerekir:
* **Serokonversiyon:** Son 1 yıl içinde (veya 12 ay öncesine kadar) yapılmış negatif bir sifiliz (VDRL/TPHA) testinin bulunması.
* **Klinik Öykü:** Son 1 yıl içinde doktor tarafından doğrulanmış primer şankr veya sekonder sifiliz döküntüsü öyküsünün olması.
* **Titre Artışı:** Son 1 yıl içinde belgelenmiş VDRL/RPR titresinde dört kat (2 dilüsyon, örn. 1:4'ten 1:16'ya) artış saptanması.
* **Kesin Temas:** Primer, sekonder veya erken latent sifilizi olduğu kanıtlanmış bir partnerle son 1 yıl içinde cinsel temas öyküsü.

> Bu dört kanıttan **hiçbiri yoksa**, hasta güvenli tarafta kalmak adına 'Süresi bilinmeyen Latent Sifiliz' olarak kabul edilir ve **Geç Latent** sifilizmiş gibi uzun süreli tedavi edilir.""",
        elements=[
            make_cloze("Bir latent sifiliz hastasına 'Erken Latent' diyebilmek için enfeksiyonun son {{bir}} yıl içinde alındığını kanıtlayan verilere ihtiyaç vardır."),
            make_cloze("Son 12 ay içinde yapılmış negatif bir test varken şimdiki test pozitifse (serokonversiyon), hasta kesinlikle {{Erken}} latent evrededir."),
            make_chain(
                "Evre Ayrımı Kriterleri",
                "Latent hastanın 6 ay önceki VDRL testi negatifken şu an pozitif çıkmış. Hangi evrededir?",
                "Erken Latent (<1 Yıl)",
                "Hastanın ne zaman enfekte olduğuna dair hiçbir ipucu veya eski testi yok. Hangi evre kabul edilir?",
                "Geç Latent (veya Süresi Bilinmeyen Latent)"
            ),
            make_spot_lie(
                "Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Erken-Geç Latent Ayrımı",
                [
                    {"text": "Son 1 yıl içinde belgelenmiş primer veya sekonder sifiliz semptomu geçiren bir hasta şu an asemptomatikse erken latent kabul edilir.", "isLie": False, "explanation": "Doğru, bu enfeksiyonun yeni (son 1 yılda) olduğunu kanıtlar."},
                    {"text": "Enfeksiyonun ne zaman bulaştığını gösteren hiçbir kanıt (eski test, belirti öyküsü vb.) yoksa hasta 'geç latent' gibi yönetilir.", "isLie": False, "explanation": "Doğru, süresi bilinmeyen latent her zaman geç kabul edilir."},
                    {"text": "Latent sifilizdeki her hastanın yaşına bakılır; 25 yaş altı herkes 'Erken', 25 yaş üstü herkes 'Geç' latent olarak kabul edilerek yaşa göre tedavi verilir.", "isLie": True, "explanation": "Yanlış! Evre ayrımının hastanın yaşıyla hiçbir ilgisi yoktur; tamamen enfeksiyonun vücuda ne kadar süre önce (1 yıldan az veya çok) girdiğiyle ilgilidir."}
                ]
            ),
            make_quiz(
                question="Rutin sağlık taramasında VDRL ve TPHA testleri pozitif saptanan ve tamamen asemptomatik olan bir kadın hastanın evresini belirlemek istiyorsunuz. Aşağıdaki durumlardan hangisi hastayı kesin olarak 'Erken Latent' sifiliz kategorisine sokar?",
                options=[
                    "Hastanın 45 yaşında ve menopozda olması",
                    "Hastanın 8 ay önce yaptırdığı kan bağışında sifiliz testlerinin tamamen negatif olduğunun belgelenmesi",
                    "Hastanın VDRL titresinin çok düşük (1:2) saptanması",
                    "Hastada son 2 yıldır hiçbir cinsel temas öyküsü olmaması",
                    "Kanda TPHA testinin zayıf pozitif olması"
                ],
                answer="Hastanın 8 ay önce yaptırdığı kan bağışında sifiliz testlerinin tamamen negatif olduğunun belgelenmesi",
                explanation="Son 1 yıl (8 ay) içinde negatif bir testin olması (serokonversiyon), enfeksiyonun kesinlikle son 1 yıl içinde bulaştığını kanıtlar; bu da 'Erken Latent' tanımıdır."
            )
        ]
    ))

    # Slide 40
    slides.append(make_slide(
        title="[TEKRAR SAYFASI - CHECKPOINT 4] Latent Sifilizin Evreleri ve Relaps Riskleri",
        narrative="""Latent Sifiliz dönemine ait temel kavramları özetleyelim:

* **Latent Sifiliz Nedir?** Klinik bulgunun (şikayet, lezyon) OLMADIĞI, ancak serolojik testlerin POZİTİF olduğu ve BOS'un normal olduğu sessiz evredir.
* **Erken Latent (< 1 Yıl):** Enfeksiyonun ilk 1 yılıdır. Spiroketemi atakları vardır, **cinsel yolla bulaştırıcılık yüksektir**. Hastaların büyük kısmında ilk yıl içinde sekonder bulgularla **relaps (nüks)** görülebilir.
* **Geç Latent (> 1 Yıl):** Enfeksiyondan 1 yıldan uzun süre geçmiştir. Cinsel yolla bulaş pratik olarak yoktur, bağışıklık stabildir.
* **Gebelik (Konjenital Risk):** Latent evrede (hem erken hem geç) **plasenta yoluyla bebeğe bulaş riski mevcuttur**.
* **Doğal Seyir Kuralı:** Tedavi verilmeyen hastaların %60-70'i ömür boyu hiçbir organ hasarı görmeden latent evrede kalırken, %30'u yıkıcı Tersiyer evreye ilerler.
* **Yönetim:** Zamanı bilinmeyen tüm latent vakalar 'Geç Latent' kabul edilir ve olası tersiyer hasarı önlemek için tedavi edilir.""",
        elements=[
            make_cloze("Hiçbir klinik belirtinin olmadığı ancak serolojik testlerin pozitif saptandığı evreye {{Latent}} Sifiliz denir."),
            make_cloze("Tedavi almayan latent sifiliz vakalarının %60-70'i ömür boyu semptomsuz kalırken, üçte biri organ hasarlı {{Tersiyer}} sifilize ilerler."),
            make_table(
                headers=["Karşılaştırma Noktası", "Erken Latent (<1 Yıl)", "Geç Latent (>1 Yıl)"],
                rows=[
                    ["Cinsel Bulaşıcılık", "Yüksek (spiroketemi atakları)", "Çok düşük"],
                    ["Klinik Relaps (Nüks) Riski", "Yüksek (çoğu ilk 1 yılda)", "Nadir"],
                    ["Annede Konjenital Bulaş Riski", "Çok yüksek (%40-80)", "Düşük ama var (%10)"],
                    ["Titre (VDRL)", "Genellikle yüksek", "Genellikle düşük veya düşme eğiliminde"]
                ]
            ),
            make_recall(
                "Latent sifilizi olan bir kişi, cinsel yolla partnerine ve gebelikte bebeğine hastalık bulaştırabilir mi?",
                "Erken latentse cinsel yolla yüksek oranda bulaştırır, geç latentse cinsel bulaş pratik olarak yoktur. Ancak HER İKİ evrede de (özellikle erken evrede çok daha yüksek olmak üzere) gebelikte bebeğe (konjenital) bulaştırma riski vardır."
            ),
            make_quiz(
                question="Latent sifiliz ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?",
                options=[
                    "Klinik semptomlar ve fizik muayene bulguları tamamen normaldir",
                    "Tanısı sadece serolojik (kan) testleri ile konulur",
                    "Erken latent evre, enfeksiyonun ilk 1 yılını kapsar ve relaps riski yüksektir",
                    "Geç latent evredeki bir hasta cinsel partnerine kesinlikle hastalık bulaştırmaz ancak fetüse bulaştırabilir",
                    "Latent sifilizi olan her hasta 10 yıl içinde kesinlikle öleceği için acil ameliyata alınmalıdır"
                ],
                answer="Latent sifilizi olan her hasta 10 yıl içinde kesinlikle öleceği için acil ameliyata alınmalıdır",
                explanation="Sifilizin latent evresindeki hastaların %60-70'i ömür boyu semptomsuz (asemptomatik) kalarak normal yaşamlarını sürdürürler; 'kesinlikle ölür' ifadesi yanlıştır. Ayrıca tedavisi cerrahi değil tıbbidir (penisilin)."
            )
        ]
    ))

    return slides
