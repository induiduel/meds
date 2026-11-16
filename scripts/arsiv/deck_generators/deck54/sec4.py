"""
Deck 54 - Section 4: İnvaziv Mol ve Koryokarsinom Patolojisi (Slayt 31-40)
Slayt 40: Checkpoint 4
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec4_slides():
    slides = []
    
    # Slide 31
    slides.append(make_slide(
        slide_num=31,
        title="İnvaziv Mol: Tanım ve Myometrial Penetrasyon",
        subtitle="Miyometrium derinliklerine penetre olan hidropik villuslar",
        clinical_focus="İnvaziv molün lokal doku destrüksiyonu ve kanama riski",
        narrative=(
            "İnvaziv mol (korioadenoma destruens), komplet mol hidatiformun koryonik villuslarının ve çevreleyen prolifere trofoblastlarının myometrium derinliklerine invazyon göstermesiyle tanımlanır. "
            "Komplet mol olgularının yaklaşık %10'unda küretaj sonrasında bu tablo gelişir.\n\n"
            "- **Histopatolojik Yapı:** İnvaziv molde en temel özellik, lezyonun içinde hidropik villus yapısının korunmuş olmasıdır. Bu hidropik villuslar myometrium kas demetlerini yıkarak uterus duvarının dış katmanlarına ve hatta pelvik venöz sinüslere kadar ilerler.\n"
            "- **Klinik Komplikasyonlar:** Miyometriumun derin invazyonu uterus duvarında incelmeye, rüptüre ve bazen hayatı tehdit eden masif intraabdominal kanamalara neden olabilir.\n"
            "- **Cerrahi Küretaj Yetersizliği:** Lezyon myometriumun derin katmanlarında gömülü olduğu için rutin endometrial küretaj ile tamamen çıkarılamaz.\n\n"
            "> [!IMPORTANT]\n"
            "> İnvaziv molde myometriumu istila eden hidropik koryon villusları mevcuttur; derin penetrasyon nedeniyle küretaj yetersiz kalır ve kemoterapi gerekir."
        ),
        bullets=[
            "Komplet mol olgularının yaklaşık %10'unda gelişir",
            "Miyometrium derinliklerine penetre olan hidropik villuslarla karakterizedir",
            "Uterin rüptür ve hayatı tehdit eden masif kanama riski taşır",
            "Endometrial küretaj ile tümüyle çıkarılamaz; derin yerleşimlidir"
        ],
        elements=[
            make_quiz(
                question="Komplet mol nedeniyle küretaj yapılan bir hastada 1 ay sonra devam eden vajinal kanama ve yüksek beta-hCG nedeniyle yapılan biyopside myometrium derinliklerine girmiş hidropik koryon villusları izlenmesi öncelikle hangi antiteyi işaret eder?",
                options=[
                    {"key": "A", "text": "Klasik selim leiomyom", "isCorrect": False, "explanation": "Leiomyom düz kas tümörüdür; koryon villusu veya trofoblast içermez."},
                    {"key": "B", "text": "İnvaziv mol (korioadenoma destruens)", "isCorrect": True, "explanation": "Doğru. Myometrium derinliklerine penetre olan hidropik villusların varlığı invaziv molün patognomonik tanımıdır."},
                    {"key": "C", "text": "Malign koryokarsinom", "isCorrect": False, "explanation": "Koryokarsinomda koryon villusları kesinlikle oluşmaz; saf anaplastik trofoblast kitleleri bulunur."},
                    {"key": "D", "text": "Plasental polip", "isCorrect": False, "explanation": "Plasental polip kaviter kalıntıdır; myometriuma invazyon ve derin destrüksiyon yapmaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnvaziv molde, uterus duvarının derinliklerine girerek olası yırtılmalara ve bazen yaşamı tehdit eden kanamalara neden olan hidropik villuslar izlenir.",
                masked_term="hidropik villuslar",
                hint="Miyometriuma penetre olan kistik plasental yapılar"
            ),
            make_chain(
                "İnvaziv Mol Patofizyolojik İlerleme Zinciri",
                [
                    "1. Myometrial Penetrasyon: Komplet molün trofoblastik hücreleri ve hidropik koryon villusları bazal membranı aşarak myometriuma girer.",
                    "2. Kas ve Damar Destrüksiyonu: Hidropik villuslar myometrium düz kas liflerini ve vasküler yatakları aşındırarak nekroz ve hematom oluşturur.",
                    "3. Uterin Rüptür Tehlikesi: Uterus serozasına kadar ulaşan derin invazyon serbest periton içi kanama ve şok tablosu tehdidi yaratır."
                ]
            ),
            make_recall(
                question="İnvaziv mol neden standart uterin küretaj işlemi ile tamamen temizlenemez?",
                answer="Tümör villusları endometrium kavitesinde değil, myometriumun derin kas katmanları içine gömülü olduğu için küretaja ulaşılamaz."
            )
        ]
    ))

    # Slide 32
    slides.append(make_slide(
        slide_num=32,
        title="İnvaziv Mol: Koryokarsinomdan Ayrımı ve Tedavi Yanıtı",
        subtitle="Metastaz yokluğu, koryon villus varlığı ve kemoterapi ile kür",
        clinical_focus="İnvaziv molün biyolojik sınırları ve onkolojik başarısı",
        narrative=(
            "İnvaziv molün klinik yönetiminde iki temel özellik öne çıkar: koryokarsinomdan biyolojik farkı ve kemoterapiye olan fevkalade duyarlılığı.\n\n"
            "- **Koryokarsinomdan Ayrım:** İnvaziv mol lokal olarak son derece agresif ve yıkıcı olmasına rağmen, koryokarsinomun gösterdiği yaygın, öldürücü uzak organ metastaz potansiyelini **göstermez**. Bazen embolizasyon yoluyla vajina veya akciğere taşınabilen villuslar görülse de bunlar gerçek otonom metastaz oluşturmaz ve spontan regrese olabilir.\n"
            "- **Villus Varlığı Farkı:** İnvaziv molde koryon villusları mevcuttur; koryokarsinomda ise koryon villusu kesinlikle oluşmaz.\n"
            "- **Kemoterapötik Kür:** Uterus duvarını perfore edebilecek kadar derin olmasına karşın, invaziv mol sistemik kemoterapiye (özellikle metotreksat ve aktinomisin-D) son derece duyarlıdır. Olguların tamamına yakınında (**%100 kür**) histerektomiye gerek kalmadan fertilite korunarak tam tedavi sağlanır.\n\n"
            "> [!IMPORTANT]\n"
            "> İnvaziv mol koryokarsinomun metastatik potansiyelini göstermez; hidropik villuslar içerir ve kemoterapi ile tam tedavi mümkündür."
        ),
        bullets=[
            "Koryokarsinomun agresif uzak metastaz potansiyelini göstermez",
            "Histolojisinde koryon villusları mevcuttur (koryokarsinomda yoktur)",
            "Vajina veya akciğere pasif villus embolisi olabilir ancak selimdir",
            "Kemoterapiye fevkalade duyarlıdır; %100'e yakın tam kür elde edilir"
        ],
        elements=[
            make_quiz(
                question="İnvaziv mol ile koryokarsinom karşılaştırıldığında, İNVAZİV MOL için tanısal ve prognostik açıdan DOĞRU olan ifade hangisidir?",
                options=[
                    {"key": "A", "text": "Histopatolojisinde koryon villusları kesinlikle izlenmez.", "isCorrect": False, "explanation": "Yanlış. İnvaziv molde hidropik villuslar mevcuttur; koryokarsinomda villus yoktur."},
                    {"key": "B", "text": "Koryokarsinom gibi agresif uzak organ metastazları yapmaz ve kemoterapi ile tam kür sağlanır.", "isCorrect": True, "explanation": "Doğru. İnvaziv mol metastaz yapmaz ve kemoterapiye (metotreksat) olağanüstü duyarlı olup tam tedavi edilir."},
                    {"key": "C", "text": "Kemoterapiye primer dirençlidir, tek tedavi seçeneği acil radikal histerektomidir.", "isCorrect": False, "explanation": "Yanlış. Kemoterapiye çok duyarlıdır; organ koruyucu medikal tedavi esastır."},
                    {"key": "D", "text": "Serum hCG düzeyleri daima sıfır saptanır.", "isCorrect": False, "explanation": "Yanlış. İnvaziv mol yüksek düzeyde hCG salgılar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnvaziv moller, lokal olarak daha invaziv olup koryokarsinomun agresif metastatik potansiyelini göstermeyen komplet mollerdir.",
                masked_term="metastatik potansiyelini",
                hint="Uzak organlara yayılma ve kolonize olma yeteneği"
            ),
            make_slider(
                left_title="İnvaziv Mol Davranışı",
                right_title="Koryokarsinom Davranışı",
                left_points=[
                    "Histolojide hidropik koryon villusları korunmuştur",
                    "Lokal myometrial invazyon yapar; uzak metastaz yapmaz",
                    "Kemoterapi ile %100 tam şifa sağlanır"
                ],
                right_points=[
                    "Koryon villusları kesinlikle oluşmamıştır (saf trofoblast)",
                    "Erken dönemde kan yoluyla akciğer ve beyne metastaz yapar",
                    "Aşırı agresiftir; paternal antijen varlığıyla kemoterapiye yanıt verir"
                ]
            ),
            make_recall(
                question="İnvaziv molün koryokarsinomdan mikroskobik olarak ayrılmasını sağlayan tek ve en kesin morfolojik yapı nedir?",
                answer="Koryonik villusların varlığıdır; invaziv molde hidropik villuslar varken, koryokarsinomda villus kesinlikle bulunmaz."
            )
        ]
    ))

    # Slide 33
    slides.append(make_slide(
        slide_num=33,
        title="Koryokarsinom: Tanım ve Epidemiyolojik Köken",
        subtitle="Anaplastik koryon epitelinin en agresif malign neoplazmı",
        clinical_focus="Koryokarsinomun sıklığı, anne yaşı ve coğrafi dağılımı",
        narrative=(
            "Koryokarsinom, plasental koryon epitelinden (anaplastik sito- ve sinsityotrofoblastlar) köken alan, olağanüstü hızlı büyüme ve erken vasküler invazyon kapasitesine sahip malign bir neoplazmdır.\n\n"
            "- **Coğrafi ve Etnik Sıklık:** Batı dünyasında yaklaşık 20.000-30.000 gebelikte 1 görülürken, **Afrika ve Asya'nın bazı bölgelerinde bu oran 2000 gebelikte 1'e kadar yükselir** (yaklaşık 10-15 kat daha sıktır).\n"
            "- **Anne Yaşı Faktörü:** Tıpkı mol hidatiformda olduğu gibi, 40 yaş üzerindeki gebeliklerde koryokarsinom gelişme riski dramatik şekilde artar.\n"
            "- **Köken Hücreler:** Olguların ezici çoğunluğu gebelik trofoblastlarından köken alırken (gestasyonel koryokarsinom), çok nadiren over veya testisteki totipotent germ hücrelerinden de kaynaklanabilir (non-gestasyonel koryokarsinom).\n\n"
            "> [!NOTE]\n"
            "> Koryokarsinom Afrika'da 2000 gebelikte 1 gibi yüksek bir oranda görülür ve 40 yaş üzeri gebeliklerde risk belirgin olarak artar."
        ),
        bullets=[
            "Koryon epitelinden köken alan en agresif malign trofoblastik tümördür",
            "Afrika ülkelerinde yaklaşık 2000 gebelikte 1 sıklıkta saptanır",
            "40 yaş üzeri anne yaşında görülme riski belirgin artış gösterir",
            "Çoğunlukla gebelik kaynaklıdır; nadiren gonadlardan (germ hücre) köken alır"
        ],
        elements=[
            make_quiz(
                question="Koryokarsinomun epidemiyolojisi, coğrafi dağılımı ve risk faktörleri ile ilgili aşağıdaki ifadelerden hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Kuzey Amerika'da 100 gebelikte 1 görülürken Afrika'da hiç saptanmaz.", "isCorrect": False, "explanation": "Tam tersi; Afrika'da 2000'de 1 gibi yüksek bir orandadır."},
                    {"key": "B", "text": "Görülme riski 20-25 yaş arasındaki kadınlarda en yüksek seviyededir.", "isCorrect": False, "explanation": "Risk 40 yaş üzerinde belirgin artar."},
                    {"key": "C", "text": "Afrika'da yaklaşık 2000'de 1 sıklıkta izlenir ve 40 yaş üzeri gebeliklerde risk belirgin artar.", "isCorrect": True, "explanation": "Doğru. Coğrafi olarak Afrika'da sıktır (2000'de 1) ve 40 yaş üzeri gebelikler majör risk faktörüdür."},
                    {"key": "D", "text": "Yalnızca erkeklerde testiste görülür; kadınlarda izlenmez.", "isCorrect": False, "explanation": "Koryokarsinom kadınlarda gebelik trofoblastlarından köken alan majör bir jinekolojik malignitedir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Koryokarsinom Afrika'da 2000'de 1 civarındadır ve 40 yaş üzeri gebeliklerde risk belirgin artar.",
                masked_term="2000'de 1",
                hint="Afrika kıtasındaki yaklaşık molar malignite görülme sıklığı oranı"
            ),
            make_recall(
                question="Koryokarsinom insidansının en yüksek olduğu coğrafi bölge ve kritik anne yaşı sınırı nedir?",
                answer="Afrika (2000 gebelikte 1) ve Güneydoğu Asya'dır; kritik yaş eşiği 40 yaş üzeridir."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Koryokarsinom Epidemiyolojisi",
                items=[
                    {"text": "Koryon epitelinden köken alan son derece agresif bir malign tümördür.", "isLie": False, "explanation": "Doğru. En habis trofoblastik tümördür."},
                    {"text": "Afrika'da görülme sıklığı Batı toplumlarına kıyasla belirgin şekilde daha fazladır.", "isLie": False, "explanation": "Doğru. Coğrafi yatkınlık 2000'de 1'e kadar çıkar."},
                    {"text": "40 yaş üzeri gebeliklerde koryokarsinom gelişme ihtimali katlanarak artar.", "isLie": False, "explanation": "Doğru. İleri anne yaşı belirgin bir risk faktörüdür."},
                    {"text": "Koryokarsinom sadece menopoz sonrası dönemde görülür, gebelikle hiçbir ilişkisi yoktur.", "isLie": True, "explanation": "Tuzak! Koryokarsinom olgularının tamamına yakını gebelik kökenlidir (gestasyonel trofoblastik hastalık)."}
                ]
            )
        ]
    ))

    # Slide 34
    slides.append(make_slide(
        slide_num=34,
        title="Koryokarsinom: Öncül Gebelik Olayları Dağılımı",
        subtitle="%50 komplet mol, %25 abortus ve %22 normal term gebelik",
        clinical_focus="Koryokarsinomun öncesindeki obstetrik öykü dağılımı",
        narrative=(
            "Koryokarsinom tek bir gebelik tablosunun ardından değil, kadın hayatındaki her türlü obstetrik sürecin sonrasında ortaya çıkabilir. Hastaların geriye dönük obstetrik öyküleri incelendiğinde son derece karakteristik bir dağılım görülür:\n\n"
            "- **1. Komplet Mol Hidatiform (%50):** Olguların tam yarısı önceden geçirilmiş bir komplet mol hidatiformu izler. Mol ne kadar komplet ise risk o kadar belirgindir.\n"
            "- **2. Spontan Abortus / Düşük (%25):** Olguların dörtte biri bir düşük veya küretaj öyküsünden sonra gelişir.\n"
            "- **3. Normal Term Gebelik (%22):** Olguların yaklaşık beşte biri tamamen sağlıklı, miadında doğum yapmış bir kadında doğumdan aylar veya yıllar sonra ortaya çıkar.\n"
            "- **4. Ektopik Gebelik (%3):** Kalan küçük bir grup dış gebelik sonrasında saptanır.\n\n"
            "> [!IMPORTANT]\n"
            "> Koryokarsinom olgularının %50'si komplet mol hidatiformu, %25'i düşüğü, geriye kalanların çoğu ise normal seyreden bir term gebeliği izler."
        ),
        bullets=[
            "Olguların %50'sinde öncül lezyon komplet mol hidatiformdur",
            "Olguların %25'i spontan abortusu (düşüğü) izler",
            "Olguların yaklaşık %22'si normal miadında term gebelik sonrası gelişir",
            "Kalan %2-3'lük dilim ise ektopik gebelikten kaynaklanır"
        ],
        elements=[
            make_quiz(
                question="Gestasyonel koryokarsinom tanısı alan kadınların obstetrik öyküleri incelendiğinde, bu malignitenin en sık hangi gebelik tablosunun ardından geliştiği görülür?",
                options=[
                    {"key": "A", "text": "Parsiyel mol hidatiform (%80)", "isCorrect": False, "explanation": "Parsiyel molden koryokarsinom gelişimi son derece nadirdir (<%0.1)."},
                    {"key": "B", "text": "Komplet mol hidatiform (%50)", "isCorrect": True, "explanation": "Doğru. Koryokarsinom olgularının %50'si komplet mol hidatiformu izler."},
                    {"key": "C", "text": "Tubal ektopik gebelik (%70)", "isCorrect": False, "explanation": "Ektopik gebelik sonrası oran sadece %2-3 civarındadır."},
                    {"key": "D", "text": "Çoğul ikiz gebelik (%90)", "isCorrect": False, "explanation": "Çoğul gebelik koryokarsinomun majör öncülü değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Koryokarsinom vakalarının yüzde 50 kadarında lezyon komplet mol hidatiformu izlerken, yüzde 25 kadarı ise düşükten sonra gelişir.",
                masked_term="yüzde 50",
                hint="Tümörün komplet molar gebelikten kaynaklanma oranı"
            ),
            make_table(
                title="Koryokarsinom Öncül Gebelik Olayları",
                headers=["Öncül Obstetrik Durum", "Görülme Oranı (%)", "Klinik Önem"],
                rows=[
                    [
                        {"text": "Komplet Mol Hidatiform", "isMasked": False},
                        {"text": "Olguların %50'si", "isMasked": True, "hint": "Vakaların tam yarısı"},
                        {"text": "En sık görülen öncül obstetrik olaydır", "isMasked": False}
                    ],
                    [
                        {"text": "Spontan Abortus (Düşük)", "isMasked": False},
                        {"text": "Olguların %25'i", "isMasked": True, "hint": "Vakaların dörtte biri"},
                        {"text": "Düşük sonrası anormal kanamada akla gelmelidir", "isMasked": False}
                    ],
                    [
                        {"text": "Normal Term Gebelik", "isMasked": False},
                        {"text": "Olguların yaklaşık %22'si", "isMasked": False},
                        {"text": "Doğumdan aylar sonra metastazla ortaya çıkabilir", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Normal doğum yapmış bir kadında doğumdan 6 ay sonra akciğerde multiple kanamalı nodüller ve vajinal kanama saptanması hangi jinekolojik tümörü düşündürmelidir?",
                answer="Term gebelik sonrası gelişen koryokarsinomu düşündürmelidir; serum beta-hCG ölçülmelidir."
            )
        ]
    ))

    # Slide 35
    slides.append(make_slide(
        slide_num=35,
        title="Koryokarsinom: Klinik Belirtiler ve Uterus Hacmi",
        subtitle="Kahverengi vajinal akıntı, yüksek hCG ve normal uterus boyutu",
        clinical_focus="Molar gebelikten koryokarsinoma klinik semptom değişimi",
        narrative=(
            "Koryokarsinomun klinik prezentasyonu mol hidatiformdan belirgin farklılıklar gösterir. Tanıdaki en tipik klinik ipucu anormal uterin kanamadır.\n\n"
            "- **Vajinal Akıntı ve Kanama:** Hastalar sıklıkla önceden geçirilmiş bir gebelik, düşük veya molar tahliyenin ardından durmayan, aralıklı veya sürekli, kötü kokulu, **kanlı kahverengimsi akıntı** ile başvururlar.\n"
            "- **Uterus Hacmi Sürprizi:** Mol hidatiformda uterus kistik veziküllerle dolu olduğu için gününe göre çok büyüktür. Oysa koryokarsinomda **uterusta moldekinin aksine belirgin bir büyüme izlenmez**; uterus normal boyutlarda veya sadece hafif genişlemiş olabilir.\n"
            "- **Aşırı hCG Yüksekliği:** Serum ve idrar hCG (özellikle beta alt birim) düzeyleri olağanüstü yüksek seviyelere tırmanır.\n"
            "- **Primer Odak Regresyonu:** Bazen uterustaki primer tümör tamamen iskemik nekroza uğrayıp yok olabilir ve hasta sadece uzak metastazların (öksürük, hemoptizi, konvülsiyon) bulgularıyla hekime başvurabilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Koryokarsinom kanlı kahverengimsi akıntı ve aşırı yüksek hCG ile seyreder; mol hidatiformun aksine uterusta belirgin büyüme görülmez."
        ),
        bullets=[
            "En sık şikayet inatçı, kanlı kahverengimsi vajinal akıntıdır",
            "Serum ve idrar beta-hCG düzeyleri aşırı derecede yüksektir",
            "Moldekinin aksine uterusta belirgin hacim artışı veya büyüme izlenmez",
            "Primer uterin kitle nekrozla kaybolabilir; metastazla prezente olabilir"
        ],
        elements=[
            make_quiz(
                question="Koryokarsinomlu bir hastanın klinik muayenesinde uterus hacmi ile ilgili saptanan ve onu klasik mol hidatiformdan ayıran temel özellik nedir?",
                options=[
                    {"key": "A", "text": "Uterusun devasa kistik bir kitle halinde umbilikusu aşması", "isCorrect": False, "explanation": "Bu durum mol hidatiformun özelliğidir."},
                    {"key": "B", "text": "Mol hidatiformun aksine uterusta belirgin bir büyümenin olmaması", "isCorrect": True, "explanation": "Doğru. Koryokarsinomda kistik vezikül kitlesi olmadığı için uterusta moldekinin aksine belirgin büyüme izlenmez; normal boyutlarda kalabilir."},
                    {"key": "C", "text": "Uterus kavitesinin tamamen taşlaşmış kemik dokusuyla dolması", "isCorrect": False, "explanation": "Kemik dokusu metaplazi veya fetal retansiyonda nadiren görülür; koryokarsinomla ilgisizdir."},
                    {"key": "D", "text": "Uterus serviksinin tamamen oblitere olarak yok olması", "isCorrect": False, "explanation": "Servikal atrezi konjenitaldir; koryokarsinom uterusta kanamalı kitle yapar."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Olguların çoğu kanlı kahverengimsi akıntı, kanda aşırı yükselen hCG ve moldekinin aksine uterusta belirgin büyümenin olmaması ile ortaya konur.",
                masked_term="belirgin büyümenin olmaması",
                hint="Molar gebelikteki devasa kavite genişlemesinin karsinomda bulunmama durumu"
            ),
            make_recall(
                question="Koryokarsinomda primer uterin lezyonun patolojide saptanamaması nasıl açıklanır?",
                answer="Tümörün aşırı hızlı büyüyerek kendi damarlanmasını aşması sonucu primer odağın yaygın nekrozla tamamen yok olmasıyla açıklanır."
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Koryokarsinom Kliniği",
                items=[
                    {"text": "Hastalar sıklıkla kanlı kahverengimsi vajinal akıntı şikayetiyle başvururlar.", "isLie": False, "explanation": "Doğru. Tipik prezentasyon vajinal akıntı ve kanamadır."},
                    {"text": "Serum beta-hCG seviyeleri mol hidatiformdakinden çok daha yüksek değerlere ulaşır.", "isLie": False, "explanation": "Doğru. Spektrum boyunca hCG artar."},
                    {"text": "Koryokarsinomda uterus mutlaka 30 haftalık ikiz gebelik boyutuna kadar büyür.", "isLie": True, "explanation": "Tuzak! Mol hidatiformun aksine koryokarsinomda uterusta belirgin bir büyüme izlenmez."},
                    {"text": "Bazen primer uterin tümör tamamen nekroze olup gerilerken sadece akciğer metastazı kalabilir.", "isLie": False, "explanation": "Doğru. Spontan primer regresyon koryokarsinomda iyi bilinen bir fenomendir."}
                ]
            )
        ]
    ))

    # Slide 36
    slides.append(make_slide(
        slide_num=36,
        title="Koryokarsinom: Makroskopi ve Mikroskopi",
        subtitle="Kanamalı-nekrotik kitle ve koryon villuslarının kesin yokluğu",
        clinical_focus="Koryokarsinomun patognomonik histopatolojik kriterleri",
        narrative=(
            "Koryokarsinomun morfolojik incelemesi patoloji laboratuvarında en çarpıcı malignite tablolarından birini sunar.\n\n"
            "- **Makroskopi:** Uterus lümeninde veya myometrium içinde yerleşmiş, **oldukça yumuşak, koyu kırmızı-kahverengi, yaygın kanamalı ve nekrotik kitleler** halindedir. Çoğu zaman nekroz ve hemoraji o kadar yaygındır ki tümör dokusunun mikroskobik olarak tanınması güçleşir.\n"
            "- **Mikroskopi (Koryon Villus Yokluğu):** Mol hidatiform ve invaziv molün aksine, koryokarsinomda **koryon villusları KESİNLİKLE oluşmamıştır**. Villus çatısı tamamen kaybolmuştur.\n"
            "- **Hücresel Kompozisyon:** Tümör, birbirini saran anaplastik sitotrofoblast (mononükleer berrak hücreler) ve sinsityotrofoblast (pleomorfik multinükleer dev hücreler) tabakalarından oluşan saf epitelyal bir neoplazmdır.\n"
            "- **Vasküler Yıkım:** Tümör hücreleri kan damarlarını doğrudan invaze eder; ancak tümörün kendine ait bir stroması ve damar yapısı yoktur; beslenmesini doku kanamalarından sağlar.\n\n"
            "> [!IMPORTANT]\n"
            "> Koryokarsinomun en kritik histopatolojik kuralı: Koryon villusları kesinlikle izlenmez; kitle saf anaplastik sito/sinsityotrofoblastlardan ve yaygın nekrozdan oluşur."
        ),
        bullets=[
            "Uterus içinde oldukça yumuşak, kanamalı ve nekrotik kitledir",
            "Koryon villusları KESİNLİKLE oluşmamıştır (en kritik patoloji kuralı)",
            "Saf anaplastik sito- ve sinsityotrofoblast kitlelerinden oluşur",
            "Tümörün kendi damarları yoktur; myometrium damarlarını invaze ederek beslenir"
        ],
        elements=[
            make_quiz(
                question="Bir trofoblastik tümörün histopatolojik incelemesinde koryokarsinom tanısını kesinleştiren ve onu mol hidatiform ile invaziv molden ayıran temel negatif mikroskobik bulgu nedir?",
                options=[
                    {"key": "A", "text": "Düz kas fasiküllerinin ve puro biçimli nükleusların bulunmaması", "isCorrect": False, "explanation": "Düz kas miyomda bulunur; trofoblastik lezyonların hiçbirinde primer tümör dokusu değildir."},
                    {"key": "B", "text": "Koryonik villusların kesinlikle oluşmamış olması", "isCorrect": True, "explanation": "Doğru. Mol hidatiform ve invaziv molde hidropik villuslar varken; koryokarsinomda villus oluşumu kesinlikle yoktur."},
                    {"key": "C", "text": "Sinsityotrofoblast hücrelerinin hCG üretmemesi", "isCorrect": False, "explanation": "Yanlış. Sinsityotrofoblastlar devasa miktarda hCG üretir."},
                    {"key": "D", "text": "Tümör kesitinde psammom cisimciklerinin saptanması", "isCorrect": False, "explanation": "Psammom cisimciği over seröz tümörlerinde ve tiroid kanserinde görülür."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Mol hidatiform ve invaziv molün aksine koryokarsinomda koryon villusları oluşmamıştır; lezyon anaplastik trofoblastlardan meydana gelir.",
                masked_term="koryon villusları oluşmamıştır",
                hint="Plasental parankimin temel fonksiyonel çatısının kesin yokluğu"
            ),
            make_table(
                title="Trofoblastik Lezyonlarda Villus Varlığı Karşılaştırması",
                headers=["Antite", "Koryon Villus Durumu", "Trofoblast Proliferasyon Patern"],
                rows=[
                    [
                        {"text": "Komplet Mol", "isMasked": False},
                        {"text": "Diffüz hidropik villuslar", "isMasked": True, "hint": "Tüm koryon yapılarında kistik ödem"},
                        {"text": "Villus çevresinde diffüz trofoblast hiperplazisi", "isMasked": False}
                    ],
                    [
                        {"text": "İnvaziv Mol", "isMasked": False},
                        {"text": "Myometriuma penetre villuslar", "isMasked": True, "hint": "Derin kas tabakasını istila eden kistik yapılar"},
                        {"text": "Myometrium içinde villuslarla birlikte invazyon", "isMasked": False}
                    ],
                    [
                        {"text": "Koryokarsinom", "isMasked": False},
                        {"text": "Kesinlikle villus yoktur", "isMasked": True, "hint": "Koryon çatısının tamamen bulunmaması"},
                        {"text": "Saf anaplastik sito/sinsityotrofoblast tabakaları", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Patoloji preparatında yaygın kanamalı trofoblastik bir tümör incelenirken tek bir koryon villusunun görülmesi koryokarsinom tanısını neden ekarte ettirir?",
                answer="Çünkü koryokarsinomda koryon villusları oluşmaz; villus görülmesi lezyonun mol hidatiform veya invaziv mol olduğunu gösterir."
            )
        ]
    ))

    # Slide 37
    slides.append(make_slide(
        slide_num=37,
        title="Koryokarsinom: Erken Vasküler İnvazyon ve Akciğer Metastazı",
        subtitle="%50 akciğer, vajina, beyin, karaciğer ve böbrek hematojen yayılımı",
        clinical_focus="Koryokarsinomun sistemik metastatik paterni ve lenfatik nadirliği",
        narrative=(
            "Koryokarsinom, insan vücudundaki tüm malign tümörler arasında kan damarlarını en erken ve en agresif şekilde istila eden neoplazmdır. "
            "Tümör hücreleri doğal olarak plasental trofoblastların maternal spiral damarları eritme yeteneğini (anjiyo-destrüksiyon) kontrolsüzce sergiler.\n\n"
            "- **Hematojen Yayılım:** Tümör çok erken dönemde myometrium venlerine ve uterin sinüzoidlere penetre olur. **Lenfatik invazyon son derece seyrektir**; yayılım neredeyse tamamen kan dolaşımı aracılığıyla gerçekleşir.\n"
            "- **Metastaz Organları Dağılımı:**\n"
            "  * **Akciğerler (%50):** Açık ara en sık metastaz bölgesidir. Multiple kanamalı nodüller oluşturarak hemoptizi, nefes darlığı ve göğüs ağrısı yapar.\n"
            "  * **Vajina (%30-40):** Subepitelyal pleksuslara retrograd venöz yayılımla vajen ön duvarında mavi-kırmızı kanamalı nodüller belirir.\n"
            "  * **Beyin, Karaciğer ve Böbrek:** İleri evrede sistemik arteriyel yayılımla intrakraniyal kanamalara ve hepatik yetmezliğe yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> Koryokarsinom kan yoluyla çok erken yayılır; en sık (%50) akciğerlere, ardından vajina, beyin ve karaciğere metastaz yapar; lenfatik tutulum seyrektir."
        ),
        bullets=[
            "Damarları çok erken istila eder; yayılım neredeyse tamamen hematojendir",
            "Lenfatik metastaz kural olarak son derece seyrektir",
            "En sık metastaz bölgesi akciğerdir (olguların %50'si)",
            "Vajinada mavi-kırmızı kanamalı metastatik nodüller tipiktir"
        ],
        elements=[
            make_quiz(
                question="Koryokarsinomun sistemik yayılımında tercih ettiği primer vasküler yol ve tanıda en sık saptanan uzak metastaz lokalizasyonu hangisidir?",
                options=[
                    {"key": "A", "text": "Lenfatik yol — Paraaortik lenf nodları", "isCorrect": False, "explanation": "Koryokarsinomda lenfatik yayılım seyrektir; kan yolu esastır."},
                    {"key": "B", "text": "Hematojen yol — Akciğer (%50)", "isCorrect": True, "explanation": "Doğru. Koryokarsinom damarları erken invaze ederek kan yoluyla yayılır ve olguların %50'sinde akciğere metastaz yapar."},
                    {"key": "C", "text": "Sölomik yayılım — Over korteksi", "isCorrect": False, "explanation": "Over karsinomları peritoneal yayılır; koryokarsinom hematojen yayılır."},
                    {"key": "D", "text": "Transservikal dökülme — Vulva derisi", "isCorrect": False, "explanation": "Yüzeyel dökülme metastaz mekanizması değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Tanı konulduğunda koryokarsinom olgularında sıklıkla akciğer organında kan yoluyla gelişen yaygın metastazlar saptanır.",
                masked_term="akciğer",
                hint="Olguların yüzde ellisinde tutulan solunum organı"
            ),
            make_table(
                title="Koryokarsinom Metastaz Lokalizasyonları ve Klinik Tablo",
                headers=["Metastaz Bölgesi", "Görülme Sıklığı", "Karakteristik Klinik Belirti"],
                rows=[
                    [
                        {"text": "Akciğer Parankimi", "isMasked": False},
                        {"text": "Olguların yaklaşık %50'si", "isMasked": True, "hint": "Vakaların yarısında görülen oran"},
                        {"text": "Öksürük, nefes darlığı ve hemoptizi (kan tükürme)", "isMasked": False}
                    ],
                    [
                        {"text": "Vajina (Submukoza)", "isMasked": False},
                        {"text": "Olguların %30-40'ı", "isMasked": True, "hint": "Üçte bir ile yüzde kırk arası"},
                        {"text": "Mavi-kırmızı renkli, kanamalı subepitelyal nodüller", "isMasked": False}
                    ],
                    [
                        {"text": "Beyin ve Karaciğer", "isMasked": False},
                        {"text": "İleri evre olgular", "isMasked": False},
                        {"text": "İntrakraniyal kanama, konvülsiyon ve karaciğer yetmezliği", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Koryokarsinomlu bir hastada jinekolojik spekulum muayenesinde vajina ön duvarında saptanabilen metastatik lezyonun makroskobik görünümü nasıldır?",
                answer="Mavi-kırmızı veya koyu bordo renkli, oldukça yumuşak ve kolay kanayan kitle nodülleri şeklindedir."
            )
        ]
    ))

    # Slide 38
    slides.append(make_slide(
        slide_num=38,
        title="Koryokarsinom: Kemoterapiye Yanıt ve Kür Başarısı",
        subtitle="Agresif malignitede %100'e yakın kemoterapötik şifa",
        clinical_focus="Onkolojide metastatik koryokarsinomun kemoterapi başarısı",
        narrative=(
            "Koryokarsinom tıp tarihinde kemoterapi ile metastatik evrede dahi tamamen kür edilebilen ilk solid epitelyal tümördür. "
            "1950'li yıllardan önce tanı konduğunda %100 ölümcül olan bu tümör, modern kombinasyon kemoterapilerinin (metotreksat, aktinomisin-D, etoposid) devreye girmesiyle onkolojinin en büyük başarı öyküsüne dönüşmüştür.\n\n"
            "- **Kür Oranı:** Bugün yaygın akciğer, vajina veya karaciğer metastazı bulunan ileri evre gestasyonel koryokarsinom hastalarında dahi **kemoterapi ile %100'e yakın tam tedavi (şifa)** sağlanabilmektedir.\n"
            "- **Fertilite Korunumu:** Histerektomiye gerek kalmaksızın uygulanan sistemik kemoterapi sayesinde kadınların uterusları ve doğurganlıkları korunabilmektedir.\n"
            "- **Tedavi Monitörizasyonu:** Tedavinin başarısı ve sonlandırılması haftalık serum beta-hCG seviyelerinin sıfıra inmesi ve en az 3 ardışık hafta negatif kalması ile belgelenir.\n\n"
            "> [!IMPORTANT]\n"
            "> Geçmişte tamamen ölümcül olan koryokarsinomda günümüzde modern kemoterapi protokolleri ile metastatik evrede dahi %100 oranında tam kür sağlanabilmektedir."
        ),
        bullets=[
            "Metastatik evrede kemoterapiyle tam kür sağlanan ilk solid kanserdir",
            "Geçmişte ölümcülken bugün kemoterapiyle %100'e yakın tam kür elde edilir",
            "Metotreksat, aktinomisin-D ve etoposid temel ajanlardır",
            "Uterus korunarak hastaların fertilite fonksiyonları sürdürülebilir"
        ],
        elements=[
            make_quiz(
                question="Tıp tarihinde metastatik evrede dahi sistemik kemoterapiye (metotreksat bazlı rejimler) olağanüstü duyarlılık göstererek %100'e yakın tam kür elde edilen majör jinekolojik malignite hangisidir?",
                options=[
                    {"key": "A", "text": "Overin seröz karsinomu", "isCorrect": False, "explanation": "İleri evre over seröz kanserinde rekürrens sıktır; %100 kür sağlanamaz."},
                    {"key": "B", "text": "Uterin leiomyosarkom", "isCorrect": False, "explanation": "Leiomyosarkom kemoterapiye dirençlidir; 5 yıllık sağkalım %40 altındadır."},
                    {"key": "C", "text": "Gestasyonel koryokarsinom", "isCorrect": True, "explanation": "Doğru. Gestasyonel koryokarsinom kemoterapiye fevkalade duyarlıdır ve metastatik olgularda bile %100 kür sağlanır."},
                    {"key": "D", "text": "Endometriumun berrak hücreli karsinomu", "isCorrect": False, "explanation": "Tip 2 endometrium kanseridir; kemoterapiye dirençli ve agresiftir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Geçmişte tamamen ölümcül olan bu tümörde günümüzde kemoterapi ile yüzde 100 oranında tam tedavi sağlanabilmektedir.",
                masked_term="yüzde 100",
                hint="Modern medikal onkolojide ulaşılan eksiksiz tam kür oranı"
            ),
            make_branching(
                scenario="26 yaşında kadın hasta, komplet mol küretajından 3 ay sonra nefes darlığı ve hemoptizi şikayetiyle başvuruyor. Akciğer grafisinde multiple kanamalı nodüller ve serum beta-hCG: 450.000 mIU/mL saptanarak metastatik gestasyonel koryokarsinom tanısı konuyor. Hastaya ve ailesine verilecek en doğru onkolojik bilgilendirme nedir?",
                options=[
                    {"text": "Tümör kemoterapiye olağanüstü duyarlıdır; metastazlara rağmen sistemik kemoterapi ile %100'e yakın tam şifa şansı mevcuttur.", "isCorrect": True, "feedback": "Mükemmel. Gestasyonel koryokarsinom akciğer metastazı olsa bile kemoterapiye fevkalade yanıt verir ve kür oranı %100'e yakındır."},
                    {"text": "Tümör kemoterapiye dirençlidir, hastanın beklenen yaşam süresi 3 aydan kısadır.", "isCorrect": False, "feedback": "Tamamen yanlış. Koryokarsinom kemoterapinin en başarılı olduğu solid tümördür."},
                    {"text": "Tek tedavi seçeneği acilen bilateral akciğer rezeksiyonu ve radikal histerektomidir.", "isCorrect": False, "feedback": "Hatalı. Primer tedavi cerrahi değil sistemik kombinasyon kemoterapisidir."}
                ]
            ),
            make_recall(
                question="Metastatik koryokarsinomlu bir hastada kemoterapinin başarılı olduğunu ve tedavinin sonlandırılabileceğini gösteren kriter nedir?",
                answer="Serum beta-hCG seviyelerinin tamamen sıfırlanması ve ardışık ölçümlerde negatif kalmasıdır."
            )
        ]
    ))

    # Slide 39
    slides.append(make_slide(
        slide_num=39,
        title="Gestasyonel vs Gonadal Koryokarsinom: Paternal Antijen Ayrımı",
        subtitle="Uterus kaynaklıda tam şifa, gonad kaynaklıda kemodirenç",
        clinical_focus="Kemoterapi yanıtındaki immünolojik temelin moleküler açıklaması",
        narrative=(
            "Koryokarsinom iki farklı anatomik bölgeden köken alabilir ve bu iki grubun kemoterapiye yanıtı dramatik bir uçurum gösterir.\n\n"
            "- **Gestasyonel (Plasental) Koryokarsinom:** Uterusta gebelik trofoblastlarından köken alır. Kemoterapi ile kür oranı **%100'e yakındır**.\n"
            "- **Non-Gestasyonel (Gonadal) Koryokarsinom:** Over veya testisteki germ hücrelerinden köken alır. Bu tümörler **kemoterapiye dirençlidir ve prognozları son derece kötüdür**.\n"
            "- **İmmünolojik Mekanizma (Paternal Antijenler):** Gestasyonel koryokarsinom döllenmiş bir zigottan türediği için hücrelerinde **babadan gelen (paternal) yabancı antijenler** taşır. Anne organizmasının immün sistemi (allogreft benzeri) bu paternal antijenleri yabancı tanır ve kemoterapinin tümör hücrelerini öldürmesine güçlü bir sinerji ile yardımcı olur. Gonadal tümörler ise hastanın kendi saf somatik/germinal hücrelerinden geliştiği için paternal yabancı antijen taşımazlar; maternal immün yanıt oluşmaz ve kemoterapi başarısız kalır.\n\n"
            "> [!IMPORTANT]\n"
            "> Gestasyonel koryokarsinomda paternal antijenler maternal immün yanıtı tetikleyerek kemoterapinin %100 kür sağlamasına yardım eder; gonadal tümörde paternal antijen yoktur ve prognoz kötüdür."
        ),
        bullets=[
            "Plasental koryokarsinom kemoterapiye tam yanıt verir (%100 kür)",
            "Gonadal (over/testis) koryokarsinom kemoterapiye dirençlidir",
            "Yanıt farkının temeli tümördeki paternal (baba) antijenleridir",
            "Maternal immün sistem paternal antijenleri allogreft gibi tanıyarak kemoterapiyi destekler"
        ],
        elements=[
            make_quiz(
                question="Uterus kaynaklı gestasyonel koryokarsinom kemoterapi ile %100 kür edilebilirken, over veya testis kökenli non-gestasyonel koryokarsinomun kemoterapiye kötü yanıt vermesinin temel immünolojik nedeni nedir?",
                options=[
                    {"key": "A", "text": "Gonadal koryokarsinomun hCG hormonu yerine insülin salgılaması", "isCorrect": False, "explanation": "Her iki tümör de hCG salgılar; hormon tipi yanıt farkını açıklamaz."},
                    {"key": "B", "text": "Plasental koryokarsinomda paternal antijenlerin bulunması ve maternal immün yanıtın kemoterapiye destek vermesi", "isCorrect": True, "explanation": "Doğru. Gestasyonel tümör paternal yabancı antijenler taşır ve maternal immün yanıt kemoterapiyle sinerji oluşturarak %100 kürü sağlar; gonadal tümörde paternal antijen yoktur."},
                    {"key": "C", "text": "Gonadal koryokarsinomun sadece 80 yaş üstü erkeklerde ortaya çıkması", "isCorrect": False, "explanation": "Gonadal tümörler genç erişkinlerde görülür."},
                    {"key": "D", "text": "Plasental tümörde TP53 geninin tamamen kaybolması", "isCorrect": False, "explanation": "TP53 durumu immünolojik paternal antijen farkını açıklamaz."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Prognozlar arasındaki önemli farklılıklar, plasental koryokarsinomda paternal antijenlerin bulunması, buna karşın gonad tümörlerinde bulunmaması ile ilişkilidir.",
                masked_term="paternal antijenlerin bulunması",
                hint="Babadan gelen yabancı doku proteinlerinin varlığı"
            ),
            make_slider(
                left_title="Gestasyonel (Plasental) Koryokarsinom",
                right_title="Non-Gestasyonel (Gonadal) Koryokarsinom",
                left_points=[
                    "Köken: Uterustaki gebelik trofoblastları",
                    "Paternal antijenler mevcuttur (babadan gelen genler)",
                    "Maternal immün yanıt kemoterapiyi güçlü destekler",
                    "Tedavi sonucu: %100'e yakın tam kür"
                ],
                right_points=[
                    "Köken: Over veya testisteki totipotent germ hücreleri",
                    "Paternal yabancı antijen bulunmaz (hastanın kendi genomu)",
                    "Maternal immün destekleyici yanıt oluşmaz",
                    "Tedavi sonucu: Kemoterapiye dirençli ve kötü prognoz"
                ]
            ),
            make_recall(
                question="Gestasyonel koryokarsinomun kemoterapiye verdiği olağanüstü yüksek kür yanıtında hangi genetik ebeveyn faktörü rol oynar?",
                answer="Babadan gelen (paternal) yabancı antijenlerin tümör hücrelerinde bulunması ve konağın immün sistemini aktive etmesidir."
            )
        ]
    ))

    # Slide 40 - Checkpoint 4
    slides.append(make_slide(
        slide_num=40,
        title="[TEKRAR SAYFASI - CHECKPOINT 4] İnvaziv Mol ve Koryokarsinom Patolojisi",
        subtitle="Bölüm 4 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="İnvaziv mol özellikleri, koryokarsinom morfolojisi, metastaz ve tedavi özeti",
        narrative=(
            "Bu tekrar sayfası, 31-39. adımlarda işlenen İnvaziv Mol ve Koryokarsinom Patolojisi kazanımlarını pekiştirmek için düzenlenmiştir. "
            "İnvaziv mol, komplet molün hidropik villuslarının myometrium derinliklerine penetre olmasıdır; rüptür ve kanama riski taşır ancak koryokarsinomun agresif metastatik potansiyelini göstermez ve kemoterapiyle tam şifaya kavuşur.\n\n"
            "- **Koryokarsinom Kökeni:** Olguların %50'si komplet molü, %25'i düşüğü, %22'si normal term gebeliği izler. Afrika'da 2000'de 1 sıklıktadır; 40 yaş üzeri risk artar.\n"
            "- **Klinik ve Makroskopi:** Kahverengi akıntı ve aşırı hCG yüksekliği vardır; moldekinin aksine uterusta belirgin büyüme olmaz. Yumuşak, koyu kanamalı ve nekrotiktir.\n"
            "- **Histoloji ve Metastaz:** Koryon villusu KESİNLİKLE yoktur; saf anaplastik sito/sinsityotrofoblast kitlelerinden oluşur. Hematojen yolla en sık akciğerlere (%50) ve vajinaya metastaz yapar.\n"
            "- **Paternal Antijen Mucizesi:** Paternal antijen taşıması nedeniyle maternal immün yanıtın desteğiyle kemoterapiden %100 kür sağlanır; oysa gonadal koryokarsinom kemodirençlidir.\n\n"
            "> [!NOTE]\n"
            "> İnvaziv molde villus vardır ve metastaz yoktur; koryokarsinomda ise villus yoktur ve kan yoluyla akciğere yayılır; her ikisi de kemoterapiye çok duyarlıdır."
        ),
        bullets=[
            "İnvaziv mol: Myometriuma penetre hidropik villuslar; metastaz yok, tam kür",
            "Koryokarsinom öncülü: %50 komplet mol, %25 düşük, %22 term gebelik",
            "Koryokarsinom kliniği: Kahverengi akıntı, aşırı hCG, uterusta büyüme yok",
            "Histoloji: Koryon villusu KESİNLİKLE yoktur; saf anaplastik trofoblastlar",
            "Metastaz: Hematojen (en sık %50 akciğer); paternal antijenlerle %100 kemoterapötik kür"
        ],
        elements=[
            make_quiz(
                question="İnvaziv mol ve koryokarsinomun patolojik ve klinik özellikleri hakkında aşağıdaki ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "İnvaziv molde koryon villusları bulunmazken koryokarsinom kistik villuslarla doludur.", "isCorrect": False, "explanation": "Tam tersi; invaziv molde villus vardır, koryokarsinomda villus kesinlikle yoktur."},
                    {"key": "B", "text": "Koryokarsinom en sık lenfatik yolla inguinal lenf nodlarına yayılır ve kemoterapiye dirençlidir.", "isCorrect": False, "explanation": "Yanlış. Hematojen yolla akciğere yayılır ve kemoterapiye %100'e yakın yanıt verir."},
                    {"key": "C", "text": "Koryokarsinomda koryon villusları oluşmaz; hematojen yolla en sık akciğere metastaz yapar ve kemoterapiyle %100 kür sağlanabilir.", "isCorrect": True, "explanation": "Doğru. Koryokarsinom villussuzdur, %50 akciğere yayılır ve kemoterapiye mükemmel yanıtla kür edilir."},
                    {"key": "D", "text": "İnvaziv mol cerrahi küretaj ile daima tek seansta tamamen temizlenir.", "isCorrect": False, "explanation": "Yanlış. Myometrium derinliklerinde olduğu için küretajla temizlenemez, medikal kemoterapi gerekir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Mol hidatiform ve invaziv molün aksine koryokarsinomda koryon villusları oluşmamıştır ve tümör tümüyle anaplastik trofoblastlardan oluşur.",
                masked_term="koryon villusları oluşmamıştır",
                hint="Malign trofoblastik tümörün en kritik negatif patoloji kriteri"
            ),
            make_table(
                title="Bölüm 4 İnvaziv Mol ve Koryokarsinom Özeti",
                headers=["Özellik", "İnvaziv Mol", "Koryokarsinom"],
                rows=[
                    [
                        {"text": "Koryon Villus Varlığı", "isMasked": False},
                        {"text": "Hidropik villuslar mevcuttur", "isMasked": True, "hint": "Kistik yapıların korunması"},
                        {"text": "Kesinlikle villus yoktur", "isMasked": True, "hint": "Koryon çatısının tamamen bulunmaması"}
                    ],
                    [
                        {"text": "Uzak Metastaz Potansiyeli", "isMasked": False},
                        {"text": "Metastaz yapmaz", "isMasked": False},
                        {"text": "Çok erken hematojen metastaz (akciğer %50)", "isMasked": False}
                    ],
                    [
                        {"text": "Kemoterapiye Yanıt", "isMasked": False},
                        {"text": "Tam şifa (kür)", "isMasked": False},
                        {"text": "Paternal antijen desteğiyle %100 kür", "isMasked": True, "hint": "Babadan gelen proteinlerin sağladığı başarı"}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 4 Kontrol Önermeleri",
                items=[
                    {"text": "İnvaziv mol komplet molün myometrium derinliklerine penetre olmasıyla oluşur.", "isLie": False, "explanation": "Doğru. Tanım gereği myometrial penetrasyondur."},
                    {"text": "Koryokarsinom olgularının %50'si komplet mol hidatiformu izler.", "isLie": False, "explanation": "Doğru. Vakaların yarısında öncül komplet moldür."},
                    {"text": "Koryokarsinomda uterus kavitesi tıpkı mol hidatiform gibi daima 35 haftalık gebelik boyutuna ulaşır.", "isLie": True, "explanation": "Tuzak! Koryokarsinomda moldekinin aksine uterusta belirgin bir büyüme izlenmez."},
                    {"text": "Gestasyonel koryokarsinom paternal antijenler taşıdığı için kemoterapiye mükemmel yanıt verir.", "isLie": False, "explanation": "Doğru. Paternal antijenler immün yanıtı tetikler."}
                ]
            ),
            make_recall(
                question="Checkpoint 4: İnvaziv mol ile koryokarsinom arasındaki en temel iki farkı (biri mikroskobik, biri biyolojik) belirtiniz.",
                answer="Mikroskobik olarak invaziv molde hidropik koryon villusları varken koryokarsinomda kesinlikle villus yoktur; biyolojik olarak invaziv mol uzak metastaz yapmazken koryokarsinom kan yoluyla erken metastaz yapar."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=4
    ))
    
    return slides
