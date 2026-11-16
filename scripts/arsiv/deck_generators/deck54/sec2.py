"""
Deck 54 - Section 2: Leiomyosarkom ve Benign/Malign Ayırıcı Tanısı (Slayt 11-20)
Slayt 20: Checkpoint 2
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec2_slides():
    slides = []
    
    # Slide 11
    slides.append(make_slide(
        slide_num=11,
        title="Leiomyosarkom: Genel Tanım ve Demografi",
        subtitle="Postmenopozal çağda soliter ve de novo gelişen malignite",
        clinical_focus="Leiomyosarkomun epidemiyolojik profili ve yaş dağılımı",
        narrative=(
            "Leiomyosarkom, myometriumdaki düz kas hücrelerinden köken alan nadir fakat oldukça agresif bir malign mezenkimal tümördür. "
            "Uterin malignitelerin küçük bir bölümünü oluştursa da kötü prognozu nedeniyle büyük klinik öneme sahiptir.\n\n"
            "- **Yaş ve Menopozal Durum:** Leiomyomların aksine neredeyse her zaman postmenopozal dönemdeki kadınlarda (genellikle 50-60'lı yaşlar ve üzeri) ortaya çıkar.\n"
            "- **Lezyon Sayısı:** Leiomyomlar sıklıkla multiple odaklar halinde bulunurken, leiomyosarkomlar neredeyse istisnasız olarak tek bir kitle (soliter lezyon) şeklindedir.\n"
            "- **Irksal ve Klinik Profil:** Postmenopozal kanama, hızla büyüyen pelvik kitle ve alt karın ağrısı ile hekime başvurulur.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyomların en sık görüldüğü reprodüktif dönemin aksine, leiomyosarkom tipik bir postmenopozal çağ malignitesidir ve soliter kitle olarak prezente olur."
        ),
        bullets=[
            "Myometrium düz kasının nadir ve agresif malign neoplazmıdır",
            "Neredeyse her zaman postmenopozal dönemde saptanır",
            "Leiomyomların aksine her zaman soliter (tek odaklı) kitledir",
            "Postmenopozal kanama ve hızlı kitle büyümesi temel semptomdur"
        ],
        elements=[
            make_quiz(
                question="Myometrium kaynaklı malign bir neoplazm olan leiomyosarkomun tipik hasta demografisi ve odak sayısı aşağıdakilerden hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "Prepubertal kız çocukları — Bilateral multiple odaklar", "isCorrect": False, "explanation": "Prepubertal dönemde izlenmez; çocukluk çağında botriyoid rabdomyosarkom görülür."},
                    {"key": "B", "text": "Adolesan dönem — Uterusu diffüz dolduran poliklonal nodüller", "isCorrect": False, "explanation": "Adolesanlarda sarkom izlenmez; bu dönemde anovulatuar kanamalar sıktır."},
                    {"key": "C", "text": "Reprodüktif çağ — Myometriumda en az 5-10 adet nodül", "isCorrect": False, "explanation": "Reprodüktif çağda multiple nodüller benign leiomyomun özelliğidir."},
                    {"key": "D", "text": "Postmenopozal dönem — Uterusta tek (soliter) kitle", "isCorrect": True, "explanation": "Doğru. Leiomyosarkomlar tipik olarak postmenopozal yaş grubunda ve her zaman soliter kitle olarak ortaya çıkarlar."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Malign bir düz kas tümörü olan leiomyosarkomlarda lezyon her zaman soliter olup postmenapozal dönemde izlenirler.",
                masked_term="her zaman soliter",
                hint="Miyomdaki çok odaklılığın aksine tek kitle olma durumu"
            ),
            make_slider(
                left_title="Benign Leiomyom Profili",
                right_title="Malign Leiomyosarkom Profili",
                left_points=[
                    "Aktif reprodüktif çağdaki genç kadınlarda (%30-50) sıktır",
                    "Uterusta sıklıkla birden fazla (multiple) nodül bulunur",
                    "Östrojen bağımlı olup menopoz sonrasında küçülür"
                ],
                right_points=[
                    "Postmenopozal ileri yaştaki kadınlarda ortaya çıkar",
                    "Uterusta neredeyse her zaman tek (soliter) kitle izlenir",
                    "Hormondan bağımsız hızlı kitle büyümesi ve kanama yapar"
                ]
            ),
            make_recall(
                question="Leiomyom ile leiomyosarkom arasında lezyon sayısı ve hasta yaşı açısından en temel ayrım nedir?",
                answer="Leiomyom reprodüktif çağda ve sıklıkla multiple iken; leiomyosarkom postmenopozal çağda ve her zaman soliterdir."
            )
        ]
    ))

    # Slide 12
    slides.append(make_slide(
        slide_num=12,
        title="Leiomyosarkom: De Novo Gelişim Kuralı",
        subtitle="Malign transformasyon efsanesi ve prekürsörsüz başlangıç",
        clinical_focus="Leiomyomların sarkoma dönüşmediği gerçeği ve onkolojik yaklaşım",
        narrative=(
            "Patoloji ve jinekoloji pratiğinde en sık yapılan kavram yanılgılarından biri, benign leiomyomların zamanla malignleşerek leiomyosarkoma dönüştüğü inancıdır. "
            "Modern moleküler, sitogenetik ve histopatolojik veriler bu iddiayı kesin olarak çürütmüştür.\n\n"
            "- **De Novo Gelişim:** Leiomyosarkomlar önceden var olan benign bir leiomyom odağının içinden malign transformasyonla değil, myometriumdaki düz kas hücrelerinden doğrudan doğruya (**de novo**) gelişirler.\n"
            "- **Farklı Moleküler Yolaklar:** Leiomyomlarda MED12 mutasyonları ve HMGA2 yeniden düzenlenmeleri bulunurken; leiomyosarkomlarda kompleks anöploidi, TP53 mutasyonları ve RB1 kayıpları izlenir; genetik profilleri tamamen farklıdır.\n"
            "- **Lezyon Sayısı ve Risk:** Hastada çok sayıda (multiple) leiomyom bulunması maligniteye dönüşüm riskini hiçbir şekilde artırmaz.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyomlar sarkoma dönüşmezler ve multiple olmaları malignite riskini artırmaz; leiomyosarkom daima de novo ortaya çıkar."
        ),
        bullets=[
            "Leiomyosarkomlar daima de novo (sıfırdan) gelişir",
            "Benign leiomyomdan malign dönüşüm kanıtlanmamıştır",
            "Miyom sayısı fazlalığı (multiple miyomatöz) sarkom riskini artırmaz",
            "Moleküler ve sitogenetik mutasyon yolakları birbirinden tamamen bağımsızdır"
        ],
        elements=[
            make_quiz(
                question="Leiomyomların biyolojik seyri ve leiomyosarkom patogenezi ile ilgili aşağıdaki temel ilkelerden hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Submukoz leiomyomların en az %20'si 10 yıl içinde leiomyosarkoma dönüşür.", "isCorrect": False, "explanation": "Yanlış. Leiomyomlar histolojik tip fark etmeksizin sarkoma dönüşmezler."},
                    {"key": "B", "text": "Leiomyosarkomlar öncül benign miyom olmaksızın doğrudan de novo gelişirler.", "isCorrect": True, "explanation": "Doğru. Leiomyosarkomlar benign miyomun malignleşmesiyle değil, de novo mutasyonlarla bağımsız olarak ortaya çıkar."},
                    {"key": "C", "text": "Uterusunda 10'dan fazla miyom olan hastalar sarkom profilaksisi için acilen opere edilmelidir.", "isCorrect": False, "explanation": "Yanlış. Miyom sayısının çokluğu malignite riskini artırmaz."},
                    {"key": "D", "text": "Hiyalin dejenerasyon gösteren tüm miyomlar malign sarkom prekürsörüdür.", "isCorrect": False, "explanation": "Yanlış. Hiyalin dejenerasyon selim asellüler kollajenleşmedir; prekürsör lezyon değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Leiomyomlardan malign transformasyon gerçekleşmez; moleküler incelemeler leiomyosarkomların de novo geliştiğini göstermektedir.",
                masked_term="de novo",
                hint="Öncül bir lezyon olmaksızın sıfırdan primer başlama"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Leiomyosarkom Patogenezi",
                items=[
                    {"text": "Leiomyosarkomlar benign leiomyomların malignleşmesi sonucu değil de novo gelişir.", "isLie": False, "explanation": "Doğru. Tümör bağımsız genetik olaylarla de novo başlar."},
                    {"text": "Bir kadında çok sayıda leiomyom bulunması sarkom gelişme ihtimalini artırmaz.", "isLie": False, "explanation": "Doğru. Multiple olması malignite riskini yükseltmez."},
                    {"text": "Leiomyosarkomlar genellikle postmenopozal dönemde tek kitle olarak saptanır.", "isLie": False, "explanation": "Doğru. Postmenopozal çağ ve soliter kitle karakteristiktir."},
                    {"text": "Leiomyom tespit edilen her hastada 5 yıl içinde %10 oranında leiomyosarkom dönüşümü beklenir.", "isLie": True, "explanation": "Tuzak! Leiomyomların leiomyosarkoma dönüşüm oranı %0'dır; malign transformasyon göstermezler."}
                ]
            ),
            make_recall(
                question="Multiple leiomyomu olan bir kadında lezyon sayısının fazla olması sarkom riskini artırır mı?",
                answer="Hayır; leiomyomlar sarkoma dönüşmez ve lezyon sayısının çokluğu malignite riskini kesinlikle artırmaz."
            )
        ]
    ))

    # Slide 13
    slides.append(make_slide(
        slide_num=13,
        title="Leiomyosarkom: Makroskobik Görünüm",
        subtitle="Yumuşak, etsi, kanamalı ve nekrotik kitle morfolojisi",
        clinical_focus="Cerrahi masada selim miyom ile malign sarkomun makroskobik ayrımı",
        narrative=(
            "Leiomyosarkomun makroskobik görünümü benign leiomyomdan taban tabana zıttır. Keskin sınırlı, sert ve homojen gri-beyaz leiomyomun aksine leiomyosarkom tipik bir malign mezenkimal tümör görüntüsü sergiler.\n\n"
            "- **Kıvam:** Tümör son derece yumuşak, gevrek ve balık eti (fleshy) kıvamındadır; çevre myometriuma invazyon gösterebilir ve sınırları genellikle düzensizdir.\n"
            "- **Kesit Yüzeyi:** Kesit yüzeyinde leiomyomdaki düzenli girdapsı (whorled) patern tamamen kaybolmuştur.\n"
            "- **Kanama ve Nekroz:** Tümörün hızlı büyümesine eşlik eden yetersiz anjiyogenez nedeniyle kitle içinde yaygın, harita benzeri nekroz odakları ve alacalı koyu kırmızı-kahverengi hemoraji alanları izlenir.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyosarkomlar tipik olarak yumuşak, etsi, yaygın kanamalı ve nekrotik kitlelerdir; girdapsı desen yerine düzensiz heterojen doku içerirler."
        ),
        bullets=[
            "Yumuşak, gevrek ve balık eti (fleshy) kıvamındadır",
            "Keskin sınırlı değildir; çevre myometriuma infiltrasyon gösterir",
            "Kesit yüzeyinde girdapsı desen bulunmaz",
            "Yaygın koagülatif nekroz ve geniş kanama odakları içerir"
        ],
        elements=[
            make_quiz(
                question="Histerektomi materyalinde myometriumda yerleşmiş bir kitlenin makroskobisinde yumuşak kıvam, yaygın hemoraji ve belirgin nekroz odakları izlenmesi öncelikle hangisini işaret eder?",
                options=[
                    {"key": "A", "text": "Basit intramural leiomyom", "isCorrect": False, "explanation": "Basit leiomyom sert-elastik, gri-beyaz ve girdapsıdır; yumuşak ve nekrotik değildir."},
                    {"key": "B", "text": "Subseröz parazitik miyom", "isCorrect": False, "explanation": "Parazitik miyom da selimdir ve sert gri-beyaz fibriler yapı gösterir."},
                    {"key": "C", "text": "Malign leiomyosarkom", "isCorrect": True, "explanation": "Doğru. Yumuşak kıvam, yaygın kanama ve nekroz leiomyosarkomun patognomonik makroskobik bulgularıdır."},
                    {"key": "D", "text": "Adenomyozis", "isCorrect": False, "explanation": "Adenomyoziste myometrium diffüz kalınlaşır ve küçük kahverengi trabeküller içerir; yumuşak etsi nekrotik kitle yapmaz."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Leiomyomların sert ve gri-beyaz yapısının aksine leiomyosarkomlar tipik olarak yumuşak, kanamalı ve nekrotik kitlelerdir.",
                masked_term="yumuşak, kanamalı ve nekrotik",
                hint="Malign dokunun kıvamı, vasküler hasarı ve doku yıkımı özellikleri"
            ),
            make_table(
                title="Leiomyom vs Leiomyosarkom Makroskopi Karşılaştırması",
                headers=["Özellik", "Leiomyom (Benign)", "Leiomyosarkom (Malign)"],
                rows=[
                    [
                        {"text": "Doku Kıvamı", "isMasked": False},
                        {"text": "Sert ve elastik", "isMasked": False},
                        {"text": "Yumuşak ve etsi", "isMasked": True, "hint": "Gevrek balık eti kıvamı"}
                    ],
                    [
                        {"text": "Kesit Yüzeyi", "isMasked": False},
                        {"text": "Girdapsı (whorled) desen", "isMasked": False},
                        {"text": "Düzensiz heterojen doku", "isMasked": True, "hint": "Girdap deseninin kaybolduğu şekilsiz yapı"}
                    ],
                    [
                        {"text": "Nekroz ve Kanama", "isMasked": False},
                        {"text": "Kural olarak yoktur", "isMasked": False},
                        {"text": "Yaygın nekroz ve hemoraji", "isMasked": True, "hint": "Tümör dokusunun iskemik çöküşü"}
                    ]
                ]
            ),
            make_recall(
                question="Cerrahi patoloğun bir myometrium kitlesini kestiğinde 'Bu bir leiomyom değil, leiomyosarkom olabilir' dedirten iki makroskobik bulgu nedir?",
                answer="Kitlenin sert değil yumuşak kıvamda olması ve kesit yüzünde yaygın kanama ile nekroz odaklarının bulunmasıdır."
            )
        ]
    ))

    # Slide 14
    slides.append(make_slide(
        slide_num=14,
        title="Leiomyosarkom: Histopatolojik Tanı Triadı",
        subtitle="Mitoz sayısı, sitolojik atipi ve koagülatif tümör nekrozu",
        clinical_focus="Düz kas tümörlerinde malignite ayrımının Stanford kriterleri",
        narrative=(
            "Düz kas neoplazmlarında benign-malign ayrımı histopatolojideki üç ana parametrenin (Stanford kriterleri) bir arada değerlendirilmesiyle yapılır. Tek başına tek bir kriter yerine bu triadın kombinasyonu esastır.\n\n"
            "- **1. Belirgin Sitolojik Atipi:** Hücrelerde boyut ve şekil değişkenliği (pleomorfizm), hiperkromatik dev multinükleer tümör hücreleri ve belirgin nükleoller.\n"
            "- **2. Yüksek Mitotik İndeks:** 10 büyük büyütme alanında (BÜA) 10 veya daha fazla mitotik figür saptanması (özellikle atipik, asimetrik üç kutuplu mitotik figürler).\n"
            "- **3. Koagülatif Tümör Hücresi Nekrozu:** İskemik infarkt nekrozundan farklı olarak, tümör hücrelerinin canlı alandan nekrotik alana granülasyon dokusu olmaksızın aniden geçiş gösterdiği gerçek koagülatif tümör nekrozu.\n\n"
            "> [!NOTE]\n"
            "> Bu üç kriterden en az ikisinin bulunması düz kas tümöründe kesin leiomyosarkom tanısı koydurur."
        ),
        bullets=[
            "1. Belirgin ve yaygın sitolojik nükleer atipi",
            "2. Yüksek mitotik aktivite (genellikle ≥10 mitoz / 10 BÜA)",
            "3. Koagülatif tümör hücresi nekrozu (CTN)",
            "Kriterlerin kombinasyonu kesin malignite tanısını belirler"
        ],
        elements=[
            make_quiz(
                question="Bir uterin düz kas neoplazmının mikroskobik incelemesinde malignite (leiomyosarkom) lehine olan en güvenilir tanısal histopatolojik triad aşağıdakilerden hangisidir?",
                options=[
                    {"key": "A", "text": "Hiyalin birikimi, distrofik kalsifikasyon ve ödem", "isCorrect": False, "explanation": "Bunlar selim leiomyomun sekonder dejenerasyon bulgularıdır; malignite göstermez."},
                    {"key": "B", "text": "Belirgin sitolojik atipi, yüksek mitotik aktivite ve koagülatif tümör nekrozu", "isCorrect": True, "explanation": "Doğru. Stanford kriterlerine göre atipi, mitotik indeks (≥10/10 BÜA) ve koagülatif tümör nekrozu leiomyosarkomun tanı triadıdır."},
                    {"key": "C", "text": "Kromozom 6 translokasyonu, girdapsı patern ve psödokapsül", "isCorrect": False, "explanation": "Bu özellikler klasik selim leiomyomun sitogenetik ve morfolojik nitelikleridir."},
                    {"key": "D", "text": "Endometrial gland proliferasyonu, stromada nötrofil ve desidualizasyon", "isCorrect": False, "explanation": "Endometrit veya gebelik değişiklikleridir; myometrium sarkom kriteri değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Leiomyosarkomun histolojik tanısında nükleer atipi ve yüksek mitotik aktiviteye eşlik eden koagülatif tümör hücresi nekrozu en kritik malignite göstergesidir.",
                masked_term="koagülatif tümör hücresi nekrozu",
                hint="Canlı atipik alanlar ile doku kaybı arasında ani sınır"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Leiomyosarkom Mikroskopisi",
                items=[
                    {"text": "Tümör dokusunda anormal, atipik mitotik figürler izlenir.", "isLie": False, "explanation": "Doğru. Tripolar veya asimetrik atipik mitozlar sarkomda sıktır."},
                    {"text": "Canlı hücrelerden nekroza ani geçiş gösteren koagülatif tümör nekrozu bulunur.", "isLie": False, "explanation": "Doğru. Koagülatif tümör nekrozu en güvenilir malignite kriteridir."},
                    {"text": "Leiomyosarkom tanısı için düz kas hücrelerinin tümörde hiç bulunmaması, saf kıkırdak içermesi şarttır.", "isLie": True, "explanation": "Tuzak! Leiomyosarkom düz kas hücrelerinden köken alan bir sarkomdur; düz kas diferansiasyonu gösteren atipik iğsi hücrelerden oluşur."},
                    {"text": "Hücrelerde belirgin pleomorfizm ve dev nükleer atipi saptanır.", "isLie": False, "explanation": "Doğru. Anaplastik dev hücreler ve sitolojik atipi karakteristiktir."}
                ]
            ),
            make_recall(
                question="Düz kas tümörlerinde iskemik dejeneratif nekroz ile koagülatif tümör nekrozu arasındaki temel fark nedir?",
                answer="İskemik nekrozda granülasyon dokusu ve hiyalinizasyon eşlik ederken; tümör nekrozunda canlı atipik tümör hücrelerinden nekroza ani geçiş vardır."
            )
        ]
    ))

    # Slide 15
    slides.append(make_slide(
        slide_num=15,
        title="Leiomyosarkom: Metastaz Yolları ve Klinik Seyir",
        subtitle="Hematojen yayılım, akciğer tutulumu ve agresif rekürrens",
        clinical_focus="Leiomyosarkomun sistemik onkolojik davranışı",
        narrative=(
            "Leiomyosarkomlar son derece vasküler tümörler olup lenfatik yoldan ziyade doğrudan **kan yoluyla (hematojen yolla)** yayılma eğilimindedirler. Bu özellikleri nedeniyle bölgesel lenf nodu tutulumu seyrektir.\n\n"
            "- **En Sık Metastaz Odağı:** Hematojen metastazların en sık yerleştiği organ **akciğerlerdir** (bunu karaciğer, kemik ve beyin izler). Akciğerde 'top güllesi' (cannonball) benzeri multiple metastatik nodüller oluşturabilir.\n"
            "- **Lokal Rekürrens:** Cerrahi olarak tamamen çıkarılsa bile pelvik nüks ve batın içi dissemine yayılım riski çok yüksektir.\n"
            "- **Prognoz:** 5 yıllık sağkalım oranları %40'ın altındadır. Hastanın prognozunu belirleyen en kritik parametre tanı anındaki cerrahi evre ve tümörün boyutudur (>5 cm kötü prognoz).\n\n"
            "> [!NOTE]\n"
            "> Uterin leiomyosarkom şüphesi olan bir hastada evreleme ve preoperatif değerlendirmede ilk istenecek görüntüleme toraks tomografisidir (akciğer metastazı taraması)."
        ),
        bullets=[
            "Lenfatik yayılımdan ziyade hematojen yolla metastaz yapar",
            "En sık metastaz bölgesi akciğer parankimidir",
            "Cerrahi sonrası lokal pelvik rekürrens oranı yüksektir",
            "5 yıllık sağkalım düşüktür; agresif klinik seyir gösterir"
        ],
        elements=[
            make_quiz(
                question="Uterin leiomyosarkomun sistemik yayılımında tercih ettiği birincil metastaz yolu ve en sık tuttuğu uzak organ hangisidir?",
                options=[
                    {"key": "A", "text": "Hematojen yol — Akciğer", "isCorrect": True, "explanation": "Doğru. Leiomyosarkomlar sarkomların genel kuralı olarak hematojen yolla yayılır ve en sık akciğere metastaz yaparlar."},
                    {"key": "B", "text": "Lenfatik yol — İnguinal lenf nodları", "isCorrect": False, "explanation": "İnguinal lenf tutulumu vulva kanserlerinde görülür; leiomyosarkomda lenfatik yayılım seyrektir."},
                    {"key": "C", "text": "Sölomik sıvı yolu — Fallop tüpü mukozası", "isCorrect": False, "explanation": "Over kanserleri peritoneal implantasyon yapar; sarkomlar kan yoluyla yayılır."},
                    {"key": "D", "text": "Retrograd akım — Servikal kanal", "isCorrect": False, "explanation": "Uzak metastaz mekanizması değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Malign mezenkimal bir tümör olan leiomyosarkom lenfatiklerden ziyade kan yoluyla yayılarak en sık akciğer organına metastaz yapar.",
                masked_term="akciğer",
                hint="Solunum sisteminin primer parankimal organı"
            ),
            make_chain(
                "Leiomyosarkom Sistemik Metastaz Zinciri",
                [
                    "1. Myometrial Vasküler İnvazyon: Atipik tümör hücreleri myometriumdaki geniş venöz sinüzoidleri yıkarak lümene penetre olur.",
                    "2. Sistemik Dolaşıma Katılım: İntravasküler tümör embolileri vena kava inferior yoluyla sağ kalbe ve pulmoner arter yatağına taşınır.",
                    "3. Pulmoner Parankim Kolonizasyonu: Akciğer kapillerlerinde tutunan malign hücreler ekstravaze olarak multiple hematojen metastaz nodülleri üretir."
                ]
            ),
            make_recall(
                question="Leiomyosarkom metastaz paterni karsinomlardan nasıl farklıdır?",
                answer="Karsinomlar öncelikle lenfatik yolla lenf nodlarına yayılırken; leiomyosarkom doğrudan hematojen yolla en sık akciğere yayılır."
            )
        ]
    ))

    # Slide 16
    slides.append(make_slide(
        slide_num=16,
        title="Leiomyom vs Leiomyosarkom: Karşılaştırmalı Ayırıcı Tanı",
        subtitle="Klinik, cerrahi ve mikroskobik parametrelerin sentezi",
        clinical_focus="İki antite arasındaki kritik onkolojik ayrımlar",
        narrative=(
            "Myometriumun bu iki zıt antitesi arasındaki ayırıcı tanı gerek hasta yönetimi gerekse cerrahi strateji açısından hayati önem taşır.\n\n"
            "- **Epidemiyolojik Karşılaştırma:** Leiomyom reprodüktif çağın son derece yaygın (%30-50) bir selim tümörüyken; leiomyosarkom postmenopozal dönemin nadir malignitesidir.\n"
            "- **Makroskopi:** Leiomyom sert-elastik, gri-beyaz, kesit yüzü girdapsı ve genellikle multiple iken; leiomyosarkom daima soliter, yumuşak, gevrek, yaygın kanamalı ve nekrotiktir.\n"
            "- **Biyolojik Davranış:** Leiomyom menopozda küçülür, sarkoma dönüşmez; leiomyosarkom de novo başlar, hızla büyür ve hematojen yolla akciğere metastaz yapar.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyom ile leiomyosarkom arasındaki ayrım tek bir özelliğe değil; yaş, lezyon sayısı, makroskopi ve histolojik kriterlerin tamamına dayanır."
        ),
        bullets=[
            "Leiomyom: Reprodüktif yaş, multiple, sert, girdapsı, benign",
            "Leiomyosarkom: Postmenopozal yaş, soliter, yumuşak, nekrotik, de novo malign",
            "Dönüşüm yoktur: Leiomyom sarkoma dönüşmez",
            "Metastaz: Leiomyomda yok; leiomyosarkomda hematojen (akciğer)"
        ],
        elements=[
            make_swipe(
                title="Leiomyom vs Leiomyosarkom Refleks Eşleme",
                left_category="Leiomyom (Benign)",
                right_category="Leiomyosarkom (Malign)",
                cards=[
                    {"text": "Reprodüktif dönemdeki kadınların %30-50'sinde izlenen en sık benign tümördür.", "category": "left", "explanation": "Leiomyom doğurganlık çağının en yaygın selim neoplazmıdır."},
                    {"text": "Postmenopozal dönemde tek (soliter) kitle olarak ortaya çıkar; yumuşak ve nekrotiktir.", "category": "right", "explanation": "Leiomyosarkom ileri yaşta soliter ve nekrotik malign kitle olarak belirir."},
                    {"text": "Kesit yüzeyinde karakteristik gri-beyaz girdapsı (whorled) desen izlenir.", "category": "left", "explanation": "Girdapsı desen selim düz kas fasiküllerinin tipik makroskobik bulgusudur."},
                    {"text": "Öncül bir miyom olmaksızın de novo gelişir ve kan yoluyla akciğere metastaz yapar.", "category": "right", "explanation": "Leiomyosarkom de novo köken alır ve hematojen yayılır."}
                ]
            ),
            make_quiz(
                question="Aşağıdaki özellik eşleştirmelerinden hangisi myometriumun düz kas tümörleri için DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Leiomyom: Her zaman soliter — Leiomyosarkom: Her zaman multiple", "isCorrect": False, "explanation": "Tam tersi; leiomyom sıklıkla multiple iken leiomyosarkom her zaman soliterdir."},
                    {"key": "B", "text": "Leiomyom: Yumuşak ve nekrotik — Leiomyosarkom: Sert ve girdapsı", "isCorrect": False, "explanation": "Tam tersi; leiomyom sert ve girdapsıdır; sarkom yumuşak ve nekrotiktir."},
                    {"key": "C", "text": "Leiomyom: Reprodüktif çağda sık — Leiomyosarkom: Postmenopozal çağda soliter", "isCorrect": True, "explanation": "Doğru. Leiomyom doğurganlık çağında sıktır; leiomyosarkom postmenopozal dönemde soliter lezyondur."},
                    {"key": "D", "text": "Leiomyom: De novo gelişmez, sarkomdan dönüşür — Leiomyosarkom: Benign prekürsördür", "isCorrect": False, "explanation": "Miyom benign bir primer lezyondur; sarkom ise de novo gelişen malign neoplazmdır."}
                ],
                correct_key="C"
            ),
            make_slider(
                left_title="Leiomyom Temel Kriterleri",
                right_title="Leiomyosarkom Temel Kriterleri",
                left_points=[
                    "Sert-elastik kıvam, keskin sınırlı psödokapsül",
                    "Gri-beyaz renkli, belirgin girdapsı (whorled) kesit yüzü",
                    "Mitoz sayısı çok düşüktür; koagülatif tümör nekrozu yoktur"
                ],
                right_points=[
                    "Yumuşak-etsi kıvam, infiltratif düzensiz sınırlar",
                    "Girdap deseni kaybolmuş, yaygın kanama ve nekroz alanları",
                    "Yüksek mitoz (≥10/10 BÜA), atipi ve koagülatif tümör nekrozu vardır"
                ]
            ),
            make_recall(
                question="Uterusta 12 adet miyom nodülü olan 38 yaşındaki bir kadının histerektomi materyalinde patoloğun leiomyosarkom bulma olasılığı bu nodül fazlalığına bağlı olarak artmış mıdır?",
                answer="Hayır; leiomyomlar sarkoma dönüşmez ve nodül sayısının çokluğu sarkom riskini artırmaz."
            )
        ]
    ))

    # Slide 17
    slides.append(make_slide(
        slide_num=17,
        title="Gestasyonel Trofoblastik Hastalıklar: Spektruma Giriş",
        subtitle="Mol hidatiform, invaziv mol ve koryokarsinom üçlüsü",
        clinical_focus="Trofoblastik hastalıkların agresiflik ve hormon salınım skalası",
        narrative=(
            "Gestasyonel trofoblastik hastalıklar (GTH), gebelikte plasentayı oluşturan trofoblastik hücrelerin (sito- ve sinsityotrofoblastlar) anormal proliferasyonundan kaynaklanan birbiriyle ilişkili lezyonlar grubudur. "
            "Bu hastalık grubu morfolojik ve klinik davranış açısından üç ana basamakta incelenir: **mol hidatiform**, **invaziv mol** ve **koryokarsinom**.\n\n"
            "- **Biyolojik Davranış Spektrumu:** Bu üçlü sıra, tamamen benign karakterdeki klasik mol hidatiformdan, lokal invaziv mole ve nihayetinde son derece agresif, metastatik bir karsinom olan koryokarsinoma doğru ilerleyen bir biyolojik spektrum oluşturur.\n"
            "- **Genetik ve Döllenme Kusuru:** Hastalıkların temelinde normal embriyogenezisi bozan paternal kromozom dengesizlikleri ve anormal fertilizasyon mekanizmaları yer alır.\n"
            "- **Tümör Biyobelirteci:** Tüm bu antitelerin ortak paydası trofoblastik dokunun salgıladığı **human koryonik gonadotropindir (hCG)**.\n\n"
            "> [!NOTE]\n"
            "> Trofoblastik hastalıklar, selim kistik molde başlayıp kemoterapiye çok duyarlı malign koryokarsinoma uzanan kesintisiz bir klinik spektrumdur."
        ),
        bullets=[
            "Trofoblastik hücrelerin anormal proliferasyonudur",
            "Üç ana basamak: Mol hidatiform, invaziv mol, koryokarsinom",
            "Benign molden agresif malign koryokarsinoma uzanan spektrumdur",
            "Temelinde anormal fertilizasyon ve paternal genom yatar"
        ],
        elements=[
            make_quiz(
                question="Gestasyonel trofoblastik hastalıklar spektrumunda benign formdan en agresif malign forma doğru sıralama aşağıdakilerden hangisinde doğru verilmiştir?",
                options=[
                    {"key": "A", "text": "Koryokarsinom → İnvaziv mol → Mol hidatiform", "isCorrect": False, "explanation": "Bu sıralama en malignden benigne doğrudur; spektrum yönü terstir."},
                    {"key": "B", "text": "Mol hidatiform → İnvaziv mol → Koryokarsinom", "isCorrect": True, "explanation": "Doğru. Spektrum benign mol hidatiform ile başlar, lokal invaziv mol ile devam eder ve malign koryokarsinom ile sonlanır."},
                    {"key": "C", "text": "İnvaziv mol → Mol hidatiform → Koryokarsinom", "isCorrect": False, "explanation": "İnvaziv mol komplet molün derin invazyonudur; başlangıç noktası mol hidatiformdur."},
                    {"key": "D", "text": "Endometrial polip → Leiomyom → Koryokarsinom", "isCorrect": False, "explanation": "Polip ve leiomyom trofoblastik hastalık değildir; trofoblastik spektrumda yer almazlar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Gebelikle ilgili trofoblastik hastalıklar, birbirleri ile ilişkili üç morfolojik bölüme ayrılmıştır: mol hidatiform, invaziv mol ve koryokarsinom.",
                masked_term="mol hidatiform, invaziv mol ve koryokarsinom",
                hint="Selim kistik olandan başlayıp uzak organa yayılan üçlü skala"
            ),
            make_chain(
                "Gestasyonel Trofoblastik Spektrum Basamakları",
                [
                    "1. Benign Trofoblastik Lezyon: Koryonik villusların kistik hidrofik genişlemesiyle karakterize mol hidatiform.",
                    "2. Lokal İnvaziv Form: Hidrofik villusların myometriumun derinliklerine penetre olduğu invaziv mol.",
                    "3. Malign Anaplastik Neoplazm: Villus yapısı içermeyen, anaplastik trofoblastlardan oluşan metastatik koryokarsinom."
                ]
            ),
            make_recall(
                question="Gestasyonel trofoblastik hastalıkları oluşturan üç temel klinik antite hangileridir?",
                answer="Mol hidatiform, invaziv mol ve koryokarsinomdur."
            )
        ]
    ))

    # Slide 18
    slides.append(make_slide(
        slide_num=18,
        title="Gestasyonel Trofoblastik Hastalıklar: hCG Biyobelirteci",
        subtitle="Tanı, takip ve nüksün izlenmesinde beta-hCG'nin rolü",
        clinical_focus="Trofoblastik tümörlerde hormon dinamikleri ve onkolojik izlem",
        narrative=(
            "Trofoblastik hücreler normal gebelikte olduğu gibi neoplastik çoğalmalarında da human koryonik gonadotropin (hCG) hormonu sentezler ve kana salgılarlar. "
            "Ancak trofoblastik hastalıklarda serum ve idrar hCG konsantrasyonları normal tekil bir gebelikte beklenen değerlerin kat kat üzerindedir.\n\n"
            "- **Spektrum Boyunca Progresyon:** Serum hCG seviyeleri hastalıktaki trofoblastik kitle ve proliferasyon hızıyla doğru orantılıdır; **mol hidatiformdan invaziv mole ve koryokarsinoma doğru gidildikçe dramatik şekilde artar**.\n"
            "- **Beta Alt Birimi:** Tanı ve takipte hormonun biyolojik olarak en spesifik kısmı olan **beta-hCG** alt birimi ölçülür.\n"
            "- **Tedavi Yanıtı ve Rekürrens:** Küretaj veya kemoterapi sonrasında hCG'nin normale dönmesi tam remisyonu; plato çizmesi veya yeniden yükselmesi ise persistan molar hastalığı, invaziv molü veya koryokarsinom gelişimini haber verir.\n\n"
            "> [!IMPORTANT]\n"
            "> hCG düzeyleri spektrum boyunca (mol → invaziv mol → koryokarsinom) artar; hormon takibi hem tanı hem de tedavinin etkinliğini belirlemede altın standarttır."
        ),
        bullets=[
            "Tüm trofoblastik hastalıklar yüksek düzeyde hCG salgılar",
            "hCG düzeyleri mol hidatiformdan koryokarsinoma doğru giderek artar",
            "Ölçümde en duyarlı ve spesifik belirteç beta alt birimidir (beta-hCG)",
            "Küretaj sonrası persistan yüksek hCG invazyon veya maligniteyi gösterir"
        ],
        elements=[
            make_quiz(
                question="Gestasyonel trofoblastik hastalıkların tanısında, tedavi etkinliğinin değerlendirilmesinde ve nükslerin saptanmasında kullanılan majör tümör biyobelirteci hangisidir?",
                options=[
                    {"key": "A", "text": "Alfa-fetoprotein (AFP)", "isCorrect": False, "explanation": "AFP yolk sak tümörleri ve hepatosellüler karsinomda yükselir; trofoblastik hastalık belirteci değildir."},
                    {"key": "B", "text": "Karsinoembriyonik antijen (CEA)", "isCorrect": False, "explanation": "CEA kolorektal ve gastrointestinal karsinomlarda kullanılır."},
                    {"key": "C", "text": "Human koryonik gonadotropin (hCG)", "isCorrect": True, "explanation": "Doğru. Sito- ve sinsityotrofoblastlar hCG (özellikle beta-hCG) salgılar; spektrum boyunca düzeyi artar ve tedavi takibinde kullanılır."},
                    {"key": "D", "text": "CA-125", "isCorrect": False, "explanation": "CA-125 over seröz epitelyal tümörlerinde ve endometrioziste yükselir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Trofoblastik lezyonların tümü kan ve idrarda normal gebeliktekine oranla çok daha yüksek düzeylerde human koryonik gonadotropin salgılarlar.",
                masked_term="human koryonik gonadotropin",
                hint="Plasental trofoblastların salgıladığı glikoprotein yapılı gebelik hormonu"
            ),
            make_branching(
                scenario="28 yaşında komplet mol tanısıyla uterin küretaj uygulanan bir hastada, işlem sonrası haftalık beta-hCG takiplerinde değerlerin önce düştüğü, ancak 4. haftadan itibaren tekrar logaritmik olarak yükselmeye başladığı saptanıyor. Bu klinik tablonun en olası nedeni nedir?",
                options=[
                    {"text": "İnvaziv mol gelişimi veya rezidü trofoblastik dokunun koryokarsinoma transforme olması.", "isCorrect": True, "feedback": "Doğru. Küretaj sonrası hCG'nin yeniden yükselmesi myometrial invazyonu (invaziv mol) veya malign koryokarsinomu gösterir; acil kemoterapi endikasyonudur."},
                    {"text": "Hastada fizyolojik olarak yeni bir ovulasyon siklusunun başlaması.", "isCorrect": False, "feedback": "Yanlış. Ovulasyon LH artışıyla olur, beta-hCG'yi yükseltmez; bu yükselme persistan trofoblastik neoplazidir."},
                    {"text": "Miyometriyumda basit bir benign leiomyomun hiyalin dejenerasyona uğraması.", "isCorrect": False, "feedback": "Yanlış. Leiomyomlar hCG salgılamaz; hCG tamamen trofoblastlara özgüdür."}
                ]
            ),
            make_recall(
                question="Mol hidatiformdan invaziv mole ve koryokarsinoma doğru ilerledikçe serum hCG konsantrasyonu nasıl bir eğilim gösterir?",
                answer="Tümörün proliferasyon ve invazyon derecesine paralel olarak dramatik şekilde giderek artar."
            )
        ]
    ))

    # Slide 19
    slides.append(make_slide(
        slide_num=19,
        title="Mol Hidatiform: Makroskopi ve Üzüm Salkımı Deseni",
        subtitle="Kistik hidrofik villuslar ve kaviter genişleme",
        clinical_focus="Molar gebeliğin patognomonik cerrahi ve ultrasonografi bulgusu",
        narrative=(
            "Mol hidatiform, plasental koryon villuslarının aşırı hidrofik ödemi ve kistik genişlemesiyle karakterize neoplastik bir süreçtir. "
            "Uterin kavite boşaltıldığında veya açıldığında patoloji masasında karşılaşılan görüntü tıp tarihinin en klasik patognomonik lezyonlarından biridir.\n\n"
            "- **Üzüm Salkımı Morfolojisi:** Genişlemiş, ince duvarlı, içleri berrak sıvı ile dolu, ışığı geçiren şeffaf kistik veziküller birbirine ince saplarla tutunur. Bu görünüm birebir bir **üzüm salkımına** benzer.\n"
            "- **Kavite Deformasyonu:** Uterus kavitesi normal gebelik haftasına göre belirgin olarak daha büyüktür ('gününe göre büyük uterus'). Kavite tümüyle bu kistik veziküller ve pıhtılaşmış kanla doludur.\n"
            "- **Fetal Yapı Varlığı/Yokluğu:** Klasik tam gelişmiş bir komplet molde bu veziküller arasında embriyoya veya fetüse ait hiçbir kemik, kıkırdak veya parça bulunmaz.\n\n"
            "> [!NOTE]\n"
            "> Ultrasonda molar gebelik fetal doku içermeyen kistik veziküller nedeniyle 'kar fırtınası' (snowstorm) manzarası verir; makroskopide ise üzüm salkımı görünümündedir."
        ),
        bullets=[
            "Koryonik villusların kistik hidrofik genişlemesidir",
            "Makroskopik olarak şeffaf 'üzüm salkımı' görünümündedir",
            "Uterus boyutları sıklıkla gestasyonel haftasına göre çok büyüktür",
            "Komplet formda fetal parça izlenmezken parsiyelde eşlik edebilir"
        ],
        elements=[
            make_quiz(
                question="Molar gebelik nedeniyle küretaj yapılan bir hastanın tahliye materyalinde ince duvarlı, şeffaf, içi berrak sıvı dolu kistik veziküllerin oluşturduğu patognomonik makroskobik görünüm hangisidir?",
                options=[
                    {"key": "A", "text": "Karnabahar görünümü", "isCorrect": False, "explanation": "Karnabahar görünümü ekzofitik serviks kanserlerinde ve kondilomlarda izlenir."},
                    {"key": "B", "text": "Top güllesi (cannonball) lezyonları", "isCorrect": False, "explanation": "Top güllesi sarkomların akciğer metastazlarındaki radyolojik lezyonlardır."},
                    {"key": "C", "text": "Üzüm salkımı görünümü", "isCorrect": True, "explanation": "Doğru. Mol hidatiformun kistik hidrofik vezikülleri klasik olarak 'üzüm salkımı' görünümündedir."},
                    {"key": "D", "text": "Çikolata kisti görünümü", "isCorrect": False, "explanation": "Çikolata kisti overdeki endometriozis odaklarının eski hemorajiye bağlı görüntüsüdür."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Tipik mol hidatiform, şişmiş bazen kistik genişleme gösteren ve makroskobik olarak üzüm salkımı görünümünde olan koryon villuslardan oluşur.",
                masked_term="üzüm salkımı",
                hint="Kistik hidrofik veziküllerin meyve kümesine benzetilen klasik makroskopi tanımı"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Mol Hidatiform Makroskopisi",
                items=[
                    {"text": "Koryon villusları hidrofik şişme göstererek kistik veziküllere dönüşmüştür.", "isLie": False, "explanation": "Doğru. Villöz ödem kistik genişlemeyi oluşturur."},
                    {"text": "Materyal makroskopik olarak üzüm salkımına benzer şeffaf veziküller içerir.", "isLie": False, "explanation": "Doğru. Üzüm salkımı patognomonik morfolojidir."},
                    {"text": "Komplet mol hidatiformda üzüm taneleri arasında daima canlı 20 haftalık bir fetüs gövdesi saptanır.", "isLie": True, "explanation": "Tuzak! Komplet mol hidatiform embriyogenezise izin vermez ve hiçbir zaman fetüse ait doku içermez; fetal parçalar ancak parsiyel molde görülebilir."},
                    {"text": "Uterus kavitesi gestasyonel yaşa göre beklenenden daha büyük olma eğilimindedir.", "isLie": False, "explanation": "Doğru. 'Gününe göre büyük uterus' tipik molar bulgudur."}
                ]
            ),
            make_recall(
                question="Mol hidatiformun patoloji laboratuvarında tanınmasını sağlayan en tipik makroskobik benzetme nedir?",
                answer="Kistik genişlemiş koryonik villusların oluşturduğu 'üzüm salkımı' görünümüdür."
            )
        ]
    ))

    # Slide 20 - Checkpoint 2
    slides.append(make_slide(
        slide_num=20,
        title="[TEKRAR SAYFASI - CHECKPOINT 2] Leiomyosarkom ve Trofoblastik Spektrum",
        subtitle="Bölüm 2 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Leiomyosarkom özellikleri, de novo gelişim ve trofoblastik hastalıklara giriş özeti",
        narrative=(
            "Bu tekrar sayfası, 11-19. adımlarda işlenen Leiomyosarkom Biyolojisi ve Gestasyonel Trofoblastik Hastalık Spektrumu kazanımlarını pekiştirmek için düzenlenmiştir. "
            "Leiomyosarkom, myometriumun düz kas hücrelerinden köken alan, postmenopozal dönemde tek (soliter) kitle olarak ortaya çıkan ve de novo gelişen malign bir tümördür.\n\n"
            "- **Miyomdan Dönüşmez:** Leiomyomlar kesinlikle sarkoma dönüşmez; multiple miyom varlığı sarkom riskini artırmaz.\n"
            "- **Makroskopi ve Histoloji:** Leiomyomun sert, gri-beyaz ve girdapsı yapısının aksine; sarkom yumuşak, kanamalı, nekrotiktir. Tanıda atipi, ≥10 mitoz/10 BÜA ve koagülatif tümör nekrozu esastır. En sık akciğere hematojen metastaz yapar.\n"
            "- **Trofoblastik Spektrum:** Mol hidatiform (benign), invaziv mol ve koryokarsinom (malign) üçlüsüdür. Spektrum boyunca hCG salınımı artar. Mol hidatiform makroskopide 'üzüm salkımı' manzarası verir.\n\n"
            "> [!NOTE]\n"
            "> Leiomyosarkomda lenfatik yayılım değil hematojen akciğer metastazı ön plandadır; trofoblastik tümörlerde ise beta-hCG tedavinin en duyarlı takip parametresidir."
        ),
        bullets=[
            "Leiomyosarkom postmenopozda, soliter ve de novo gelişir",
            "Leiomyom sarkoma dönüşmez; nodül sayısı riski etkilemez",
            "Sarkom: Yumuşak, kanamalı, nekrotik makroskopi; hematojen akciğer yayılımı",
            "Histoloji triadı: Belirgin atipi, yüksek mitoz, koagülatif tümör nekrozu",
            "Trofoblastik spektrum: Mol → İnvaziv mol → Koryokarsinom; hCG artar, üzüm salkımı makroskopisi"
        ],
        elements=[
            make_quiz(
                question="Leiomyosarkom ve gestasyonel trofoblastik hastalıklar ile ilgili aşağıdaki klinik ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "Leiomyosarkomlar benign miyomlardan malignleşerek gelişir ve en sık inguinal lenf nodlarını tutar.", "isCorrect": False, "explanation": "Yanlış. De novo gelişir ve lenfatik değil hematojen yolla akciğere yayılır."},
                    {"key": "B", "text": "Trofoblastik hastalıklarda hCG seviyeleri benign kistik molden malign koryokarsinoma doğru gidildikçe azalır.", "isCorrect": False, "explanation": "Yanlış. hCG düzeyleri spektrum boyunca progresif olarak belirgin şekilde artar."},
                    {"key": "C", "text": "Leiomyosarkom postmenopozal dönemde soliter, yumuşak, nekrotik kitle olarak de novo gelişir.", "isCorrect": True, "explanation": "Doğru. Leiomyosarkom postmenopozda tek kitle halinde, yumuşak-nekrotik yapıda ve de novo ortaya çıkar."},
                    {"key": "D", "text": "Mol hidatiform makroskopik olarak sert-elastik kıvamda ve kesit yüzü girdapsı desendedir.", "isCorrect": False, "explanation": "Yanlış. Girdapsı desen leiomyomun özelliğidir; mol hidatiform üzüm salkımı görünümündedir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Leiomyomların sert ve girdapsı yapısının aksine leiomyosarkomlar tipik olarak yumuşak, kanamalı ve nekrotik kitlelerdir.",
                masked_term="yumuşak, kanamalı ve nekrotik",
                hint="Malign tümörün kıvam, hemoraji ve iskemik doku kaybı bulguları"
            ),
            make_table(
                title="Bölüm 2 Temel Ayırıcı Tanı Özeti",
                headers=["Antite", "Tipik Klinik & Makroskopi", "Yayılım & Biyobelirteç"],
                rows=[
                    [
                        {"text": "Leiomyosarkom", "isMasked": False},
                        {"text": "Postmenopozal soliter kitle", "isMasked": True, "hint": "İleri yaşta tek odaklı olma durumu"},
                        {"text": "Hematojen yolla akciğer metastazı", "isMasked": False}
                    ],
                    [
                        {"text": "Mol Hidatiform", "isMasked": False},
                        {"text": "Kistik hidrofik villuslar", "isMasked": True, "hint": "Genişlemiş şeffaf veziküller"},
                        {"text": "Serum beta-hCG yüksekliği", "isMasked": False}
                    ],
                    [
                        {"text": "Koryokarsinom", "isMasked": False},
                        {"text": "Geniş nekroz ve hemoraji", "isMasked": False},
                        {"text": "Aşırı yüksek serum hCG düzeyi", "isMasked": True, "hint": "Spektrumun zirvesindeki hormon miktarı"}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 2 Kontrol Önermeleri",
                items=[
                    {"text": "Leiomyosarkom cerrahi kesit yüzünde girdapsı desen bulunmaz; tümör yumuşak ve nekrotiktir.", "isLie": False, "explanation": "Doğru. Düzensiz, etsi ve nekrotiktir."},
                    {"text": "Leiomyom sarkoma dönüşmez ve multiple olması malignite riskini artırmaz.", "isLie": False, "explanation": "Doğru. De novo gelişim kuralı geçerlidir."},
                    {"text": "Trofoblastik hastalıklarda hCG hormonu koryokarsinoma doğru gidildikçe kaybolur ve sıfıra iner.", "isLie": True, "explanation": "Tuzak! hCG düzeyleri koryokarsinoma doğru gidildikçe dramatik şekilde yükselir ve yüzbinlerce üniteye ulaşır."},
                    {"text": "Mol hidatiformun kistik vezikülleri makroskobide üzüm salkımı görüntüsü verir.", "isLie": False, "explanation": "Doğru. Patognomonik makroskopi üzüm salkımıdır."}
                ]
            ),
            make_recall(
                question="Checkpoint 2: Leiomyosarkomun benign miyomdan ayrımında histopatologların kullandığı üç majör mikroskobik kriter nedir?",
                answer="Belirgin nükleer atipi, yüksek mitotik aktivite (≥10 mitoz/10 BÜA) ve koagülatif tümör hücresi nekrozudur."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=2
    ))
    
    return slides
