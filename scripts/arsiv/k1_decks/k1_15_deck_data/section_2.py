# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-15-s11",
        "title": "Kök Hücreler: Kendini Yenileme ve Asimetrik Bölünme",
        "content": "Rejenerasyon ve sürekli doku homeostazının temel kaynağı kök hücrelerdir (stem cells):\n\n- **Kök Hücre Tanımı (Sınav Spotu):** Kendi kendini sınırsız veya uzun süre yenileyebilme (self-renewal) ve özelleşmiş çoklu hücre tiplerine farklılaşabilme (differentiation) yeteneğine sahip farklılaşmamış hücrelerdir.\n- **Asimetrik Bölünme Mekanizması:** Kök hücre bölündüğünde iki hücre oluşur:\n  1. Bir yavru hücre **kök hücre olarak kalır** (böylece kök hücre havuzu tükenmez).\n  2. Diğer yavru hücre **farklılaşma yoluna girer** (progenitör / geçici çoğalan hücre haline gelir ve olgun doku hücrelerine dönüşür).\n- **Önemi:** Asimetrik bölünme olmasaydı, kök hücreler her yaralanmada tükenir ve organizma yaşlandıkça dokularını yenileyemezdi.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Simetrik Bölünme vs Asimetrik Bölünme",
                "Simetrik Bölünme (Havuz Büyümesi)",
                "Bir kök hücreden iki özdeş kök hücre çıkar; embriyogenezde kök hücre rezervini katlamak için kullanılır.",
                "Asimetrik Bölünme (Homeostaz ve Onarım)",
                "Bölünmeyle bir kök hücre rezervde kalırken, diğeri olgun doku hücrelerine dönüşerek hasarı onarır."
            ),
            make_cloze(
                "Kök hücrelerin havuzunu tüketmeden bir yavruyu kök hücre, diğerini farklılaşan hücre yapmasına asimetrik bölünme denir.",
                "asimetrik",
                "Farklılaşma ve rezervi aynı anda koruyan bölünme biçimi"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-15-s12",
        "title": "Embriyonik vs Erişkin (Doku) Kök Hücreleri",
        "content": "Gelişimsel potansiyellerine göre kök hücreler iki ana kategoriye ayrılır:\n\n- **1. Embriyonik Kök Hücreler (ES Hücreleri - Pluripotent):**\n  - Blastokist evresindeki embriyonun iç hücre kitlesinden (inner cell mass) elde edilir.\n  - **Pluripotent Kapasite:** Vücuttaki üç germ yaprağından (ektoderm, mezoderm, endoderm) köken alan her türlü özelleşmiş hücre tipine dönüşebilirler.\n  - Sınırsız kendini yenileme potansiyeline sahiptirler.\n- **2. Erişkin (Doku / Somatik) Kök Hücreleri (Multipotent / Unipotent):**\n  - Olgun organizmanın dokularında özel mikroçevrelerde (niş) sessizce yaşayan hücrelerdir.\n  - **Multipotent / Sınırlı Kapasite:** Genellikle sadece bulundukları dokunun hücre tiplerini üretirler (örneğin hematopoetik kök hücre kan hücrelerini üretir).\n  - Görevleri: Günlük fizyolojik hücre kaybını telafi etmek ve yaralanmalarda hızlı onarım sağlamaktır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Özellik", "Embriyonik Kök Hücre (ES)", "Erişkin Doku Kök Hücresi"],
                [
                    ["Köken", "Blastokist iç hücre kitlesi", "Özel doku nişleri (kemik iliği, bağırsak, beyin)"],
                    ["Potansiyel", "Pluripotent (tüm hücrelere döner)", "Multipotent veya unipotent (dokuya özgü)"],
                    ["Çoğalma Gücü", "Sınırsız (ölümsüz kültür)", "Sınırlı (ihtiyaç halinde aktive olur)"],
                    ["Fizyolojik Rolü", "Tüm embriyonik organogenez", "Doku homeostazı ve hasar onarımı"]
                ]
            ),
            make_quiz(
                "Blastokistin iç hücre kitlesinden izole edilen ve vücuttaki her üç embriyonik germ yaprağına ait tüm hücre tiplerine dönüşebilen kök hücre türü hangisidir?",
                [
                    {"key": "A", "text": "Unipotent kök hücre", "isCorrect": False, "explanation": "Unipotent hücreler sadece tek bir hücre tipine dönüşebilir (ör. spermatogonyum)."},
                    {"key": "B", "text": "Embriyonik pluripotent kök hücre", "isCorrect": True, "explanation": "Doğru cevap B'dir: Blastokist iç hücre kitlesinden türetilen embriyonik kök hücreler pluripotenttir ve her türlü dokuya farklılaşabilir."},
                    {"key": "C", "text": "Hematopoetik multipotent kök hücre", "isCorrect": False, "explanation": "Hematopoetik hücreler erişkin kök hücrelerdir, sadece kan hücrelerini üretir."},
                    {"key": "D", "text": "Post-mitotik nöron", "isCorrect": False, "explanation": "Nöronlar bölünemez, kök hücre değildir."}
                ]
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-15-s13",
        "title": "Kök Hücre Nişi (Niche): Koruyucu Mikroçevre",
        "content": "Erişkin dokularda kök hücreler doku içinde rastgele dağılmaz; **Niş (Niche)** adı verilen son derece özelleşmiş mikroçevrelerde barınırlar:\n\n- **Nişin Yapısı ve Önemi (Sınav Spotu):** Destekleyici stromal hücreler, özelleşmiş ekstrasellüler matriks proteinleri ve parakrin sinyal moleküllerinden (Wnt, Notch, Hedgehog) oluşan korunaklı anatomik yuvadır.\n- **Nişin Görevleri:**\n  - Kök hücreleri mutasyonlardan ve oksidatif stresten korumak.\n  - Kök hücrelerin zamansız farklılaşmasını engelleyerek onları 'sessiz ve uykuda' (quiescent) tutmak.\n  - Hasar anında sinyal vererek kontrollü bölünmeyi ve dokuya göçü tetiklemek.\n- **Tipik Niş Örnekleri:**\n  - **Bağırsak:** Kriptlerin en dibinde, Paneth hücrelerinin hemen yanında (Lgr5+ hücreler).\n  - **Deri:** Kıl folikülünün **kabarıklık (bulge)** bölgesinde.\n  - **Kornea:** Kornea ile konjonktiva sınırındaki **limbus** bölgesinde (limbal kök hücreler).\n  - **Beyin:** Subventriküler zon ve hipokampus gyrus dentatusu.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Organ / Doku", "Kök Hücre Nişi Lokasyonu", "Hasar Sonucu Klinik Tablo"],
                [
                    ["Deri", "Kıl folikülü 'bulge' (şişkinlik) bölgesi", "Derin yanıklarda folikül yoksa re-epitelizasyon çöker"],
                    ["Göz (Kornea)", "Limbus tabakası (kornea-sklera bileşkesi)", "Limbal yetmezlikte kornea matlaşır ve körlük gelişir"],
                    ["Bağırsak", "Liberkühn kriptlerinin tabanı", "Radyasyon hasarında kriptler ölür ve mukoza dökülür"],
                    ["Kemik İliği", "Endosteal ve vasküler sinüzoidal niş", "Aplastik anemi veya pansitopeni"]
                ]
            ),
            make_cloze(
                "Erişkin doku kök hücrelerinin sessizliğini koruyan ve çoğalmasını denetleyen özel mikroçevreye kök hücre nişi denir.",
                "nişi",
                "Kök hücrelerin korunaklı yuvası terimi"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-15-s14",
        "title": "Karaciğer Rejenerasyonu: Kompansatuvar Büyüme Modeli",
        "content": "Karaciğer, insan vücudundaki en muazzam ve en kusursuz rejenerasyon yeteneğine sahip organdır:\n\n- **Yunan Mitolojisinden Tıbba:** Mitolojide Prometheus'un her gün kartal tarafından yenen karaciğerinin her gece yeniden büyümesi, karaciğerin bu olağanüstü biyolojisinin antik çağdan beri bilindiğini gösterir.\n- **Parsiyel Hepatektomi Modeli (Sınav Spotu):**\n  - Bir insanda veya deney hayvanında karaciğerin **üçte ikisi (%60-70)** cerrahi olarak çıkarıldığında (parsiyel hepatektomi), geride kalan sağlam doku hızla büyüyerek **1-2 hafta içinde** orijinal karaciğer ağırlığına ve kütlesine tam olarak ulaşır.\n- **Kritik Patolojik Gerçek: Gerçek Bir 'Yeniden Doğuş' Değil, Kompansatuvar Büyümedir!**\n  - Çıkarılan loblar anatomik olarak eski şekilleriyle tekrar uzamaz!\n  - Bunun yerine geride kalan sağlam loblardaki olgun hepatositler ve vasküler yapılar hiperplazi (hücre sayısı artışı) ve hipertrofi yaparak orijinal kütleyi tamamlar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Klasik Morfogenetik Yenilenme vs Karaciğer Kompansatuvar Büyümesi",
                "Morfogenetik Yenilenme (Semender Bacağı)",
                "Kesilen uzuv anatomik parmakları ve eklemleriyle sıfırdan aynı biçimde uzar.",
                "Karaciğer Kompansatuvar Büyümesi",
                "Kesilen loblar geri çıkmaz; geride kalan mevcut loblar büyüyüp genişleyerek orijinal ağırlığa ulaşır."
            ),
            make_recall(
                "Parsiyel hepatektomi sonrası karaciğerin eski boyutuna ulaşması neden 'gerçek bir uzuv rejenerasyonu' değil de 'kompansatuvar hiperplazi' olarak tanımlanır?",
                "Çünkü kesilip çıkarılan loblar orijinal anatomik şekilleriyle yeniden oluşmaz; geride kalan sağlam loblardaki hepatositler bölünerek kütleyi tamamlar."
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-15-s15",
        "title": "Karaciğer Rejenerasyonu Faz 1: Başlatma (Priming Fazı)",
        "content": "Karaciğer rejenerasyonu bir yarış arabasının motorunu çalıştırmaya benzer; önce kontak açılır (priming), sonra gaza basılır (proliferasyon):\n\n- **Priming (Uyarılmaya Hazırlık) Nedir? (Sınav Spotu):**\n  - Normalde G0 fazında dinlenen hepatositlerin büyüme faktörlerine yanıt verebilecek duyarlılığa getirilmesi sürecidir.\n  - Tek başına priming mitozu başlatmaz; hücreyi büyüme faktörlerinin 'bölün' emrine hazır hale getirir.\n- **Hücresel Aktör: Kupffer Hücreleri:**\n  - Doku rezeksiyonu veya hasarından hemen sonra karaciğerin yerleşik makrofajları olan Kupffer hücreleri aktive olur.\n  - Kupffer hücreleri **Tümör Nekroz Faktörü (TNF)** ve **İnterlökin-6 (IL-6)** salgılar.\n- **Sinyal Yolağı:** TNF ve IL-6 hepatositlerdeki NF-kB ve STAT3 yolaklarını aktive eder. Bu sayede hepatositler G0 fazından G1 fazına adım atar.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Karaciğer Rejenerasyonunda Priming Fazı Basamakları",
                [
                    "1. Cerrahi Rezeksiyon / Hasar: Karaciğer doku kütlesi aniden üçte iki oranında azalır.",
                    "2. Kupffer Hücresi Uyarımı: Sinüzoidal makrofajlar hemodinamik ve metabolik stresi algılar.",
                    "3. TNF ve IL-6 Salınımı: Kupffer hücreleri parakrin olarak yüksek düzeyde TNF ve IL-6 salar.",
                    "4. NF-kB ve STAT3 Aktivasyonu: Hepatosit çekirdeğinde transkripsiyon faktörleri uyarılır.",
                    "5. G0'dan G1'e Geçiş (Hazırlık): Hepatositler büyüme faktörlerine duyarlı hale gelir (Priming tamamlanır)."
                ]
            ),
            make_quiz(
                "Parsiyel hepatektomi sonrası karaciğer rejenerasyonunun 'priming (başlatma)' fazında hepatositlerin G0'dan G1'e geçişini sağlayan temel sitokinler hangi seçenekte doğru verilmiştir?",
                [
                    {"key": "A", "text": "TGF-beta ve İnterferon-gama", "isCorrect": False, "explanation": "TGF-beta rejenerasyonu durduran inhibitör sitokindir."},
                    {"key": "B", "text": "TNF ve IL-6", "isCorrect": True, "explanation": "Doğru cevap B'dir: Priming fazında Kupffer hücrelerinden salınan TNF ve IL-6, hepatositleri büyüme faktörlerine duyarlı hale getirir."},
                    {"key": "C", "text": "Histamin ve Serotonin", "isCorrect": False, "explanation": "Bunlar akut vazoaktif aminlerdir."},
                    {"key": "D", "text": "İnsülin ve Glukagon", "isCorrect": False, "explanation": "Pankreatik hormonlardır, primer priming sitokinleri değildir."}
                ]
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-15-s16",
        "title": "Karaciğer Rejenerasyonu Faz 2: Proliferasyon Fazı",
        "content": "Priming aşamasını tamamlayan hepatositler, kan dolaşımındaki ve stromadaki güçlü büyüme faktörlerinin etkisiyle hızla hücre döngüsünde ilerler:\n\n- **Kilit Büyüme Faktörleri (Sınav Spotu):**\n  - **Hepatosit Büyüme Faktörü (HGF):** Karaciğerdeki fibroblastlar, endotel hücreleri ve hepatik stellat hücreler tarafından üretilir; hepatosit üzerindeki **c-Met (MET)** reseptör tirozin kinazına bağlanarak en güçlü mitojenik etkiyi yaratır.\n  - **Epidermal Büyüme Faktörü (EGF) ve TGF-alfa:** Hepatosit proliferasyonunu ve DNA sentezini (S fazına girişi) güçlü şekilde uyarır.\n- **Dalga Dalga Çoğalma Sırası:**\n  1. Önce **hepatositler** bölünür (ilk 24-48 saatte DNA sentezi zirve yapar).\n  2. Ardından sinüzoidleri döşeyen **endotel hücreleri**, **Kupffer hücreleri** ve **stellat hücreler** çoğalır.\n  3. Yeni oluşan hücrelerECM bazal membranını örerek düzenli hepatik kordonlar ve lobüller halinde organize olur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Priming Fazı (Hazırlık) vs Proliferasyon Fazı (Bölünme)",
                "Priming Fazı (TNF / IL-6)",
                "Hepatositleri uykudan (G0) uyandırır, büyüme faktörü reseptörlerini hazır hale getirir.",
                "Proliferasyon Fazı (HGF / EGF / TGF-α)",
                "c-Met ve EGFR üzerinden hücreyi S fazına sokarak devasa bir mitoz dalgası başlatır."
            ),
            make_cloze(
                "Karaciğer rejenerasyonunda hepatosit mitozunu en güçlü uyaran ve c-Met reseptörüne bağlanan faktör hepatosit büyüme faktörüdür.",
                "büyüme",
                "HGF faktörünün ortasındaki biyolojik kelime"
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-15-s17",
        "title": "Karaciğer Rejenerasyonu Faz 3: Sonlanma (Terminasyon Fazı)",
        "content": "Rejenerasyon sürecinde 'bölünmeyi başlatmak' kadar, doku orijinal boyutuna ulaştığında 'bölünmeyi zamanında durdurmak' da hayati önem taşır; durmazsa tümör gelişir:\n\n- **Terminasyonun Amacı:** Karaciğer kütlesi vücut ağırlığının tam %100'üne ulaştığında çoğalmayı derhal frenlemektir.\n- **En Kritik İnhibitör Sitokin (Sınav Spotu): Transforming Büyüme Faktörü-Beta (TGF-β):**\n  - Karaciğer orijinal kütlesine yaklaştığında stellat hücrelerden ve endotelden yoğun şekilde salınır.\n  - Hepatositlerde hücre döngüsünü durdurucu proteinleri (p15, p21, p27 gibi siklin bağımlı kinaz inhibitörlerini) uyarır.\n  - Hepatositlerin mitozunu kesin olarak bloke eder.\n- **Aktivinler ve Temas İnhibisyonu:** Hücreler birbirine sıkıca temas ettiğinde katenin ve kadherin sinyalleri de çoğalmayı durdurur.\n- **Sonuç:** Karaciğer orijinal boyut ve ağırlığına ulaştığı anda kusursuz bir hassasiyetle durur.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Rejenerasyon Fazı", "Anahtar Moleküller", "Hücre Siklusu Düzeyi", "Hücresel Olay"],
                [
                    ["1. Priming (Başlama)", "TNF, IL-6 (Kupffer kaynaklı)", "G0 -> G1 geçişi", "Hepatositlerin mitoza duyarlı kılınması"],
                    ["2. Proliferasyon (Çoğalma)", "HGF (c-Met), EGF, TGF-alfa", "S ve M fazları", "Hızlı DNA replikasyonu ve hepatosit mitozu"],
                    ["3. Terminasyon (Durdurma)", "TGF-beta, Aktivinler", "G1 arresti (p21, p27)", "Kütle tamamlanınca çoğalmanın frenlenmesi"]
                ]
            ),
            make_quiz(
                "Karaciğer rejenerasyonunun sonlanma (terminasyon) aşamasında hepatosit çoğalmasını durduran ve hücre döngüsünü frenleyen en önemli inhibitör sitokin hangisidir?",
                [
                    {"key": "A", "text": "HGF (Hepatosit Büyüme Faktörü)", "isCorrect": False, "explanation": "HGF mitozu uyarır, durdurmaz."},
                    {"key": "B", "text": "TGF-beta", "isCorrect": True, "explanation": "Doğru cevap B'dir: TGF-beta, karaciğer rejenerasyonunda ve hücre döngüsünde en güçlü antiproliferatif ve terminatör sitokindir."},
                    {"key": "C", "text": "IL-6", "isCorrect": False, "explanation": "IL-6 priming fazında rol oynar."},
                    {"key": "D", "text": "VEGF", "isCorrect": False, "explanation": "VEGF anjiyogenezi uyarır."}
                ]
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-15-s18",
        "title": "Karaciğerde Kök Hücre Kompartımanı: Oval Hücreler ve Hering Kanalları",
        "content": "Peki karaciğer hasarı hepatositlerin çoğalamayacağı kadar ağırsa (örneğin kronik hepatit, siroz veya ağır toksik nekroz) ne olur?\n\n- **Yedek Kök Hücre Rezervi (Sınav Spotu):**\n  - Normalde karaciğer rejenerasyonunu hepatositlerin kendisi yürütür; kök hücrelere ihtiyaç duyulmaz.\n  - Ancak hepatositler yaşlanmış (senesens), kronik virüsle tükenmiş veya bölünemez hale gelmişse karaciğerin kök hücreleri devreye girer.\n- **Hering Kanalları ve Oval Hücreler:**\n  - Biliyer sistem ile hepatosit kordonlarının birleştiği mikroskopik **Hering kanallarında** karaciğer kök hücreleri (progenitör hücreler) yerleşiktir.\n  - Kemirgenlerde oval şekilli oldukları için **'oval hücreler'** olarak adlandırılır.\n  - **Bipotansiyel Güç:** Bu progenitör hücreler hem yeni **hepatositlere** hem de safra kanalı epitel hücrelerine (**kolanjiyositlere**) dönüşebilirler.\n- **Klinik Yansıması:** Ağır sirotik karaciğer biyopsilerinde görülen 'duktular reaksiyon' bu kök hücrelerin çaresizce çoğalma çabasıdır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Ağır Kronik Karaciğer Hasarında Oval Hücre Aktivasyonu",
                [
                    "1. Hepatosit Tükenmesi: Kronik hepatit B/C veya toksin hepatositlerin bölünmesini bloke eder.",
                    "2. Sinyal Yayılımı: Karaciğer doku kütlesini tamamlayabilmek için kök hücre nişini uyarır.",
                    "3. Hering Kanalı Proliferasyonu: Safra kanalcığı diplerindeki oval/progenitör hücreler uyanır.",
                    "4. Bipotansiyel Farklılaşma: Oval hücreler çoğalarak hepatosit ve kolanjiyosit öncüllerini üretir.",
                    "5. Duktular Reaksiyon: Patolog biyopside safra kanalı proliferasyonu ve duktular reaksiyonu izler."
                ]
            ),
            make_cloze(
                "Hepatositlerin bölünemediği ağır karaciğer hasarlarında Hering kanallarındaki oval kök hücreler devreye girer.",
                "oval",
                "Karaciğer progenitör hücresinin morfolojik adı"
            )
        ]
    })

    # Slide 19 - CHECKPOINT 2
    slides.append({
        "id": "k1-15-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Kök Hücre Biyolojisi ve Karaciğer Rejenerasyonu",
        "content": "Bu checkpointte kök hücre dinamiklerini ve karaciğerin üç fazlı rejenerasyonunu özetliyoruz:\n\n- **Kök Hücre Özellikleri:** Kendi kendini yenileme (self-renewal) ve asimetrik bölünme.\n- **Embriyonik (Pluripotent) vs Erişkin (Multipotent):** Embriyonik kök hücreler 3 germ yaprağının tamamını üretir.\n- **Kök Hücre Nişi:** Kök hücreleri koruyan ve uykuda tutan özel anatomik mikroçevre (bağırsak kript tabanı, saç folikülü bulge).\n- **Karaciğer Kompansatuvar Büyümesi:** 2/3 rezeksiyon sonrası geride kalan hepatositlerin hiperplazisiyle 1-2 haftada eski kütleye ulaşılır.\n- **Üç Aşamalı Faz:**\n  1. **Priming Fazı:** Kupffer hücreleri -> TNF ve IL-6 -> G0'dan G1'e hazırlık.\n  2. **Proliferasyon Fazı:** HGF (c-Met), EGF, TGF-alfa -> S fazı ve yoğun mitoz.\n  3. **Terminasyon Fazı:** TGF-beta ve aktivinler -> Rejenerasyonu zamanında durdurma.\n- **Yedek Kök Hücre:** Hering kanallarındaki bipotansiyel oval hücreler (hepatosit + kolanjiyosit).",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Karaciğer Rejenerasyon Fazı", "Tetikleyici Molekül", "Kaynak Hücre", "Görevi"],
                [
                    ["Priming", "TNF ve IL-6", "Kupffer hücreleri", "Hepatositleri mitoza duyarlı kılmak"],
                    ["Proliferasyon", "HGF (c-Met)", "Stellat ve endotel hücreleri", "DNA sentezi ve mitozu başlatmak"],
                    ["Terminasyon", "TGF-beta", "Stellat hücreler ve endotel", "Kütle tamamlanınca çoğalmayı frenlemek"]
                ]
            ),
            make_slider(
                "Hepatosit Rejenerasyonu vs Oval Hücre Rejenerasyonu",
                "Akut Hasar (Hepatosit Proliferasyonu)",
                "Parsiyel hepatektomide sağlam hepatositler hızla bölünerek kütleyi tek başına tamamlar.",
                "Kronik Hasar (Oval Kök Hücre Aktivasyonu)",
                "Hepatositler yaşlanıp tükendiğinde Hering kanallarındaki oval kök hücreler devreye girer."
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-15-s20",
        "title": "Mini Vaka: Canlı Vericili Karaciğer Nakli Sonrası Donörün İyileşmesi",
        "content": "32 yaşında sağlıklı bir donör, siroz hastası kardeşine karaciğer nakli için sağ lobunu (%60 karaciğer hacmi) bağışlıyor. Başarılı bir cerrahi operasyonla sağ lob alınıyor:\n\n- **1. Gün:** Donörün kalan sol karaciğer lobundaki Kupffer hücreleri hemodinamik değişimi algılayarak hızla TNF ve IL-6 salgılıyor (Priming fazı).\n- **3. Gün:** HGF ve TGF-alfa seviyeleri zirve yapıyor; kalan sol lobdaki hepatositlerin %90'ından fazlası S fazına girerek hızla bölünüyor (Proliferasyon fazı).\n- **4. Hafta:** Kontrol abdominal BT anjiyografide, donörün kalan karaciğerinin hiperplazi ile büyüyerek ameliyat öncesi toplam karaciğer hacminin %92'sine ulaştığı ve biyokimya testlerinin (AST, ALT, Bilirubin, Albumin) tamamen normale döndüğü görülüyor.\n- **Sonuç:** TGF-beta salınımı ile proliferasyon durdurulmuş, organ kusursuz bir kompanse kütleye ulaşmıştır.",
        "sourcePdf": "Kurul 1 - Ders 15: Doku Onarımı ve Yara İyileşmesi (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Klinik Karar: Donörün Karaciğer Fonksiyonlarını İzleme",
                "Karaciğer donörü ameliyatın 3. gününde 'Doktor bey, karnımdaki kesilen sağ lob yeniden uzayıp eski şekline geldi mi?' diye soruyor. En doğru patolojik yaklaşım hangisidir?",
                [
                    {
                        "text": "'Evet, kesilen sağ lob aynı bir ağaç dalı gibi orijinal şekliyle yerine uzamıştır.'",
                        "outcome": "Anatomik yanılgı: Kesilen lob geri çıkmaz.",
                        "isCorrect": False
                    },
                    {
                        "text": "'Hayır, kesilen sağ lob geri çıkmaz; ancak kalan sol lobdaki hücreler bölünerek büyüdü ve karaciğerinizin toplam hacmini ve çalışma gücünü orijinal seviyesine getirdi.'",
                        "outcome": "Kusursuz hekim açıklaması: Kompansatuvar hiperplazi mantığı hastaya net ve dürüstçe aktarılır.",
                        "isCorrect": True
                    },
                    {
                        "text": "'Karaciğeriniz hiç büyümedi, kalan parça aşırı yorularak çalışıyor.'",
                        "outcome": "Yanlış ve gereksiz panik yaratan ifade.",
                        "isCorrect": False
                    }
                ]
            ),
            make_quiz(
                "Bu nakil vakasında donörün kalan karaciğer lobundaki hepatositlerin hızla çoğalmasını sağlayan temel büyüme faktörü ve reseptör ikilisi hangisidir?",
                [
                    {"key": "A", "text": "HGF ve c-Met reseptörü", "isCorrect": True, "explanation": "Doğru cevap A'dır: Hepatosit proliferasyonunun ana itici gücü HGF'nin c-Met reseptör tirozin kinazını aktive etmesidir."},
                    {"key": "B", "text": "Eritropoietin ve JAK2", "isCorrect": False, "explanation": "Eritropoietin kemik iliğinde alyuvar yapımını uyarır."},
                    {"key": "C", "text": "Kalsitonin ve Tiroid reseptörü", "isCorrect": False, "explanation": "Kalsitonin kalsiyum metabolizması hormonudur."},
                    {"key": "D", "text": "Prolaktin ve Meme reseptörü", "isCorrect": False, "explanation": "Süt salgısı hormonudur."}
                ]
            )
        ]
    })

    return slides
