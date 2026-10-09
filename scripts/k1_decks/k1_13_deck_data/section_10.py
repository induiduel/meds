# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-13-s91",
        "title": "Kronik Enflamasyon Tedavisinde Temel Stratejiler",
        "content": "Kronik enflamatuar ve granülomatöz hastalıkların tedavisinde hekimin izlemesi gereken iki temel prensip vardır:\n\n1. **Etiyolojik Eliminasyon (Patojenin Temizlenmesi):** Eğer neden enfeksiyöz bir patojen ise (tüberküloz, sifiliz, mantar), öncelik patojeni uygun antibiyotik/antifungallerle tamamen öldürmektir (ör. tüberkülozda 4'lü rejim: İzoniazid, Rifampisin, Pirazinamid, Etambutol). Bu grupta tek başına immünsüpresyon vermek ölümcül bir sepsis ve dissemine basiler yayılıma yol açar!\n2. **İmmün Baskılama ve Doku Koruması:** Eğer neden otoimmün veya steril immün aracılı bir tablo ise (romatoid artrit, sarkoidoz, Crohn), hedef konak yangı yanıtını kontrol altına alarak masum çevre doku hasarını ve fibrogenezisi durdurmaktır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Enfeksiyöz vs Otoimmün Kronik Yangı Tedavisi",
                "Enfeksiyöz Yangı (Ör. Tüberküloz)",
                "Öncelik basili öldürmektir; tek başına immünsüpresif vermek basili serbest bırakıp öldürür.",
                "Otoimmün Yangı (Ör. Romatoid Artrit, Sarkoidoz)",
                "Ortadan kaldırılamayan antijen uyarısını steroid ve biyolojik ajanlarla baskılamak esastır."
            ),
            make_cloze(
                "Enfeksiyöz granülomatöz hastalıklarda ilk ve en kritik tedavi basamağı etken mikroorganizmanın antimikrobiyal ajanlarla eradike edilmesidir.",
                "antimikrobiyal",
                "Mikropları öldüren ilaç sınıfı"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-13-s92",
        "title": "Kortikosteroidlerin Moleküler Etkisi ve Yangı Baskılanması",
        "content": "Glukokortikoidler (prednizolon, deksametazon), kronik enflamasyon ve granülom tedavisinde en yaygın kullanılan birinci basamak anti-enflamatuar ajanlardır:\n\n- **Genomik Mekanizma:** Sitoplazmik glukokortikoid reseptörüne (GR) bağlanarak çekirdeğe girerler.\n- **Transkripsiyonel Baskılama (Transrepresyon):** Baş pro-enflamatuar transkripsiyon faktörleri olan **NF-κB** ve **AP-1**'i doğrudan bloke ederler; böylece TNF-α, IL-1, IL-6, IL-12, iNOS ve COX-2 gen ekspresyonu tamamen susar.\n- **Hücresel Etkiler:**\n  - Dolaşımdaki lenfosit, monosit ve eozinofil sayısını hızla düşürürler (dokuya çıkışlarını engeller ve apoptozlarını uyarırlar).\n  - Makrofajların antijen sunma (MHC II) ve fagositoz kapasitesini köreltirler.\n  - Fibroblast proliferasyonunu ve kollajen sentezini baskılarlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kortikosteroidlerin Anti-Enflamatuar Moleküler Zinciri",
                [
                    "1. Hücreye Giriş: Lipofilik steroid molekülü plazma zarından serbestçe sitoplazmaya sızar.",
                    "2. Reseptör Bağlanması: Glukokortikoid reseptörüne (GR) bağlanıp şaperon proteinlerinden ayrılır.",
                    "3. Çekirdeğe Translokasyon: Aktif steroid-GR kompleksi çekirdeğe geçerek DNA'ya tutunur.",
                    "4. NF-κB İnhibisyonu: NF-κB baskılanarak sitokin, kemokin ve eikozanoid sentezi durdurulur."
                ]
            ),
            make_quiz(
                "Kortikosteroidlerin sitoplazmik reseptörlerine bağlanarak çekirdeğe geçtiğinde baskıladığı ve pro-enflamatuar sitokin sentezini durduran ana transkripsiyon faktörü hangisidir?",
                [
                    {"key": "A", "text": "NF-κB (Nükleer Faktör Kappa B)", "explanation": "A seçeneği DOĞRUDUR: Steroidler NF-κB'yi transrepresyonla bloke ederek yangı genlerini kapatır."},
                    {"key": "B", "text": "HIF-1α", "explanation": "B seçeneği yanlıştır: Hipoksi faktörüdür."},
                    {"key": "C", "text": "Smad2/3", "explanation": "C seçeneği yanlıştır: TGF-beta yolağı proteinleridir."},
                    {"key": "D", "text": "Kaspaz-9", "explanation": "D seçeneği yanlıştır: İntrensek apoptoz proteazıdır."},
                    {"key": "E", "text": "Telomeraz", "explanation": "E seçeneği yanlıştır: Kromozom ucu uzatan enzimdir."}
                ],
                "A"
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-13-s93",
        "title": "Anti-TNF Biyolojikler ve Granülom Yıkımı: İki Ucu Keskin Kılıç",
        "content": "Romatoid artrit, Crohn hastalığı ve ankilozan spondilit tedavisinde Tümör Nekroz Faktörü (TNF-α) blokerleri (infliksimab, adalimumab, etanersept) olağanüstü başarı sağlamıştır:\n\n- **Terapötik Yarar:** TNF-α nötralize edildiğinde sinovyumdaki pannus erir, kıkırdak ve kemik erozyonu durur; bağırsak mukozasındaki transmural yangı geriler.\n- **Kritik Risk (Granülomun Çözülmesi - Sınav Spotu):**\n  - TNF-α, granülomun epiteloid histiositlerini bir arada tutan ve etkeni izole eden 'biyolojik çimento'dur.\n  - Anti-TNF ilaçlar verildiğinde vücutta sessizce bekleyen kazeifiye tüberküloz granülomları **parçalanır ve çözülür**.\n  - Hapsedilmiş canlı basiller sistemik dolaşıma dökülerek **milier tüberküloz, menenjit tüberküloz ve yaygın ölümcül sepsise** yol açar!\n- **Klinik Zorunluluk:** Anti-TNF başlanacak HER HASTAYA tedavi öncesi mutlaka PPD/Quantiferon testi yapılmalı ve akciğer grafisi çekilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "36 yaşında kadın hastaya şiddetli Crohn hastalığı nedeniyle anti-TNF monoklonal antikor (infliksimab) tedavisi planlanıyor.",
                "Bu hastada TNF-alfa blokajının granülom mimarisini çözmesi sonucu gelişebilecek en tehlikeli ölümcül enfeksiyöz komplikasyon hangisidir?",
                [
                    {
                        "text": "Latent Tüberküloz enfeksiyonunun reaktivasyonu ve milier yayılımıdır.",
                        "isCorrect": True,
                        "feedback": "Tebrikler! TNF granülom duvarının harcıdır; blokajında kazeöz granülom çözülür ve basil kana saçılır."
                    },
                    {
                        "text": "Akut apandisit perforasyonudur.",
                        "isCorrect": False,
                        "feedback": "Yanlış: Apandisit granülom çözülmesiyle ilişkili primer risk değildir."
                    },
                    {
                        "text": "Demir eksikliği anemisidir.",
                        "isCorrect": False,
                        "feedback": "Yanlış: TNF blokajı hepsidini azaltarak anemiyi düzeltebilir, reaktivasyon riski tüberkülozdur."
                    }
                ]
            ),
            make_cloze(
                "Anti-TNF biyolojik tedaviler granülomun yapısal bütünlüğünü bozarak latent tüberküloz reaktivasyonuna yol açtığından tedavi öncesi tarama zorunludur.",
                "latent tüberküloz",
                "Akciğerde sessiz bekleyen mikobakteriyel tehdit"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-13-s94",
        "title": "Anti-Fibrotik Ajanlar: Pirfenidon ve Nintedanib",
        "content": "Kronik enflamasyonun son durağı olan organ fibrozisi geçmişte geri döndürülemez bir kader olarak kabul edilirdi. Günümüzde onay alan anti-fibrotik ilaçlar bu süreci yavaşlatabilmektedir:\n\n1. **Pirfenidon:**\n   - Doğrudan **TGF-β sentezini ve sinyal iletimini** inhibe eder.\n   - Fibroblast proliferasyonunu ve kollajen sentezini baskılar; antioksidan ve anti-enflamatuar özellik gösterir.\n2. **Nintedanib:**\n   - Güçlü bir küçük molekül **tirozin kinaz inhibitörüdür (TKI)**.\n   - Fibrogeneziste rol alan üç temel reseptörü aynı anda bloke eder: **PDGFR (Trombosit Kaynaklı Büyüme Faktörü Reseptörü)**, **FGFR (Fibroblast Büyüme Faktörü Reseptörü)** ve **VEGFR (Vasküler Endotelyal Büyüme Faktörü Reseptörü)**.\n- **Klinik Endikasyon:** İdiyopatik Pulmoner Fibrozis (IPF) ve sklerodermaya bağlı sistemik interstisyel akciğer hastalığı tedavisinde kullanılırlar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Anti-Enflamatuar (Steroid) vs Anti-Fibrotik (Nintedanib) Hedefler",
                "Anti-Enflamatuar İlaçlar",
                "Lökositleri, sitokinleri (TNF, IL-1) ve akut/kronik hücresel yangıyı baskılar; oturmuş fibrozise etkisizdir.",
                "Anti-Fibrotik Ajanlar (Nintedanib, Pirfenidon)",
                "Doğrudan fibroblast reseptörlerini (PDGFR, FGFR, TGF-beta) kilitleyerek kollajen birikimini durdurur."
            ),
            make_quiz(
                "İdiyopatik pulmoner fibrozis tedavisinde PDGFR, FGFR ve VEGFR reseptör kinazlarını aynı anda bloke ederek fibroblast proliferasyonunu durduran oral tirozin kinaz inhibitörü hangisidir?",
                [
                    {"key": "A", "text": "Nintedanib", "explanation": "A seçeneği DOĞRUDUR: Nintedanib PDGF, FGF ve VEGF reseptörlerini üçlü bloke eden anti-fibrotik kinaz inhibitörüdür."},
                    {"key": "B", "text": "İnfliksimab", "explanation": "B seçeneği yanlıştır: Anti-TNF monoklonal antikordur."},
                    {"key": "C", "text": "Metotreksat", "explanation": "C seçeneği yanlıştır: Dihidrofolat redüktaz inhibitörüdür."},
                    {"key": "D", "text": "Kolşisin", "explanation": "D seçeneği yanlıştır: Tübülin polimerizasyon inhibitörüdür."},
                    {"key": "E", "text": "Aspirin", "explanation": "E seçeneği yanlıştır: Siklooksijenaz inhibitörüdür."}
                ],
                "A"
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-13-s95",
        "title": "Hedefe Yönelik Biyolojikler ve Sitokin Reseptör Blokerleri",
        "content": "Kronik ve granülomatöz hastalıklarda hücreler arası haberleşmeyi kesmek amacıyla geliştirilen modern hedefe yönelik biyolojik ilaçlar klinik tıbbı dönüştürmüştür:\n\n- **Anti-IL-6 Reseptör Antikorları (Tosilizumab):** Romatoid artritte ve dev hücreli temporal arteritte yüksek ESR/CRP ve damar inflamasyonunu dramatik biçimde baskılar.\n- **Anti-IL-12 / IL-23 Antikorları (Ustekinumab):** Th1 ve Th17 farklılaşmasını ortak p40 alt ünitesinden vurarak Crohn hastalığı ve psöriyaziste kullanılır.\n- **Anti-IL-17 Antikorları (Sekukinumab, İksekizumab):** Nötrofilik infiltrasyonu durdurarak ankilozan spondilit ve psöriyaziste devrim yaratmıştır.\n- **Anti-Integrin Antikorları (Vedolizumab):** Yalnızca bağırsak venüllerindeki α4β7 integrinini bloke ederek lenfositlerin bağırsak dokusuna göçünü seçici olarak durdurur.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Biyolojik İlaç Adı", "Moleküler Hedef", "Klinik Endikasyon"],
                [
                    [
                        {"text": "Tosilizumab", "isMasked": False, "hint": ""},
                        {"text": "İnterlökin-6 Reseptörü (IL-6R)", "isMasked": True, "hint": "Akut faz sitokin reseptörü"},
                        {"text": "Dev Hücreli Temporal Arterit, Romatoid Artrit", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Sekukinumab", "isMasked": True, "hint": "Th17 efektör sitokin antikoru"},
                        {"text": "İnterlökin-17A (IL-17A)", "isMasked": False, "hint": ""},
                        {"text": "Ankilozan Spondilit ve Psöriyazis", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Vedolizumab", "isMasked": False, "hint": ""},
                        {"text": "Gastrointestinal α4β7 integrini", "isMasked": True, "hint": "Bağırsağa özgü lökosit yapışma molekülü"},
                        {"text": "İnflamatuar Bağırsak Hastalıkları (Crohn, ÜK)", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Dev hücreli arterit ve romatoid artritte akut faz protein sentezini karaciğerde durduran ve endotel aktivasyonunu kesen anti-IL-6 reseptör antikoru hangisidir?",
                "Tosilizumabdır.",
                "IL-6R blokeri monoklonal antikor"
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-13-s96",
        "title": "İmmünsüpresyon Riski: Fırsatçı Mantar ve Mikobakteri Tehdidi",
        "content": "Kronik enflamatuar veya granülomatöz hastalıklarda kullanılan immünsüpresif tedaviler (yüksek doz steroidler, anti-TNF ajanlar, JAK inhibitörleri) konak savunmasını zayıflatarak fırsatçı enfeksiyonlara kapı açar:\n\n- **Granülom Savunmasının Çöküşü:** Normalde granülom içinde hapsedilmiş olan tüberküloz basilleri, Histoplasma mayaları veya Coccidioides sferülleri immünsüpresyon altında serbest kalarak vücuda dissemine olur.\n- **Pneumocystis jirovecii Pnömonisi (PJP):** CD4+ T lenfositleri baskılanan hastalarda alveollerde köpüksü eksüda ve boğulmayla seyreden öldürücü akciğer enfeksiyonu gelişir (profilaktik ko-trimoksazol verilir).\n- **Aspergilloz ve Mukormikoz:** Nötrofil ve makrofaj fonksiyonları steroidle baskılandığında anjiyoinvaziv küf mantarları damarları tıkayarak masif doku enfarktüsü yapar.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "İmmün Yeterli Granülom vs İmmünsüpresyonda Granülom Dağılması",
                "İmmün Yeterli Durum",
                "Granülom basili veya mantarı sımsıkı hapseder; enfeksiyon lokalize ve latent kalır.",
                "İmmünsüpresif Tedavi Altında",
                "T hücre ve sitokin desteği biter; granülom erir ve patojen kana karışarak milier dissemine olur."
            ),
            make_cloze(
                "Yüksek doz steroid ve biyolojik tedavi alan hastalarda CD4+ T hücre baskılanması nedeniyle alveolleri köpüksü eksüdayla dolduran fırsatçı mantar Pneumocystis jiroveciidir.",
                "Pneumocystis jirovecii",
                "Fırsatçı atipik mantar pnömonisi etkeni"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-13-s97",
        "title": "Akut ve Kronik Enflamasyonun Bütüncül Patofizyolojik Haritası",
        "content": "Akut ve kronik enflamasyon birbirinden bağımsız iki ayrı süreç değil, aynı biyolojik savunma ekseninin birbirine bağlanan evreleridir:\n\n1. **Giriş:** Doku hasarı veya enfeksiyon → Mast hücre histamini ve makrofaj sitokinleri (TNF, IL-1).\n2. **Akut Faz (Saatler):** Vazodilatasyon, artmış venüler permeabilite, nötrofil ekstravazasyonu ve fagositoz.\n3. **Yol Ayrımı (24-48. Saat):**\n   - Etken temizlenirse → Apoptoz, eferositoz, lipoksin/rezolvin salınımı ve **Tam Rezolüsyon**.\n   - Doku yıkımı ağırsa → Granülasyon dokusu ve **Skar (Fibrozis)**.\n   - Etken temizlenemezse → Monosit ve T lenfosit akını, pozitif geri bildirim ve **Kronik Enflamasyona Geçiş**.\n4. **Kronik Faz (Haftalar-Aylar):** Mononükleer infiltrasyon, masum doku hasarı, granülomlar (tüberküloz, sarkoidoz), organ fibrozisi veya amiloidoz.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Enflamasyonun Büyük Yaşam Döngüsü Haritası",
                [
                    "1. Zararlı Uyarım: Patojen veya hasar endotel ve mast hücrelerini uyararak akut yanıtı başlatır.",
                    "2. Akut Nötrofil Dalgası: Ödem sıvısı ve nötrofiller ilk 24 saatte bölgeyi istila eder.",
                    "3. Mononükleer Bayrak Devri: 48. saatte monositler ve lenfositler nötrofillerin yerini alır.",
                    "4. Çözünme veya Kronikleşme: Etken ölürse rezolüsyon; etken direnirse granülom ve fibrozis gelişir."
                ]
            ),
            make_quiz(
                "Akut enflamasyonun kronik enflamasyona dönüşmeyip orijinal doku mimarisine tamamen kavuşarak iyileşmesine ne ad verilir?",
                [
                    {"key": "A", "text": "Rezolüsyon", "explanation": "A seçeneği DOĞRUDUR: Rezolüsyon dokunun hasar ve skar bırakmadan tamamen iyileşmesidir."},
                    {"key": "B", "text": "Organizasyon", "explanation": "B seçeneği yanlıştır: Eksüdanın fibröz dokuya dönüşmesidir."},
                    {"key": "C", "text": "Kazeifikasyon", "explanation": "C seçeneği yanlıştır: Tüberküloz nekrozudur."},
                    {"key": "D", "text": "Metaplazi", "explanation": "D seçeneği yanlıştır: Hücre tipinin değişmesidir."},
                    {"key": "E", "text": "Amiloidoz", "explanation": "E seçeneği yanlıştır: Anormal protein birikimidir."}
                ],
                "A"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-13-s98",
        "title": "Doku Onarımı, Skarlaşma ve Kronik Enflamasyon Köprüsü",
        "content": "Kronik enflamasyon ile doku onarımı arasındaki ilişki, yapım ve yıkımın bitmeyen trajik savaşıdır:\n\n- **Granülasyon Dokusu:** Erken onarım fazında gelişen, yeni narin kılcal damarlar (anjiyogenez), prolifere olan fibroblastlar ve ödemli gevşek ekstraselüler matriksten oluşan pembe, granüler görünümlü dokudur.\n- **Skarlaşmaya Geçiş:** Zamanla damarlanma azalır, fibroblastlar kollajen sentezini artırır; doku büzülerek soluk, damarsız ve sert bir fibröz skara dönüşür.\n- **Kronik Yangının Farkı:** Normal yarada granülasyon dokusu skara dönüşüp biter. Kronik enflamasyonda ise iltihap sönmediği için bir odakta granülasyon dokusu kurulurken bitişik odakta nekroz ve diğer odakta sert skarlaşma **aynı anda yan yana** görülür!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Granülasyon Dokusu vs Granülomatöz Enflamasyon (Kritik Ayrım)",
                "Granülasyon Dokusu (Onarım Dokusu)",
                "Yeni kapiller damarlar, fibroblastlar ve ödem içerir; yara iyileşmesinin erken vasküler basamağıdır.",
                "Granülomatöz Enflamasyon (İzolasyon Yanıtı)",
                "Epiteloid histiositler, dev hücreler ve lenfosit kuşağı içerir; fagositoza dirençli etken karantinasıdır."
            ),
            make_cloze(
                "Yeni oluşan kapiller damarlar, fibroblastlar ve gevşek ekstraselüler matriksten oluşan erken yara iyileşme dokusuna granülasyon dokusu denir.",
                "granülasyon dokusu",
                "Granülom ile karıştırılmaması gereken vasküler onarım dokusu"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-13-s99",
        "title": "Kronik Enflamasyon ve Granülom Patolojisi: Klinik İnciler ve Sınav Spotları",
        "content": "Tıp fakültesi kurullarında ve uzmanlık sınavlarında kronik ve granülomatöz enflamasyonla ilgili en sık sorulan klinik inciler:\n\n1. **Baskın Hücre:** Kronik enflamasyonda baskın hücre makrofajdır.\n2. **M1 vs M2:** M1 (IFN-γ) mikrop öldürür/doku yıkar; M2 (IL-4/IL-13) onarım ve fibrozis yapar.\n3. **Langhans Dev Hücresi:** Periferik nal/taç dizilimli çekirdekler (Tüberküloz); Langerhans hücresi ile KARIŞTIRILMAZ!\n4. **Kazeöz vs Non-Kazeöz:** Tüberküloz = kazeöz; Sarkoidoz ve Crohn = non-kazeöz çıplak granülom.\n5. **Sifiliz (Gumma):** Yoğun plazma hücresi ve endarteritis obliterans.\n6. **Kedi Tırmığı:** Yıldızsı (stellat) süpüratif nekrotizan granülom (merkezde nötrofiller).\n7. **Yabancı Cisim:** Polarize ışıkta çift kırıcılık (birefringens).\n8. **Anti-TNF Tehlikesi:** Granülom harcını eriterek latent tüberkülozu patlatır!",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hastalık / Durum", "Anahtar Hücre / Yapı", "Tanısal İpucu / Sınav Spotu"],
                [
                    [
                        {"text": "Tüberküloz", "isMasked": False, "hint": ""},
                        {"text": "Langhans dev hücresi ve kazeöz nekroz", "isMasked": False, "hint": ""},
                        {"text": "EZN boyasında kırmızı basiller, amorf nekroz", "isMasked": True, "hint": "Asit-fast boyama bulgusu"}
                    ],
                    [
                        {"text": "Sarkoidoz", "isMasked": True, "hint": "Bilateral hiler LAP yapan hastalık"},
                        {"text": "Çıplak non-kazeöz granülomlar", "isMasked": False, "hint": ""},
                        {"text": "Schaumann ve Asteroid cisimcikleri", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Kedi Tırmığı Hastalığı", "isMasked": False, "hint": ""},
                        {"text": "Stellat süpüratif granülom", "isMasked": True, "hint": "Nötrofilli yıldızsı lezyon"},
                        {"text": "Bartonella henselae, merkezde nötrofiller", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Sarkoidozda dev hücre sitoplazmasında görülen konsantrik lamine kalsiyum birikimlerine ne ad verilir?",
                "Schaumann cisimciğidir.",
                "Sarkoidozun kalsifiye inklüzyon adı"
            )
        ]
    })

    # Slide 100
    slides.append({
        "id": "k1-13-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Kronik ve Granülomatöz Enflamasyon Bütüncül Özeti",
        "content": "Tebrikler! 100 slaytlık devasa Kronik ve Granülomatöz Enflamasyon destesini başarıyla tamamladınız. Bu büyük finalde tüm dersi tek bir panoramik zihin haritasında birleştiriyoruz:\n\n- **Kronik Enflamasyon:** Haftalar-aylar süren, mononükleer hücrelerin (makrofaj, lenfosit, plazma hücresi) dokuyu istila ettiği, doku yıkımı ve onarımın (fibrozis/anjiyogenez) eş zamanlı sürdüğü yanıttır.\n- **Makrofaj Kutupları:** M1 mikrop avcısı ve doku tahripçisi (IFN-γ uyarılı); M2 onarım ve organ fibrozisi mimarı (IL-4/IL-13 ve TGF-β uyarılı).\n- **Granülom Mimarisi:** Fagositoza dirençli etkenlerin epiteloid histiosit duvarıyla karantinaya alınması. Langhans dev hücresi (nal dizilimli), kazeöz (tüberküloz) ve non-kazeöz (sarkoidoz, Crohn) ayrımı.\n- **Sistemik Yansımalar:** TNF kaynaklı kaşeksi, IL-6 ve hepsidin kaynaklı kronik hastalık anemisi, SAA kaynaklı sekonder AA amiloidoz ve organ fibrozisleri.\n- **Klinik ve Tedavi:** Granülomatöz hastalıklarda etkenin özel boyalarla (EZN, GMS, Warthin-Starry) tespiti ve anti-TNF tedavilerde tüberküloz reaktivasyonunun önlenmesi hayati önem taşır.",
        "sourcePdf": "Kurul 1 - Ders 13: Kronik ve Granülomatöz Enflamasyon (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Kronik ve granülomatöz enflamasyonun tüm patolojisi göz önüne alındığında, granülomun merkezinde epiteloid hücre oluşumunu tetikleyen ve granülom duvarının stabilitesini koruyan iki anahtar sitokin hangisidir?",
                [
                    {"key": "A", "text": "İnterferon-gama (IFN-γ) ve Tümör Nekroz Faktörü (TNF-α)", "explanation": "A seçeneği DOĞRUDUR: IFN-gama epiteloid dönüşümü başlatır, TNF-alfa granülomun yapısal bütünlüğünü korur."},
                    {"key": "B", "text": "İnterlökin-4 ve İnterlökin-5", "explanation": "B seçeneği yanlıştır: Th2 alerjik sitokinleridir."},
                    {"key": "C", "text": "Histamin ve Bradikinin", "explanation": "C seçeneği yanlıştır: Akut vazoaktif mediyatörlerdir."},
                    {"key": "D", "text": "İnterlökin-10 ve TGF-beta", "explanation": "D seçeneği yanlıştır: Anti-enflamatuar ve onarıcı sitokinlerdir."},
                    {"key": "E", "text": "Eotaksin ve LTB4", "explanation": "E seçeneği yanlıştır: Kemotaktik moleküllerdir."}
                ],
                "A"
            ),
            make_cloze(
                "Kronik ve granülomatöz enflamasyon patolojisinin bütüncül anlaşılması otoimmünite, tüberküloz ve modern biyolojik tedavilerin temelini oluşturur.",
                "granülomatöz enflamasyon",
                "Epiteloid histiositlerle karakterize özel kronik yangı tipi"
            )
        ]
    })

    return slides
