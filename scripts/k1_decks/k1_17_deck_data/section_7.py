# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-17-s61",
        "title": "Pelvik İnflamatuvar Hastalık (PİH): Asendan Yayılım ve Anatomi",
        "content": "Pelvik inflamatuvar hastalık (PİH), mikroorganizmaların endoserviksten yukarıya doğru tırmanarak üst genital traktusu enfekte etmesidir (Sınav Spotu):\n\n- **Asendan Yayılım Yolu:**\n  - Enfeksiyon servikal bariyeri aşar $\\to$ Endometriyum (**Endometrit**) $\\to$ Fallop tüpleri (**Salpenjit**) $\\to$ Overler (**Ooforit**) $\\to$ Tuboovaryan kompleks (**Tuboovaryan Abse - TOA**) $\\to$ Periton boşluğu (**Pelvik Peritonit**).\n- **Uzun Dönem Yıkıcı Sonuçlar:**\n  - PİH geçiren kadınlarda fallop tüplerinde gelişen fibrozis ve tıkanıklık nedeniyle:\n    1. **Tübal İnfertilite:** Tek bir PİH atağı kısırlık riskini %12 artırırken; üç atak sonrası kısırlık riski %50'yi aşar.\n    2. **Ektopik (Dış) Gebelik:** Döllenen zigot tıkalı tüpten rahme inemez; dış gebelik riski 7 ila 10 kat artar.\n    3. **Kronik Pelvik Ağrı:** Periton içi yapışıklıklar (adezyonlar) nedeniyle yıllar süren inatçı kasık ağrısı.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Lokalize Servisit vs Asendan Pelvik İnflamatuvar Hastalık",
                "Servisit Aşaması",
                "Enfeksiyon servikal os ile sınırlıdır; erken antibiyotik tedavisiyle üst genital traktusa geçiş engellenir.",
                "PİH Aşaması (Asendan Yayılım)",
                "Bakteriler tüplere ve pelvise tırmanmıştır; salpenjit, apse, tübal yapışıklık ve kalıcı kısırlık riski yaratır."
            ),
            make_cloze(
                "Endoserviksten yukarı tırmanan bakterilerin fallop tüplerinde oluşturduğu iltihabi enfeksiyon tablosuna salpenjit denir.",
                "salpenjit",
                "Fallop tüplerinin iltihaplanması terimi"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-17-s62",
        "title": "PİH Mikrobiyolojisi: Polimikrobiyal Doğa ve Sinerji",
        "content": "PİH başlangıçta cinsel yolla bulaşan bir patojenle tetiklense de hızla karmaşık polimikrobiyal bir enfeksiyona dönüşür (Sınav Spotu):\n\n- **1. Başlatıcı Primer Patojenler:**\n  - **Chlamydia trachomatis:** Olguların %30-50'sinde primer başlatıcıdır; sessizce tübal epitel silyalarını yıkar.\n  - **Neisseria gonorrhoeae:** Olguların %25-40'ında rol oynar; daha gürültülü ve akut semptomlar yaratır.\n  - **Mycoplasma genitalium:** İnatçı PİH olgularında giderek artan sıklıkta saptanmaktadır.\n- **2. Sekonder Süperenfeksiyon (Vajinal Flora Bakterileri):**\n  - Primer patojen mukozal bariyeri ve servikal tıkacı yıktıktan sonra vajinadaki anaerop ve fakültatif bakteriler yukarı dökülür:\n  - Anaeroplar (Bacteroides fragilis, Prevotella, Peptostreptococcus), Gardnerella vaginalis, enterik gram negatif basiller ve Streptococcus agalactiae.\n- **Tedavi Çıkarımı:** Bu polimikrobiyal karmaşa nedeniyle PİH tedavisi **asla tek bir antibiyotikle yapılamaz; mutlaka klamidya, gonokok ve anaeropları aynı anda örten geniş spektrumlu kombinasyonlar** seçilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["PİH Patojen Grubu", "Örnek Bakteriler", "Patojenik Rolü", "Hedefleyen Antibiyotik"],
                [
                    ["Primer CYBE Başlatıcıları", "N. gonorrhoeae, C. trachomatis", "Mukozal invazyon ve doku hasarı", "Seftriakson / Sefoksitin + Doksisiklin"],
                    ["Vajinal Anaeroplar", "Bacteroides, Prevotella, Peptostreptococcus", "Doku nekrozu ve apse oluşumu", "Metronidazol, Klindamisin"],
                    ["Fakültatif / Enterik Bakteriler", "E. coli, Grup B Streptokoklar", "Süpürasyon ve peritonit", "Beta-laktamlar, Sulbaktam"]
                ]
            ),
            make_quiz(
                "Pelvik inflamatuvar hastalığın (PİH) tedavisinde tek bir antibiyotik yerine mutlaka çoklu kombine antibiyotik rejimleri seçilmesinin temel gerekçesi nedir?",
                [
                    {"key": "A", "text": "PİH'in sadece virüslerden kaynaklanması", "isCorrect": False, "explanation": "PİH bakteriyel polimikrobiyal bir tablodur."},
                    {"key": "B", "text": "Enfeksiyonun gonokok ve klamidyanın yanı sıra vajinal anaeroplar ve enterik bakterileri içeren polimikrobiyal bir süreç olması", "isCorrect": True, "explanation": "Doğru cevap B'dir: PİH polimikrobiyaldir; anaeropları, klamidyayı ve gonokoku aynı anda hedeflemek şarttır."},
                    {"key": "C", "text": "Hastanın ağrı kesici istememesi", "isCorrect": False, "explanation": "Klinik gerekçe değildir."},
                    {"key": "D", "text": "Fallop tüplerinin antibiyotikleri yok etmesi", "isCorrect": False, "explanation": "Bilim dışı iddia."}
                ]
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-17-s63",
        "title": "PİH Klinik Belirtileri ve Tanı Kriterleri: Avize Bulgusu",
        "content": "PİH tanısı gecikirse kalıcı infertilite riski hızla katlanır; bu nedenle klinik şüphe halinde tedaviye derhal başlanmalıdır:\n\n- **En Sık Başvuru Semptomları:**\n  - Alt karın ve bilateral kasık ağrısı (en duyarlı semptom), anormal vajinal akıntı, disparoni, ara kanamalar ve ateş.\n- **Minimal Muayene Kriterleri (3 Kardinal Fizik Muayene Bulgusu - Sınav Spotu):**\n  1. **Servikal Hareket Hassasiyeti ('Avize Bulgusu' / Chandelier Sign):** Bimanuel muayenede serviks iki parmak arasında sağa-sola oynatıldığında peritonun gerilmesine bağlı hastanın şiddetle yerinden sıçramasıdır.\n  2. **Uterin Hassasiyet:** Uterus fundusunun palpasyonunda belirgin ağrı.\n  3. **Adneksiyal Hassasiyet:** Sağ ve sol over/tüp lojlarının muayenesinde bilateral veya unilateral şiddetli ağrı.\n- **Ek Destekleyici Kriterler:** Ateş (>38.3°C), mukopürülan servikal akıntı, kanda lökositoz ve artmış CRP/Sedimantasyon hızı.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Minimal Klinik Kriterler vs Ek Tanısal Destekleyiciler",
                "Minimal Muayene Kriterleri (Tedavi Başlatıcı)",
                "Servikal hareket hassasiyeti (avize bulgusu), uterin hassasiyet veya adneksiyal hassasiyetten en az birinin varlığı.",
                "Ek Destekleyici Kriterler",
                "Ateş >38.3°C, servikal pürülan eksuda, CRP/Sedim yüksekliği ve NAAT ile gonokok/klamidya pozitifliği."
            ),
            make_cloze(
                "Bimanuel pelvik muayenede serviksin hareket ettirilmesiyle periton gerilmesine bağlı şiddetli ağrı oluşmasına servikal hareket hassasiyeti veya avize bulgusu denir.",
                "servikal hareket hassasiyeti",
                "PİH'te bimanuel muayenede hastayı sıçratan kardinal fizik bulgu"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-17-s64",
        "title": "Tuboovaryan Abse (TOA) ve Fitz-Hugh-Curtis Sendromu",
        "content": "PİH'in en ağır iki anatomik komplikasyonu cerrahi aciliyet veya özel klinik sendrom yaratır:\n\n- **1. Tuboovaryan Abse (TOA - Sınav Spotu):**\n  - Fallop tüpü, over ve komşu bağırsak kıvrımlarının pürülan enflamasyonla birbirine yapışarak oluşturduğu loküle kistik iltihap kitlesidir.\n  - Pelvik ultrasonografi veya MR'da kalın duvarlı, septalı, ekojenik sıvı içeren kitle olarak izlenir.\n  - **Rüptür Tehlikesi:** Abse rüptüre olursa püy tüm karına boşalır; generalize peritonit, septik şok ve akut cerrahi gerektirir.\n- **2. Fitz-Hugh-Curtis Sendromu (Perihepatit - Sınav Spotu):**\n  - Bakterilerin parakolik oluklar boyunca karaciğer kapsülüne tırmanmasıyla gelişir.\n  - Karaciğer kapsülü ile ön karın duvarı arasında mikroskobik fibröz yapışıklıklar oluşur.\n  - Laparoskopide patognomonik **'keman teli' (violin-string) tarzında ince fibröz adezyonlar** görülür.\n  - Hasta sağ üst kadran ağrısı (akut kolesistiti taklit eder) ve nefes alırken batan plöretik ağrıdan yakınır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Komplikasyon", "Tutulan Bölge", "Patognomonik Görsel / Radyolojik Bulgu", "Klinik Tablo"],
                [
                    ["Tuboovaryan Abse (TOA)", "Fallop tüpü ve over kompleksi", "USG'de kalın duvarlı multiloküle kistik kitle", "Yüksek ateş, pelvik kitle, lökositoz, rüptür riski"],
                    ["Fitz-Hugh-Curtis Sendromu", "Glisson kapsülü ve karaciğer yüzeyi", "Laparoskopide 'keman teli' (violin-string) adezyonları", "Sağ üst kadran ağrısı, kolesistit benzeri tablo"]
                ]
            ),
            make_quiz(
                "PİH öyküsü olan genç bir kadında laparoskopide karaciğer kapsülü ile ön karın duvarı arasında 'keman teli' (violin-string) tarzında fibröz bantlar saptanması hangi klinik sendromu gösterir?",
                [
                    {"key": "A", "text": "Fitz-Hugh-Curtis sendromu (Perihepatit)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Klamidya veya gonorenin subfrenik alana yayılmasıyla karaciğer kapsülünde keman teli yapışıklıkları oluşturan sendrom Fitz-Hugh-Curtis sendromudur."},
                    {"key": "B", "text": "Budd-Chiari sendromu", "isCorrect": False, "explanation": "Hepatik ven trombozudur."},
                    {"key": "C", "text": "Meigs sendromu", "isCorrect": False, "explanation": "Over fibromu, asit ve hidrotoraks triadıdır."},
                    {"key": "D", "text": "Mallory-Weiss sendromu", "isCorrect": False, "explanation": "Gastroözofageal yırtık kanamasıdır."}
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-17-s65",
        "title": "PİH'te Hastaneye Yatış ve İV Tedavi Endikasyonları",
        "content": "PİH şüphesi olan her hasta ayaktan oral tedaviye uygun değildir; bazı klinik durumlarda hasta acilen servise yatırılarak parenteral tedaviye alınmalıdır (Sınav Spotu):\n\n- **Kesin Yatış Endikasyonları:**\n  1. **Tuboovaryan Abse (TOA) Varlığı:** Rüptür ve septik şok riski nedeniyle mutlak parenteral tedavi ve cerrahi hazırlık gerektirir.\n  2. **Gebelik:** PİH gebelikte nadirdir ancak geliştiğinde maternal ve fetal mortalite çok yüksektir; tüm oral ilaçlar (doksisiklin vb.) kontrendikedir.\n  3. **Cerrahi Acillerin Dışlanamaması:** Akut apandisit, over kist torsiyonu veya ektopik gebelik gibi cerrahi tablolar klinik olarak ekarte edilemiyorsa.\n  4. **Ağır Klinik Tablo:** Yüksek ateş (>38.5°C), aşırı bulantı-kusma (hastanın oral ilaç içememesi) ve peritonit/defans bulguları.\n  5. **Ayaktan Oral Tedaviye Yanıtsızlık:** Oral tedavi başlanmasına rağmen 48-72 saat içinde klinik düzelme sağlanamaması.\n  6. **Hasta Uyumu Zafiyeti:** İlaçlarını düzenli kullanamayacak veya kontrole gelemeyecek hastalar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Ayaktan Tedavi Edilebilecek PİH vs Hastaneye Yatış Endikasyonu",
                "Ayaktan Tedavi (Hafif-Orta PİH)",
                "Genel durumu iyi, ateşi düşük, bulantısı olmayan, apse saptanmayan ve oral ilaç içebilen hasta.",
                "Yatarak Tedavi (Hastaneye Yatış Şart)",
                "Tuboovaryan apse, gebelik, şiddetli kusma/peritonit, oral tedaviye yanıtsızlık veya apandisit şüphesi."
            ),
            make_quiz(
                "Aşağıdaki klinik tablolardan hangisi pelvik inflamatuvar hastalık (PİH) tanısı alan bir hastanın MUTLAKA hastaneye yatırılarak intravenöz tedaviye alınmasını gerektiren bir endikasyondur?",
                [
                    {"key": "A", "text": "Pelvik ultrasonda tuboovaryan abse (TOA) saptanması veya hastanın gebe olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tuboovaryan abse varlığı ve gebelik PİH'te kesin hastaneye yatış ve parenteral tedavi endikasyonudur."},
                    {"key": "B", "text": "Hastanın yaşının 25 olması", "isCorrect": False, "explanation": "Yaş tek başına yatış endikasyonu değildir."},
                    {"key": "C", "text": "Hafif vajinal akıntı varlığı", "isCorrect": False, "explanation": "Vajinal akıntı standart PİH semptomudur, yatış gerektirmez."},
                    {"key": "D", "text": "Hastanın evli olması", "isCorrect": False, "explanation": "Medeni hal yatış kriteri değildir."}
                ]
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-17-s66",
        "title": "Yatarak Parenteral PİH Tedavisi: Sefoksitin ve Doksisiklin",
        "content": "Hastaneye yatırılan PİH hastalarında kılavuzların önerdiği intravenöz parenteral rejimler (Sınav Spotu):\n\n- **1. Birinci Tercih Parenteral Rejim:**\n  - **Sefoksitin 4x2 g İV** (veya Sefotetan 2x2 g İV) $\\to$ Gonokok ve anaeropları güçlü biçimde örter.\n  - **ARTI**\n  - **Doksisiklin 2x100 mg oral veya İV** $\\to$ Chlamydia trachomatis ve Mycoplasma'yı örter.\n- **2. İkinci Tercih Parenteral Rejim (Özellikle Apseli Olgularda):**\n  - **Ampisilin / Sulbaktam 4x3 g İV**\n  - **ARTI**\n  - **Doksisiklin 2x100 mg oral/İV**\n- **İdameye Geçiş Kuralı:**\n  - Hasta yatırılarak İV tedavi verilir; klinik düzelme (ateşin düşmesi, karın hassasiyetinin kaybolması) sağlandıktan **24-48 saat sonra İV tedavi kesilir**.\n  - Tedavi oral Doksisiklin (2x100 mg) ile **toplam 14 güne tamamlanır**.\n- **Tuboovaryan Apsede Klindamisin Kuralı:** TOA varlığında rezidüel anaeropları tam kurutmak için rejime mutlaka **Klindamisin veya Metronidazol** eklenir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Parenteral PİH Rejimi", "İlaç ve Dozaj", "Hedeflenen Patojen Yelpazesi", "Tedavi Süresi"],
                [
                    ["Birinci Rejim (İV)", "Sefoksitin 4x2 g İV + Doksisiklin 2x100 mg oral/İV", "Gonokok, enterik basiller, klamidya, anaeroplar", "Düzelmeden 24-48 saat sonraya kadar İV"],
                    ["İkinci Rejim (İV)", "Ampisilin/sulbaktam 4x3 g İV + Doksisiklin 2x100 mg", "Geniş anaerop ve enterik kapsama", "Düzelmeden 24-48 saat sonraya kadar İV"],
                    ["Oral Tamamlama", "Doksisiklin 2x100 mg oral (± Klindamisin/Metronidazol)", "Klamidya ve anaeropların tam temizlenmesi", "Toplam 14 güne tamamlanır"]
                ]
            ),
            make_cloze(
                "Hastaneye yatırılan PİH hastalarında klinik düzelme sağlandıktan 24-48 saat sonra İV tedavi kesilerek oral doksisiklin ile tedavi toplam 14 güne tamamlanır.",
                "14 gün",
                "PİH tedavisinin tamamlanması gereken toplam gün sayısı"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-17-s67",
        "title": "Ayaktan Oral PİH Tedavi Rejimi: Seftriakson ve Doksisiklin",
        "content": "Genel durumu iyi olan, kusması ve peritoniti bulunmayan hafif-orta PİH hastaları ayaktan tedavi edilebilir:\n\n- **Standart Ayaktan Tedavi Protokolü (Sınav Spotu):**\n  - **Seftriakson 250 mg (veya 500 mg) İM TEK DOZ** (Gonokok kapsaması)\n  - **ARTI**\n  - **Doksisiklin 2x100 mg oral, 14 GÜN** (Chlamydia trachomatis kapsaması)\n  - **ARTI / OPSİYONEL**\n  - **Metronidazol 2x500 mg oral, 14 GÜN** (Bakteriyel vajinozis ve anaerop kapsaması; son kılavuzlarda PİH'e anaerop eşliği sık olduğu için metronidazol eklenmesi kuvvetle önerilmektedir).\n- **Kritik 72 Saat Takibi (Re-evalüasyon):**\n  - Ayaktan tedavi başlanan her hasta **48 ila 72 saat sonra mutlaka kontrole çağrılmalıdır**.\n  - Eğer 72 saat içinde hastanın ağrısı gerilememiş, ateşi düşmemişse ayaktan tedavi başarısız kabul edilir ve hasta derhal hastaneye yatırılarak İV tedaviye geçirilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Başlangıç İM Seftriakson vs 14 Günlük Oral Tedavi",
                "Klinikte İlk Gün",
                "Seftriakson 250-500 mg İM tek doz uygulanır; gonokok yükü anında kırılır.",
                "Evde 14 Gün Boyunca",
                "Doksisiklin 2x100 mg ve Metronidazol 2x500 mg aksatılmadan 14 gün içilmelidir; 72. saatte kontrol şarttır."
            ),
            make_quiz(
                "Ayaktan oral tedavi başlanan hafif-orta şiddette bir PİH hastasında klinik tablonun düzelip düzelmediğini değerlendirmek için zorunlu kontrol muayenesi ne zaman yapılmalıdır?",
                [
                    {"key": "A", "text": "48 - 72 saat sonra", "isCorrect": True, "explanation": "Doğru cevap A'dır: Ayaktan PİH hastaları 48-72 saat sonra yeniden değerlendirilmeli; düzelme yoksa yatırılmalıdır."},
                    {"key": "B", "text": "1 ay sonra", "isCorrect": False, "explanation": "1 ay çok geçtir, tübal hasar kalıcılaşır."},
                    {"key": "C", "text": "İlaç bittikten 6 ay sonra", "isCorrect": False, "explanation": "Takip süresi dışındadır."},
                    {"key": "D", "text": "Hiç kontrole gerek yoktur", "isCorrect": False, "explanation": "Kontrolsüz bırakılamaz."}
                ]
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-17-s68",
        "title": "Akut Epididimit ve Epididimoorşit Tedavi Stratejileri",
        "content": "Erkekte PİH'in karşılığı olan epididimit tedavisinde hastanın yaşı ve cinsel risk profili antibiyotik seçimini belirler (Sınav Spotu):\n\n- **1. Genç Cinsel Aktif Erkekler (< 35 Yaş - CYBE Kökenli):**\n  - Başlıca Etkenler: Chlamydia trachomatis ve Neisseria gonorrhoeae.\n  - Tedavi: **Seftriakson 250 mg İM tek doz + Doksisiklin 2x100 mg oral, 10 gün**.\n- **2. İleri Yaş (> 35 Yaş) veya İnsertif Anal Seks Öyküsü Olanlar (Enterik Bakteri Kökenli):**\n  - Başlıca Etkenler: Escherichia coli, Klebsiella, Pseudomonas gibi enterik gram negatif basiller.\n  - Tedavi: İdrar yollarına ve prostat/epididime mükemmel penetre olan florokinolonlar:\n    - **Levofloksasin 1x500 mg oral, 10 gün** VEYA Ofloksasin 2x300 mg oral, 10 gün.\n  - Eğer hem CYBE hem anal temas şüphesi varsa: **Seftriakson 250 mg İM tek doz + Levofloksasin 1x500 mg oral, 10 gün** kombine edilir.\n- **Destek Tedavi:** Yatak istirahati, skrotal elevasyon (askı/süspansuar), buz uygulaması ve NSAİİ.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Hasta Profili", "Olası Patojenler", "Önerilen Tedavi Protokolü", "Süre"],
                [
                    ["< 35 Yaş, Cinsel Aktif", "C. trachomatis, N. gonorrhoeae", "Seftriakson 250 mg İM + Doksisiklin 2x100 mg", "10 gün"],
                    ["> 35 Yaş, İdrar Yolu Kaynaklı", "E. coli ve enterik gram (-) basiller", "Levofloksasin 1x500 mg oral", "10 gün"],
                    ["İnsertif Anal Seks Yapan Erkek", "Gonokok + Enterik bakteriler", "Seftriakson 250 mg İM + Levofloksasin 1x500 mg", "10 gün"]
                ]
            ),
            make_quiz(
                "İnsertif anal seks öyküsü olan ve akut epididimit tanısı konan bir erkekte hem gonokokları hem de olası enterik gram negatif bakterileri kapsamak için önerilen rejim hangisidir?",
                [
                    {"key": "A", "text": "Seftriakson 1x250 mg İM tek doz + Levofloksasin 1x500 mg oral, 10 gün", "isCorrect": True, "explanation": "Doğru cevap A'dır: Anal temas öykülü epididimitte Seftriakson (gonokok için) + Levofloksasin (enterik basiller için) 10 gün uygulanır."},
                    {"key": "B", "text": "Yalnızca Flukonazol 150 mg", "isCorrect": False, "explanation": "Flukonazol mantar ilacıdır."},
                    {"key": "C", "text": "Sadece aspirin", "isCorrect": False, "explanation": "Antibiyotik değildir."},
                    {"key": "D", "text": "Metronidazol 500 mg tek doz", "isCorrect": False, "explanation": "Enterik basillere ve gonokoka etkisizdir."}
                ]
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-17-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] PİH ve Epididimit Tedavisi",
        "content": "Bu checkpointte üst genital sistem komplikasyonlarını, PİH yatış kriterlerini ve rejimlerini özetliyoruz:\n\n- **PİH Anatomisi:** Asendan yayılım (endometrit $\\to$ salpenjit $\\to$ ooforit $\\to$ TOA $\\to$ pelvik peritonit). Uzun dönemde tübal infertilite ve dış gebelik riski.\n- **Klinik Tanı:** Servikal hareket hassasiyeti (avize bulgusu), uterin veya adneksiyal hassasiyetten en az birinin bulunması tedavi başlamak için yeterlidir.\n- **Komplikasyonlar:** Tuboovaryan abse (TOA) rüptür riski; Fitz-Hugh-Curtis perihepatitinde 'keman teli' adezyonları.\n- **Hastaneye Yatış:** TOA, gebelik, peritonit/şiddetli kusma, oral tedaviye yanıtsızlık (72 saatte düzelmeme).\n- **Parenteral Rejim:** Sefoksitin 4x2 g İV + Doksisiklin 2x100 mg; klinik düzelmeden 24-48 saat sonra oral doksisiklin ile toplam 14 güne tamamlama (apsede klindamisin eklenir).\n- **Epididimit:** <35 yaşta Seftriakson + Doksisiklin (10 gün); anal seks/enterik şüphede Seftriakson + Levofloksasin (10 gün).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Klinik Tablo", "Yatış Durumu", "Birinci Tercih Tedavi Protokolü", "Toplam Süre"],
                [
                    ["Hafif-Orta PİH", "Ayaktan", "Seftriakson 250 mg İM + Doksisiklin 2x100 mg (± Metronidazol)", "14 gün"],
                    ["Ağır PİH / TOA", "Yatarak İV", "Sefoksitin 4x2 g İV + Doksisiklin 2x100 mg oral/İV", "Toplam 14 gün (apsede klindamisin)"],
                    ["CYBE Epididimit (<35 yaş)", "Ayaktan", "Seftriakson 250 mg İM + Doksisiklin 2x100 mg", "10 gün"],
                    ["Enterik Epididimit (Anal temas)", "Ayaktan", "Seftriakson 250 mg İM + Levofloksasin 1x500 mg", "10 gün"]
                ]
            ),
            make_chain(
                "PİH Yönetim ve Yatış Karar Basamakları",
                [
                    "1. Muayene: Avize bulgusu veya adneksiyal ağrıyla PİH tanınır.",
                    "2. Risk Kontrolü: TOA, gebelik veya peritonit varsa derhal yatış verilir.",
                    "3. Parenteral Başlangıç: Sefoksitin + Doksisiklin İV başlanır.",
                    "4. Taburculuk ve 14 Gün: Klinik düzelmeyle oral doksisiklin 14 güne tamamlanır."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-17-s70",
        "title": "Bölüm Özeti: PİH ve Epididimitten Genital Ülserlere Geçiş",
        "content": "Bölüm 7 boyunca pelvik inflamatuvar hastalığın polimikrobiyal yapısını, hastaneye yatış kriterlerini ve 14 günlük tedavi rejimlerini tamamladık:\n\n- **Kritik Kural:** PİH tedavisinde yetersiz süre veya gecikme kalıcı kısırlıkla sonuçlanır; tedavi daima 14 güne tamamlanmalıdır.\n- **Sonraki Bölüm:** Bir sonraki bölümde genital bölgede açık yaralarla seyreden **genital ülser sendromunu, ağrılı şankroid (Haemophilus ducreyi) ile ağrısız primer sifiliz (Treponema pallidum) ayrımını** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Laparoskopide karaciğer kapsülü ile ön karın duvarı arasında keman teli (violin-string) adezyonları ile karakterize PİH komplikasyonu nedir?",
                "Fitz-Hugh-Curtis sendromu (Perihepatit)",
                "Subfrenik yapışıklıklarla seyreden kolesistit taklitçisi tablo"
            ),
            make_quiz(
                "Tuboovaryan abse (TOA) saptanan bir PİH hastasında anaerobik bakterileri tam eradike etmek için standart parenteral rejime eklenmesi önerilen antibiyotik hangisidir?",
                [
                    {"key": "A", "text": "Klindamisin (veya Metronidazol)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tuboovaryan apselerde güçlü anaerop kapsama sağlamak için idameye Klindamisin eklenmesi önerilir."},
                    {"key": "B", "text": "Vankomisin tek başına", "isCorrect": False, "explanation": "Vankomisin anaerop gram negatiflere etkisizdir."},
                    {"key": "C", "text": "Flukonazol", "isCorrect": False, "explanation": "Mantar ilacıdır."},
                    {"key": "D", "text": "Asiklovir", "isCorrect": False, "explanation": "Herpes ilacıdır."}
                ]
            )
        ]
    })

    return slides
