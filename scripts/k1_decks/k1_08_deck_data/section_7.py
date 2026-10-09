"""
Section 7: Telomeraz Biyolojisi, Kanser ve Telomeropatiler (Slayt 61 - 70)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-08-s61",
        "title": "Telomeraz Enzimi: Ters Transkriptaz Ribonükleoproteini",
        "subtitle": "Kromozom uçlarına nükleotid ekleyerek telomer boyunu uzatan enzim",
        "badge": "Enzim Biyolojisi",
        "badgeColor": "indigo",
        "coreContent": {
            "text": (
                "**Telomeraz**, hücrenin kendi RNA kalıbını kullanarak kromozom uçlarına TTAGGG tekrarları ekleyen "
                "özelleşmiş bir ==ribonükleoprotein ters transkriptaz== enzimidir.\n\n"
                "1984 yılında Carol Greider ve Elizabeth Blackburn tarafından keşfedilmiş ve Nobel Tıp Ödülü kazandırmıştır.\n\n"
                "Telomeraz olmaksızın lineer genomların replikasyonu kalıcı bilgi kaybı olmaksızın sürdürülemez."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomer boyunu uzatan telomeraz enzimi biyokimyasal yapı olarak bir ribonükleoprotein ters transkriptaz enzimidir.",
                "ters transkriptaz",
                "RNA kalıbından DNA sentezleyen enzim sınıfı"
            ),
            make_active_recall(
                "Telomeraz enziminin retrovirüs ters transkriptazından en temel yapısal farkı nedir?",
                "Retrovirüs ters transkriptazı dışarıdan gelen viral RNA'yı okurken; telomeraz kendi kalıp RNA molekülünü (TERC) bünyesinde ayrılmaz bir parça olarak taşır."
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-08-s62",
        "title": "TERT ve TERC: Katalitik Çekirdek ve RNA Şablonu",
        "subtitle": "hTERT proteini, hTERC molekülü ve diskerin stabilitesi",
        "badge": "Moleküler Yapı",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "İnsan telomeraz kompleksi iki ana temel bileşenden ve yardımcı proteinlerden oluşur:\n\n"
                "1. **hTERT (Telomerase Reverse Transcriptase):** Enzimin protein yapısındaki katalitik alt birimidir.\n"
                "2. **hTERC (Telomerase RNA Component):** 5'-CUAACCCUAA-3' dizisini içeren ve telomerik TTAGGG'yi sentezleten RNA kalıbıdır.\n"
                "3. **Diskerin (DKC1):** RNA bileşenini stabilize eden nükleolar yardımcı proteindir.\n\n"
                "> Normal somatik hücrelerde hTERC geni açık olmasına rağmen, **hTERT geni suskundur** (kapalıdır); telomeraz aktivitesi hTERT ekspresyonu ile kısıtlanır."
            )
        },
        "interactiveElements": [
            make_table(
                ["Telomeraz Bileşeni", "Kimyasal Yapı", "Hücresel İşlevi"],
                [
                    [("hTERT", False, ""), ("Katalitik Protein Alt Birimi", False, ""), ("DNA sentez reaksiyonunu yürütmek", True, "Uçları polimerize eden enzim faaliyeti")],
                    [("hTERC", False, ""), ("Kodlamayan RNA Molekülü", False, ""), ("TTAGGG hekzanükleotidi için şablonluk yapmak", True, "Kalıp sağlayan nükleik asit")],
                    [("Diskerin", False, ""), ("Nükleolar Yardımcı Protein", False, ""), ("RNA bileşenini parçalanmaktan korumak", True, "Kompleksi stabilize eden nükleolar faktör")]
                ]
            ),
            make_cloze(
                "Normal somatik hücrelerde telomerazın kapalı olmasını belirleyen kısıtlayıcı alt birim hTERT alt birimidir.",
                "hTERT",
                "Telomerase reverse transcriptase katalitik proteini"
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-08-s63",
        "title": "Somatik Kriz Evresi (M2): Köprü-Füzyon-Kırılma Döngüsü",
        "subtitle": "p53 ve Rb yokluğunda telomersiz uçların yapışması ve mitotik felaket",
        "badge": "Genomik Felaket",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "Eğer bir hücrede p53 ve Rb inaktive edilmişse, telomerleri bitse bile M1 senesensine girmez; bölünmeye devam eder.\n\n"
                "Telomerler tamamen tükendiğinde kromozomların çıplak uçları NHEJ ile birbirine yapışır (**uç uca füzyon**).\n\n"
                "Mitozda çift sentromerli kromozomlar zıt kutuplara çekilirken kırılır (**Köprü-Füzyon-Kırılma / BFB döngüsü**).\n\n"
                "Bu tablo **M2 Kriz Evresidir**; hücrelerin %99.9'u masif kromozomal parçalanma ile ==mitotik felakete== (hücre ölümüne) uğrar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomersiz kromozom uçlarının birbirine yapışıp mitozda kopmasıyla tekrarlayan döngüye köprü-füzyon-kırılma döngüsü denir.",
                "köprü-füzyon-kırılma",
                "Bridge-fusion-breakage (BFB) döngüsünün Türkçe karşılığı"
            ),
            make_causal_chain(
                "M2 Kriz Evresinden Tümöral Dönüşüme Giden Yol",
                [
                    "1. Bekçi Kaybı: p53 ve Rb mutasyonuyla hücre senesensi atlatır.",
                    "2. Tam Telomer Kaybı: Kromozom uçlarında tek bir TTAGGG bile kalmaz.",
                    "3. Uç Uca Füzyon: Çıplak kromozomlar dikentrik kromozomlar oluşturur.",
                    "4. Mitotik Felaket: Anafazda kromozomlar yırtılır, masif hücre ölümü başlar.",
                    "5. Kanser Kaçışı: Nadir bir hücre telomerazı açarsa genomik instabiliteyle malignleşir."
                ]
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-08-s64",
        "title": "Kanser Hücrelerinde Telomeraz Reaktivasyonu",
        "subtitle": "M2 krizinden kaçış, hTERT promotör mutasyonları ve hücresel ölümsüzlük",
        "badge": "Karsinojenez",
        "badgeColor": "rose",
        "coreContent": {
            "text": (
                "M2 krizindeki milyonlarca ölen hücre arasından nadir bir mutant klon **hTERT genini yeniden aktive etmeyi** başarır.\n\n"
                "En sık mekanizma **hTERT gen promotöründeki** (C228T, C250T) somatik nokta mutasyonlarıdır (örneğin melanom ve glioblastomda).\n\n"
                "Telomeraz devreye girince telomer boyu stabilize edilir; hücre krizden çıkarak ==ölümsüz (immortal)== hale gelir.\n\n"
                "> İnsan kanserlerinin yaklaşık **%85-90'ında** telomeraz yeniden aktive edilmiştir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "İnsan malign tümörlerinin yaklaşık yüzde 85 ila 90'ında telomeraz enzimi yeniden aktive edilir.",
                "yüzde 85 ila 90'ında",
                "Tümörlerdeki telomeraz reaktivasyon prevalansı"
            ),
            make_active_recall(
                "Glioblastom ve melanom gibi agresif kanserlerde telomerazın yeniden açılmasını sağlayan en yaygın mutasyon bölgesi neresidir?",
                "hTERT geninin çekirdek promotör bölgesindeki (promoter) somatik C228T ve C250T nokta mutasyonlarıdır."
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-08-s65",
        "title": "Alternatif Telomer Uzaması (ALT): Telomeraz Dışı Yolak",
        "subtitle": "Homolog rekombinasyon aracılığıyla telomer kopyalanması (kanserlerin %10-15'i)",
        "badge": "Onkopatoloji",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "Kanser hücrelerinin yaklaşık %10-15'inde telomeraz enzimi hiç aktifleşmez; buna rağmen hücreler ölümsüzleşir.\n\n"
                "Bu tümörler **ALT** (==Alternative Lengthening of Telomeres==) adı verilen mekanizmayı kullanır.\n\n"
                "Hücre, bir kromozomun telomerini diğer bir kromozomun telomeri üzerine kalıp olarak kullanarak **homolog rekombinasyon** ile telomerini uzatır.\n\n"
                "> Tipik olarak osteosarkom, yumuşak doku sarkomları ve glioblastomaların bir alt grubunda (ATRX/DAXX mutasyonlarıyla) görülür."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomeraz enzimi kullanmadan homolog rekombinasyonla telomer uzatan mekanizmaya ALT mekanizması denir.",
                "ALT",
                "Telomeraz bağımsız rekombinatif uzatma mekanizmasının İngilizce baş harfleri"
            ),
            make_before_after(
                "Telomeraz Pozitif Tümör ile ALT Pozitif Tümör",
                "Telomeraz Pozitif Tümör (%90)",
                "hTERT aktiftir; telomer boyları tüm kromozomlarda nispeten uniform ve homojen uzunluktadır.",
                "ALT Pozitif Tümör (%10)",
                "hTERT kapalıdır; homolog rekombinasyon nedeniyle telomer boyları aşırı değişkendir (heterojen kütükler)."
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-08-s66",
        "title": "Telomeropatiler: Kalıtsal Telomeraz Yetersizlikleri",
        "subtitle": "Kök hücre havuzunun erken tükenmesi ve çoklu organ fibrozisleri",
        "badge": "Genetik Patoloji",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "**Telomeropatiler** (Telomer kısalma sendromları), telomeraz enzimini veya Shelterin kompleksini kodlayan "
                "genlerdeki (TERT, TERC, DKC1, TINF2) kalıtsal mutasyonlar sonucu ortaya çıkar.\n\n"
                "Hastalarda telomerler normal bireylere kıyasla kat kat daha hızlı aşınır.\n\n"
                "Özellikle sürekli bölünmek zorunda olan **hematopoetik ve epitelyal kök hücreler** hızla tükenir.\n\n"
                "> Klinik sonuç: Erken yaşta kemik iliği yetmezliği, akciğer fibrozisi, karaciğer sirozu ve erken yaşlanma fenotipi."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomeraz veya telomer bakım genlerindeki kalıtsal mutasyonlar sonucu gelişen hastalıklara telomeropatiler denir.",
                "telomeropatiler",
                "Kalıtsal telomer kısalma sendromları sınıfı"
            ),
            make_active_recall(
                "Telomeropatilerde en erken ve en şiddetli etkilenen hücre tipleri hangileridir ve neden?",
                "Kemik iliği hematopoetik kök hücreleri ve deri/bağırsak epitel kök hücreleridir; çünkü bu dokular sürekli yüksek oranda bölünerek yenilenmek zorundadır."
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-08-s67",
        "title": "Diskeratozis Konjenita: Klasik Telomeropati Modeli",
        "subtitle": "Kutanöz triat, aplastik anemi ve X'e bağlı DKC1 mutasyonu",
        "badge": "Sendrom Biyolojisi",
        "badgeColor": "slate",
        "coreContent": {
            "text": (
                "**Diskeratozis Konjenita**, prototipik kalıtsal telomeropati tablosudur (en sık X'e bağlı **DKC1 / Diskerin** mutasyonu).\n\n"
                "Karakteristik klinik triadı:\n"
                "1. **Distrofik Tırnaklar:** El ve ayak tırnaklarında incelme, boyuna çizgilenme ve dökülme.\n"
                "2. **Ağız İçi Lökoplaki:** Dil ve yanak mukozasında premalign beyaz plaklar.\n"
                "3. **Retiküler Deri Pigmentasyonu:** Boyun ve göğüste dantelsi hiperpigmentasyon.\n\n"
                "> Hastaların %80'den fazlasında hayatı tehdit eden ==Aplastik Anemi== (pansitopeni) gelişir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Diskeratozis konjenitada hastaların hayatını tehdit eden en ağır hematolojik tablo aplastik anemi tablosudur.",
                "aplastik anemi",
                "Kemik iliği kök hücre tükenmesi sonucu gelişen pansitopeni"
            ),
            make_micro_quiz(
                "Distrofik tırnaklar, ağızda lökoplaki ve retiküler boyun pigmentasyonu ile başvuran 12 yaşındaki erkek çocuğun laboratuvarında pansitopeni (aplastik anemi) saptanıyor. En olası altta yatan moleküler defekt nedir?",
                {
                    "A": "Telomeraz diskerin (DKC1) gen mutasyonu sonucu aşırı hızlı telomer kısalması",
                    "B": "WRN gen mutasyonuna bağlı DNA helikaz yetersizliği",
                    "C": "HFE mutasyonuna bağlı aşırı demir emilimi",
                    "D": "CFTR mutasyonuna bağlı klor kanal tıkanıklığı",
                    "E": "Tirozinaz enzim mutasyonu"
                },
                "A",
                {
                    "A": "Doğru cevap A'dır: Diskeratozis konjenita klasik telomeropati tablosudur ve DKC1/telomeraz mutasyonuna bağlıdır.",
                    "B": "Werner sendromu erişkin progeriasıdır.",
                    "C": "Hemokromatozdur.",
                    "D": "Kistik fibrozistir.",
                    "E": "Albinizmdir."
                }
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-08-s68",
        "title": "İdiyopatik Pulmoner Fibrozis ve Karaciğer Sirozunda Telomer Rolü",
        "subtitle": "Erişkin çağda TERT ve TERC heterozigot mutasyonlarının organ yetmezlikleri",
        "badge": "Erişkin Telomeropatisi",
        "badgeColor": "teal",
        "coreContent": {
            "text": (
                "Telomeropatiler sadece çocuklukta görülmez; erişkin yaşta saptanan birçok kronik organ fibrozisinin altında yatar.\n\n"
                "Ailesel **İdiyopatik Pulmoner Fibrozis (IPF)** olgularının yaklaşık %15'inde **TERT veya TERC** heterozigot mutasyonu saptanır.\n\n"
                "Tip II pnömosit kök hücrelerinin erken senesense girmesi alveol hasarının tamirini imkansız kılar; yerini kontrolsüz kollajen skar dokusuna bırakır.\n\n"
                "> Benzer şekilde kriptojenik (nedeni bilinmeyen) karaciğer sirozlarında ve erken saç beyazlamasında telomeraz gen mutasyonları sorumludur."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Ailesel idiyopatik pulmoner fibrozis olgularında en sık saptanan genetik anomali TERT veya TERC mutasyonlarıdır.",
                "TERT veya TERC",
                "Telomeraz enziminin katalitik ve RNA alt birim genleri"
            ),
            make_active_recall(
                "İdiyopatik pulmoner fibrozisli bir hastada telomer kısalması alveolleri nasıl tahrip eder?",
                "Alveol epitelini yenileyen Tip II pnömosit kök hücreleri erkenden senesense girdiği için epitel yenilenemez; hasarlı bölgeye fibroblastlar göç ederek akciğeri bal peteği skarına dönüştürür."
            )
        ]
    })

    # Slide 69 (CHECKPOINT 7)
    slides.append({
        "id": "k1-08-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Telomeraz, Kanser ve Telomeropatiler",
        "subtitle": "Bölüm 7 Ribonükleoprotein Mimarisi, hTERT, M2 Krizi ve Diskeratozis",
        "badge": "Checkpoint 7",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 7,
        "coreContent": {
            "text": (
                "Yedinci kontrol noktasında telomeraz ve hastalık ilişkilerini toparlıyoruz:\n\n"
                "1. **Enzim:** hTERT (protein ters transkriptaz) + hTERC (RNA kalıbı) + Diskerin.\n"
                "2. **Somatik Kriz (M2):** p53/Rb yokluğunda uç uca füzyon ve köprü-füzyon-kırılma (BFB) felaketi.\n"
                "3. **Kanser Ölümsüzlüğü:** Kanserlerin %85-90'ında telomeraz reaktivasyonu; %10'unda ALT yolağı.\n"
                "4. **Telomeropatiler:** Diskeratozis konjenita (tırnak distrofisi, lökoplaki, aplastik anemi).\n"
                "5. **Erişkin Tablolar:** Ailesel idiyopatik pulmoner fibrozis ve kriptojenik siroz."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "Aşağıdakilerden hangisi telomeraz kullanmadan homolog rekombinasyon aracılığıyla telomer boyunu koruyan kanser hücrelerinin mekanizmasıdır?",
                {
                    "A": "MOMP yolağı",
                    "B": "ALT (Alternative Lengthening of Telomeres)",
                    "C": "BFB döngüsü",
                    "D": "BER yolağı",
                    "E": "NHEJ tamiri"
                },
                "B",
                {
                    "A": "MOMP mitokondriyal delinmedir.",
                    "B": "Doğru cevap B'dir: ALT homolog rekombinasyonla telomerazsız ölümsüzlük sağlayan yoldur.",
                    "C": "BFB köprü-füzyon-kırılma krizidir.",
                    "D": "Baz eksizyon onarımıdır.",
                    "E": "Non-homolog uç birleştirmedir."
                }
            ),
            make_active_recall(
                "Diskeratozis konjenitanın patognomonik kutanöz/mukozal triadı nelerden oluşur?",
                "1) Distrofik tırnaklar, 2) Oral mukozal lökoplaki, 3) Retiküler dantelsi boyun/göğüs hiperpigmentasyonudur."
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-08-s70",
        "title": "Telomeraz İnhibitörleri ve Onkolojik Tedavi",
        "subtitle": "Kanser hücrelerinin ölümsüzlüğünü kırma stratejileri (İmetelstat)",
        "badge": "Hedefli Onkoloji",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "Kanser hücrelerinin %90'ı telomeraza bağımlı olduğu için telomeraz onkolojide ideal bir ilaç hedefidir.\n\n"
                "**İmetelstat**, hTERC RNA kalıbına bağlanan lipid konjuge 13-mer oligonükleotid inhibitörüdür.\n\n"
                "Telomerazı bloke ederek malign klonların telomerlerini hızla eritir ve tümör hücrelerini M2 krizine ve apoptoza sürükler.\n\n"
                "> Miyelodisplastik sendrom (MDS) ve miyelofibrozis tedavisinde onay alarak klinik kullanıma girmiştir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Telomerazın RNA kalıbına bağlanarak enzimi inhibe eden ve MDS'de kullanılan onkolojik ajan İmetelstat ilacıdır.",
                "İmetelstat",
                "Lipid bağlı telomeraz oligonükleotid inhibitörü"
            ),
            make_branching_logic(
                "Miyelodisplastik sendromlu bir hastaya telomeraz inhibitörü verildiğinde ilacın tümör hücrelerini yok etme mekanizması nedir?",
                [
                    {"text": "Hücre zarını delerek doğrudan nekroz yapmak", "isCorrect": False, "feedback": "Telomeraz inhibitörleri deterjan etkisi yapmaz."},
                    {"text": "Malign hematopoetik klonların telomer boyunun korunmasını engelleyerek hücreleri mitotik krize ve apoptoza zorlamak", "isCorrect": True, "feedback": "Kusursuz onkolojik etki mekanizması! İmetelstat telomerazı durdurarak kanser hücrelerinin ölümsüzlüğünü bitirir."},
                    {"text": "Kalsiyum çökelmesini artırarak metastatik kalsifikasyon oluşturmak", "isCorrect": False, "feedback": "Kalsiyumla ilgisi yoktur."}
                ]
            )
        ]
    })

    return slides
