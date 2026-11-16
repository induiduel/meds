# -*- coding: utf-8 -*-
"""
Part 1 of the Tumor Staging and Laboratory Diagnosis Deck (Slides 1 to 12)
"""

SLIDES_PART1 = [
    {
        "slideNumber": 1,
        "title": "Neoplazmların Konak Üzerindeki Lokal ve Mekanik Etkileri",
        "subtitle": "Kitle Etkisi, Kritik Anatomik Konum, Lümen Obstrüksiyonu ve Doku İskemisi",
        "synthesisNarrative": "Neoplazmların klinik ciddiyeti yalnızca histopatolojik derecelerine değil, yerleştikleri anatomik bölgeye ve çevre dokularda yarattıkları mekanik bası, iskemi ve obstrüksiyona doğrudan bağlıdır.",
        "content": """Neoplazi, ister selim (benign) ister habis (malign) tabiatta olsun, konak organizma üzerinde yalnızca hücresel çoğalmasıyla değil; yerleştiği anatomik bölge, kitlenin çevre dokulara yaptığı mekanik bası ve organ fonksiyonlarını kısıtlaması nedeniyle son derece yıkıcı sonuçlar doğurabilir. Tıbbi patolojide temel bir aksiyom vardır: Bir neoplazmın klinik ciddiyeti, her zaman onun histopatolojik malignite derecesiyle orantılı değildir; lezyonun yerleşim gösterdiği anatomik lokalizasyon, hastanın kaderini belirleyen en kritik parametrelerden biridir.

Kritik anatomik lokalizasyonun dramatik sonuçlarını gösteren en klasik örneklerden biri hipofiz bezi lezyonlarıdır. Sella turcica gibi kemik çatıyla çevrili, rijit ve genişleme payı bulunmayan dar bir boşlukta gelişen yalnızca 1 cm çapındaki benign bir hipofiz adenomu, çevreleyen normal hipofiz parankimini mekanik olarak sıkıştırarak bası atrofisine uğratır. Bu bası, ön hipofiz hormonlarının sekresyonunu durdurarak hastada panhipopituitarizme, kiazma optikuma bası yaparak bitemporal hemianopsiye ve intrakraniyal basınç artışına yol açabilir. Benzer şekilde, kafa içi kemik kavitede büyüyen benign bir menenjiyom, beyin parankimini iterek herniasyona ve solunum merkezi felcine neden olarak hastayı öldürebilir.

Mekanik obstrüksiyonun bir diğer çarpıcı örneği vasküler ve lüminal yapılarda izlenir. Renal arter duvarında gelişen ve çapı sadece 0,5 cm olan küçücük bir benign düz kas tümörü (leiomyom), damar lümenini daraltarak böbrek kan akımını kritik düzeyde düşürür. Böbrek bu durumu sistemik hipotansiyon olarak algılar; jukstaglomerüler aparattan yoğun renin deşarjı başlar ve Goldblatt böbreği mekanizmasıyla şiddetli, tedaviye dirençli renovasküler hipertansiyon tablosu ortaya çıkar.

Safra yollarında veya pankreas başında yerleşen lezyonlarda da benzer bir lüminal felaket görülür. Koledok distalinde veya Ampulla Vateri'de gelişen henüz birkaç milimetrelik küçük bir karsinom, ana safra kanalını mekanik olarak tıkar. Safra akışının durması süratle derin obstrüktif sarılığa (kolestaz), ardından staz zemininde gelişen bakteriyel asendan kolanjite ve sepsise zemin hazırlar. İnce veya kalın bağırsakta intralüminal polipoid büyüyen benign veya malign tümörler ise peristaltik hareketlerle ileriye sürüklenerek invajinasyona (intussusepsiyon) ve akut bağırsak perforasyonuna sebebiyet verebilir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Tümörün benign veya malign olmasından bağımsız olarak, yerleşim gösterdiği anatomik lokalizasyon hayati önem taşır; sella turcica veya kafa içi gibi kapalı kemik boşluklarda ya da hayati damar/kanal lümenlerinde gelişen milimetrik benign neoplazmlar dahi ölümcül bası ve organ yetmezliğine yol açabilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Hipofiz adenomunun normal dokuyu sıkıştırarak hipopituitarizme yol açması, renal arter leiomyomunun renovasküler hipertansiyona ve koledok tümörünün obstrüktif sarılığa neden olması tümörlerin konak üzerindeki hangi patolojik mekanizmasına örnektir? (Lokal / mekanik kitle etkisi).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Sella turcica içinde 1 cm'lik hipofiz adenomu normal hipofiz parankimini baskılayarak panhipopituitarizme yol açabilir.",
            "0,5 cm'lik renal arter leiomyomu lümeni daraltarak renin-anjiyotensin aktivasyonuyla şiddetli renovasküler hipertansiyona neden olur.",
            "Koledok veya ampulla vateri lezyonları çok küçük boyutlarda dahi safra lümenini tıkayarak derin obstrüktif sarılık yaratır."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-001",
            "question": "Tümörlerin konak organizma üzerindeki lokal ve mekanik kitle etkileri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Sella turcica içine yerleşen 1 cm çapındaki bir benign hipofiz adenomu normal hipofiz dokusunu sıkıştırarak panhipopituitarizme yol açabilir.",
                "B) Renal arter lümeninde gelişen milimetrik bir leiomyom iskemi yaratarak sekonder renovasküler hipertansiyona neden olabilir.",
                "C) Ampulla Vateri veya koledok yerleşimli küçük karsinomlar safra akışını engelleyerek erken dönemde obstrüktif sarılık oluşturabilir.",
                "D) Bir tümörün klinik ciddiyeti ve hayati riski, her zaman histolojik malignite derecesi ile doğru orantılıdır; benign lezyonlar ölümcül bası yapamaz.",
                "E) İntralüminal polipoid bağırsak tümörleri peristaltizm ile ilerleyerek invajinasyon ve bağırsak obstrüksiyonuna yol açabilir."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü bir tümörün klinik ciddiyeti ve yaşamsal tehdidi her zaman histopatolojik derecesiyle paralel gitmez; yerleştiği anatomik bölge çok daha belirleyicidir. Kafa içi kapalı kemik boşlukta (foramen magnum basısı yapan menenjiyom) veya kritik lüminal kanallarda yerleşen selim (benign) tümörler dahi herniasyon, solunum felci veya organ iskemisi yaparak ölümcül olabilir. A, B, C ve E seçenekleri mekanik kitle etkisinin klasik klinik örnekleridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-001",
                "question": "Tümörlerin konak organizma üzerindeki lokal ve mekanik kitle etkileri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Sella turcica içine yerleşen 1 cm çapındaki bir benign hipofiz adenomu normal hipofiz dokusunu sıkıştırarak panhipopituitarizme yol açabilir.",
                    "B) Renal arter lümeninde gelişen milimetrik bir leiomyom iskemi yaratarak sekonder renovasküler hipertansiyona neden olabilir.",
                    "C) Ampulla Vateri veya koledok yerleşimli küçük karsinomlar safra akışını engelleyerek erken dönemde obstrüktif sarılık oluşturabilir.",
                    "D) Bir tümörün klinik ciddiyeti ve hayati riski, her zaman histolojik malignite derecesi ile doğru orantılıdır; benign lezyonlar ölümcül bası yapamaz.",
                    "E) İntralüminal polipoid bağırsak tümörleri peristaltizm ile ilerleyerek invajinasyon ve bağırsak obstrüksiyonuna yol açabilir."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü bir tümörün klinik ciddiyeti ve yaşamsal tehdidi her zaman histopatolojik derecesiyle paralel gitmez; yerleştiği anatomik bölge çok daha belirleyicidir. Kafa içi kapalı kemik boşlukta (foramen magnum basısı yapan menenjiyom) veya kritik lüminal kanallarda yerleşen selim (benign) tümörler dahi herniasyon, solunum felci veya organ iskemisi yaparak ölümcül olabilir. A, B, C ve E seçenekleri mekanik kitle etkisinin klasik klinik örnekleridir."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Yüzey Ülserasyonu, Kanama ve İmmün Sistem Disfonksiyonu",
        "subtitle": "Mukozal Erozyon, Kronik Kan Kaybı, Sekonder Süperenfeksiyon ve İmmünsüpresyon",
        "synthesisNarrative": "Mukozal tümörlerde yüzey ülserasyonu kronik kan kaybı ve demir eksikliği anemisine yol açarken, bariyer kaybı ve tümör yükü sekonder enfeksiyonlar ile immünsüpresyona zemin hazırlar.",
        "content": """Lümenli organların epitelyal yüzeylerinde ve mukozalarda gelişen neoplazmlar, ekzofitik ve infiltratif büyüme paternleri sırasında mikrovasküler ağın yetersiz kalması, yüzeyel iskemi ve lüminal mekanik sürtünmeler nedeniyle süratle ülserasyona uğrarlar. Gastrointestinal sistem, solunum yolları ve ürogenital traktusta yerleşen tümörlerde bu ülserasyon süreci, konağın klinik tablosunu doğrudan belirleyen kanama ve enfeksiyon zincirini başlatır.

Mukozal ülserasyonun en tipik ve sinsi klinik tablosu gastrointestinal sistem karsinomlarında izlenir. Sağ kolon (çekum ve çıkan kolon) yerleşimli adenokarsinomlar genellikle geniş lümen içinde polipoid ve ülseröz kitleler olarak büyürler. Dışkı bu bölgede henüz sıvı kıvamda olduğundan mekanik tıkanma geç evrelere kadar fark edilmez; ancak tümör yüzeyindeki nekrotik ülserlerden haftalar ve aylar boyunca mikroskobik düzeyde gizli kan kaybı meydana gelir. Bu durum hastada derin demir eksikliği anemisine, halsizliğe, solukluğa ve kardiyak iş yükünde artışa yol açar. Sol kolon karsinomlarında ise lümenin dar ve dışkının katı olması nedeniyle ülserasyon hem erken lümen tıkanıklığına hem de taze rektal kanamaya (hematokezya) neden olur. Mide karsinomlarında benzer şekilde kronik kan sızıntısı melena ve anemiye, solunum sistemi karsinomlarında bronşiyal damar erozyonu masif hemoptiziye, mesane karsinomlarında ise ağrısız hematüriye yol açar.

Ülserasyonun ikinci kaçınılmaz sonucu sekonder bakteriyel enfeksiyondur. Koruyucu epitel bariyerinin parçalanması ve tümör yüzeyinde nekrotik doku artıkları bulunması, lüminal bakterilerin kitle içine invaze olması için mükemmel bir besi yeri oluşturur. Tümör zemininde gelişen pürülan enflamasyon, doku destruksiyonunu hızlandırır, kötü kokulu akıntılara ve bakteriyemiye zemin hazırlar.

Tümör yükünün konak bağışıklık sistemi üzerindeki baskılayıcı etkisi de klinik seyri ağırlaştırır. Masif tümör yükü varlığında, dalak ve kemik iliği metastazları hematopoezi baskılar; kemik iliği infiltrasyonu nötropeniye yol açar. Ayrıca sitokin dengesindeki bozulmalar ve tümörün ürettiği immünsüpresif mediyatörler (TGF-beta, IL-10) hücresel bağışıklığı felce uğratır. Kanser kaşeksisine bağlı gelişen protein-kalori malnütrisyonu ve eşlik eden antineoplastik kemoradyoterapiler immün sistemi daha da çökertir. Sonuç olarak kanser hastaları, Pneumocystis jirovecii, Candida türleri, Aspergillus, Sitomegalovirüs (CMV) ve dirençli nozokomiyal bakteriler gibi fırsatçı patojenlerin yol açtığı ölümcül enfeksiyonlara son derece açık hale gelirler.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Erişkin bir erkekte veya menopoz sonrası bir kadında açıklanamayan demir eksikliği anemisi saptandığında, aksi kanıtlanana kadar gastrointestinal sistem malignitesi (özellikle sağ kolon adenokarsinomu) düşünülmeli ve kolonoskopik araştırma yapılmalıdır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Sağ kolon (çekum) adenokarsinomlarında barsak lümeninin geniş olması ve tümörün yüzeyel ülserasyonu nedeniyle hastaların hekime en sık başvuru nedeni olan hematolojik bulgu nedir? (Kronik gizli kan kaybına bağlı demir eksikliği anemisi).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Ülseröz lezyonlar kronik kan kaybına yol açarak mikrositer hipokrom demir eksikliği anemisine zemin hazırlar.",
            "Epitel bariyerinin yıkılması nekrotik tümör tabanında sekonder bakteriyel süperenfeksiyon ve sepsis riskini tetikler.",
            "İleri tümör yükü, kemik iliği tutulumu ve malnütrisyon fırsatçı patojenlere karşı konak immünitesini derin şekilde baskılar."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-002",
            "question": "Mukozal yüzey yerleşimli neoplazmlarda görülen yüzey ülserasyonu, kronik kanama ve immünite bozuklukları ile ilgili aşağıdaki klinik ve patolojik ifadelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Sağ kolon karsinomlarında lümen dar olduğu için ülserasyona bağlı kronik kanamadan ziyade akut mekanik obstrüksiyon ilk semptomdur.",
                "B) Erişkin bir erkekte veya postmenopozal kadında saptanan açıklanamayan demir eksikliği anemisinde ilk olarak gastrointestinal malignite (özellikle sağ kolon) düşünülmelidir.",
                "C) Tümör yüzeyinde gelişen sekonder bakteriyel enfeksiyonlar tümör dokusunun yıkımını yavaşlatarak koruyucu bir bariyer oluşturur.",
                "D) Masif tümör yükü varlığında dalak ve kemik iliği metastazları polistemiye ve lökositoza yol açarak konak immünitesini güçlendirir.",
                "E) Malign tümör hücrelerinde hücreler arası bağlantıların (E-kaderin) artması ülserasyon ve kanama riskini artıran temel hücresel faktördür."
            ],
            "correctAnswer": 1,
            "explanation": "B seçeneği doğrudur. Erişkin erkeklerde ve postmenopozal kadınlarda fizyolojik kan kaybı (menstrüasyon vb.) beklenmediğinden, saptanan demir eksikliği anemisi aksi kanıtlanana kadar gastrointestinal sistem malignitelerine (özellikle geniş lümende sinsi mikroskobik kanama yapan sağ kolon çekum adenokarsinomuna) bağlı kronik kan kaybı olarak kabul edilmeli ve kolonoskopik inceleme yapılmalıdır. A yanlıştır (sağ kolon geniştir, kanama sinsi anemi yapar; sol kolon dardır). C yanlıştır (enfeksiyon doku hasarını artırır ve sepsise yol açar). D yanlıştır (kemik iliği tutulumu nötropeni ve immün yetmezlik yapar). E yanlıştır (malign hücrelerde E-kaderin azalır)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-002",
                "question": "Mukozal yüzey yerleşimli neoplazmlarda görülen yüzey ülserasyonu, kronik kanama ve immünite bozuklukları ile ilgili aşağıdaki klinik ve patolojik ifadelerden hangisi DOĞRUDUR?",
                "options": [
                    "A) Sağ kolon karsinomlarında lümen dar olduğu için ülserasyona bağlı kronik kanamadan ziyade akut mekanik obstrüksiyon ilk semptomdur.",
                    "B) Erişkin bir erkekte veya postmenopozal kadında saptanan açıklanamayan demir eksikliği anemisinde ilk olarak gastrointestinal malignite (özellikle sağ kolon) düşünülmelidir.",
                    "C) Tümör yüzeyinde gelişen sekonder bakteriyel enfeksiyonlar tümör dokusunun yıkımını yavaşlatarak koruyucu bir bariyer oluşturur.",
                    "D) Masif tümör yükü varlığında dalak ve kemik iliği metastazları polistemiye ve lökositoza yol açarak konak immünitesini güçlendirir.",
                    "E) Malign tümör hücrelerinde hücreler arası bağlantıların (E-kaderin) artması ülserasyon ve kanama riskini artıran temel hücresel faktördür."
                ],
                "correctAnswer": 1,
                "explanation": "B seçeneği doğrudur. Erişkin erkeklerde ve postmenopozal kadınlarda fizyolojik kan kaybı (menstrüasyon vb.) beklenmediğinden, saptanan demir eksikliği anemisi aksi kanıtlanana kadar gastrointestinal sistem malignitelerine (özellikle geniş lümende sinsi mikroskobik kanama yapan sağ kolon çekum adenokarsinomuna) bağlı kronik kan kaybı olarak kabul edilmeli ve kolonoskopik inceleme yapılmalıdır. A yanlıştır (sağ kolon geniştir, kanama sinsi anemi yapar; sol kolon dardır). C yanlıştır (enfeksiyon doku hasarını artırır ve sepsise yol açar). D yanlıştır (kemik iliği tutulumu nötropeni ve immün yetmezlik yapar). E yanlıştır (malign hücrelerde E-kaderin azalır)."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Endokrin Fonksiyon Gösteren Tümörler ve Otonom Hormon Sentezi",
        "subtitle": "Benign ve Malign Endokrin Neoplazmlar, Hormonal Hiperfonksiyon Sendromları",
        "synthesisNarrative": "İyi diferansiye benign endokrin tümörler, anaplastik malign karsinomlara kıyasla hücresel maturasyonlarını korudukları için hormon sentezleme ve klinik hiperfonksiyon yaratma konusunda belirgin şekilde daha etkindir.",
        "content": """Endokrin bezlerden köken alan neoplazmlar, hücrelerin otonom çoğalmasına ek olarak dokunun kendine özgü hormonal ürünlerini sentezleme ve dolaşıma kontrolsüz biçimde verme yeteneğine sahiptir. Bu tümörler hem benign (adenom) hem de malign (karsinom) morfolojide karşımıza çıkabilir. Ancak endokrin patolojisinde geçerli olan son derece kritik bir kural vardır: İyi diferansiye, morfolojik olarak selim (benign) karakterdeki adenomlar; yapısal ve fonksiyonel maturasyonlarını korudukları için hormon üretme ve klinik hiperfonksiyon sendromu oluşturma konusunda anaplastik malign karsinomlardan genellikle çok daha etkindir. Bir tümör dediferansiye olup anaplaziye kaydıkça, hücresel özgül hormon sentez yolaklarını kaybeder.

Pankreasın Langerhans adacıklarından kaynaklanan nöroendokrin tümörler bu durumun en bilinen örneğidir. Beta hücrelerinden köken alan ve genellikle 1-2 cm çapında küçük, benign bir lezyon olan İnsülinoma, kontrolsüz biçimde kanda insülin deşarjı yapar. Bu otonom hiperinsülinizm, hastada ağır açlık hipoglisemisine, terleme, taşikardi, titreme ve nöroglikopenik semptomlara (konfüzyon, davranış değişiklikleri, nöbet ve hipoglisemik koma) yol açar. Bu tablo klinikte Whipple triadı (hipoglisemi semptomları + semptom anında ölçülen plazma glukozunun <50 mg/dL olması + glukoz verilmesiyle semptomların hızla düzelmesi) ile karakterizedir.

Adrenal korteks tümörleri de ürettikleri spesifik steroid hormonlara göre ağır klinik tablolar oluştururlar. Zona glomerulosa kaynaklı benign bir adrenokortikal adenom otonom aldosteron salgılayarak Conn sendromuna (primer hiperaldosteronizm) yol açar; böbrek distal tübüllerinden aşırı sodyum geri emilimi ve potasyum atılımı sonucu dirençli hipertansiyon, hipervolemi ve hipokalemik metabolik alkaloz gelişir. Zona fasciculata kaynaklı bir adenom ise aşırı kortizol üreterek ACTH'tan bağımsız Cushing sendromu meydana getirir; santral obezite, aydede yüzü, bufalo hörgücü, deride mor strialar, osteoporoz ve diyabet ile seyreder.

Benzer şekilde tiroid bezinde otonom T3 ve T4 üreten soliter benign foliküler adenomlar (toksik adenom / Plummer hastalığı) sekonder tirotoksikoza yol açarken; adrenal medulladaki kromafin hücrelerden köken alan Feokromositoma ise aşırı adrenalin ve noradrenalin salgılayarak paroksismal hipertansif krizler, baş ağrısı, çarpıntı ve profüz terleme atakları yaratır. Bu sendromların tümünde klinik tabloyu belirleyen faktör tümörün kitlesel boyutu değil, sentezlediği hormonun biyolojik gücüdür.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Endokrin tümörlerde hormon üretimi ve hormonal hiperfonksiyon tablosu, iyi diferansiye benign tümörlerde kötü diferansiye malign tümörlere kıyasla çok daha sıktır; hücre anaplastik hale geldikçe hormon sentezleme yeteneğini kaybeder.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Paroksismal hipoglisemi krizleri, konfüzyon atakları ve glukoz infüzyonu ile hızla düzelen nöroglikopenik koma tablosu (Whipple triadı) ile karakterize olan en sık benign endokrin pankreas neoplazmı hangisidir? (İnsülinoma / Beta hücre adenomu).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "İyi diferansiye benign endokrin tümörler, anaplastik karsinomlara göre çok daha etkin hormon sentezler.",
            "İnsülinoma küçük boyutuna rağmen derin hipoglisemi ve koma yaratan en sık adacık hücresi neoplazmıdır.",
            "Adrenal korteks adenomları aşırı hormon üretimiyle Cushing veya Conn sendromuna yol açabilir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-003",
            "question": "Endokrin bez neoplazmlarının hormon üretimi ve hormonal hiperfonksiyon sendromları ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Endokrin tümörlerde hormon üretimi ve klinik hiperfonksiyon sendromları, genellikle iyi diferansiye benign tümörlerde kötü diferansiye karsinomlara göre daha sıktır.",
                "B) Pankreas Langerhans adacığı beta hücrelerinden köken alan insülinoma, paroksismal hipoglisemi ve Whipple triadı ile karakterizedir.",
                "C) Adrenal korteksin zona glomerulosa tabakasından köken alan adenomlar aşırı aldosteron salgılayarak hipertansiyon ve hipokalemiye (Conn sendromu) neden olur.",
                "D) Anaplastik karsinomlar doku maturasyonunu kaybettikçe özgül hormon sentezleme yeteneklerini artırarak daha şiddetli endokrinopatiler oluştururlar.",
                "E) Adrenal medulladan köken alan feokromositoma aşırı katekolamin deşarjı ile paroksismal hipertansiyon krizleri, baş ağrısı ve çarpıntı yapar."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü tümörler anaplastik hale geldikçe ve diferansiasyonlarını kaybettikçe hücresel fonksiyonel maturasyonlarını ve özgül hormon sentez yolaklarını kaybederler. Bu nedenle hormon salgılayan fonksiyonel endokrin sendromlar kural olarak iyi diferansiye benign adenomlarda anaplastik malign karsinomlara kıyasla belirgin biçimde daha sık ve etkindir. A, B, C ve E seçenekleri endokrin neoplazmların klasik patofizyolojik ve klinik özellikleridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-003",
                "question": "Endokrin bez neoplazmlarının hormon üretimi ve hormonal hiperfonksiyon sendromları ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Endokrin tümörlerde hormon üretimi ve klinik hiperfonksiyon sendromları, genellikle iyi diferansiye benign tümörlerde kötü diferansiye karsinomlara göre daha sıktır.",
                    "B) Pankreas Langerhans adacığı beta hücrelerinden köken alan insülinoma, paroksismal hipoglisemi ve Whipple triadı ile karakterizedir.",
                    "C) Adrenal korteksin zona glomerulosa tabakasından köken alan adenomlar aşırı aldosteron salgılayarak hipertansiyon ve hipokalemiye (Conn sendromu) neden olur.",
                    "D) Anaplastik karsinomlar doku maturasyonunu kaybettikçe özgül hormon sentezleme yeteneklerini artırarak daha şiddetli endokrinopatiler oluştururlar.",
                    "E) Adrenal medulladan köken alan feokromositoma aşırı katekolamin deşarjı ile paroksismal hipertansiyon krizleri, baş ağrısı ve çarpıntı yapar."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü tümörler anaplastik hale geldikçe ve diferansiasyonlarını kaybettikçe hücresel fonksiyonel maturasyonlarını ve özgül hormon sentez yolaklarını kaybederler. Bu nedenle hormon salgılayan fonksiyonel endokrin sendromlar kural olarak iyi diferansiye benign adenomlarda anaplastik malign karsinomlara kıyasla belirgin biçimde daha sık ve etkindir. A, B, C ve E seçenekleri endokrin neoplazmların klasik patofizyolojik ve klinik özellikleridir."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Kanser Kaşeksisinin Patofizyolojisi ve Sitokin Ağı",
        "subtitle": "TNF-alfa (Kaşektin), İnterlökinler (IL-1, IL-6) ve Sistemik Katabolik Tüketim",
        "synthesisNarrative": "Kanser kaşeksisi basit açlıktan farklı olarak artmış bazal metabolizma hızı ile seyreder; TNF-alfa (kaşektin) lipoprotein lipazı inhibe ederek ve proteazomu uyararak yağ ve iskelet kasını tüketir.",
        "content": """Kanser kaşeksisi; ileri evre malign neoplazmı olan hastaların yaklaşık %80'inde gelişen, ilerleyici ve istemsiz kilo kaybı, derin halsizlik (asteni), yaygın iskelet kası kaybı (sarkopeni), adipöz doku depolarının tükenmesi, anemi ve iştahsızlık (anoreksi) ile karakterize kompleks bir metabolik sendromdur. Bu tablo, ileri evre kanser hastalarında doğrudan morbidite ve mortalitenin en önde gelen nedenlerinden birini oluşturur; kanser ölümlerinin en az üçte biri doğrudan kaşeksiye bağlı kardiyorespiratuar kas yetmezliğinden kaynaklanır.

Kanser kaşeksisinin anlaşılmasındaki en kritik fizyopatolojik ilke, kaşeksinin basit bir açlık (starvasyon) veya sadece yetersiz besin alımı durumu OLMADIĞIDIR. Basit açlıkta insan organizması hayatta kalabilmek için bir adaptasyon geliştirir: Bazal metabolizma hızını (BMR) belirgin şekilde düşürür, glikojen depolarını tükettikten sonra enerji kaynağı olarak öncelikle yağ dokusunu mobilize eder ve yapısal iskelet kası proteinlerini korumaya çalışır. Oysa kanser kaşeksisinde durum tam tersidir: Tümör ve konak arasındaki enflamatuar etkileşim nedeniyle bazal metabolizma hızı düşmez; aksine anormal derecede artar veya patolojik olarak yüksek kalır. Eşzamanlı olarak hem yağ dokusu hem de iskelet kası kitlesi amansız bir katabolizmaya maruz kalarak erir.

Bu masif doku yıkımının merkezinde konağın bağışıklık hücreleri (özellikle aktive makrofajlar) ve tümör hücreleri tarafından üretilen pro-enflamatuar sitokin ağı yer alır. Bu ağın baş aktörü Tümör Nekroz Faktörü-alfa'dır (TNF-alfa; bu nedenle tarihsel olarak 'Kaşektin' adını almıştır). TNF-alfa üç temel mekanizmayla yıkımı tetikler:
1) Hipotalamustaki beslenme ve tokluk merkezlerini etkileyerek iştah açıcı neuropeptid Y'yi baskılar ve şiddetli anoreksiye yol açar.
2) Yağ dokusunda kandan dolaşımdaki trigliseritlerin adiposit içine depolanmasını sağlayan temel enzim olan Lipoprotein Lipazı (LPL) güçlü biçimde inhibe eder; aynı zamanda lipolizi hızlandırarak yağ depolarını tüketir.
3) İskelet kasında ubikitin-proteazom yolağını aktive ederek miyofibriler proteinlerin proteolitik parçalanmasını uyarır.

TNF-alfa'ya ek olarak İnterlökin-1 (IL-1), İnterlökin-6 (IL-6) ve interferon-gama (IFN-gama) gibi mediyatörler karaciğerde akut faz yanıtını (CRP artışı, albümin sentezinin baskılanması) tetikler. Bu biyolojik gerçek klinikte hayati bir sonuç doğurur: Nedensel tümör kütlesi cerrahi, kemoterapi veya radyoterapi ile ortadan kaldırılmadıkça, tek başına parenteral beslenme veya kalori desteği kaşeksiyi durduramaz veya geri döndüremez.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Kanser kaşeksisinde basit açlığın aksine bazal metabolizma hızı artmıştır. Adipoz dokuda lipoprotein lipazı (LPL) inhibe ederek yağ depolanmasını engelleyen ve iskelet kasında ubikitin-proteazom yolağıyla proteolizi tetikleyen temel mediyatör TNF-alfa'dır (kaşektin).",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Kanser hastalarında iştahsızlık, yağ depolarının erimesi, kas kitlesinde masif kayıp ve artmış bazal metabolizma ile seyreden kanser kaşeksisinin patogenezinde rol oynayan en önemli pro-enflamatuar sitokin hangisidir? (TNF-alfa / Kaşektin).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Kanser kaşeksisinde basit açlıktan farklı olarak bazal metabolizma hızı artmış veya yüksek seyreder.",
            "TNF-alfa (kaşektin) lipoprotein lipazı inhibe eder ve iskelet kasında proteazom aracılı yıkımı uyarır.",
            "Nedensel tümör yok edilmedikçe tek başına beslenme desteği kaşeksi tablosunu düzeltemez."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-004",
            "question": "İleri evre kanser hastalarında görülen kanser kaşeksisinin patogenezi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Kanser kaşeksisinde basit açlığın (starvasyon) aksine bazal metabolizma hızı artmış veya patolojik olarak yüksek seyreder.",
                "B) Adipöz dokuda dolaşımdaki yağ asitlerinin depolanmasını sağlayan lipoprotein lipaz (LPL) enzimini inhibe eden temel sitokin TNF-alfa'dır.",
                "C) İskelet kasında miyofibriler proteinlerin yıkımı temel olarak ubikitin-proteazom yolağının aşırı aktivasyonuyla gerçekleşir.",
                "D) Kanser kaşeksisi sadece yetersiz gıda alımına bağlı bir tablo olduğundan agresif parenteral beslenme desteği ile tümör varlığında dahi tamamen düzeltilebilir.",
                "E) IL-1 ve IL-6 gibi pro-enflamatuar sitokinler karaciğerde akut faz yanıtını uyarırken hipotalamus üzerinden iştahsızlığa (anoreksi) katkıda bulunur."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü kanser kaşeksisi basit bir besin eksikliği veya açlık durumu değildir; sistemik sitokin aracılı katabolik bir yıkım tablosudur. Nedensel tümör kütlesi cerrahi veya onkolojik tedavilerle yok edilmedikçe, tek başına parenteral beslenme veya kalori desteği kaşeksinin ilerleyişini durduramaz veya geri döndüremez. A, B, C ve E seçenekleri kanser kaşeksisinin moleküler patogenezini doğru ifade eder."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-004",
                "question": "İleri evre kanser hastalarında görülen kanser kaşeksisinin patogenezi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Kanser kaşeksisinde basit açlığın (starvasyon) aksine bazal metabolizma hızı artmış veya patolojik olarak yüksek seyreder.",
                    "B) Adipöz dokuda dolaşımdaki yağ asitlerinin depolanmasını sağlayan lipoprotein lipaz (LPL) enzimini inhibe eden temel sitokin TNF-alfa'dır.",
                    "C) İskelet kasında miyofibriler proteinlerin yıkımı temel olarak ubikitin-proteazom yolağının aşırı aktivasyonuyla gerçekleşir.",
                    "D) Kanser kaşeksisi sadece yetersiz gıda alımına bağlı bir tablo olduğundan agresif parenteral beslenme desteği ile tümör varlığında dahi tamamen düzeltilebilir.",
                    "E) IL-1 ve IL-6 gibi pro-enflamatuar sitokinler karaciğerde akut faz yanıtını uyarırken hipotalamus üzerinden iştahsızlığa (anoreksi) katkıda bulunur."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü kanser kaşeksisi basit bir besin eksikliği veya açlık durumu değildir; sistemik sitokin aracılı katabolik bir yıkım tablosudur. Nedensel tümör kütlesi cerrahi veya onkolojik tedavilerle yok edilmedikçe, tek başına parenteral beslenme veya kalori desteği kaşeksinin ilerleyişini durduramaz veya geri döndüremez. A, B, C ve E seçenekleri kanser kaşeksisinin moleküler patogenezini doğru ifade eder."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Paraneoplastik Sendromlar: Genel İlkeler ve Klinik Önemi",
        "subtitle": "Uzak Sistemik Etkiler, Ektopik Peptit Sentezi ve İmmünolojik Moleküler Taklit",
        "synthesisNarrative": "Paraneoplastik sendromlar; kitle basısı veya metastaz ile açıklanamayan sistemik tablolardır; gizli malignitelerin ilk habercisi olabilir ve metastazı taklit ederek yanlış evrelemeye yol açabilir.",
        "content": """Paraneoplastik sendromlar; kanserli bir hastada ortaya çıkan, ancak tümörün primer kitle etkisiyle, komşu dokulara lokal invazyonuyla veya metastatik lezyonlarının anatomik yayılımıyla doğrudan AÇIKLANAMAYAN semptom ve bulgu kompleksleridir. Aynı zamanda bu klinik tablolar, tümörün çıktığı dokunun normal fizyolojik hormon üretimi ile de ilişkili değildir (örneğin adrenal adenomun kortizol üretmesi paraneoplastik değildir, oysa akciğer kanserinin ACTH üretmesi paraneoplastiktir).

Malign neoplazmlı hastaların yaklaşık %10-15'inde paraneoplastik sendromlar gelişir. Klinik onkolojide bu sendromların tanınması şu üç temel nedenden ötürü hayati derecede önemlidir:
1) Erken Uyarı ve Gizli Tümörün Tespiti: Paraneoplastik sendromlar, henüz primer tümör hiçbir lokal semptom vermemişken ve radyolojik olarak tespit edilemeyecek kadar küçük boyuttayken ortaya çıkan ilk klinik bulgu olabilir. Örneğin açıklanamayan bir hiperkalsemi veya dermatomyozit tablosu, altta yatan gizli bir akciğer veya over kanserinin aylar öncesinden yakalanmasını sağlayabilir.
2) Bağımsız Morbidite ve Mortalite Tehdidi: Bazı paraneoplastik tablolar, primer tümörün kendisinden çok daha hızlı biçimde hastanın hayatını tehdit edebilir. Örneğin kontrol altına alınamayan derin bir paraneoplastik hiperkalsemi kardiyak arreste; uygunsuz ADH salınımına bağlı ağır hiponatremi ise serebral ödem ve status epileptikusa yol açarak hastayı öldürebilir.
3) Yanlış Evreleme ve Tedavi Hatası Tuzağı: Paraneoplastik semptomlar sıklıkla yaygın metastatik hastalığı taklit edebilir. Örneğin bir karsinom hastasında paraneoplastik periferik nöropati veya hipertrofik osteoartropatinin kemik ağrıları, hekim tarafından kemik veya beyin metastazı (Evre IV) zannedilebilir. Bu durum küratif cerrahi şansı olan bir hastanın yanlışlıkla inoperabl kabul edilmesine yol açabilir.

Paraneoplastik sendromların iki ana etyopatogenetik mekanizması vardır:
Birincisi, tümör hücrelerinin genomik instabilite ve transkripsiyonel disregülasyon sonucu embriyonik veya ektopik genleri aktive ederek hormon veya sitokin benzeri peptitler üretmesidir (örneğin nöroendokrin tümörlerin ACTH veya ADH salgılaması, karsinomların PTHrP üretmesi).
İkincisi ise immünolojik mekanizmadır: Tümör hücreleri tarafından eksprese edilen onkonöral veya hücresel neoantijenler, konağın bağışıklık sistemi tarafından yabancı olarak algılanır. Üretilen antikorlar ve sitotoksik T hücreleri, normal nöronal veya kas dokusundaki benzer antijenlerle çapraz reaksiyona girerek (moleküler taklit) otoimmün doku hasarı meydana getirir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Paraneoplastik sendromlar metastatik yayılıma bağlı değildir; gizli bir tümörün ilk belirtisi olabilir ve metastazı taklit ederek küratif cerrahi adayı hastaların yanlışlıkla Evre IV olarak değerlendirilmesine yol açabilir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Kanserli bir olguda primer tümörün anatomik basısı, lokal invazyonu veya metastazı ile açıklanamayan, primer dokunun fizyolojik fonksiyonuna ait olmayan uzak sistemik semptomlar bütününe ne ad verilir? (Paraneoplastik sendrom).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Kanser hastalarının yaklaşık %10-15'inde paraneoplastik sendrom izlenir.",
            "Gizli bir malignitenin ilk klinik habercisi olarak erken tanı fırsatı sunabilir.",
            "Ektopik hormon üretimi ve otoantikor aracılı immünolojik çapraz reaksiyon olmak üzere iki temel mekanizmayla oluşur."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-005",
            "question": "Paraneoplastik sendromların genel ilkeleri ve klinik önemi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Paraneoplastik sendromlar tümörün lokal invazyonu veya metastatik lezyonlarının doğrudan basısı ile açıklanamayan sistemik tablolardır.",
                "B) Kanserli olguların yaklaşık %10-15'inde görülür ve bazen gizli bir malignitenin ilk klinik belirtisi olarak erken tanı fırsatı sağlar.",
                "C) Paraneoplastik bir sendromun varlığı, hastada mutlaka yaygın uzak organ metastazı (Evre IV) geliştiğini kanıtlar.",
                "D) Paraneoplastik semptomlar klinik ve radyolojik olarak metastatik hastalığı taklit ederek yanlış evrelemeye (overstaging) yol açabilir.",
                "E) Ektopik peptit sentezi ve tümör antijenlerine karşı oluşan otoantikorların normal dokularla çapraz reaksiyonu (moleküler taklit) iki temel patogenetik mekanizmadır."
            ],
            "correctAnswer": 2,
            "explanation": "C seçeneği yanlıştır çünkü paraneoplastik sendromlar metastatik yayılıma bağlı DEĞİLDİR. Aksine, primer tümör henüz hiçbir metastaz yapmamışken ve erken lokalize evredeyken de paraneoplastik sendrom ortaya çıkabilir. Hatta paraneoplastik bulguların metastaz zannedilmesi hastanın yanlışlıkla Evre IV kabul edilmesine ve küratif cerrahi şansını kaçırmasına yol açabilir. A, B, D ve E seçenekleri paraneoplastik sendromların temel kavramlarıdır."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-005",
                "question": "Paraneoplastik sendromların genel ilkeleri ve klinik önemi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Paraneoplastik sendromlar tümörün lokal invazyonu veya metastatik lezyonlarının doğrudan basısı ile açıklanamayan sistemik tablolardır.",
                    "B) Kanserli olguların yaklaşık %10-15'inde görülür ve bazen gizli bir malignitenin ilk klinik belirtisi olarak erken tanı fırsatı sağlar.",
                    "C) Paraneoplastik bir sendromun varlığı, hastada mutlaka yaygın uzak organ metastazı (Evre IV) geliştiğini kanıtlar.",
                    "D) Paraneoplastik semptomlar klinik ve radyolojik olarak metastatik hastalığı taklit ederek yanlış evrelemeye (overstaging) yol açabilir.",
                    "E) Ektopik peptit sentezi ve tümör antijenlerine karşı oluşan otoantikorların normal dokularla çapraz reaksiyonu (moleküler taklit) iki temel patogenetik mekanizmadır."
                ],
                "correctAnswer": 2,
                "explanation": "C seçeneği yanlıştır çünkü paraneoplastik sendromlar metastatik yayılıma bağlı DEĞİLDİR. Aksine, primer tümör henüz hiçbir metastaz yapmamışken ve erken lokalize evredeyken de paraneoplastik sendrom ortaya çıkabilir. Hatta paraneoplastik bulguların metastaz zannedilmesi hastanın yanlışlıkla Evre IV kabul edilmesine ve küratif cerrahi şansını kaçırmasına yol açabilir. A, B, D ve E seçenekleri paraneoplastik sendromların temel kavramlarıdır."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Majör Paraneoplastik Endokrinopatiler: Hiperkalsemi, Cushing ve SIADH",
        "subtitle": "PTHrP Üretimi, Ektopik ACTH Sekresyonu ve Uygunsuz ADH Sendromu",
        "synthesisNarrative": "En sık paraneoplastik sendrom PTHrP aracılı hiperkalsemi olup en sık akciğer skuamöz hücreli karsinomunda görülür; ektopik ACTH ve SIADH ise en sık akciğer küçük hücreli karsinomu ile ilişkilidir.",
        "content": """Endokrin paraneoplastik sendromlar, tümörlerin normalde o dokuda üretilmeyen hormonları veya hormon benzeri peptitleri otonom biçimde sentezlemesiyle ortaya çıkar. Bu grupta klinikte en sık karşılaşılan üç majör sendrom hiperkalsemi, Cushing sendromu ve uygunsuz ADH salınımıdır (SIADH).

Paraneoplastik Hiperkalsemi, tüm kanser hastalarında en sık görülen paraneoplastik sendromdur. Bu sendromun klinik ve patolojik olarak iki temel formu vardır:
1) Hümoral Hiperkalsemi: En sık mekanizmadır. Kemiklerde hiçbir metastatik odak bulunmamasına rağmen, tümör hücreleri tarafından dolaşıma Paratiroid Hormon İlişkili Protein (PTHrP) salgılanır. PTHrP, normal PTH reseptörlerine (PTH1R) bağlanarak osteoklastik kemik rezorpsiyonunu ve böbrekten kalsiyum geri emilimini uyarır. En sık Akciğer Skuamöz Hücreli Karsinomu'nda görülür; ayrıca meme karsinomu, renal hücreli karsinom ve erişkin T hücreli lösemi/lenfomada (HTLV-1 ilişkili) sıktır. Ek olarak TGF-alfa ve tümör kaynaklı aktif D vitamini metabolitleri (lenfomalarda 1-alfa hidroksilaz üretimi) hiperkalsemiyi tetikleyebilir.
2) Osteolitik Hiperkalsemi: Kemik metastazlarının (multipl miyelom veya metastatik meme kanseri) lokal sitokinler (RANKL, IL-1, TNF) salgılayarak kemiği doğrudan eritmesiyle oluşur; bu durum gerçek anlamda paraneoplastik değil, metastatik kitle etkisidir. Hiperkalsemi klinikte letarji, konfüzyon, kas güçsüzlüğü, poliüri, kabızlık, bulantı ve kardiyak ritim bozuklukları ile kendini gösterir.

Ektopik Cushing Sendromu: Malign tümörlerin kontrolsüz ACTH veya pro-opiomelanokortin (POMC) üretimine bağlı gelişir. En sık Akciğer Küçük Hücreli Karsinomu'nda (SCLC; yaklaşık %50'sinden sorumludur) ve bronşiyal karsinoid tümörlerde görülür. Hipofiz kaynaklı Cushing hastalığından farkı; tablonun çok hızlı gelişmesi, hipofiz-adrenal aksın yüksek doz deksametazonla dahi baskılanamaması ve masif hipokalemik metabolik alkaloz, şiddetli hipertansiyon ve hiperpigmentasyonun (POMC türevlerine bağlı) ön planda olmasıdır.

Uygunsuz Antidiüretik Hormon Salınımı Sendromu (SIADH): En sık yine Akciğer Küçük Hücreli Karsinomu (SCLC) ve intrakraniyal neoplazmlar tarafından salgılanan otonom ADH (vazopressin) nedeniyle oluşur. Aşırı ADH böbrek toplayıcı kanallarında akuaporin-2 kanallarını açarak aşırı serbest su geri emilimine yol açar. Sonuçta dolaşımda hipervolemi olmaksızın derin bir dilüsyonel hiponatremi tablosu gelişir. Serum osmolaritesi düşerken idrar konsantre kalır. Hastada beyin ödemi, baş ağrısı, konfüzyon, nöbet ve koma gelişebilir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "En sık görülen paraneoplastik sendrom hiperkalsemidir ve kemik metastazı olmaksızın en sık Akciğer Skuamöz Hücreli Karsinomundan salgılanan PTHrP (Paratiroid Hormon İlişkili Protein) aracılığıyla meydana gelir. Ektopik Cushing ve SIADH ise en sık Akciğer Küçük Hücreli Karsinomu (SCLC) ile ilişkilidir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Kemik grafisinde metastaz saptanmayan, ancak serum kalsiyumu belirgin yüksek bulunan bir akciğer skuamöz hücreli karsinom olgusunda paraneoplastik hiperkalsemiye yol açan temel biyomolekül hangisidir? (PTHrP - Paratiroid Hormon İlişkili Protein).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "En sık paraneoplastik sendrom olan hiperkalsemiye en sık akciğer skuamöz hücreli karsinomu (PTHrP ile) yol açar.",
            "Ektopik ACTH üretimi en sık akciğer küçük hücreli karsinomunda (SCLC) izlenir ve ağır hipokalemi ile seyreder.",
            "SIADH, SCLC kaynaklı otonom ADH üretimi sonucu dilüsyonel hiponatremi ve nörolojik semptomlar oluşturur."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-006",
            "question": "Kanser hastalarında görülen paraneoplastik endokrinopatilerle ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
            "options": [
                "A) Paraneoplastik hiperkalsemi (PTHrP aracılı) — En sık Akciğer Skuamöz Hücreli Karsinomu",
                "B) Ektopik ACTH salınımı ve Cushing sendromu — En sık Renal Hücreli Karsinom",
                "C) Uygunsuz ADH salınımı (SIADH) — En sık Akciğer Adenokarsinomu",
                "D) Paraneoplastik hipoglisemi (İnsülin benzeri büyüme faktörü) — En sık Tiroid Medüller Karsinomu",
                "E) Eritropoetin salınımı ve polisitemi — En sık Akciğer Küçük Hücreli Karsinomu"
            ],
            "correctAnswer": 0,
            "explanation": "A seçeneği doğrudur. Kanser hastalarında en sık görülen paraneoplastik sendrom hiperkalsemidir ve kemik metastazı olmaksızın en sık Akciğer Skuamöz Hücreli Karsinomundan salgılanan PTHrP (Paratiroid Hormon İlişkili Protein) aracılığıyla meydana gelir. B ve C yanlıştır (Ektopik ACTH ve SIADH en sık Akciğer Küçük Hücreli Karsinomunda [SCLC] görülür). D yanlıştır (paraneoplastik hipoglisemi mezenkimal fibrosarkomlar ve retroperitoneal sarkomlarla ilişkilidir). E yanlıştır (paraneoplastik eritropoetin salınımı renal hücreli karsinom, serebellar hemanjiyom ve hepatosellüler karsinomda görülür)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-006",
                "question": "Kanser hastalarında görülen paraneoplastik endokrinopatilerle ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                "options": [
                    "A) Paraneoplastik hiperkalsemi (PTHrP aracılı) — En sık Akciğer Skuamöz Hücreli Karsinomu",
                    "B) Ektopik ACTH salınımı ve Cushing sendromu — En sık Renal Hücreli Karsinom",
                    "C) Uygunsuz ADH salınımı (SIADH) — En sık Akciğer Adenokarsinomu",
                    "D) Paraneoplastik hipoglisemi (İnsülin benzeri büyüme faktörü) — En sık Tiroid Medüller Karsinomu",
                    "E) Eritropoetin salınımı ve polisitemi — En sık Akciğer Küçük Hücreli Karsinomu"
                ],
                "correctAnswer": 0,
                "explanation": "A seçeneği doğrudur. Kanser hastalarında en sık görülen paraneoplastik sendrom hiperkalsemidir ve kemik metastazı olmaksızın en sık Akciğer Skuamöz Hücreli Karsinomundan salgılanan PTHrP (Paratiroid Hormon İlişkili Protein) aracılığıyla meydana gelir. B ve C yanlıştır (Ektopik ACTH ve SIADH en sık Akciğer Küçük Hücreli Karsinomunda [SCLC] görülür). D yanlıştır (paraneoplastik hipoglisemi mezenkimal fibrosarkomlar ve retroperitoneal sarkomlarla ilişkilidir). E yanlıştır (paraneoplastik eritropoetin salınımı renal hücreli karsinom, serebellar hemanjiyom ve hepatosellüler karsinomda görülür)."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Nörolojik, Dermatolojik ve Vasküler Paraneoplastik Sendromlar",
        "subtitle": "Lambert-Eaton, Myastenia Gravis, Akantozis Nigrikans, Trousseau ve Marantik Endokardit",
        "synthesisNarrative": "Lambert-Eaton sendromu SCLC ile ilişkili kalsiyum kanalı otoantikorlarına dayanırken; timoma myastenia ve saf kırmızı hücre aplazisiyle, pankreas kanseri ise Trousseau tromboflebitiyle eşleşir.",
        "content": """Paraneoplastik sendromlar yalnızca hormonal mekanizmalarla sınırlı kalmayıp; otoantikorlar, büyüme faktörleri ve pıhtılaşmayı tetikleyen tümör ürünleri aracılığıyla sinir, kas, deri ve damar sistemlerinde özgül tablolar meydana getirirler.

Nöromusküler ve İmmünolojik Sendromlar:
1) Lambert-Eaton Miyastenik Sendromu: En sık Akciğer Küçük Hücreli Karsinomu (SCLC) zemininde gelişir. Presinaptik voltaj kapılı kalsiyum kanallarına (P/Q tipi VGCC) karşı otoantikorlar oluşur; asetilkolin salınımı bloke olur. Myastenia Gravis'ten farkı, kas güçsüzlüğünün tekrarlayan egzersizle geçici olarak ARTMA göstermesidir.
2) Myastenia Gravis ve Saf Kırmızı Hücre Aplazisi (Pure Red Cell Aplasia): Her iki tablo da Timoma ile güçlü birliktelik gösterir. Myastenia gravis'te postsinaptik asetilkolin reseptörlerine (AChR) karşı antikorlar oluşur; yorulmakla artan pitoz ve diplopi izlenir. Timomalı olgularda ayrıca eritroid öncüllerin seçici baskılanmasına bağlı saf kırmızı hücre aplazisi gelişebilir.

Dermatolojik Paraneoplastik Sendromlar:
1) Akantozis Nigrikans: Aksilla, ense ve fleksör alanlarda derinin kadifemsi, hiperpigmente kalınlaşmasıdır. İleri yaşta aniden gelişen malign formu başta Mide Adenokarsinomu olmak üzere gastrointestinal kanserlerin habercisidir. Tümör kaynaklı EGF ve TGF-alfa salınımıyla keratinosit proliferasyonu tetiklenir.
2) Dermatomyozit: Proksimal kas güçsüzlüğü, heliotrop döküntü ve Gottron papülleri ile karakterizedir; altta yatan akciğer, meme veya over karsinomu ile ilişkili otoimmün bir tablodur.

Vasküler ve Hematolojik Paraneoplastik Tablolar:
1) Trousseau Sendromu (Tromboflebitis Migrans): Ekstremitelerde yer değiştiren gezici yüzeyel venöz trombozlardır. Başta Pankreas Adenokarsinomu olmak üzere müsinöz karsinomlarda izlenir; tümör müsinlerinin faktör X ve pıhtılaşmayı aktive etmesiyle oluşur.
2) Nonbakteriyel Trombotik Endokardit (Marantik Endokardit): İleri evre kanserlerde kalp kapaklarında steril fibrin-trombosit vejetasyonlarının oluşmasıdır; sistemik embolilere zemin hazırlar.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Lambert-Eaton sendromu SCLC ile ilişkili presinaptik kalsiyum kanalı blokajıdır (egzersizle güç artar). Timoma; Myastenia Gravis ve saf eritrosit aplazisi (pure red cell aplasia) ile ilişkilidir. Gezici tromboflebit (Trousseau fenomeni) ise pankreas adenokarsinomunun klasik paraneoplastik bulgusudur.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "İleri yaşta ani başlayan generalize akantozis nigrikans lezyonları saptanan bir hastada öncelikle hangi organ malignitesi araştırılmalıdır? (Mide adenokarsinomu).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Lambert-Eaton sendromu presinaptik VGCC antikorlarına bağlıdır ve SCLC ile güçlü ilişkilidir.",
            "Ani gelişen malign akantozis nigrikans en sık mide adenokarsinomu ile ilişkilidir.",
            "Trousseau sendromu (gezici tromboflebit), pankreas adenokarsinomunun müsin kaynaklı hiperkoagülabilite tablosudur."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-007",
            "question": "Aşağıdaki paraneoplastik sendrom ve ilişkili klinik/patolojik mekanizma eşleştirmelerinden hangisi YANLIŞTIR?",
            "options": [
                "A) Lambert-Eaton sendromu — Akciğer küçük hücreli karsinoması zemininde presinaptik voltaj kapılı kalsiyum kanallarına karşı antikor gelişimi",
                "B) Saf kırmızı hücre aplazisi (Pure red cell aplasia) — Timoma zemininde eritroid öncüllerin immünolojik baskılanması",
                "C) Trousseau sendromu (gezici tromboflebit) — Pankreas ve müsinöz adenokarsinomlarda müsinlerin pıhtılaşma faktörlerini aktive etmesi",
                "D) Malign Akantozis Nigrikans — Mide adenokarsinomu zemininde büyüme faktörlerinin keratinositleri stimüle etmesi",
                "E) Myastenia Gravis — Renal hücreli karsinom zemininde eritropoetin aracılı nöromusküler kavşak hasarı"
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır çünkü Myastenia Gravis renal hücreli karsinomla değil, Timoma ile güçlü birliktelik gösterir ve patogenezinde postsinaptik asetilkolin reseptörlerine (AChR) karşı gelişen otoantikorlar rol oynar (eritropoetin ile hiçbir ilgisi yoktur). A, B, C ve D seçeneklerindeki klinik sendrom, tümör ve mekanizma eşleştirmeleri tamamen doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-007",
                "question": "Aşağıdaki paraneoplastik sendrom ve ilişkili klinik/patolojik mekanizma eşleştirmelerinden hangisi YANLIŞTIR?",
                "options": [
                    "A) Lambert-Eaton sendromu — Akciğer küçük hücreli karsinoması zemininde presinaptik voltaj kapılı kalsiyum kanallarına karşı antikor gelişimi",
                    "B) Saf kırmızı hücre aplazisi (Pure red cell aplasia) — Timoma zemininde eritroid öncüllerin immünolojik baskılanması",
                    "C) Trousseau sendromu (gezici tromboflebit) — Pankreas ve müsinöz adenokarsinomlarda müsinlerin pıhtılaşma faktörlerini aktive etmesi",
                    "D) Malign Akantozis Nigrikans — Mide adenokarsinomu zemininde büyüme faktörlerinin keratinositleri stimüle etmesi",
                    "E) Myastenia Gravis — Renal hücreli karsinom zemininde eritropoetin aracılı nöromusküler kavşak hasarı"
                ],
                "correctAnswer": 4,
                "explanation": "E seçeneği yanlıştır çünkü Myastenia Gravis renal hücreli karsinomla değil, Timoma ile güçlü birliktelik gösterir ve patogenezinde postsinaptik asetilkolin reseptörlerine (AChR) karşı gelişen otoantikorlar rol oynar (eritropoetin ile hiçbir ilgisi yoktur). A, B, C ve D seçeneklerindeki klinik sendrom, tümör ve mekanizma eşleştirmeleri tamamen doğrudur."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Kanser Derecelendirmesi (Grading): Histopatolojik Diferansiasyon ve Agresiflik",
        "subtitle": "Diferansiasyon Derecesi, Mitotik İndeks, Nükleer Pleomorfizm ve Tümör Nekrozu",
        "synthesisNarrative": "Kanser derecelendirmesi (grading) mikroskobik diferansiasyonu, nükleer pleomorfizmi ve mitotik indeksi değerlendiren patolojik bir incelemedir; Grade 1'den Grade 4'e (anaplastik) uzanır.",
        "content": """Kanser derecelendirmesi (grading); malign neoplazm kesitlerinin ışık mikroskobu altında incelenerek, tümör hücrelerinin köken aldıkları normal dokuya benzerlik derecesini (diferansiasyon) ve proliferasyon hızını belirleyen histopatolojik bir değerlendirmedir. Temel amaç, tümörün biyolojik davranış agresifliğini tahmin etmektir.

Patolog mikroskop başında bir tümörü derecelendirirken dört temel morfolojik unsuru analiz eder:
1) Diferansiasyon ve Mimari Düzen: Hücrelerin normal doku mimarisini taklit edebilme yetisidir. Örneğin adenokarsinomun glandüler tübüller yapabilmesi veya skuamöz karsinomun keratin incileri üretmesi diferansiasyon kanıtıdır. Bez yapısının kaybolup solid tabakalar oluşması diferansiasyon kaybını gösterir.
2) Nükleer Atipi ve Pleomorfizm: Nükleusların boyut, şekil ve kromatin dağılımındaki anormalliklerdir. Hiperkromazi, kaba kromatin, belirgin nükleoller ve artmış nükleus/sitoplazma (N/C) oranı yüksek derece işaretidir.
3) Mitotik Aktivite: Standart yüksek büyütme alanında (HPF) sayılan mitotik figür sayısıdır. Sayıca artışın yanı sıra tripolar veya yıldızsı atipik mitozların varlığı malignitenin agresifliğini yansıtır.
4) Tümör Nekrozu: Hızlı büyümenin anjiyogenez kapasitesini aşmasıyla gelişen koagülasyon nekrozu alanlarıdır; yüksek biyolojik agresiflik göstergesidir.

Standart Dörtlü Derecelendirme Skalası:
- Grade 1 (İyi Diferansiye / Low Grade): Hücreler ve mimari normal dokuya çok benzer. Bezler düzenlidir, mitotik aktivite düşüktür.
- Grade 2 (Orta Diferansiye): Bez yapıları kısmen korunmuştur, orta düzeyde pleomorfizm ve mitoz izlenir.
- Grade 3 (Kötü Diferansiye / High Grade): Mimari büyük ölçüde bozulmuştur, düzensiz hücre tabakaları, belirgin atipi ve yüksek mitotik indeks mevcuttur.
- Grade 4 (Anaplastik / Diferansiye Olmamış): Orijinal dokuya dair hiçbir morfolojik iz taşımayan, aşırı pleomorfik dev tümör hücreleri hakimdir.

Derecelendirmenin Sınırlılıkları: Subjektif bir morfolojik inceleme olduğundan gözlemciler arası (inter-observer) değişkenlik gösterebilir ve tümör içi heterojeniteden etkilenebilir. Bu nedenle meme kanserinde Nottingham ve prostatta Gleason / ISUP skoru gibi objektif puanlama sistemleri geliştirilmiştir.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Grading (derecelendirme) saf mikroskobik/histopatolojik bir değerlendirmedir; tümörün diferansiasyonunu, hücresel pleomorfizmini ve mitotik indeksini inceler. Biyolojik agresiflik hakkında kaba bir tahmin sağlasa da gözlemciye bağımlı ve subjektif yönü vardır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Malign tümörlerin histopatolojik incelenmesinde glandüler tübül formasyonu yapabilme derecesi, nükleer pleomorfizm ve yüksek büyütme alanındaki mitoz sayısı puanlanarak yapılan değerlendirmeye ne ad verilir? (Grading / Derecelendirme).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Derecelendirme (Grading), tümörün mikroskobik diferansiasyonunu ve mitotik aktivitesini gösterir.",
            "Grade 1 iyi diferansiye iken, Grade 4 tamamen anaplastik ve diferansiye olmamış tümörü ifade eder.",
            "Subjektif değişkenliği azaltmak için Nottingham (meme) ve Gleason (prostat) gibi özel skorlama sistemleri kullanılır."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-008",
            "question": "Malign tümörlerde kanser derecelendirmesi (grading) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Grading, doku kesitlerinin ışık mikroskobunda incelenmesine dayanan histopatolojik bir değerlendirmedir.",
                "B) Bir tümörün bez (tübül) yapma veya keratin üretme yeteneğini koruması iyi diferansiye (Grade 1) göstergesidir.",
                "C) Yüksek büyütme alanında (HPF) sayılan mitotik figür sayısının ve atipik mitozların artması derecenin yükseldiğini gösterir.",
                "D) Grading, patologlar arasında hiçbir sübjektif değişkenlik içermeyen, tümör içi heterojeniteden etkilenmeyen mutlak bir ölçümdür.",
                "E) Anaplastik (Grade 4) tümörler köken aldıkları normal dokuya ait hiçbir mimari ve sitolojik özellik barındırmazlar."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü grading (derecelendirme) ışık mikroskobunda yapılan görsel bir morfolojik inceleme olduğundan patologlar arasında gözlemci içi ve gözlemciler arası (intra/inter-observer) sübjektif değişkenlik gösterebilir. Ayrıca tümörün farklı alanlarında diferansiasyon derecesi değişebileceğinden (tümör içi heterojenite), sınırlı biyopsiler tüm tümörün derecesini tam yansıtmayabilir. Bu nedenle meme (Nottingham) ve prostatta (Gleason) skorlama sistemleri geliştirilmiştir. A, B, C ve E seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-008",
                "question": "Malign tümörlerde kanser derecelendirmesi (grading) ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Grading, doku kesitlerinin ışık mikroskobunda incelenmesine dayanan histopatolojik bir değerlendirmedir.",
                    "B) Bir tümörün bez (tübül) yapma veya keratin üretme yeteneğini koruması iyi diferansiye (Grade 1) göstergesidir.",
                    "C) Yüksek büyütme alanında (HPF) sayılan mitotik figür sayısının ve atipik mitozların artması derecenin yükseldiğini gösterir.",
                    "D) Grading, patologlar arasında hiçbir sübjektif değişkenlik içermeyen, tümör içi heterojeniteden etkilenmeyen mutlak bir ölçümdür.",
                    "E) Anaplastik (Grade 4) tümörler köken aldıkları normal dokuya ait hiçbir mimari ve sitolojik özellik barındırmazlar."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü grading (derecelendirme) ışık mikroskobunda yapılan görsel bir morfolojik inceleme olduğundan patologlar arasında gözlemci içi ve gözlemciler arası (intra/inter-observer) sübjektif değişkenlik gösterebilir. Ayrıca tümörün farklı alanlarında diferansiasyon derecesi değişebileceğinden (tümör içi heterojenite), sınırlı biyopsiler tüm tümörün derecesini tam yansıtmayabilir. Bu nedenle meme (Nottingham) ve prostatta (Gleason) skorlama sistemleri geliştirilmiştir. A, B, C ve E seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Kanser Evrelemesi (Staging): Anatomik Yayılım ve Tedavi Seçimindeki Rol",
        "subtitle": "Anatomik Yayılım Sınırları, Tümör Yükü ve Onkolojik Karar Hiyerarşisi",
        "synthesisNarrative": "Kanser evrelemesi (staging) tümörün anatomik yayılım derecesini ve metastaz varlığını tanımlar; prognozu belirlemede ve tedavi protokolü seçiminde derecelendirmeden çok daha üstündür.",
        "content": """Kanser evrelemesi (staging); bir malign neoplazmın tanı anında konak organizma içerisindeki anatomik yayılım derecesinin, primer kitle büyüklüğünün, komşu organlara lokal invazyon derinliğinin, bölgesel lenfatik havzaya sıçrama durumunun ve uzak organlara metastaz yapıp yapmadığının belirlenmesidir. Evreleme, mikroskobik hücresel detaylara değil; tümörün makroskobik ve anatomik sınırlarına odaklanan klinik, radyolojik ve cerrahi-patolojik bir süreçtir.

Onkoloji ve Tıbbi Patolojinin Altın Kuralı:
Kanser hastasında hastalığın prognozunu (beklenen sağkalım süresini) belirlemede ve hastaya uygulanacak cerrahi rezeksiyon, kemoterapi, radyoterapi veya palyatif bakım kararlarını vermede Evreleme (Staging), Derecelendirmeden (Grading) çok daha güçlü, bağımsız ve belirleyicidir!

Bu aksiyomun klinik mantığı son derece berraktır: Bir tümör mikroskop altında Grade 1 (iyi diferansiye) morfolojide olsa dahi, eğer tanı anında karaciğere veya akciğere uzak metastaz yapmışsa (Evre IV), hastanın ortanca sağkalımı aylar veya sınırlı yıllarla ölçülecektir. Buna karşılık, mikroskop altında Grade 3 (kötü diferansiye, bol mitozlu, ileri derecede atipik) morfolojiye sahip bir adenokarsinom yalnızca 0,8 cm boyutundayken erken evrede (Evre I / T1 N0 M0) yakalanıp cerrahi olarak tamamen çıkarıldığında, 5 yıllık hastalıksız sağkalım oranı %90'ın üzerindedir. Dolayısıyla tümörün biyolojik hücresel derecesi ne olursa olsun, nihai klinik sonucu ve kür şansını anatomik yayılımın derecesi (evre) belirler.

Modern onkolojik tedavi protokollerinin tamamı evreleme basamaklarına göre şekillendirilir:
- Erken Evre (Evre I): Tümör organa sınırlıdır, lenf nodu tutulumu yoktur. Temel tedavi küratif cerrahi rezeksiyondur.
- Lokal İleri Evre (Evre II - III): Kitle çevre dokuları invaze etmiş veya bölgesel lenf nodlarına yayılmıştır. Cerrahi öncesi tümör kütlesini küçültmek için neoadjuvan tedavi ve cerrahi sonrasında adjuvan kemoradyoterapi protokolleri devreye girer.
- Metastatik Evre (Evre IV): Uzak organ metastazı mevcuttur; cerrahi kural olarak küratif vasfını kaybeder, sistemik kemoterapi, hedefe yönelik tedaviler, immünoterapi ve palyatif destek ön plana geçer.

Aynı histolojik tipteki iki tümör, tamamen aynı patolog tarafından incelenip aynı dereceyi alsa dahi; farklı evrelerde bulunduklarında birbirlerinden tamamen zıt klinik seyir gösterirler. Bu nedenle kanserli her hastada tedavinin ilk ve vazgeçilmez adımı doğru evrelemenin eksiksiz yapılmasıdır.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Kanserli bir hastada prognozu (sağkalımı) belirlemede ve tedavi protokolü seçiminde Evreleme (Staging), Derecelendirmeden (Grading) tartışmasız çok daha üstün, güçlü ve belirleyicidir!",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Solid organ malignitelerinde tedavi stratejisinin belirlenmesinde ve genel sağkalım prognozunun tahmin edilmesinde en güvenilir ve belirleyici parametre hangisidir? (Tümörün evresi / Staging).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Evreleme tümörün anatomik yayılım derecesini, kitle boyutunu ve metastaz varlığını tanımlar.",
            "Prognoz ve tedavi seçiminde Evreleme (Staging), Derecelendirmeden (Grading) çok daha üstündür.",
            "Grade 1 metastatik bir tümörün prognozu, Grade 3 erken evre lokalize bir tümörden çok daha kötüdür."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-009",
            "question": "Kanser evrelemesi (staging) ile derecelendirme (grading) arasındaki klinik ve prognostik ilişki hakkında aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
            "options": [
                "A) Hastanın sağkalım prognozunu belirlemede ve tedavi seçiminde Evreleme (Staging), Derecelendirmeden (Grading) çok daha üstün ve belirleyicidir.",
                "B) Derecelendirme (Grading) klinik ve radyolojik bir inceleme iken, Evreleme (Staging) saf mikroskobik bir incelemedir.",
                "C) Grade 1 (iyi diferansiye) olan bir tümör karaciğer metastazı yapsa dahi prognozu Evre I Grade 3 bir tümörden her zaman daha iyidir.",
                "D) Cerrahi rezeksiyon kararı verilirken tümörün evresine bakılmaz, sadece histolojik derecesi esas alınır.",
                "E) Aynı evrede bulunan iki hastada histolojik diferansiasyon derecesinin prognoz üzerinde hiçbir etkisi olamaz."
            ],
            "correctAnswer": 0,
            "explanation": "A seçeneği kesinlikle doğrudur. Onkoloji patolojisinin altın kuralı: Prognozu (sağkalımı) belirlemede ve hastaya cerrahi, kemoterapi veya radyoterapi protokolü seçiminde Evreleme (Staging), Derecelendirmeden (Grading) çok daha güçlü, bağımsız ve belirleyicidir. B yanlıştır (tam tersidir; grading mikroskobik, staging klinik-radyolojik-anatomiktir). C yanlıştır (uzak metastazlı Grade 1 tümör Evre IV'tür ve prognozu çok kötüdür). D yanlıştır (cerrahi kararı doğrudan evreye bağlıdır). E yanlıştır (derecelendirme evre içinde ek prognostik bilgi sağlar)."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-009",
                "question": "Kanser evrelemesi (staging) ile derecelendirme (grading) arasındaki klinik ve prognostik ilişki hakkında aşağıdaki ifadelerden hangisi KESİNLİKLE DOĞRUDUR?",
                "options": [
                    "A) Hastanın sağkalım prognozunu belirlemede ve tedavi seçiminde Evreleme (Staging), Derecelendirmeden (Grading) çok daha üstün ve belirleyicidir.",
                    "B) Derecelendirme (Grading) klinik ve radyolojik bir inceleme iken, Evreleme (Staging) saf mikroskobik bir incelemedir.",
                    "C) Grade 1 (iyi diferansiye) olan bir tümör karaciğer metastazı yapsa dahi prognozu Evre I Grade 3 bir tümörden her zaman daha iyidir.",
                    "D) Cerrahi rezeksiyon kararı verilirken tümörün evresine bakılmaz, sadece histolojik derecesi esas alınır.",
                    "E) Aynı evrede bulunan iki hastada histolojik diferansiasyon derecesinin prognoz üzerinde hiçbir etkisi olamaz."
                ],
                "correctAnswer": 0,
                "explanation": "A seçeneği kesinlikle doğrudur. Onkoloji patolojisinin altın kuralı: Prognozu (sağkalımı) belirlemede ve hastaya cerrahi, kemoterapi veya radyoterapi protokolü seçiminde Evreleme (Staging), Derecelendirmeden (Grading) çok daha güçlü, bağımsız ve belirleyicidir. B yanlıştır (tam tersidir; grading mikroskobik, staging klinik-radyolojik-anatomiktir). C yanlıştır (uzak metastazlı Grade 1 tümör Evre IV'tür ve prognozu çok kötüdür). D yanlıştır (cerrahi kararı doğrudan evreye bağlıdır). E yanlıştır (derecelendirme evre içinde ek prognostik bilgi sağlar)."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "TNM Evreleme Sistemi Mimarisi (AJCC / UICC)",
        "subtitle": "T (Primer Tümör), N (Bölgesel Lenf Nodu), M (Uzak Metastaz) ve Klinik Evre Gruplaması",
        "synthesisNarrative": "TNM sistemi; primer tümörün boyut/derinliğini (T), lenf nodu yayılımını (N) ve uzak metastazı (M) kodlar; Tis metastaz potansiyeli olmayan karsinoma in situ iken, M1 tümörü doğrudan Evre IV yapar.",
        "content": """Dünya genelinde malign tümörlerin anatomik yayılımını standartlaştırmak amacıyla kullanılan evrensel referans sistemi, American Joint Committee on Cancer (AJCC) ve Union for International Cancer Control (UICC) tarafından ortaklaşa yürütülen TNM Evreleme Sistemidir. Bu sistem tümörün yayılımını üç temel anatomik bileşene ayırarak harfler ve sayılarla kodlar.

1) T Kategorisi (Primer Tümör - Tumor):
- TX: Primer tümör değerlendirilemiyor (örneğin spesimen parçalanmış veya yetersiz).
- T0: Primer tümöre dair hiçbir kanıt bulunamadı.
- Tis: Karsinoma in situ. Neoplastik hücreler bazal membranı kesinlikle aşmamıştır. Kan ve lenfatik damarlar bazal membranın altındaki stromada yer aldığından, Tis lezyonlarının metastaz yapma riski sıfırdır.
- T1, T2, T3, T4: Organ spesifik kriterlere göre tanımlanan artan primer tümör büyüklüğü ve/veya primer organ duvarındaki lokal invazyon derinliğidir. Örneğin meme kanserinde kitle çapı (T1 <=2 cm, T2 2-5 cm, T3 >5 cm, T4 göğüs duvarı/cilt invazyonu) esas alınırken; gastrointestinal sistemde (mide, kolon) kitle çapı değil, duvar katmanlarının (submukoza, muskularis propria, subseroza, seroza/komşu organ) invazyon derinliği esas alınır.

2) N Kategorisi (Bölgesel Lenf Nodları - Nodes):
- NX: Bölgesel lenf nodları değerlendirilemiyor.
- N0: Bölgesel lenf nodu istasyonlarında hiçbir mikroskobik metastaz saptanmadı.
- N1, N2, N3: Bölgesel lenf nodu havzasında metastaz saptanan lenf nodu sayısının artması, metastazın daha uzak lenf nodu istasyonlarına ulaşması veya tümörün lenf nodu kapsülünü yırtarak çevre yağ dokusuna taşması (ekstrakapsüler yayılım) durumudur. Meme kanserinde aksiller lenf nodu sayısı (N1: 1-3 adet, N2: 4-9 adet, N3: >=10 adet veya supraklaviküler tutulum) kritik önem taşır.

3) M Kategorisi (Uzak Metastaz - Metastasis):
- M0: Bölgesel lenfatik havza dışında hiçbir uzak organ metastazı kanıtı yoktur.
- M1: Uzak organlara (karaciğer, akciğer, kemik, beyin, periton) veya bölgesel olmayan uzak lenf nodu gruplarına tümör metastazının varlığıdır.

Klinik Evre Gruplaması (Stage 0 - IV):
TNM bileşenleri bir araya getirilerek prognozu benzer homojen klinik evrelere dönüştürülür:
- Evre 0: Tis N0 M0 (karsinoma in situ; tam kür oranı %100).
- Evre I: T1-T2 N0 M0 (küçük, lokalize, lenf nodu negatif lezyonlar).
- Evre II ve III: T3-T4 ve/veya N1-N3 M0 (büyük primer tümörler veya lenf nodu pozitif bölgesel hastalık).
- Evre IV: Herhangi bir T, herhangi bir N ve M1. Uzak metastaz varlığı, primer tümörün boyutu veya lenf nodu tutulumu ne olursa olsun tümörü doğrudan en yüksek evre olan Evre IV'e taşır.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "TNM sınıflamasında Tis (karsinoma in situ) epitel bazal membranını aşmamış neoplazmı gösterir ve metastaz potansiyeli yoktur. M1 kategorisi ise primer tümörün boyutu ne olursa olsun hastalığı doğrudan Evre IV yapar.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "TNM evreleme sisteminde primer tümörün bazal membranı aşmadığı ve invazyon göstermediği karsinoma in situ lezyonları hangi sembolle kodlanır? (Tis).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "T kategorisi tümörün boyutunu veya organ duvarındaki invazyon derinliğini yansıtır.",
            "Tis bazal membranı aşmamış karsinoma in situdur; damar ağına ulaşamadığı için metastaz yapamaz.",
            "Tek bir uzak organ metastazının (M1) varlığı tümörü doğrudan Evre IV sınıfına sokar."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-010",
            "question": "AJCC / UICC tarafından belirlenen TNM evreleme sistemi mimarisi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Tis (karsinoma in situ), epitelyal bazal membranı henüz aşmamış lezyonları tanımlar ve metastaz yapma potansiyeli yoktur.",
                "B) T kategorisi organ spesifik kriterlere göre kitle çapını veya organ duvarındaki lokal invazyon derinliğini gösterir.",
                "C) Bölgesel lenf nodlarında mikroskobik tümör metastazı saptanmaması N0 olarak kodlanır.",
                "D) Uzak organ metastazının (M1) varlığı, primer tümörün boyutu (T) veya lenf nodu (N) ne olursa olsun tümörü doğrudan Evre IV yapar.",
                "E) Lenf nodu metastazı saptanan her olgu (N1-N3), uzak organ metastazı olmasa dahi doğrudan Evre IV kabul edilir."
            ],
            "correctAnswer": 4,
            "explanation": "E seçeneği yanlıştır çünkü uzak metastazı olmayan (M0) ancak bölgesel lenf nodu tutulumu bulunan (N1-N3) olgular Evre IV DEĞİL; primer tümörün boyutuna göre Evre II veya Evre III (lokal-bölgesel ileri evre) olarak sınıflandırılır. Bir tümörün Evre IV olabilmesi için kural olarak uzak organ metastazının (M1) bulunması gerekir. A, B, C ve D seçenekleri TNM sınıflamasının temel kurallarıdır."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-010",
                "question": "AJCC / UICC tarafından belirlenen TNM evreleme sistemi mimarisi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Tis (karsinoma in situ), epitelyal bazal membranı henüz aşmamış lezyonları tanımlar ve metastaz yapma potansiyeli yoktur.",
                    "B) T kategorisi organ spesifik kriterlere göre kitle çapını veya organ duvarındaki lokal invazyon derinliğini gösterir.",
                    "C) Bölgesel lenf nodlarında mikroskobik tümör metastazı saptanmaması N0 olarak kodlanır.",
                    "D) Uzak organ metastazının (M1) varlığı, primer tümörün boyutu (T) veya lenf nodu (N) ne olursa olsun tümörü doğrudan Evre IV yapar.",
                    "E) Lenf nodu metastazı saptanan her olgu (N1-N3), uzak organ metastazı olmasa dahi doğrudan Evre IV kabul edilir."
                ],
                "correctAnswer": 4,
                "explanation": "E seçeneği yanlıştır çünkü uzak metastazı olmayan (M0) ancak bölgesel lenf nodu tutulumu bulunan (N1-N3) olgular Evre IV DEĞİL; primer tümörün boyutuna göre Evre II veya Evre III (lokal-bölgesel ileri evre) olarak sınıflandırılır. Bir tümörün Evre IV olabilmesi için kural olarak uzak organ metastazının (M1) bulunması gerekir. A, B, C ve D seçenekleri TNM sınıflamasının temel kurallarıdır."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Klinik Evreleme (cTNM) ile Patolojik Cerrahi Evreleme (pTNM) Karşılaştırması",
        "subtitle": "Preoperatif Radyolojik Evrelemeden Cerrahi Rezeksiyon Spesimenine ve R Sınıflamasına",
        "synthesisNarrative": "cTNM preoperatif fizik muayene ve radyolojik verilere dayanırken; pTNM rezeke edilen cerrahi spesimen ve lenf nodlarının mikroskobik incelenmesiyle kesin anatomik evreyi belirler.",
        "content": """TNM evreleme sistemi statik ve tek seferlik bir kavram değildir; hastanın tanı anından cerrahi operasyona ve tedavi sonrasına uzanan klinik yolculuğunda farklı evrelerde tekrarlanarak güncellenir. Bu bağlamda klinikte en sık kullanılan ve birbirini tamamlayan iki temel evreleme düzeyi Klinik Evreleme (cTNM) ve Patolojik Cerrahi Evrelemedir (pTNM).

Klinik Evreleme (cTNM - Clinical TNM):
Herhangi bir definitif tedaviye (cerrahi rezeksiyon, kemoterapi veya radyoterapi) başlanmadan önce elde edilen tüm verilerin sentezlenmesiyle konulan evredir. Fizik muayene bulguları, görüntüleme yöntemleri (kontrastlı BT, dinamik MR, PET-BT, endoskopik ultrasonografi), endoskopik biyopsiler ve laboratuvar parametrelerine dayanır. Klinik evrelemenin en temel amacı: Hastanın anatomik rezektabilitesini (ameliyat edilebilirliğini) değerlendirmek ve hastanın doğrudan ameliyata mı gideceğine, yoksa önce tümörü küçültmek amacıyla neoadjuvan (operasyon öncesi) kemoradyoterapi mi alacağına karar vermektir.

Patolojik Cerrahi Evreleme (pTNM - Pathological TNM):
Tümörün cerrahi olarak rezeke edilmesi sonrasında, cerrahi spesimenin, tümörün duvar katmanlarındaki mikroskobik invazyon derinliğinin, cerrahi sınırların ve çıkarılan bölgesel lenf nodlarının patoloji laboratuvarında histopatolojik olarak incelenmesiyle konulur.
Klinik Karşılaştırma: pTNM, cTNM'den çok daha hassas ve kesindir. Çünkü radyolojik görüntülemelerin ayırt edemediği birkaç milimetrelik mikroskobik lenf nodu metastazlarını, perinöral invazyonu veya lenfovasküler tümör embolilerini patolog mikroskop altında kesin olarak saptar. Klinik olarak cT2 N0 M0 (Evre I) zannedilen bir olgu, patoloji incelemesinde lenf nodunda mikrometastaz saptanmasıyla pT2 N1 M0 (Evre III) olarak yukarı evrelenebilir (upstaging).

Özel Evreleme Önekleri:
- ypTNM: Neoadjuvan kemoterapi veya radyoterapi verildikten sonra ameliyat edilen cerrahi spesimende yapılan patolojik evrelemedir ('y' öneki neoadjuvan tedaviyi simgeler).
- rTNM: Tedavi sonrası remisyona girmiş bir hastada aylar veya yıllar sonra tümör nüksettiğinde yapılan re-evrelemedir ('r' öneki rekürrensi simgeler).

Rezeksiyon Marjini ve Rezidüel Tümör (R Sınıflaması):
Cerrahi operasyonun onkolojik başarısını tanımlayan evrensel patolojik ölçüttür:
- R0: Cerrahi sınırlar mikroskobik olarak tamamen temizdir (tümörsüz marjin; küratif rezeksiyon).
- R1: Makroskobik olarak tümör çıkarılmıştır ancak mikroskop altında cerrahi sınırda tümör hücreleri mevcuttur (lokal nüks riski çok yüksektir).
- R2: Cerrahın operasyon sırasında tümörü tamamen çıkaramadığı, geride gözle görülür makroskobik tümör bıraktığı durumdur (palyatif rezeksiyon).""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Neoadjuvan (ameliyat öncesi) kemoradyoterapi uygulanan bir hastanın cerrahi rezeksiyon spesimeninde yapılan patolojik evreleme 'ypTNM' olarak adlandırılır. Cerrahi sınırda mikroskobik tümör saptanması 'R1 rezeksiyon' olarak tanımlanır.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Ameliyat öncesi klinik ve radyolojik verilerle yapılan evreleme (cTNM) ile rezekte edilen cerrahi spesimen ve lenf nodlarının mikroskobik incelenmesiyle konulan kesin evreleme (pTNM) arasındaki en önemli fark nedir? (pTNM'nin histopatolojik incelemeye dayanarak cerrahi sınırlar ve mikroskobik lenf nodu metastazlarını kesin olarak göstermesi).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "cTNM preoperatif fizik muayene ve radyolojiye dayanır; neoadjuvan tedavi ve cerrahi kararını belirler.",
            "pTNM cerrahi spesimenin mikroskobik incelenmesiyle konulur; prognoz için en güvenilir evredir.",
            "R0 mikroskobik temiz cerrahi sınırı, R1 mikroskobik pozitif sınırı, R2 makroskobik kalıntı tümörü gösterir."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-011",
            "question": "Klinik evreleme (cTNM) ile patolojik cerrahi evreleme (pTNM) arasındaki farklar ve evreleme terminolojisi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) cTNM preoperatif fizik muayene, radyolojik görüntülemeler ve biyopsilerle ameliyat öncesi yapılır.",
                "B) pTNM rezeke edilen cerrahi spesimenin ve çıkarılan lenf nodlarının mikroskobik histopatolojik incelenmesine dayanır.",
                "C) Neoadjuvan (ameliyat öncesi) kemoradyoterapi uygulandıktan sonra çıkarılan spesimende yapılan patolojik evreleme 'ypTNM' olarak kodlanır.",
                "D) Cerrahi sınırda mikroskobik olarak tümör hücresi saptanması patoloji raporunda 'R0 rezeksiyon' olarak tanımlanır.",
                "E) pTNM, cerrahın veya radyoloğun gözden kaçırdığı mikroskobik lenf nodu metastazlarını göstererek klinik evreyi yukarı taşıyabilir (upstaging)."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü cerrahi sınırda mikroskobik tümör kalması 'R1 rezeksiyon' olarak adlandırılır. 'R0 rezeksiyon', mikroskobik olarak tüm cerrahi sınırların temiz (tümörsüz) olduğunu ifade eder. 'R2 rezeksiyon' ise cerrahın gözle görülür makroskobik tümör bıraktığı durumdur. A, B, C ve E seçenekleri doğrudur."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-011",
                "question": "Klinik evreleme (cTNM) ile patolojik cerrahi evreleme (pTNM) arasındaki farklar ve evreleme terminolojisi ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) cTNM preoperatif fizik muayene, radyolojik görüntülemeler ve biyopsilerle ameliyat öncesi yapılır.",
                    "B) pTNM rezeke edilen cerrahi spesimenin ve çıkarılan lenf nodlarının mikroskobik histopatolojik incelenmesine dayanır.",
                    "C) Neoadjuvan (ameliyat öncesi) kemoradyoterapi uygulandıktan sonra çıkarılan spesimende yapılan patolojik evreleme 'ypTNM' olarak kodlanır.",
                    "D) Cerrahi sınırda mikroskobik olarak tümör hücresi saptanması patoloji raporunda 'R0 rezeksiyon' olarak tanımlanır.",
                    "E) pTNM, cerrahın veya radyoloğun gözden kaçırdığı mikroskobik lenf nodu metastazlarını göstererek klinik evreyi yukarı taşıyabilir (upstaging)."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü cerrahi sınırda mikroskobik tümör kalması 'R1 rezeksiyon' olarak adlandırılır. 'R0 rezeksiyon', mikroskobik olarak tüm cerrahi sınırların temiz (tümörsüz) olduğunu ifade eder. 'R2 rezeksiyon' ise cerrahın gözle görülür makroskobik tümör bıraktığı durumdur. A, B, C ve E seçenekleri doğrudur."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Histopatolojik Biyopsi Yöntemleri ve Doku Takibi",
        "subtitle": "Eksizyonel, İnsizyonel, Kalın İğne (Tru-cut) Biyopsileri ve Doku Fiksasyonu",
        "synthesisNarrative": "Tru-cut biyopsi doku mimarisini koruyarak in situ-invaziv karsinom ayrımına izin verirken; biyopside altın standart fiksatif dokunun 10-20 katı hacimde %10 nötral tamponlu formalindir.",
        "content": """Kanser tanısında klinik ve radyolojik tüm bulgular şüphe uyandırıcı olsa da; kesin malignite tanısı, histopatolojik tiplendirme ve moleküler testlerin icrası doku biyopsisine dayanır. Biyopsi materyalinin alınış şekli, incelenecek doku hacmini, mimari bütünlüğü ve tanısal doğruluğu doğrudan etkiler.

Biyopsi Çeşitleri ve Endikasyonları:
1) Eksizyonel Biyopsi: Şüpheli lezyonun etrafındaki sağlıklı normal doku sınırı (salim cerrahi marjin) ile birlikte bir bütün halinde tamamen çıkarılmasıdır. Küçük kutanöz lezyonlarda (displastik nevüs, şüpheli melanom), küçük meme nodüllerinde ve büyümüş lenf nodu eksizyonlarında altın standarttır. Lezyonun hem kesin histopatolojik tanısını koydurur hem de cerrahi sınırları değerlendirerek primer tedavisini sağlar.
2) İnsizyonel Biyopsi: Çok büyük kitlelerden veya cerrahi olarak tamamen çıkarılması çevre dokulara masif hasar verecek lezyonlardan (örneğin uylukta dev bir retroperitoneal/derin yumuşak doku kitlesi) histopatolojik tanı koyabilmek amacıyla lezyonun en canlı ve temsili bölgesinden bir doku kamasının cerrahi olarak çıkarılmasıdır.
3) Kalın İğne (Tru-cut / Core Needle) Biyopsisi: Özel yaylı ve kesici bir iğne mekanizması (genellikle 14-18 gauge) kullanılarak solid organlardaki (meme, karaciğer, prostat, böbrek) şüpheli lezyonlardan doku silindirleri elde edilmesidir. Tru-cut biyopsinin ince iğne aspirasyonuna (İİAB) en büyük üstünlüğü, doku mimarisini (stroma-tümör ilişkisini) ve bazal membran bütünlüğünü korumasıdır. Bu sayede patolog karsinoma in situ ile invaziv karsinom ayrımını kesin olarak yapabilir ve parafin bloktan onlarca immünohistokimyasal/genetik test uygulayabilir.
4) Forseps ve Punch Biyopsileri: Endoskopik yöntemlerle gastrointestinal, bronşiyal mukozalardan veya cilt lezyonlarından forseps/punch aletiyle küçük doku parçaları alınmasıdır.

Doku Takibi ve Fiksasyonun Hayati Önemi:
Vücuttan çıkarılan bir biyopsi dokusunda hücreler hızla kendi lizozomal enzimleri tarafından sindirilmeye (otoliz) ve bakteriyel çürümeye başlar. Bu hücresel yıkımı durdurmak, enzim aktivitesini sonlandırmak, hücresel morfolojiyi dondurmak ve antijenik epitopları korumak amacıyla doku derhal fikse edilmelidir.
Standart Fiksatif: %10 Nötral Tamponlu Formalin (yaklaşık %3,7-4'lük formaldehit solüsyonu). Fiksatif hacmi, doku hacminin en az 10 ila 20 katı olmalıdır. Yetersiz fiksasyon veya aşırı gecikme; doku nekrozuna, nükleer kromatin detayının kaybına, immünohistokimyasal antijen maskelenmesine ve özellikle FISH/NGS gibi moleküler genetik testlerde DNA/RNA fragmentasyonuna neden olarak tanıyı imkansız kılar.""",
        "spots": [
            {
                "type": "warning",
                "badge": "🔴 ÖNEMLİ",
                "text": "Tru-cut (kalın iğne) biyopsisinin İİAB'ye temel üstünlüğü doku mimarisini ve stromayı korumasıdır; bu sayede duktal karsinoma in situ (DCIS) ile invaziv duktal karsinom ayrımı kesin olarak yapılabilir. Fiksasyonda altın standart %10 nötral tamponlu formalindir.",
                "color": "rose"
            },
            {
                "type": "exam",
                "badge": "🔵 ÇIKMIŞ SORU",
                "text": "Meme kitlesi bulunan bir hastada doku mimarisini koruyarak tümörün çevre stromaya invazyonunu ve immünohistokimyasal reseptör profilini güvenle değerlendirmek için tercih edilen biyopsi tekniği hangisidir? (Tru-cut / Kalın iğne biyopsisi).",
                "color": "sky"
            }
        ],
        "spotPearls": [
            "Eksizyonel biyopside lezyon salim sınırla tamamen çıkarılır; hem tanı hem tedavidir.",
            "Tru-cut biyopsi doku mimarisini korur ve in situ-invaziv ayrımını mümkün kılar.",
            "Doku fiksasyonunda %10 nötral tamponlu formalin kullanılır; doku hacminin 10-20 katı olmalıdır."
        ],
        "practiceQuestion": {
            "id": "prac-tumor-012",
            "question": "Histopatolojik biyopsi yöntemleri ve doku takibi ilkeleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
            "options": [
                "A) Eksizyonel biyopsi küçük şüpheli kitlelerin salim doku marjini ile tamamen çıkarılması olup hem tanı hem tedavi sağlar.",
                "B) Tru-cut (kalın iğne) biyopsisinin İİAB'ye temel üstünlüğü doku mimarisini koruyarak in situ-invaziv karsinom ayrımına olanak sağlamasıdır.",
                "C) Biyopsi dokusunun fiksasyonunda altın standart %10 nötral tamponlu formalindir ve doku hacminin en az 10-20 katı fiksatif kullanılmalıdır.",
                "D) Fiksasyonda gecikme olması doku morfolojisini etkilemez, yalnızca nükleer boyanmayı hafifçe artırarak tanıyı kolaylaştırır.",
                "E) İnsizyonel biyopsi çevre dokulara zarar vermeden çıkarılamayacak büyük kitlelerden temsili doku parçası almak için uygulanır."
            ],
            "correctAnswer": 3,
            "explanation": "D seçeneği yanlıştır çünkü fiksasyonda gecikme hücresel otolize, bakteriyel çürümeye, nükleer detay kaybına ve antijenlerin maskelenmesine yol açar; bu durum immünohistokimya ve FISH/NGS gibi moleküler genetik analizleri tamamen imkansız hale getirir. A, B, C ve E seçenekleri doğru biyopsi ve fiksasyon prensipleridir."
        },
        "relatedQuestions": [
            {
                "id": "prac-tumor-012",
                "question": "Histopatolojik biyopsi yöntemleri ve doku takibi ilkeleri ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                "options": [
                    "A) Eksizyonel biyopsi küçük şüpheli kitlelerin salim doku marjini ile tamamen çıkarılması olup hem tanı hem tedavi sağlar.",
                    "B) Tru-cut (kalın iğne) biyopsisinin İİAB'ye temel üstünlüğü doku mimarisini koruyarak in situ-invaziv karsinom ayrımına olanak sağlamasıdır.",
                    "C) Biyopsi dokusunun fiksasyonunda altın standart %10 nötral tamponlu formalindir ve doku hacminin en az 10-20 katı fiksatif kullanılmalıdır.",
                    "D) Fiksasyonda gecikme olması doku morfolojisini etkilemez, yalnızca nükleer boyanmayı hafifçe artırarak tanıyı kolaylaştırır.",
                    "E) İnsizyonel biyopsi çevre dokulara zarar vermeden çıkarılamayacak büyük kitlelerden temsili doku parçası almak için uygulanır."
                ],
                "correctAnswer": 3,
                "explanation": "D seçeneği yanlıştır çünkü fiksasyonda gecikme hücresel otolize, bakteriyel çürümeye, nükleer detay kaybına ve antijenlerin maskelenmesine yol açar; bu durum immünohistokimya ve FISH/NGS gibi moleküler genetik analizleri tamamen imkansız hale getirir. A, B, C ve E seçenekleri doğru biyopsi ve fiksasyon prensipleridir."
            }
        ]
    }
]
