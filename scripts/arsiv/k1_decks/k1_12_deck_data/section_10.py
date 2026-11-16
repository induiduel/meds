# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-12-s91",
        "title": "Anti-TNF Ajanlar ve Granülom Bütünlüğü: Tüberküloz Reaktivasyonu Riski",
        "content": "Tümör Nekroz Faktörü (TNF-α), granülomatöz enflamasyonda epiteloid histiositlerin ve dev hücrelerin bir arada tutulması, yani granülomun yapısal bütünlüğü için mutlak gereklidir:\n\n- **Anti-TNF Ajanlar:** İnfliksimab (kimerik monoklonal antikor), Adalimumab (tam insan monoklonal antikor) ve Etanersept (çözünür TNF reseptör füzyon proteini).\n- **Romatolojide Kullanım:** Romatoid artritte sinoviyal pannus gelişimini, kemik erozyonunu ve kıkırdak yıkımını dramatik biçimde durdururlar.\n- **Kritik Klinik Uyarı (Sınav Spotu):** Anti-TNF tedavi alan hastalarda önceden sessizce kireçlenmiş (kazeifiye) tüberküloz granülomları çözülür; hapsedilmiş basiller serbest kalarak **milier tüberküloz veya yaygın ekstrapulmoner tüberküloz reaktivasyonuna** yol açar. Bu nedenle tedaviye başlamadan önce mutlaka PPD deri testi veya IGRA (Quantiferon) testi yapılmalı, latent enfeksiyon varsa profilaktik izoniazid başlanmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "48 yaşında romatoid artrit tanılı hastaya anti-TNF biyolojik ajan (adalimumab) başlanması planlanmaktadır.",
                "Bu hastada tedaviye başlamadan önce granülom stabilitesinin bozulması riski nedeniyle mutlaka taranması ve profilaksi gerektiren enfeksiyon hangisidir?",
                [
                    {
                        "text": "Latent Tüberküloz enfeksiyonu taranmalı; PPD/IGRA pozitifse izoniazid profilaksisi verilmelidir.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! TNF granülom duvarını korur; blokajında kazeifiye tüberküloz odağı patlayarak dissemine basiler yayılım yapar."
                    },
                    {
                        "text": "Yalnızca idrar yolu enfeksiyonu taranmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: İdrar yolu enfeksiyonu granülomatöz bir risk değildir."
                    },
                    {
                        "text": "Hepatit A aşısı yapılıp doğrudan başlanmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Granülom çözülmesi riski mikobakteriyel enfeksiyonlarla (tüberküloz) doğrudan ilişkilidir."
                    }
                ]
            ),
            make_cloze(
                "Anti-TNF biyolojik tedaviler kazeifiye granülomların bütünlüğünü bozarak latent tüberküloz reaktivasyonuna yol açabileceğinden tedavi öncesi tarama şarttır.",
                "latent tüberküloz",
                "Akciğerde sessiz bekleyen mikobakteriyel enfeksiyon durumu"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-12-s92",
        "title": "İnterlökin-1 Blokajı ve Otoinflamatuar Periyodik Ateş Sendromları",
        "content": "İnterlökin-1 (IL-1), inflamazom kaskadının nihai ürünü olup otoinflamatuar hastalıklarda hedeflenen primer mediyatördür:\n\n- **Otoinflamatuar vs Otoimmün:** Otoimmün hastalıklarda otoantikorlar ve autoreaktif T/B lenfositler rol alırken, otoinflamatuar sendromlarda edinsel bağışıklık değil doğal bağışıklık (inflamazom ve nötrofiller) kontrolsüz çalışır.\n- **Ailesel Akdeniz Ateşi (FMF):** Pyrin gen (MEFV) mutasyonu sonucu inflamazom aşırı uyarılır; tekrarlayan serözit (peritonit, plörit) ve ateş atakları görülür. Kolşisin temel tedavidir; dirençli olgularda IL-1 blokajı hayat kurtarır.\n- **Kriyopirin İlişkili Sendromlar (CAPS):** NLRP3 mutasyonları sonucu aşırı IL-1β salınır.\n- **Anakinra:** Rekombinant insan IL-1 reseptör antagonistidir (IL-1Ra); IL-1'in reseptörüne bağlanmasını yarışmalı olarak bloke eder.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Otoinflamatuar vs Otoimmün Hastalık Mekanizması",
                "Otoinflamatuar Sendromlar (Ör. FMF, CAPS)",
                "Doğal bağışıklık, NLRP3 inflamazom ve aşırı IL-1 üretimi; otoantikor bulunmaz.",
                "Otoimmün Hastalıklar (Ör. SLE, Romatoid Artrit)",
                "Edinsel bağışıklık, otoantikorlar (ANA, RF) ve autoreaktif T lenfositleri hakimdir."
            ),
            make_quiz(
                "NLRP3 mutasyonuna bağlı kriyopirin ilişkili periyodik sendromlarda (CAPS) ve kolşisine dirençli FMF ataklarında kullanılan rekombinant IL-1 reseptör antagonisti biyolojik ajan hangisidir?",
                [
                    {"key": "A", "text": "Anakinra", "explanation": "A seçeneği DOĞRUDUR: Anakinra rekombinant insan IL-1 reseptör antagonistidir."},
                    {"key": "B", "text": "Etanersept", "explanation": "B seçeneği yanlıştır: TNF reseptör füzyon proteinidir."},
                    {"key": "C", "text": "Ekulizumab", "explanation": "C seçeneği yanlıştır: Anti-C5 kompleman antikorudur."},
                    {"key": "D", "text": "Rituksimab", "explanation": "D seçeneği yanlıştır: Anti-CD20 B-hücre antikorudur."},
                    {"key": "E", "text": "Omalizumab", "explanation": "E seçeneği yanlıştır: Anti-IgE antikorudur."}
                ],
                "A"
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-12-s93",
        "title": "IL-6 Reseptör Antagonisti Tosilizumab ve Dev Hücreli Arterit",
        "content": "İnterlökin-6 (IL-6), hem karaciğerden akut faz proteinlerinin sentezini yöneten hem de T-hücrelerinin Th17 yönünde farklılaşmasını tetikleyen merkezi bir sitokindir:\n\n- **Tosilizumab:** Hem çözünür hem de membrana bağlı IL-6 reseptörlerini (IL-6R) bloke eden hümanize bir monoklonal antikordur.\n- **Dev Hücreli (Temporal) Arterit:** Yaşlı bireylerde baş ağrısı, çene kladikasyosu, ani görme kaybı ve aşırı yüksek ESR/CRP ile seyreden vaskülittir. Yüksek doz steroidlerin yanı sıra tosilizumab bu hastalığın ilk onaylı biyolojik ajanıdır.\n- **Sitokin Fırtınası / CRS:** Yoğun bakım hastalarında hızla artan sistemik IL-6 düzeyini ve kılcal damar sızıntısını tosilizumab hızla gerileterek mortaliteyi düşürür.\n- **Laboratuvar Etkisi:** Tosilizumab verilen bir hastada CRP üretimi karaciğerde doğrudan kesildiği için CRP düzeyi sıfırlanabilir; bu durum enfeksiyon takibinde hekimi yanıltmamalıdır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Hem membranöz hem de çözünür IL-6 reseptörlerini bloke eden monoklonal antikor tosilizumab dev hücreli arterit ve sitokin salınım sendromu tedavisinde kullanılır.",
                "tosilizumab",
                "IL-6 reseptörünü bloke eden biyolojik ajan"
            ),
            make_recall(
                "Tosilizumab tedavisi alan bir hastada karaciğerdeki hepatosit uyarısı kesildiği için hangi akut faz reaktanı enfeksiyon olsa dahi yalancı olarak sıfıra yakın kalabilir?",
                "C-Reaktif Proteindir (CRP).",
                "Karaciğerden IL-6 ile sentezlenen majör akut faz proteini"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-12-s94",
        "title": "IL-17 ve IL-23 Aksı Blokajı: Psöriyazis ve Ankilozan Spondilit",
        "content": "Son yıllarda otoimmün ve enflamatuar deri-eklem hastalıklarında 'IL-23 / Th17 / IL-17' ekseninin başrol oynadığı anlaşılmıştır:\n\n1. **Aksın Mekanizması:** Dendritik hücrelerden salınan **IL-23**, naif T hücrelerini **Th17 lenfositlerine** dönüştürür. Th17 lenfositleri ise dokuya bol miktarda **IL-17 (özellikle IL-17A)** salgılar. IL-17 epitel hücrelerini uyararak yoğun kemokin ve antimikrobiyal peptit salgılatır, nötrofilleri çağırır.\n2. **Sekukinumab ve İksekizumab:** IL-17A'yı doğrudan nötralize eden monoklonal antikorlardır. Psöriyazis ve ankilozan spondilit tedavisinde olağanüstü yüksek etkinlik sağlarlar.\n3. **Ustekinumab:** IL-12 ve IL-23'ün ortak p40 alt ünitesini hedefleyen monoklonal antikordur.\n4. **Yan Etki Profili:** IL-17 mukozal fungal bağışıklıkta hayati olduğundan, bu ilaçları alanlarda **mukokutanöz Candida enfeksiyonları** riski belirgin artar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "IL-23 / IL-17 Enflamatuar Aksı ve Nötrofilik Hasar",
                [
                    "1. Dentritik Hücre Aktivasyonu: Antijen uyarısıyla dentritik hücreler bol miktarda IL-23 salgılar.",
                    "2. Th17 Farklılaşması: IL-23 naif CD4+ T hücrelerini Th17 lenfosit soyuna farklılaştırır.",
                    "3. IL-17 Üretimi: Th17 hücreleri dokularda güçlü bir pro-enflamatuar olan IL-17A salgılar.",
                    "4. Nötrofil İnfiltrasyonu: IL-17 epitelden CXCL8 salgılatarak nötrofilleri deriye ve entezislere yığar."
                ]
            ),
            make_quiz(
                "Psöriyazis ve ankilozan spondilit tedavisinde doğrudan IL-17A sitokinini nötralize eden ve yan etki olarak mukokutanöz Candida enfeksiyonu riskini artıran monoklonal antikor hangisidir?",
                [
                    {"key": "A", "text": "Sekukinumab", "explanation": "A seçeneği DOĞRUDUR: Sekukinumab seçici IL-17A inhibitörüdür."},
                    {"key": "B", "text": "İnfliksimab", "explanation": "B seçeneği yanlıştır: Anti-TNF ajandır."},
                    {"key": "C", "text": "Anakinra", "explanation": "C seçeneği yanlıştır: IL-1 reseptör antagonistidir."},
                    {"key": "D", "text": "Tosilizumab", "explanation": "D seçeneği yanlıştır: IL-6 reseptör antagonistidir."},
                    {"key": "E", "text": "Ekulizumab", "explanation": "E seçeneği yanlıştır: Anti-C5 antikorudur."}
                ],
                "A"
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-12-s95",
        "title": "Kompleman İnhibisyonu: Ekulizumab ve Terminal Yol Blokajı",
        "content": "Kompleman sisteminin kontrolsüz aktivasyonu hayatı tehdit eden nadir hematolojik ve nefrolojik tablolara yol açar:\n\n- **Ekulizumab:** Kompleman proteini **C5'e bağlanan** ve onun C5a ve C5b'ye bölünmesini engelleyen hümanize monoklonal antikordur. Böylece membran atak kompleksinin (MAC / C5b-9) oluşumu tamamen önlenir.\n- **Paroksismal Noktürnal Hemoglobinüri (PNH):** Eritrositlerde CD55/CD59 eksikliği nedeniyle gelişen intravasküler kompleman kaynaklı hemoliz ekulizumab ile durdurulur.\n- **Atipik Hemolitik Üremik Sendrom (aHUS):** Kompleman düzenleyici faktör H mutasyonlarında gelişen endotel hasarı ve mikrotrombozları önler.\n- **Kritik Yan Etki ve Uyarı:** MAC kompleksi kapsüllü bakterilere (özellikle **Neisseria meningitidis**) karşı en kritik savunma hattı olduğundan, ekulizumab alacak her hastaya tedavi öncesi mutlaka **Meningokok aşısı** yapılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Paroksismal noktürnal hemoglobinüri tanısıyla takip edilen hastaya C5 konvertaz bölünmesini durduran anti-C5 monoklonal antikor ekulizumab başlanacaktır.",
                "Ekulizumabın MAC kompleksini bloke etmesi nedeniyle bu hastaya tedavi öncesinde mutlak surette yapılması gereken aşı hangisidir?",
                [
                    {
                        "text": "Neisseria meningitidis (Meningokok) aşısı yapılmalıdır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! MAC (C5b-9) eksikliğinde Neisseria türlerine duyarlılık bin kat artar; meningokok aşısı zorunludur."
                    },
                    {
                        "text": "Kızamık-Kızamıkçık-Kabakulak aşısı yapılmalıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Viral kapsülsüz ajanlara karşı kompleman terminal yolu primer savunma değildir."
                    },
                    {
                        "text": "Hepatit B aşısı yeterlidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Hayatı tehdit eden menenjit riski nedeniyle Meningokok aşısı endikedir."
                    }
                ]
            ),
            make_cloze(
                "Anti-C5 monoklonal antikoru ekulizumab membran atak kompleksinin oluşmasını engelleyerek paroksismal noktürnal hemoglobinürideki hemolizi durdurur.",
                "ekulizumab",
                "C5'e bağlanan terminal kompleman inhibitörü monoklonal antikor"
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-12-s96",
        "title": "Astımda Hedefe Yönelik Tedaviler: Omalizumab, Mepolizumab ve Lökotrien Blokerleri",
        "content": "Bronşiyal astım, hava yollarında kimyasal mediyatörlerin orkestre ettiği kronik eozinofilik ve mast hücre kaynaklı bir enflamasyondur:\n\n1. **Lökotrien Reseptör Antagonistleri (Montelukast, Zafirlukast):** Düz kas CysLT1 reseptörlerini bloke eder; egzersiz ve aspirinle tetiklenen astımda ilk tercihlerdendir.\n2. **5-Lipoksijenaz İnhibitörü (Zileuton):** Lökotrien sentezini en baştan durdurur; hepatotoksik riski nedeniyle karaciğer enzimleri izlenir.\n3. **Omalizumab (Anti-IgE):** Serbest IgE'nin Fc bölgesine bağlanarak mast hücreleri ve bazofiller üzerindeki FcεRI reseptörlerine tutunmasını engeller. Ağır alerjik astımda kullanılır.\n4. **Mepolizumab ve Reslizumab (Anti-IL-5):** Eozinofillerin primer sağkalım ve aktivasyon sitokini olan IL-5'i nötralize ederek dirençli eozinofilik astımda eozinofil sayısını sıfıra indirir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İlaç Grubu / Adı", "Moleküler Hedef", "Klinik Endikasyon"],
                [
                    [
                        {"text": "Omalizumab", "isMasked": True, "hint": "Serbest IgE'yi bağlayan monoklonal antikor"},
                        {"text": "Serbest IgE molekülünün Fc bölgesi", "isMasked": False, "hint": ""},
                        {"text": "Ağır refrakter alerjik astım", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Mepolizumab", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-5 (IL-5)", "isMasked": True, "hint": "Eozinofil büyüme ve sağkalım sitokini"},
                        {"text": "Dirençli eozinofilik astım", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Montelukast", "isMasked": False, "hint": ""},
                        {"text": "Sisteinil lökotrien CysLT1 reseptörü", "isMasked": False, "hint": ""},
                        {"text": "Aspirin ve egzersizle tetiklenen astım", "isMasked": True, "hint": "Aspirin duyarlılığında hava yolu spazmı"}
                    ]
                ]
            ),
            make_recall(
                "Ağır eozinofilik astımda eozinofillerin kemik iliğinden çıkışını ve dokuda sağkalımını durdurmak için hedeflenen temel sitokin hangisidir?",
                "İnterlökin-5'tir (IL-5).",
                "Eozinofillerin en kritik büyüme faktörü"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-12-s97",
        "title": "Gut Artriti: Ürat Kristalleri, NLRP3 İnflamazomu ve IL-1β Patlaması",
        "content": "Akut gut artriti, kimyasal mediyatör kaskadının ve doğal bağışıklığın kristal uyarısıyla nasıl alevlendiğini gösteren en klasik modeldir:\n\n- **Monosodyum Ürat (MSU) Kristalleri:** Sinoviyal sıvıda çöken iğne şeklindeki MSU kristalleri eklem makrofajları tarafından fagositozla yutulur.\n- **Fagozom Yıkımı ve K+ Çıkışı:** Kristaller makrofaj fagozomunu deler; sitoplazmik potasyum iyonu dışarı sızar.\n- **NLRP3 İnflamazom Aktivasyonu:** Potasyum düşüşü NLRP3 inflamazom kompleksini toplar ve prokaspaz-1'i aktif kaspaz-1'e çevirir.\n- **Masif IL-1β Salgılanması:** Kaspaz-1 pro-IL-1β'yı parçalayarak ortama bolca aktif **IL-1β** salar.\n- **Klinik Tablo:** IL-1 sinovyum endotelinde E-selektin ve kemokin patlaması yapar; nötrofiller ekleme hücum eder. Başparmak metatarsofalangeal ekleminde (podagra) dakikalar içinde kızarıklık, şişlik ve dayanılmaz ağrı gelişir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Akut Gut Atağında Moleküler Mekanizma Zinciri",
                [
                    "1. Kristal Çökmesi: Sinoviyal sıvıda aşırı doymuş monosodyum ürat (MSU) kristalleri çöker.",
                    "2. Makrofaj Fagositozu: Eklem makrofajları kristalleri yutar ve fagozomal membran yırtılır.",
                    "3. İnflamazom Kurulumu: Sitoplazmik potasyum kaybı NLRP3 inflamazomunu aktive eder.",
                    "4. Kaspaz-1 ve IL-1beta: Kaspaz-1 pro-IL-1beta molekülünü aktif IL-1beta haline çevirip dokuya salar.",
                    "5. Nötrofil Akını ve Podagra: IL-1beta etkisiyle ekleme nötrofiller üşüşür ve şiddetli artrit oluşur."
                ]
            ),
            make_quiz(
                "Akut gut artritinde monosodyum ürat kristallerinin eklem makrofajlarında tetiklediği ve aktif IL-1β salınımına yol açan sitoplazmik multiprotein kompleksi hangisidir?",
                [
                    {"key": "A", "text": "NLRP3 İnflamazomu", "explanation": "A seçeneği DOĞRUDUR: MSU kristalleri NLRP3 inflamazomunu aktive ederek kaspaz-1 üzerinden IL-1beta üretir."},
                    {"key": "B", "text": "Membran Atak Kompleksi", "explanation": "B seçeneği yanlıştır: C5b-9 litik komplemandır."},
                    {"key": "C", "text": "Siklooksijenaz-2", "explanation": "C seçeneği yanlıştır: Eikozanoid sentez enzimidir."},
                    {"key": "D", "text": "Hageman Faktörü", "explanation": "D seçeneği yanlıştır: Faktör XII koagülasyon proteinidir."},
                    {"key": "E", "text": "Proteazom 26S", "explanation": "E seçeneği yanlıştır: Protein yıkım organelidir."}
                ],
                "A"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-12-s98",
        "title": "Aterosklerozda Kimyasal Mediyatörler: Kronik Endotel Hasarı",
        "content": "Ateroskleroz günümüzde basit bir lipid birikim hastalığı değil, arter intima tabakasında gelişen **kronik enflamatuar bir mediyatör hastalığı** olarak kabul edilmektedir:\n\n1. **Endotel Aktivasyonu:** Okside LDL (ox-LDL), hipertansiyon ve sigara endotelde VCAM-1, ICAM-1 ve MCP-1 (CCL2) ekspresyonunu uyarır.\n2. **Monosit Çağrısı ve Köpük Hücreleri:** MCP-1 monositleri intimaya çeker; burada makrofaja dönüşen hücreler scavenger reseptörleriyle ox-LDL'yi yutarak köpük hücrelerine (foam cells) dönüşür.\n3. **T-Hücreleri ve IFN-γ:** İntimadaki T lenfositleri IFN-γ salgılayarak makrofajları aktive eder ve kollajen sentezini baskılar.\n4. **Plak Rüptürü:** Aktif makrofajlar **Matriks Metalloproteinazlar (MMP)** salgılayarak fibröz şapkayı inceltir. Şapkanın yırtılmasıyla kolesterol çekirdeği kana temas eder; trombin ve PAF aktivasyonuyla akut koroner sendrom (miyokard enfarktüsü) tetiklenir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Stabil Plak vs İnflame Kararsız (Vulnerable) Plak",
                "Stabil Aterom Plağı",
                "Kalın fibröz şapka, zengin düz kas ve kollajen; düşük enflamatuar sitokin ve mediyatör düzeyi.",
                "Kararsız (Rüptüre Yatkın) Plak",
                "Yoğun makrofaj/T-hücre infiltrasyonu, yüksek MMP ve IFN-gama; ince fibröz şapka ve yüksek rüptür riski."
            ),
            make_cloze(
                "Ateroskleroz patogenezinde intimada yer alan makrofajların salgıladığı matriks metalloproteinazlar fibröz şapkayı eriterek plak rüptürüne ve tromboza zemin hazırlar.",
                "matriks metalloproteinazlar",
                "Kollajen ve ekstraselüler matriksi yıkan enzim ailesi"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-12-s99",
        "title": "Enflamasyon Farmakolojisi Entegrasyon Haritası ve Klinik İnciler",
        "content": "Kimyasal mediyatörlerin farmakolojik regülasyonu klinik tıpın temel taşlarından biridir. Bu harita klinikteki en kritik ilaç-hedef ilişkilerini özetler:\n\n- **Kortikosteroidler:** Lipokortin-1 indüksiyonu ile PLA2'yi inhibe eder; araşidonik asit açığa çıkamaz. COX-2 ve iNOS transkripsiyonunu NF-κB baskılamasıyla durdurur.\n- **Klasik NSAİİ'ler (Aspirin, İbuprofen, İndometazin):** COX-1 ve COX-2'yi geri dönüşümlü veya geri dönüşümsüz (aspirin) inhibe ederler.\n- **Koksibler (Selekoksib):** Seçici COX-2 inhibitörleridir; mideyi korurlar ancak TXA2/PGI2 dengesini bozarak kardiyovasküler tromboz riskini artırabilirler.\n- **Kromolin ve Nedokromil:** Mast hücre membranını stabilize ederek histamin degranülasyonunu engeller.\n- **Kolşisin:** Nötrofil mikrotübül polimerizasyonunu engelleyerek nötrofillerin dokuya göçünü ve fagositozunu durdurur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["İlaç Sınıfı", "Primer Enzim / Reseptör Hedefi", "Klinik Etki / Risk"],
                [
                    [
                        {"text": "Kortikosteroidler", "isMasked": False, "hint": ""},
                        {"text": "Fosfolipaz A2 (Lipokortin yolu) ve NF-κB", "isMasked": True, "hint": "En tepedeki membran lipazı baskısı"},
                        {"text": "Tüm lipid ve sitokin yolağının küntleşmesi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Aspirin", "isMasked": False, "hint": ""},
                        {"text": "COX-1 ve COX-2 kovalent asetilasyonu", "isMasked": True, "hint": "Geri dönüşümsüz kovalent enzim bağlanması"},
                        {"text": "Trombositte 7-10 gün TXA2 sentezinin durması", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kolşisin", "isMasked": True, "hint": "FMF ve gutta kullanılan tübülin zehiri"},
                        {"text": "Mikrotübül polimerizasyonu (Tübülün)", "isMasked": False, "hint": ""},
                        {"text": "Nötrofil kemotaksisi ve degranülasyon blokajı", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Aspirinin diğer tüm NSAİİ'lerden farklı olarak siklooksijenaz enzimlerini inhibe etme mekanizması nasıldır?",
                "Aktif bölgedeki serin rezidüsünü kovalent asetilleyerek geri dönüşümsüz (irreversibl) inaktivasyon yapmasıdır.",
                "Kovalent bağla geri dönüşümsüz bağlanma"
            )
        ]
    })

    # Slide 100
    slides.append({
        "id": "k1-12-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Enflamasyonun Kimyasal Mediyatörleri Bütüncül Özeti",
        "content": "Tebrikler! 100 slaytlık devasa Enflamasyonun Kimyasal Mediyatörleri destesini tamamladınız. Bu büyük finalde dersin omurgasını oluşturan tüm temel kavramları zihninizde birleştiriyoruz:\n\n- **Hücre Kaynaklılar:** Preforme histamin ve serotonin saniyeler içinde vazodilatasyon ve venüler permeabilite yapar. Eikozanoidler (PG, TXA2, LT) membran fosfolipidlerinden sentezlenir.\n- **Plazma Kaynaklılar:** Karaciğer kökenli kompleman kaskadı (C3a, C5a, MAC), kinin sistemi (bradikinin) ve pıhtılaşma/fibrinoliz sistemleri birbirine Hageman faktörü (Faktör XII) ve kallikrein ile kenetlenmiştir.\n- **Sitokin Ağı:** Akut fazda TNF, IL-1 ve IL-6 lökosit-endotel etkileşimini ve sistemik reaksiyonları yönetir. Kronik fazda IFN-γ makrofajları aktive eder, IL-17 nötrofilik yangıyı sürdürür.\n- **Sonlanma ve Tedavi:** Enflamasyon lipoksinler, rezolvinler, protektinler ve eferositoz ile aktif olarak çözülür. Bu moleküler ağın düğüm noktaları modern hedefe yönelik biyolojik tedavilerin ana hedefidir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Enflamasyon sürecinde arterioler vazodilatasyon, artmış venüler geçirgenlik, endotelyal yapışma moleküllerinin ekspresyonu, sistemik ateş ve nötrofil kemotaksisini aynı anda düzenleyen en merkezi pro-enflamatuar sitokin çifti hangisidir?",
                [
                    {"key": "A", "text": "Tümör Nekroz Faktörü (TNF) ve İnterlökin-1 (IL-1)", "explanation": "A seçeneği DOĞRUDUR: TNF ve IL-1 endotel aktivasyonundan ateşe kadar akut enflamasyonun baş mimarlarıdır."},
                    {"key": "B", "text": "İnterlökin-10 ve TGF-beta", "explanation": "B seçeneği yanlıştır: Anti-enflamatuar ve onarıcı sitokinlerdir."},
                    {"key": "C", "text": "İnterlökin-4 ve İnterlökin-5", "explanation": "C seçeneği yanlıştır: Alerjik ve paraziter Th2 yanıt sitokinleridir."},
                    {"key": "D", "text": "Serotonin ve Heparin", "explanation": "D seçeneği yanlıştır: Sitokin değillerdir."},
                    {"key": "E", "text": "Faktör XII ve Kallikrein", "explanation": "E seçeneği yanlıştır: Plazma enzimleridir."}
                ],
                "A"
            ),
            make_cloze(
                "Enflamasyonun hücresel ve plazma mediyatör kaskadlarının bütüncül anlaşılması romatolojiden onkolojiye uzanan hedefe yönelik biyolojik tedavilerin temelini oluşturur.",
                "biyolojik tedavilerin",
                "Monoklonal antikorlar ve reseptör füzyon proteinleri ailesi"
            )
        ]
    })

    return slides
