# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_3_slides():
    slides = []

    # Slide 21
    slides.append({
        "id": "k1-19-s21",
        "title": "Over Gelişiminin Aktif Genetiği: RSPO1, WNT4, CTNNB1, FOXL2 Dörtlüsü",
        "content": "Eski klasik embriyoloji kitaplarında kadın gelişiminin yalnızca 'erkek sinyalinin yokluğunda kendiliğinden oluşan pasif bir varsayılan yol' olduğu düşünülürdü. Güncel moleküler genetik verileri bu görüşü tamamen çürütmüştür (Sınav Spotu):\n\n- **Aktif Over Kaskadı:** Over gelişimi de en az testis kadar katı ve organize bir genetik program gerektirir.\n- **Dört Anahtar Gen:** SRY yokluğunda pregranüloza hücrelerinde aktifleşen **RSPO1, WNT4, CTNNB1 (β-katenin) ve FOXL2** genleridir.\n- **Çift Yönlü Karşılıklı Baskılama:**\n  - Erkek yolunda SOX9 ve FGF9 over yolunu susturur.\n  - Dişi yolunda ise WNT4/RSPO1/β-katenin ve FOXL2, **SOX9 ve FGF9'un ekspresyonunu aktif olarak bloke eder**.\n- **Klinik Sonuç:** Bu dört genden herhangi birindeki mutasyon, 46,XX bireyde over disgenezisine, virilizasyona veya tam erkek cinsiyet tersinmesine yol açabilir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Over Geni", "Kromozom", "Temel Moleküler Fonksiyonu", "Patoloji"],
                [
                    ["RSPO1", "1p34.3", "Wnt ligand sinyalini güçlendirir, β-katenini stabilize eder", "46,XX cinsiyet tersinmesi, palmar hiperkeratoz"],
                    ["WNT4", "1p36.12", "DAX1'i aktive eder, Leydig benzeri hücreleri baskılar", "Müller aplazisi, SERKAL sendromu"],
                    ["CTNNB1", "3p22.1", "β-katenin; çekirdeğe geçerek over genlerini açar", "Over yetmezliği, teratomlar"],
                    ["FOXL2", "3q23", "Granüloza hücresi kimliği ve postnatal over devamlılığı", "BPES (Blefarofimozis sendromu), POI"]
                ]
            ),
            make_cloze(
                "Dişi gonadal farklılaşmasında pregranüloza hücrelerinde SOX9 ve FGF9'u aktif olarak baskılayan dört temel gen RSPO1, WNT4, CTNNB1 ve FOXL2 genleridir.",
                "FOXL2",
                "Blefarofimozis sendromuyla da ilişkili olan ve 3q23 bölgesinde yer alan over koruyucu transkripsiyon faktörü"
            )
        ]
    })

    # Slide 22
    slides.append({
        "id": "k1-19-s22",
        "title": "WNT4 Geni: 1p36, DAX1 Aktivasyonu ve Müller Kanal Gelişimi",
        "content": "Kromozom 1p36 bölgesinde yer alan **WNT4** (Wnt Family Member 4), potansiyel over gelişiminin birincil sinyal molekülüdür (Sınav Spotu):\n\n- **Ligand Görevi:** WNT4 hücre dışına salgılanan parakrin bir glikoproteindir; Frizzled reseptörlerine bağlanarak hücre içi β-katenin yıkımını engeller.\n- **DAX1 Aktivasyonu:** WNT4 doğrudan X kromozomundaki **DAX1 geninin ekspresyonunu artırır**; DAX1 de SF1'i inhibe ederek SOX9 aktivasyonunu engeller.\n- **Steroidogenez Freni:** Bipotansiyel gonadın erken evrede androjen (testosteron) üretmesini engelleyen moleküler fren WNT4'tür. WNT4 mezenkimal hücrelerin Leydig hücresine dönüşmesini bloke eder.\n- **Müller Kanal Oluşumu:** WNT4 yalnız over için değil, paramezonefrik (Müller) kanallarının mezenkimden epitele dönüşmesi ve fallop tüpü/uterus taslağının kurulması için de zorunludur.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "WNT4 ile Over Farklılaşması ve Testis Baskılanması",
                [
                    "1. Parakrin Sinyal: 1p36 lokusundan salgılanan WNT4 proteini Frizzled reseptörlerine bağlanır.",
                    "2. β-Katenin Stabilizasyonu: Yıkım kompleksi bloke edilerek sitoplazmik β-katenin düzeyi artar.",
                    "3. DAX1 Uyarımı: β-katenin çekirdeğe girerek DAX1 transkripsiyonunu tetikler.",
                    "4. SOX9 ve Leydig İnhibisyonu: DAX1 ve β-katenin, SOX9 ve steroidogenik Leydig yolunu kapatır.",
                    "5. Müller Farklılaşması: Paramezonefrik kanallar tüp ve uterusa farklılaşır."
                ]
            ),
            make_quiz(
                "Over farklılaşmasında DAX1 genini aktive eden, Leydig benzeri hücrelerin androjen üretimini baskılayan ve Müller kanallarının gelişimini destekleyen 1p36 lokusundaki gen hangisidir?",
                [
                    {"key": "A", "text": "WNT4", "isCorrect": True, "explanation": "Doğru cevap A'dır: WNT4 over gelişiminin anahtar ligandıdır, DAX1'i aktive eder ve Müller kanallarının oluşmasını sağlar."},
                    {"key": "B", "text": "SRY", "isCorrect": False, "explanation": "SRY testis belirleyicidir."},
                    {"key": "C", "text": "SOX9", "isCorrect": False, "explanation": "SOX9 testis kaskadının ana faktörüdür."},
                    {"key": "D", "text": "WT1", "isCorrect": False, "explanation": "WT1 böbrek ve erken katlantı genidir."}
                ]
            )
        ]
    })

    # Slide 23
    slides.append({
        "id": "k1-19-s23",
        "title": "WNT4 Mutasyon Spektrumu: Müller Aplazisi, Hiperandrojenizm ve SERKAL",
        "content": "WNT4 genindeki genetik kusurlar, mutasyonun dozu ve türüne bağlı olarak çok farklı fenotipler üretir (Sınav Spotu):\n\n- **Heterozigot İnaktive Edici Mutasyon (46,XX Kadın):**\n  - Müller kanalları düzgün gelişemez; **Müller aplazisi (uterus ve vajina agenezisi)** görülür.\n  - Leydig hücreleri üzerindeki baskı kalktığı için gonadda kontrolsüz androjen sentezi başlar: **Overyan disfonksiyon, hiperandrojenizm ve virilizasyon** (klitoromegali, hirsutizm) ortaya çıkar.\n- **Homozigot Fonksiyon Kaybı (SERKAL Sendromu):**\n  - Otozomal resesif geçişli ölümcül bir sendromdur: **SERKAL** (Seks Reversali, Renal, Adrenal ve Akciğer disgenezi).\n  - 46,XX bireyde tam kadın-erkek cinsiyet tersinmesi, bilateral böbrek agenezisi ve pulmoner hipoplazi görülür.\n- **WNT4 Duplikasyonu / Fonksiyon Artışı (46,XY Erkek):**\n  - Aşırı WNT4 dozu SOX9'u ezer; 46,XY genetik yapısına rağmen testis gelişemez ve **dişi/ambigus fenotip** gelişir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "WNT4 Heterozigot Mutasyon vs Homozigot SERKAL Sendromu",
                "WNT4 Heterozigot (Kadın)",
                "Uterus agenezisi (Müller aplazisi), over disfonksiyonu ve yüksek androjen seviyeleri ile kliniğe gelir.",
                "WNT4 Homozigot (SERKAL)",
                "46,XX cinsiyet tersinmesi, ölümcül renal agenezi, adrenal aplazi ve akciğer hipoplazisi ile seyreder."
            ),
            make_cloze(
                "WNT4 geninin homozigot mutasyonunda 46,XX cinsiyet tersinmesi ile birlikte böbrek, böbrek üstü bezi ve akciğer disgenezisi ile giden tabloya SERKAL sendromu denir.",
                "SERKAL sendromu",
                "WNT4 homozigot kaybında görülen letal sendrom"
            )
        ]
    })

    # Slide 24
    slides.append({
        "id": "k1-19-s24",
        "title": "RSPO1 ve β-Katenin (CTNNB1): Kanonik Wnt Yolu ve Testis Baskılanması",
        "content": "Wnt sinyal yolunun hücre yüzeyindeki en kritik kuvvetlendiricisi **RSPO1** (R-spondin 1) ve hücre içindeki yürütücüsü **CTNNB1** (β-katenin) molekülüdür (Sınav Spotu):\n\n- **RSPO1 Mekanizması:** RSPO1, LGR4/5/6 reseptörlerine ve ZNRF3/RNF43 ubikitin ligazlarına bağlanarak Frizzled reseptörlerinin hücre yüzeyinde kalmasını sağlar; böylece WNT4 sinyalini katbekat artırır.\n- **RSPO1 Mutasyonu ve 46,XX Cinsiyet Tersinmesi:**\n  - RSPO1'in otozomal resesif inaktivasyonunda Wnt/β-katenin yolu çöker.\n  - SRY olmamasına rağmen SOX9 baskılanamaz ve **46,XX bireyde testis dokusu (ovotestis veya tam testis) gelişir**.\n  - Bu tabloya sıklıkla palmar ve plantar hiperkeratoz ile skuamöz hücreli deri kanserine yatkınlık eşlik eder.\n- **β-Katenin (CTNNB1) Rolü:**\n  - β-katenin aşırı aktive edilirse XY gonadı overe dönüşür.\n  - β-katenin knockout edilirse XX gonadı testise dönüşür. Bu durum β-kateninin dişi cinsiyet determinasyonunun omurgası olduğunu gösterir.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_quiz(
                "Karyotipi 46,XX olan bir çocukta ovotestis gelişimi, palmoplantar hiperkeratoz ve deri kanseri yatkınlığı saptanıyor. Bu tabloda en olası genetik defekt hangisidir?",
                [
                    {"key": "A", "text": "RSPO1 mutasyonu", "isCorrect": True, "explanation": "Doğru cevap A'dır: RSPO1 mutasyonları 46,XX bireylerde ovotestis/testis gelişimi ve palmoplantar hiperkeratoz tablosuyla karakterizedir."},
                    {"key": "B", "text": "CYP21A2 mutasyonu", "isCorrect": False, "explanation": "CYP21A2 hiperkeratoz ve testis dokusu yapmaz, adrenal hiperplazi yapar."},
                    {"key": "C", "text": "Androjen reseptör mutasyonu", "isCorrect": False, "explanation": "AR mutasyonu 46,XY bireylerde görülür."},
                    {"key": "D", "text": "FOXL2 mutasyonu", "isCorrect": False, "explanation": "FOXL2 mutasyonu blefarofimozis yapar."},
                ]
            ),
            make_recall(
                "Kanonik Wnt yolunun hücre içi ana mediyatörü olan, yokluğunda XX gonadı testise, aşırı varlığında XY gonadı overe dönüştüren molekül hangisidir?",
                "β-katenin (CTNNB1)",
                "WNT ve RSPO1 sinyalinin çekirdeğe aktarılmasını sağlayan protein"
            )
        ]
    })

    # Slide 25
    slides.append({
        "id": "k1-19-s25",
        "title": "FOXL2 Geni: 3q23, Pregranüloza Hücreleri ve BPES Sendromu",
        "content": "Kromozom 3q23 bölgesinde yer alan **FOXL2**, 'forkhead/winged-helix' ailesine ait çok kritik bir transkripsiyon faktörüdür (Sınav Spotu):\n\n- **Postnatal Over Kimliğinin Korunması:** FOXL2, embriyonik dönemde pregranüloza hücrelerinde başlar ancak asıl mucizesi **doğumdan sonra yaşam boyu overin granüloza hücre kimliğini korumasıdır**; FOXL2 kapatılırsa erişkin bir kadının over hücreleri anında Sertoli hücrelerine dönüşerek testosteron üretmeye başlar.\n- **BPES (Blefarofimozis, Pitozis, Epikantus İnversus Sendromu):**\n  - FOXL2 genindeki heterozigot mutasyonlar otozomal dominant geçişli **BPES** tablosuna yol açar.\n  - **BPES Tip 1:** Göz kapağı malformasyonları (küçük göz açıklığı, düşük kapak) ile birlikte **prematür over yetmezliği (POI) ve infertilite** görülür.\n  - **BPES Tip 2:** Yalnızca göz kapağı bulguları vardır, fertilite korunmuştur.\n- **Klinik Önem:** Göz anomalisi ile başvuran genç bir kızda erken menopoz ve over disfonksiyonu riski akılda tutulmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["BPES Klinik Tipi", "Göz Anomalileri", "Over Fonksiyonu ve Fertilite Durumu"],
                [
                    ["BPES Tip 1", "Blefarofimozis, pitozis, epikantus inversus", "Prematür over yetmezliği (POI), hipergonadotropik hipogonadizm, infertilite"],
                    ["BPES Tip 2", "Blefarofimozis, pitozis, epikantus inversus", "Normal over fonksiyonu ve tam fertilite korunmuştur"]
                ]
            ),
            make_cloze(
                "Blefarofimozis, pitozis ve epikantus inversus ile birlikte prematür over yetmezliğine yol açan FOXL2 geni 3q23 bölgesinde yer alır.",
                "FOXL2",
                "Pregranüloza hücrelerinde eksprese edilen forkhead ailesi over geni"
            )
        ]
    })

    # Slide 26
    slides.append({
        "id": "k1-19-s26",
        "title": "DAX1 (NR0B1): Xp21, Dozaj Duyarlı Cinsiyet Tersinmesi (DSS)",
        "content": "X kromozomunun kısa kolunda (Xp21) yer alan **DAX1** (NR0B1), nükleer reseptör süper ailesine ait atipik bir transkripsiyonel represördür (Sınav Spotu):\n\n- **Dozaj Duyarlı Cinsiyet Tersinmesi (DSS):**\n  - DAX1 bölgesi ilk kez 'Dozaj Duyarlı Cinsiyet Tersinmesi Bölgesi' olarak tanımlanmıştır.\n  - Normal erkekte tek X kromozomunda tek kopya DAX1 vardır ve bu miktar SRY/SOX9'u durdurmaya yetmez.\n  - Ancak 46,XY bir bireyde Xp21 bölgesinde **DAX1 geni duplikasyonu** olursa (çift doz DAX1), SRY'nin etkisi tamamen bastırılır; testis gelişemez ve **46,XY tam cinsiyet tersinmesi (dişi fenotip)** gelişir.\n- **Moleküler Mekanizma:** DAX1, SF1 proteinine doğrudan bağlanarak onun DNA'ya tutunmasını ve SOX9/AMH/steroid enzim genlerini aktive etmesini engeller (SF1 antagonistidir).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_slider(
                "Normal XY (Tek Doz DAX1) vs Duplike DAX1 (Çift Doz DAX1)",
                "Tek Doz DAX1 (Normal Erkek)",
                "SRY ve SF1 hakimdir; SOX9 aktive edilir, AMH ve testosteron üretilir; erkek yönünde gelişir.",
                "Çift Doz DAX1 (XY Cinsiyet Tersinmesi)",
                "Aşırı DAX1 proteini SF1 ve SOX9'u tamamen bloke eder; testis gelişemez; kadın fenotip (streak gonad) oluşur."
            ),
            make_quiz(
                "Karyotipi 46,XY olan ancak Xp21 bölgesinde mikroduplikasyon saptanan bir hastada beklenen primer fenotipik bulgu ve sorumlu gen hangisidir?",
                [
                    {"key": "A", "text": "DAX1 duplikasyonu - Dişi fenotip (46,XY cinsiyet tersinmesi)", "isCorrect": True, "explanation": "Doğru cevap A'dır: Xp21 lokusundaki DAX1 geninin çift kopyası (duplikasyon) dozaj duyarlı cinsiyet tersinmesine ve 46,XY dişi fenotipe yol açar."},
                    {"key": "B", "text": "SRY delesyonu - Normal erkek fenotip", "isCorrect": False, "explanation": "SRY delesyonunda erkek fenotip gelişemez."},
                    {"key": "C", "text": "SOX9 duplikasyonu - İskelet displazisi", "isCorrect": False, "explanation": "SOX9 duplikasyonu iskelet displazisi değil erkek yönünde uyarım yapar."},
                    {"key": "D", "text": "WT1 mutasyonu - Adrenal hiperplazi", "isCorrect": False, "explanation": "WT1 böbrek tümörleri ve FSGS ile ilişkilidir."}
                ]
            )
        ]
    })

    # Slide 27
    slides.append({
        "id": "k1-19-s27",
        "title": "DAX1 Mutasyonları: X'e Bağlı Konjenital Adrenal Hipoplazi",
        "content": "DAX1 geninin duplikasyonu dişi fenotipe yol açarken, fonksiyon kaybı mutasyonları çok farklı bir klinik tabloya neden olur (Sınav Spotu):\n\n- **X'e Bağlı Konjenital Adrenal Hipoplazi (AHC):**\n  - DAX1 (NR0B1) genindeki inaktive edici mutasyonlar veya mikrodelesyonlar, adrenal korteksin fetal zonunun gerileyememesine ve kalıcı korteksin gelişememesine yol açar.\n  - Yenidoğan veya süt çocukluğu döneminde **şiddetli primer adrenal yetmezlik** (tuz kaybı, hiponatremi, hiperkalemi, hipoglisemi, şok) tablosu gelişir.\n- **Hipogonadotropik Hipogonadizm (HH):**\n  - DAX1 hipofiz gonadotrof hücrelerinde de eksprese edilir.\n  - Bu hastalar puberte çağına geldiklerinde LH ve FSH salgılayamazlar; puberteye hiç giremezler (gecikmiş puberte ve infertilite).\n- **Özet:** DAX1 duplikasyonu = 46,XY CGB (dişi fenotip); DAX1 delesyonu/mutasyonu = X'e bağlı adrenal hipoplazi + hipogonadotropik hipogonadizm.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_chain(
                "DAX1 Fonksiyon Kaybının Klinik Seyri",
                [
                    "1. Genetik Kusur: Xp21 lokusundaki DAX1 geninde inaktive edici mutasyon oluşur.",
                    "2. Adrenal Hipoplazi: Kalıcı adrenal korteks tabakaları düzgün gelişemez.",
                    "3. Neonatal Tuz Kaybı: Aldosteron ve kortizol yetersizliğine bağlı adrenal kriz gelişir.",
                    "4. Hipofizer Defekt: Pubertede LH ve FSH gonadotropin salgısı yetersiz kalır.",
                    "5. Hipogonadizm: Sekonder seks karakterleri gelişmez ve infertilite kalıcı olur."
                ]
            ),
            make_cloze(
                "Xp21 bölgesindeki DAX1 geninin inaktive edici mutasyonları X'e bağlı konjenital adrenal hipoplazi ve pubertede hipogonadotropik hipogonadizm tablosuna yol açar.",
                "adrenal hipoplazi",
                "DAX1 mutasyonunda kalıcı korteksin gelişememesi sonucu oluşan böbrek üstü bezi patolojisi"
            )
        ]
    })

    # Slide 28
    slides.append({
        "id": "k1-19-s28",
        "title": "Streak Gonad (İpliksi Gonad) Patolojisi ve Gonadoblastom Riski",
        "content": "Gonadal disgenezi tablolarında karşılaşılan en tipik morfolojik bulgu **streak gonad** (ipliksi/şerit gonad) yapısıdır (Sınav Spotu):\n\n- **Histopatolojik Tanım:** Streak gonad, germ hücrelerinin erken dönemde apoptozise uğraması veya göç edememesi sonucu geride yalnızca fibröz bağ dokusu ve stroma kordonlarının kaldığı işlevsiz beyazımsı bir banttır.\n- **Hormonal Sonuç:** Ne oosit/folikül ne de seminifer tübül içerir; östrojen ve progesteron (veya testosteron) üretemez. Negatif geri besleme kalktığı için **LH ve FSH aşırı yükselir (hipergonadotropik hipogonadizm)**.\n- **Kanser Riski ve Profilaktik Gonadektomi:**\n  - Karyotipinde **Y kromozomu veya Y materyali (GBY bölgesi)** bulunan streak gonadlarda (ör. Swyer sendromu, 45,X/46,XY miks gonadal disgenezi, Frasier sendromu) **%20-30 oranında gonadoblastom ve disgerminom** gelişme riski vardır.\n  - Bu nedenle Y kromozomu taşıyan streak gonadlar tanı anında cerrahi olarak çıkarılmalıdır (profilaktik bilateral gonadektomi).",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Karyotip / Durum", "Streak Gonad Varlığı", "Malignite Riski", "Klinik Yönetim"],
                [
                    ["Turner Sendromu (45,X)", "Bilateral streak gonad", "Y kromozomu yoksa ihmal edilebilir", "Hormon replasmanı (östrojen+progesteron)"],
                    ["Swyer Sendromu (46,XY)", "Bilateral streak gonad", "%20-30 Gonadoblastom / Disgerminom", "Erken profilaktik bilateral gonadektomi"],
                    ["Miks Gonadal Disgenezi (45,X/46,XY)", "Bir tarafta streak, diğerde disgenetik testis", "Yüksek (%15-25)", "Streak gonad eksizyonu ve yakın takip"]
                ]
            ),
            make_quiz(
                "Y kromozomu materyali taşıyan streak gonadlı bireylerde (örneğin 46,XY gonadal disgenezide) erken dönemde cerrahi gonadektomi yapılmasının birincil tıbbi gerekçesi hangisidir?",
                [
                    {"key": "A", "text": "Yüksek oranda gonadoblastom ve disgerminom gelişme riski", "isCorrect": True, "explanation": "Doğru cevap A'dır: Y materyali taşıyan disgenetik gonadlarda gonadoblastom ve malign disgerminom riski çok yüksektir; erken profilaktik gonadektomi şarttır."},
                    {"key": "B", "text": "Aşırı testosteron salgılayarak kalp yetmezliği yapması", "isCorrect": False, "explanation": "Streak gonad hormon üretmez, fibröz banttır."},
                    {"key": "C", "text": "Kistik rüptür ve peritonit oluşturması", "isCorrect": False, "explanation": "Streak gonadlarda kistik patoloji ve peritonit primer risk değildir."},
                    {"key": "D", "text": "Uterusun aşırı büyümesine neden olması", "isCorrect": False, "explanation": "Streak gonad uterus büyümesi yapmaz."}
                ]
            )
        ]
    })

    # Slide 29 - CHECKPOINT 3
    slides.append({
        "id": "k1-19-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Over Gelişimi ve Genetik Düzenleme",
        "content": "Bu checkpointte over gelişimini ve gonadal disgenezi genetiğini özetliyoruz:\n\n- **Over Gelişiminin Dörtlüsü:** RSPO1, WNT4, CTNNB1 (β-katenin) ve FOXL2 pregranüloza hücrelerinde aktifleşerek SOX9 ve FGF9'u bloke eder.\n- **WNT4 (1p36):** DAX1'i aktive eder, Leydig oluşumunu ve androjen üretimini baskılar; Müller kanallarını organize eder. Heterozigot mutasyonunda **Müller aplazisi ve hiperandrojenizm**, homozigot mutasyonunda **SERKAL sendromu** görülür.\n- **RSPO1 (1p34):** Wnt/β-katenin yolunu kuvvetlendirir; kaybında **46,XX cinsiyet tersinmesi ve palmoplantar hiperkeratoz** gelişir.\n- **FOXL2 (3q23):** Doğumdan sonra granüloza hücresi kimliğini korur; mutasyonu **BPES Tip 1 (blefarofimozis + prematür over yetmezliği)** ve Tip 2'ye yol açar.\n- **DAX1 (Xp21):** Çift dozu (duplikasyonu) **46,XY cinsiyet tersinmesine** neden olur. İnaktive edici mutasyonu ise **X'e bağlı adrenal hipoplazi ve hipogonadotropik hipogonadizm** yapar.\n- **Streak Gonad:** Germ hücresiz fibröz banttır; Y kromozomu taşıyan olgularda **gonadoblastom riski** nedeniyle cerrahi olarak çıkarılmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_table(
                ["Over Geni / Tablo", "Temel Mekanizma", "Sınav İçin Anahtar İpucu"],
                [
                    ["WNT4", "DAX1 aktivasyonu ve Müller oluşumu", "Heterozigotta Müller aplazisi; homozigotta SERKAL sendromu"],
                    ["RSPO1", "β-katenin stabilizasyonu", "46,XX cinsiyet tersinmesi + palmoplantar hiperkeratoz"],
                    ["FOXL2", "Granüloza hücresi devamlılığı", "BPES (Blefarofimozis + Prematür Over Yetmezliği)"],
                    ["DAX1 Duplikasyonu", "SF1 inhibisyonu (çift doz etki)", "46,XY kadın fenotip (dozaj duyarlı cinsiyet tersinmesi)"],
                    ["DAX1 Mutasyonu", "Adrenal ve hipofiz defekti", "X'e bağlı adrenal hipoplazi + hipogonadotropik hipogonadizm"]
                ]
            ),
            make_chain(
                "Over Farklılaşması Genetik Özeti",
                [
                    "1. SRY Yokluğu: Bipotansiyel gonadda SOX9 tetiklenmez.",
                    "2. Wnt Aktivasyonu: RSPO1 ve WNT4 ligandları salgılanarak Frizzled reseptörlerini uyarır.",
                    "3. β-Katenin Girişi: Sitoplazmik β-katenin stabilize olarak çekirdeğe girer.",
                    "4. Baskılama ve Farklılaşma: DAX1 aktive olur, steroidogenez frenlenir ve FOXL2 açılır.",
                    "5. Folikül Korunması: Pregranüloza hücreleri primordial folikülleri sarar."
                ]
            )
        ]
    })

    # Slide 30
    slides.append({
        "id": "k1-19-s30",
        "title": "Bölüm Özeti: Gonadlardan İç ve Dış Genital Kanal Farklılaşmasına Geçiş",
        "content": "Bölüm 3 boyunca over gelişiminin aktif genetiğini (WNT4, RSPO1, FOXL2, DAX1) ve streak gonad klinik yaklaşımını inceledik:\n\n- **Özet:** Over gelişimi pasif değildir; WNT4/RSPO1/β-katenin ve FOXL2 eksikliği 46,XX gonadal disgenezi ve maskülinizasyona yol açar.\n- **Sonraki Bölüm (Bölüm 4):** Gonadlar oluştuktan sonra salgılanan hormonların (AMH, Testosteron, 5α-redüktaz ile üretilen DHT) **Wolff ve Müller kanallarını ile genital tüberkül, labioskrotal kabartı ve ürogenital katlantıları nasıl erkek ve dişi organlara dönüştürdüğünü** inceleyeceğiz.",
        "sourcePdf": "Kurul 1 - Ders 19: Doğumsal Kadın-Erkek Gelişim Anomalileri (Dr. Öğr. Üyesi Serap Arslan)",
        "elements": [
            make_recall(
                "3q23 kromozomunda yer alan ve mutasyonunda blefarofimozis ile prematür over yetmezliği (BPES Tip 1) görülen transkripsiyon faktörü hangisidir?",
                "FOXL2",
                "Granüloza hücre kimliğini koruyan forkhead ailesi transkripsiyon faktörü"
            ),
            make_quiz(
                "Xp21 bölgesinde yer alan DAX1 geni ile ilgili ifadelerden hangisi BİYOLOJİK OLARAK DOĞRUDUR?",
                [
                    {"key": "A", "text": "DAX1 geninin çift kopyası (duplikasyonu) 46,XY bireyde cinsiyet tersinmesine yol açar", "isCorrect": True, "explanation": "Doğru cevap A'dır: DAX1 doza duyarlı bir cinsiyet tersinmesi genidir; duplikasyonu SF1'i aşırı baskılayarak 46,XY dişi fenotipe neden olur."},
                    {"key": "B", "text": "DAX1 mutasyonunda hiçbir adrenal problem görülmez", "isCorrect": False, "explanation": "DAX1 inaktivasyonunda X'e bağlı adrenal hipoplazi görülür."},
                    {"key": "C", "text": "DAX1 sadece Y kromozomunda bulunan bir gendir", "isCorrect": False, "explanation": "DAX1 X kromozomundadır (Xp21)."},
                    {"key": "D", "text": "DAX1 doğrudan SOX9'u uyararak testis yapar", "isCorrect": False, "explanation": "DAX1 SOX9'u baskılar, over yönünü destekler."}
                ]
            )
        ]
    })

    return slides
