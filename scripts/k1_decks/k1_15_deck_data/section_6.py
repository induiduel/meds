# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_6_slides():
    slides = []

    # Slide 51
    slides.append({
        "id": "k1-15-s51",
        "title": "Ekstrasellüler Matriks (ECM) Bileşenleri ve Doku Mimarisi",
        "content": "Doku onarımında hücrelerin yerleştiği ve gerilme kuvveti kazandığı ana çatı ekstrasellüler matrikstir (ECM):\n\n- **ECM'nin Üç Temel Makromolekül Grubu (Sınav Spotu):**\n  1. **Fibriler Yapısal Proteinler (Kollajen ve Elastin):** Dokulara çekme kuvveti (tensile strength) ve geri yaylanma (elastisite) sağlar.\n  2. **Su Tutucu Hidrate Jeller (Proteoglikanlar ve Hyaluronan):** Dokulara basınca ve sıkışmaya karşı direnç (turgor) ve lubrikasyon kazandırır.\n  3. **Yapıştırıcı (Adeziv) Glikoproteinler (Fibronektin ve Laminin):** Matriks elemanlarını birbirine ve hücre yüzeyindeki **integrin reseptörlerine** bağlayan moleküler çimentodur.\n- **Dinamik Dengenin Önemi:** ECM sabit bir betonarme yapı değildir; yara iyileşmesi boyunca sürekli sentezlenir, yıkılır ve yeniden şekillenir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["ECM Grubu", "Temel Moleküller", "Biyomekanik Görevi", "Hastalık Örneği"],
                [
                    ["Fibriler Proteinler", "Kollajen (Tip I-IV), Elastin", "Çekme gerilimine ve yırtılmaya direnç", "Osteogenezis İmperfekta / Skorbüt"],
                    ["Hidrate Jeller", "Proteoglikanlar, Hyaluronik asit", "Basınç direnci ve hücre göç ortamı", "Kıkırdak aşınması / Dehidratasyon"],
                    ["Adeziv Glikoproteinler", "Fibronektin, Laminin", "Hücre-ECM integrin bağlantısı", "Epidermolizis Bülloza (Laminin mutasyonu)"]
                ]
            ),
            make_cloze(
                "ECM bileşenlerini hücre yüzeyindeki integrin reseptörlerine bağlayan temel adeziv glikoproteinler fibronektin ve laminindir.",
                "laminindir",
                "Bazal membranın temel adeziv proteini"
            )
        ]
    })

    # Slide 52
    slides.append({
        "id": "k1-15-s52",
        "title": "Kollajen Tipleri ve Yara İyileşmesindeki Değişim",
        "content": "Vücuttaki en bol protein olan kollajenin yara iyileşmesinde iki ana türü kritik rol oynar (Sınav Sorusu):\n\n- **Kollajen Tipleri ve Dağılımı:**\n  - **Tip I Kollajen:** Deri, kemik, tendon, fasya ve **olgun skar dokusunda** bulunur. Kalın lifler oluşturur; olağanüstü yüksek çekme direncine sahiptir.\n  - **Tip II Kollajen:** Eklem kıkırdağı ve vitreus cismi.\n  - **Tip III Kollajen (Retikülin Lifleri):** Embriyonik dokular, kan damarları ve **erken dönem granülasyon dokusunda** en bol bulunan kollajendir. İnce ve esnek liflerdir.\n  - **Tip IV Kollajen:** Fibril oluşturmaz; epitelyal ve endotelyal **bazal membranları** kuran tabaka tarzı ağ örgüsüdür.\n- **Yara İyileşmesindeki Tipik Değişim (Shift):**\n  - Erken granülasyon dokusunda (ilk hafta) **Tip III kollajen** sentezlenir (hızlı dolgu).\n  - İlerleyen haftalarda Tip III kollajen matriks metalloproteinazlarca yıkılır ve yerini kalıcı, sert **Tip I kollajene** bırakır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Genç Granülasyon Dokusu vs Olgun Skar Dokusu Kollajeni",
                "Genç Granülasyon Dokusu (İlk Hafta)",
                "Baskın olarak Tip III kollajen içerir; lifler ince, gevşek ve gerilme direnci düşüktür.",
                "Olgun Skar Dokusu (Aylar Sonra)",
                "Baskın olarak Tip I kollajen içerir; lifler kalın, çapraz bağlı ve çekme direnci çok yüksektir."
            ),
            make_quiz(
                "Normal yara iyileşmesinde genç granülasyon dokusunda ilk sentezlenen kollajen türü ile aylar sonra olgun skarda en fazla bulunan kollajen türü sırasıyla hangileridir?",
                [
                    {"key": "A", "text": "Tip IV ve Tip II", "isCorrect": False, "explanation": "Tip IV bazal membran, Tip II kıkırdak kollajenidir."},
                    {"key": "B", "text": "Tip III ve Tip I", "isCorrect": True, "explanation": "Doğru cevap B'dir: Erken granülasyon dokusunda Tip III kollajen sentezlenirken, olgun skarda yerini sağlam Tip I kollajene bırakır."},
                    {"key": "C", "text": "Tip I ve Tip III", "isCorrect": False, "explanation": "Sıralama tam tersi olmalıdır."},
                    {"key": "D", "text": "Yalnızca Tip II", "isCorrect": False, "explanation": "Yara skarında Tip II bulunmaz."}
                ]
            )
        ]
    })

    # Slide 53
    slides.append({
        "id": "k1-15-s53",
        "title": "Kollajen Biyosentezi ve C Vitamini Bağımlılığı",
        "content": "Kollajen molekülünün sağlam bir halat gibi örülebilmesi karmaşık bir post-translasyonel biyokimyasal modifikasyon zincirine bağlıdır:\n\n- **1. Pre-Prokollajen Sentezi:** Ribozomlarda sentezlenip granüllü endoplazmik retikuluma (GER) girer.\n- **2. Hidroksilasyon (Hayati Basamak - Sınav Spotu):**\n  - Prokollajen zincirindeki **prolin ve lizin** amino asitleri, sırasıyla **prolil hidroksilaz** ve **lizil hidroksilaz** enzimleri tarafından hidroksillenir.\n  - Bu enzimler kofaktör olarak **C Vitamini (Askorbik Asit)** ve demir ($Fe^{2+}$) kullanmak ZORUNDADIR!\n- **3. Triple-Heliks Kurulması:** Hidroksiprolinler sayesinde üçlü heliks (tropokollajen) oluşur.\n- **4. Hücre Dışına Salınım ve Çapraz Bağlanma:**\n  - Prokollajen peptidazlar uç peptidleri keser.\n  - **Lizil Oksidaz** enzimi (kofaktörü **Bakır - Cu**) kollajen lifleri arasında kovalent çapraz bağlar (cross-links) kurarak dokuya nihai çekme gücünü kazandırır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kollajen Sentez ve Olgunlaşma Zinciri",
                [
                    "1. Polipeptid Sentezi: GER'de pre-prokollajen zinciri üretilir.",
                    "2. C Vitamini ile Hidroksilasyon: Prolil ve lizil artıkları Askorbik Asit kofaktörlüğüyle hidroksillenir.",
                    "3. Üçlü Heliks Teşekkülü: Üç zincir hidrojen bağlarıyla sarılarak prokollajene döner.",
                    "4. Ekzositoz: Molekül Golgiden geçerek hücre dışı ortama salınır.",
                    "5. Lizil Oksidaz ve Çapraz Bağ: Bakır bağımlı lizil oksidaz lifleri kovalent bağlarla kenetler."
                ]
            ),
            make_cloze(
                "Kollajen biyosentezinde prolin ve lizin artıklarının hidroksilasyonu için mutlak gerekli vitamin C vitaminidir.",
                "C",
                "Askorbik asit olarak da bilinen vitamin harfi"
            )
        ]
    })

    # Slide 54
    slides.append({
        "id": "k1-15-s54",
        "title": "C Vitamini Eksikliği (Skorbüt): Yara Açılmasının Biyokimyası",
        "content": "Tarihte denizcileri kırıp geçiren skorbüt hastalığı, doku onarımının biyokimyasal önemini en net gösteren tablodur:\n\n- **Moleküler Kusur (Sınav Spotu):**\n  - C vitamini eksikliğinde prolil ve lizil hidroksilaz enzimleri çalışamaz.\n  - Hidroksiprolin üretilemediği için prokollajen zincirleri kararlı bir üçlü heliks (triple-helix) yapısı oluşturamaz.\n  - Bozuk kollajen polipeptidleri hücre içinde birikir, hücre dışına salınamaz veya salınsa bile hızla parçalanır.\n- **Klinik Yansıması:**\n  - Damar bazal membranları zayıflar; diş etlerinde kanamalar, ciltte peteşi ve purpuralar görülür.\n  - **Yara İyileşmesi Tamamen Durur:** Yeni yaralar hiç kaynamaz.\n  - **Eski Skarların Çözülmesi:** Aylar veya yıllar önce kapanmış eski cerrahi yaralar dahi kollajen turnover'ı bozulduğu için yeniden açılır (yara dehisensi).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Yeterli C Vitamini vs Skorbüt (C Vitamini Yokluğu)",
                "Yeterli C Vitamini (Sağlam Kollajen)",
                "Prolinler hidroksillenir; stabil üçlü heliksler lizil oksidazla kovalent kenetlenerek sağlam skar kurar.",
                "Skorbüt (C Vitamini Eksikliği)",
                "Hidroksilasyon yapılamaz; kollajen heliksi çözülür, damarlar çatlar ve eski yaralar bile tekrar açılır."
            ),
            make_quiz(
                "Uzun süreli C vitamini eksikliğinde (skorbüt) yara iyileşmesinin bozulmasının ve eski skarların açılmasının temel moleküler mekanizması nedir?",
                [
                    {"key": "A", "text": "Lizil ve prolil artıklarının hidroksilasyonunun bozulması sonucu stabil kollajen heliksinin kurulamaması", "isCorrect": True, "explanation": "Doğru cevap A'dır: C vitamini prolil ve lizil hidroksilazın kofaktörüdür; eksikliğinde kollajen üçlü heliksi sentezlenemez."},
                    {"key": "B", "text": "Hücre zarlarında kolesterol sentezinin aşırı artması", "isCorrect": False, "explanation": "Kolesterolle ilgisi yoktur."},
                    {"key": "C", "text": "DNA helikaz enziminin mutasyona uğraması", "isCorrect": False, "explanation": "Genetik bir mutasyon değildir, beslenme yetersizliğidir."},
                    {"key": "D", "text": "Makrofajların fagositoz yeteneğinin sıfırlanması", "isCorrect": False, "explanation": "Doğrudan kollajen hidroksilasyon kusurudur."}
                ]
            )
        ]
    })

    # Slide 55
    slides.append({
        "id": "k1-15-s55",
        "title": "TGF-beta: En Güçlü Fibrogenik Sitokin (Anahtar Faktör)",
        "content": "Doku onarımı, fibrozis ve skar oluşumunun en tartışmasız imparatoru **Transforming Büyüme Faktörü-beta (TGF-β)** molekülüdür (Sınavların 1 Numaralı Spotu):\n\n- **Kaynağı:** M2 makrofajlar, trombositler, endotel hücreleri ve aktive fibroblastlar.\n- **Üçlü Fibrogenik Etki Mekanizması (Sınav Sorusu):**\n  1. **ECM Sentezini Şiddetle Uyarır:** Fibroblastları yara yatağına çeker ve gen düzeyinde Tip I ve Tip III kollajen, fibronektin ve proteoglikan üretimini katbekat artırır.\n  2. **ECM Yıkımını Baskılar:** Kollajeni eriten Matriks Metalloproteinazların (MMP'lerin) sentezini doğrudan bloke eder.\n  3. **Yıkım İnhibitörlerini Artırır:** MMP'leri durduran **TIMP (Doku Metalloproteinaz İnhibitörleri)** sentezini artırır.\n- **Bileşik Sonuç:** Bir taraftan kollajen üretimi zirveye çıkarılırken, diğer taraftan kollajen yıkımı tamamen durdurulur! Bu sayede yara hızla fibröz bağ dokusuyla dolar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "TGF-beta'nın Üçlü Fibrozis Mekanizması",
                [
                    "1. Reseptör Aktivasyonu: TGF-beta serin/treonin kinaz reseptörüne bağlanır.",
                    "2. Smad2/3 Fosforilasyonu: Hücre içi Smad sinyal molekülleri çekirdeğe göç eder.",
                    "3. Kollajen Genlerinin Açılması: Tip I ve Tip III kollajen transkripsiyonu uyarılır.",
                    "4. MMP Enzimlerinin Baskılanması: Kollajen yıkan proteazların üretimi kapatılır.",
                    "5. TIMP Salınımının Artırılması: Matriks yıkımı durdurulur ve yoğun skar dokusu çöker."
                ]
            ),
            make_cloze(
                "Yara iyileşmesi ve kronik fibroziste ekstrasellüler matriks sentezini en güçlü uyaran fibrogenik sitokin TGF-beta molekülüdür.",
                "TGF-beta",
                "En güçlü fibrogenik sitokinin kısaltması"
            )
        ]
    })

    # Slide 56
    slides.append({
        "id": "k1-15-s56",
        "title": "Miyofibroblastlar ve Yara Kontraksiyonu",
        "content": "Granülasyon dokusu oluştuktan sonra yaranın kapanabilmesi için doku defektinin fiziksel olarak daraltılması gerekir:\n\n- **Miyofibroblast Nedir? (Sınav Spotu):**\n  - TGF-β ve PDGF etkisiyle doku fibroblastlarının fenotip değiştirerek düz kas hücrelerine benzeyen kasılabilen bir forma dönüşmesidir.\n  - Sitoplazmalarında yüksek konsantrasyonda **alfa-düz kas aktini (α-SMA)** flamanları içerirler.\n- **Yara Kontraksiyonu (Yaranın Büzülmesi):**\n  - Miyofibroblastlar uzantılarıyla çevrelerindeki kollajen liflerine ve birbirlerine tutunurlar.\n  - Hep birlikte koordineli şekilde kasılarak yara kenarlarını merkeze doğru çekerler.\n  - Özellikle doku kaybının çok geniş olduğu **sekonder iyileşen yaralarda**, yara yüzey alanını **%70-80 oranında küçülterek** iyileşmeyi hızlandırırlar.\n- **Patolojik Aşırılık:** Miyofibroblast kontraksiyonu kontrolsüz devam ederse eklemlerde hareket kısıtlılığına yol açan **kontraktürler** gelişir.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Durgun Fibroblast vs Aktif Kasılabilen Miyofibroblast",
                "Durgun Fibroblast",
                "Kollajen sentezler; kasılma yeteneği düşüktür, düzensiz uzantılara sahiptir.",
                "Miyofibroblast (α-SMA Ekspresyonu)",
                "Hücre içi aktin-miyozin aygıtıyla güçlü bir kasılma oluşturarak yara kenarlarını merkeze çeker."
            ),
            make_quiz(
                "Yara iyileşmesinin 2. haftasında yara alanının büzülerek (kontraksiyon) defektin küçülmesini sağlayan, sitoplazmasında alfa-düz kas aktini (α-SMA) içeren özelleşmiş hücre hangisidir?",
                [
                    {"key": "A", "text": "Miyofibroblast", "isCorrect": True, "explanation": "Doğru cevap A'dır: Miyofibroblastlar alfa-düz kas aktini eksprese ederek yara kontraksiyonunu gerçekleştiren kilit hücrelerdir."},
                    {"key": "B", "text": "Kupffer hücresi", "isCorrect": False, "explanation": "Kupffer hücresi karaciğer makrofajıdır."},
                    {"key": "C", "text": "Mast hücresi", "isCorrect": False, "explanation": "Mast hücreleri histamin salgılar."},
                    {"key": "D", "text": "Osteoblast", "isCorrect": False, "explanation": "Osteoblast kemik yapan hücredir."}
                ]
            )
        ]
    })

    # Slide 57
    slides.append({
        "id": "k1-15-s57",
        "title": "TGF-beta'nın Anti-enflamatuar ve Pleiotropik Rolü",
        "content": "TGF-β yalnızca kollajen yaptıran kör bir molekül değildir; organizmada birden fazla karşıt görevi aynı anda yürüten pleiotropik bir mediyatördür:\n\n- **1. Enflamasyonu Söndürme (İmmünosüpresif Rol):**\n  - TGF-β, lenfosit çoğalmasını, makrofaj aktivasyonunu ve nötrofil infiltrasyonunu güçlü şekilde baskılar.\n  - Akut enflamasyonun bitip doku onarımına geçilmesini garanti eder.\n- **2. Epitel Çoğalmasını Frenleme:**\n  - Karaciğer rejenerasyonunda gördüğümüz gibi, parankim ve epitel hücrelerinde hücre döngüsünü durdurarak (G1 arresti) kontrolsüz büyümeyi engeller.\n- **3. Fibrogenezis (Skar Yapımı):**\n  - Mezenkimal hücreleri uyararak bağ dokusunu artırır.\n- **Klinik İki Yüzü:**\n  - TGF-β yara onarımı için vazgeçilmezdir.\n  - Ancak aşırı ve kronik salınımı karaciğer sirozuna, akciğer pulmoner fibrozisine, böbrek sklerozuna ve keloid gelişimine yol açar!",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Hedef Hücre / Doku", "TGF-beta Etkisi", "Hücresel Sonuç"],
                [
                    ["Fibroblastlar", "Güçlü uyarım", "Aşırı kollajen sentezi ve miyofibroblast dönüşümü"],
                    ["Lenfosit ve Makrofajlar", "Güçlü baskılama", "Enflamasyonun söndürülmesi (immünsüpresyon)"],
                    ["Epitel Hücreleri", "Bölünmeyi durdurma", "G1 arresti ve hücre proliferasyonunun sonlanması"],
                    ["MMP Enzimleri", "Transkripsiyonel blokaj", "Kollajen yıkımının durdurulması"]
                ]
            ),
            make_recall(
                "TGF-beta'nın hem enflamasyonu söndürücü hem de skar yapıcı çift yönlü etkisinin doku onarımındaki amacı nedir?",
                "Zararlı yangıyı durdurarak dokuyu korumak ve eşzamanlı olarak bağ dokusu sentezini uyararak hasarlı doku açığını hızla kapatmaktır."
            )
        ]
    })

    # Slide 58
    slides.append({
        "id": "k1-15-s58",
        "title": "İntegrinler: Hücre ile Matriks Arasındaki Mekanotransdüksiyon",
        "content": "Fibroblastlar yara yatağında ne kadar kollajen sentezleyeceklerini ve ne kadar kasılacaklarını nasıl anlarlar? Hücrelerin 'dokunma duyusu' olan integrinlerle:\n\n- **İntegrin Ailesi:** Hücre zarını boydan boya geçen alfa ve beta heterodimerlerinden oluşan transmembran reseptörleridir.\n- **Çift Yönlü İletişim (Inside-out ve Outside-in):**\n  - Dışarıda ECM'deki **fibronektin, laminin ve kollajene** bağlanırlar.\n  - İçeride hücre iskeletindeki (sitoiskelet) **aktin mikroflamanlarına** tutunurlar.\n- **Mekanotransdüksiyon (Sınav Spotu):**\n  - Yara dokusundaki mekanik gerilimi (tension) hissederler.\n  - Yaranın kenarları gerildikçe integrinler hücre çekirdeğine sinyal göndererek daha fazla kollajen sentezlenmesini ve miyofibroblast kontraksiyonunu emreder.\n  - Yaranın dikişlerle yaklaştırılması mekanik gerilimi düşürerek gereksiz aşırı skar oluşumunu engeller.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Mekanik Gerilimli Yara vs Dikişle Kapatılmış Gerilimsiz Yara",
                "Gerilimli Açık Yara (Yüksek Mekanik Stres)",
                "İntegrinler sürekli sinyal verir; fibroblastlar aşırı kollajen üretir ve geniş, kaba bir skar kalır.",
                "Dikişle Kapatılmış Yara (Düşük Mekanik Stres)",
                "İntegrin uyarısı minimaldir; kontrollü ve incecik bir cerrahi skar hattı ile iyileşir."
            ),
            make_cloze(
                "Ekstrasellüler matriksteki mekanik gerilimi hücre içi aktin iskeletine ileten transmembran reseptör ailesine integrinler denir.",
                "integrinler",
                "Hücre-ECM bağlantısını kuran transmembran protein ailesi"
            )
        ]
    })

    # Slide 59 - CHECKPOINT 6
    slides.append({
        "id": "k1-15-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Fibroblast Aktivasyonu, TGF-beta ve ECM Sentezi",
        "content": "Bu checkpointte kollajen biyolojisini, TGF-beta mekanizmasını ve miyofibroblastları özetliyoruz:\n\n- **ECM Bileşenleri:** Yapısal proteinler (kollajen, elastin), su jelleri (proteoglikan, hyaluronan) ve yapışkanlar (fibronektin, laminin).\n- **Kollajen Değişimi:** Genç granülasyon dokusunda Tip III kollajen; olgun skarda sağlam Tip I kollajen.\n- **C Vitamini:** Prolil ve lizil hidroksilaz kofaktörüdür; eksikliğinde (skorbüt) triple-heliks kurulamaz, yaralar açılır.\n- **Lizil Oksidaz:** Bakır (Cu) bağımlıdır; kollajen lifleri arasında çapraz bağlar kurar.\n- **TGF-beta:** En güçlü fibrogenik sitokin. (1) Kollajen sentezini uyarır, (2) MMP'leri baskılar, (3) TIMP'leri artırır.\n- **Miyofibroblastlar:** Alfa-düz kas aktini (α-SMA) içerir; yara kontraksiyonunu sağlar.\n- **İntegrinler:** ECM ile hücre içi aktin arasında mekanik stres iletimi (mekanotransdüksiyon) sağlar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Molekül / Hücre", "Biyolojik Fonksiyonu", "Eksiklik / Patoloji"],
                [
                    ["C Vitamini", "Prolin/lizin hidroksilasyonu", "Skorbüt, kollajen çöküşü, yara açılması"],
                    ["Bakır (Cu)", "Lizil oksidaz ile çapraz bağ kurma", "Menkes hastalığı, zayıf gerilme direnci"],
                    ["TGF-beta", "Kollajen sentezi, MMP inhibisyonu", "Aşırı salınımında siroz ve keloid"],
                    ["Miyofibroblast", "α-SMA ile yara kontraksiyonu", "Aşırı kasılmada kontraktür sakatlığı"]
                ]
            ),
            make_chain(
                "Kollajen Üretiminden Yara Kontraksiyonuna Akış",
                [
                    "1. M2 Makrofaj Sinyali: Yoğun TGF-beta salgılanır.",
                    "2. Hidroksilasyon ve Sentez: C vitamini desteğiyle fibroblastlar Tip III ve Tip I kollajen üretir.",
                    "3. Çapraz Bağlanma: Bakır bağımlı lizil oksidaz lifleri kenetler.",
                    "4. Miyofibroblast Diferansiasyonu: Fibroblastlar aktin kazanarak miyofibroblasta döner.",
                    "5. Yara Kontraksiyonu: Yara kenarları merkeze doğru çekilerek defekt daraltılır."
                ]
            )
        ]
    })

    # Slide 60
    slides.append({
        "id": "k1-15-s60",
        "title": "Mini Vaka: Yaşlı Bir Hastada C Vitamini Eksikliği ve Yara Dehisensi",
        "content": "74 yaşında yalnız yaşayan, dişleri olmadığı için taze sebze ve meyve tüketmeyen, aylardır sadece çay ve bisküvi ile beslenen bir hastaya fıtık ameliyatı yapılıyor:\n\n- **Ameliyat Sonrası 12. Gün:** Dikişler alındıktan 2 saat sonra hasta öksürdüğünde, ameliyat kesisinin boydan boya açıldığı ve içeriden omentumun dışarı sarktığı (evisserasyon / yara dehisensi) görülüyor.\n- **Klinik Muayene:** Hastanın bacaklarında kıl köklerinde perifoliküler kanamalar (peteşi) ve diş etlerinde morarma saptanıyor.\n- **Patolojik İnceleme:** Yara dudaklarından alınan biyopside, fibroblastların bol olduğu ancak aralarındaki kollajen liflerinin son derece zayıf, amorf ve çapraz bağ kuramamış olduğu izleniyor.\n- **Tanı ve Tedavi:** Skorbüt (C vitamini eksikliği) tanısıyla hastaya yüksek doz oral ve IV askorbik asit başlanıyor; yara tekrar dikildikten sonra 10 günde sağlam skar dokusuyla iyileşiyor.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Ameliyat Kesisinin Açıldığı Skorbütlü Hastaya Müdahale",
                "Hastanın cerrahi yarası dikişler alınır alınmaz açıldığında nöbetçi asistan cerrah 'Hemen hastayı ameliyathaneye alıp kalın çelik tellerle dikelim, başka bir şeye gerek yok' diyor. Kıdemli uzman hekim olarak düzeltmeniz ne olmalıdır?",
                [
                    {
                        "text": "'Haklısın, çelik tel her şeyi çözer, hastanın beslenmesinin cerrahiyle ilgisi yoktur.'",
                        "outcome": "Ölümcül hata: Temelde kollajen sentezi bozuk olduğu için çelik teller de dokuyu keser ve yara tekrar patlar.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Çelik tel yetmez; hastada bariz skorbüt (C vitamini eksikliği) bulguları var. Derhal yüksek doz C vitamini replasmanı başlamalı, dokunun kollajen sentez yeteneğini düzeltmeli ve eşzamanlı destekli cerrahi kapatma yapmalıyız.'",
                        "outcome": "Kusursuz cerrahi-biyokimyasal yaklaşım: Hem mekanik hem moleküler kusur düzeltilir, kalıcı iyileşme sağlanır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Yarayı açık bırakıp hastayı evine gönderelim.'",
                        "outcome": "Ağır peritonit ve ölüm riski.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu vakada hastanın cerrahi yarasının dikişler alınır alınmaz açılmasına yol açan doğrudan biyokimyasal aksaklık nedir?",
                [
                    {"key": "A", "text": "Askorbik asit eksikliğine bağlı prolil ve lizil hidroksilasyonunun durması ve zayıf kollajen sentezi", "isCorrect": True, "explanation": "Doğru cevap A'dır: C vitamini eksikliğinde kollajen üçlü heliksi kurulamaz; doku gerilme kuvveti kazanamadığı için yara dehisensi gelişir."},
                    {"key": "B", "text": "Kanda trombositlerin aşırı pıhtı yapması", "isCorrect": False, "explanation": "Trombosit pıhtısı yarayı açmaz."},
                    {"key": "C", "text": "Hücrelerde ribozomların tamamen yok olması", "isCorrect": False, "explanation": "Ribozom kaybı genel bir ölüm nedenidir."},
                    {"key": "D", "text": "Kemik iliğinde lökosit üretiminin durması", "isCorrect": False, "explanation": "Aplastik anemi tablosu değildir."}
                ]
            )
        ]
    })

    return slides
