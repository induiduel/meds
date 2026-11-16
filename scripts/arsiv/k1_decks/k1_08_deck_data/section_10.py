"""
Section 10: "Inflammaging", Senolitikler ve Klinik Sentez (Slayt 91 - 100)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-08-s91",
        "title": "Inflammaging: Yaşlanmanın Steril Yangısı",
        "subtitle": "Enfeksiyöz olmayan, düşük dereceli, sistemik ve kalıcı kronik inflamasyon",
        "badge": "İmmünogeriatri",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "**Inflammaging**, yaşlanma sürecinde belirgin bir mikrobiyal enfeksiyon olmaksızın gelişen, "
                "düşük dereceli, steril ve kronik sistemik inflamasyon durumudur.\n\n"
                "Yaşlanan dokularda parçalanan hücre artıklarının saldığı endojen tehlike sinyalleri (**DAMPs**) doğuştan bağışıklık sistemini sürekli uyarır.\n\n"
                "Kanda **IL-6, TNF-alfa ve hs-CRP** gibi proinflamatuvar mediyatörler sürekli yüksek kalır.\n\n"
                "> Inflammaging; ateroskleroz, tip 2 diyabet, osteoartrit ve Alzheimer gibi neredeyse tüm dejeneratif hastalıkların ortak alevlendiricisidir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Yaşlanmaya eşlik eden düşük dereceli kronik steril inflamasyon tablosuna inflammaging adı verilir.",
                "inflammaging",
                "İnflamasyon ve yaşlanma kelimelerinden türetilen geriatrik terim"
            ),
            make_active_recall(
                "Inflammaging tablosunu akut enfeksiyöz inflamasyondan ayıran en temel iki özellik nedir?",
                "1) Mikrobiyal bir patojen olmaksızın hücresel enkazla (DAMPs) steril tetiklenmesi ve 2) Şiddetli/akut değil, düşük dereceli fakat on yıllar boyu kesintisiz sürmesidir."
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-08-s92",
        "title": "SASP: Senesens İlişkili Salgı Fenotipi",
        "subtitle": "Bölünmeyen yaşlı hücrelerin çevre dokulara yaydığı sitokin ve kemokin fırtınası",
        "badge": "Senesens Biyolojisi",
        "badgeColor": "orange",
        "coreContent": {
            "text": (
                "Senesent hücreler mitozu durdurmalarına rağmen metabolik olarak son derece aktiftir.\n\n"
                "Bu hücreler çevre doku mikroçevresine yoğun miktarda sitokin, kemokin, büyüme faktörü ve doku eritici enzim salgılar.\n\n"
                "Bu patolojik salgı profiline ==SASP== (**Senescence-Associated Secretory Phenotype**) adı verilir.\n\n"
                "> SASP, yaşlanmış bir hücrenin sadece kendi içinde kalmayıp etrafındaki sağlıklı hücreleri ve ekstrasellüler matriksi de tahrip etmesine yol açar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Senesent hücrelerin çevreye salgıladığı proinflamatuvar sitokin profiline SASP fenotipi denir.",
                "SASP",
                "Senescence-associated secretory phenotype kısaltması"
            ),
            make_before_after(
                "Genç Sessiz Hücre Salgısı ile Senesent Hücrenin SASP Salgısı",
                "Genç İstirahat Hücresi",
                "Doku dengesini koruyan minimal bazal sitokin salgısı ve sağlam ekstrasellüler matriks.",
                "SASP Salgılayan Yaşlı Hücre",
                "Yoğun IL-6, IL-8, TNF ve MMP salgısı; çevredeki kollajeni eriten ve lökosit toplayan toksik mikroçevre."
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-08-s93",
        "title": "SASP Bileşenleri ve Doku Harabiyeti",
        "subtitle": "İnterlökinler, kemokinler ve matriks metalloproteinazların (MMP) doku erozyonu",
        "badge": "Biyokimyasal Mediyatörler",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "SASP havuzunda yer alan başlıca mediyatörler ve etkileri:\n\n"
                "1. **Proinflamatuvar Sitokinler (IL-1β, IL-6, TNF-α):** Sistemik kronik inflamasyonu alevlendirir, insülin direncini artırır ve katabolizmayı (sarkopeni) tetikler.\n"
                "2. **Kemokinler (IL-8, MCP-1):** Nötrofil ve monositleri dokuya çekerek mikroçevrede steril inflamatuvar infiltrat oluşturur.\n"
                "3. **Matriks Metalloproteinazlar (==MMP-1, MMP-3, MMP-9==):** Ekstrasellüler matriks kollajenini ve elastinini parçalayarak doku elastikiyetini yok eder ve tümör invazyonunu kolaylaştırır."
            )
        },
        "interactiveElements": [
            make_table(
                ["SASP Mediyatör Grubu", "Örnek Moleküller", "Doku Düzeyindeki Yıkıcı Etkisi"],
                [
                    [("Proinflamatuvar Sitokinler", False, ""), ("IL-1β, IL-6, TNF-α", False, ""), ("İnsülin direnci ve kas erimesi (sarkopeni)", True, "Sistemik yangı ve metabolik bozulma")],
                    [("Kemokinler", False, ""), ("IL-8, MCP-1", False, ""), ("Sürekli lökosit göçü ve kronik yangı", True, "Mikroçevrede steril inflamatuvar infiltrasyon")],
                    [("Matriks Enzimleri", False, ""), ("MMP-1, MMP-3, MMP-9", False, ""), ("Kollajen parçalanması, damar sertliği ve kırışıklık", True, "Ekstrasellüler matriks liflerinin lizisi")]
                ]
            ),
            make_cloze(
                "SASP profilinde yer alarak ekstrasellüler matriks kollajenini parçalayan enzimler matriks metalloproteinazlar ailesidir.",
                "matriks metalloproteinazlar",
                "MMP kısaltmasıyla bilinen çinko bağımlı matriks eriticiler"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-08-s94",
        "title": "Parakrin Senesens: Yaşlanmanın Bulaşıcı Doğası",
        "subtitle": "Bir çürük elmanın tüm sepeti çürütmesi: SASP aracılı komşu hücre yaşlanması",
        "badge": "Parakrin Etki",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "SASP'ın en yıkıcı özelliği **parakrin senesens** oluşturmasıdır.\n\n"
                "Tek bir senesent hücrenin salgıladığı IL-1, TGF-beta ve reaktif oksijen radikalleri komşu sağlıklı hücrelerin reseptörlerine bağlanır.\n\n"
                "Komşu hücrelerde DNA hasar yanıtı ve p16/p21 ekspresyonu tetiklenir; onlar da bölünmeyi durdurup senesense girer.\n\n"
                "> Tıpkı 'bir çürük elmanın sepetteki diğer elmaları çürütmesi' gibi, dokuda biriken az sayıda yaşlı hücre geometrik bir hızla çevre dokuyu yaşlandırır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Senesent hücrelerin SASP yoluyla komşu sağlıklı hücreleri de senesense sürüklemesine parakrin senesens denir.",
                "parakrin senesens",
                "Yaşlanma sinyalinin çevre hücrelere yayılması olayı"
            ),
            make_causal_chain(
                "Parakrin Senesens Yayılım Zinciri",
                [
                    "1. İlk Senesens: Bir kök hücre telomer tükenmesiyle senesense girer.",
                    "2. SASP Başlatma: Hücre yoğun miktarda IL-6, IL-1 ve TGF-beta salgılar.",
                    "3. Komşu Teması: Sitokinler yanındaki genç ve sağlıklı hücrelerin reseptörlerini uyarır.",
                    "4. İkincil Stres: Komşu hücrede ROS patlaması ve p16 aktivasyonu oluşur.",
                    "5. Doku Yaşlanması: Senesent hücre kümesi büyüyerek doku rejenerasyonunu kilitler."
                ]
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-08-s95",
        "title": "Inflammaging ve SASP'ın İkincil Hastalıkları",
        "subtitle": "Ateroskleroz, tip 2 diyabet, osteoartrit ve sarkopeninin moleküler motoru",
        "badge": "Sistemik Patoloji",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "Kronik düşük dereceli inflamasyon ve SASP aşağıdaki dejeneratif hastalıkları doğrudan besler:\n\n"
                "- **Ateroskleroz:** Endotelde adezyon moleküllerini (VCAM-1) artırır, köpük hücre birikimini ve plak rüptürünü hızlandırır.\n"
                "- **Tip 2 Diyabet:** TNF-alfa ve IL-6 insülin reseptör substratını (IRS-1) serin fosforilasyonu ile inaktive ederek ==insülin direnci== yapar.\n"
                "- **Osteoartrit:** Kondrosit senesensi ve MMP salgısı eklem kıkırdağını aşındırır.\n"
                "- **Sarkopeni:** Çizgili kasta protein katabolizmasını kamçılayarak kas kütlesini ve gücünü eritir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "SASP sitokinleri insülin reseptör yolağını bloke ederek yaşlılarda sistemik insülin direnci gelişmesine yol açar.",
                "insülin direnci",
                "Tip 2 diyabetin temel metabolik patolojisi"
            ),
            make_active_recall(
                "Yaşlanmayla ortaya çıkan kas kütlesi ve kuvveti kaybına (sarkopeni) SASP sitokinleri nasıl katkıda bulunur?",
                "TNF-alfa ve IL-6 çizgili kasta protein sentezini (anabolizmayı) baskılarken, ubiquitin-proteazom aracılı kas proteini yıkımını (katabolizmayı) fırlatır."
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-08-s96",
        "title": "Senolitik Tedaviler: Yaşlı Hücreleri Hedefli İmha",
        "subtitle": "Dasatinib, Quercetin ve senesent hücrelerin seçici apoptoza uğratılması",
        "badge": "Senolitikler",
        "badgeColor": "teal",
        "coreContent": {
            "text": (
                "**Senolitikler**, bölünmeyen ancak çevreye SASP saçan senesent hücreleri seçici olarak intrensek apoptoza götüren ajanlardır.\n\n"
                "Senesent hücrelerin apoptotik hayatta kalma yollarını (BCL-2, BCL-XL, PI3K/Akt) geçici olarak kilitlerler:\n\n"
                "- **Dasatinib (Tirozin kinaz inhibitörü) + Quercetin (Doğal flavonoid):** Birlikte kullanıldığında yaşlı farelerde doku fonksiyonunu geri kazandırmış ve ömrü uzatmıştır.\n"
                "- **Navitoclax (ABT-263):** Güçlü bir BCL-2 ve BCL-XL inhibitörüdür.\n\n"
                "> Yaşlı dokudan senesent hücreler temizlendiğinde kök hücreler yeniden uyanır ve doku gençleşir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Senolitik kombinasyon tedavisinde tirozin kinaz inhibitörü Dasatinib ile doğal flavonoid Quercetin birlikte kullanılır.",
                "Dasatinib",
                "Lösemide de kullanılan senolitik tirozin kinaz inhibitörü"
            ),
            make_micro_quiz(
                "Senolitik ilaçların temel terapötik hedefi ve çalışma mekanizması aşağıdakilerden hangisidir?",
                {
                    "A": "Vücuttaki tüm kök hücreleri mitoza zorlamak",
                    "B": "Senesent hücrelerin apoptotik kalkanını kırarak onları seçici olarak apoptoza sürüklemek",
                    "C": "Telomer boyunu sentetik nükleotidlerle yapay olarak uzatmak",
                    "D": "Tüm kalsiyum tuzlarını kandan temizlemek",
                    "E": "mTOR kompleksini sürekli aktive etmek"
                },
                "B",
                {
                    "A": "Kök hücreleri erken tüketir.",
                    "B": "Doğru cevap B'dir: Senolitikler senesent hücrelerin hayatta kalma kalkanını (SCAPs) kırıp onları hedefli apoptozla yok eder.",
                    "C": "Telomer uzatıcı değildir.",
                    "D": "Kalsiyumla ilgisizdir.",
                    "E": "mTOR aktivasyonu yaşlanmayı hızlandırır."
                }
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-08-s97",
        "title": "Senomorfik İlaçlar: Zehirli Salgıyı Susturma",
        "subtitle": "Hücreyi öldürmeden SASP sitokin üretimini NF-kB ve mTOR üzerinden durdurma",
        "badge": "Senomorfikler",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "Senolitikler yaşlı hücreyi doğrudan öldürürken, **Senomorfikler** hücreyi öldürmeden onun toksik salgısını (**SASP**) susturur.\n\n"
                "SASP transkripsiyonunun ana yöneticileri **NF-κB** ve **mTOR** dur.\n\n"
                "- **Rapamisin:** mTOR'u baskılayarak SASP sitokinlerinin translasyonunu belirgin düşürür.\n"
                "- **Metformin:** NF-κB aktivasyonunu engelleyerek IL-6 ve TNF salgısını keser.\n\n"
                "> Böylece senesent hücreler dokuda kalsa bile çevreye yangı ve parakrin senesens yayamaz."
            )
        },
        "interactiveElements": [
            make_table(
                ["İlaç Sınıfı", "Etki Mekanizması", "Hücresel Akıbet"],
                [
                    [("Senolitik (Dasatinib, Navitoclax)", False, ""), ("Apoptotik direnci kırma (BCL-2 blokajı)", False, ""), ("Senesent hücre apoptozla tamamen ölür", True, "Dirençli hücrenin intihara sürüklenmesi")],
                    [("Senomorfik (Rapamisin, Metformin)", False, ""), ("NF-κB ve mTOR inhibisyonu", False, ""), ("Hücre yaşar ancak SASP salgısı susturulur", True, "Sitotoksisite olmadan parakrin yangının kesilmesi")]
                ]
            ),
            make_cloze(
                "Senesent hücreleri öldürmeden zararlı SASP salgılarını susturan moleküllere senomorfik ajanlar denir.",
                "senomorfik",
                "SASP baskılayıcı moleküllerin farmakolojik sınıf adı"
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-08-s98",
        "title": "Altı Yaşlanma Mekanizmasının Büyük Entegrasyon Matrisi",
        "subtitle": "Moleküler kusurlardan klinik hastalıklara uzanan patoloji sentezi",
        "badge": "Büyük Matris",
        "badgeColor": "indigo",
        "coreContent": {
            "text": (
                "Hücresel yaşlanmanın altı temel mekanizması bağımsız değildir; birbirini tetikleyen bir ağ oluşturur:\n\n"
                "DNA hasarı ve telomer kısalması p53/p21 üzerinden senesensi başlatır.\n\n"
                "Mitokondri hasarı ROS üretir; ROS hem DNA'yı hem zarları vurur.\n\n"
                "Proteostazis kaybı agregatları biriktirir; besin fazlalığı mTOR ile otofajiyi kilitler.\n\n"
                "Tüm bu hasarlar SASP ve Inflammaging ile dokuya yayılarak organ yetmezliğini mühürler."
            )
        },
        "interactiveElements": [
            make_table(
                ["Hücresel Mekanizma", "Kritik Moleküler Gösterge", "İlişkili Başlıca Klinik Patoloji"],
                [
                    [("1. DNA Hasarı", False, ""), ("gama-H2AX, p53 aktivasyonu, ATM/ATR", False, ""), ("Werner progeriası, erken karsinojenez", True, "Genomik instabiliteye bağlı erken yaşlanma sendromu")],
                    [("2. Telomer Aşınması", False, ""), ("Kritik 4 kb boyu, TAF odakları, M1 kilit", False, ""), ("Replikatif senesens, aplastik anemi, IPF", True, "Kromozom uçlarının kısalmasıyla organ yetmezliği")],
                    [("3. Mitokondriyal ROS", False, ""), ("mtDNA heteroplazmisi, MDA, Lipofuksin", False, ""), ("Kahverengi atrofi, iskemik nekroz eğilimi", True, "Organellerde oksidatif aşınma tablosu")],
                    [("4. Proteostazis Kaybı", False, ""), ("20S proteazom tıkanması, azalmış Hsp70", False, ""), ("Alzheimer (A-beta/Tau), Parkinson (Lewy)", True, "Nörodejeneratif kümelenme hastalıkları")]
                ]
            ),
            make_active_recall(
                "Altı temel yaşlanma mekanizması içinde hücrenin bölünme sayısını sınırlayan hücresel sayaç hangisidir?",
                "Telomer-telomeraz sistemi ve Hayflick limitidir (replikatif senesens)."
            )
        ]
    })

    # Slide 99 (CHECKPOINT 10)
    slides.append({
        "id": "k1-08-s99",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Inflammaging, Senolitikler ve Klinik Sentez",
        "subtitle": "Bölüm 10 Steril Yangı, SASP Mediyatörleri, Senolitik vs Senomorfik",
        "badge": "Checkpoint 10",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 10,
        "coreContent": {
            "text": (
                "Onuncu ve son kontrol noktasında inflamatuvar yaşlanmayı sabitliyoruz:\n\n"
                "1. **Inflammaging:** Düşük dereceli, steril, sistemik kronik inflamasyon zeminidir.\n"
                "2. **SASP:** Senesent hücrelerin IL-1, IL-6, TNF ve MMP salgılayarak çevre dokuyu tahrip etmesi.\n"
                "3. **Parakrin Senesens:** SASP sinyallerinin komşu sağlıklı hücreleri de senesense sokması.\n"
                "4. **Senolitikler (Dasatinib, Quercetin):** Senesent hücreleri seçici apoptozla öldürüp temizler.\n"
                "5. **Senomorfikler (Rapamisin, Metformin):** Senesent hücreyi öldürmeden SASP salgısını susturur."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "Senesent hücrelerin çevreye salgıladığı SASP profilini baskılayan ancak hücreyi öldürmeyen ilaç sınıfı hangisidir?",
                {
                    "A": "Senolitikler",
                    "B": "Senomorfikler",
                    "C": "Kaspaz aktivatörleri",
                    "D": "Telomeraz inhibitörleri",
                    "E": "Bakteriyel antibiyotikler"
                },
                "B",
                {
                    "A": "Senolitikler hücreyi doğrudan öldürür.",
                    "B": "Doğru cevap B'dir: Senomorfikler SASP salgısını susturur, hücreyi öldürmez.",
                    "C": "Apoptoz başlatır.",
                    "D": "Kanser ilacıdır.",
                    "E": "Bakteri öldürür."
                }
            ),
            make_active_recall(
                "Inflammaging zemininde sürekli salgılanan TNF-alfa ve IL-6 yaşlı bireylerde neden tip 2 diyabet riskini fırlatır?",
                "İnsülin reseptör sinyal yolağında yer alan IRS-1 molekülünü serin rezidülerinden fosforilleyerek tirozin kinaz kaskadını bloke eder ve periferik insülin direncine yol açar."
            )
        ]
    })

    # Slide 100
    slides.append({
        "id": "k1-08-s100",
        "title": "Ders 8 Master Sentezi: Hücresel Yaşlanmanın Moleküler Haritası",
        "subtitle": "TIP 310 Patoloji Kurul 1 dersinin tüm mekanik, genetik ve klinik entegrasyonu",
        "badge": "Büyük Sentez",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "Tebrikler! Ders 8 Hücresel Yaşlanma destesini başarıyla tamamladınız:\n\n"
                "- **Genom ve Telomer:** Spontan DNA hasarı + TTAGGG telomer aşınması -> p53/p21 ve p16/Rb ile G1/S senesensi (Werner/Progeria).\n"
                "- **Telomeraz:** hTERT + hTERC; kanserlerin %90'ında ölümsüzlük; eksikliğinde telomeropatiler (Diskeratozis, aplastik anemi, IPF).\n"
                "- **Mitokondri ve ROS:** ETC sızıntısı -> O2•- -> H2O2 -> •OH; SOD, Katalaz, GPx savunması; lipid peroksidasyonu ve lipofuksin.\n"
                "- **Apoptoz:** MOMP -> BAX/BAK gözenekleri -> Sitokrom c + APAF-1 -> Kaspaz-9 -> Kaspaz-3 -> DNA merdiveni ve fagositoz.\n"
                "- **Proteostazis:** Şaperon (Hsp70) ve proteazom çöküşü -> Alzheimer (A-beta/Tau) ve Parkinson (Alfa-sinüklein/Lewy).\n"
                "- **Metabolizma ve Tedavi:** IGF-1/mTOR yaşlandırır; Kalori kısıtlaması, AMPK ve SIRT1 ömrü uzatır; Senolitikler SASP'ı bitirir."
            )
        },
        "interactiveElements": [
            make_branching_logic(
                "Genç bir hekim olarak geriatri polikliniğinde yaşlanma biyolojisini yönetirken en temel yaklaşım prensibiniz ne olmalıdır?",
                [
                    {"text": "Yaşlanmanın kaçınılmaz bir yıpranma olduğunu düşünüp hiçbir koruyucu önlem almamak", "isCorrect": False, "feedback": "Yaşlanma regüle bir süreçtir, erken müdahaleler sağlığı korur."},
                    {"text": "Biyolojik yaşlanmanın altta yatan hücresel mekanizmalarını (DNA bakımı, mitokondri sağlığı, inflamasyon kontrolü) kanıta dayalı yaşam tarzı ve metabolik kontrollerle optimize etmek", "isCorrect": True, "feedback": "Kusursuz tıp vizyonu! Hücresel mekanizmaları bilmek, yaşa bağlı kronik hastalıkları önlemenin en güçlü anahtarıdır."},
                    {"text": "Hastaya kontrolsüz yüksek doz hormon tedavileri vermek", "isCorrect": False, "feedback": "Tümör riskini artırır."}
                ]
            ),
            make_active_recall(
                "Hücresel yaşlanma konusunda bir patoloğun unutmaması gereken altın kural nedir?",
                "Yaşlanma rastgele bir bozulma değil; hücrenin genomik hasar ve kansere karşı geliştirdiği bir savunma sınırıdır. Telomer kısalması ve senesens gençlikte tümör baskılarken, ileri yaşta kök hücre tükenmesi ve doku yetmezliği bedelini ödetir."
            )
        ]
    })

    return slides
