# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_8_slides():
    slides = []

    # Slide 71
    slides.append({
        "id": "k1-14-s71",
        "title": "Salgın Patojenlerinin Bulaş Yolları ve DSÖ Müdahale Başlıkları",
        "content": "Salgın yönetimi patojenin biyolojisine ve bulaş yoluna göre özelleştirilmiş sektörel müdahaleler gerektirir:\n\n- **Bulaş Yolunun Önemi:** Solunumla bulaşan bir virüs için uygulanan tedbirler (maske, havalandırma), fekal-oral yolla bulaşan bir bakteride (su klorlama) veya kene ile bulaşan bir virüste (vektör kontrolü) tamamen anlamsız kalır.\n- **DSÖ Temel Müdahale Başlıkları (Sınav Spotu):**\n  1. **Klinik Yönetim:** Spesifik antiviraller, antibiyotikler ve destekleyici bakım.\n  2. **Güçlendirilmiş Enfeksiyon Önleme ve Kontrol (IPC):** Hastane içi izolasyon ve KKE standartları.\n  3. **Aşılama:** Duyarlı konak havuzunu kurutma ve sürü bağışıklığı.\n  4. **Güvenli ve Onurlu Defin:** Cenaze ritüellerinde ceset kaynaklı enfeksiyonu engelleme.\n  5. **Vektör Kontrolü:** Sivrisinek, kene ve pire popülasyonunu kırma.\n  6. **Su ve Sanitasyon (WASH):** Güvenli içme suyu sağlama, kanalizasyon ve el yıkama altyapısı.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Müdahale Başlığı", "Hedeflenen Bulaş Yolu", "Temel Saha Eylemi"],
                [
                    ["Su ve Sanitasyon (WASH)", "Fekal-oral / su ve gıda", "Şebeke klorlama, temiz su tankeri, tuvalet sanitasyonu"],
                    ["Vektör Kontrolü", "Vektörler (sivrisinek, kene, pire)", "Larvasit, insektisit ilaçlama, sineklik, kene kovucu"],
                    ["Güvenli ve Onurlu Defin", "Doğrudan temas / vücut sıvıları", "Ceset torbası, dezenfeksiyon, kültürel saygılı gömü"],
                    ["Klinik IPC ve KKE", "Damlacık, hava yolu, kan teması", "Maske, tulum, negatif basınç, el hijyeni"]
                ]
            ),
            make_cloze(
                "DSÖ'nün salgın yanıtı müdahale başlıkları arasında klinik yönetim, aşılama, vektör kontrolü, su-sanitasyon ve güvenli ve onurlu defin yer alır.",
                "defin",
                "Cenaze bulaşını önleyen kritik halk sağlığı uygulaması"
            )
        ]
    })

    # Slide 72
    slides.append({
        "id": "k1-14-s72",
        "title": "Vektörle Bulaşan Salgın Patojenleri",
        "content": "Tropikal ve subtropikal kuşaktan iklim değişikliğiyle ılıman bölgelere yayılan en büyük salgın tehditlerinden biri vektör kaynaklı hastalıklardır:\n\n- **Temel Vektör Kaynaklı Hastalıklar (DSÖ Listesi - Sınav Sorusu):**\n  - **Chikungunya Virüsü:** Aedes sivrisinekleriyle bulaşır; şiddetli eklem ağrıları ve ateşle seyreder.\n  - **Sıtma (Malaria):** Anopheles cinsi dişi sivrisineklerle bulaşan Plasmodium parazitleridir.\n  - **Sarı Humma (Yellow Fever):** Aedes ve Haemagogus sivrisinekleriyle bulaşan ölümcül flavivirüstür; aşısı vardır.\n  - **Zika Virüsü:** Aedes sivrisinekleriyle bulaşır; gebelerde fetal mikrosefali ve Guillain-Barré sendromuna yol açar.\n- **Kontrol Stratejisi:**\n  - Sivrisinek üreme alanlarının (durgun sular, eski araba lastikleri, saksı altlıkları) kurutulması.\n  - Biyolojik larvasit uygulamaları ve insektisitli cibinlikler (ITN).\n  - Sarı humma için endemik bölgelere seyahat edenlere zorunlu aşılama.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Aşağıdaki hastalıklardan hangisi Dünya Sağlık Örgütü sınıflandırmasına göre başlıca 'vektör' yoluyla bulaşan hastalıklar grubundadır?",
                [
                    {"key": "A", "text": "Kolera", "isCorrect": False, "explanation": "Kolera fekal-oral yolla (kirli su ve gıda) bulaşır."},
                    {"key": "B", "text": "Polio (Çocuk felci)", "isCorrect": False, "explanation": "Polio fekal-oral yolla bulaşır."},
                    {"key": "C", "text": "Chikungunya ve Sarı humma", "isCorrect": True, "explanation": "Doğru cevap C'dir: Chikungunya, sarı humma, sıtma ve Zika virüsü sivrisinek vektörleriyle bulaşır."},
                    {"key": "D", "text": "Kızamık", "isCorrect": False, "explanation": "Kızamık solunum yoluyla damlacık/aerosol ile bulaşır."}
                ]
            ),
            make_recall(
                "Vektörle bulaşan arbovirüs salgınlarında (Zika, Dang, Chikungunya) neden tek başına evde karantina uygulamak salgını durduramaz?",
                "Çünkü patojen sivrisinekler aracılığıyla bir evden diğer eve kolayca taşınır; ortamdaki sivrisinek popülasyonu kırılmadıkça bulaş sürer."
            )
        ]
    })

    # Slide 73
    slides.append({
        "id": "k1-14-s73",
        "title": "Hayvan ve Kene Kaynaklı Tehditler: KKKA, Mpox ve Rift Vadisi Ateşi",
        "content": "Zoonotik kökenli salgınların en ölümcül örnekleri hayvan rezervuarları ve eklembacaklılar üzerinden insanlara geçer:\n\n- **Kırım-Kongo Kanamalı Ateşi (KKKA - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Hayvanlar (başlıca Hyalomma cinsi keneler) ve enfekte hayvan kanı/dokusuyla doğrudan temas**.\n  - İkincil bulaş: Nozokomiyal olarak hastane ortamında kan ve vücut sıvılarıyla sağlık personeline bulaşır.\n- **Maymun Çiçeği (Mpox - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Hayvanlar ve insandan insana doğrudan yakın fiziksel/lezyon teması**.\n  - Cilt lezyonları, döküntüler ve kontamine çarşaflarla yayılır.\n- **Rift Vadisi Ateşi (Sınav Spotu):**\n  - Başlıca bulaş yolu: **Hayvanlar (enfekte hayvan dokusu teması) ve vektörler (sivrisinekler)**.\n  - Çiftlik hayvanlarında kitlesel düşüklere (abortus fırtınası) yol açar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Hastalık", "Başlıca Bulaş Yolu (DSÖ)", "Temel Korunma Tedbiri"],
                [
                    ["KKKA", "Hayvanlar (başlıca kene) / kan teması", "Pantolon paçalarını çoraba sokma, kene kontrolü, KKE"],
                    ["Maymun Çiçeği (Mpox)", "Hayvanlar / yakın fiziksel ve cilt teması", "Lezyonlu hastaları izole etme, temaslı aşılama"],
                    ["Rift Vadisi Ateşi", "Hayvanlar / vektörler (sivrisinek)", "Hayvan aşılaması, çiğ et ve sütten kaçınma, sineklik"]
                ]
            ),
            make_cloze(
                "Kırım-Kongo kanamalı ateşi başlıca Hyalomma cinsi kene ısırması veya enfekte hayvan kanı ve dokusuyla temas sonucu bulaşır.",
                "kene",
                "KKKA'nın başlıca omurgasız vektörü"
            )
        ]
    })

    # Slide 74
    slides.append({
        "id": "k1-14-s74",
        "title": "Fekal-Oral ve Su Kaynaklı Salgınlar: Kolera, Polio ve Şigelloz",
        "content": "Altyapı yetersizliği, savaşlar ve doğal afetler sonrasında patlak veren en hızlı salgınlar fekal-oral yolla bulaşan enfeksiyonlardır:\n\n- **Kolera (Vibrio cholerae - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Fekal-oral / kontamine su ve deniz ürünleri**.\n  - Pirinç suyu benzeri masif sekresyonlu diyare; saatler içinde hipovolemik şok ve ölüm. Temel müdahale: Acil klorlama, temiz su sağlama ve oral rehidrasyon sıvısı (ORS).\n- **Poliomiyelit (Çocuk Felci - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Fekal-oral** (nadir solunum).\n  - Motor nöron harabiyeti ve flask paralizi. Temel müdahale: Oral polio aşısı (OPV) ve inaktif polio aşısı (IPV).\n- **Şigelloz (Basilli Dizanteri - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Fekal-oral / gıda ve sinekler**.\n  - Çok düşük enfeksiyon dozu (10-100 bakteri yeterlidir); kanlı-mukuslu diyare ve tenesmus. Temel müdahale: El yıkama, gıda hijyeni.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Kolera Bulaş Dinamiği vs Kolera Salgın Müdahalesi",
                "Bulaş Dinamiği (Kanalizasyonun Suya Karışması)",
                "İçme suyu şebekesine karışan kanalizasyon binlerce insanı aynı anda enfekte ederek saatler içinde öldürür.",
                "Halk Sağlığı Müdahalesi (WASH ve Klorlama)",
                "Şebeke suyuna serbest klor (0.5 mg/L) verilmesi ve ORS dağıtımıyla vaka ölüm oranı %1'in altına indirilir."
            ),
            make_quiz(
                "Dünya Sağlık Örgütü verilerine göre kolera ve şigellozun toplumda yayılmasındaki başlıca bulaş yolları hangi seçenekte doğru verilmiştir?",
                [
                    {"key": "A", "text": "Sivrisinek sokması ve kene ısırması", "isCorrect": False, "explanation": "Bu vektörel bulaştır; kolera ve şigelloz vektörle bulaşmaz."},
                    {"key": "B", "text": "Fekal-oral yol, kontamine su ve gıdalar", "isCorrect": True, "explanation": "Doğru cevap B'dir: Kolera suyla, şigelloz gıda/fekal-oral yolla bulaşan klasik enterik patojenlerdir."},
                    {"key": "C", "text": "Havadaki aerosollerin solunması", "isCorrect": False, "explanation": "Kolera aerosol veya solunumla bulaşmaz."},
                    {"key": "D", "text": "Sadece cinsel temas", "isCorrect": False, "explanation": "Klasik su ve gıda kaynaklı enfeksiyonlardır."}
                ]
            )
        ]
    })

    # Slide 75
    slides.append({
        "id": "k1-14-s75",
        "title": "Solunum Yolu Salgınları: Kızamık, Grip ve Koronavirüsler",
        "content": "Küresel çapta yayılma hızı en yüksek olan ve kontrolü en zor salgınlar solunum yoluyla yayılan hastalıklardır:\n\n- **Kızamık (Measles - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Solunum (havada saatlerce asılı kalan ince aerosoller)**.\n  - Bulaştırıcılığı bilinen en yüksek virüstür (R0 = 12-18). Bir sınıfta bir hasta çocuk varsa aşılanmamış herkes enfekte olur.\n  - Tek kesin kurtuluş: İki doz KKK aşısı ile toplum bağışıklığının **%95'in üzerinde** tutulmasıdır.\n- **İnfluenza ve Koronavirüsler:**\n  - Damlacık ve aerosol bulaşı.\n  - Kapalı alanlarda yetersiz havalandırma, kalabalık ortamlar ve yakın temas patojenin amplifikasyonuna yol açar.\n  - Önlemler: Kaynak kontrolü (maske), etkili mekanik havalandırma (HEPA filtre), fiziksel mesafe ve el hijyeni.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Patojen", "R0 Değeri", "Başlıca Bulaş Yolu", "Gereken Toplum Bağışıklık Eşiği"],
                [
                    ["Kızamık Virüsü", "12 – 18", "Solunum (Aerosol / havada asılı)", "%92 – %95"],
                    ["COVID-19 (Omicron)", "8 – 12", "Solunum (Damlacık ve aerosol)", "%85 – %90"],
                    ["Mevsimsel İnfluenza", "1.3 – 1.8", "Solunum (Damlacık)", "%40 – %50"]
                ]
            ),
            make_cloze(
                "Dünya Sağlık Örgütü tablosunda kızamık hastalığının başlıca bulaş yolu solunum yoludur.",
                "solunum",
                "Kızamığın havadaki yayılma rotası"
            )
        ]
    })

    # Slide 76
    slides.append({
        "id": "k1-14-s76",
        "title": "Kemirgen Kaynaklı Tarihi Tehdit: Veba (Yersinia pestis)",
        "content": "Orta Çağ'da Avrupa nüfusunun üçte birini yok eden 'Kara Ölüm' günümüzde de endemik odaklar halinde varlığını sürdürmektedir:\n\n- **Bübonik Veba Bulaş Yolu (DSÖ Listesi - Sınav Spotu):**\n  - Başlıca bulaş yolu: **Kemirgenler (rodentler - sıçanlar) ve onların üzerinde yaşayan enfekte pireler (Xenopsylla cheopis)**.\n  - Pireler enfekte kemirgenden kan emdikten sonra insanı ısırarak Yersinia pestis bakterisini lenfatiklere aşılar.\n  - Büyümüş, ağrılı ve nekroze lenf nodları (bübo) gelişir.\n- **Pnömonik Veba (İkincil Dönüşüm):**\n  - Bakteri akciğere ulaştığında insandan insana **solunum yoluyla (öksürük damlacıkları)** bulaşmaya başlar; tedavi edilmezse saatler içinde %100 öldürücüdür.\n- **Müdahale:** Pire ilaçlaması yapılmadan doğrudan sıçanlar zehirlenirse, aç kalan pireler doğrudan insanlara saldırır! Önce pire kontrolü, sonra kemirgen kontrolü yapılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_quiz(
                "Dünya Sağlık Örgütü sınıflandırmasında bübonik veba hastalığının başlıca rezervuar ve bulaş kaynağı hangisidir?",
                [
                    {"key": "A", "text": "Kemirgenler (ve üzerlerindeki pireler)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bübonik veba (Yersinia pestis) kemirgenler ve pire vektörleri aracılığıyla bulaşır."},
                    {"key": "B", "text": "Sadece temiz kaynak suları", "isCorrect": False, "explanation": "Veba su kaynaklı bir enfeksiyon değildir."},
                    {"key": "C", "text": "Aedes cinsi sivrisinekler", "isCorrect": False, "explanation": "Aedes sivrisinekleri sarı humma, dang ve zika bulaştırır."},
                    {"key": "D", "text": "İyi pişmiş dana eti", "isCorrect": False, "explanation": "Pişmiş et bulaş kaynağı değildir."}
                ]
            ),
            make_recall(
                "Veba salgınında kemirgenlerle mücadele ederken neden önce pire ilaçlaması yapılmalıdır?",
                "Çünkü önce kemirgenler öldürülürse, üzerlerindeki aç enfekte pireler konak arayışıyla hemen insanlara geçer ve salgın patlar."
            )
        ]
    })

    # Slide 77
    slides.append({
        "id": "k1-14-s77",
        "title": "Güvenli ve Onurlu Defin (Safe and Dignified Burial) Prensipleri",
        "content": "Ebola, Marburg ve KKKA gibi yüksek mortaliteli kanamalı ateş salgınlarında cenaze törenleri en büyük süper-bulaş kaynağıdır:\n\n- **Ölü Bedendeki Viral Yük:** Ebola veya KKKA'dan ölen bir hastanın cansız bedenindeki viral yük, yaşayan bir hastadan katbekat daha yüksektir. Kan, kusmuk ve vücut sıvıları aşırı derecede bulaştırıcıdır.\n- **Geleneksel Ritüellerin Tehlikesi:** Cesedi çıplak elle yıkamak, öpmek, sarılmak ve toplu cenaze yemekleri tek bir cenazeden onlarca yeni vakanın çıkmasına yol açar.\n- **Güvenli ve Onurlu Defin Protokolü (DSÖ - Sınav Spotu):**\n  - **Güvenli (Safe):** Cenaze ekibi tam koruyucu tulumlar giyer, ceset sızdırmaz ceset torbasına konur, klor solüsyonuyla dezenfekte edilir.\n  - **Onurlu (Dignified):** Ailenin dini ve kültürel inançlarına saygı gösterilir; aile üyelerinin güvenli mesafeden dua etmelerine ve cenazeyi görmelerine izin verilir.\n- **Halk Sağlığı İlkesi:** Aile dışlanır veya ceset zorla kaçırılırsa halk cenazelerini gizlice gömmeye başlar ve salgın kontrolden çıkar.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_chain(
                "Güvenli ve Onurlu Defin Protokolü Basamakları",
                [
                    "1. Aileyle İletişim ve İkna: Defin ekibi aileye empatiyle yaklaşır, dini lider sürece dahil edilir.",
                    "2. KKE ile Giriş: Ekip tam sızdırmaz tulum, çift eldiven ve maskeyle odaya girer.",
                    "3. Cesedin Torbalanması: Ceset hareket ettirilmeden çift katlı sızdırmaz torbaya yerleştirilir ve klorlanır.",
                    "4. Güvenli Mesafeden Dua: Ailenin 2-3 metre mesafeden dini ritüellerini yapmasına izin verilir.",
                    "5. Derin Gömü ve Dezenfeksiyon: Mezar güvenli derinlikte kapatılır ve ekip doffing yaparak ayrılır."
                ]
            ),
            make_cloze(
                "Kanamalı ateş salgınlarında cenazelerden bulaşı önlemek için güvenli ve onurlu defin protokolü uygulanır.",
                "onurlu",
                "Ailenin inanç ve değerlerine saygıyı simgeleyen defin kavramı"
            )
        ]
    })

    # Slide 78
    slides.append({
        "id": "k1-14-s78",
        "title": "Su ve Sanitasyon (WASH): Salgınların Sessiz Temel Direği",
        "content": "DSÖ'nün 'WASH' (Water, Sanitation and Hygiene) programı, enfeksiyon kontrolünün görünmeyen en büyük kahramanıdır:\n\n- **Su Güvenliği ve Klorlama:** Şebeke suyunda serbest bakiye klor düzeyinin **en az 0.5 mg/L** tutulması kolera, tifo ve hepatit A gibi etkenleri saniyeler içinde etkisiz hale getirir.\n- **Sanitasyon ve Tuvaletler:** İnsan dışkısının içme suyu havzalarından ve tarım arazilerinden tamamen izole edilmesi fekal-oral döngüyü kırar.\n- **El Hijyeni Altyapısı:** Su ve sabuna erişim solunum ve sindirim yolu enfeksiyonlarını %30 ila %50 oranında tek başına azaltır.\n- **Afetlerde WASH:** Deprem, sel veya mülteci krizlerinde ilk 48 saatte temiz su tankerleri ve klor tabletleri sağlanamazsa ikincil salgınlar travmadan daha çok insan öldürür.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_slider(
                "Kirli Su ve Sanitasyonsuzluk vs Güvenli WASH Altyapısı",
                "Sanitasyonsuzluk (Salgın Fabrikası)",
                "Kanalizasyon içme suyuna karışır; kolera ve dizanteri patlak vererek çocukları dehidrate eder.",
                "Güvenli WASH Altyapısı (Kesintisiz Kalkan)",
                "0.5 mg/L klorlanmış su, kapalı kanalizasyon ve sabun kullanımıyla enterik salgınlar tamamen sıfırlanır."
            ),
            make_recall(
                "Halk sağlığında acil durumlarda içme suyu güvenliğini sağlamanın en hızlı ve maliyet-etkin yöntemi nedir?",
                "Şebeke suyunun veya depolanan suların klorlanması (serbest bakiye klorun en az 0.5 mg/L seviyesinde tutulması) ve klor tabletleri dağıtımıdır."
            )
        ]
    })

    # Slide 79 - CHECKPOINT 8
    slides.append({
        "id": "k1-14-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Bulaş Yollarına Göre Salgın Patojenleri ve Kontrol Önlemleri",
        "content": "Bu checkpointte DSÖ'nün bulaş yolları sınıflamasını ve özgül müdahaleleri pekiştiriyoruz:\n\n- **Vektör Kaynaklı:** Chikungunya, sıtma, sarı humma, Zika (Sivrisinek kontrolü, larvasit, cibinlik).\n- **Hayvan / Kene / Temas:** KKKA (Kene ve kan teması), Maymun çiçeği / Mpox (Yakın cilt lezyonu teması), Rift Vadisi ateşi (Hayvan ve vektör).\n- **Fekal-Oral / Su ve Gıda:** Kolera (Su), Polio (Fekal-oral), Şigelloz (Gıda/su) -> WASH ve klorlama.\n- **Solunum Yolu:** Kızamık (Aerosol, R0=12-18), İnfluenza, SARS-CoV-2 -> Maske, havalandırma, %95 aşılama.\n- **Kemirgen Kaynaklı:** Veba (Yersinia pestis - sıçanlar ve pireler) -> Önce pire, sonra kemirgen kontrolü.\n- **Güvenli ve Onurlu Defin:** Ebola ve kanamalı ateşlerde ceset kaynaklı yayılımı dini inançlara saygıyla önleme.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_table(
                ["Hastalık", "Başlıca Bulaş Yolu (DSÖ)", "Kritik Müdahale Aracı"],
                [
                    ["KKKA", "Hayvanlar (başlıca kene) / kan", "Kene kontrolü, KKE, doffing"],
                    ["Kolera", "Fekal-oral / su", "Klorlama (0.5 mg/L), WASH, ORS"],
                    ["Kızamık", "Solunum (Aerosol)", "İki doz KKK aşısı (%95 kapsayıcılık)"],
                    ["Veba (bübonik)", "Kemirgen (sıçan ve pire)", "Önce pire ilaçlaması, sonra rodentisit"],
                    ["Chikungunya / Sarı Humma", "Vektör (sivrisinek)", "Larvasit, cibinlik, sarı humma aşısı"]
                ]
            ),
            make_chain(
                "Bulaş Yoluna Göre Müdahale Eşleştirmesi",
                [
                    "1. Patojen Tespiti: Bulaş yolu (vektör, fekal-oral, solunum, temas) dakikalar içinde belirlenir.",
                    "2. Kaynak Kontrolü: Sivrisinek odağı kurutulur, su klorlanır veya hasta izole edilir.",
                    "3. Bulaş Zincirini Kırma: KKE, güvenli defin, maske veya sineklik devreye sokulur.",
                    "4. Duyarlı Kalkanı: Temaslılar aşılanır veya kemoprofilaksi başlanır."
                ]
            )
        ]
    })

    # Slide 80
    slides.append({
        "id": "k1-14-s80",
        "title": "Mini Vaka: Deprem Sonrası Çadır Kentte Su Kaynaklı Kolera Tehdidi",
        "content": "Büyük bir depremin 5. gününde, 20.000 kişinin yaşadığı çadır kentte aniden pirinç suyu görünümünde yoğun sulu ishali olan 12 hasta sahra hastanesine başvuruyor:\n\n- **Epidemiyolog Teşhisi:** Hastaların dışkı mikroskopisinde hareketli Vibrio bakterileri görülüyor; kolera salgını alarmı veriliyor.\n- **Kaynak Taraması:** Çadır kent sakinlerinin ana su borusundaki patlak nedeniyle yakındaki dere suyunu kullandığı ve tuvalet çukurlarının su kaynağına 10 metre mesafede kazıldığı saptanıyor.\n- **Müdahale:**\n  1. Dere suyu kullanımı jandarma kontrolüyle derhal yasaklanıyor.\n  2. Çadır kente tankerlerle klorlanmış (serbest bakiye klor: 0.8 mg/L) içme suyu getiriliyor.\n  3. Tuvaletler su havzasından 50 metre uzağa taşınıyor ve kireçleniyor.\n  4. Sahra hastanesinde ORS ve IV sıvı istasyonu kurularak vaka ölüm oranı %0'da tutuluyor.",
        "sourcePdf": "Kurul 1 - Ders 14: Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri (Uzm. Dr. Erkay Nacar)",
        "elements": [
            make_branching(
                "Saha Yönetimi: Çadır Kentte Kolera Tehdidine İlk Müdahale",
                "Çadır kentte kolera vakaları görülmeye başlandığında depolarda yeterli antibiyotik bulunmadığı bildiriliyor. Bu kriz anında en hayat kurtarıcı adımınız ne olmalıdır?",
                [
                    {
                        "text": "Ankara'dan uçakla pahalı geniş spektrumlu antibiyotikler gelene kadar beklemek",
                        "outcome": "Ölümcül hata: Kolera hastaları saatler içinde dehidrate olarak ölür; antibiyotik beklenirken onlarca kayıp verilir.",
                        "isCorrect": False
                    },
                    {
                        "text": "Tüm hastalara agresif oral rehidrasyon sıvısı (ORS) ve damardan sıvı desteği başlatmak, aynı anda çadır kentin tüm sularını süperklorlamak",
                        "outcome": "Kusursuz halk sağlığı müdahalesi: Sıvı desteği hayat kurtarır (mortalite <%1), klorlama yeni vakaların çıkmasını anında durdurur.",
                        "isCorrect": True
                    },
                    {
                        "text": "Çadır kenti tamamen boşaltıp insanları çevre illere dağıtmak",
                        "outcome": "Felaket senaryosu: Kolera tüm ülkeye yayılır.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada çadır kentte koleranın önlenmesi için yapılan su klorlaması ve tuvalet sanitasyonu DSÖ'nün hangi temel müdahale başlığına girer?",
                [
                    {"key": "A", "text": "Su ve Sanitasyon (WASH)", "isCorrect": True, "explanation": "Doğru cevap A'dır: İçme suyu klorlaması, atık su yönetimi ve tuvalet hijyeni su ve sanitasyon (WASH) müdahalesidir."},
                    {"key": "B", "text": "Vektör kontrolü", "isCorrect": False, "explanation": "Kolera sivrisinek veya keneyle bulaşmaz."},
                    {"key": "C", "text": "Güvenli ve onurlu defin", "isCorrect": False, "explanation": "Defin cenaze yönetimidir."},
                    {"key": "D", "text": "Yalnızca kemoprofilaksi", "isCorrect": False, "explanation": "Altyapı müdahalesi kemoprofilaksi değildir."}
                ]
            )
        ]
    })

    return slides
