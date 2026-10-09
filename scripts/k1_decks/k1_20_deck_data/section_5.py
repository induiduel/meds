# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_5_slides():
    slides = []

    # Slide 41
    slides.append({
        "id": "k1-20-s41",
        "title": "Rudolf Virchow (1856) ve Trombozun Üç Sacayağı (Virchow Triadı)",
        "content": "Modern patolojinin kurucusu Rudolf Virchow, 1856 yılında damar içi pıhtı oluşumunu yöneten üç temel anormalliği tanımlamıştır (Sınav Spotu):\n\n- **Virchow Üçlüsü (Virchow's Triad):** İntravasküler trombozun patogenezinde rol oynayan üç ana sacayağıdır:\n  1. **Endotel Hasarı veya Disfonksiyonu:** Damar duvarının yapısal veya fonksiyonel bozulmasıdır (özellikle arteriyel ve kardiyak trombozda en kritik etken).\n  2. **Anormal Kan Akımı:** Normal laminer akımın bozulması; ya **kan akımının yavaşlaması/duraklaması (Staz)** ya da kaotik girdapların oluşması (**Türbülans**).\n  3. **Hiperkoagülabilite (Trombofili):** Kanın pıhtılaşma eğiliminin artması; ya primer (kalıtsal) ya da sekonder (edinsel) nedenlere bağlıdır (özellikle venöz trombozda en kritik etken).\n- **Kombinasyon Kuralı:** Çoğu klinik tromboz vakasında bu üç faktörden birden fazlası aynı anda bulunur ve birbirini tetikler.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Arteriyel Tromboz Zirvesi vs Venöz Tromboz Zirvesi",
                "Arteriyel Tromboz (Endotel Hasarı)",
                "Yüksek akım hızında endotel hasarı ve türbülans baskındır; aterosklerotik plak yırtılması tipiktir.",
                "Venöz Tromboz (Staz ve Hiperkoagülabilite)",
                "Düşük akım hızında staz ve kanın pıhtılaşma eğilimi (hiperkoagülabilite) baskındır; DVT tipiktir."
            ),
            make_cloze(
                "Damar içi tromboz patogenezini açıklayan Virchow üçlüsünün üç bileşeni endotel hasarı, anormal kan akımı ve hiperkoagülabilitedir.",
                "hiperkoagülabilitedir",
                "Kanın anormal pıhtılaşma eğilimini ifade eden Virchow üçlüsü bileşeni"
            )
        ]
    })

    # Slide 42
    slides.append({
        "id": "k1-20-s42",
        "title": "Endotelin Çift Yüzü: Normal Antitrombotik Koruma",
        "content": "Sağlıklı bir damar endoteli, kanın sıvı kalmasını sağlayan son derece aktif bir biyolojik kalkan oluşturur (Sınav Spotu):\n\n- **1. Antiplatelet Özellikler:**\n  - **Prostasiklin (PGI2) ve Nitrik Oksit (NO):** Endotelden sürekli salgılanır; trombositlerin endotel yüzeyine yapışmasını ve aktive olmasını güçlü şekilde engeller; ayrıca damarları gevşetir (vazodilatasyon).\n  - **Adenozin Difosfataz (ADPaz / CD39):** Trombositleri toplayan ADP moleküllerini parçalayarak adenozine çevirir ve agregasyon döngüsünü kırar.\n- **2. Antikoagülan Özellikler:**\n  - Endotel yüzeyindeki **Trombomodulin** ve **EPCR**, trombinle birleşerek Protein C'yi aktive eder.\n  - Endotel membranındaki **Heparan Sülfat**, Antitrombin III'ü (ATIII) aktive eder.\n  - Endotelden salgılanan **TFPI**, doku faktörü-Faktör VIIa kompleksini bloke eder.\n- **3. Fibrinolitik Özellik:**\n  - Endotel sürekli **t-PA (doku plazminojen aktivatörü)** sentezleyerek olası mikro-fibrin tortularını anında eritir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Endotelyal Antitrombotik Etki", "Sorumlu Moleküller", "Mekanizma"],
                [
                    ["Trombosit İnhibisyonu", "PGI2 (Prostasiklin), NO, CD39 (ADPaz)", "Trombosit adezyon ve agregasyonunu engelleme"],
                    ["Antikoagülan Kalkan", "Trombomodulin, Heparan sülfat, TFPI", "Trombin, Faktör Xa ve TF-VIIa'yı inaktive etme"],
                    ["Fibrinolitik Kalkan", "Doku Plazminojen Aktivatörü (t-PA)", "Plazminojeni plazmine çevirerek fibrini eritme"]
                ]
            ),
            make_quiz(
                "Sağlıklı endotel hücreleri tarafından sentezlenerek trombosit agregasyonunu engelleyen ve güçlü lokal vazodilatasyon sağlayan temel lipid ve gaz aracıları hangileridir?",
                [
                    {"key": "A", "text": "Prostasiklin (PGI2) ve Nitrik Oksit (NO)", "isCorrect": True, "explanation": "Doğru cevap A'dır: PGI2 ve NO endotelin en önemli antiplatelet ve vazodilatatör savunma molekülleridir."},
                    {"key": "B", "text": "Tromboksan A2 (TxA2) ve Endotelin", "isCorrect": False, "explanation": "TxA2 ve endotelin agregasyon ve vazokonstriksiyon yapar."},
                    {"key": "C", "text": "Fibrinojen ve Faktör V", "isCorrect": False, "explanation": "Pıhtılaşma faktörleridir."},
                    {"key": "D", "text": "PAI-1 ve Doku Faktörü", "isCorrect": False, "explanation": "Protrombotik mediyatörlerdir."}
                ]
            )
        ]
    })

    # Slide 43
    slides.append({
        "id": "k1-20-s43",
        "title": "Aktive Endotelin Protrombotik Dönüşümü",
        "content": "İnflamatuar sitokinlere, travmaya veya toksinlere maruz kalan endotel hücreleri gen ekspresyon profilini değiştirerek bir pıhtılaşma fabrikasına döner (Sınav Spotu):\n\n- **Endotel Aktivasyonu:** TNF-α, IL-1, bakteriyel endotoksinler (LPS), sigara dumanı ve hiperkolesterolemi endoteli 'aktive' eder.\n- **Protrombotik Değişiklikler:**\n  1. **Doku Faktörü (TF) Sentezi:** Normalde endotel yüzeyinde TF bulunmazken, aktive endotel yüzeyine yoğun şekilde Doku Faktörü sererek kaskadı doğrudan ateşler.\n  2. **Antikoagülanların Baskılanması:** Trombomodulin, EPCR ve heparan sülfat ekspresyonu belirgin şekilde azalır (antikoagülan frenler sökülür).\n  3. **Adezyon Moleküllerinin Açılması:** Weibel-Palade cisimciklerindeki **vWF** kana dökülür; **P-selektin, E-selektin, ICAM-1 ve VCAM-1** eksprese edilerek trombosit ve lökositler yakalanır.\n  4. **Antifibrinolitik Salgı:** Endotelden yüksek miktarda **PAI-1** salgılanarak t-PA bloke edilir ve fibrinoliz durdurulur.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Sakin Antitrombotik Endotel vs Aktive Protrombotik Endotel",
                "Sakin Endotel (Antitrombotik)",
                "PGI2, NO, trombomodulin, heparan sülfat ve t-PA salgılar; trombositler kayıp geçer.",
                "Aktive Endotel (Protrombotik)",
                "Doku faktörü serer, vWF döker, P-selektin açar ve PAI-1 salgılayarak pıhtıyı çağırır."
            ),
            make_cloze(
                "Aktive endotel hücreleri yüzeylerinde yoğun şekilde doku faktörü eksprese ederek ve PAI-1 salgılayarak protrombotik bir zemin oluşturur.",
                "doku faktörü",
                "Aktive endotelde ekstrinsik kaskadı başlatan subendotelyal ve endotelyal reseptör"
            )
        ]
    })

    # Slide 44
    slides.append({
        "id": "k1-20-s44",
        "title": "Endotel Hasarı: Arteriyel ve Kardiyak Trombozun Tetikleyicisi",
        "content": "Virchow üçlüsünün tartışmasız en dominant ve bağımsız bileşeni endotel hasarıdır (Sınav Spotu):\n\n- **Arteriyel Sistemde Zorunluluk:**\n  - Arterlerde ve sol ventrikülde kan çok yüksek basınç ve hızla akar; bu yüksek kayma gerilimi altında pıhtılaşmanın başlaması için **fiziksel bir endotel kaybı (denudasyon) veya şiddetli endotel hasarı neredeyse bir ön koşuldur**.\n  - Tek başına kanın yavaşlaması arteriyel tromboz yapmaya yetmez.\n- **Hasarın Başlattığı İki Yıkıcı Olay:**\n  1. **Subendotelyal Matriksin Açığa Çıkması:** Tip I/III kollajen ve vWF açığa çıkarak trombositlerin saniyeler içinde GpIb ile yapışmasını tetikler.\n  2. **Doku Faktörünün Kana Maruz Kalması:** Subendotelyal hücrelerin Doku Faktörü Faktör VIIa'yı bağlayarak devasa bir trombin patlaması başlatır.\n- **Sonuç:** Hasar bölgesinde trombositten zengin beyaz arteriyel trombüs hızla şekillenir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Endotel Hasarından Arteriyel Tromboza Akış",
                [
                    "1. Endotel Kaybı: Aterom plağı yırtılır veya endotel tabakası soyulur.",
                    "2. Matriks Teması: Subendotelyal kollajen, vWF ve Doku Faktörü açığa çıkar.",
                    "3. Trombosit Adezyonu: vWF-GpIb köprüsüyle trombositler hasara yapışır.",
                    "4. Agregasyon ve Kaskad: Fibrinojen ve trombin ile trombosit tıkacı sertleşir.",
                    "5. Arter Tıkanması: Büyüyen trombüs arter lümenini tıkayarak infarktüs yapar."
                ]
            ),
            make_quiz(
                "Kalp boşluklarında ve yüksek akımlı arteriyel dolaşımda trombüs oluşabilmesi için Virchow üçlüsünden hangisinin varlığı NEREDEYSE ZORUNLU BİR ÖN KOŞULDUR?",
                [
                    {"key": "A", "text": "Endotel hasarı veya denudasyonu", "isCorrect": True, "explanation": "Doğru cevap A'dır: Yüksek akımlı arterlerde ve ventriküllerde trombüs oluşabilmesi için endotel hasarı olmazsa olmaz birincil faktördür."},
                    {"key": "B", "text": "İzole kan stazı", "isCorrect": False, "explanation": "Staz tek başına arteriyel tromboza yol açmaz, venlerde etkilidir."},
                    {"key": "C", "text": "Faktör VIII eksikliği", "isCorrect": False, "explanation": "Bu durum kanama yapar."},
                    {"key": "D", "text": "Düşük hematokrit düzeyi", "isCorrect": False, "explanation": "Anemi tromboz ön koşulu değildir."}
                ]
            )
        ]
    })

    # Slide 45
    slides.append({
        "id": "k1-20-s45",
        "title": "Endotel Hasarının Nedenleri: Ateroskleroz, Sigara ve Sitokinler",
        "content": "Klinik pratikte endotel bütünlüğünü bozan en sık patolojik etkenler kronik vasküler risk faktörleridir (Sınav Spotu):\n\n- **1. Ülserleşmiş Aterosklerotik Plaklar (En Sık Neden):**\n  - Aterosklerozda koroner, serebral ve femoral arterlerin intiması lipid ve nekrotik debrisle dolar.\n  - Fibröz başlığın yırtılması (plak rüptürü) veya yüzeyel erozyonu, nekrotik kitleyi ve yoğun Doku Faktörünü kan akımına sunarak **akut miyokard enfarktüsü veya inme trombüsünü** anında tetikler.\n- **2. Hemodinamik Stres (Hipertansiyon):** Yüksek tansiyon damar dallanma noktalarında endotelde mekanik yıpranmaya ve mikro-erozyonlara yol açar.\n- **3. Biyokimyasal ve Toksik Toksisite:**\n  - **Sigara dumanındaki toksinler:** Endotel NO sentezini baskılar ve oksidatif hasar yapar.\n  - **Hiperkolesterolemi (Ox-LDL):** Endotel hücrelerinde apoptozisi uyarır.\n  - **Homosistein yüksekliği:** Endotelyal toksisite yaratan amino asit metabolitidir.\n- **4. Vaskülit ve İnfeksiyonlar:** Damar duvarı iltihapları endoteli doğrudan nekroza uğratır.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hasar Nedeni", "Mekanizma", "En Sık Görüldüğü Klinik Tablo"],
                [
                    ["Aterom Plak Rüptürü", "Kollajen ve nekrotik doku faktörünün açığa çıkması", "Akut Koroner Sendrom (Miyokard Enfarktüsü)"],
                    ["Kronik Hipertansiyon", "Kayma gerilimi ve mekanik mikroyırtıklar", "Laküner inme ve aort anevrizması trombozu"],
                    ["Sigara ve Toksinler", "Oksidatif stres, NO kaybı ve endotel disfonksiyonu", "Periferik arter hastalığı ve erken koroner tromboz"],
                    ["Vaskülit (Damar İltihabı)", "İmmün kompleks ve nötrofil kaynaklı nekroz", "Kawasakide koroner tromboz, poliarteritis nodosa"]
                ]
            ),
            make_cloze(
                "Arteriyel sistemde endotel hasarına yol açarak akut miyokard enfarktüsü trombozunu tetikleyen en sık patolojik lezyon ülserleşmiş aterosklerotik plak yırtılmasıdır.",
                "aterosklerotik plak",
                "Damar intimasında lipid çekirdeği örten fibröz yapının rüptürü"
            )
        ]
    })

    # Slide 46
    slides.append({
        "id": "k1-20-s46",
        "title": "Anormal Kan Akımı I: Türbülans ve Girdap Oluşumu",
        "content": "Normal damarlarda kan laminer (katmanlı) olarak akar; hücresel elemanlar lümenin merkezinde, endotel yüzeyinde ise ince bir plazma tabakası akar. Bu akış bozulduğunda tromboz kaçınılmazdır (Sınav Spotu):\n\n- **Türbülansın Biyomekaniği:**\n  - Kanın düzensiz, kaotik ve girdaplar (eddy akımları) çizerek akmasıdır.\n  - Akımın doğrusal hız vektörleri bozulur; kan elemanları damar duvarına dik açılarla çarpmaya başlar.\n- **Türbülansın Tromboza Katkısı:**\n  1. **Endotel Hasarı Yaratır:** Girdaplar endotel hücrelerini mekanik olarak hırpalar ve mikro-denudasyonlar oluşturur.\n  2. **Hücreleri Duvara Savurur:** Laminer akımdaki plazma yastığı kalkar; trombositler doğrudan endotel zarına fırlatılır.\n  3. **Lokal Staz Cepleri Yaratır:** Girdapların merkezinde ve kenarlarında kanın durakladığı mikro-staz cepleri oluşur.\n- **Klinik Örnekler:** Ülserleşmiş aterosklerotik plak çıkıntıları, damar dallanma noktaları (karotis bifurkasyonu), **arteriyel anevrizmalar** ve stenotik kalp kapakları (mitral darlık).",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Laminer Akım vs Türbülanslı Kaotik Akım",
                "Laminer Akım (Fizyolojik)",
                "Eritrosit ve trombositler merkezde akar; endotelle temas eden ince koruyucu plazma tabakası vardır.",
                "Türbülanslı Akım (Patolojik)",
                "Kaotik girdaplar oluşur; trombositler duvara savrulur, endotel mekanik aşınır ve lokal staz cepleri belirir."
            ),
            make_quiz(
                "Laminer kan akımının bozulup kaotik girdapların oluştuğu türbülans durumu en karakteristik olarak aşağıdaki patolojilerin hangisinde endotel hasarına ve trombüse yol açar?",
                [
                    {"key": "A", "text": "Aort anevrizmaları ve karotis bifurkasyonundaki aterom plakları", "isCorrect": True, "explanation": "Doğru cevap A'dır: Anevrizmalar ve bifurkasyonlardaki aterosklerotik plaklar lümen geometrisini bozarak şiddetli türbülans yaratır."},
                    {"key": "B", "text": "Uzun süreli yatak istirahatindeki baldır venleri", "isCorrect": False, "explanation": "Yatak istirahatinde türbülans değil staz görülür."},
                    {"key": "C", "text": "Gebelik uterusunun vena cavaya basısı", "isCorrect": False, "explanation": "Bası staza yol açar."},
                    {"key": "D", "text": "Akut masif kanama", "isCorrect": False, "explanation": "Kanamada hipovolemi görülür."}
                ]
            )
        ]
    })

    # Slide 47
    slides.append({
        "id": "k1-20-s47",
        "title": "Anormal Kan Akımı II: Staz ve Venöz Trombozun Temeli",
        "content": "Türbülans arteriyel trombozla ilişkiliyken, kan akımının yavaşlaması veya duraklaması olan **Staz**, venöz trombozun mutlak temelidir (Sınav Spotu):\n\n- **Stazın Patofizyolojik Etkileri:**\n  1. **Faktörlerin Birikmesi:** Hasar veya aktivasyon bölgesinde üretilen aktif pıhtılaşma enzimleri yıkanıp uzaklaştırılamaz (wash-out kalkar); konsantrasyonları kritik eşiği aşar.\n  2. **İnhibitörlerin Ulaşamaması:** Karaciğer kökenli doğal antikoagülanlar (ATIII, Protein C) kan akımı durduğu için pıhtılaşma odağına taze olarak taşınamaz.\n  3. **Marjinasyon:** Trombositler ve lökositler yavaşlayan akımda lümen merkezinden damar duvarına doğru çöker ve endotelle uzun süreli temas kurar.\n  4. **Hipoksinin Tetiklenmesi:** Durgun kanda oksijen tükenir; endotel hipoksiye uğrayarak adeziv moleküller eksprese eder.\n- **Klinik Nedenler:** Uzun süreli yatak istirahati (ameliyat sonrası, felç), uzun uçak yolculukları, konjestif kalp yetmezliği, varisler ve gebelik basısı.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Stazdan Venöz Tromboza Gidiş Mekanizması",
                [
                    "1. Akımın Yavaşlaması: Hareketsizlik veya kalp yetmezliği venöz akımı durdurur.",
                    "2. Yıkama Kaybı: Aktif pıhtılaşma faktörleri seyreltilemeyip lokal olarak birikir.",
                    "3. Hücresel Marjinasyon: Trombositler ve eritrositler venöz kapak ceplerine çöker.",
                    "4. Endotelyal Hipoksi: Oksijensiz kalan ven endoteli protrombotik hale geçer.",
                    "5. Kırmızı Trombüs: Fibrin ve eritrositlerden zengin staz trombüsü büyür."
                ]
            ),
            make_cloze(
                "Derin ven trombozu patogenezinde kan akımının duraklamasını ifade eden staz tablosu aktif koagülasyon faktörlerinin seyreltilmesini önleyerek pıhtıyı tetikler.",
                "staz",
                "Venöz dolaşımda kan akımının yavaşlaması veya durması durumu"
            )
        ]
    })

    # Slide 48
    slides.append({
        "id": "k1-20-s48",
        "title": "Atriyal Fibrilasyon ve Sol Atriyal Apendiks Stazı: Kardiyoemboli",
        "content": "Stazın kalpteki en tehlikeli ve sık karşılaşılan klinik örneği **Atriyal Fibrilasyondur (AF)** (Sınav Spotu):\n\n- **Aritminin Mekaniği:**\n  - Atriyal fibrilasyonda atriyum kası dakikada 300-600 kez kaotik ve koordinesiz elektrik dalgalarıyla uyarılır.\n  - Atriyumlar mekanik olarak etkili şekilde kasılamaz; kanı ventriküllere pompalayamaz ve atriyum duvarı adeta 'titreşir' (mekanik paralizi).\n- **Sol Atriyal Apendiks (LAA) Çıkmazı:**\n  - Sol atriyumun parmaksı çıkıntısı olan apendiks, kan akımının en yavaşladığı kör bir ceptir.\n  - AF sırasında bu cepte **ciddi bir staz gölü** oluşur.\n- **Mural Trombüs ve İnme:**\n  - Staz zemininde sol atriyal apendikste büyük bir **mural trombüs** oturur.\n  - Bu trombüsten kopan emboli parçaları sol ventriküle, oradan aortaya ve karotis arterler yoluyla doğrudan serebral dolaşıma uçar $\\to$ **Kardiyoembolik İskemik İnme**.\n- **Klinik Önemi:** AF hastalarında rutin antikoagülan (Varfarin veya DOAC) kullanılmasının temel gerekçesi bu staz trombüsünü önlemektir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Aşama", "Patofizyolojik Olay", "Klinik Karşılığı"],
                [
                    ["1. Elektriksel Aritmi", "Atriyumların koordinesiz kaotik uyarılması", "Atriyal Fibrilasyon (AF)"],
                    ["2. Mekanik Durgunluk", "Atriyal kontraksiyon kaybı ve kanın duraklaması", "Sol atriyal apendikste masif staz"],
                    ["3. Pıhtılaşma", "Eritrosit ve fibrinden zengin pıhtı oturması", "Sol Atriyal Mural Trombüs"],
                    ["4. Embolizasyon", "Pıhtı parçasının karotis yoluyla beyne gitmesi", "Akut Kardiyoembolik İskemik İnme (Felç)"]
                ]
            ),
            make_quiz(
                "Atriyal fibrilasyonu olan yaşlı bir hastada sol atriyal apendikste trombüs gelişmesinin ve sistemik emboli riskinin artmasının temel patofizyolojik mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Atriyal kontraksiyon kaybına bağlı sol atriyal staz", "isCorrect": True, "explanation": "Doğru cevap A'dır: AF'de atriyum kasılamaz ve kan sol atriyal apendikste duraklayarak (staz) trombüs oluşturur."},
                    {"key": "B", "text": "Aşırı endotel vazokonstriksiyonu", "isCorrect": False, "explanation": "AF endotel vazokonstriksiyonuyla ilişkili değildir."},
                    {"key": "C", "text": "Kanda Faktör VIII fazlalığı", "isCorrect": False, "explanation": "Primer sorun faktör yüksekliği değil mekanik stazdır."},
                    {"key": "D", "text": "Fibrinolitik sistemin hiperaktivitesi", "isCorrect": False, "explanation": "Fibrinoliz hiperaktif olsaydı trombüs oluşmazdı."}
                ]
            )
        ]
    })

    # Slide 49 - CHECKPOINT 5
    slides.append({
        "id": "k1-20-s49",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Endotel ve Virchow Üçlüsü",
        "content": "Bu checkpointte Virchow üçlüsünün ilk iki ayağını ve endotel dinamiklerini özetliyoruz:\n\n- **Virchow Üçlüsü:** **1. Endotel Hasarı**, **2. Anormal Kan Akımı (Staz/Türbülans)**, **3. Hiperkoagülabilite**.\n- **Sakin Endotel (Antitrombotik):** **PGI2, NO, CD39 (ADPaz)** ile trombositi durdurur; **trombomodulin, heparan sülfat ve TFPI** ile faktörleri kilitler; **t-PA** ile pıhtıyı eritir.\n- **Aktive Endotel (Protrombotik):** TNF/LPS ile uyarılır; **Doku Faktörü** üretir, **PAI-1** salgılar, **P-selektin** açar ve trombomodulini azaltır.\n- **Endotel Hasarı:** Yüksek akımlı **arteriyel ve kardiyak trombozun birincil ön koşuludur**; en sık neden **ülserleşmiş aterom plak rüptürüdür**.\n- **Türbülans:** Anevrizma ve plak kenarlarında girdaplar oluşturarak endoteli mekanik hırpalar ve trombositleri duvara savurur.\n- **Staz:** Yavaşlayan akımda faktörlerin seyreltilememesi, inhibitörlerin gelememesi ve trombosit marjinasyonudur; **venöz trombozun (DVT)** ve **atriyal fibrilasyonda sol atriyal trombüsün** temelidir.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Virchow Bileşeni", "Temel Mekanizma", "En Tipik Klinik Örnek"],
                [
                    ["Endotel Hasarı", "Kollajen ve TF maruziyeti, PGI2/NO kaybı", "Akut Koroner Tromboz (MI)"],
                    ["Türbülans", "Kaotik girdaplar, mekanik aşınma, duvar teması", "Aort anevrizması ve karotis bifurkasyon trombüsü"],
                    ["Staz", "Yıkama kaybı, inhibitör yokluğu, marjinasyon", "DVT ve Atriyal Fibrilasyonda LAA trombüsü"],
                    ["Hiperkoagülabilite", "Pıhtılaşma faktör fazlalığı / fren eksikliği", "Faktör V Leiden ve Antifosfolipid Sendromu"]
                ]
            ),
            make_chain(
                "Virchow Triadı Büyük Özeti",
                [
                    "1. Endotel Bozulması: Aterom plağı yırtılarak kollojen ve doku faktörü açığa çıkar.",
                    "2. Akım Değişikliği: Türbülans arterde endoteli aşındırır, staz vende pıhtıyı çöktürür.",
                    "3. Trombofililer: Kanda antikoagülan eksikliği veya faktör hiperaktivitesi eklenir.",
                    "4. Trombüs Patlaması: Üç sacayağının birleşmesiyle canlı damarda tıkayıcı kitle oluşur."
                ]
            )
        ]
    })

    # Slide 50
    slides.append({
        "id": "k1-20-s50",
        "title": "Bölüm Özeti: Virchow Üçlüsünden Kalıtsal Trombofililere Geçiş",
        "content": "Bölüm 5 boyunca Virchow üçlüsünün ilk iki ayağını (endotel hasarı ve anormal kan akımı) ve endotelin zıt yüzlerini inceledik:\n\n- **Özet:** Arteriyel trombozda endotel hasarı liderken, venöz trombozda staz ve hiperkoagülabilite liderdir.\n- **Sonraki Bölüm (Bölüm 6):** Virchow üçlüsünün üçüncü ayağı olan ve genetik mutasyonlarla seyreden **Primer (Kalıtsal) Trombofilileri (Faktör V Leiden, Protrombin G20210A, Antitrombin III, Protein C/S eksiklikleri ve Homosistinüri)** detaylarıyla ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Virchow üçlüsünde atriyal fibrilasyon ve uzun süreli yatak istirahatinde tromboza yol açan temel akım anormalliği nedir?",
                "Staz (Kan akımının yavaşlaması veya duraklaması)",
                "Pıhtılaşma faktörlerinin yıkanmasını engelleyen venöz akım durgunluğu"
            ),
            make_quiz(
                "Sağlıklı damar endotelinin trombosit adezyonunu engelleyen ve pıhtılaşmayı baskılayan 'antitrombotik' yüzeyinde aşağıdaki moleküllerden hangisi YER ALMAZ?",
                [
                    {"key": "A", "text": "Doku Faktörü (TF / Tromboplastin)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Doku Faktörü sakin endotelde bulunmaz; sadece aktive veya hasarlı endotelde açığa çıkan güçlü bir protrombotik başlatıcıdır."},
                    {"key": "B", "text": "Prostasiklin (PGI2)", "isCorrect": False, "explanation": "PGI2 sakin endotelin antiplatelet molekülüdür."},
                    {"key": "C", "text": "Trombomodulin", "isCorrect": False, "explanation": "Trombomodulin sakin endotelin antikoagülanıdır."},
                    {"key": "D", "text": "Heparan Sülfat", "isCorrect": False, "explanation": "Heparan sülfat ATIII'ü aktive eden antitrombotik glikozaminoglikandır."}
                ]
            )
        ]
    })

    return slides
