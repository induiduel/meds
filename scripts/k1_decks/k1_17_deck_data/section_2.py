# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-17-s11",
        "title": "Vajinit ve Servisit Ayrımı: Anatomik ve Klinik Parametreler",
        "content": "Kadın genital akıntı şikayetinde en kritik tanı basamağı lezyonun vajina kaynaklı (vajinit) mı yoksa serviks kaynaklı (servisit) mı olduğunu ayırt etmektir (Sınav Spotu):\n\n- **1. Vajinit (Vajina Mukozasının Enflamasyonu):**\n  - Enfeksiyon vajina duvarı ve vulvadadır; serviks intakt ve temizdir.\n  - Başlıca Semptomlar: Vulvar kaşıntı, yanma, irritasyon, yüzeyel dizüri ve vajina duvarında karakteristik akıntı/eksuda.\n  - En Sık Nedenler: Bakteriyel vajinozis (%40-50), Vulvovajinal kandidiyazis (%20-25), Trikomoniyazis (%15-20).\n- **2. Servisit (Endoservikal Epitelin Enfeksiyonu):**\n  - Enfeksiyon servikal os ve glandüler kolumnar epiteldedir.\n  - Başlıca Semptomlar: Derin disparoni (ağrılı cinsel ilişki), **postkoital kanama (ilişki sonrası lekelenme)**, pelvik dolgunluk; servikal kanaldan sarı-yeşil pürülan akıntı gelmesi ve serviksin en ufak dokunmada kanaması (frajilite).\n  - En Sık Nedenler: Chlamydia trachomatis, Neisseria gonorrhoeae, Mycoplasma genitalium.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Vajinit Kliniği vs Servisit Kliniği",
                "Vajinit Tablosu",
                "Vulvada şiddetli kaşıntı, yanma ve vajinal akıntı vardır; postkoital kanama veya derin pelvik ağrı beklenmez.",
                "Servisit Tablosu",
                "Servikal os'tan mukopürülan akıntı gelir; temasla kolay kanar (frajilite) ve postkoital kanama tipiktir."
            ),
            make_cloze(
                "Servikal os enfeksiyonunda özellikle cinsel ilişki sonrasında meydana gelen tipik kanamaya postkoital kanama denir.",
                "postkoital kanama",
                "Cinsel temas sonrası lekelenme tarzı kanama"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-17-s12",
        "title": "Bakteriyel Vajinozis (BV): Laktobasil Kaybı ve Mikrobiyota Çöküşü",
        "content": "Bakteriyel vajinozis klasik bir yangı (lökositoz) içermediği için 'vajinit' değil 'vajinozis' olarak adlandırılır:\n\n- **Normal Vajinal Flora:** Sağlıklı doğurganlık çağındaki bir kadında vajina lümenine hidrojen peroksit (H2O2) ve laktik asit üreten **Lactobacillus (Döderlein basilleri)** hakimdir; vajinal pH <4.5 (asidik) tutularak patojenlerin üremesi engellenir.\n- **Floranın Bozulması:** Sık vajinal duş, yeni cinsel partner veya antibiyotik kullanımı laktobasilleri yok eder.\n- **Anaerop Patlaması:** Laktik asit azalınca pH yükselir (>4.5); fırsatçı anaerobik bakteriler katlanarak çoğalır:\n  - Gardnerella vaginalis, Atopobium vaginae, Mobiluncus türleri, Prevotella ve Peptostreptococcus.\n- **Koku Üretimi:** Bu anaeroplar poliaminler (kadaverin, putresin) üretir; alkali ortamda bu maddeler buharlaşarak karakteristik 'bozuk balık kokusu' salar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Bakteriyel Vajinozis Patogenez Basamakları",
                [
                    "1. Laktobasil Sayısında Çöküş: Koruyucu H2O2 üreten Döderlein basilleri kaybolur.",
                    "2. Vajinal pH Artışı: Asidite kaybolur ve vajinal ortam pH >4.5 seviyesine çıkar.",
                    "3. Anaerop Bakteri İstilaı: Gardnerella vaginalis ve anaerop mikroorganizmalar ürer.",
                    "4. Uçucu Amin Salınımı: Kadaverin ve putresin kötü balık kokulu gri-beyaz akıntı yapar."
                ]
            ),
            make_quiz(
                "Bakteriyel vajinozis gelişiminde ilk tetikleyici mikrobiyolojik basamak aşağıdakilerden hangisidir?",
                [
                    {"key": "A", "text": "Vajinada hidrojen peroksit üreten koruyucu laktobasillerin yok olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Normal floradaki koruyucu Lactobacillus türlerinin kaybı anaeropların aşırı üremesini başlatır."},
                    {"key": "B", "text": "Vajinal pH'nın 3.0'ın altına düşerek aşırı asidik olması", "isCorrect": False, "explanation": "pH düşmez, aksine >4.5'e yükselir."},
                    {"key": "C", "text": "Mantar sporlarının vajina duvarını delmesi", "isCorrect": False, "explanation": "Bu kandidiyazisin özelliğidir."},
                    {"key": "D", "text": "Uterus düz kaslarının ritmik spazmı", "isCorrect": False, "explanation": "Kas spazmı vajinozis nedeni değildir."}
                ]
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-17-s13",
        "title": "Bakteriyel Vajinozis Tanısı: Amsel Kriterleri ve Clue Cell",
        "content": "Bakteriyel vajinozisin klinik tanısında Amsel kriterleri altın standarttır (4 kriterden en az 3'ü bulunmalıdır - Sınav Spotu):\n\n- **1. Homojen Gri-Beyaz Akıntı:** Vajina duvarlarını homojen biçimde sıvayan, ince gri-beyaz akıntı.\n- **2. Vajinal pH > 4.5:** pH kağıdı ile ölçüldüğünde asiditenin kaybolması.\n- **3. Pozitif Whiff (Koku / KOH) Testi:** Vajinal akıntı lam üzerine alınıp üzerine %10 Potasyum Hidroksit (KOH) damlatıldığında açığa çıkan keskin **amin / bozuk balık kokusu**.\n- **4. İpucu Hücreleri (Clue Cell - Mikroskopi):**\n  - Serum fizyolojik damlatılmış taze yaymada vajinal yassı epitel hücrelerinin sınırlarının yüz binlerce kokobasil (Gardnerella) ile kaplanarak silinmesi ve buzlu cam manzarası almasıdır.\n  - Yassı epitel hücrelerinin en az %20'sinin clue cell olması patognomoniktir.\n- **Önemli Negatif:** Vajinada belirgin lökosit (nötrofil) infiltrasyonu ve eritem/inflamasyon görülmez.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Amsel Kriteri", "Muayene / Test Yöntemi", "Pozitiflik Eşiği"],
                [
                    ["Akıntı Niteliği", "Spekulum muayenesi", "Vajina duvarını ince sıvayan homojen gri-beyaz akıntı"],
                    ["Vajinal pH", "pH indikatör kağıdı", "pH > 4.5 (alkalen kayma)"],
                    ["Whiff (Amin) Testi", "%10 KOH damlatılması", "Tipik çürümüş balık / amin kokusu yayılması"],
                    ["Clue Cell (İpucu Hücresi)", "SF ile direkt mikroskopi", "Epitel hücre sınırlarının bakterilerce örtülmesi (>%20)"]
                ]
            ),
            make_cloze(
                "Bakteriyel vajinoziste mikroskop altında sınırları yoğun Gardnerella bakterileriyle kaplanmış yassı epitel hücrelerine clue cell denir.",
                "clue cell",
                "İpucu hücresi teriminin tıbbi adı"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-17-s14",
        "title": "Bakteriyel Vajinozis Tedavi Protokolleri ve Gebelik Yönetimi",
        "content": "Bakteriyel vajinozisin tedavisinde amaç anaerobik aşırı çoğalmayı baskılayıp laktobasillerin yeniden kolonize olmasını sağlamaktır:\n\n- **Birinci Basamak Oral Rejim:**\n  - **Metronidazol 2x500 mg oral, 7 gün** (en sık tercih edilen standart tedavi).\n  - Alternatif Tek Doz: Metronidazol 2 g oral tek doz (uyumu artırır ancak nüks oranı 7 günlük rejime göre biraz daha yüksektir).\n- **Topikal Alternatifler:**\n  - Metronidazol jel (%0.75) günde 1 kez intravajinal, 5 gün.\n  - Klindamisin krem (%2) gece yatarken intravajinal, 7 gün.\n- **Gebelikte Tedavi (Sınav Spotu):**\n  - BV gebelikte erken doğum, erken membran rüptürü (EMR) ve koryoamniyonit riskini katlar; bu nedenle semptomatik gebeler mutlaka tedavi edilmelidir.\n  - Gebelerde oral **Metronidazol (2x500 mg, 7 gün)** ilk trimester dahil güvenle kullanılır.\n- **Partner Tedavisi:** BV cinsel temasla bulaşabilen bir disbiyozis olmakla birlikte, erkek partnerin rutin tedavisi nüks oranını azaltmadığı için **rutin partner tedavisi önerilmez**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Standart Oral Metronidazol vs Topikal Vajinal Rejim",
                "Oral Metronidazol (2x500 mg, 7 gün)",
                "En yüksek klinik kür oranına sahiptir; sistemik etki sağlar ancak ağızda metalik tat ve bulantı yapabilir.",
                "Topikal Vajinal Jel/Krem",
                "Sistemik yan etkilerden kaçınmak isteyenlerde uygundur; gebelikte de tercih edilebilir."
            ),
            make_quiz(
                "Bakteriyel vajinozis tanısı alan gebe bir hastada erken doğum ve koryoamniyonit riskini önlemek için önerilen standart birinci basamak tedavi rejimi nedir?",
                [
                    {"key": "A", "text": "Doksisiklin 2x100 mg oral, 14 gün", "isCorrect": False, "explanation": "Doksisiklin gebelikte diş ve kemik hasarı nedeniyle kontrendikedir."},
                    {"key": "B", "text": "Metronidazol oral (2x500 mg, 7 gün)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Gebelerde BV tedavisinde oral metronidazol 7 gün güvenli ve standart rejimdir."},
                    {"key": "C", "text": "Siprofloksasin 1x500 mg tek doz", "isCorrect": False, "explanation": "Kinolonlar gebelikte ve BV'de ilk seçenek değildir."},
                    {"key": "D", "text": "Penisilin G intramusküler", "isCorrect": False, "explanation": "Penisilin BV'deki anaeroplara etkisizdir."}
                ]
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-17-s15",
        "title": "Vulvovajinal Kandidiyazis: Candida albicans ve Risk Faktörleri",
        "content": "Kadınların yaklaşık %75'inin yaşamı boyunca en az bir kez geçirdiği en sık semptomatik vajinit tablosudur:\n\n- **Etken:** Olguların %85-90'ından **Candida albicans** sorumludur. Kalan vakalarda tedaviye daha dirençli olan non-albicans türler (Candida glabrata, Candida krusei) rol oynar.\n- **Tetikleyici Risk Faktörleri:**\n  1. **Geniş Spektrumlu Antibiyotik Kullanımı:** Vajinal laktobasilleri öldürerek mayaların kontrolsüz çoğalmasına zemin hazırlar.\n  2. **Yüksek Östrojen Düzeyleri:** Gebelik, oral kontraseptif kullanımı veya hormon replasmanı glikojen depolarını artırarak mayayı besler.\n  3. **Diabetes Mellitus:** Kontrolsüz hiperglisemi doku şekerini artırır ve fungal adezyonu güçlendirir.\n  4. **İmmünsüpresyon:** Kortikosteroid tedavisi, kemoterapi veya HIV enfeksiyonu.\n- **Klinik Belirtiler:** Dayanılmaz **şiddetli vulvar kaşıntı (pruritus)**, yanma, disparoni ve vulvada belirgin ödem ve eritem.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Antibiyotik Kullanımından Kandidiyazise Gidiş Zinciri",
                [
                    "1. Sistemik Antibiyotik Alımı: Başka bir enfeksiyon için geniş spektrumlu antibiyotik kullanılır.",
                    "2. Laktobasillerin Ölümü: Vajinayı koruyan Döderlein basilleri yok olur.",
                    "3. Fungal Fırsatçılık: Normalde sessiz kommensal olan Candida albicans hızla çoğalır.",
                    "4. Şiddetli Pruritus: Peynirimsi akıntı ve yoğun vulvar kaşıntı ile kandidiyazis tablosu yerleşir."
                ]
            ),
            make_cloze(
                "Geniş spektrumlu antibiyotik kullanımı sonrası vajinada laktobasillerin azalmasıyla aşırı çoğalan en sık maya mantarı Candida albicans türüdür.",
                "Candida albicans",
                "Peynirimsi akıntı ve kaşıntı yapan majör maya"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-17-s16",
        "title": "Kandidiyazis Tanı ve Tedavisi: Peynirimsi Akıntı ve Flukonazol",
        "content": "Kandidiyazisin klinik ve mikroskopik tanısı kendine has özellikler taşır (Sınav Spotu):\n\n- **Karakteristik Akıntı:** Tipik olarak **peynirimsi, süt kesiği kıvamında (cottage cheese)**, beyaz renkte ve kokusuzdur; vajina duvarına yapışık plaklar oluşturur.\n- **Vajinal pH:** Bakteriyel vajinozis ve trikomoniyazisten farklı olarak kandidiyaziste **vajinal pH normal asidik sınırdadır (pH < 4.5)**.\n- **Mikroskopik İnceleme (%10 KOH Bakısı):**\n  - Lam üzerine damlatılan KOH epitel hücrelerini eritir; geride tomurcuklanan maya hücreleri ve yalancı hifler (**psödohifler**) net olarak izlenir.\n- **Tedavi Seçenekleri:**\n  - **Oral Tedavi:** **Flukonazol 150 mg oral tek doz** (en pratik ve yüksek başarı oranlı yaklaşım).\n  - **Topikal Tedavi:** Klotrimazol veya Mikonazol vajinal ovül/krem (3-7 gün).\n  - **Gebelerde Tedavi:** Oral azoller teratojenite riski nedeniyle gebelikte önerilmez; gebelerde **topikal klotrimazol veya mikonazol ovülleri 7 gün** kullanılır.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Özellik", "Bakteriyel Vajinozis (BV)", "Vulvovajinal Kandidiyazis", "Trikomoniyazis"],
                [
                    ["Akıntı Görünümü", "Homojen ince gri-beyaz", "Beyaz, peynirimsi / süt kesiği", "Köpüklü, sarı-yeşil, kötü kokulu"],
                    ["Vajinal pH", "> 4.5 (alkalen)", "< 4.5 (normal asidik)", "> 4.5 (alkalen)"],
                    ["Whiff (Amin) Testi", "Pozitif (keskin balık kokusu)", "Negatif", "Genellikle pozitif"],
                    ["Mikroskopik Bulgusu", "Clue cell (ipucu hücresi)", "Psödohif ve tomurcuklanan maya", "Hareketli kamçılı trofozoitler"],
                    ["Birincil Tedavi", "Metronidazol 2x500 mg, 7 gün", "Flukonazol 150 mg oral tek doz", "Metronidazol 2 g oral tek doz"]
                ]
            ),
            make_quiz(
                "Vajinal akıntı şikayeti olan bir kadında peynirimsi beyaz akıntı, şiddetli kaşıntı, normal asidik vajinal pH (<4.5) ve KOH bakısında psödohifler saptanıyor. İlk tercih oral tedavi nedir?",
                [
                    {"key": "A", "text": "Metronidazol 2 g tek doz", "isCorrect": False, "explanation": "Metronidazol trikomoniyazis ve BV tedavisidir, mantara etkisizdir."},
                    {"key": "B", "text": "Flukonazol 150 mg oral tek doz", "isCorrect": True, "explanation": "Doğru cevap B'dir: Vulvovajinal kandidiyaziste birinci basamak oral tedavi Flukonazol 150 mg tek dozdur."},
                    {"key": "C", "text": "Azitromisin 1 g oral tek doz", "isCorrect": False, "explanation": "Azitromisin antibakteriyeldir."},
                    {"key": "D", "text": "Seftriakson 250 mg İM", "isCorrect": False, "explanation": "Gonore tedavisidir."}
                ]
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-17-s17",
        "title": "Mukopürülan Servisit: Patofizyoloji ve Mikrobiyoloji",
        "content": "Servisit, vajinanın skuamöz epitelinin değil; endoservikal kanalın glandüler kolumnar epitelinin enfeksiyonudur (Sınav Spotu):\n\n- **Patojen Tropizmi:** Neisseria gonorrhoeae ve Chlamydia trachomatis özellikle tek katlı kolumnar epitele affinite gösterir; vajinanın çok katlı yassı epitelini enfekte edemezler.\n- **Mukopürülan Eksuda:** Endoservikal bezlerde yoğun nötrofilik infiltrasyon ve lökosit birikimi gelişir. Servikal kanaldan dışarı sarı-yeşil renkli, kıvamlı mukopürülan sekresyon boşalır.\n- **Etiyolojik Dağılım:**\n  - **Chlamydia trachomatis:** Servisitin en sık bakteriyel nedenidir (%30-50).\n  - **Neisseria gonorrhoeae:** Ağır mukopürülan akıntıyla seyreder.\n  - **Mycoplasma genitalium:** Klamidya ve gonore negatif olguların önemli bir kısmından sorumludur.\n  - **Trichomonas vaginalis ve HSV:** Nadiren servisit tablosuna eşlik edebilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Vajina Skuamöz Epiteli vs Endoserviks Kolumnar Epiteli",
                "Vajina Epiteli",
                "Çok katlı yassı epiteldir; klamidya ve gonokok buraya tutunamaz; kandida ve Gardnerella etkiler.",
                "Endoserviks Epiteli",
                "Tek katlı kolumnar bez epitelidir; klamidya ve gonokok için spesifik hedef dokudur (mukopürülan servisit)."
            ),
            make_cloze(
                "Endoservikal kanalın glandüler kolumnar epiteline tutunarak mukopürülan servisit oluşturan en sık mikroorganizma Chlamydia trachomatis bakterisidir.",
                "Chlamydia trachomatis",
                "Servisitin en yaygın bakteriyel etkeni"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-17-s18",
        "title": "Servisitte Klinik Bulgular: Ektropiyon, Frajilite ve Tanı",
        "content": "Servisitin klinik muayenesi jinekolojik spekulum bakısı ile netleştirilir:\n\n- **1. Servikal Frajilite (Kolay Kanamalık - Sınav Spotu):**\n  - Enflame olmuş endoservikal mukoza aşırı derecede vasküler ve ödemlidir.\n  - Pamuklu sürüntü çubuğu (eküvyon) endoservikal osa hafifçe değdirildiğinde bile yüzeyden derhal sızıntı şeklinde kanama başlar (servikal frajilite).\n- **2. Postkoital ve İntermenstrüel Kanama:**\n  - Hastalar özellikle cinsel temas sonrası lekelenme veya iki adet dönemi arasında düzensiz kanamadan yakınır.\n- **3. Sarı-Yeşil Endoservikal Eksuda:**\n  - Servikal os silindiğinde sarı-yeşil pürülan akıntının kanaldan gelmeye devam ettiği görülür.\n- **Tanı:**\n  - Endoservikal sürüntünün Gram boyamasında >30 lökosit/büyütme alanı saptanır.\n  - Nötrofil içi Gram (-) diplokok varsa gonore; yoksa nongonokokal servisit (klamidya / mikoplazma) düşünülür; kesin tanı **NAAT** ile konur.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Servisit Muayenesinde Tanı Adımları",
                [
                    "1. Spekulum Muayenesi: Servikal os gözlenir ve ektropiyon/ödem değerlendirilir.",
                    "2. Frajilite Kontrolü: Pamuk uçlu eküvyonla temas ettirildiğinde kolay kanama izlenir.",
                    "3. Sürüntü Alımı: Endoservikal kanaldan NAAT ve Gram boyama için sürüntü alınır.",
                    "4. Hedefe Yönelik Tedavi: Gonokok veya klamidya saptanarak ikili tedavi başlanır."
                ]
            ),
            make_quiz(
                "Spekulum muayenesinde pamuklu eküvyonun servikal osa hafifçe dokundurulmasıyla anında sızıntı şeklinde kanama başlaması (servikal frajilite) öncelikle hangi tablonun göstergesidir?",
                [
                    {"key": "A", "text": "Akut mukopürülan servisit", "isCorrect": True, "explanation": "Doğru cevap A'dır: Servikal frajilite ve mukopürülan eksuda servisitin en karakteristik muayene bulgusudur."},
                    {"key": "B", "text": "Basit vajinal kuruluk", "isCorrect": False, "explanation": "Vajinal kurulukta servikal pürülan eksuda ve frajilite olmaz."},
                    {"key": "C", "text": "Over kisti rüptürü", "isCorrect": False, "explanation": "Over kisti batın içi kanama yapar, servikal frajilite yapmaz."},
                    {"key": "D", "text": "Fizyolojik ovülasyon kanaması", "isCorrect": False, "explanation": "Ovülasyonda serviks frajil ve pürülan değildir."}
                ]
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-17-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Vajinal ve Servikal Enfeksiyon Sendromları",
        "content": "Bu checkpointte vajinit ve servisit ayırıcı tanısını, Amsel kriterlerini ve mikrobiyolojik özellikleri pekiştiriyoruz:\n\n- **Vajinit vs Servisit:** Vajinitte vulvar kaşıntı/irritasyon ön plandadır; servisitte ise endoservikal kanal tutulur, servikal frajilite ve postkoital kanama tipiktir.\n- **Bakteriyel Vajinozis (BV):** Laktobasil kaybı $\\to$ pH >4.5 $\\to$ Gardnerella ve anaerop artışı $\\to$ Gri-beyaz akıntı, pozitif Whiff testi (amin kokusu) ve Clue cell (ipucu hücresi). Tedavi: Metronidazol (2x500 mg, 7 gün).\n- **Kandidiyazis:** Candida albicans; antibiyotik veya östrojen tetikler; peynirimsi/süt kesiği akıntı, şiddetli kaşıntı; pH <4.5 (normal asidik!); psödohifler. Tedavi: Flukonazol 150 mg oral tek doz.\n- **Mukopürülan Servisit:** C. trachomatis ve N. gonorrhoeae kolumnar epitele affinite gösterir; sarı-yeşil akıntı ve temasla kanama yapar.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Sendrom", "Tipik Akıntı", "Vajinal pH", "Patognomonik İnceleme", "İlk Seçenek İlaç"],
                [
                    ["Bakteriyel Vajinozis", "İnce gri-beyaz, balık kokulu", "> 4.5", "Clue cell ve pozitif Whiff testi", "Metronidazol 2x500 mg, 7 gün"],
                    ["Vulvovajinal Kandidiyazis", "Beyaz peynirimsi, kokusuz", "< 4.5", "KOH bakısında psödohif ve maya", "Flukonazol 150 mg tek doz"],
                    ["Mukopürülan Servisit", "Endoservikal sarı-yeşil pürülan", "Değişken", "Servikal frajilite ve NAAT pozitifliği", "Seftriakson + Azitromisin"]
                ]
            ),
            make_chain(
                "Akıntı Sendromunda 3 Adımlı Ayırıcı Tanı",
                [
                    "1. pH Ölçümü: pH <4.5 ise Kandidiyazis; pH >4.5 ise BV veya Trikomonas.",
                    "2. Whiff Testi: KOH ile amin kokusu varsa BV tanısı güçlenir.",
                    "3. Mikroskopi: Clue cell varsa BV; psödohif varsa Kandida; trofozoit varsa Trikomonas."
                ]
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-17-s20",
        "title": "Bölüm Özeti: Vajinal Akıntıdan Üretrit Sendromuna Geçiş",
        "content": "Bölüm 2 boyunca kadınlarda sık görülen vajinit (BV, Kandida) ve servisit sendromlarının klinik ve laboratuvar ayrımını tamamladık:\n\n- **Kritik İlke:** Vajinal pH ölçümü (<4.5 vs >4.5) ve taze mikroskopi klinik ayırıcı tanıda en hızlı ve en ucuz anahtardır.\n- **Sonraki Bölüm:** Bir sonraki bölümde erkeklerde en sık görülen CYBE klinik sendromu olan **üretral akıntıyı**, **gonokokal üretrit ile nongonokokal üretrit (NGU) ayrımını** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Bakteriyel vajinoziste lam üzerine damlatılan yüzde 10 KOH ile açığa çıkan amin/balık kokusunu değerlendiren klinik testin adı nedir?",
                "Whiff testi (Koku testi)",
                "Amin kokusu açığa çıkarma testi"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi vulvovajinal kandidiyazisi bakteriyel vajinozisten ayıran en kesin laboratuvar bulgusudur?",
                [
                    {"key": "A", "text": "Vajinal pH'nın kandidiyaziste normal asidik (<4.5) olması, BV'de ise >4.5 olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kandidiyaziste vajinal pH daima normal asidiktir (<4.5), oysa BV'de laktobasil kaybıyla pH yükselir (>4.5)."},
                    {"key": "B", "text": "Kandidiyaziste clue cell görülmesi", "isCorrect": False, "explanation": "Clue cell BV'ye özgüdür."},
                    {"key": "C", "text": "Kandidiyazisin sadece erkeklerde görülmesi", "isCorrect": False, "explanation": "Kandidiyazis kadınlarda çok daha sıktır."},
                    {"key": "D", "text": "Kandidiyaziste Whiff testinin güçlü pozitif olması", "isCorrect": False, "explanation": "Whiff testi BV'de pozitiftir, kandidada negatiftir."}
                ]
            )
        ]
    })

    return slides
