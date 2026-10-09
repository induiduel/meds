# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-16-s51",
        "title": "Lenfatik Obstrüksiyon (Lenfödem): Fizyopatoloji ve Özellikler",
        "content": "Lenfatik dolaşım, interstisyuma süzülen proteinleri ve net sıvı fazlasını temizleyen yegane drenaj hattıdır:\n\n- **Mekanizma:** Lenf kanalları veya drene oldukları bölgesel lenf düğümleri tıkandığında, dokudan sıvı ve makromolekül uzaklaştırılamaz.\n- **Protein Zenginliği:** Kardiyak veya renal ödemde interstisyel sıvı protein açısından fakir iken; lenf ödeminde interstisyumda yüksek miktarda protein birikir.\n- **Kronik İnflamasyon ve Fibrozis:** Doku aralığında biriken proteinler kronik makrofaj uyarımına ve fibroblast aktivasyonuna yol açar. Zamanla doku kalınlaşır, sertleşir ve fibrotik bir zırha dönüşür.\n- **Gode Bırakmayan (Non-pitting) Karakter:** Erken dönemde parmak basısıyla çukurlaşabilirken, kronik lenfödemde doku fibrozisi nedeniyle ödem **serttir ve çukur bırakmaz (non-pitting)**.\n- **Etiyolojik Yelpaze:** İnflamatuvar, paraziter, neoplastik, cerrahi ve radyasyon hasarlarına bağlı gelişebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kardiyak/Venöz Ödem vs Kronik Lenfödem Karakteri",
                "Kardiyak/Venöz Ödem",
                "Proteinden fakirdir, doku yumuşaktır, parmak basısıyla derin çukur bırakır (pitting).",
                "Kronik Lenfödem",
                "Proteinden zengindir, yoğun fibroblastik fibrozis içerir, serttir ve çukur bırakmaz (non-pitting)."
            ),
            make_cloze(
                "Lenf damarlarının tıkanması sonucu protein zengini sıvının birikmesi ve sekonder fibrozisle karakterize sert ödeme lenfödem denir.",
                "lenfödem",
                "Lenfatik dolaşım yetersizliğine bağlı gelişen doku şişliği"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-16-s52",
        "title": "Paraziter Lenfödem: Filaryazis ve Fil Hastalığı (Elefantiyazis)",
        "content": "Dünya genelinde lenfödemin en sık paraziter ve enfeksiyöz nedeni filaryazistir (Sınav Spotu):\n\n- **Etken Parazit:** Sivrisineklerle bulaşan bir nematod olan **Wuchereria bancrofti**'dir.\n- **Yerleşim ve Hasar:** Erişkin parazitler özellikle kasık (inguinal) ve pelvik lenfatik damarlara ve lenf düğümlerine yerleşir.\n- **Kronik Enflamasyon ve Fibrozis:** Parazitlerin varlığı ve ölümü şiddetli kronik lenfanjite, lenfadenite ve masif obstrüktif fibrozise yol açar.\n- **Fil Hastalığı (Elefantiyazis):**\n  - Alt ekstremitelerde ve eksternal genital bölgede (skrotum/labium) drenaj tamamen durur.\n  - Bacaklar ve skrotum devasa boyutlara ulaşır; deri kurur, kalınlaşır ve fil derisi gibi çatlaklı-hiperkeratotik bir hal alır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Filaryaziste Elefantiyazis Gelişim Aşamaları",
                [
                    "1. Parazit İstilası: Wuchereria bancrofti larvaları inguinal lenfatiklere yerleşir.",
                    "2. Lenfanjit ve Fibrozis: Lenf damarlarında kronik yangı ve lümen obliterasyonu gelişir.",
                    "3. Masif Lenfatik Göllenme: Alt ekstremitelerden lenf drenajı tamamen bloke olur.",
                    "4. Fil Hastalığı (Elefantiyazis): Bacaklarda devasa boyutlu, hiperkeratotik sert lenfödem oturur."
                ]
            ),
            make_quiz(
                "İnguinal lenf damarlarında fibrozis yaparak alt ekstremitede masif lenfödeme ('fil hastalığı / elefantiyazis') yol açan paraziter etken hangisidir?",
                [
                    {"key": "A", "text": "Entamoeba histolytica", "isCorrect": False, "explanation": "Amipli dizanteri ve karaciğer absesi etkenidir."},
                    {"key": "B", "text": "Wuchereria bancrofti (Filaryazis)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Wuchereria bancrofti lenfatikleri tıkayarak elefantiyazise neden olur."},
                    {"key": "C", "text": "Giardia lamblia", "isCorrect": False, "explanation": "İnce bağırsak malabsorpsiyon etkenidir."},
                    {"key": "D", "text": "Taenia saginata", "isCorrect": False, "explanation": "Sığır tenyasıdır, lenfatikleri tıkamaz."}
                ]
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-16-s53",
        "title": "Neoplastik Lenfödem: Meme Kanseri ve 'Peau d'Orange'",
        "content": "Kanser hücrelerinin lenf damarlarını istila etmesi lokalize lenfödemin en kritik onkolojik bulgusudur (Sınav Spotu):\n\n- **Meme Karsinomunda Lenfatik Emboli:** İnvaziv meme kanseri hücreleri derialtı subdermal lenfatik kanalları infiltre eder ve tıkar.\n- **Meme Derisinde Ödem:** Memenin lenfatik drenajı bozulur ve deri altı bağ dokusunda yoğun interstisyel sıvı toplanır; meme derisi şişer ve kalınlaşır.\n- **Portakal Kabuğu Manzarası (Peau d'Orange):**\n  - Şişen meme derisinde kıl folikülleri ve ter bezleri cildin derin bağ dokusuna asıcı Cooper ligamanları ile bağlı kalır.\n  - Bu asıcı noktalar çukurlaşırken aradaki ödemli deri dışarı kabarır.\n  - Sonuçta meme derisi tıpkı bir portakalın pürtüklü dış kabuğuna benzer bir görünüm alır (Peau d'orange).\n- **Klinik Önem:** Peau d'orange bulgusu, kanserin lokal olarak ileri evreye (enflamatuvar karsinom veya T4 tümör) ulaştığını gösterir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Klinik Bulgu", "Patolojik Mekanizma", "Görsel Özellik", "Onkolojik Değeri"],
                [
                    ["Peau d'Orange (Portakal Kabuğu)", "Tümör hücrelerinin subdermal lenfatikleri tıkaması", "Kıl folikülleri çukurda, çevre deri ödemli ve pürtüklü", "Lokal ileri meme kanseri bulgusu"],
                    ["Meme Başı Retraksiyonu", "Tümörün büyük süt kanallarını çekmesi", "Meme ucunun içeriye çökmesi", "Malign invazyon şüphesi"],
                    ["Cooper Ligamanı Çekintisi", "Tümörün fibröz ligamanları kısaltması", "Deride sınırlı çekinti (gamzeleşme)", "Karsinomun doku infiltrasyonu"]
                ]
            ),
            make_quiz(
                "Meme kanserinde meme derisinde 'portakal kabuğu' (peau d'orange) görünümünün ortaya çıkmasına yol açan primer mekanizma hangisidir?",
                [
                    {"key": "A", "text": "Subdermal lenfatik damarların malign tümör hücreleri tarafından infiltre edilip tıkanması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kanser embolilerinin subdermal lenfatikleri tıkaması deride lenfödeme ve peau d'orange görünümüne yol açar."},
                    {"key": "B", "text": "Meme dokusunun aşırı C vitamini depolaması", "isCorrect": False, "explanation": "Vitamin birikimiyle ilişkisizdir."},
                    {"key": "C", "text": "Aksiller arterin tamamen pıhtıyla tıkanması", "isCorrect": False, "explanation": "Arter tıkanıklığı iskemik nekroz yapar."},
                    {"key": "D", "text": "Hastada derin ven trombozu gelişmesi", "isCorrect": False, "explanation": "Meme derisinde DVT görülmez."}
                ]
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-16-s54",
        "title": "İyatrojenik Lenfödem: Aksiller Diseksiyon ve Radyoterapi",
        "content": "Kanser cerrahisi ve onkolojik tedavilerin istenmeyen ancak sık görülen bir komplikasyonu iyatrojenik lenfödemdir (Sınav Spotu):\n\n- **Aksiller Lenf Nodu Diseksiyonu:**\n  - Meme kanseri veya melanom cerrahisinde tümörün yayılmasını engellemek veya evrelemek için koltuk altı (aksilla) lenf nodları cerrahi olarak çıkarılır.\n  - Aksiller nodlar aynı zamanda tüm kolun lenfatik sıvısının boşaldığı ana istasyondur.\n- **Radyasyon Hasarı:** Ameliyat sonrası uygulanan radyoterapi kalan lenf kanallarında yoğun fibröz skarlaşma ve obliterasyon yaratır.\n- **Kolda Masif Lenfödem:** Drenaj hattı kesilen kolda ameliyattan aylar veya yıllar sonra ilerleyici, kalıcı ve sakatlayıcı bir kol şişliği (lenfödem) gelişir.\n- **Komplikasyon:** Etkilenen kolda bakteriyel lenfanjit/selülit atakları kolaylaşır ve nadiren uzun yıllar sonra kötü huylu vasküler bir tümör olan **anjiyosarkom (Stewart-Treves sendromu)** gelişebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Lenfatik Drenaj vs Aksiller Diseksiyon Sonrası",
                "Normal Aksiller Drenaj",
                "Koldan gelen tüm interstisyel sıvı aksiller nodlardan süzülerek subklavyen vene akar; kol incedir.",
                "Diseksiyon Sonrası Kol Lenfödemi",
                "Lenf nodları çıkarıldığı ve fibrozis geliştiği için kol dokusunda masif sıvı toplanır; kol ağırlaşır ve sertleşir."
            ),
            make_cloze(
                "Meme kanseri cerrahisinde aksiller lenf nodu diseksiyonu ve radyoterapi sonrası ilgili üst ekstremitede kolda lenfödem gelişebilir.",
                "kolda lenfödem",
                "Cerrahi lenf nodu çıkarılması sonrası kolda gelişen şişlik"
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-16-s55",
        "title": "Primer Sodyum ve Su Retansiyonu: Renal Hastalıklar",
        "content": "Böbrekler vücuttaki su ve elektrolit dengesinin en üst düzey denetleyicisidir:\n\n- **Böbrek Yetmezliği ve Glomerülonefrit:**\n  - Akut poststreptokokal glomerülonefrit veya son dönem böbrek yetmezliğinde glomerüler filtrasyon değeri (GFR) dramatik biçimde düşer.\n  - Böbrek kandan yeterli süzme yapamaz ve alınan günlük tuzu ve suyu idrara aktaramaz.\n- **Primer Tutulum:** Kalp yetmezliğindeki 'sekonder' tutulumdan farklı olarak, burada sorun kalpte değil doğrudan böbreğin kendi primer fonksiyon bozukluğundadır.\n- **Klinik Profil:** İdrar miktarı azalır (oligüri veya anüri), kan üre azotu ve kreatinin yükselir; vücutta su hızla birikir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Renal Yetmezlikte Sıvı Tutulum Basamakları",
                [
                    "1. Glomerül Hasarı: Yangı veya skleroz süzme yüzeyini ve GFR'yi çökertir.",
                    "2. Oligüri Gelişimi: Günlük atılan idrar hacmi kritik düzeyde azalır.",
                    "3. Sodyum ve Su Birikimi: Diyetle alınan tuz ve sıvı vücutta hapsolur.",
                    "4. İntravasküler Hacim Artışı: Damar yatağında aşırı sıvı göllenmesi başlar."
                ]
            ),
            make_quiz(
                "Akut glomerülonefritli bir hastada ödem oluşumunun primer başlangıç mekanizması hangisidir?",
                [
                    {"key": "A", "text": "Böbreğin glomerüler filtrasyonunun çökmesi sonucu primer sodyum ve su retansiyonu gelişmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Akut glomerülonefritte primer sorun böbreğin tuzu ve suyu süzüp atamamasıdır."},
                    {"key": "B", "text": "Aşırı lenf sıvısı üretimi", "isCorrect": False, "explanation": "Lenf sıvısı üretimi artmaz."},
                    {"key": "C", "text": "Karaciğerin aşırı albümin sentezleyip damarları patlatması", "isCorrect": False, "explanation": "Albümin artışı ödem yapmaz."},
                    {"key": "D", "text": "Koroner arterlerde primer kireçlenme", "isCorrect": False, "explanation": "Koroner kireçlenme glomerülonefrit ödemini doğrudan açıklamaz."}
                ]
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-16-s56",
        "title": "Aşırı Tuz Alımı ve Hipervoleminin Vasküler Etkisi",
        "content": "Böbrek fonksiyonları sınırda olan veya böbrek yetmezliği bulunan hastalarda diyetle aşırı tuz alımı felaketi tetikler:\n\n- **Tuzun Ozmotik Çekimi:** Alınan sodyum ekstrasellüler alanda kalır ve ozmotik olarak suyu damar içine çeker.\n- **Hipervolemi:** Dolaşan toplam kan hacmi hızla artar (plazma hacim ekspansiyonu).\n- **Kardiyovasküler Yük:** Artan intravasküler hacim hem sistemik kan basıncını yükseltir (hipertansiyon) hem de kalbin venöz dolum basıncını (preload) aşırı artırır.\n- **Klinik Dekompansasyon:** Hasta birkaç gün içinde hızla kilo alır (sıvı artışı); hipertansif akciğer ödemi ve periferik ödemle acil servise başvurur.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Tuz Dengesi vs Aşırı Tuz Tutulumu ve Hipervolemi",
                "Normal Tuz Dengesi",
                "Alınan sodyum kadar sodyum idrarla atılır; damar içi hacim ve kan basıncı sabit kalır.",
                "Aşırı Tuz Tutulumu (Hipervolemi)",
                "Böbrek sodyumu atamaz; su tutulur, plazma hacmi genişler, hipertansiyon ve ödem tetiklenir."
            ),
            make_cloze(
                "Böbrek yetersizliğinde aşırı tuz ve su tutulumu sonucu dolaşımdaki toplam kan hacminin anormal artmasına hipervolemi denir.",
                "hipervolemi",
                "Dolaşımdaki sıvı hacminin aşırı yükselmesi"
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-16-s57",
        "title": "Hipervolemik Ödemde İkili Mekanizma: Hidrostatik Artış ve Onkotik Dilüsyon",
        "content": "Renal kaynaklı sodyum ve su retansiyonu ödemi iki ayrı koldan birden besler (Sınav Spotu):\n\n- **1. Kol: Artmış Kapiller Hidrostatik Basınç:**\n  - İntravasküler hacmin hipervolemiyle devasa boyutlara ulaşması tüm arteriyel ve venöz yatakta damar içi gerilimi ve kılcal damar hidrostatik basıncını doğrudan artırır.\n  - Yüksek basınç sıvıyı interstisyuma doğru pompalar.\n- **2. Kol: Azalmış Plazma Onkotik Basıncı (Dilüsyonel Hipoalbüminemi):**\n  - Damar içinde litrelerce fazladan su biriktiğinde, mevcut albümin havuzu sulanır (hemodilüsyon).\n  - Gram olarak albümin miktarı değişmese bile, desilitredeki konsantrasyonu düşer (ör. 4.0 g/dL'den 2.8 g/dL'ye iner).\n  - Düşen konsantrasyon onkotik çekim kuvvetini zayıflatır.\n- **Sonuç:** Hem itici hidrostatik basınç yükselmiş hem de tutucu onkotik güç azalmıştır; masif ödem kaçınılmazdır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Mekanizma Kolu", "Oluşma Şekli", "Kılcal Damar Etkisi", "Ödeme Katkısı"],
                [
                    ["Hidrostatik Artış", "Aşırı plazma hacminin damar duvarına yaptığı mekanik basınç", "Kapiller içi itici kuvvet fırlar", "Sıvıyı interstisyuma doğru dışarı iter"],
                    ["Onkotik Dilüsyon", "Aşırı suyun mevcut plazma albüminini seyreltmesi (hemodilüsyon)", "Plazma kolloid ozmotik çekim gücü zayıflar", "Sıvının venül ucunda geri emilimini bozar"]
                ]
            ),
            make_quiz(
                "Primer böbrek yetmezliğinde aşırı su tutulmasının plazma protein konsantrasyonunu düşürerek ödeme katkıda bulunması hangi mekanizmayla açıklanır?",
                [
                    {"key": "A", "text": "Karaciğerin aniden albümin parçalaması", "isCorrect": False, "explanation": "Karaciğer albümini parçalamaz."},
                    {"key": "B", "text": "Aşırı plazma suyu nedeniyle albüminin seyreltilmesi (dilüsyonel hipoalbüminemi)", "isCorrect": True, "explanation": "Doğru cevap B'dir: Fazla su damar içindeki albümini sulandırarak (dilüsyon) onkotik basıncı düşürür."},
                    {"key": "C", "text": "Albüminin idrarla değil ter bezleriyle atılması", "isCorrect": False, "explanation": "Albümin terle atılmaz."},
                    {"key": "D", "text": "Eritrositlerin plazma proteinlerini yemesi", "isCorrect": False, "explanation": "Eritrositler fagositoz yapmaz."}
                ]
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-16-s58",
        "title": "Enflamatuvar Ödem: Vasküler Geçirgenlik Artışı ve Eksuda",
        "content": "Ödemin beşinci mekanizması akut ve kronik enflamasyonda ortaya çıkan vasküler geçirgenlik artışıdır:\n\n- **Endotel Aralıklarının Açılması:** Histamin, bradikinin, lökotrienler ve PAF gibi yangı mediyatörleri postkapiller venül endotel hücrelerini kasar; hücreler arası kavşaklar açılır.\n- **Doğrudan Endotel Hasarı:** Ağır yanıklar, bakteriyel toksinler veya lökosit proteazları endotel hücrelerini öldürerek damar duvarında delikler açar.\n- **Eksuda Karakteri (Sınav Spotu):**\n  - Açılan geniş aralıklardan yalnızca su ve tuz değil; büyük plazma proteinleri (fibrinojen, globulinler) ve lökositler interstisyuma dökülür.\n  - Biriken sıvı yüksek proteinli (>3 g/dL) ve yüksek dansiteli (>1.020) bir **enflamatuvar eksudadır**.\n- **Anjiyogenez Katkısı:** İyileşen dokuda oluşan yeni kılcal damarların endoteli henüz tam olgunlaşmadığı için sızdırıcıdır (ödemli granülasyon dokusu).",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Hemodinamik Transuda vs Enflamatuvar Eksuda",
                "Hemodinamik Transuda",
                "Endotel intakttır; hidrostatik/onkotik dengesizlikle oluşur; proteinden fakir seröz sıvıdır.",
                "Enflamatuvar Eksuda",
                "Endotel aralıkları açılmıştır; yangı mediyatörleriyle oluşur; protein ve hücreden zengin yoğun sıvıdır."
            ),
            make_cloze(
                "Enflamasyonda endotel geçirgenliğinin artması sonucu doku aralığına sızan yüksek proteinli ve lökosit zengini sıvıya eksuda denir.",
                "eksuda",
                "Enflamatuvar vasküler geçirgenlik artışına bağlı sıvı"
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-16-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Lenfödem ve Renal Sıvı Tutulumu",
        "content": "Bu checkpointte lenfatik obstrüksiyon, neoplastik invazyon ve primer renal sıvı tutulumunu özetliyoruz:\n\n- **Lenfödem:** Lenf yollarının tıkanmasıyla proteinden zengin sıvının birikmesi; kronik dönemde yoğun doku fibrozisi nedeniyle sert ve çukur bırakmayan (non-pitting) ödem.\n- **Filaryazis (Wuchereria bancrofti):** Kasık lenfatiklerinde paraziter fibrozis sonucu alt ekstremite ve skrotumda 'fil hastalığı (elefantiyazis)'.\n- **Peau d'Orange (Portakal Kabuğu):** Meme kanseri hücrelerinin subdermal lenfatikleri tıkamasıyla meme derisinde pürtüklü ödem tablosu.\n- **Aksiller Diseksiyon:** Cerrahi ve radyasyon sonrası kolda kalıcı iyatrojenik lenfödem.\n- **Renal Sıvı Tutulumu:** Glomerülonefrit ve böbrek yetmezliğinde GFR düşüşü $\\to$ primer tuz/su retansiyonu $\\to$ hipervolemi $\\to$ hidrostatik basınç ↑ + dilüsyonel onkotik basınç ↓.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Patoloji", "Etiyoloji", "Karakteristik Morfolojik Özellik", "Klinik Önem"],
                [
                    ["Fil Hastalığı (Elefantiyazis)", "Wuchereria bancrofti paraziti", "Masif bacak ve genital lenfödem, kalın deri", "Tropikal paraziter lenfatik hasar"],
                    ["Peau d'Orange", "Meme karsinomu infiltrasyonu", "Meme derisinde portakal kabuğu görünümü", "Lokal ileri evre kanser bulgusu"],
                    ["Aksiller Lenfödem", "Meme cerrahisi ve radyoterapi", "İlgili kolda kalınlaşma ve ağırlık", "Cerrahi komplikasyon"],
                    ["Renal Ödem", "Akut glomerülonefrit / Yetmezlik", "Hipervolemik genel ödem ve hipertansiyon", "Primer sodyum/su atılım kusuru"]
                ]
            ),
            make_chain(
                "Lenfatik ve Renal Ödem Mekanizmaları Özeti",
                [
                    "1. Paraziter/Tümöral Blokaj: Lenf kanalları tıkanır $\\to$ Proteinli lenfödem.",
                    "2. Doku Reaksiyonu: Kronik lenf göllenmesi fibroblastları uyarır $\\to$ Non-pitting sertlik.",
                    "3. Renal Glomerül Hasarı: İdrarla sodyum atılamaz $\\to$ Hipervolemi.",
                    "4. İkili Kuvvet: Damar içi hidrostatik fırlar, albümin dilüe olur $\\to$ Genel ödem."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-16-s60",
        "title": "Bölüm Özeti: Ödem Mekanizmalarından Organ Kliniklerine Geçiş",
        "content": "Bölüm 6 ile birlikte ödemin 5 temel patofizyolojik mekanizmasını (hidrostatik ↑, onkotik ↓, lenfatik tıkanma, Na/su retansiyonu ve permeabilite ↑) eksiksiz tamamladık:\n\n- **Geniş Perspektif:** Mekanizmalar klinik pratikte sıklıkla bir arada işler (ör. sirozda hem hidrostatik artış hem onkotik düşüş vardır).\n- **Sonraki Bölüm:** Bir sonraki bölümde ödemin hayati organlardaki özgül morfolojisini ve ölümcül klinik komplikasyonlarını — **akciğer ödemi** ve **beyin ödemi herniasyonlarını** — inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Meme kanseri tanısı almış bir kadında meme cildinin pürtüklü portakal kabuğu (peau d'orange) manzarası almasına neden olan temel histopatolojik olay nedir?",
                "Tümör embolilerinin subdermal lenfatik damarları tıkaması (lenfatik tümör infiltrasyonu)",
                "Deri altı lenfatik kanalların karsinom hücreleriyle dolması"
            ),
            make_quiz(
                "Aşağıdakilerden hangisi kronik lenfödemi kardiyak kaynaklı hidrostatik ödemden ayıran en önemli klinik ve histopatolojik farktır?",
                [
                    {"key": "A", "text": "Lenfödemde sıvının tamamen su olup sıfır protein içermesi", "isCorrect": False, "explanation": "Lenfödem tam aksine proteinden son derece zengindir."},
                    {"key": "B", "text": "Lenfödemde yüksek protein içeriği ve sekonder doku fibrozisi nedeniyle ödemin sert ve çukur bırakmayan (non-pitting) karakter kazanması", "isCorrect": True, "explanation": "Doğru cevap B'dir: Proteinden zengin lenf sıvısı kronik fibrozise yol açar ve gode bırakmaz (non-pitting)."},
                    {"key": "C", "text": "Lenfödemin sadece göz kapaklarında görülmesi", "isCorrect": False, "explanation": "Göz kapağı nefrotik sendromda tipiktir."},
                    {"key": "D", "text": "Lenfödem hastalarında kan basıncının daima sıfır olması", "isCorrect": False, "explanation": "Kan basıncı sıfır olamaz."}
                ]
            )
        ]
    })

    return slides
