# -*- coding: utf-8 -*-
"""
Rebuild Cellular Aging & Tissue Repair Decks with High-Quality Medical Standards
1. learn-hucresel-yaslanma-ve-hucr (24 Slayt)
2. learn-doku-onarimi-yara-iyilesmesi (24 Slayt)
Prof. Dr. Hikmet Keleş & Robbins Pathology
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = 'src/data/interactive_learning_decks.json'
with open(DECKS_PATH, 'r', encoding='utf-8') as f:
    decks = json.load(f)

def make_slide(slide_num, title, subtitle, narrative, spots, practice_q):
    return {
        "slideNumber": slide_num,
        "title": title,
        "subtitle": subtitle,
        "content": narrative,
        "synthesisNarrative": narrative,
        "spots": spots,
        "spotPearls": spots,
        "relatedQuestions": [practice_q],
        "practiceQuestion": practice_q
    }

# ==============================================================================
# 1. HÜCRESEL YAŞLANMA MEKANİZMALARI (24 SLAYT)
# ==============================================================================
aging_slides = [
    make_slide(
        1,
        "Hücresel Yaşlanma: Biyolojik Tanım ve Kavramsal Çerçeve",
        "Kronolojik Yaş vs Biyolojik Yaşlanma ve Hücresel Homeostazın Çöküşü",
        """Hücresel yaşlanma, yaşam boyu maruz kalınan subletal moleküler hasarların birikmesi sonucunda hücrelerin replikatif kapasitesinin, stres yanıt mekanizmalarının ve fonksiyonel verimliliğinin ilerleyici biçimde azalması sürecidir.

**1. Temel Biyolojik Paradigma:**
• Yaşlanma basitçe zamanın geçişi (kronolojik yaş) ile tanımlanamaz. Biyolojik yaşlanma; hücresel düzeyde genetik instabilite, protein homeostazının kaybı ve metabolik dengenin bozulmasıyla şekillenen aktif ve regüle bir süreçtir.
• Yaşlanma hızı türler arasında ve aynı türün bireyleri arasında genetik faktörler, epigenetik modifikasyonlar ve çevresel maruziyetler (beslenme, toksinler, radyasyon) nedeniyle dramatik farklılıklar gösterir.

**2. Hücresel Yaşlanmanın 4 Temel Patolojik Ayağı:**
1. DNA hasarının birikmesi ve onarım enzimlerinin yetersizleşmesi,
2. Replikatif yaşlanma ve telomer kısalması (Hayflick limiti),
3. Protein homeostazının (proteostazis) bozulması,
4. Besin algılama yolaklarının disregülasyonu ve mitokondriyal oksidatif stres.""",
        [
            {"type": "warning", "badge": "🔴 BİYOLOJİK GERÇEK", "text": "Hücresel yaşlanma pasif bir yıpranma değil; DNA hasarı, telomer erozyonu ve metabolik sinyal yolaklarının regüle ettiği aktif hücresel bir programdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Hücresel yaşlanmanın temel belirteçleri: Replikatif kapasite kaybı, biriken DNA mutasyonları, proteazom yetersizliği ve mitokondriyal disfonksiyondur.", "color": "sky"}
        ],
        {
            "id": "prac-age-001",
            "question": "Aşağıdakilerden hangisi hücresel yaşlanmanın gelişiminde rol oynayan temel biyolojik mekanizmalardan biri değildir?",
            "options": [
                "A) Telomer uzunluğunun her hücre bölünmesinde kısalması",
                "B) Serbest oksijen radikallerine (ROS) bağlı kümülatif DNA hasarı",
                "C) Telomeraz enzim aktivitesinin somatik hücrelerde aşırı artması",
                "D) Şaperon ve proteazom sistemlerinin yetersizleşmesiyle hatalı protein birikimi",
                "E) Mitokondriyal solunum zincirinde elektron sızıntısı ve ATP düşüşü"
            ],
            "correctAnswer": 2,
            "explanation": "Normal somatik hücrelerde telomeraz aktivitesi bulunmaz veya çok düşüktür; telomeraz aktivitesinin artması yaşlanmayı değil, tümöral immortaliteyi (kanserleşmeyi) sağlar."
        }
    ),
    make_slide(
        2,
        "DNA Hasarı ve Onarım Yetersizliği: Progeroid Sendromlar",
        "Werner Sendromu (WRN Helikaz), Bloom Sendromu ve Ataksi-Telenjiektazi",
        """Hücre nükleusu yaşam boyunca endojen (serbest radikaller) ve ekzojen (UV ışınları, iyonizan radyasyon, karsinojenler) kaynaklı sürekli DNA hasarına maruz kalır. Genç hücrelerde baz eksizyon onarımı, nükleotid eksizyon onarımı ve homolog rekombinasyon hasarı kusursuz onarırken, yaşlanan hücrede bu kapasite aşılır.

**1. DNA Onarım Defektleri ve Erken Yaşlanma:**
Kalıtsal erken yaşlanma (progeria) sendromları DNA onarım mekanizmalarının yaşlanmadaki merkezi rolünü kesin olarak kanıtlamıştır:
• **Werner Sendromu (Erişkin Progeriası):** Otozomal resesif kalıtılır. **WRN geninde** mutasyon vardır; bu gen bir DNA helikaz ve ekzonükleaz enzimini kodlar. Hastalar 20'li yaşlarda katarakt, saç dökülmesi ve beyazlaşması, osteoporoz, ateroskleroz ve erken kanser geliştirerek 40-50 yaşlarında kaybedilir.
• **Hutchinson-Gilford Progeria Sendromu (HGPS):** Lamin A proteinini kodlayan *LMNA* gen mutasyonu sonucu nükleer zar anomalisi (**progerin** proteini birikimi) ve çocuklukta ileri yaşlanma tablosu.
• **Bloom Sendromu (BLM helikaz) ve Ataksi-Telenjiektazi (ATM kinaz):** Çift zincir kırık onarım defektleri sonucu erken yaşlanma ve aşırı kanser yatkınlığı.""",
        [
            {"type": "warning", "badge": "🔴 GENETİK KODLAMA", "text": "Werner sendromunda defektif enzim WRN DNA Helikazdır; Hutchinson-Gilford progeriasında ise defekt nükleer zar proteini olan Lamin A'dır (progerin).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Erişkin progeriası olan Werner sendromundan sorumlu gen mutasyonu DNA replikasyon ve tamirinde görevli WRN helikaz genidir.", "color": "sky"}
        ],
        {
            "id": "prac-age-002",
            "question": "25 yaşındaki bir hastada erken katarakt, deride atrofi, yaygın ateroskleroz ve osteoporoz gelişiyor. Genetik analizde DNA helikaz aktivitesinde defekt saptanan bu hastada erken yaşlanmaya yol açan sendrom hangisidir?",
            "options": [
                "A) Werner sendromu",
                "B) Li-Fraumeni sendromu",
                "C) Alport sendromu",
                "D) Cowden sendromu",
                "E) Marfan sendromu"
            ],
            "correctAnswer": 0,
            "explanation": "WRN geni mutasyonuna bağlı DNA helikaz enzim defekti sonucu 20'li yaşlarda erken yaşlanma tablosu oluşturan hastalık Werner Sendromudur."
        }
    ),
    make_slide(
        3,
        "Reaktif Oksijen Türleri (ROS) ve Oksidatif Stres Kuramı",
        "Süperoksit, Hidroksil Radikali, Lipid Peroksidasyonu ve Lipofuskin Birikimi",
        """Hücresel yaşlanmanın en köklü teorilerinden biri 'Serbest Radikal Hipotezi'dir (Harman kuramı).

**1. ROS Üretimi ve Mitokondriyal Kaynak:**
• Mitokondriyal solunum zincirinde (oksidatif fosforilasyon) oksijenin suya indirgenmesi sırasında elektron sızıntısı ile kaçınılmaz olarak **Süperoksit (O2•-)**, **Hidrojen Peroksit (H2O2)** ve en tahrip edici olan **Hidroksil Radikali (•OH)** üretilir.
• Normalde Süperoksit Dismutaz (SOD), Katalaz ve Glutatyon Peroksidaz bu radikalleri nötralize eder. Yaşlanma ile bu antioksidan enzim rezervi tükenir.

**2. Hücresel Hasar Hedefleri:**
• **Lipid Peroksidasyonu:** Poliansatüre membran yağ asitlerinin peroksidasyonu hücre zar geçirgenliğini bozar.
• **Lipofuskin (Yaşlanma / Aşınma Pigmenti):** Peroksidasyona uğramış lipid-protein kompleksleri lizozomlarda sindirilemez ve sitoplazmada sarı-kahverengi ince granüler **Lipofuskin pigmenti** olarak çöker. Özellikle kalp kası (kahverengi atrofi) ve nöronlarda yaşlanmanın histopatolojik imzasıdır.
• **Protein ve DNA Hasarı:** Nükleer ve mitokondriyal DNA'da 8-hidroksideoksiguanozin (8-OHdG) oksidasyon ürünleri birikir.""",
        [
            {"type": "warning", "badge": "🔴 PATOGNOMONİK BULGU", "text": "Yaşlı kalpte ve karaciğerde izlenen sarı-kahverengi intraselüler pigment 'Lipofuskin'dir (aşınma/yıpranma pigmenti); lipid peroksidasyonunun doğrudan kalıntısıdır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "Lipofuskin demir İÇERMEZ; Prusya mavisi ile boyanmaz; serbest radikal hasarı sonucu lizozomlarda biriken peroksidize lipid ve fosfolipid kalıntılarıdır.", "color": "sky"}
        ],
        {
            "id": "prac-age-003",
            "question": "82 yaşındaki bir hastanın otopside kalbinin küçüldüğü ve kesitinde koyu kahverengi görünüm kazandığı izleniyor. Mikroskopta miyosit nükleuslarının çevresinde sarı-kahverengi ince granüler pigment birikimi (kahverengi atrofi) saptanıyor. Bu pigment hangisidir?",
            "options": [
                "A) Hemosiderin",
                "B) Lipofuskin",
                "C) Melanin",
                "D) Bilirubin",
                "E) Homogentisik asit"
            ],
            "correctAnswer": 1,
            "explanation": "Serbest radikallerin membran lipidlerini peroksidasyona uğratması sonucu lizozomlarda biriken aşınma pigmenti Lipofuskindir; yaşlı kalpte 'kahverengi atrofi' oluşturur."
        }
    ),
    make_slide(
        4,
        "Mitokondriyal Disfonksiyon ve İntrensek Apoptoz Yolağı",
        "Sitokrom c, Apaf-1, Kaspaz Kaskadı ve Bax/Bak/Bcl-2 Regülasyonu",
        """Mitokondri yaşlanan hücrede hem hasarın ana kaynağı hem de biriken hasarın nihai infaz organelidir.

**1. Mitokondriyal DNA (mtDNA) Hassasiyeti:**
• Mitokondriyal DNA histon proteinlerinden yoksundur ve nükleer DNA'ya kıyasla DNA tamir sistemleri son derece ilkeldir.
• Bu nedenle solunum zincirinin hemen bitişiğindeki mtDNA nükleer DNA'dan 10-20 kat daha hızlı mutasyona uğrar. Hasarlı mitokondriler daha az ATP üretirken daha fazla serbest radikal kaçırır.

**2. İntrensek (Mitokondriyal) Apoptoz Yolağı:**
• **Pro-Apoptotik Proteinler:** Hücresel stres ve p53 aktivasyonu ile **Bax** ve **Bak** proteinleri oligomerize olarak mitokondri dış zarında porlar açar. BH3-only proteinleri (Bid, Bim, Bad, Puma, Noxa) bu süreci tetikler.
• **Anti-Apoptotik Proteinler:** **Bcl-2, Bcl-xL ve Mcl-1** normalde Bax ve Bak'ı baskılar. Yaşlanma ve hasar durumunda bu koruma kırılır.
• **İnfaz Kompleksi (Apoptozom):** Porlardan sitoplazmaya sızan **Sitokrom c**, sitoplazmadaki **Apaf-1** (Apoptotik Proteaz Aktive Edici Faktör-1) ve pro-kaspaz 9 ile birleşerek çark benzeri dev bir **Apoptozom** kompleksi oluşturur.
• Apoptozom **Kaspaz-9'u (başlatıcı kaspaz)** aktive eder; o da **Kaspaz-3 ve Kaspaz-6'yı (infazcı / efektör kaspazlar)** keserek hücre iskeletini ve nükleusu parçalar.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER KASKAT", "text": "İntrensek apoptozda Sitokrom c + Apaf-1 + Pro-kaspaz 9 = Apoptozom oluşturur; Başlatıcı kaspaz Kaspaz-9, İnfazcı kaspaz ise Kaspaz-3'tür.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Bax ve Bak pro-apoptotik olup mitokondri zar geçirgenliğini artırırken; Bcl-2 ve Bcl-xL anti-apoptotiktir ve sitokrom c sızıntısını bloke eder.", "color": "sky"}
        ],
        {
            "id": "prac-age-004",
            "question": "İntrensek (mitokondriyal) apoptoz yolağında mitokondri dış zar geçirgenliğinin artması sonucu sitoplazmaya salınan Sitokrom c, apoptozom kompleksini oluşturmak için sitoplazmada hangi faktörle birleşir?",
            "options": [
                "A) FasL",
                "B) Apaf-1 (Apoptotic Protease Activating Factor-1)",
                "C) TNF reseptörü",
                "D) FADD adaptör proteini",
                "E) Granzim B"
            ],
            "correctAnswer": 1,
            "explanation": "Sitokrom c sitoplazmada Apaf-1 ile birleşerek apoptozom kompleksini kurar ve pro-kaspaz 9'u aktive eder."
        }
    ),
    make_slide(
        5,
        "Replikatif Yaşlanma ve Hayflick Limiti",
        "Somatik Hücrelerin Sonlu Bölünme Kapasitesi ve Hücre Döngüsü Blokajı",
        """1961 yılında Leonard Hayflick tarafından keşfedilen 'Hayflick Limiti', normal insan somatik hücrelerinin kültür ortamında sınırsız bölünemeyeceğini, belirli bir bölünme sayısından sonra kalıcı olarak durduğunu kanıtlamıştır.

**1. Hücresel Yaşlanma Durumu (Senescence):**
• İnsan yenidoğan fibroblastları laboratuvarda yaklaşık **50-60 kez bölündükten sonra** mitozu tamamen durdurur. İleri yaştaki bireylerden alınan hücrelerde bu bölünme potansiyeli çok daha düşüktür (20-30 bölünme).
• Bu hücreler ölmez; metabolik olarak aktiftir ancak büyüme faktörlerine veya mitojenik uyarılara kesinlikle yanıt vermezler.
• Hücreler morfolojik olarak yassılaşır, devleşir ve **Senescence-Associated Beta-Galactosidase (SA-beta-gal)** enzimi yönünden kuvvetli pozitif boyanır.

**2. Hücre Döngüsü Frenleri (p53 ve p16):**
Kritik derecede kısalan telomerler DNA çift zincir kırığı gibi algılanır. Bu durum iki güçlü tümör süpresör yolu uyarır:
• **ATM/ATR -> p53 -> p21:** p21 CDK inhibitörü siklin bağımlı kinazları baskılayarak hücreyi G1 fazında tutar.
• **p16/INK4a Yolağı:** Siklin D-CDK4/6 kompleksini bloke eder; Retinoblastom (Rb) proteininin fosforilasyonu engellenir. De-fosforile Rb E2F transkripsiyon faktörünü hapsederek hücreyi **G1/S kontrol noktasında kalıcı olarak dondurur**.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER FREN", "text": "Replikatif yaşlanmada hücre döngüsünü G1 evresinde kalıcı olarak kilitleyen temel faktörler p16/INK4a ve p53-p21 yolağıdır; Rb proteini de-fosforile kalarak E2F'yi bloke eder.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Yaşlanan hücrelerin histokimyasal en tipik laboratuvar belirteci 'Senescence-Associated Beta-Galactosidase' (SA-beta-gal) pozitifliğidir.", "color": "sky"}
        ],
        {
            "id": "prac-age-005",
            "question": "Normal somatik hücrelerin belirli bir bölünme sayısına (Hayflick limiti) ulaştıktan sonra bölünmeyi kalıcı olarak durdurduğu replikatif yaşlanmada, hücre döngüsünün G1/S geçişini kilitleyen temel moleküler inhibitörler hangileridir?",
            "options": [
                "A) Siklin B ve CDK1",
                "B) p16 (INK4a) ve p21 (CIP1)",
                "C) BCL-2 ve Mcl-1",
                "D) Ras ve Raf kinazlar",
                "E) Telomeraz ve Shelterin"
            ],
            "correctAnswer": 1,
            "explanation": "Replikatif yaşlanmada p16 (INK4a) ve p53 aracılı indüklenen p21 (CIP1), CDK komplekslerini inhibe ederek Rb üzerinden hücreyi G1 fazında kalıcı olarak durdurur."
        }
    ),
    make_slide(
        6,
        "Telomer Biyolojisi: Uç Replikasyon Problemi ve Shelterin Kompleksi",
        "TTAGGG Tekrarları, T-Loop Koruyucu İlmeği ve Telomer Kısalması",
        """Ökaryotik doğrusal kromozomların uçlarında bulunan özelleşmiş nükleotid dizilerine ve nükleoprotein yapılarına **Telomer** adı verilir.

**1. Telomer Yapısı ve Dizisi:**
• İnsanlarda telomerler çift zincirli **5'-TTAGGG-3'** hekzanükleotid tekrarlarından oluşur. İnsanda doğumda telomer uzunluğu 10-15 kilobaz (kb) civarındadır.
• 3' uçta tek zincirli bir çıkıntı bulunur. Bu tek zincirli uç kendi içine katlanarak bir ilmek oluşturur (**T-loop**).
• **Shelterin Kompleksi:** Telomer uçlarını örten 6 üyeli özel bir protein kompleksidir (TRF1, TRF2, POT1, TIN2, TPP1, RAP1). Bu kompleks kromozom ucunu DNA kırık onarım mekanizmalarından (NHEJ) saklar; aksi halde hücre kromozom uçlarını çift zincir kırığı sanıp birbirine yapıştırırdı (dikentrik kromozomlar).

**2. Uç Replikasyon Problemi (End-Replication Problem):**
• DNA polimeraz enzimi zincir sentezini başlatmak için bir RNA primere ihtiyaç duyar ve sadece 5'->3' yönünde sentez yapabilir.
• Kesintili (lagging) zincirin en ucundaki primer kaldırıldığında, polimeraz bu boşluğu dolduramaz.
• Bu biyokimyasal kısıtlılık nedeniyle **her hücre bölünmesinde telomerlerden 50-200 baz çifti kaçınılmaz olarak kaybolur**. Telomerler kritik bir eşiğe (ortalama 4-5 kb) kadar kısaldığında shelterin ayrılır ve replikatif yaşlanma başlar.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER KOD", "text": "İnsan telomerlerinin hekzanükleotid tekrar dizisi 'TTAGGG'dir; telomer uçlarını kromozomal füzyonlardan koruyan protein kompleksi 'Shelterin'dir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "DNA polimerazın doğrusal kromozomun en ucunu replike edememesine 'uç replikasyon problemi' denir ve somatik hücrelerde telomer kısalmasının temel biyolojik nedenidir.", "color": "sky"}
        ],
        {
            "id": "prac-age-006",
            "question": "İnsan ökaryotik kromozomlarının uçlarında bulunan ve her hücre bölünmesinde kademeli olarak kısalan telomerlerin hekzanükleotid tekrar dizisi aşağıdakilerden hangisidir?",
            "options": [
                "A) 5'-AATAAA-3'",
                "B) 5'-TTAGGG-3'",
                "C) 5'-CCGCCA-3'",
                "D) 5'-TATAAA-3'",
                "E) 5'-GAATTC-3'"
            ],
            "correctAnswer": 1,
            "explanation": "İnsan telomerik DNA dizisi binlerce kez tekrarlayan 5'-TTAGGG-3' hekzanükleotid motifinden oluşur."
        }
    ),
    make_slide(
        7,
        "Telomeraz Enzimi ve Kanser Hücrelerinde Ölümsüzlük (İmmortalite)",
        "TERT Katalitik Alt Birimi, TERC RNA Şablonu ve Neoplazik Reaktivasyon",
        """Telomeraz, kromozom uçlarına de novo TTAGGG telomer dizileri ekleyerek telomer erozyonunu önleyen özelleşmiş bir ribonükleoprotein enzim kompleksidir (Ters Transkriptaz).

**1. Telomerazın İki Ana Bileşeni:**
• **hTERT (Human Telomerase Reverse Transcriptase):** Enzimin protein katalitik ters transkriptaz alt birimidir. Somatik hücrelerde TERT geninin promotörü epigenetik olarak susturulmuştur; bu nedenle somatik hücrelerde enzim inaktiftir.
• **hTERC (Human Telomerase RNA Component):** Telomer dizisinin sentezlenmesi için kalıp (şablon) görevi gören RNA molekülüdür.

**2. Fizyolojik Dağılım:**
• Somatik farklılaşmış hücrelerde: Telomeraz inaktiftir (hücreler yaşlanır).
• Germ hücrelerinde (sperm, oosit) ve doku kök hücrelerinde: Telomeraz aktiftir; telomer boyu korunur.

**3. Karsinojenezde Telomeraz Reaktivasyonu:**
• Malign tümörlerin **%85-90'ında** hTERT promotör mutasyonları (özellikle melanom ve glioblastomda) veya gen amplifikasyonu ile **telomeraz enzimi yeniden aktive edilir**.
• Kanser hücreleri sınırsız replikasyon potansiyeli kazanarak **ölümsüz (immortal)** hale gelir. Kalan %10-15 kanser ise telomerleri alternatif uzatma yolu (ALT - homolog rekombinasyon) ile korur.""",
        [
            {"type": "warning", "badge": "🔴 ONKOLOJİK ENZİM", "text": "İnsan kanserlerinin %90'ında hücrelerin sınırsız bölünme yeteneği (immortalite) hTERT aktivasyonu ve telomeraz reaktivasyonu ile sağlanır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Telomeraz enzimi bir RNA-bağımlı DNA polimerazdır (ters transkriptaz); germ hücrelerinde ve kanser hücrelerinde aktiftir.", "color": "sky"}
        ],
        {
            "id": "prac-age-007",
            "question": "Kanser hücrelerinin replikatif sınıra takılmadan ölümsüzlük (immortalite) kazanarak sınırsız bölünmesini sağlayan ve tümörlerin yaklaşık %90'ında yeniden aktive olan enzim kompleksi hangisidir?",
            "options": [
                "A) DNA polimeraz alfa",
                "B) Telomeraz (TERT)",
                "C) Topoizomeraz II",
                "D) RNA polimeraz II",
                "E) DNA ligaz IV"
            ],
            "correctAnswer": 1,
            "explanation": "Kanser hücrelerinin sonsuz çoğalma yeteneği TERT gen aktivasyonu ve telomeraz enziminin reaktivasyonu ile telomerlerin sürekli yenilenmesi sayesinde elde edilir."
        }
    ),
    make_slide(
        8,
        "Telomeropatiler: Kalıtsal Telomer Yetersizliği Hastalıkları",
        "Diskeratozis Konjenita, İdiyopatik Pulmoner Fibrozis ve Aplastik Anemi",
        """Telomeraz enzim bileşenlerini veya telomer koruyucu proteinleri kodlayan genlerdeki kalıtsal germline mutasyonlar 'Telomeropatiler' (kısa telomer sendromları) adı verilen bir grup klinik tabloya yol açar.

**1. Diskeratozis Konjenita:**
• *DKC1* (Diskerin) veya *TERT* / *TERC* gen mutasyonlarına bağlıdır.
• **Klasik Tanı Triadı:**
  1. Ciltte ağsı (retiküler) hiperpigmentasyon,
  2. Tırnak distrofisi (tırnakların çatlaması ve dökülmesi),
  3. Ağız mukozasında lökoplaki.
• Hastalarda erken yaşta **kemik iliği yetmezliği (aplastik anemi)**, immün yetmezlik ve malignite gelişir.

**2. Ailesel İdiyopatik Pulmoner Fibrozis (İPF):**
• Erişkinde ailesel pulmoner fibrozis olgularının %15'inde *TERT* veya *TERC* mutasyonları saptanır; alveol tip II pnömosit kök hücrelerinin erken tükenmesi fibrozisi tetikler.

**3. Kriptojenik Siroz ve Aplastik Anemi:**
Karaciğer kök hücrelerinin ve hematopoetik kök hücrelerin telomer kısalması sonucu erken yaşlanıp tükenmesidir.""",
        [
            {"type": "clinical", "badge": "🔴 GENETİK TRİAD", "text": "Retiküler cilt pigmentasyonu + tırnak distrofisi + oral lökoplaki triadı Diskeratozis Konjenitadır; kısa telomer sendromudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Diskeratozis konjenita ve ailesel idiyopatik pulmoner fibrozis patogenezinde telomeraz genlerinde (TERT, TERC, DKC1) fonksiyon kaybı mutasyonları yer alır.", "color": "sky"}
        ],
        {
            "id": "prac-age-008",
            "question": "Ağız mukozasında lökoplaki, tırnaklarda atrofik distrofi, boyunda retiküler pigmentasyon ve ilerleyici aplastik anemi saptanan 18 yaşındaki bir hastada telomeraz kompleksine ait hangi moleküler yapıda mutasyon aranmalıdır?",
            "options": [
                "A) Diskerin (DKC1) veya TERT",
                "B) FGFR3",
                "C) CFTR",
                "D) VHL",
                "E) Fibrillin-1"
            ],
            "correctAnswer": 0,
            "explanation": "Diskeratozis konjenita telomeraz enzimini stabilize eden Diskerin (DKC1) veya TERT gen mutasyonlarına bağlı prototipik bir telomeropatidir."
        }
    ),
    make_slide(
        9,
        "Protein Homeostazı (Proteostazis) Bozulması ve Otofaji Yetersizliği",
        "Şaperonlar, Ubiquitin-Proteazom Sistemi (UPS) ve Agregat Toksisitesi",
        """Genç hücrelerde proteinlerin doğru katlanması, işlenmesi ve hasarlı olanların yıkılması mükemmel bir denge (Proteostazis) içindedir. Yaşlanma ile bu sistemler kademeli olarak çöker.

**1. Şaperon Yetersizliği:**
Isı şok proteinleri (Hsp70, Hsp90 gibi moleküler şaperonlar) yeni sentezlenen polipeptidlerin doğru üçüncül yapıya katlanmasını sağlar. Yaşlanmayla şaperon sentezi azalır; yanlış katlanmış proteinler hücre içinde birikir.

**2. Ubiquitin-Proteazom Sistemi (UPS) İflası:**
Yanlış katlanmış veya hasarlı sitozolik proteinler ubiquitin molekülleri ile etiketlenerek 26S proteazom kompleksinde aminoasitlere parçalanır. Yaşlanan hücrelerde proteazom enzim aktivitesi belirgin olarak geriler.

**3. Otofaji (Makrootofaji) Yavaşlaması:**
Hasarlı büyük organellerin (özellikle yaşlı mitokondrilerin — mitofaji) ve protein agregatlarının otofagozomlar içinde lizozomla birleşerek eritilmesidir. Yaşlanma ile otofaji genleri (Atg genleri) baskılanır; temizlenemeyen hasarlı proteinler kümeleşerek toksik agregatlar oluşturur.
• Sonuç: Nörodejeneratif hastalıklar (Alzheimer'da amiloid-beta ve tau; Parkinson'da alfa-sinüklein / Lewy cisimcikleri).""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Yaşlanan nöronlarda proteazom ve otofajinin yetersizleşmesi yanlış katlanmış protein agregatlarının (tau, alfa-sinüklein) birikmesine ve nörodejenerasyona yol açar.", "color": "rose"},
            {"type": "exam", "badge": "🔵 KOMİTE ÇIKMIŞI", "text": "Hücrede sitozolik proteinlerin proteazomda yıkılabilmesi için 'Ubiquitin' molekülleriyle etiketlenmesi şarttır; yaşlanmayla proteazomal klirens çöker.", "color": "sky"}
        ],
        {
            "id": "prac-age-009",
            "question": "Hücre içi yanlış katlanmış ve hasarlanmış proteinlerin 26S proteazom kompleksinde tanınıp yıkılabilmesi için bu proteinlere kovalent olarak bağlanması gereken işaretleyici polipeptid hangisidir?",
            "options": [
                "A) Sitokrom c",
                "B) Ubiquitin",
                "C) Lamin A",
                "D) Kalretikülin",
                "E) Transferrin"
            ],
            "correctAnswer": 1,
            "explanation": "Proteinlerin proteazomda degrade edilmesi için ubiquitin ligaz enzimleri aracılığıyla poli-ubiquitin zinciri ile etiketlenmesi zorunludur."
        }
    ),
    make_slide(
        10,
        "Besin Algılama Yolakları ve Kalori Kısıtlaması (Caloric Restriction)",
        "IGF-1 / mTOR Ekseni Yaşlanmayı Hızlandırırken, Sirtuinler ve AMPK Ömrü Uzatır",
        """Hücrelerin besin ve enerji düzeyini algılayan moleküler yolaklar yaşam süresini doğrudan kontrol eder.

**1. Yaşlanmayı Hızlandıran Yolak: İnsülin / IGF-1 ve mTOR Ekseni:**
• Bol gıda ve aşırı kalori alımı pankreastan insülin ve karaciğerden **IGF-1** salgısını artırır.
• IGF-1 hücre içi **mTOR (mechanistic target of rapamycin)** kinaz kompleksini aktive eder.
• mTOR hücre büyümesini ve protein sentezini uyarırken; DNA onarımını, şaperonları ve **otofajiyi şiddetle baskılar**. Sonuç: Hücresel hasar hızla birikir, yaşlanma hızlanır.
• mTOR inhibitörü olan **Rapamisin** deney hayvanlarında ömrü uzatan kanıtlanmış bir ajandır.

**2. Yaşlanmayı Yavaşlatan Yolak: Sirtuinler ve AMPK:**
• **Kalori Kısıtlaması (Caloric Restriction):** Malnütrisyon olmaksızın kalori alımının %30-40 azaltılması tüm canlı türlerinde ömrü en tutarlı uzatan müdahaledir.
• Düşük glukoz ve yüksek AMP düzeyi **AMPK (AMP-aktive protein kinaz)** enzimini aktive eder; AMPK mTOR'u frenler.
• **Sirtuinler (SIRT1-7):** NAD+ bağımlı protein deasetilazlardır. Açlıkta NAD+ artışıyla uyarılırlar. p53'ü deasetile ederek aşırı apoptozu engeller, DNA onarım enzimlerini (PARP) aktive eder, PGC-1-alfa üzerinden mitokondriyal biyogenezi artırır ve antioksidan enzimleri uyarır. Kırmızı şaraptaki **Resveratrol** sirtuin aktivatörüdür.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER DENGESİ", "text": "mTOR aktivasyonu yaşlanmayı hızlandırır; Kalori kısıtlaması, AMPK ve Sirtuinler (SIRT1) ise mTOR'u baskılayıp DNA onarımını uyararak ömrü uzatır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Kalori kısıtlamasının ömrü uzatıcı etkisine aracılık eden NAD-bağımlı deasetilaz enzimleri 'Sirtuinler'dir (SIRT1).", "color": "sky"}
        ],
        {
            "id": "prac-age-010",
            "question": "Deneysel hayvan modellerinde kalori kısıtlamasının (caloric restriction) hücresel ömrü uzatıcı ve yaşlanmayı geciktirici etkisine aracılık eden, NAD+ bağımlı deasetilaz aktivitesine sahip enzim ailesi hangisidir?",
            "options": [
                "A) Kaspazlar",
                "B) Sirtuinler (SIRT)",
                "C) Siklin bağımlı kinazlar",
                "D) Matriks metalloproteinazlar",
                "E) Telomerazlar"
            ],
            "correctAnswer": 1,
            "explanation": "Sirtuinler (özellikle SIRT1) NAD+ düzeyine duyarlı deasetilazlar olup kalori kısıtlaması sırasında aktive olarak DNA tamirini uyarır ve ömrü uzatır."
        }
    ),
    make_slide(
        11,
        "Kalıcı Düşük Dereceli İnflamasyon ('Inflammaging') ve SASP",
        "Yaşlanma İlişkili Salgı Fenotipi (SASP): IL-1, IL-6, TNF ve Doku Hasarı Döngüsü",
        """Yaşlanma sürecine immün sistemin fonksiyonel gerilemesi (immünosenesans) ve eş zamanlı olarak steril kronik düşük dereceli sistemik bir yangı eşlik eder. Bu fenomene **'Inflammaging'** denir.

**1. Yaşlanma İlişkili Salgı Fenotipi (SASP - Senescence-Associated Secretory Phenotype):**
• Replikatif olarak yaşlanan (senesent) hücreler bölünmeyi durdurmalarına rağmen metabolik olarak son derece aktiftir.
• Bu hücreler çevre dokuya yoğun biçimde **pro-enflamatuar sitokinler (IL-1-alfa, IL-1-beta, IL-6, TNF-alfa)**, kemokinler (IL-8, MCP-1) ve doku yıkan **Matriks Metalloproteinazlar (MMP-1, MMP-3)** salgılar.
• Bu sekresyon paternine **SASP** adı verilir.

**2. Parakrin Hasar ve Kanser Zemin:**
• SASP faktörleri komşu genç hücreleri de parakrin yolla strese sokarak erken yaşlanmaya sevk eder (bulaşıcı senesans).
• Dokularda kollajeni yıkarak elastikiyet kaybına ve fibrozise neden olur.
• Kronik enflamatuar ortam kök hücre nişlerini bozar ve mikroçevrede gizli karsinom gelişimini kolaylaştırır (ateroskleroz, Tip 2 diyabet, osteoartrit ve kanser).""",
        [
            {"type": "clinical", "badge": "🔴 PATOLOJİK KAVRAM", "text": "Yaşlanan hücrelerin çevre dokuya IL-1, IL-6, TNF ve metalloproteinaz salgılayarak doku yıkımını hızlandırmasına SASP (Senescence-Associated Secretory Phenotype) denir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Yaşlanmaya eşlik eden steril, düşük dereceli kronik sistemik enflamasyon 'Inflammaging' olarak adlandırılır.", "color": "sky"}
        ],
        {
            "id": "prac-age-011",
            "question": "Bölünmesi durmuş senesent (yaşlanmış) hücrelerin çevre dokulara yoğun şekilde IL-1, IL-6, TNF ve doku yıkan proteazlar salgılayarak komşu hücrelerde de yaşlanmayı tetiklemesine ne ad verilir?",
            "options": [
                "A) Hayflick limiti",
                "B) Yaşlanma İlişkili Salgı Fenotipi (SASP)",
                "C) Otofaji kaskadı",
                "D) Apoptozom kompleksi",
                "E) Shelterin koruması"
            ],
            "correctAnswer": 1,
            "explanation": "Senesent hücrelerin çevreye pro-enflamatuar sitokin ve proteaz salgılaması SASP (Senescence-Associated Secretory Phenotype) olarak tanımlanır."
        }
    ),
    make_slide(
        12,
        "Ders 6 Kapsamlı Sentezi: Hücresel Yaşlanmanın Sınav ve Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Hücresel Yaşlanma dersinin komite ve sınav odaklı 10 altın kuralı:

**1. Hücresel Yaşlanmanın 10 Altın Kuralı:**
1. *Biyolojik Yaşlanma:* Zamanın geçişi değil; biriken DNA hasarı, telomer erozyonu ve proteostazis kaybıdır.
2. *Progeroid Sendromlar:* Werner sendromunda defekt WRN DNA helikazdır; Hutchinson-Gilford'da nükleer lamin A'dır.
3. *ROS ve Oksidatif Stres:* Mitokondriyal elektron kaçağı süperoksit ve hidroksil radikali üretir; lipid peroksidasyonu hücre zarlarını tahrip eder.
4. *Lipofuskin:* Yaşlı kalpte ve karaciğerde biriken sarı-kahverengi yıpranma pigmentidir; peroksidize lipid kalıntısıdır, demir içermez.
5. *Mitokondriyal Apoptoz:* Pro-apoptotik Bax/Bak por açar; Sitokrom c sitoplazmada Apaf-1 ile birleşip Apoptozom kurar; Başlatıcı kaspaz 9, İnfazcı kaspaz 3'tür.
6. *Hayflick Limiti:* Somatik hücreler 50-60 bölünme sonrası kalıcı durur; p16/INK4a ve p53-p21 yolağı Rb'yi defosforile tutarak G1'de kilitler; belirteç SA-beta-gal'dir.
7. *Telomer Biyolojisi:* Hekzanükleotid TTAGGG dizisi ve Shelterin kompleksi; uç replikasyon problemi nedeniyle her bölünmede kısalır.
8. *Telomeraz (hTERT):* Kanserlerin %90'ında reaktive olarak immortalite sağlar.
9. *Besin Algılama:* IGF-1 ve mTOR yaşlanmayı hızlandırır; Kalori kısıtlaması, AMPK ve Sirtuinler (SIRT1) ömrü uzatır.
10. *Inflammaging ve SASP:* Yaşlanan hücreler IL-1, IL-6, TNF ve MMP salgılayarak doku yıkımını ve kanserojenezi tetikler.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Hücresel yaşlanmayı özetleyen formül: Kısalan telomerler + Yetersizleşen proteazom + Mitokondriyal ROS hasarı + SASP enflamasyonu.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta özetlenen 10 kural hücresel yaşlanma konusundan komitede gelecek soruların tamamını çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-age-012",
            "question": "Aşağıdaki eşleştirmelerden hangisinde yaşlanma sürecindeki hücresel mekanizma ve ilişkili molekül yanlış verilmiştir?",
            "options": [
                "A) Uç replikasyon problemi — Telomer kısalması",
                "B) İntrensek apoptoz kaskadı — Sitokrom c ve Apaf-1",
                "C) Ömrü uzatıcı besin algılama — mTOR'un aşırı uyarılması",
                "D) Hücresel aşınma pigmenti — Lipofuskin",
                "E) Replikatif duraklama — p16 ve p21 artışı"
            ],
            "correctAnswer": 2,
            "explanation": "mTOR uyarılması yaşlanmayı yavaşlatmaz, tam tersine hızlandırır! Ömrü uzatan mekanizma mTOR'un baskılanması, AMPK ve Sirtuinlerin uyarılmasıdır."
        }
    )
]

print("Hücresel Yaşlanma 12 slayt hazırlandı (tamamlama için 24'e genişletilecek).")

# Devamı: Doku Onarımı ve Yara İyileşmesi (24 slayt)
# ==============================================================================
# 2. DOKU ONARIMI VE YARA İYİLEŞMESİ (24 SLAYT)
# ==============================================================================
repair_slides = [
    make_slide(
        1,
        "Doku Onarımı: Tanım ve İki Temel Yol",
        "Rejenerasyon (Restitutio ad Integrum) vs Skar Oluşumu (Fibrozis)",
        """Doku onarımı (iyileşme), bir dokuda gelişen hasar veya hücre kaybı sonrasında organın yapısal ve fonksiyonel bütünlüğünü yeniden kazanması sürecidir.

**1. İki Temel Onarım Yolu:**
• **Rejenerasyon (Restitutio ad Integrum):** Hasar gören hücrelerin yerini sağlam kalan parankim hücrelerinin veya doku kök hücrelerinin çoğalarak almasıdır. Doku orijinal mimarisine ve tam fonksiyonuna eksiksiz geri döner.
• **Skarla Onarım (Bağ Dokusu Birikimi / Skarlaşma):** Hasar gören parankim hücreleri çoğalamadığında veya dokunun çatısını oluşturan ekstraselüler matriks (ECM) iskeleti tahrip olduğunda devreye girer. Hasarlı alan kollajen ve bağ dokusu depolanması ile doldurulur; fonksiyonel parankim dokusu kaybolarak yerini fibröz bir skara bırakır.

**2. Rejenerasyonun Temel Koşulu:**
Rejenerasyonun gerçekleşebilmesi için sadece parankim hücrelerinin bölünme yeteneğinin olması yetmez; **ekstraselüler matriks ve bazal membran iskeletinin sağlam kalması şarttır!** İskelet çökerse organ rejenere olamaz, skarla iyileşir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KURAL", "text": "Bir dokunun skarsız tam rejenere olabilmesi için hücrelerin bölünebilmesi VE ekstraselüler matriks (ECM) bazal membran çatısının sağlam kalması zorunludur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Karaciğer toksik nekrozunda retikülin çatısı sağlamsa tam rejenerasyon olur; apse veya sirozda çatı çöktüğü için fibrozis ve skar gelişir.", "color": "sky"}
        ],
        {
            "id": "prac-rep-001",
            "question": "Hasar gören bir organda bağ dokusu birikimi (skar) olmadan tam parankimal rejenerasyonun gerçekleşebilmesi için bölünme yeteneğindeki hücrelerin varlığı dışında mutlak gerekli olan yapısal unsur hangisidir?",
            "options": [
                "A) Yoğun nötrofil infiltrasyonu",
                "B) Ekstraselüler matriks (ECM) ve bazal membran çatısının sağlam kalması",
                "C) Mast hücre degranülasyonu",
                "D) Sitokrom c salınımı",
                "E) Yüksek düzeyde p16 ekspresyonu"
            ],
            "correctAnswer": 1,
            "explanation": "Hücreler bölünse bile yönlendirici ekstraselüler matriks ve bazal membran iskelesi çökmüşse organize parankim oluşamaz ve skarlaşma gerçekleşir."
        }
    ),
    make_slide(
        2,
        "Hücre Çoğalma Kapasitesine Göre Dokular",
        "Labil (Sürekli Bölünen), Stabil (Sakin) ve Kalıcı (Permanent) Dokular",
        """Vücuttaki dokular yaralanma sonrası çoğalma ve yenilenme potansiyellerine göre üç ana gruba ayrılır.

**1. Labil (Sürekli Bölünen) Dokular:**
• Yaşam boyu sürekli hücre siklusunda (G1, S, G2, M) olan ve kök hücrelerden hızla yenilenen dokulardır.
• Hasar sonrası mükemmel rejenere olurlar.
• *Örnekler:* Kemik iliği hematopoetik hücreleri, derinin çok katlı yassı epiteli, gastrointestinal sistem (ağızdan kolona) epitel döşemesi, solunum ve üriner sistem epiteli.

**2. Stabil (Sakin / Quiescent) Dokular:**
• Normalde hücre döngüsünün dinlenme evresindedir (**G0 evresi**); mitotik aktivite düşüktür.
• Ancak doku kaybı veya uyarı olduğunda hızla G1 evresine girerek çoğalabilirler.
• *Örnekler:* **Karaciğer (hepatositler)**, böbrek tübül epiteli, pankreas parankimi, mezenkimal hücreler (fibroblastlar, vasküler endotel, osteoblastlar, düz kas hücreleri).

**3. Kalıcı (Permanent / Bölünmeyen) Dokular:**
• Hücre döngüsünü kalıcı olarak terk etmiş, terminal diferansiye hücrelerdir; mitotik bölünme yetenekleri **SIFIRDIR**.
• Hasar gördüklerinde asla rejenere olamazlar; **daima bağ dokusu skarı ile iyileşirler**.
• *Örnekler:* **Nöronlar** (santral sinir sistemi), **Kardiyak Miyositler** (kalp kası), İskelet kası lifleri.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK KODLAMA", "text": "Miyokard infarktüsü sonrası kalp kası bölünemez (kalıcı doku); nekroze miyositlerin yeri daima fibröz kollajen skarı ile doldurulur!", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV GRUBU", "text": "Labil: Deri ve GİS; Stabil: Karaciğer hepatositleri ve renal tübüller; Kalıcı (bölünmeyen): Kalp kası ve nöronlar.", "color": "sky"}
        ],
        {
            "id": "prac-rep-002",
            "question": "Aşağıdaki dokulardan hangisi hücre döngüsünü kalıcı olarak terk etmiş olup, nekroz veya infarktüs sonrasında hasarlı alanı sadece fibröz skar dokusu oluşturarak onarabilir?",
            "options": [
                "A) Karaciğer hepatositleri",
                "B) İnce bağırsak mukozal epiteli",
                "C) Kemik iliği öncül hücreleri",
                "D) Erişkin kalp kası miyositleri",
                "E) Deri epidermisi"
            ],
            "correctAnswer": 3,
            "explanation": "Kardiyak miyositler ve nöronlar kalıcı (permanent) dokulardır; bölünme yetenekleri olmadığından hasar gördüklerinde daima skar dokusuyla iyileşirler."
        }
    ),
    make_slide(
        3,
        "Karaciğer Rejenerasyonu: Moleküler Basamaklar ve İki Dalga",
        "Hepatositlerin G0'dan G1'e Hazırlığı (Priming) ve Hücre Döngüsü İlerlemesi",
        """Karaciğer stabil dokuların mükemmel rejenerasyon yeteneğine sahip en prototipik organıdır. İnsanda veya deney hayvanlarında karaciğerin üçte ikisi cerrahi olarak çıkarıldığında (parsiyel hepatektomi), kalan hepatositler çoğalarak karaciğer kitlesini birkaç hafta içinde tam orijinal ağırlığına ulaştırır.

**1. Basamak 1: Hazırlık (Priming) Fazı:**
• Dinlenme evresindeki (G0) hepatositlerin büyüme faktörlerine yanıt verebilir hale gelmesi sürecidir.
• Kupffer hücrelerinden salgılanan **İnterlökin-6 (IL-6)** ve **Tümör Nekroz Faktörü (TNF)** bu hazırlığı başlatır.
• Hepatositler G0'dan hücre döngüsünün **G1 fazına** geçer.

**2. Basamak 2: Büyüme ve Proliferasyon Fazı:**
• Hazırlanmış hepatositleri G1'den DNA sentez fazına (**S fazına**) sokan temel büyüme faktörleri **Hepatosit Büyüme Faktörü (HGF)** ve **TGF-alfa** (Transforming Growth Factor-alpha) / EGF'dir.
• Hepatositler 1-2 kez bölünür; ardından endotel ve Kupfer hücreleri çoğalarak lobül mimarisini tamamlar.

**3. Basamak 3: Terminasyon (Durdurma) Fazı:**
Karaciğer orijinal boyutuna ulaştığında çoğalmayı durduran en güçlü antiproliferatif sitokin **TGF-beta** (Transforming Growth Factor-beta)'dır.

**4. Kök Hücrelerin Rolü (Oval Hücreler):**
Eğer hepatositlerin bölünme kapasitesi kronik hasarla (kronik hepatit, siroz) tükenmişse, Hering kanallarında yerleşen karaciğer kök hücreleri (**oval hücreler / duktüler reaksiyon**) çoğalarak hepatosite dönüşür.""",
        [
            {"type": "warning", "badge": "🔴 MOLEKÜLER KASKAT", "text": "Karaciğer rejenerasyonunda hazırlık (priming) sitokinleri IL-6 ve TNF; çoğalmayı sağlayan faktörler HGF ve TGF-alfa; durduran faktör ise TGF-beta'dır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Parsiyel hepatektomi sonrası hepatositlerin S fazına geçişini sağlayan en güçlü mitojenik büyüme faktörü Hepatosit Büyüme Faktörüdür (HGF).", "color": "sky"}
        ],
        {
            "id": "prac-rep-003",
            "question": "Parsiyel hepatektomi sonrası hepatositlerin G0 fazından G1 evresine geçmesini sağlayan hazırlık (priming) fazında rol oynayan temel sitokin çifti aşağıdakilerden hangisidir?",
            "options": [
                "A) HGF ve VEGF",
                "B) IL-6 ve TNF",
                "C) TGF-beta ve PDGF",
                "D) FGF ve İnterferon-gama",
                "E) Eritropoietin ve TPO"
            ],
            "correctAnswer": 1,
            "explanation": "Hepatositlerin G0'dan G1'e uyarılması (priming) Kupffer hücrelerinden salgılanan IL-6 ve TNF aracılığıyla gerçekleşir."
        }
    ),
    make_slide(
        4,
        "Skarla Onarımın 4 Temel Aşaması",
        "Hemostaz/Enflamasyon, Granülasyon Dokusu, ECM Sentezi ve Remodeling",
        """Doku hasarı derin olduğunda veya parankim hücreleri bölünemediğinde devreye giren skarla onarım kronolojik olarak 4 birbiri içine geçen evreden oluşur.

**1. Evre 1: Hemostaz ve Akut Enflamasyon (0 - 24 Saat):**
• Yaralanma anında trombosit tıkacı ve fibrin pıhtısı oluşur; kanama durdurulur ve yara yüzeyi mühürlenir.
• İlk 24 saatte yara yatağına hızla **Nötrofil lökositler** göç eder; bakterileri fagositozla yok eder ve nekrotik debrisleri temizler.

**2. Evre 2: Hücre Proliferasyonu ve Granülasyon Dokusu (3 - 5. Gün):**
• 48-72. saatte nötrofillerin yerini **Makrofajlar (özellikle M2 onarım makrofajları)** alır. Makrofajlar doku onarımının orkestra şefidir.
• Hasarlı alanda pembe, yumuşak, granüllü ve son derece damarlı bir onarım dokusu gelişir: **Granülasyon Dokusu**.

**3. Evre 3: Kollajen Birikimi ve Skar Oluşumu (1 - 3. Hafta):**
• Fibroblastlar masif miktarda ekstraselüler matriks ve kollajen sentezleyerek yara yatağını doldurur.

**4. Evre 4: Doku Yeniden Şekillenmesi (Remodeling) (Haftalar - Aylar):**
• Damarlar regrese olur, skar soluklaşır; zayıf Tip III kollajenin yerini güçlü Tip I kollajen alır.""",
        [
            {"type": "clinical", "badge": "🔴 ORKESTRA ŞEFİ", "text": "Doku onarımının ve granülasyon dokusunun en kritik hücresi MAKROFAJDIR; salgıladığı VEGF, TGF-beta ve PDGF ile tüm süreci yönetir.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Yaralanmadan 3-5 gün sonra oluşan pembe, yumuşak, ödemli ve narin damarlardan zengin geçici onarım dokusu 'Granülasyon Dokusu'dur.", "color": "sky"}
        ],
        {
            "id": "prac-rep-004",
            "question": "Doku hasarından sonra 3. ve 5. günler arasında yara tabanında izlenen, bol yeni kılcal damarlar (anjiyogenez), prolifere olan fibroblastlar ve ödemli gevşek ekstraselüler matriksten oluşan doku hangisidir?",
            "options": [
                "A) Granülamatöz doku",
                "B) Granülasyon dokusu",
                "C) Keloid dokusu",
                "D) Osteoid doku",
                "E) Fibröz kıkırdak"
            ],
            "correctAnswer": 1,
            "explanation": "Yara tabanında yeni damarlar, fibroblastlar ve gevşek ECM'den oluşan pembe doku Granülasyon Dokusudur (granülom ile karıştırılmamalıdır)."
        }
    ),
    make_slide(
        5,
        "Granülasyon Dokusu ve Anjiyogenez Mekanizması",
        "VEGF, Perisitler, Notch Sinyali ve Narin Geçirgen Kapillerler",
        """Granülasyon dokusu adını cerrahi pansuman sırasında yara yatağında izlenen pembe, yumuşak, küçük tanecikli (granüler) görünümünden alır. Mikroskobik olarak **yeni narin damarlar (anjiyogenez)** ve prolifere olan fibroblastlardan oluşur.

**1. Anjiyogenezin (Yeni Damar Oluşumu) Temel Basamakları:**
1. *Damar Vazodilatasyonu ve Geçirgenlik:* Nitrik oksit (NO) ve VEGF etkisiyle endotel hücreleri gevşer.
2. *Bazal Membran Yıkımı:* Ana damarın bazal membranı matriks metalloproteinazlar (MMP'ler) ile eritilir.
3. *Endotel Göçü ve Uç Hücre (Tip Cell):* Büyüme faktörü gradiyentine doğru yönelen öncü bir endotel hücresi (**Tip cell**) filopodiyalar uzatarak göç eder; arkasındaki hücreler çoğalarak damar lümenini uzatır (**Stalk cells**). Bu seçim **Notch / DLL4 sinyali** ile regüle edilir.
4. *Damar Olgunlaşması ve Stabilizasyon:* Yeni oluşan kılcal damarın çevresine düz kas hücreleri ve **perisitler** toplanır. Perisit toplanmasını ve damar stabilitesini sağlayan ana faktörler **Anjiyopoietin-1 (Ang-1)** ve **PDGF**'dir.

**2. Neden Ödemlidir?**
Yeni oluşan endotel hücreleri arasındaki bağlantılar henüz tam kapanmamıştır ve VEGF güçlü bir vasküler geçirgenlik faktörüdür; bu nedenle granülasyon dokusu daima belirgin derecede ödemlidir.""",
        [
            {"type": "warning", "badge": "🔴 PATOLOJİK AYRIM", "text": "Granülom (kronik granülamatöz yangı: tüberküloz epiteloid histiyositleri) ile Granülasyon Dokusu (yara onarımında yeni damar ve fibroblastlar) tamamen farklı iki kavramdır!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Anjiyogenezde yeni damar tomurcuklanmasını başlatan ana büyüme faktörü VEGF; damarın çevresine perisit toplayarak damarı olgunlaştıran faktör PDGF ve Ang-1'dir.", "color": "sky"}
        ],
        {
            "id": "prac-rep-005",
            "question": "Yara iyileşmesinde anjiyogenez sürecinde endotel hücrelerinin tomurcuklanmasını, göçünü ve erken damar proliferasyonunu uyaran en temel büyüme faktörü hangisidir?",
            "options": [
                "A) Vasküler Endotelyal Büyüme Faktörü (VEGF)",
                "B) İnterferon gama",
                "C) İnterlökin-2",
                "D) Eritropoietin",
                "E) Trombopoietin"
            ],
            "correctAnswer": 0,
            "explanation": "VEGF endotel hücre proliferasyonu, göçü ve vazodilatasyonunu sağlayarak anjiyogenezin ana tetikleyicisidir."
        }
    ),
    make_slide(
        6,
        "Doku Onarımında Temel Büyüme Faktörleri Haritası",
        "TGF-beta, PDGF, FGF, EGF ve Sitokinlerin Görev Dağılımı",
        """Doku onarımı çeşitli hücrelerce salgılanan büyüme faktörlerinin sıkı kontrolü altındadır.

**1. Büyüme Faktörleri ve Başlıca İşlevleri:**
• **TGF-beta (Transforming Growth Factor-beta):**
  - Doku onarımında **FİBROZİS VE SKAR OLUŞUMUNUN EN GÜÇLÜ VE EN ÖNEMLİ SİTOKİNİDİR**.
  - Fibroblast kemotaksisini uyarır, fibroblastları aktive eder.
  - Tip I ve Tip III kollajen, fibronektin ve proteoglikan sentezini dramatik olarak artırır.
  - Kollajeni yıkan matriks metalloproteinazları (MMP) inhibe eder; doku inhibitörlerini (TIMP) artırarak kollajen yıkımını durdurur.
  - Aynı zamanda güçlü bir anti-enflamatuar ve immünsüpresif sitokindir.
• **PDGF (Trombosit Kaynaklı Büyüme Faktörü):**
  - Trombosit granüllerinden ve makrofajlardan salınır. Fibroblast ve düz kas hücre kemotaksisini uyarır, kollajen sentezini destekler.
• **FGF-2 (Temel Fibroblast Büyüme Faktörü / bFGF):**
  - Endotel proliferasyonunu uyararak anjiyogenezde görev alır; reepitelizasyonu destekler.
• **EGF ve TGF-alfa:**
  - Epitelyal hücre çoğalmasını uyararak yara yüzeyinin epitel ile örtülmesini (reepitelizasyon) sağlar.""",
        [
            {"type": "warning", "badge": "🔴 1 NUMARALI FİBROJENİK SİTOKİN", "text": "Doku onarımında ve tüm organ fibrozislerinde (akciğer, karaciğer, böbrek) kollajen sentezini artıran ve yıkımını durduran EN ÖNEMLİ SİTOKİN TGF-beta'dır!", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS KLASİĞİ", "text": "TGF-beta fibroblastlardan kollajen sentezini uyarırken; aynı zamanda MMP'leri baskılayıp TIMP'leri artırarak kollajen birikimini maksimize eder.", "color": "sky"}
        ],
        {
            "id": "prac-rep-006",
            "question": "Doku onarımı ve yara iyileşmesi sürecinde fibroblast kemotaksisini uyaran, kollajen sentezini en güçlü artıran ve metalloproteinazları baskılayarak fibrozisi yöneten temel sitokin hangisidir?",
            "options": [
                "A) Tümör Nekroz Faktörü (TNF)",
                "B) İnterlökin-1",
                "C) Transforming Growth Factor-beta (TGF-beta)",
                "D) Vasküler Endotelyal Büyüme Faktörü (VEGF)",
                "E) İnterlökin-8"
            ],
            "correctAnswer": 2,
            "explanation": "TGF-beta ekstraselüler matriks ve kollajen sentezini uyararak fibrozis ve skar oluşumunu yöneten ana fibrogenik faktördür."
        }
    ),
    make_slide(
        7,
        "Ekstraselüler Matriks (ECM) Bileşenleri: Kollajen, Elastin ve Glikoproteinler",
        "Tip I vs Tip III Kollajen, Çapraz Bağlar, C Vitamini ve Lizil Oksidaz",
        """Ekstraselüler matriks dokulara mekanik destek sağlar, hücrelerin tutunmasını ve büyümesini yönlendirir.

**1. Kollajen Biyolojisi:**
• Vücuttaki en bol proteindir. Üçlü sarmal (triple-helix) yapısındadır; her 3 aminoasitte bir **Glisin** bulunur (Gly-X-Y).
• **Tip I Kollajen:** Kemik, tendon, geç evre olgun skar dokusu ve deride bulunur; gerilmeye karşı en dayanıklı sert kollajendir.
• **Tip II Kollajen:** Kıkırdak dokusu ve kornea.
• **Tip III Kollajen:** Erken yara iyileşmesi (granülasyon dokusu), damar duvarı ve uterus; narin, esnek retiküler lifleri oluşturur.
• **Tip IV Kollajen:** Bazal membranların temel iskeletidir.

**2. Kollajen Sentezinde Kritik Biyokimyasal Adımlar:**
• Prolin ve Lizin aminoasitlerinin hidroksilasyonu için **C Vitamini (Askorbik Asit)** ve demir zorunludur. C vitamini eksikliğinde (Skorbüt) kollajen sarmalı kararsız kalır; yara iyileşmesi durur ve eski yaralar açılır!
• Prokollajenin hücre dışına salınmasından sonra liflerin birbirine çapraz bağlanarak (cross-linking) mekanik güç kazanmasını sağlayan enzim bakır bağımlı **Lizil Oksidaz** enzimidir.""",
        [
            {"type": "warning", "badge": "🔴 BİYOKİMYASAL BAĞLANTI", "text": "C vitamini eksikliğinde (Skorbüt) prolin hidroksilasyonu bozulduğu için kollajen sentezlenemez; yara iyileşmesi durur ve dikişler açılır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV BİLGİSİ", "text": "Erken granülasyon dokusunda Tip III kollajen hakimdir; yara olgunlaştıkça Tip III kollajenin yerini gerilmeye dayanıklı Tip I kollajen alır.", "color": "sky"}
        ],
        {
            "id": "prac-rep-007",
            "question": "Yara iyileşmesinin erken evresinde granülasyon dokusunda sentezlenen ilk kollajen tipi ve yaranın olgunlaşması sürecinde onun yerini alan mekanik dayanıklı kollajen tipi sırasıyla hangileridir?",
            "options": [
                "A) Tip I kollajen — Tip II kollajen",
                "B) Tip III kollajen — Tip I kollajen",
                "C) Tip IV kollajen — Tip III kollajen",
                "D) Tip II kollajen — Tip IV kollajen",
                "E) Tip I kollajen — Tip IV kollajen"
            ],
            "correctAnswer": 1,
            "explanation": "Yaranın erken fazında önce narin Tip III kollajen sentezlenir; remodeling evresinde bunun yerini gerilme direnci yüksek Tip I kollajen alır."
        }
    ),
    make_slide(
        8,
        "Yara İyileşmesinin Tipleri: Primer ve Sekonder İyileşme",
        "Per Primam (Cerrahi Kesi) vs Per Secundam (Doku Kayıplı / Enfekte Yara)",
        """Kutanöz yaraların iyileşme paterni doku kaybının büyüklüğüne ve yara kenarlarının durumuna göre iki temel sınıfa ayrılır.

**1. Primer İyileşme (İntentionem per Primam):**
• Temiz, enfekte olmayan, doku kaybının minimal olduğu cerrahi insizyonların cerrahi dikiş veya zımba ile uç uca getirilmesiyle gerçekleşir.
• Yalnızca ince bir fibrin pıhtısı ve minimal nötrofilik eksüda oluşur.
• Granülasyon dokusu miktarı çok azdır.
• Epitelyal rejenerasyon 24-48 saatte yara yüzeyini tamamen kapatır.
• İyileşme sonucunda minimal, **ince çizgi şeklinde bir skar** kalır; doku kontraksiyonu önemsiz düzeydedir.

**2. Sekonder İyileşme (İntentionem per Secundam):**
• Geniş doku kaybı olan yaralar (ülserler, yanıklar, abseler, infekte cerrahi yaralar) kenarları karşılıklı getirilemediğinde açık bırakılır.
• Doku kaybı büyük olduğu için temizleme ve enflamasyon çok daha uzun sürer.
• Hasarlı boşluğu doldurmak için **çok büyük miktarda granülasyon dokusu** oluşur.
• **Yara Kontraksiyonu:** Sekonder iyileşmenin en ayırt edici özelliğidir. Doku kusurunu küçültmek için **miyofibroblastlar** yara kenarlarını merkeze doğru çeker; yara alanı %70-80 oranında küçülür.
• Belirgin, kaba, çökük ve geniş bir skar dokusu ile sonuçlanır.""",
        [
            {"type": "clinical", "badge": "🔴 AYIRICI TANI KRİTİĞİ", "text": "Sekonder iyileşmeyi primerden ayıran temel özellikler: Masif granülasyon dokusu, kaba skar ve miyofibroblastların yaptığı güçlü Yara Kontraksiyonudur.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Geniş doku kayıplı sekonder yara iyileşmesinde yara alanını büzüştürerek küçülten hücre grubu alfa-düz kas aktini içeren 'Miyofibroblastlar'dır.", "color": "sky"}
        ],
        {
            "id": "prac-rep-008",
            "question": "Geniş doku kaybı olan açık bir yaranın sekonder iyileşmesi sürecinde yara kenarlarını birbirine yaklaştırarak yara defektini büzüştüren (yara kontraksiyonu) temel hücre hangisidir?",
            "options": [
                "A) Nötrofiller",
                "B) Miyofibroblastlar",
                "C) Mast hücreleri",
                "D) Endotel hücreleri",
                "E) Keratinositler"
            ],
            "correctAnswer": 1,
            "explanation": "Miyofibroblastlar aktin filamentleri içerir ve kasılarak yara defektini küçültür (yara kontraksiyonu)."
        }
    ),
    make_slide(
        9,
        "Yara Gücünün Kazanılması ve Yeniden Şekillenme (Remodeling)",
        "Dikiş Alınması (%10), Çapraz Bağlar ve Maksimum Dayanıklılık Limiti (%70-80)",
        """Yara iyileşmesi sadece dokunun kapanmasıyla bitmez; ekstraselüler matriksin aylar süren dinamik bir yeniden modellenme (remodeling) sürecine girmesi gerekir.

**1. Matriks Metalloproteinazlar (MMP'ler) ve Denge:**
• Kollajen birikimi ile kollajen yıkımı sürekli dengede olmalıdır. Kollajeni parçalayan enzimler çinko bağımlı **Matriks Metalloproteinazlardır (MMP'ler)**:
  - *İnterstisyel Kollajenazlar (MMP-1, 2, 3):* Fibriler Tip I, II, III kollajeni keser.
  - *Jelatinazlar (MMP-2, 9):* Parçalanmış kollajeni ve Tip IV bazal membranı eritir.
• Bu enzimlerin kontrolsüz yıkım yapmasını doku inhibitörleri olan **TIMP'ler (Tissue Inhibitors of Metalloproteinases)** engeller.

**2. Yara Gücünün Zamansal Seyri:**
• **1. Haftada (Cerrahi dikişler alındığında):** Yara gerilme direnci sağlam derinin **yalnızca yaklaşık %10'u** kadardır! Bu nedenle erken dönemde ağır yük binmesi dikiş açılmasına (dehisens) yol açabilir.
• **3. Ayda:** Tip III kollajenin Tip I'e dönmesi ve lizil oksidaz ile liflerin çapraz bağlanması sonucu yara gerilme gücü platoya ulaşır.
• **Nihai Sınır:** İyileşmiş bir yaranın mekanik dayanıklılığı hiçbir zaman sağlam orijinal derinin gücüne (%100) ulaşamaz; **maksimum %70-80 seviyesinde kalır!**""",
        [
            {"type": "clinical", "badge": "🔴 KLİNİK EŞİK", "text": "Cerrahi dikişler alındığında yara gücü sağlam derinin sadece %10'udur; 3 ay sonunda ulaşılan maksimum yara gücü ise sağlam derinin %70-80'idir (asla %100 olmaz).", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ SINAV SPOTU", "text": "ECM remodeling sürecinde kollajeni yıkan enzimler çinko bağımlı Matriks Metalloproteinazlardır (MMP); inhibitörleri TIMP'lerdir.", "color": "sky"}
        ],
        {
            "id": "prac-rep-009",
            "question": "Temiz bir cerrahi insizyonun iyileşmesi sürecinde 1. haftanın sonunda cerrahi dikişler alındığında yaranın gerilme direnci sağlam orijinal cildin yaklaşık yüzde kaçı kadardır?",
            "options": [
                "A) %10",
                "B) %30",
                "C) %50",
                "D) %80",
                "E) %100"
            ],
            "correctAnswer": 0,
            "explanation": "1. haftanın sonunda dikişler alındığında yara gücü sağlam dokunun sadece yaklaşık %10'u seviyesindedir; 3. ayda maksimum %70-80'e ulaşır."
        }
    ),
    make_slide(
        10,
        "Yara İyileşmesini Geciktiren Faktörler: Lokal ve Sistemik Engeller",
        "Enfeksiyon (1 Numara), Diyabet, Glukokortikoidler, C Vitamini ve Çinko Eksikliği",
        """Yara iyileşmesi vücuttaki birçok lokal ve sistemik faktörün olumsuz etkisine karşı son derece hassastır.

**1. Lokal Faktörler:**
• **Enfeksiyon:** Yara iyileşmesinin gecikmesinde **açık ara en sık ve en önemli nedendir!** Kalıcı nötrofilik infiltrasyon doku yıkımını sürdürür ve granülasyon dokusunu tahrip eder.
• **Mekanik Faktörler:** Erken hareket, gerginlik veya öksürükle karın içi basınç artışı yara kenarlarını ayırır (yara dehisensi).
• **Yabancı Cisimler:** Cerrahi dikiş parçaları, kemik fragmanları veya cam kırıkları kronik süpürasyona yol açar.
• **İskemi / Yetersiz Perfüzyon:** Aterosklerotik arter hastalığı veya venöz staz doku oksijenasyonunu bozar.

**2. Sistemik Faktörler:**
• **Beslenme Bozuklukları:** Protein malnütrisyonu ve özellikle kollajen hidroksilasyonu için şart olan **C Vitamini eksikliği** ile metalloenzimler için gerekli **Çinko eksikliği**.
• **Diabetes Mellitus:** Mikrovasküler yetersizlik, azalmış nötrofil fagositozu ve glikozillenmiş dokular nedeniyle enfeksiyon ve gecikmiş iyileşme kuraldır.
• **Glukokortikoidler (Kortikosteroid Kullanımı):** Anti-enflamatuar etkileriyle TGF-beta salınımını ve kollajen sentezini baskılarlar; yara iyileşmesini zayıflatıp yara açılmasına zemin hazırlarlar.""",
        [
            {"type": "warning", "badge": "🔴 1 NUMARALI GECİKTİRİCİ FAKTÖR", "text": "Yara iyileşmesini geciktiren en sık lokal faktör Enfeksiyondur; sistemik faktörler içinde ise Diyabet ve Glukokortikoid kullanımı başı çeker.", "color": "rose"},
            {"type": "exam", "badge": "🔵 ÇIKMIŞ TUS VURGUSU", "text": "Glukokortikoidler fibroblast proliferasyonunu ve TGF-beta aracılı kollajen sentezini inhibe ederek yara gücünü belirgin azaltır.", "color": "sky"}
        ],
        {
            "id": "prac-rep-010",
            "question": "Aşağıdakilerden hangisi yara iyileşmesini geciktiren lokal faktörler arasında en sık karşılaşılan nedendir?",
            "options": [
                "A) Çinko eksikliği",
                "B) Yara yeri enfeksiyonu",
                "C) C vitamini eksikliği",
                "D) Protein malnütrisyonu",
                "E) Sistemik kortikosteroid kullanımı"
            ],
            "correctAnswer": 1,
            "explanation": "Yara iyileşmesini bozan en sık lokal neden yara yeri enfeksiyonudur (diğer seçenekler sistemik faktörlerdir)."
        }
    ),
    make_slide(
        11,
        "Aşırı Yara İzi Oluşumu: Hipertrofik Skar vs Keloid Ayrımı",
        "Orijinal Sınırlar İçinde Kalma vs Çevreye Taşma, Kollajen Tipleri ve Zenci Irk Yatkınlığı",
        """Onarım sürecinde ekstraselüler matriks ve kollajen üretiminin kontrolsüz artışı patolojik aşırı yara izlerine (fibroproliferatif lezyonlar) yol açar.

**1. Hipertrofik Skar:**
• Genellikle derin termal yanıklar veya travmatik yaralanmalar sonrasında hızlı kollajen birikimiyle oluşur.
• **Sınırlar:** Ciltten kabarıktır ancak **asla orijinal yara sınırlarının dışına TAŞMAZ**.
• **Histoloji:** Ağırlıklı olarak paralel demetler halinde dizilmiş **Tip III kollajen** içerir.
• **Seyir:** Zamanla aylar içinde kendiliğinden gerileme (regresyon) eğilimi gösterebilir; cerrahi eksizyon sonrası nüks düşüktür.

**2. Keloid:**
• Bireysel ve genetik yatkınlığı olan kişilerde (özellikle **Zenci / Afrika kökenlilerde** 10-20 kat daha sıktır) cerrahi kesi, kulak deldirme, aşı veya minimal akne izi sonrası gelişir.
• **Sınırlar:** Belirgin şekilde kabarık, parlak, sert ve **orijinal yara sınırlarını aşarak çevre normal deriye karnabahar gibi TAŞAR**.
• **Histoloji:** Gelişigüzel, kalın, hiyalinize devasa **Tip I ve Tip III kollajen demetleri** içerir.
• **Seyir:** Kendiliğinden **asla gerilemez**; cerrahi olarak kesilip çıkarıldığında çok daha büyük bir kitle olarak **yüksek oranda nükseder!** Tedavide intralezyonel steroid enjeksiyonu uygulanır.""",
        [
            {"type": "warning", "badge": "🔴 KRİTİK AYIRICI TANI", "text": "Hipertrofik skar orijinal yara sınırları içinde kalır ve gerileyebilir; Keloid ise orijinal yara sınırlarını taşarak çevre sağlam dokuya yayılır ve kendiliğinden asla gerilemez!", "color": "rose"},
            {"type": "exam", "badge": "🔵 EN SIK SORULAN SINAV MATRİSİ", "text": "Keloid Afrika ırkında sıktır; kalın hiyalinize kollajen demetleri içerir; cerrahi eksizyonu kontrendikedir çünkü nüksü tetikler.", "color": "sky"}
        ],
        {
            "id": "prac-rep-011",
            "question": "Kulağını deldirdikten 6 ay sonra delik bölgesinde orijinal delinme sınırlarını belirgin şekilde aşan, çevre sağlam deriye doğru genişleyen, kaşıntılı ve sert nodüler fibröz kitle gelişen siyah tenli hastada tanı nedir?",
            "options": [
                "A) Hipertrofik skar",
                "B) Keloid",
                "C) Dermatofibrom",
                "D) Eksuberan granülasyon",
                "E) Epidermal kist"
            ],
            "correctAnswer": 1,
            "explanation": "Orijinal travma sınırlarını aşarak çevre sağlam dokuya taşan kaba fibroproliferatif lezyon Keloiddir (zenci ırkta sıktır)."
        }
    ),
    make_slide(
        12,
        "Ders 9 Kapsamlı Sentezi: Doku Onarımı ve Yara İyileşmesinin Klinik Kodları",
        "Prof. Dr. Hikmet Keleş Amfi Dersinin En Kritik Sınav İncileri ve 10 Temel Kuralı",
        """Doku Onarımı ve Yara İyileşmesi dersinin komite ve sınav odaklı 10 altın kuralı:

**1. Doku Onarımının 10 Altın Kuralı:**
1. *Onarım Yolları:* Rejenerasyon (orijinal dokuya tam dönüş) ve Skarla Onarım (kollajen birikimi/fibrozis).
2. *Doku Tipleri:* Labil = Sürekli bölünen (deri, bağırsak); Stabil = G0'dan G1'e giren (hepatosit, tübül); Kalıcı = Asla bölünmeyen (miyokard miyositi, nöron).
3. *Karaciğer Rejenerasyonu:* Kupffer'den IL-6 ve TNF ile priming (G0->G1); HGF ve TGF-alfa ile çoğalma (S fazı); TGF-beta ile durdurma.
4. *Orkestra Şefi:* Doku onarımını yöneten ana hücre M2 Makrofajdır; büyüme faktörlerini salgılar.
5. *Granülasyon Dokusu:* 3-5. günde yeni damarlar (anjiyogenez) + fibroblastlar + gevşek ödemli matriks.
6. *Büyüme Faktörleri:* Anjiyogenez = VEGF ve FGF; Fibrozis ve kollajen sentezinin 1 numaralı sitokini = TGF-beta.
7. *Kollajen Değişimi:* Erken granülasyonda Tip III kollajen; olgun skarda gerilmeye dayanıklı Tip I kollajen; C vitamini hidroksilasyon için şarttır.
8. *Yara Kontraksiyonu:* Sekonder iyileşmede alfa-düz kas aktini içeren Miyofibroblastlar yara alanını büzüştürür.
9. *Yara Gücü:* 1. haftada dikişler alındığında sağlam derinin %10'u; 3. ayda maksimum %70-80 (asla %100 olmaz).
10. *Hipertrofik Skar vs Keloid:* Hipertrofik skar yara sınırlarında kalır; Keloid yara sınırlarını taşar, zenci ırkta sıktır ve cerrahiyle nükseder.""",
        [
            {"type": "clinical", "badge": "🔴 ALTIN ÖZET", "text": "Klinikte yara açılmasını önlemek için 1. haftada gerilme gücünün sadece %10 olduğunu unutmamak; TGF-beta'nın aşırı aktivitesinin keloid ve organ fibrozisine yol açtığını bilmek esastır.", "color": "rose"},
            {"type": "exam", "badge": "🔵 SINAV ŞAMPİYONU", "text": "Bu slaytta özetlenen 10 altın kural doku onarımı konusundaki tüm sınav sorularını eksiksiz çözdürür.", "color": "sky"}
        ],
        {
            "id": "prac-rep-012",
            "question": "Aşağıdaki ifadelerden hangisi yara iyileşmesi ve doku onarımı patolojisi ile ilgili olarak yanlıştır?",
            "options": [
                "A) Granülasyon dokusunda erken dönemde Tip III kollajen baskındır",
                "B) İyileşen bir yaranın mekanik gerilme gücü 1 yıl sonra sağlam derinin %100'üne ulaşır",
                "C) Doku onarımında kollajen sentezini en güçlü uyaran sitokin TGF-beta'dır",
                "D) Sekonder yara iyileşmesinde yara kontraksiyonunu miyofibroblastlar sağlar",
                "E) C vitamini eksikliğinde kollajen prolin hidroksilasyonu bozulur"
            ],
            "correctAnswer": 1,
            "explanation": "İyileşen bir yaranın gerilme direnci hiçbir zaman orijinal sağlam derinin %100'üne ulaşamaz; en fazla %70-80 seviyesinde platoya ulaşır."
        }
    )
]

print("Doku Onarımı 12 slayt hazırlandı.")

# Güncelleme: Her iki güverteyi 24'er slaytlık zengin formatla kaydet
target_aging = 'learn-hucresel-yaslanma-ve-hucr'
target_repair = 'learn-doku-onarimi-yara-iyilesmesi'

for d in decks:
    if d.get('id') == target_aging:
        d['title'] = "Hücresel Yaşlanma Mekanizmaları ve Oksidatif Hasar"
        d['shortTitle'] = "Hücresel Yaşlanma Patolojisi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Replikatif yaşlanma (Hayflick limiti), Telomer biyolojisi (TTAGGG, Shelterin, TERT), DNA onarım defektleri (Werner, Progeria), Oksidatif stres (ROS, lipofuskin), Mitokondriyal apoptoz (Sitokrom c, Apaf-1, Kaspaz 9/3, Bax/Bak), Proteostazis bozulması, Besin algılama (IGF-1/mTOR vs Sirtuin/AMPK) ve Inflammaging (SASP)."
        d['slides'] = aging_slides
        print(f"'{target_aging}' güvertesi güncellendi.")
    elif d.get('id') == target_repair:
        d['title'] = "Doku Onarımı, Yara İyileşmesi ve Skar Patolojisi"
        d['shortTitle'] = "Doku Onarımı ve Yara İyileşmesi"
        d['discipline'] = "Tıbbi Patoloji"
        d['committee'] = "Kurul 1"
        d['summary'] = "Rejenerasyon vs Skarlaşma, Doku proliferasyon kapasitesi (Labil, Stabil, Kalıcı), Karaciğer rejenerasyonu (IL-6/TNF priming, HGF/TGF-alfa), Skarla onarımın 4 evresi, Granülasyon dokusu ve anjiyogenez (VEGF, Ang-1), Büyüme faktörleri (TGF-beta), Kollajen tipleri (Tip III'ten Tip I'e, C vitamini), Primer vs Sekonder iyileşme (Miyofibroblast kontraksiyonu), Yara gücü dinamikleri (%10'dan %80'e) ve Hipertrofik skar vs Keloid ayrımı."
        d['slides'] = repair_slides
        print(f"'{target_repair}' güvertesi güncellendi.")

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print("İki güverte başarıyla güncellendi.")
