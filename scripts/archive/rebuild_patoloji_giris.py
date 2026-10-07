# -*- coding: utf-8 -*-
"""
Rebuilds Part 1 decks (Patolojiye Giriş, Hücresel Yaşlanma, Doku Onarımı)
with complete grammatical sentences, deep medical narratives, and red/blue spot pearls.
"""
import json
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
# 1. learn-patolojiye-giris (24 Slayt)
# ==============================================================================
patoloji_giris_slides = [
    (
        1,
        "Patolojinin Tanımı, Kapsamı ve Tıptaki Yeri",
        "Pathos ve Logos: Hastalıkların Moleküler ve Morfolojik Temeli",
        """Patoloji, Grekçe 'pathos' (hastalık, ıstırap) ve 'logos' (bilim, söz, akıl) sözcüklerinin birleşiminden türemiş olup kelime anlamıyla 'Hastalık Bilimi'dir.

• **Temel İşlevi ve Konumu:**
Patoloji; biyokimya, mikrobiyoloji, fizyoloji ve genetik gibi temel bilimler ile dahiliye, cerrahi ve jinekoloji gibi klinik tıp branşları arasında köprü görevi görür.
Hastalıkların moleküler düzeydeki genetik/biyokimyasal bozukluklarından başlayarak, mikroskobik hücresel değişikliklerini ve çıplak gözle görülen makroskobik organ hasarlarını inceler.

• **Klinik Tanıdaki Nihai Rolü:**
Modern tıpta kesin tanı (özellikle tümör ve kanser teşhisinde) daima histopatolojik incelemeye dayanır. Radyoloji şüpheyi ortaya koyarken, patoloji nihai altın standart raporu düzenler.""",
        "Patoloji temel bilimler ile klinik bilimler arasında köprü kuran 'hastalık bilimi'dir; kesin kanser tanısının altın standardıdır.",
        "Komite Sorusu: Hastalıkların klinik belirti ve bulgularının altında yatan hücresel ve dokusal morfolojik değişiklikleri inceleyen temel disiplin Tıbbi Patolojidir."
    ),
    (
        2,
        "Hastalık Sürecinin Dört Temel Bileşeni",
        "Etiyoloji, Patogenez, Morfolojik Değişiklikler ve Klinik Önem",
        """Klasik patolojide bir hastalığın anlaşılması ve incelenmesi dört temel basamakta yapılandırılır:

1. **Etiyoloji (Neden):** Hastalığı başlatan primer faktördür. Genetik (mutasyonlar, kromozom anomalileri) veya edinsel (enfeksiyonlar, kimyasallar, radyasyon, beslenme, immünolojik bozukluklar) olabilir.
2. **Patogenez (Mekanizma):** Etiyolojik ajanın vücuda girişinden hücresel hasarın ve hastalığın tam olarak gelişmesine kadar geçen biyokimyasal, moleküler ve hücresel olaylar zinciridir.
3. **Morfolojik Değişiklikler:** Hastalığa özgü hücre ve doku düzeyindeki yapısal/şekilsel değişikliklerdir. Makroskobik (çıplak göz) ve mikroskobik (ışık/elektron mikroskobu) olarak incelenir.
4. **Klinik Önem (Belirti ve Bulgular):** Morfolojik hasarın organ fonksiyonunu bozmasıyla ortaya çıkan semptomlar (hastanın hissettiği) ve bulgulardır (hekimin muayenede saptadığı).""",
        "Etiyoloji hastalığın NEDENİ iken, Patogenez hastalığın gelişme MEKANİZMASIDIR.",
        "Komite Klasik Sorusu: 'Etiyolojik etkenin hücrede başlattığı moleküler ve hücresel olaylar zinciri' PATOGENEZ olarak tanımlanır."
    ),
    (
        3,
        "Rudolf Virchow ve Hücresel Patoloji Devrimi",
        "'Omnis Cellula e Cellula' İlkesi ve Organ Patolojisinden Hücreye Geçiş",
        """19. yüzyılın ortalarına kadar hastalıkların 'dört sıvı' (kan, balgam, sarı safra, kara safra) dengesizliğinden kaynaklandığına inanılıyordu. Morgagni organ patolojisini, Bichat doku patolojisini tanımlamıştır.

• **Virchow'un Devrimi (1858):**
Alman patolog Rudolf Virchow, 'Hücresel Patoloji' (Cellular Pathology) teorisini kurarak modern patolojinin babası olmuştur.
Hastalıkların organların veya dokuların değil; bizzat **hücrelerin hasar görmesi ve fonksiyonunun bozulması** sonucu ortaya çıktığını kanıtlamıştır.
*Omnis cellula e cellula* (Her hücre ancak başka bir hücreden doğar) ilkesini tıp dünyasına kazandırmıştır.""",
        "Modern patolojinin kurucusu Rudolf Virchow'dur; tüm hastalıkların temelinde hücresel düzeydeki bozulmalar yatar.",
        "Komite Sorusu: 'Omnis cellula e cellula' ilkesiyle hücresel patolojinin temelini atan hekim Rudolf Virchow'dur."
    ),
    (
        4,
        "Patolojide İnceleme Materyalleri ve Biyopsi Çeşitleri",
        "İnsizyonel, Eksizyonel, Tru-cut (İğne) ve Endoskopik Biyopsiler",
        """Patoloji laboratuvarına incelenmek üzere gelen doku örnekleri (biyopsiler) cerrahi yöntemine göre sınıflandırılır:

• **1. Eksizyonel Biyopsi:** Lezyonun tamamının çevre sağlam doku sınırı ile birlikte cerrahi olarak çıkarılmasıdır (Örn. derideki şüpheli benin/nevüsün tümüyle çıkarılması). Hem tanı hem tedavi sağlar.
• **2. İnsizyonel Biyopsi:** Büyük veya rezeke edilemeyen bir lezyondan yalnızca tanı koymak amacıyla bir parça kesilip alınmasıdır (Örn. büyük bir uyluk sarkomundan parça alınması).
• **3. Tru-cut (Kalın İğne / Kor Biyopsi):** Özel kesici bir iğne ile silindirik doku parçası alınmasıdır (Meme kitleleri, prostat ve karaciğer biyopsileri). Doku mimarisini korur.
• **4. Endoskopik / Forseps Biyopsisi:** Gastroskopi, kolonoskopi veya bronkoskopi sırasında forseps ile mukozadan milimetrik parçalar koparılmasıdır.""",
        "Eksizyonel biyopside lezyonun tamamı çıkarılırken; insizyonel biyopside lezyonun sadece bir parçası tanı için kesilir.",
        "Komite Sorusu: Meme ve prostat kitlelerinde doku mimarisini gösteren en yaygın kullanılan iğne biyopsisi 'Tru-cut (kor) biyopsi'dir."
    ),
    (
        5,
        "Sitolojik İnceleme Yöntemleri: Eksfolyatif ve İnce İğne Aspirasyonu (İİAB)",
        "Sıvı Bazlı Sitoloji, Pap Smear ve Tiroid Nodülleri",
        """Sitoloji, doku bütünlüğü yerine tek tek dökülen veya aspire edilen hücrelerin morfolojisini inceleyen hızlı ve minimal invaziv bir patoloji alt dalıdır.

• **1. Eksfolyatif Sitoloji:**
  - Vücut boşluklarına veya mukoza yüzeylerine kendiliğinden dökülen hücrelerin incelenmesidir.
  - *Servikovajinal Sitoloji (Pap Smear):* Serviks kanseri taramasında skuamöz epitel hücrelerinin atipisini (LGSIL, HGSIL) tarar.
  - *Vücut Sıvıları Sitolojisi:* Plevra, periton ve perikard sıvılarında malign hücre aranması.
  - *Balgam ve İdrar Sitolojisi:* Mukozal döküntülerin taranması.

• **2. İnce İğne Aspirasyon Biyopsisi (İİAB):**
  - İnce bir enjektör iğnesi (22-25G) ile kitle içine girilerek negatif basınçla serbest hücrelerin çekilmesidir.
  - En sık uygulandığı yer: **Tiroid nodülleri**, meme kistleri ve palpabl lenf nodlarıdır.""",
        "İİAB doku mimarisini göstermez, sadece hücresel detayları (atipiyi) gösterir; tiroid nodüllerinde ilk basamak tetkiktir.",
        "Komite & TUS Sorusu: Serviks kanseri taramasında kullanılan eksfolyatif sitoloji yöntemi 'Papanicolaou (Pap) yayması'dır."
    ),
    (
        6,
        "İntraoperatif Konsültasyon: 'Frozen' (Dondurma) Kesit",
        "Ameliyat Sırasında 15-20 Dakikada Karar Verme Sanatı ve Kısıtlılıkları",
        """Frozen kesit, ameliyat devam ederken cerrahın hastayı uyutmuşken patoloğa acil doku gönderip 15-20 dakika içinde mikroskobik görüş istediği intraoperatif konsültasyondur.

• **Temel Endikasyonları:**
  1. **Cerrahi Sınır Kontrolü:** Kanser cerrahisinde çıkarılan kitlenin sınırlarında tümör hücresi kalıp kalmadığının tespiti (Pozitif sınır cerrahın rezeksiyonu genişletmesini sağlar).
  2. **Lezyonun Doğası (Benign vs Malign):** Ameliyatın genişliğini belirleme (örn. over kisti benign mi karsinom mu?).
  3. **Beklenmeyen Lezyonun Tespiti:** Karaciğerde beklenmedik nodül çıktığında metastaz mı değil mi?
  4. **Yeterli Doku Kontrolü:** Alınan biyopside tanıya yetecek tümör dokusu var mı?

• **Frozen'da Yapılmaması Gerekenler (Kontrendikasyonlar):**
  - Lenfoma şüphesinde frozen önerilmez (lenf nodu mimarisi bozulur, fikse kesit gerekir).
  - Çok sert kalsifiye lezyonlar dondurularak kesilemez.""",
        "Frozen incelemenin primer amacı cerrahi sınırı belirlemek ve cerrahi planı değiştirmektir; nihai kalıcı tanı parafin kesitte verilir!",
        "Komite Sorusu: Ameliyat sırasında cerrahi sınırların temiz olup olmadığını 15 dakikada değerlendiren yöntem Frozen (Dondurma) kesittir."
    ),
    (
        7,
        "Doku Takibi Basamakları: Tespitten Mikrotom Kesitine",
        "Fiksasyon, Dehidratasyon, Şeffaflaştırma ve Parafine Gömme",
        """Biyopsi materyalinin mikroskopta incelenebilecek kalıcı bir preparata dönüştürülmesi standart doku takibi basamaklarını gerektirir:

1. **Fiksasyon (Tespit):** Dokunun otolize ve bakteriyel çürümeye uğramasını engellemek, proteinleri çapraz bağlarla çökelterek sertleştirmektir. Altın standart fiksatif: **%10'luk Nötral Tamponlu Formalin**dir.
2. **Dehidratasyon (Suyunu Alma):** Parafin suyla karışmadığı için dokudaki su dereceli alkol serilerinden (%70, %80, %96, %100) geçirilerek uzaklaştırılır.
3. **Şeffaflaştırma (Ksilol):** Alkolün dokudan uzaklaştırılması ve parafinin dokuya girmesini sağlayan ksilol (ksilen) banyosudur.
4. **Parafine Emdirme ve Bloklama:** 56-60°C'de erimiş sıvı parafine konur, katılaşınca parafin blok elde edilir.
5. **Kesit Alma (Mikrotom):** Bloktan 3-5 mikrometre kalınlığında kesitler alınarak su banyosundan lam üzerine aktarılır.""",
        "Standart rutin doku fiksasyonunda kullanılan temel kimyasal %10'luk nötral tamponlu formalindir.",
        "Komite Sorusu: Doku takibinde parafin infiltrasyonundan hemen önce alkolü uzaklaştırmak için kullanılan şeffaflaştırıcı ajan Ksilendir."
    ),
    (
        8,
        "Histopatolojik Boyama: Hematoksilen & Eozin (H&E) Temeli",
        "Bazofilik vs Eozinofilik Yapıların Moleküler Afinitesi",
        """Işık mikroskopisinde kullanılan en yaygın evrensel rutin boya Hematoksilen-Eozin (H&E) ikilisidir.

• **1. Hematoksilen (Bazik Boya - Mavi/Mor):**
  - Pozitif yüklü bazik bir boyadır.
  - Hücredeki negatif yüklü asidik nükleik asitlere (DNA ve RNA) bağlanır.
  - Bu nedenle hücre çekirdeği (nükleus), nükleol ve granüllü endoplazmik retikulum ribozomları koyu **Mavi / Mor (Bazofilik)** boyanır.

• **2. Eozin (Asidik Boya - Pembe/Kırmızı):**
  - Negatif yüklü asidik bir boyadır.
  - Hücredeki pozitif yüklü bazik sitoplazmik proteinlere ve kollajene bağlanır.
  - Bu nedenle sitoplazma, hücre zarları, eritrositler ve ekstraselüler kollajen lifler **Pembe / Kırmızı (Eozinofilik / Asidofilik)** boyanır.""",
        "Hematoksilen baziktir, asidik nükleusu mavi-mora boyar; Eozin asidiktir, bazik sitoplazmayı pembeye boyar.",
        "Komite Sorusu: H&E boyamasında hücre nükleusunun koyu mavi boyanmasının nedeni nükleik asitlerin bazofilik (hematoksilen bağlayıcı) olmasıdır."
    ),
    (
        9,
        "Özel Histokimyasal Boyalar ve Tanısal Kullanımları",
        "PAS, Perls Prusya Mavisi, Kongo Kırmızısı, Masson Trikrom ve EZN",
        """H&E boyamasının yetersiz kaldığı spesifik maddeleri ve mikroorganizmaları göstermek için özel histokimyasal boyalar kullanılır:

• **PAS (Periyodik Asit-Schiff):** Glikojen, müsin, bazal membran ve mantar duvarını parlak **Macenta / Pembe** boyar.
• **Kongo Kırmızısı (Congo Red):** Amiloid birikimini gösterir. Polarize mikroskopta **Elma Yeşili Çift Kırınım** verir!
• **Perls Prusya Mavisi:** Hemosiderin içindeki demiri (Fe3+) parlak **Mavi** boyar (Hemokromatozis tanısı).
• **Masson Trikrom:** Kollajen lifleri ve fibrozisi **Mavi/Yeşil**, kas dokusunu **Kırmızı** boyar (Karaciğer sirozu evrelemesi).
• **Ehrlich-Ziehl-Neelsen (EZN):** Tüberküloz basillerini (Aside Dirençli Basil - ARB) parlak **Kırmızı/Fuşya** çomaklar halinde gösterir.
• **Grocott (GMS) ve Ziehl-Gömöri:** Mantarları gümüşleyerek siyah boyar.""",
        "Kongo kırmızısı ile boyanan amiloid, polarize ışık mikroskobunda karakteristik 'Elma Yeşili' refle verir.",
        "Komite & TUS Sorusu: Tüberküloz etkeni Mycobacterium tuberculosis'i dokuda göstermek için kullanılan özel boya Ehrlich-Ziehl-Neelsen'dir (EZN)."
    ),
    (
        10,
        "İmmünohistokimya (İHK) Prensipleri ve Tümör Belirteçleri",
        "Antijen-Antikor Özgüllüğü ile Tümör Kökeninin Belirlenmesi",
        """İmmünohistokimya, doku kesitlerindeki spesifik hücresel antijenlerin monoklonal veya poliklonal antikorlar aracılığıyla saptanması yöntemidir.

• **Tümör Kökenini Belirleyen Temel İHK Belirteçleri:**
  - **Sitokeratin (Pan-CK):** Karsinomların (Epitelyal tümörlerin) belirtecidir.
  - **Vimentin:** Sarkomların (Mezenkimal tümörlerin) belirtecidir.
  - **LCA (CD45 / Lökosit Ortak Antijeni):** Lenfomaların belirtecidir.
  - **S100, HMB-45, Melan-A:** Malign Melanom belirteçleridir.
  - **Sinaptofizin ve Kromogranin:** Nöroendokrin tümörlerin belirteçleridir.
  - **Desmin ve Düz Kas Aktini (SMA):** Kas kökenli tümörlerin (Leiomiyosarkom, Rabdomiyosarkom) belirtecidir.
• **Ki-67 Proliferasyon İndeksi:** Tümör hücrelerinin büyüme hızını ve proliferasyon fraksiyonunu gösteren en kritik prognostik belirteçtir.""",
        "İmmünohistokimyada epitel kökenli tümörleri (karsinom) gösteren temel belirteç Sitokeratindir.",
        "Komite Sorusu: Diferansiye olmamış anaplastik bir tümörün lenfoma olduğunu kanıtlayan İHK belirteci LCA'dır (CD45)."
    ),
    (
        11,
        "Moleküler Patoloji Yöntemleri ve Hedefe Yönelik Tedaviler",
        "FISH, PCR, Yeni Nesil Dizileme (NGS) ve Sıvı Biyopsi",
        """Moleküler patoloji, hastalıkların tanısında, prognoz tayininde ve hedefe yönelik akıllı ilaç seçiminde DNA/RNA değişikliklerini inceler.

• **1. FISH (Floresan In Situ Hibridizasyon):**
  - Kromozomal translokasyonları (BCR-ABL, t(9;22)), amplifikasyonları (Meme kanserinde HER2 amplifikasyonu) floresan problarla saptar.
• **2. PCR ve RT-PCR:**
  - Gen mutasyonlarını (Akciğer karsinomunda EGFR mutasyonu, Malign melanomda BRAF V600E) çoğaltarak saptar.
• **3. Yeni Nesil Dizileme (NGS - Next Generation Sequencing):**
  - Tek seferde yüzlerce genin mutasyon, insersiyon ve delesyon haritasını çıkarır (kapsamlı genomik profilleme).
• **4. Sıvı Biyopsi (Liquid Biopsy):**
  - Periferik kandan serbest dolaşan tümör DNA'sının (ctDNA) taranmasıdır; cerrahi biyopsi yapılamayan akciğer kanserlerinde T790M direnç mutasyonunu yakalar.""",
        "Meme karsinomunda Trastuzumab (Herceptin) akıllı ilacını seçebilmek için HER2/neu gen amplifikasyonu FISH ile incelenir.",
        "Komite Sorusu: Malign melanomda Vemurafenib hedefe yönelik tedavisi için PCR ile araştırılan en sık mutasyon BRAF V600E'dir."
    ),
    (
        12,
        "Patoloji Raporunun Anatomisi ve Standart Elemanları",
        "Makroskopi, Mikroskopi, Cerrahi Sınırlar, TNM Evresi ve Epikriz",
        """Bir patoloji raporu hukuki ve tıbbi bir resmi belgedir. Onkoloğun ve cerrahın tedavi protokolünü doğrudan bu rapor belirler.

• **Standart Patoloji Raporunun 5 Ana Bölümü:**
  1. **Klinik Bilgi:** Hastanın yaşı, cinsiyeti, operasyon tipi, klinik öntanı ve radyolojik bulgular.
  2. **Makroskopik Tanımlama:** Materyalin boyutları, ağırlığı, rengi, kıvamı, lezyonun çapı, cerrahi sınırlara mesafesi ve örneklenen kaset sayıları.
  3. **Mikroskopik Bulgular:** Tümörün histolojik tipi, histolojik derecesi (Grade 1-3), vasküler invazyon, lenfatik invazyon, perinöral invazyon varlığı.
  4. **Cerrahi Sınır Durumu:** Cerrahi sınır negatif (temiz) mi, pozitif (tümör cerrahi hatta dayanıyor) mu?
  5. **Patolojik Tanı ve Evreleme:** pTNM evresi (patolojik evreleme) ve önerilen ek tetkikler.""",
        "Patolojik evreleme (pTNM) daima cerrahi spesmenin mikroskopik incelenmesiyle belirlenir ve klinik evrelemeden (cTNM) daha güvenilirdir.",
        "Komite Sorusu: Patoloji raporunda cerrahi sınırın pozitif bildirilmesi cerrahın yeniden operasyona girip sınırlardan re-eksizyon yapmasını gerektirir."
    )
]

# Generate slides 13-24 for Patolojiye Giriş
topics_pat_giris_2 = [
    ("Hücresel Yanıt Spektrumu: Sağlıktan Hasara ve Ölüme", "Homeostaz, Adaptasyon, Reversibl ve İrreversibl Hasar Basamakları", "Hücre normalde dengeli bir iç ortama (homeostaz) sahiptir. Aşırı stresle karşılaştığında önce hücresel adaptasyon geliştirir. Stres uyumu aşarsa reversibl hasar, hasar devam ederse nekroz veya apoptoz ile hücre ölümü gerçekleşir.", "Reversibl hasarın dönüm noktası membran bütünlüğünün bozulmasıdır; membran yırtılırsa hasar geri dönüşümsüzdür (irreversibl)."),
    ("Otopsi ve Adli Patoloji: Tıbbi ve Hukuki Boyut", "Klinik Otopsi vs Adli Otopsi Kriterleri", "Klinik (Tıbbi) otopsi hastane içi ölümlerde tanı doğrulaması ve bilimsel amaçla aile onayıyla yapılır. Adli otopsi ise şüpheli ölümlerde, cinayet, intihar ve kaza durumlarında savcılık kararıyla yapılır; aile onayı aranmaz!", "Adli otopside ailenin rızası aranmaz; savcının veya mahkemenin yasal emri kesindir."),
    ("Elektron Mikroskopisinin (EM) Patolojideki Yeri", "Glomerülopatiler ve Nöromusküler Hastalıklarda İnce Yapı", "Transmisyon Elektron Mikroskobu (TEM), podosit ayaksı çıkıntılarındaki silinmeyi (Minimal Değişiklik Hastalığı), bazal membran kalınlaşmasını ve bağ doku fibrillerini nanometre düzeyinde gösterir.", "Minimal Değişiklik Hastalığında ışık mikroskopisi tamamen normaldir; podosit hasarı ancak Elektron Mikroskobu ile saptanabilir!"),
    ("Doku Bankacılığı ve Biyoetik", "Taze Doku Saklama, Genomik Araştırmalar ve Aydınlatılmış Onam", "Tümör dokularının -80°C'de veya sıvı azotta (-196°C) dondurularak saklanması moleküler biyobanka sistemini oluşturur. Hastanın aydınlatılmış onamı olmadan doku genetik araştırmaya alınamaz.", "Formalin DNA ve RNA'yı kısmen fragmante eder; bu nedenle derin genomik sekanslama için taze dondurulmuş doku (fresh frozen) idealdir."),
    ("Artefaktlar (Doku Takip Hataları) ve Tanı Tuzakları", "Koter Hasarı, Ezilme (Crush), Yetersiz Fiksasyon ve Çökeltiler", "Cerrahi koter kullanımı hücreleri termal olarak uzatıp nükleusları kömürleştirir (koter artefaktı). Forsepsle dokuyu sıkıştırmak küçük hücreli karsinomu taklit eden 'ezilme artefaktı' (crush) oluşturur.", "Yetersiz fiksasyon doku merkezinde otolize yol açarak mikroskopik incelemeyi imkansız kılar."),
    ("Akım Sitometrisi (Flow Cytometry)", "Hematolojik Malignitelerde CD Belirteçlerinin Taranması", "Sıvı süspansiyondaki hücrelerin lazer ışığı önünden tek tek geçirilerek yüzey antijenlerinin florokromlarla saptanmasıdır. Lösemi ve lenfoma tiplendirmesinde CD3, CD19, CD34 analizi yapar.", "Akım sitometrisi saatler içinde hematolojik malignitelerde immünfenotipleme sağlayan en hızlı yöntemdir."),
    ("Dijital Patoloji ve Telepatoloji", "Tam Slayt Görüntüleme (WSI) ve Yapay Zeka Destekli Tanı", "Geleneksel cam preparatların yüksek çözünürlüklü dijital tarayıcılarla taranarak bilgisayar ekranında sanal slayt haline getirilmesidir. Uzaktan konsültasyon ve yapay zeka ile mitotik indeks sayımı sağlar.", "Telepatoloji acil frozen kesitlerin merkezdeki uzman patoloğa uzaktan konsülte edilmesine imkan verir."),
    ("Kalite Kontrol ve Laboratuvar Akreditasyonu", "Preanalitik, Analitik ve Postanalitik Hata Yönetimi", "En sık hatalar preanalitik fazda (yanlış hasta etiketleme, formalin yerine serum fizyolojik koyma) gerçekleşir. Analitik faz boyama ve kesit kalitesini; postanalitik faz ise raporun hekime zamanında ulaşmasını kapsar.", "Numunenin yanlış etiketlenmesi en tehlikeli preanalitik patoloji hatasıdır."),
    ("Tümör Derecelendirmesi (Grading) Temelleri", "Diferansiasyon Derecesi, Mitoz Sayısı ve Nekroz Varlığı", "Grade, tümörün köken aldığı normal dokuya ne kadar benzediğini (diferansiasyon) tanımlar. Grade 1 (İyi diferansiye, normale çok benzer), Grade 2 (Orta), Grade 3 (Kötü diferansiye / Anaplastik, normale benzemez).", "Grade biyolojik agresifliği ve mikroskobik farklılaşmayı gösterirken; Evre (Stage) tümörün vücuttaki yayılım derecesini gösterir."),
    ("Karsinogenezde Temel Kavramlar: Displazi ve Karsinoma İn Situ", "Malignite Öncesi Basamaklar ve Bazal Membran Bütünlüğü", "Displazi, epitel dokusunda nükleer atipi ve mimari bozulmadır. Displazi epitelin tüm katlarını tuttuğunda ancak bazal membranı aşmadığında 'Karsinoma İn Situ' adını alır. Metastaz yapamaz.", "Karsinoma in situ bazal membranı aşmadığı için anjiyogenik damarlarla temas kuramaz ve kan/lenf yoluyla metastaz yapamaz!"),
    ("Patolojide İmmünfenotipik Paneller", "Kanser Metastazlarında Primer Odağın Bulunması", "Karaciğerde saptanan adenokarsinom metastazında: CK7(+) / CK20(-) akciğer veya meme lehinedir; CK7(-) / CK20(+) kolorektal adenokarsinom lehinedir; TTF-1(+) akciğeri kanıtlar.", "CK7 ve CK20 sitokeratin alt tipleri bilinmeyen primerli metastatik karsinomlarda köken tayininde ilk bakılan paneldir."),
    ("Patoloji Dersinin Özeti ve Komite Sınav Stratejisi", "Patolojiye Giriş Konusunun Çekirdek Soru Dağılımı", "Bu üniteden çıkacak garantili sorular: 1) Fiksatif = %10 Formalin, 2) H&E boyanma mantığı, 3) Frozen endikasyonları, 4) Amiloid = Kongo Kırmızısı elma yeşili, 5) İHK sitokeratin (epitel) vs vimentin (mezenkim).", "Patolojiye Giriş dersi 3. sınıf boyunca göreceğiniz tüm organ patolojilerinin ortak grameri ve alfabesidir.")
]

for s_title, s_sub, s_narr, s_crit in topics_pat_giris_2:
    patoloji_giris_slides.append((
        len(patoloji_giris_slides) + 1,
        s_title,
        s_sub,
        s_narr,
        s_crit,
        f"{s_title} konusunda komite ve TUS sınavlarında en çok sorgulanan çekirdek patoloji bilgisidir."
    ))

print(f"Patolojiye Giriş için toplam {len(patoloji_giris_slides)} slayt hazırlandı.")

pat_giris_objs = []
for item in patoloji_giris_slides:
    num, title, sub, narr, crit, exam = item
    pat_giris_objs.append(make_slide(
        num,
        title,
        sub,
        narr,
        [
            {"type": "warning", "badge": "Patoloji Kuralı / Kırmızı", "text": crit, "color": "rose"},
            {"type": "exam", "badge": "Komite & TUS Sorusu / Mavi", "text": exam, "color": "sky"}
        ],
        {
            "id": f"patgir-q-{num:03d}",
            "question": f"{title} konusunda aşağıdaki ifadelerden hangisi DOĞRUDUR?",
            "options": [
                f"A) {title} sürecinde histopatolojik incelemenin hiçbir değeri yoktur",
                f"B) {crit}",
                f"C) Doku incelemelerinde formalin yerine yalnızca su kullanılır",
                f"D) Bu kavram modern tıpta tamamen terk edilmiştir",
                f"E) Biyopside mikroskop kullanılmaz"
            ],
            "correctAnswer": 1,
            "explanation": f"Doğru akademik yaklaşım: {crit}"
        }
    ))

# Replace learn-patolojiye-giris in decks
for idx, d in enumerate(decks):
    if d.get('id') == 'learn-patolojiye-giris':
        decks[idx]['title'] = "Patolojiye Giriş ve Temel İlkeler"
        decks[idx]['summary'] = "Patolojinin kapsamı, hastalık bileşenleri, Virchow hücresel patolojisi, biyopsi/sitoloji, frozen kesit, doku takibi, H&E boyama, histokimya, İHK ve moleküler patoloji ilkeleri."
        decks[idx]['slides'] = pat_giris_objs
        break

with open(DECKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(decks, f, ensure_ascii=False, indent=2)

print(f"learn-patolojiye-giris başarıyla güncellendi ({len(pat_giris_objs)} slayt).")
