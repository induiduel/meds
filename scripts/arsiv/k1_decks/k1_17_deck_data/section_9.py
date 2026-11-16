# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-17-s81",
        "title": "Genital Herpes Etiyolojisi ve Epidemiyolojisi (HSV-1 vs HSV-2)",
        "content": "Genital herpes, dünya genelinde en sık rastlanan ülseratif cinsel yolla bulaşan enfeksiyondur (Sınav Spotu):\n\n- **Etken Virüsler:** Herpesviridae ailesinden çift iplikli, zarflı DNA virüsleri olan **Herpes Simpleks Virüs Tip 1 (HSV-1)** ve **Herpes Simpleks Virüs Tip 2 (HSV-2)**.\n- **HSV-1 vs HSV-2 Dağılımı:**\n  - Tarihsel ve klasik olarak genital lezyonların %70-80'inden **HSV-2** sorumludur.\n  - Ancak orogenital cinsel temas sıklığının artışıyla birlikte genç erişkinlerde ilk atak genital herpes olgularında **HSV-1** oranı belirgin şekilde artmaktadır.\n- **Bulaş Mekanizması:**\n  - Virüs taşıyan lezyonlarla, enfekte müköz membranlarla veya lezyon olmaksızın genital sekresyonlarla doğrudan yakın temas sonucu bulaşır.\n  - Bulaşmaların büyük çoğunluğu virüsü taşıdığını bilmeyen veya aktif yarası bulunmayan asemptomatik partnerlerden gerçekleşir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "HSV-2 vs HSV-1 Genital Dağılımı",
                "HSV-2 (Klasik Genital Etken)",
                "Genital herpesin en sık ve tipik etkenidir; tekrarlama sıklığı ve sakral ganglion nüksleri çok daha yüksektir.",
                "HSV-1 (Orogenital Artış)",
                "Geleneksel labial herpes etkenidir; günümüzde orogenital temasla genital ilk ataklarda sıklığı artmaktadır."
            ),
            make_quiz(
                "Genital herpes enfeksiyonlarının etiyolojisi ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                [
                    {"key": "A", "text": "Klasik etken HSV-2 olmakla birlikte, orogenital temasla genital HSV-1 sıklığı artmaktadır", "isCorrect": True, "explanation": "Doğru cevap A'dır: Genital herpesin geleneksel etkeni HSV-2'dir; ancak orogenital seks artışı nedeniyle ilk ataklarda HSV-1 oranı yükselmiştir."},
                    {"key": "B", "text": "Yalnızca aktif açık vezikülü olan hastalar virüsü bulaştırabilir", "isCorrect": False, "explanation": "Bulaşların çoğu subklinik asemptomatik viral saçılım sırasında gerçekleşir."},
                    {"key": "C", "text": "HSV tek iplikli bir RNA virüsüdür", "isCorrect": False, "explanation": "HSV çift iplikli zarflı bir DNA virüsüdür."},
                    {"key": "D", "text": "HSV-1 genital bölgeyi asla enfekte edemez", "isCorrect": False, "explanation": "Orogenital temas ile HSV-1 genital lezyonlara yol açabilir."}
                ]
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-17-s82",
        "title": "Genital Herpes Patogenezi: Latens ve Subklinik Viral Saçılım",
        "content": "Herpes virüslerinin en temel patogenetik özelliği yaşam boyu süren latentlik ve reaktivasyon döngüsüdür (Sınav Spotu):\n\n- **İnokülasyon ve Retrograd Taşınma:**\n  - Virüs mukozal epitelden veya derideki mikro çatlaklardan girerek keratinositlerde çoğalır.\n  - Duyu sinir uçlarına girer ve **retrograd aksonal transport** mekanizması ile dorsal kök ganglionlarına taşınır.\n  - Genital bölgeyi innerve eden **sakral duyusal ganglionlarda (S2-S4)** ömür boyu latent (sessiz) kalır.\n- **Reaktivasyon ve Anterograd Taşınma:**\n  - Fiziksel veya duygusal stres, ateşli hastalıklar, ultraviyole ışık, cerrahi travma veya immünsüpresyon durumunda latent virüs uyanır.\n  - Akson boyunca **anterograd transport** ile deriye/mukozaya geri dönerek çoğalır ve lezyonları tekrarlar.\n- **Subklinik Viral Saçılım:** Lezyon olmadığı dönemde dahi servikovajinal veya penil sıvılarda virüs replike olup çevreye yayılır; cinsel bulaşların %70'inden fazlası bu asemptomatik saçılım evresinde olur.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "HSV Enfeksiyonunda Latens ve Reaktivasyon Basamakları",
                [
                    "1. Mukozal Çoğalma: Virüs genital epitele girer ve lokal olarak replike olur.",
                    "2. Retrograd Aksonal Göç: Duyu nöronlarının aksonlarıyla sakral ganglionlara (S2-S4) taşınır.",
                    "3. Gangliyonik Latens: Virüs DNA'sı ganglion nöronlarında ömür boyu sessizce bekler.",
                    "4. Reaktivasyon ve Saçılım: Tetikleyici faktörlerle anterograd olarak cilde döner ve saçılır."
                ]
            ),
            make_cloze(
                "Genital herpes virüsü primer enfeksiyondan sonra retrograd yolla ilerleyerek sakral ganglionlarda ömür boyu latent kalır.",
                "sakral ganglionlarda",
                "HSV-2'nin sessizce yerleştiği S2-S4 duyu gangliyon bölgesi"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-17-s83",
        "title": "Genital Herpes Klinik Tablosu: Primer Atak vs Rekürren Atak",
        "content": "Genital herpes kliniği, hastanın virüsle ilk kez mi karşılaştığına yoksa daha önce antikor geliştirip geliştirmediğine göre dramatik farklılık gösterir (Sınav Spotu):\n\n- **1. Primer Atak (İlk Klinik Epizot):**\n  - **Çok Şiddetlidir:** 2-12 günlük kuluçkadan sonra başlar.\n  - Eritematöz ödemli zemin üzerinde grup yapmış, berrak sıvı dolu küçük **veziküller** belirir.\n  - Veziküller 24-48 saatte patlayarak çoklu, birleşme eğiliminde, son derece **ağrılı, sığ ülserler** oluşturur.\n  - **Sistemik Bulgular:** Hastaların %70'inde ateş, baş ağrısı, miyalji, halsizlik ve bilateral ağrılı inguinal LAP bulunur; aseptik menenjit ve üriner retansiyon gelişebilir.\n  - Lezyonların kabuklanıp iyileşmesi **2 ila 3 hafta** sürer.\n- **2. Rekürren Atak (Tekrarlayan Epizot):**\n  - Lezyon çıkmadan saatler önce bölgede yanma, karıncalanma, batma (**prodromal parestezi**) hissedilir.\n  - Lezyonlar çok daha az sayıda, tek taraflı ve sınırlıdır; sistemik bulgular görülmez.\n  - Lezyonlar **7 ila 10 gün** içinde iz bırakmadan hızla iyileşir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Özellik", "Primer (İlk) Atak", "Rekürren (Tekrarlayan) Atak"],
                [
                    ["Sistemik Bulgular (Ateş/Miyalji)", "Sıktır (%70), şiddetli seyreder", "Yoktur veya son derece hafiftir"],
                    ["Lezyon Yaygınlığı", "Bilateral, çok sayıda vezikül ve ülser", "Unilateral, lokalize, az sayıda lezyon"],
                    ["Prodrom Belirtisi", "Genellikle yoktur", "Tipiktir (karıncalanma, yanma, nöropatik sızı)"],
                    ["İyileşme Süresi", "14-21 gün (uzun ve ağrılı)", "7-10 gün (kısa)"]
                ]
            ),
            make_quiz(
                "Genital herpesin primer atağı ile rekürren atağı karşılaştırıldığında aşağıdakilerden hangisi rekürren atağın karakteristik bir özelliğidir?",
                [
                    {"key": "A", "text": "Lezyon çıkmadan önce lokal yanma ve karıncalanma şeklinde prodromal semptomların varlığı", "isCorrect": True, "explanation": "Doğru cevap A'dır: Nöronal reaktivasyon nedeniyle lezyon öncesi prodromal parestezi rekürren atakların tipik özelliğidir."},
                    {"key": "B", "text": "Yüksek ateş ve aseptik menenjitin eşlik etmesi", "isCorrect": False, "explanation": "Sistemik bulgular primer atağın özelliğidir."},
                    {"key": "C", "text": "Lezyonların iyileşmesinin bir aydan uzun sürmesi", "isCorrect": False, "explanation": "Rekürren ataklar 7-10 günde hızla iyileşir."},
                    {"key": "D", "text": "Bilateral masif süpüratif bubon oluşumu", "isCorrect": False, "explanation": "Herpes bubo yapmaz; bubon şankroid ve LGV'de görülür."}
                ]
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-17-s84",
        "title": "Genital Herpes Tanısı: NAAT, Tzanck Yayması ve Seroloji",
        "content": "Genital herpes tanısında lezyonların vezikülo-ülseratif görünümü klinik şüphe uyandırsa da laboratuvar teyidi şarttır (Sınav Spotu):\n\n- **1. NAAT (Nükleik Asit Amplifikasyon Testi / PCR) - Altın Standart:**\n  - Genital lezyondan alınan sürüntüde viral DNA'yı saptar.\n  - Viral kültüre göre duyarlılığı 3-5 kat daha yüksektir; günümüzde tüm uluslararası kılavuzlarda **birinci tercih tanı yöntemidir**.\n  - HSV-1 ve HSV-2 tip ayrımını kesin olarak yapar.\n- **2. Tzanck Sitolojik Yayması:**\n  - Taze vezikül tabanı kazınarak Giemsa veya Wright ile boyanır.\n  - Mikroskopta **multinükleer dev hücreler** ve **intranükleer eozinofilik Cowdry A inklüzyon cisimcikleri** görülür.\n  - Hızlı ve ucuzdur; ancak duyarlılığı düşüktür ve HSV-1, HSV-2 veya VZV ayrımı yapamaz.\n- **3. Tip-Spesifik Seroloji:**\n  - Viral glikoprotein G (gG1 ve gG2) antikorlarını araştırır. Atipik seyirli, tekrarlayan veya asemptomatik partner değerlendirmesinde kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "NAAT (PCR) vs Tzanck Yayması Tanısal Değeri",
                "NAAT (PCR - Altın Standart)",
                "En yüksek duyarlılık ve özgüllüğe sahiptir; HSV-1 ve HSV-2 tip ayrımını kesinleştirir.",
                "Tzanck Yayması (Hızlı Sitoloji)",
                "Multinükleer dev hücreleri gösterir; pratik ve ucuzdur ancak tipler arasında ayrım yapamaz."
            ),
            make_cloze(
                "Taze vezikül tabanından hazırlanan Tzanck yaymasında multinükleer dev hücreler ve intranükleer Cowdry A inklüzyonları görülür.",
                "multinükleer dev hücreler",
                "Herpesvirüs sitopatik etkisiyle kaynaşan keratinositlerin oluşturduğu dev hücresel yapı"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-17-s85",
        "title": "Genital Herpes Tedavi Rejimleri: Asiklovir, Valasiklovir, Famsiklovir",
        "content": "Genital herpesin farmakoterapisinde nükleozid analoğu antiviral ajanlar kullanılır (Sınav Spotu):\n\n- **Etki Mekanizması:**\n  - Bu ilaçlar viral **timidin kinaz** enzimi tarafından monofosfata çevrilir; ardından hücresel kinazlarla trifosfat formuna aktiflenir.\n  - Aktif form viral **DNA polimeraz** enzimini kompetitif olarak inhibe eder ve viral replikasyonu durdurur.\n- **İlk Klinik Atak (Primer Enfeksiyon) Tedavi Protokolü (7-10 Gün):**\n  - **Asiklovir:** 3 $\\times$ 400 mg oral VEYA 5 $\\times$ 200 mg oral, 7-10 gün.\n  - **Valasiklovir:** 2 $\\times$ 1000 mg oral, 7-10 gün (asiklovirin L-valil esteridir, oral biyoyararlanımı 3-5 kat yüksektir, kullanım kolaylığı sağlar).\n  - **Famsiklovir:** 3 $\\times$ 250 mg oral, 7-10 gün (pensiklovir ön ilacıdır).\n- **Önemli Farmakolojik İlke:** Antiviraller lezyonların iyileşme süresini kısaltır, ağrıyı ve viral saçılımı azaltır; **ancak latent gangliyonik virüsü yok edemez (kür sağlamaz)**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["İlaç", "İlk Atak Dozu (7-10 Gün)", "Farmakokinetik Avantaj"],
                [
                    ["Asiklovir", "3x400 mg veya 5x200 mg oral", "Klasik ajan; günde 5 kez alma zorunluluğu uyumu zorlaştırabilir"],
                    ["Valasiklovir", "2x1000 mg oral", "Günde 2 kez kullanılır; yüksek biyoyararlanımlı ön ilaçtır"],
                    ["Famsiklovir", "3x250 mg oral", "Pensiklovirin ön ilacı; intraselüler yarı ömrü uzundur"]
                ]
            ),
            make_quiz(
                "Asiklovirin etki mekanizmasında ilacın ilk fosforilasyon basamağını gerçekleştirerek aktive olmasını sağlayan enzim hangisidir?",
                [
                    {"key": "A", "text": "Viral timidin kinaz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Asiklovir seçici olarak virüsün kodladığı viral timidin kinaz enzimi ile monofosfat haline çevrilir, bu sayede yalnızca enfekte hücrelerde aktive olur."},
                    {"key": "B", "text": "Hücresel RNA polimeraz", "isCorrect": False, "explanation": "RNA sentez enzimidir."},
                    {"key": "C", "text": "Bakteriyel dihidrofolat redüktaz", "isCorrect": False, "explanation": "Trimetoprimin hedefidir."},
                    {"key": "D", "text": "Viral nöraminidaz", "isCorrect": False, "explanation": "İnfluenza virüs yüzey enzimidir."}
                ]
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-17-s86",
        "title": "Rekürren Atak Yönetimi ve Kronik Süpresif Tedavi",
        "content": "Tekrarlayan herpes ataklarında iki farklı tedavi stratejisi uygulanır (Sınav Spotu):\n\n- **1. Epizodik Tedavi (Atak Sırasında Kısa Süreli Tedavi):**\n  - Hasta prodromal paresteziyi (karıncalanma, sızı) hissettiği anda veya ilk lezyon çıktığı ilk 24 saat içinde başlatılmalıdır.\n  - **Valasiklovir:** 2 $\\times$ 500 mg oral, 3 gün VEYA 2 $\\times$ 1000 mg, 1 gün.\n  - **Asiklovir:** 3 $\\times$ 400 mg oral, 5 gün VEYA 2 $\\times$ 800 mg, 5 gün.\n- **2. Kronik Günlük Süpresif Tedavi:**\n  - **Endikasyonları:** Yılda $\\ge 6$ kez atak geçiren sık rekürrensli hastalar, ağır psikoseksüel sıkıntı yaşayanlar veya duyarlı eşe bulaşı önlemek isteyenler.\n  - **Rejim:** **Valasiklovir 1 $\\times$ 500 mg veya 1 $\\times$ 1000 mg/gün** kesintisiz oral VEYA Asiklovir 2 $\\times$ 400 mg/gün.\n  - **Yararları:** Yıllık atak sayısını %70-80 oranında azaltır; subklinik viral saçılımı baskılar ve heteroseksüel partnerlere bulaş riskini yaklaşık %50 oranında düşürür.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Genital Herpes Süpresif Tedavi Karar Aşamaları",
                [
                    "1. Atak Sıklığı Tespiti: Hastanın yılda 6 veya daha fazla klinik atak geçirip geçirmediği sorgulanır.",
                    "2. Partner Riskinin Değerlendirilmesi: Eşin seronegatif olup olmadığı ve bulaş kaygısı belirlenir.",
                    "3. Günlük Süpresyon Başlanması: Valasiklovir 500-1000 mg/gün sürekli oral rejim verilir.",
                    "4. Yıllık Yeniden Değerlendirme: 1 yıllık süpresyon sonrası ilaç kesilerek atak sıklığı tekrar gözlenir."
                ]
            ),
            make_cloze(
                "Yılda altı veya daha fazla genital herpes atağı geçiren hastalarda atak sıklığını ve partnere bulaş riskini azaltmak için kronik günlük süpresif tedavi uygulanır.",
                "günlük süpresif tedavi",
                "Sık tekrarlayan epizotları önlemek için kesintisiz antiviral kullanımı"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-17-s87",
        "title": "Anogenital Siğiller (Kondiloma Akuminata): HPV Tip 6 ve 11",
        "content": "Kondiloma akuminata, anogenital bölgenin en yaygın benign proliferatif viral enfeksiyonudur (Sınav Spotu):\n\n- **Etken Patojen:** **Human Papillomavirus (HPV)** adı verilen, zarfsız çift iplikli bir DNA virüsüdür.\n- **Onkojenik Risk Sınıflaması:**\n  - **Düşük Riskli Tipler (HPV 6 ve 11):** Anogenital siğillerin (kondilomların) %90'ından fazlasından sorumludur; maligniteye dönüşüm potansiyelleri yok denecek kadar düşüktür.\n  - **Yüksek Riskli Tipler (HPV 16 ve 18):** Genital siğil yapmazlar; serviks, anüs, penis ve orofarenks kanserlerinin başlıca etkenidirler.\n- **Morfolojik Özellikler:**\n  - Yumuşak, et renginde veya pembe-beyaz, eksofitik, parmaksı çıkıntıları olan **karnabahar görünümünde (verrüköz)** lezyonlardır.\n  - Tek veya birleşerek geniş plaklar oluşturabilirler.\n  - **Tamamen ağrısızdırlar** (en belirgin klinik özellik); zaman zaman kaşıntı, nem hissi veya sürtünmeyle kanamaya neden olabilirler.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "HPV 6/11 (Kondilom) vs HPV 16/18 (Kanser)",
                "Düşük Riskli Tipler (HPV 6 ve 11)",
                "Anogenital bölgede ağrısız karnabahar benzeri kondiloma akuminata siğillerini oluşturur.",
                "Yüksek Riskli Tipler (HPV 16 ve 18)",
                "Görünür siğil yapmaz; serviks, anüs ve orofarenks displazisi ve skuamöz karsinomuna yol açar."
            ),
            make_quiz(
                "Anogenital bölgede gelişen karnabahar görünümündeki ağrısız kondiloma akuminata lezyonlarının en sık etkeni olan HPV tipleri hangileridir?",
                [
                    {"key": "A", "text": "HPV tip 6 ve HPV tip 11", "isCorrect": True, "explanation": "Doğru cevap A'dır: Benign anogenital siğillerin %90'ından düşük riskli HPV tip 6 ve 11 sorumludur."},
                    {"key": "B", "text": "HPV tip 16 ve HPV tip 18", "isCorrect": False, "explanation": "HPV 16 ve 18 yüksek riskli onkojenik tiplerdir, serviks kanseri yapar."},
                    {"key": "C", "text": "HPV tip 1 ve HPV tip 2", "isCorrect": False, "explanation": "El ve ayak tabanı siğillerini (verruca vulgaris) yapar."},
                    {"key": "D", "text": "HPV tip 31 ve HPV tip 33", "isCorrect": False, "explanation": "Yüksek riskli displazi tipleridir."}
                ]
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-17-s88",
        "title": "Anogenital Siğil Tedavisi: Hasta ve Hekim Tarafından Uygulanan Yöntemler",
        "content": "Kondiloma akuminata tedavisinde temel amaç görünür siğilleri ortadan kaldırmaktır; viral DNA'yı tamamen temizleyen bir kür yoktur (Sınav Spotu):\n\n- **1. Hasta Tarafından Uygulanan Topikal Tedaviler:**\n  - **İmikimod %5 Krem:** İmmün yanıt modülatörüdür; Toll benzeri reseptör 7'yi (TLR-7) uyararak interferon-alfa ve proinflamatuar sitokin salgılatır. Haftada 3 gece uygulanır.\n  - **Podofilotoksin %0.5 Çözelti/Jel:** Mikrotübüllere bağlanarak mitotik iğ iplikçiklerini bozar ve hücre bölünmesini durdurur. **Gebelikte kesinlikle kontrendikedir (teratojeniktir)**.\n  - **Sinekaşinler %15 Merhem:** Yeşil çay polifenol ekstresi antioksidan merhem.\n- **2. Hekim Tarafından Uygulanan Tedaviler:**\n  - **Kriyoterapi (Sıvı Azot):** Termal nekrozla siğili döker; **gebelikte tamamen güvenlidir**.\n  - **Triklorasetik Asit (TCA %80-90):** Keratolitik protein koagülasyonu yapar; **gebelikte tamamen güvenlidir**.\n  - **Cerrahi Eksizyon, Küretaj veya Elektrokoter:** Büyük veya obstrüktif siğillerde tek seansta tam temizleme sağlar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Yöntem", "Uygulayıcı", "Etki Mekanizması", "Gebelikte Güvenlilik"],
                [
                    ["İmikimod %5", "Hasta (topikal)", "TLR-7 aktivasyonu ve interferon uyarımı", "Önerilmez / Yeterli veri yok"],
                    ["Podofilotoksin", "Hasta (topikal)", "Mikrotübül inhibisyonu (antimitotik)", "KESİNLİKLE KONTRENDİKE (Teratojen)"],
                    ["Kriyoterapi", "Hekim (sıvı azot)", "Donma ve termal hücre nekrozu", "Tamamen güvenli"],
                    ["TCA (%80-90)", "Hekim (kimyasal)", "Protein koagülasyonu ve koterizasyon", "Tamamen güvenli"]
                ]
            ),
            make_quiz(
                "Anogenital siğil tedavisinde mitoz bölünmeyi durduran ancak sistemik emilimle fetal toksisite ve teratojenite oluşturduğu için gebelerde KESİNLİKLE KONTRENDİKE olan topikal ajan hangisidir?",
                [
                    {"key": "A", "text": "Podofilotoksin", "isCorrect": True, "explanation": "Doğru cevap A'dır: Podofilotoksin mikrotübül zehiridir; embriyotoksik ve teratojenik olduğundan gebelerde kesinlikle yasaktır."},
                    {"key": "B", "text": "Kriyoterapi", "isCorrect": False, "explanation": "Sıvı azot gebelikte son derece güvenlidir."},
                    {"key": "C", "text": "Triklorasetik asit (TCA)", "isCorrect": False, "explanation": "TCA lokal protein yıkar, gebelikte güvenlidir."},
                    {"key": "D", "text": "Asiklovir", "isCorrect": False, "explanation": "Herpes ilacıdır, siğilde kullanılmaz."}
                ]
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-17-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Viral CYBE: Genital Herpes ve HPV Yönetimi",
        "content": "Bu checkpointte genital herpes ve anogenital siğillerin temel ilkelerini özetliyoruz:\n\n- **HSV-1 vs HSV-2:** Klasik etken HSV-2'dir; orogenital seksle genital HSV-1 sıklığı artmaktadır. Sakral gangliyonlarda (S2-S4) latent kalır. Subklinik saçılımla lezyonsuzken de bulaşır.\n- **Herpes Kliniği:** Eritematöz zeminde grupe veziküller $\\to$ çoklu ağrılı sığ ülserler. Primer atakta ateş, baş ağrısı, bilateral LAP; rekürren atakta prodromal karıncalanma ön plandadır.\n- **Herpes Tanı ve Tedavisi:** Altın standart NAAT (PCR). Tzanck'ta multinükleer dev hücreler. Tedavide Asiklovir, Valasiklovir veya Famsiklovir kullanılır; kür sağlamaz. Yılda $\\ge 6$ atakta kronik günlük süpresyon uygulanır.\n- **Kondiloma Akuminata:** HPV 6 ve 11; karnabahar görünümünde ağrısız verrüköz lezyonlar. Podofilotoksin gebede yasaktır; gebede Kriyoterapi ve TCA tercih edilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Viral Enfeksiyon", "Temel Etken Tipleri", "Karakteristik Lezyon", "Birinci Tercih Tedavi"],
                [
                    ["Genital Herpes", "HSV-2 (ve HSV-1)", "Grupe veziküller ve aşırı ağrılı sığ ülserler", "Valasiklovir / Asiklovir / Famsiklovir"],
                    ["Anogenital Siğil", "HPV 6 ve 11", "Karnabahar görünümünde, yumuşak, tamamen ağrısız", "İmikimod, Podofilotoksin, Kriyoterapi, TCA"]
                ]
            ),
            make_chain(
                "Viral CYBE Karar Algoritması",
                [
                    "1. Morfolojik Ayrım: Ağrılı vezikülo-ülser ise HSV; ağrısız karnabahar kitle ise HPV.",
                    "2. HSV Doğrulama: NAAT PCR ile etken ve tip doğrulanır.",
                    "3. Antiviral Tedavi: İlk atakta Valasiklovir 2x1000 mg 7-10 gün başlanır.",
                    "4. HPV Tedavi Seçimi: Gebe ise Kriyoterapi/TCA; gebe değilse İmikimod veya cerrahi."
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-17-s90",
        "title": "Bölüm Özeti: Viral CYBE'den Partner ve Gebe Yönetimine Geçiş",
        "content": "Bölüm 9 boyunca en sık görülen iki viral CYBE olan genital herpes ve kondiloma akuminatanın patogenezini, klinik sunumlarını ve tedavi protokollerini inceledik:\n\n- **Özet:** Herpes latent kalır ve nükleozid analoglarıyla kontrol altına alınır; HPV siğilleri benign tiplerle (6 ve 11) oluşur ve fiziksel/kimyasal ablasyonla temizlenir.\n- **Sonraki Bölüm (Bölüm 10):** Son bölümümüzde CYBE yönetiminin en hayati basamakları olan **cinsel partner tedavisi ('ping-pong' etkisinin önlenmesi), 7 gün cinsel perhiz kuralı, gebelikte ilaç güvenliliği ve kontrendikasyonları, yenidoğan oftalmiya profilaksisi ve klinik entegrasyonu** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Genital herpes virüsünün primer enfeksiyondan sonra ömür boyu latent kaldığı anatomik duyu gangliyon bölgesi neresidir?",
                "Sakral ganglionlar (S2-S4 duyu gangliyonları)",
                "Sakral dorsal kök gangliyon nöronları"
            ),
            make_quiz(
                "Anogenital siğil (kondiloma akuminata) lezyonlarının hastaya dokunulduğunda ağrı vermemesi ile şankroid ve herpes lezyonlarının şiddetli ağrılı olması arasındaki temel klinik fark neyi yansıtır?",
                [
                    {"key": "A", "text": "HPV'nin epidermis/mukoza epitelinde proliferasyon yapması ve akut nekrotik enflamasyon yapmaması", "isCorrect": True, "explanation": "Doğru cevap A'dır: HPV epitel hücre hiperplazisi yapar, belirgin akut doku hasarı ve serbest sinir ucu uyarımı yapmadığı için ağrısızdır."},
                    {"key": "B", "text": "HPV'nin sinir uçlarını tamamen kesip felç etmesi", "isCorrect": False, "explanation": "Böyle bir etki yoktur."},
                    {"key": "C", "text": "Herpesin yalnızca kemik iliğini enfekte etmesi", "isCorrect": False, "explanation": "Herpes nörotrofiktir, kemik iliğini hedeflemez."},
                    {"key": "D", "text": "Kondilomun her zaman habis bir karsinom olması", "isCorrect": False, "explanation": "Kondilom benign bir siğildir."}
                ]
            )
        ]
    })

    return slides
