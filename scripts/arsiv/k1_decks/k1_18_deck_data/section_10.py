# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_10_slides():
    slides = []

    # Slide 91
    slides.append({
        "id": "k1-18-s91",
        "title": "Korunma Düzeylerine Giriş: Hastalıkların Doğal Seyrinde Müdahale Noktaları",
        "content": "Halk sağlığının en temel operasyonel kavramı, hastalıkların doğal seyri boyunca uygulanan 'Korunma Düzeyleri'dir (Levels of Prevention) (Sınav Spotu):\n\n- **Hastalığın Doğal Seyri (Natural History of Disease):**\n  - Bir hastalık hiçbir tıbbi müdahale yapılmadığında; duyarlılık (risk) dönemi $\\to$ subklinik (pre-semptomatik patolojik) dönem $\\to$ klinik (semptomatik) dönem $\\to$ iyileşme, sakatlık veya ölüm aşamalarından geçer.\n- **Dört Temel Korunma Düzeyi:**\n  1. **Primordial (Temel/Öncül) Korunma:** Risk faktörünün henüz toplumda ve bireyde **hiç ortaya çıkmamasını** sağlamak.\n  2. **Birincil (Primer) Korunma:** Risk faktörü vardır ancak hastalık henüz başlamamıştır; **hastalığın oluşmasını (insidansını) engellemek**.\n  3. **İkincil (Sekonder) Korunma:** Hastalık başlamıştır ancak belirti vermemiştir; **pre-semptomatik dönemde erken tanı koyup ilerlemeyi durdurmak** (taramalar).\n  4. **Üçüncül (Tersiyer) Korunma:** Klinik hastalık yerleşmiştir; **komplikasyonları önlemek, sakatlığı sınırlandırmak ve hastayı rehabilite etmek**.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Korunma Düzeyi", "Uygulandığı Evre", "Temel Amaç", "Müdahale Türü"],
                [
                    ["Primordial Korunma", "Risk faktörü henüz yokken", "Risk yaratan sosyal/çevresel yaşam tarzını önleme", "Mevzuat, vergilendirme, çocuk eğitimi"],
                    ["Birincil (Primer)", "Risk faktörü varken, hastalık yokken", "Yeni vaka oluşumunu (insidansı) engelleme", "Aşılama, dengeli beslenme, kondom, temiz su"],
                    ["İkincil (Sekonder)", "Hastalık var, belirti yok (subklinik)", "Erken tanı ile hastalığın ilerlemesini durdurma", "Tarama testleri (Smear, mamografi, tansiyon)"],
                    ["Üçüncül (Tersiyer)", "Klinik hastalık var, yerleşmiş", "Sakatlığı önleme ve topluma kazandırma", "Rehabilitasyon, fizyoterapi, komplikasyon önleme"]
                ]
            ),
            make_cloze(
                "Hastalıkların doğal seyrinde risk faktörünün toplumda ve bireyde henüz hiç ortaya çıkmasını engellemeye yönelik en erken korunma basamağı primordial korunmadır.",
                "primordial",
                "Sosyal ve çevresel yaşam tarzı risklerini baştan önleyen korunma düzeyi"
            )
        ]
    })

    # Slide 92
    slides.append({
        "id": "k1-18-s92",
        "title": "Primordial Korunma: Risk Faktörlerinin Sosyal ve Kültürel Oluşumunu Önleme",
        "content": "Primordial korunma, 20. yüzyılın sonlarında kronik hastalıkların patlamasıyla tanımlanan en çağdaş korunma basamağıdır (Sınav Spotu):\n\n- **Tanım ve Amaç:**\n  - Hastalık riskini artıran **sosyal, ekonomik, çevresel ve kültürel yaşam tarzı özelliklerinin toplumda hiç oluşmamasını sağlamaktır**.\n  - Hedef belirli bir hasta değil; tüm toplum, çocuklar ve gelecek nesillerdir.\n  - Altta yatan makro nedenlerle mücadele edilir; sürekli devlet desteği, yasalar ve politik kararlılık gerektirir.\n- **Karakteristik Örnekler:**\n  - **Çocukların Hiç Sigaraya Başlamaması:** İlkokul çağından itibaren okullarda sigara karşıtı eğitim verilmesi, tütün reklamlarının yasaklanması ve tütüne yüksek vergiler konulması.\n  - **Obezitenin Baştan Engellenmesi:** Çocukların fast-food ve doymuş yağ tüketimini kısıtlayan okul kantini yasaları, kentlerde bisiklet yolları ve parklar inşa edilmesi.\n  - Doymuş hayvansal yağ tüketiminin gelenek haline gelmesinin önlenmesi (koroner kalp hastalığını önler).",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Primordial Korunma vs Birincil Korunma",
                "Primordial Korunma (Risk Yok)",
                "Çocuğun hiç sigaraya başlamamasını sağlamak; toplumsal risk ortamını yasalar ve eğitimle baştan engellemek.",
                "Birincil Korunma (Risk Var)",
                "Günde 1 paket sigara içen erişkine sigarayı bıraktırma danışmanlığı verip akciğer kanseri olmasını önlemek."
            ),
            make_quiz(
                "İlkokul çağındaki çocukların sigaraya hiç başlamaması için okullarda bilinçlendirme yapılması ve tütün ürünlerine yüksek caydırıcı vergiler konulması hangi korunma düzeyine örnektir?",
                [
                    {"key": "A", "text": "Primordial korunma", "isCorrect": True, "explanation": "Doğru cevap A'dır: Risk faktörünün (sigara içme alışkanlığı) bireyde ve toplumda hiç oluşmamasını sağlamak primordial korunmadır."},
                    {"key": "B", "text": "İkincil korunma", "isCorrect": False, "explanation": "Kanser taramasıdır."},
                    {"key": "C", "text": "Üçüncül korunma", "isCorrect": False, "explanation": "Kanser ameliyatı sonrası bakımdır."},
                    {"key": "D", "text": "Palyatif korunma", "isCorrect": False, "explanation": "Ağrı dindirme tedavisidir."}
                ]
            )
        ]
    })

    # Slide 93
    slides.append({
        "id": "k1-18-s93",
        "title": "Birincil (Primer) Korunma: Hastalık Oluşmadan Etkenden Kaçınma ve Aşı",
        "content": "Birincil korunma, risk faktörleriyle karşılaşmış veya karşılaşabilecek bireylerde hastalığın patolojik başlangıcını durdurur (Sınav Spotu):\n\n- **Tanım ve Temel Hedef:**\n  - Hastalık oluşmadan önce etkenden kaçınmak veya direnci artırmak;\n  - **Hastalığın İnsidansını (yeni vaka görülme hızını) ve prevalansını düşürmek**, şiddetini hafifletmek ve erken ölümleri önlemektir.\n- **Birincil Korunmanın Klasik Örnekleri:**\n  1. **Bağışıklama (Aşılama):** Çiçek, kızamık, çocuk felci, difteri ve tetanos aşıları.\n  2. **Yeterli ve Dengeli Beslenme:** İyotlu tuz kullanımı (guatrı önler), folik asit takviyesi (nöral tüp defektini önler).\n  3. **Güvenli Çevre ve Temizlik:** İçme suyunun klorlanması, el yıkama alışkanlığı.\n  4. **Kazalardan Korunma:** Emniyet kemeri ve kask takılması, işyerinde kişisel koruyucu donanım.\n  5. **Aile Planlaması ve Genetik:** Akraba evliliklerinin önlenmesi, düşük doğum ağırlıklı (DDA) doğumların engellenmesi.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Birincil Korunmanın İnsidansı Düşürme Mekanizması",
                [
                    "1. Risk Maruziyeti: Birey mikropla veya zararlı etkenle temas halindedir.",
                    "2. Birincil Müdahale: Aşı yapılır, kondom takılır veya emniyet kemeri bağlanır.",
                    "3. Doku Hasarı Engellenir: Etken vücuda giremez veya antikorlarla anında nötralize edilir.",
                    "4. Sıfır Yeni Vaka: Toplumda yeni hastalık vakası (insidans) görülmez."
                ]
            ),
            make_cloze(
                "Hastalığın henüz hiç oluşmadığı evrede yeni vaka sayısını yani insidansı düşürmek amacıyla yapılan aşılama ve su klorlama uygulamaları birincil korunma düzeyindedir.",
                "birincil",
                "Aşılama ve hijyen uygulamalarını kapsayan primer korunma basamağı"
            )
        ]
    })

    # Slide 94
    slides.append({
        "id": "k1-18-s94",
        "title": "İkincil (Sekonder) Korunma: Pre-semptomatik Erken Tanı ve Taramalar",
        "content": "İkincil korunma, hastalık patolojik olarak başlamış olmasına rağmen hastanın henüz hiçbir şikayetinin bulunmadığı evrede devreye girer (Sınav Spotu):\n\n- **Tanım ve Temel Hedef:**\n  - Kronik veya bulaşıcı bir hastalığın **pre-semptomatik (belirti öncesi / subklinik) dönemde erken tanısı** ile ilerlemesini, sakatlık bırakmasını ve ölüme yol açmasını engellemektir.\n- **Klinik Taramalar (Screening):**\n  - Görünüşte tamamen sağlıklı olan nüfusa basit, hızlı ve güvenilir testler uygulanarak gizli hastaların saptanmasıdır.\n- **İkincil Korunmanın Klasik Örnekleri:**\n  1. **Serviks Kanseri Taraması:** Sağlıklı kadınlara rutin **Pap-smear veya HPV-DNA** testi yapılması (kanser başlamadan displaziyi yakalar).\n  2. **Meme Kanseri Taraması:** 40 yaş üstü kadınlarda rutin **mamografi** çekilmesi.\n  3. **Hipertansiyon Taraması:** Asemptomatik bireylerde rutin kan basıncı ölçümü.\n  4. **Yenidoğan Taramaları:** Topuk kanı ile Fenilketonüri, Konjenital Hipotiroidi tespiti.\n  5. **Tüberkülin (PPD) Testi** ve çocuklarda görme-işitme taramaları.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Birincil Korunma (HPV Aşısı) vs İkincil Korunma (Pap-Smear Taraması)",
                "Birincil Korunma (HPV Aşısı)",
                "Virüsün vücuda girmesini baştan engeller; hücresel hasar ve displazi hiç oluşmaz.",
                "İkincil Korunma (Pap-Smear)",
                "Hücrede kanser öncesi displazi başlamıştır; belirti vermeden erken yakalanıp lezyon yakılır/çıkarılır."
            ),
            make_quiz(
                "Hiçbir şikayeti olmayan sağlıklı bir kadında serviks kanserini henüz belirti vermeden yakalamak amacıyla yapılan rutin Pap-smear testi hangi korunma düzeyine girer?",
                [
                    {"key": "A", "text": "İkincil (sekonder) korunma", "isCorrect": True, "explanation": "Doğru cevap A'dır: Belirti öncesi dönemde tarama testleriyle erken tanı koymak ikincil korunmadır."},
                    {"key": "B", "text": "Birincil korunma", "isCorrect": False, "explanation": "HPV aşısı birincil korunmadır."},
                    {"key": "C", "text": "Primordial korunma", "isCorrect": False, "explanation": "Risk faktörünün oluşmasını önlemektir."},
                    {"key": "D", "text": "Üçüncül korunma", "isCorrect": False, "explanation": "İlerlemiş kanser cerrahisi ve radyoterapidir."}
                ]
            )
        ]
    })

    # Slide 95
    slides.append({
        "id": "k1-18-s95",
        "title": "Taramaların Halk Sağlığı İlkeleri: Ne Zaman, Kime ve Nasıl?",
        "content": "Her hastalık için tarama testi yapılamaz; bir tarama programının halk sağlığı açısından uygulanabilir olması katı bilimsel ölçütlere bağlıdır (Wilson & Jungner İlkeleri) (Sınav Spotu):\n\n- **1. Hastalığın Önemi:** Aranan hastalık toplumda sık görülen, öldüren veya sakat bırakan **önemli bir sağlık sorunu** olmalıdır.\n- **2. Tanınabilir Pre-semptomatik Dönem:** Hastalığın belirti vermeden önce tespit edilebilecek makul uzunlukta bir gizli evresi bulunmalıdır.\n- **3. Kabul Edilebilir Test:** Tarama testi basit, ucuz, ağrısız, güvenli, duyarlılığı (sensitivite) ve özgüllüğü (spesifite) yüksek olmalıdır.\n- **4. Tedavi Olanağı:** Erken yakalanan hastalığın **kanıtlanmış, etkili ve ulaşılabilir bir tedavisi** bulunmalıdır (tedavisi olmayan ölümcül bir hastalığı erken taramak etik değildir).\n- **5. Maliyet-Etkinlik:** Taramaya harcanan para, geç kalınmış vakaların getireceği devasa tedavi giderlerinden daha ekonomik olmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Tarama Kriteri", "Gereklilik Gerekçesi", "Hatalı Uygulama Örneği"],
                [
                    ["Önemli Sağlık Sorunu", "Toplum yükünün yüksek olması", "Milyonda bir görülen zararsız lezyonları taramak"],
                    ["Kabul Edilebilir Test", "Halkın teste gönüllü katılması", "Ağrılı, tehlikeli veya aşırı pahalı biyopsilerle tarama yapmak"],
                    ["Etkili Tedavi Varlığı", "Erken tanının hastaya fayda sağlaması", "Tedavisi ve durdurulma çaresi olmayan genetik ölümcül tabloyu taramak"],
                    ["Maliyet-Etkinlik", "Ekonomik kaynakların geri dönüşü", "Bütçeyi tüketen aşırı pahalı taramalar"]
                ]
            ),
            make_quiz(
                "Halk sağlığında bir hastalığın kitle taraması programına alınabilmesi için aşağıdakilerden hangisi vazgeçilmez bir ön koşuldur?",
                [
                    {"key": "A", "text": "Erken tanı konulduğunda hastanın yaşamını kurtaran kanıtlanmış etkili bir tedavisinin bulunması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tedavisi veya müdahalesi olmayan bir hastalığı erken taramanın hastaya faydası yoktur, etik değildir."},
                    {"key": "B", "text": "Testin yalnızca cerrahi anestezi altında uygulanabilmesi", "isCorrect": False, "explanation": "Tarama testleri basit ve non-invaziv olmalıdır."},
                    {"key": "C", "text": "Hastalığın toplumda hiç görülmeyen egzotik bir enfeksiyon olması", "isCorrect": False, "explanation": "Hastalık toplum için önemli olmalıdır."},
                    {"key": "D", "text": "Testin yalnızca özel kliniklerde ücret karşılığı yapılması", "isCorrect": False, "explanation": "Halk sağlığı ilkelerine aykırıdır."}
                ]
            )
        ]
    })

    # Slide 96
    slides.append({
        "id": "k1-18-s96",
        "title": "Üçüncül (Tersiyer) Korunma: Sakatlığı Sınırlama ve Rehabilitasyon",
        "content": "Üçüncül korunma, hastalığın erken evresi kaçırılmış ve klinik tablo yerleşmiş hastalarda devreye giren son savunma hattıdır (Sınav Spotu):\n\n- **Tanım ve Temel Hedef:**\n  - İlerlemiş hastalarda **komplikasyonları önlemek, doku/organ kaybını ve sakatlığı sınırlandırmak**;\n  - Hastayı fiziksel, psikolojik ve sosyal olarak **rehabilite edip yeniden üretken yaşama kazandırmaktır**.\n- **Karakteristik Örnekler:**\n  1. **Diyabette Ayak Amputasyonunun Önlenmesi:** Diyabetik hastaya düzenli ayak bakımı eğitimi, özel tabanlık verilmesi ve gangren gelişiminin engellenmesi.\n  2. **Diyabetik Retinopati Takibi:** Göz dibi lazer tedavisiyle körlüğün engellenmesi.\n  3. **İnme (Felç) Sonrası Fizyoterapi:** İnme geçiren hastaya erken fizyoterapi ve konuşma terapisi uygulanarak hastanın yatağa bağımlı kalmasının önlenmesi.\n  4. **Miyokard Enfarktüsü Sonrası Kardiyak Rehabilitasyon.**",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "İkincil Korunma (Açlık Şekeri Taraması) vs Üçüncül Korunma (Diyabetik Ayak Bakımı)",
                "İkincil Korunma (Erken Tanı)",
                "Asemptomatik bireyde kan şekeri ölçülerek diyabet henüz organlara hasar vermeden yakalanır.",
                "Üçüncül Korunma (Rehabilitasyon)",
                "Diyabetik nöropatisi olan hastaya özel ayakkabı verilerek ayak ülseri ve bacak amputasyonu önlenir."
            ),
            make_cloze(
                "Klinik olarak diyabet tanısı almış bir hastada kangren gelişimini ve bacak amputasyonunu engellemek amacıyla yapılan ayak bakımı ve rehabilitasyon üçüncül korunma düzeyindedir.",
                "üçüncül",
                "Sakatlığı sınırlama ve rehabilitasyonu kapsayan tersiyer korunma basamağı"
            )
        ]
    })

    # Slide 97
    slides.append({
        "id": "k1-18-s97",
        "title": "Halk Sağlığı Uzmanının Görevleri: Araştırma, Salgın İnceleme ve Yönetim",
        "content": "Halk sağlığı uzmanlığı (tıpta uzmanlık dalı), klinik hekimlikten farklı olarak toplumu bir bütün olarak yöneten liderlik alanıdır (Sınav Spotu):\n\n- **1. Toplumun Sağlık Düzeyini ve Sorunlarını Saptamak:**\n  - Biyoistatistik ve epidemiyolojik tekniklerle hastalık sıklığını (insidans, prevalans, mortalite) ölçmek ve nedensel risk faktörlerini belirlemek.\n- **2. Politika ve Program Geliştirmek:**\n  - Toplumun önceliklerine göre aşı, tarama ve çevre sağlığı programları planlamak, yürütmek ve etkinliğini değerlendirmek.\n- **3. Salgınların İncelenmesi (Outbreak Investigation):**\n  - Bir salgın patlak verdiğinde filyasyon ekiplerini yönetmek, salgının kaynağını tespit etmek ve yayılımı durdurmak.\n- **4. Sağlık Yöneticiliği ve Liderlik:**\n  - Sağlık Bakanlığı, il sağlık müdürlükleri, toplum sağlığı merkezleri ve hastanelerde planlama, personel eşgüdümü, bütçe ve denetleme görevlerini üstlenmek.\n- **5. Sağlık Eğitimi ve Halk Sağlığı Laboratuvarları:** Halkı bilinçlendirmek ve su/gıda analiz laboratuvarlarını işletmek.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Halk Sağlığı Uzmanının Görev Alanı", "Uygulanan Yöntem", "Somut Çıktı"],
                [
                    ["Salgın İncelemesi", "Saha filyasyonu ve vaka-kontrol analizi", "Salgın kaynağının kapatılması"],
                    ["Sağlık Politikası", "Maliyet-etkinlik ve risk analizi", "Ulusal aşı ve tarama takvimi"],
                    ["Sağlık Eğitimi", "Kitle iletişimi ve okul programları", "Toplumda olumlu sağlık davranışı gelişimi"],
                    ["Sağlık Yönetimi", "Planlama, bütçe ve denetleme", "Entegre birinci basamak teşkilatlanması"]
                ]
            ),
            make_quiz(
                "Aşağıdakilerden hangisi bir halk sağlığı uzmanının temel görev ve yetki alanları arasında yer almaz?",
                [
                    {"key": "A", "text": "Hastanede tek bir hastanın açık kalp ameliyatını bizzat gerçekleştirmek", "isCorrect": True, "explanation": "Doğru cevap A'dır: Açık kalp cerrahisi kalp-damar cerrahının görevidir; halk sağlığı uzmanı koruyucu programları, salgınları ve toplum sağlığını yönetir."},
                    {"key": "B", "text": "Toplumda patlak veren bir kolera veya kızamık salgınını sahada inceleyip kaynağını durdurmak", "isCorrect": False, "explanation": "Temel halk sağlığı görevidir."},
                    {"key": "C", "text": "Toplumun sağlık düzeyini, bebek ölüm hızını ve risk faktörlerini bilimsel yöntemlerle ölçmek", "isCorrect": False, "explanation": "Epidemiyolojik asli görevdir."},
                    {"key": "D", "text": "Halk sağlığı laboratuvarlarında içme sularının mikrobiyolojik analizini denetlemek", "isCorrect": False, "explanation": "Çevre sağlığı görevidir."}
                ]
            )
        ]
    })

    # Slide 98
    slides.append({
        "id": "k1-18-s98",
        "title": "Sağlığı Etkileyen Faktörlerin Dönüşümü: Geçmiş vs Günümüz",
        "content": "İnsanlık son iki yüzyılda ölüm nedenlerinde ve sağlığı tehdit eden faktörlerde radikal bir epidemiyolojik geçiş (epidemiologic transition) yaşamıştır (Sınav Spotu):\n\n- **Geçmişte İnsanlığı Tehdit Edenler:**\n  - Veba, kolera, çiçek gibi kitlesel **bulaşıcı salgın hastalıklar**.\n  - Yetersiz ve tek taraflı beslenme (kıtlık, skorbüt, pellegra).\n  - Doğum ve gebelik komplikasyonlarına bağlı yüksek anne-bebek ölümleri.\n  - Bağışıklamanın ve temiz su altyapısının bulunmaması.\n- **Günümüzde Sağlığı Tehdit Edenler:**\n  - **Kronik bulaşıcı olmayan hastalıklar:** Kardiyovasküler hastalıklar, kanserler, obezite ve Tip 2 diyabet.\n  - Hareketsiz (sedanter) yaşam, tütün ve alkol kullanımı, kronik stres ve tükenmişlik.\n  - Çevre kirliliği, mikroplastikler ve küresel iklim krizi.\n- **Başarılanlar:** Örgütlenmiş sağlık hizmetleri, etkin aşılar ve sanitasyon sayesinde insan ömrü 35-40 yıldan 75-80 yıla çıkmıştır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Dönem", "Başlıca Tehditler", "Temel Mücadele Aracı", "Ortalama Yaşam Beklentisi"],
                [
                    ["Geçmiş Dönem", "Bulaşıcı salgınlar, malnütrisyon, anne-bebek ölümü", "Karantina, temiz su şebekesi, aşılar", "35-40 yıl"],
                    ["Günümüz Dönemi", "Kalp-damar, kanser, diyabet, obezite, sedanter yaşam", "Yaşam tarzı değişimi, taramalar, primordial koruma", "75-82 yıl"]
                ]
            ),
            make_cloze(
                "Geçmişte ölüm nedenleri arasında bulaşıcı enfeksiyonlar ön plandayken günümüzde kalp damar hastalıkları, kanserler ve obezite gibi bulaşıcı olmayan kronik hastalıklar birinci sıraya geçmiştir.",
                "bulaşıcı olmayan",
                "Günümüzde ölümlerin çoğundan sorumlu olan kronik hastalıklar grubu"
            )
        ]
    })

    # Slide 99
    slides.append({
        "id": "k1-18-s99",
        "title": "21. Yüzyılda Halk Sağlığı Gündemi: Pandemiler ve Küresel Tehditler",
        "content": "21. yüzyılda halk sağlığı, küreselleşen dünyanın yeni ve karmaşık tehditleriyle karşı karşıyadır (Sınav Spotu):\n\n- **1. Yeni ve Yeniden Hortlayan Salgınlar (Emerging/Re-emerging):**\n  - COVID-19 pandemisi, SARS, MERS, Kuş Gribi ve Mpox gibi zoonotik virüsler;\n  - Dünyanın herhangi bir noktasında çıkan bir virüsün uçaklarla 24 saatte tüm kıtalara yayılabileceğini kanıtlamıştır.\n- **2. Antimikrobiyal Direnç (AMR):**\n  - Antibiyotiklerin bilinçsiz ve aşırı tüketimi sonucu bakteriler direnç kazanmakta; 'antibiyotik öncesi karanlık çağa' dönme riski doğmaktadır.\n- **3. İklim Krizi ve Çevre Sağlığı:**\n  - Küresel ısınma nedeniyle sıtma ve Dang taşıyan sivrisineklerin kuzeye göç etmesi, aşırı sıcak dalgaları, kuraklık ve su kıtlığı.\n- **4. Aşı Kararsızlığı ve Dezenformasyon:**\n  - Sosyal medyada yayılan bilim dışı aşı karşıtlığı kızamık salgınlarını yeniden tetiklemektedir.\n- **Çözüm:** **'Tek Sağlık' (One Health)** yaklaşımı — insan, hayvan ve çevre sağlığının birbirinden ayrılamaz bir bütün olarak korunması.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Klasik İnsan Odaklı Sağlık vs 'Tek Sağlık' (One Health) Yaklaşımı",
                "Klasik İnsan Odaklı Sağlık",
                "Yalnızca insan hekimliğine odaklanır; vahşi doğayı ve veteriner halk sağlığını ihmal eder.",
                "Tek Sağlık (One Health)",
                "İnsan, hayvan ve ekosistem sağlığını bir arada ele alarak zoonotik pandemileri kaynağında engeller."
            ),
            make_quiz(
                "İnsan, hayvan ve çevre sağlığının birbirinden ayrılamaz bir bütün olduğunu ve zoonotik pandemilerle ancak bu üçlü işbirliğiyle mücadele edilebileceğini savunan çağdaş halk sağlığı yaklaşımı hangisidir?",
                [
                    {"key": "A", "text": "Tek Sağlık (One Health) yaklaşımı", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tek Sağlık (One Health) insan, veteriner ve ekolojik sağlığı bütünleştiren çağdaş halk sağlığı vizyonudur."},
                    {"key": "B", "text": "Yalnızca biyomedikal laboratuvar yaklaşımı", "isCorrect": False, "explanation": "Hayvan ve çevre boyutunu içermez."},
                    {"key": "C", "text": "Miazma temizleme protokolü", "isCorrect": False, "explanation": "19. yüzyıl miazma görüşüdür."},
                    {"key": "D", "text": "Yalnızca tele-tıp uygulaması", "isCorrect": False, "explanation": "Dijital iletişim aracıdır."}
                ]
            )
        ]
    })

    # Slide 100 - CHECKPOINT 10
    slides.append({
        "id": "k1-18-s100",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Korunma Düzeyleri ve Halk Sağlığı Büyük Özeti",
        "content": "Bu son checkpoint ile Halk Sağlığı Tarihçesi dersinin tüm kurucu ilkelerini ve korunma düzeylerini özetliyoruz:\n\n- **Halk Sağlığı:** Winslow (1920) 'bilim ve sanat', Fişek 'ana rahminden ölüme bütüncül hizmet ve bilim dalı' olarak tanımladı.\n- **Tarihsel Öncüler:**\n  - Hipokrat: Doğal nedenler, Humoral patoloji, 'Primum non nocere'.\n  - Razi: Et asarak hastane yeri seçimi; İbn-i Sina: 'El-Kanun'.\n  - Jenner (1796): Sığır çiçeğiyle aşılama ('vaccine'); Pasteur: Abiyogenezi çürüttü, pastörizasyon, kuduz aşısı; Koch: Tüberküloz ve kolera basili, postülatlar.\n  - John Snow (1854): Broad Street tulumbası, çevre sağlığı ve epidemiyolojinin babası.\n  - James Lind (1753): Skorbüt ve narenciye ilk kontrollü klinik deneyi; Ramazzini (1700): İş sağlığının babası ('Ne iş yaparsınız?').\n  - Grotjahn (1912): Sosyal patoloji; Fişek (1961): 224 sayılı kanun ve Sağlık Ocakları; Alma-Ata (1978): Temel Sağlık Hizmetleri.\n- **Korunma Düzeyleri:**\n  - Primordial: Risk oluşmadan yaşam tarzını önleme (çocuklara sigara/obezite yasağı).\n  - Birincil: Hastalık oluşmadan etkenden kaçınma (Aşılama, su klorlama).\n  - İkincil: Pre-semptomatik erken tanı (Smear, mamografi, tansiyon taraması).\n  - Üçüncül: Sakatlığı önleme ve rehabilitasyon (Diyabetik ayak bakımı).",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Korunma Basamağı", "Hedef Kitle", "Müdahale Örneği", "Temel Çıktı"],
                [
                    ["Primordial Korunma", "Tüm toplum / Çocuklar", "Okullarda sigara karşıtı yasalar, obezite önleme", "Risk faktörünün hiç oluşmaması"],
                    ["Birincil (Primer) Korunma", "Risk altındaki nüfus", "Genişletilmiş aşı takvimi, temiz içme suyu", "Yeni vaka oluşumunun (insidans) durması"],
                    ["İkincil (Sekonder) Korunma", "Gizli / Belirtisiz hastalar", "Pap-smear, mamografi, topuk kanı taraması", "Pre-semptomatik erken tanı ve kür"],
                    ["Üçüncül (Tersiyer) Korunma", "Klinik tanılı hastalar", "Diyabetik ayak bakımı, inme sonrası fizyoterapi", "Sakatlığın önlenmesi ve rehabilitasyon"]
                ]
            ),
            make_chain(
                "Halk Sağlığının Bütüncül Başarı Zinciri",
                [
                    "1. Primordial Koruma: Sağlıklı nesiller için zararlı yaşam tarzının baştan önlenmesi.",
                    "2. Birincil Koruma: Aşı ve sanitasyonla enfeksiyon insidansının düşürülmesi.",
                    "3. İkincil Koruma: Taramalarla kronik hastalıkların sessiz evrede yakalanması.",
                    "4. Üçüncül Koruma: İlerlemiş vakaların rehabilite edilerek hayata bağlanması."
                ]
            )
        ]
    })

    return slides
