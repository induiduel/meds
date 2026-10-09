# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_4_slides():
    slides = []

    # Slide 31
    slides.append({
        "id": "k1-17-s31",
        "title": "Trichomonas vaginalis Biyolojisi: Kistsiz Kamçılı Trofozoit",
        "content": "Trikomoniyazis, dünyada viral olmayan en yaygın cinsel yolla bulaşan enfeksiyondur (DSÖ'ye göre yılda ~160 milyon vaka):\n\n- **Taksonomi ve Biyoloji:** Trichomonas vaginalis, anaerobik, tek hücreli, kamçılı (flagellat) bir protozoondur.\n- **Kritik Biyolojik Özellik (Sınav Spotu):**\n  - Giardia veya Entamoeba gibi bağırsak parazitlerinin aksine, **Trichomonas vaginalis'in kist formu YOKTUR**.\n  - Yalnızca hareketli **trofozoit formu** bulunur.\n  - Bu morfolojik kısıtlılık nedeniyle parazit dış ortam koşullarına (kuruma, sıcaklık değişimi) son derece dayanıksızdır; dakikalar içinde ölür.\n  - Dolayısıyla enfeksiyon klozet kapağından veya havludan değil; **neredeyse istisnasız doğrudan cinsel temasla** kişiden kişiye bulaşır.\n- **Hücresel Tutunma:** Parazit dört ön kamçısı ve bir dalgalı zarı (undulating membrane) ile vajina ve üretra epitel hücrelerine tutunur; glikojenle beslenir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Bağırsak Protozoonları (Kistli) vs Trichomonas vaginalis (Kistsiz)",
                "Bağırsak Parazitleri (Amipler/Giardia)",
                "Dirençli kist formları vardır; dış ortamda aylarca yaşar; kontamine su ve gıdayla fekal-oral bulaşır.",
                "Trichomonas vaginalis",
                "Kist formu yoktur, sadece trofozoittir; dış ortamda hızla ölür ve mutlak doğrudan cinsel temasla bulaşır."
            ),
            make_cloze(
                "Trichomonas vaginalis parazitinin dış ortamda dayanıklı kist formu bulunmaz ve sadece trofozoit formuyla enfeksiyon yapar.",
                "trofozoit",
                "Protozoonun hareketli ve aktif vejetatif formu"
            )
        ]
    })

    # Slide 32
    slides.append({
        "id": "k1-17-s32",
        "title": "Trikomoniyazis Kliniği: Köpüklü Akıntı ve 'Çilek Serviks'",
        "content": "Trikomoniyazis kadınlarda florayı şiddetli bir yangıyla altüst eder (Sınav Spotu):\n\n- **Karakteristik Akıntı:**\n  - Bol miktarda, homojen, **köpüklü, sarı-yeşil veya gri renkli ve kötü kokulu** bir vajinal akıntıdır.\n  - Akıntının köpüklü olması parazitin metabolik gaz üretmesinden ve lökosit lizisinden kaynaklanır.\n- **Vajinal pH:** Parazitin laktobasilleri tüketmesi sonucu vajinal ortam bazikleşir; **vajinal pH belirgin şekilde yükselir (pH > 4.5, sıklıkla 5.0-6.0)**.\n- **Çilek Serviks (Kolpitis Makülaris - Patognomonik Bulgu):**\n  - Hastaların yaklaşık %2-5'inde çıplak gözle, kolposkopide ise %40'tan fazlasında izlenir.\n  - Serviks ve vajina üst kubbesinde parazitin epitel hasarı ve kapiller ektaziye yol açmasıyla **kırmızı punktat mikro-kanama odakları** belirir; serviks tıpkı olgun bir çileğin dış yüzeyine benzer (çilek serviks).",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Klinik Özellik", "Trichomonas vaginalis Bulgusu", "Patofizyolojik Neden"],
                [
                    ["Akıntı Tipi", "Köpüklü, bol, sarı-yeşil, kötü kokulu", "Paraziter metabolitler ve yoğun nötrofil birikimi"],
                    ["Vajinal pH", "pH > 4.5 (genellikle 5.5 - 6.5)", "Laktobasillerin ölmesi ve asitliğin kaybolması"],
                    ["Serviks Görünümü", "'Çilek serviks' (Kolpitis makülaris)", "Mukozada noktasal mikro-kanamalar ve kapiller genişleme"],
                    ["Vulvar Semptom", "Şiddetli kaşıntı, vulvada yanma, dizüri", "Eksudanın vulvayı tahriş etmesi"]
                ]
            ),
            make_quiz(
                "Jinekolojik spekulum muayenesinde servikal mukozada kırmızı noktasal mikro-kanamalarla seyreden 'çilek serviks' (kolpitis makülaris) ve köpüklü sarı-yeşil akıntı saptanan hastada etken hangisidir?",
                [
                    {"key": "A", "text": "Candida albicans", "isCorrect": False, "explanation": "Candida peynirimsi beyaz akıntı yapar, çilek serviks yapmaz."},
                    {"key": "B", "text": "Trichomonas vaginalis", "isCorrect": True, "explanation": "Doğru cevap B'dir: Köpüklü sarı-yeşil akıntı ve çilek serviks manzarası Trichomonas vaginalis için patognomoniktir."},
                    {"key": "C", "text": "Gardnerella vaginalis", "isCorrect": False, "explanation": "BV gri-beyaz ince akıntı yapar, eritem veya çilek serviks yapmaz."},
                    {"key": "D", "text": "Treponema pallidum", "isCorrect": False, "explanation": "Sert ağrısız şankr yapar."}
                ]
            )
        ]
    })

    # Slide 33
    slides.append({
        "id": "k1-17-s33",
        "title": "Taze Mikroskopi (Serum Fizyolojik Bakısı): Hareketli Trofozoitler",
        "content": "Trikomoniyazis tanısı hasta başında mikroskop altında saniyeler içinde doğrulanabilir (Sınav Spotu):\n\n- **Serum Fizyolojik (Wet-Mount) İncelemesi:**\n  - Arka forniksten alınan bir damla akıntı lam üzerine konur, bir damla ılık serum fizyolojik ile karıştırılıp lamel kapatılır.\n  - Işık mikroskobunda 40x büyütmede hemen incelenmelidir (soğudukça parazitin hareketi durur).\n- **Mikroskopik Bulgular:**\n  - Lökositlerden biraz daha büyük (yaklaşık 15-20 μm), armut veya oval biçimli hücreler görülür.\n  - **Aktif Kamçı Hareketi:** Parazitin ön kamçıları ve dalgalı zarı sayesinde **düzensiz, dönme ve sıçrama benzeri karakteristik canlı hareketler** sergilediği izlenir.\n  - Sahada parazite eşlik eden yüzlerce aktif parçalanmış nötrofil lökosit mevcuttur.\n- **Duyarlılık Sınırı:** Wet-mount bakısının duyarlılığı %50-70 civarındadır; şüpheli ancak mikroskopta parazit görülmeyen olgularda **NAAT veya antijen testleri** altın standart olarak devreye girer.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Serum Fizyolojik Taze Bakı vs Kültür/NAAT",
                "Taze SF Bakısı (Hasta Başı)",
                "Son derece hızlı ve ucuzdur; hareketli kamçılı parazit canlı görülürse anında kesin tanıdır.",
                "NAAT Testi",
                "Çok daha yüksek duyarlılığa sahiptir (>%98); parazit ölmüş veya az sayıda olsa bile DNA'sını yakalar."
            ),
            make_cloze(
                "Trikomoniyazis tanısında akıntının serum fizyolojik ile taze incelemesinde mikroskop altında aktif dönme hareketi yapan kamçılı trofozoitler izlenir.",
                "kamçılı trofozoitler",
                "SF taze bakısında izlenen canlı hareketli parazit hücreleri"
            )
        ]
    })

    # Slide 34
    slides.append({
        "id": "k1-17-s34",
        "title": "Trikomoniyaziste Standart Tedavi: Metronidazol 2 g Tek Doz",
        "content": "Trikomoniyazis tedavisinde nitroimidazol grubu antimikrobiyaller altın standarttır (Sınav Spotu):\n\n- **Birinci Basamak Standart Tedavi Protokolü:**\n  - **Metronidazol 2 g oral tek doz** (4 adet 500 mg tablet aynı anda yutulur).\n  - Alternatif Rejim: **Tinidazol 2 g oral tek doz** (yan etki profili daha hafiftir ve yarı ömrü daha uzundur).\n  - İkinci Alternatif (Özellikle Nüks veya Dirençte): Metronidazol 2x500 mg oral, 7 gün.\n- **Etki Mekanizması:**\n  - Metronidazol parazitin piruvat:ferredoksin oksidoredüktaz enzimiyle anaerobik ortamda nitro grubundan indirgenir.\n  - Açığa çıkan toksik serbest radikaller parazitin DNA sarmalını parçalayarak hızlı bakterisidal/protozoosidal ölüm sağlar.\n- **Topikal Tedavinin Başarısızlığı:**\n  - Vajinal ovül veya jeller paraziti yok etmede yetersizdir; çünkü T. vaginalis Skene ve Bartholin bezlerine ve üretraya da yerleşir; **bu nedenle tedavi mutlaka oral/sistemik olmalıdır**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["İlaç Adı", "Uygulama Şekli ve Dozu", "Tedavi Süresi", "Kür Oranı"],
                [
                    ["Metronidazol (Standart)", "2 g oral (4x500 mg)", "Tek doz", "%90 - 95"],
                    ["Tinidazol (Alternatif)", "2 g oral", "Tek doz", "%92 - 97"],
                    ["Metronidazol (Genişletilmiş)", "2x500 mg oral", "7 gün", "%95"],
                    ["Topikal Metronidazol Jel", "Vajinal jel", "5 gün", "Yetersiz (<%50 kür, önerilmez)"]
                ]
            ),
            make_quiz(
                "Trichomonas vaginalis enfeksiyonu saptanan erişkin bir hastada rehberlerin önerdiği standart birinci basamak tedavi protokolü nedir?",
                [
                    {"key": "A", "text": "Metronidazol 2 g oral, tek doz", "isCorrect": True, "explanation": "Doğru cevap A'dır: Trikomoniyaziste standart ilk seçenek tedavi Metronidazol 2 gram oral tek dozdur."},
                    {"key": "B", "text": "Azitromisin 1 g oral, tek doz", "isCorrect": False, "explanation": "Azitromisin klamidya ilacıdır, parazite etkisizdir."},
                    {"key": "C", "text": "Flukonazol 150 mg oral, tek doz", "isCorrect": False, "explanation": "Flukonazol mantar ilacıdır."},
                    {"key": "D", "text": "Topikal nistatin ovül", "isCorrect": False, "explanation": "Nistatin kandidiyazis içindir."}
                ]
            )
        ]
    })

    # Slide 35
    slides.append({
        "id": "k1-17-s35",
        "title": "Gebelikte Trikomoniyazis Yönetimi ve İlaç Güvenliliği",
        "content": "Trikomoniyazis gebelikte ciddi obstetrik komplikasyonlara zemin hazırlar (Sınav Spotu):\n\n- **Obstetrik Riskler:** Tedavi edilmemiş T. vaginalis enfeksiyonu erken membran rüptürü (EMR), erken doğum (preterm eylem) ve düşük doğum ağırlıklı bebek riskini anlamlı biçimde artırır.\n- **Gebelikte Tedavi Rejimi:**\n  - Güncel kılavuzlara ve CDC önerilerine göre: **Gebe kadınlarda da Metronidazol 2 g oral tek doz kullanılır**.\n  - Eskiden ilk trimesterde teratojenite endişesi taşınmaktaydı; ancak yapılan geniş ölçekli meta-analizler metronidazolün ilk trimester dahil konjenital anomali riskini artırmadığını kanıtlamıştır.\n- **Emzirme Dönemi Yönetimi:**\n  - Metronidazol anne sütüne geçer.\n  - Tek doz 2 g metronidazol alan annelere ilacı aldıktan sonraki **12-24 saat boyunca emzirmeye ara vermeleri**, sütü sağıp dökmeleri önerilir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Gebe Olmayan Hasta vs Gebe Hastada Trikomoniyazis Dozu",
                "Gebe Olmayan Hasta",
                "Metronidazol 2 g oral tek doz; alkol kısıtlaması; partner tedavisi uygulanır.",
                "Gebe Hasta",
                "Metronidazol 2 g oral tek doz güvenle verilir; erken doğum engellenir; emzirmede 12-24 saat ara verilir."
            ),
            make_cloze(
                "Gebelikte erken membran rüptürü ve erken doğum riskini artıran trikomoniyazis enfeksiyonunda gebelerde de oral metronidazol tek doz olarak güvenle uygulanır.",
                "metronidazol",
                "Gebelikte trikomoniyazis tedavisinde güvenle verilen antiprotozoal ajan"
            )
        ]
    })

    # Slide 36
    slides.append({
        "id": "k1-17-s36",
        "title": "Eşzamanlı Cinsel Partner Tedavisi ve 7 Gün Kuralı",
        "content": "Trikomoniyazis tedavisinin en sık başarısızlık nedeni tedavi edilmeyen partnerden yeniden enfeksiyon kapılmasıdır (Ping-Pong Enfeksiyonu - Sınav Spotu):\n\n- **Erkek Partnerin Rezervuar Rolü:**\n  - T. vaginalis bulaşan erkeklerin büyük kısmı (%70-80) tamamen asemptomatiktir; ancak üretra ve prostatlarında canlı parazit barındırırlar.\n  - Kadın tedavi edilip iyileşse bile, partneri tedavi edilmezse ilk cinsel ilişkide parazit kadına geri bulaşır (ping-pong etkisi).\n- **Altın Kurallar (Sınav Spotu):**\n  1. **Eşzamanlı Tedavi:** Hastanın tüm cinsel partnerleri asemptomatik dahi olsalar **aynı gün Metronidazol 2 g oral tek doz** ile tedavi edilmelidir.\n  2. **Yedi (7) Gün Cinsel Perhiz Kuralı:** İlaç tek doz verilse dahi, dokulardaki parazitlerin tamamen temizlenmesi ve mukozal iyileşme için **tedavi bitiminden sonra en az 7 gün boyunca her türlü cinsel ilişkiden kesinlikle kaçınılmalıdır**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_chain(
                "Ping-Pong Bulaş Zinciri ve Kırılma Basamakları",
                [
                    "1. İndeks Vakanın Başvurusu: Kadın semptomlarla hekime gelir ve trikomoniyazis saptanır.",
                    "2. Partnerin Tespiti: Semptomsuz erkek partner gizli taşıyıcı ve rezervuardır.",
                    "3. Eşzamanlı Tedavi: Her iki partnere aynı gün Metronidazol 2 g tek doz verilir.",
                    "4. 7 Gün Cinsel Perhiz: Bir hafta cinsel temas yasaklanarak reenfeksiyon önlenir."
                ]
            ),
            make_quiz(
                "Trichomonas vaginalis tanısı alıp tek doz 2 g metronidazol tedavisi verilen bir kadına reenfeksiyonu ve bulaşı önlemek için cinsel ilişki kısıtlaması hakkında ne söylenmelidir?",
                [
                    {"key": "A", "text": "İlacı yuttuktan 2 saat sonra hemen cinsel ilişkiye girebilir", "isCorrect": False, "explanation": "İki saatte parazit temizlenmez ve partner bulaşı sürer."},
                    {"key": "B", "text": "Hem kendisi hem partneri tedavi edilmeli ve tedavi bitiminden sonra en az 7 gün boyunca cinsel ilişkiden kaçınılmalıdır", "isCorrect": True, "explanation": "Doğru cevap B'dir: Trikomoniyaziste partner tedavisi zorunludur ve tedavi sonrası 7 gün cinsel perhiz şarttır."},
                    {"key": "C", "text": "Hasta 1 yıl boyunca hiçbir şekilde ilişkiye girmemelidir", "isCorrect": False, "explanation": "1 yıl gereksiz ve abartılı bir kısıtlamadır."},
                    {"key": "D", "text": "Partnerin tedavi olmasına hiç gerek yoktur", "isCorrect": False, "explanation": "Partner tedavi edilmezse ping-pong reenfeksiyonu gelişir."}
                ]
            )
        ]
    })

    # Slide 37
    slides.append({
        "id": "k1-17-s37",
        "title": "Metronidazol Yan Etkileri ve Disülfiram Benzeri Reaksiyon",
        "content": "Metronidazol ve tinidazol kullanan hastalara verilmesi gereken en hayati farmakolojik uyarı alkol etkileşimidir (Sınav Spotu):\n\n- **Ağızda Metalik Tat:** Hastaların en sık yakındığı hafif yan etkidir; tat duyusu geçici olarak bozulur.\n- **Gastrointestinal İrritasyon:** Bulantı, kusma, epigastrik kramp tarzı ağrı ve iştahsızlık.\n- **Disülfiram Benzeri Reaksiyon (Antabus Etkisi - Kritik Sınav Sorusu):**\n  - Metronidazol karaciğerde etanol metabolizmasında rol oynayan **aldehit dehidrogenaz (ALDH)** enzimini güçlü biçimde inhibe eder.\n  - İlaçla birlikte veya hemen sonrasında alkol alındığında kanda **asetaldehit** birikir.\n  - Sonuç: Yüzde ve göğüste şiddetli kızarma (flushing), zonklayıcı baş ağrısı, fışkırır tarzda kusma, terleme, taşikardi, hipotansiyon ve ölüm hissi gelişir.\n  - **Klinik Talimat:** Metronidazol tedavisi sırasında ve ilaç bittikten sonraki **en az 24 saat (Tinidazolde 72 saat) boyunca kesinlikle alkol tüketilmemelidir**.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_slider(
                "Normal Alkol Yıkımı vs Metronidazol ile Alkol Alımı",
                "Normal Alkol Metabolizması",
                "Etanol $\\to$ Asetaldehit $\\to$ ALDH enzimiyle Asetat ve suya parçalanır; toksisite olmaz.",
                "Metronidazol + Alkol (Disülfiram Reaksiyonu)",
                "ALDH bloke olur; asetaldehit kanda birikir; şiddetli kusma, taşikardi ve hipotansiyon krizine yol açar."
            ),
            make_cloze(
                "Metronidazolün aldehit dehidrogenaz enzimini inhibe etmesi sonucu alkol alındığında ortaya çıkan şiddetli reaksiyona disülfiram benzeri reaksiyon denir.",
                "disülfiram benzeri reaksiyon",
                "Alkolle metronidazol etkileşimi tablosu"
            )
        ]
    })

    # Slide 38
    slides.append({
        "id": "k1-17-s38",
        "title": "Ektoparaziter CYBE: Kasık Biti ve Uyuz Tedavisi (Permetrin)",
        "content": "Cinsel temasla bulaşabilen ektoparazitler perineal bölgede yoğun semptomlar yaratır:\n\n- **1. Kasık Biti (Phthirus pubis / Pedikülozis Pubis):**\n  - Kasık kıllarına sıkıca yapışan parazit ve yumurtalar (sirke) gözlenir; kan emilen yerlerde mavi-gri maküller (maculae caeruleae) oluşur.\n  - **Birinci Basamak Tedavi:** **Permetrin %1 losyon veya krem**.\n    - Kasıklara ve perine bölgesine sürülür, 10 dakika bekletildikten sonra yıkanır.\n    - 7-10 gün sonra (yeni yumurtadan çıkacak larvaları öldürmek için) kür tekrarlanır.\n    - Alternatif: Piretrinler ve piperonil butoksit köpük.\n- **2. Uyuz (Sarcoptes scabiei / Skabies):**\n  - Özellikle genital bölgede (penis gövdesi, skrotum) papüller, tüneller (silion) ve gece şiddetlenen yaygın kaşıntı.\n  - **Birinci Basamak Tedavi:** **Permetrin %5 krem**.\n    - Boyundan aşağı tüm vücuda sürülür, 8-14 saat vücutta bırakılıp yıkanır; 7 gün sonra tekrarlanır.\n  - **Çevre Tedavisi:** Tüm giysiler ve çarşaflar en az 60°C'de yıkanmalı veya hava almayan poşette 3-5 gün bekletilmelidir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Ektoparaziter Enfeksiyon", "Patojen", "Birinci Basamak İlaç", "Uygulama Şekli"],
                [
                    ["Kasık Biti (Pediculosis pubis)", "Phthirus pubis", "Permetrin %1 losyon/krem", "Perineye sürülür, 10 dk sonra yıkanır; 7 gün sonra tekrar"],
                    ["Uyuz (Skabies)", "Sarcoptes scabiei", "Permetrin %5 krem", "Boyundan aşağı tüm vücuda, 8-14 saat kalır; 7 gün sonra tekrar"]
                ]
            ),
            make_quiz(
                "Kasık kıllarında şiddetli kaşıntı ve kıllara yapışık sirkeler saptanan bir hastada kasık biti (Phthirus pubis) için ilk tercih lokal tedavi nedir?",
                [
                    {"key": "A", "text": "Permetrin losyon/krem", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kasık biti ve uyuz tedavisinde birinci basamak lokal ajan permetrindir."},
                    {"key": "B", "text": "Metronidazol oral", "isCorrect": False, "explanation": "Metronidazol parazitik böceklere ve bitlere etkisizdir."},
                    {"key": "C", "text": "Azitromisin tablet", "isCorrect": False, "explanation": "Azitromisin antibakteriyeldir."},
                    {"key": "D", "text": "Asiklovir krem", "isCorrect": False, "explanation": "Asiklovir antiviraldir."}
                ]
            )
        ]
    })

    # Slide 39 - CHECKPOINT 4
    slides.append({
        "id": "k1-17-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Trikomoniyazis ve Paraziter Tedaviler",
        "content": "Bu checkpointte Trichomonas vaginalis biyolojisini, klinik sendromunu ve tedavi kurallarını özetliyoruz:\n\n- **Kistsiz Patojen:** T. vaginalis'in kisti yoktur; sadece hareketli kamçılı trofozoit formu bulunur; doğrudan cinsel temasla bulaşır.\n- **Klinik Tablo:** Köpüklü, bol, sarı-yeşil, kötü kokulu akıntı; vajinal pH >4.5; servikste noktasal kanamalarla 'çilek serviks' (kolpitis makülaris).\n- **Tanı:** Taze SF bakısında aktif dönme hareketi yapan kamçılı trofozoitler; şüphelide NAAT.\n- **Standart Tedavi:** Metronidazol 2 g oral tek doz (gebede de aynı tek doz güvenle verilir).\n- **Altın Kurallar:** Partner eşzamanlı tedavi edilmeli ve tedavi sonrası 7 gün cinsel perhiz uygulanmalıdır.\n- **Alkol Etkileşimi:** ALDH enzim blokajıyla disülfiram benzeri reaksiyon yaptığından tedavi sırasında ve sonrasında alkol yasaktır.\n- **Ektoparazitler:** Kasık biti ve uyuzda birinci basamak tedavi Permetrindir.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_table(
                ["Öğe", "Klinik Özellik", "Farmakolojik Kural"],
                [
                    ["T. vaginalis Tedavisi", "Metronidazol 2 g oral tek doz", "Yalnızca oral sistemik verilir, topikal yetersizdir"],
                    ["Gebelikte Doz", "Metronidazol 2 g tek doz", "Erken membran rüptürü ve doğumu önler"],
                    ["Partner Yönetimi", "Eşzamanlı Metronidazol", "Ping-pong reenfeksiyonunu önlemek için şarttır"],
                    ["Cinsel İlişki Yasağı", "En az 7 gün perhiz", "Tedavi bitiminden sonra bulaşı engeller"],
                    ["Alkol Yasağı", "En az 24 saat alkol yok", "Asetaldehit birikimi ve disülfiram şokunu önler"]
                ]
            ),
            make_chain(
                "Trikomoniyazis Tedavi ve Güvenlik Basamakları",
                [
                    "1. Tanı Doğrulanması: SF bakısında kamçılı trofozoitler saptanır.",
                    "2. İlaç Reçetesi: Hastaya ve partnerine Metronidazol 2 g tek doz verilir.",
                    "3. Alkol Uyarısı: Disülfiram reaksiyonuna karşı alkol alımı kesin yasaklanır.",
                    "4. Cinsel İzolasyon: 7 gün cinsel perhiz uygulanarak tedavi tamamlanır."
                ]
            )
        ]
    })

    # Slide 40
    slides.append({
        "id": "k1-17-s40",
        "title": "Bölüm Özeti: Paraziter Tedavilerden Klamidya Yönetimine Geçiş",
        "content": "Bölüm 4 boyunca trikomoniyazis enfeksiyonunun patogenezini, kistsiz trofozoit biyolojisini ve tek doz metronidazol yönetimini tamamladık:\n\n- **Önemli İlke:** Trikomoniyazis tedavisi hastanın tek başına değil, mutlaka cinsel partneriyle birlikte yürütülmesi gereken mutlak bir eş tedavisidir.\n- **Sonraki Bölüm:** Bir sonraki bölümde kadınlarda kısırlığın bir numaralı sinsi nedeni olan **Chlamydia trachomatis enfeksiyonunu, serovarlarını (D-K ve LGV) ve Azitromisin/Doksisiklin tedavilerini** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 17: Cinsel Yolla Bulaşan Hastalıklarda Tedavi (Dr. Öğr. Üyesi Rüveyda Korkmazer)",
        "elements": [
            make_recall(
                "Metronidazol kullanan bir hastanın alkol alması durumunda yüzde kızarma, taşikardi, şiddetli kusma ve hipotansiyonla seyreden klinik tabloya ne ad verilir?",
                "Disülfiram benzeri reaksiyon (Antabus reaksiyonu)",
                "Aldehit dehidrogenaz inhibisyonuna bağlı asetaldehit birikimi"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi Trichomonas vaginalis tedavisinde topikal vajinal ovüller yerine oral sistemik tedavinin zorunlu olmasının temel gerekçesidir?",
                [
                    {"key": "A", "text": "Parazitin sadece kanda yaşayıp vajinada hiç bulunmaması", "isCorrect": False, "explanation": "Parazit vajinada yoğun olarak yaşar."},
                    {"key": "B", "text": "Parazitin Skene ve Bartholin bezleri ile üretraya da yerleşmesi ve topikal ilacın bu odaklara ulaşamaması", "isCorrect": True, "explanation": "Doğru cevap B'dir: T. vaginalis üretral ve glandüler odaklara gizlendiği için sistemik oral tedavi şarttır."},
                    {"key": "C", "text": "Topikal ilaçların vajinayı delmesi", "isCorrect": False, "explanation": "Böyle bir komplikasyon yoktur."},
                    {"key": "D", "text": "Parazitin ağız yoluyla beslenmeyi sevmesi", "isCorrect": False, "explanation": "Bilim dışı iddia."}
                ]
            )
        ]
    })

    return slides
