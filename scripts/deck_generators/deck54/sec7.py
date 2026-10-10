"""
Deck 54 - Section 7: Uterus Korpusu ve Myometrium Düz Kas Patolojisi Entegrasyonu (Slayt 61-70)
Slayt 70: Checkpoint 7
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec7_slides():
    slides = []
    
    # Slide 61
    slides.append(make_slide(
        slide_num=61,
        title="Uterus Düz Kas Lezyonlarında Histopatolojik Spektrum",
        subtitle="Hücresel, atipik (semptomatik), mitojenik ve epiteloid varyantlar",
        clinical_focus="Leiomyom varyantlarının leiomyosarkomla ayırıcı tanısı",
        narrative=(
            "Myometriumun düz kas neoplazmları klasik benign leiomyom ile agresif leiomyosarkom arasında geniş bir histopatolojik morfoloji çeşitliliği sergiler. "
            "Bu ara formların doğru tanınması gereksiz radikal cerrahileri önlemek açısından kritiktir.\n\n"
            "- **Sellüler (Hücresel) Leiomyom:** Düz kas hücre yoğunluğu normal myometriuma göre belirgin olarak artmıştır; ancak nükleer atipi ve tümör nekrozu yoktur, mitotik aktivite düşüktür (<4/10 BÜA). Tamamen selimdir.\n"
            "- **Atipik (Bizar / Simpatik) Leiomyom:** Hücrelerde belirgin nükleer pleomorfizm ve dev hiperkromatik nükleuslar izlenir. Ancak bu atipiye yüksek mitoz ve koagülatif tümör nekrozu eşlik etmez; biyolojik davranışı benign seyreder.\n"
            "- **Mitotik Aktif Leiomyom:** Genellikle genç, reprodüktif çağdaki veya oral kontraseptif kullanan kadınlarda görülür. 10 BÜA'da 5-9 mitoz izlenebilir ancak sitolojik atipi ve nekroz bulunmaz.\n\n"
            "> [!NOTE]\n"
            "> Sitolojik atipisi olan bir düz kas tümöründe koagülatif nekroz ve yüksek mitoz (≥10/10 BÜA) yoksa bizar (atipik) leiomyom tanısı konur; sarkom değildir."
        ),
        bullets=[
            "Sellüler leiomyom: Yoğun hücreli fakat atipisiz ve mitozsuzdur",
            "Atipik (bizar) leiomyom: Dev pleomorfik nükleuslara rağmen nekroz ve yüksek mitoz içermez",
            "Mitotik aktif leiomyom: Genç kadınlarda mitoz artmıştır fakat atipi yoktur",
            "Stanford tanı kriterleri malignite ayrımında temel kılavuzdur"
        ],
        elements=[
            make_quiz(
                question="Bir uterin düz kas tümörünün mikroskobik incelemesinde multinükleer dev bizar hücreler ve belirgin nükleer pleomorfizm saptanmasına rağmen, mitotik indeksin <2/10 BÜA olması ve koagülatif tümör nekrozunun kesinlikle bulunmaması durumunda en olası tanı hangisidir?",
                options=[
                    {"key": "A", "text": "Klasik yüksek dereceli leiomyosarkom", "isCorrect": False, "explanation": "Leiomyosarkomda yüksek mitoz (≥10) ve koagülatif tümör nekrozu şarttır."},
                    {"key": "B", "text": "Koryokarsinom myometrial metastazı", "isCorrect": False, "explanation": "Koryokarsinom trofoblastik epitelyal tümördür; bizar düz kas hücresi içermez."},
                    {"key": "C", "text": "Atipik (bizar / simpatik) leiomyom", "isCorrect": True, "explanation": "Doğru. Belirgin sitolojik atipiye rağmen nekroz ve yüksek mitozun bulunmaması atipik (bizar) leiomyomun benign karakterini gösterir."},
                    {"key": "D", "text": "Plasenta inkreta odağı", "isCorrect": False, "explanation": "İnkreta koryon villuslarının kas içine girmesidir; düz kas neoplazmı değildir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Belirgin nükleer pleomorfizm içermesine rağmen nekroz ve yüksek mitotik aktivite barındırmayan selim düz kas neoplazmına atipik bizar leiomyom adı verilir.",
                masked_term="atipik bizar leiomyom",
                hint="Sitolojik pleomorfizm taşıyan ancak selim seyreden miyom varyantı"
            ),
            make_slider(
                left_title="Atipik (Bizar) Leiomyom",
                right_title="Klasik Leiomyosarkom",
                left_points=[
                    "Dev nükleuslar ve pleomorfik bizar hücreler mevcuttur",
                    "Mitotik figürler seyrektir (<5 mitoz / 10 BÜA)",
                    "Koagülatif tümör hücresi nekrozu KESİNLİKLE yoktur",
                    "Klinik seyir tamamen selimdir; nüks ve metastaz yapmaz"
                ],
                right_points=[
                    "Yaygın nükleer pleomorfizm ve atipi mevcuttur",
                    "Mitotik aktivite çok yüksektir (≥10 mitoz / 10 BÜA)",
                    "Koagülatif tümör hücresi nekrozu KARAKTERİSTİKTİR",
                    "Klinik seyir oldukça agresiftir; hematojen akciğer metastazı yapar"
                ]
            ),
            make_recall(
                question="Düz kas tümörlerinde 'atipik (bizar) leiomyom' tanısını leiomyosarkomdan ayıran iki majör negatif bulgu nedir?",
                answer="Yüksek mitotik aktivitenin (≥10/10 BÜA) ve koagülatif tümör hücresi nekrozunun bulunmamasıdır."
            )
        ]
    ))

    # Slide 62
    slides.append(make_slide(
        slide_num=62,
        title="Uterus Düz Kas Tümörlerinde Biyolojik Davranışı Belirsiz Tümörler (STUMP)",
        subtitle="Malignite kriterlerinin kısmi varlığı ve gri zon lezyonları",
        clinical_focus="STUMP antitesinin patolojik tanı kriterleri ve onkolojik takibi",
        narrative=(
            "Patoloji pratiğinde bazı düz kas neoplazmları klasik benign leiomyom kriterlerini aşarken, kesin leiomyosarkom tanısı için gerekli üç kriteri (Stanford triadı) tam olarak dolduramaz. "
            "Bu belirsiz ara kategoriye **Bilinmeyen Malignite Potansiyelli Düz Kas Tümörü (STUMP - Smooth Muscle Tumor of Uncertain Malignant Potential)** adı verilir.\n\n"
            "- **Gri Zon Morfolojileri:** Örneğin, tümör nekrozu olan fakat sitolojik atipisi ve mitozu olmayan lezyonlar; veya belirgin atipisi ve 8-9 mitozu olan fakat nekrozu bulunmayan olgular STUMP kapsamında sınıflandırılır.\n"
            "- **Klinik Yaklaşım:** STUMP tanısı alan hastalar kesin benign kabul edilmez. Nadiren yıllar sonra lokal rekürrens veya uzak metastaz yapabilme potansiyelleri bulunduğu için uzun süreli jinekolojik onkolojik takip altında tutulurlar.\n\n"
            "> [!NOTE]\n"
            "> Leiomyom ile leiomyosarkom sınır kriterlerini kısmen taşıyan gri zon neoplazmları STUMP kategorisinde izlenir."
        ),
        bullets=[
            "Leiomyom ve leiomyosarkom arasındaki gri zon düz kas neoplazmıdır",
            "Stanford malignite kriterlerinden yalnızca birini veya sınırda değerleri taşır",
            "Kesin selim kabul edilmez; geç nüks ve metastaz riski nedeniyle izlenir",
            "Cerrahi sonrası uzun süreli onkolojik takip gerektirir"
        ],
        elements=[
            make_quiz(
                question="Bir myometriyal düz kas tümöründe malignite kriterlerinin (atipi, mitoz, nekroz) bir kısmının sınırda bulunması nedeniyle kesin benign veya malign ayrılamayan gri zon lezyonlarına verilen patolojik ad hangisidir?",
                options=[
                    {"key": "A", "text": "Adenoakantoma", "isCorrect": False, "explanation": "Adenoakantoma skuamöz metaplazi içeren endometrioid karsinomdur."},
                    {"key": "B", "text": "STUMP (Bilinmeyen Malignite Potansiyelli Düz Kas Tümörü)", "isCorrect": True, "explanation": "Doğru. Kriterleri tam dolduramayan ara formlara STUMP (Smooth Muscle Tumor of Uncertain Malignant Potential) denir."},
                    {"key": "C", "text": "İnvaziv mol", "isCorrect": False, "explanation": "İnvaziv mol trofoblastik hastalıktır; düz kas tümörü değildir."},
                    {"key": "D", "text": "Endometrial stromal nodül", "isCorrect": False, "explanation": "Endometrial stroma kaynaklı selim lezyondur; myosit neoplazmı değildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Kesin leiomyom veya leiomyosarkom kriterlerini dolduramayan sınırda myometriyal düz kas lezyonları STUMP olarak adlandırılır.",
                masked_term="STUMP",
                hint="Smooth Muscle Tumor of Uncertain Malignant Potential kısaltması"
            ),
            make_table(
                title="Myometrium Düz Kas Neoplazmları Sınıflama Spektrumu",
                headers=["Kategori", "Mitoz / Atipi / Nekroz", "Biyolojik Davranış"],
                rows=[
                    [
                        {"text": "Klasik Leiomyom", "isMasked": False},
                        {"text": "Mitoz az, atipi yok, nekroz yok", "isMasked": True, "hint": "Tüm malignite kriterlerinin negatifliği"},
                        {"text": "Tamamen selim; küçülme eğiliminde", "isMasked": False}
                    ],
                    [
                        {"text": "STUMP", "isMasked": False},
                        {"text": "Kriterlerin bir kısmı sınırda pozitif", "isMasked": True, "hint": "Gri zon morfolojik tablosu"},
                        {"text": "Belirsiz potansiyel; onkolojik izlem gerekir", "isMasked": False}
                    ],
                    [
                        {"text": "Leiomyosarkom", "isMasked": False},
                        {"text": "Atipi +, ≥10 mitoz, koagülatif nekroz +", "isMasked": False},
                        {"text": "Oldukça agresif; hematojen akciğer metastazı", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="STUMP tanısı alan bir kadında cerrahi sonrası klinik yönetim nasıl planlanır?",
                answer="Tamamen selim kabul edilmez; olası geç nüks veya metastaz açısından düzenli aralıklarla pelvik ve pulmoner onkolojik takip altında tutulur."
            )
        ]
    ))

    # Slide 63
    slides.append(make_slide(
        slide_num=63,
        title="Uterin Düz Kas vs Endometrial Lezyonlar: Karşılaştırmalı Ayırıcı Tanı",
        subtitle="Endometrial polip, adenomyozis ve leiomyom ayırımı",
        clinical_focus="Uterus korpusunda kitle ve kanama yapan antitelerin ayırıcı tanısı",
        narrative=(
            "Uterus korpusunda yer kaplayan ve anormal uterin kanama (AUK) yapan lezyonların patolojik ayrımı histogenetik kökene dayanır.\n\n"
            "- **Leiomyom:** Saf myometrial düz kas hücrelerinin monoklonal neoplazmıdır. Keskin sınırlı, gri-beyaz, girdapsı sert kitle oluşturur. Bez yapıları içermez.\n"
            "- **Endometrial Polip:** Endometrium bazalis tabakasının fokal hiperplazisidir; stroma, kalın duvarlı kan damarları ve kistik glandlardan oluşan ekzofitik kaviter lezyondur; düz kas içermez (bazen tabanında miyom lifleri olabilir).\n"
            "- **Adenomyozis:** Endometrial bez ve stromanın myometrium kas lifleri arasına gömülmesidir; sınırları belirsizdir, enüklee edilemez ve uterus duvarında diffüz kalınlaşma yapar.\n\n"
            "> [!NOTE]\n"
            "> Leiomyom düz kas neoplazmıdır ve enüklee edilebilir; adenomyozis kas içine gömülü endometriumdur ve sınırları belirsizdir; polip ise kaviter mukozal çıkıntıdır."
        ),
        bullets=[
            "Leiomyom: Myometrium düz kası kökenli, keskin sınırlı, bezsizdir",
            "Endometrial polip: Endometrium bazalis hiperplazisi, kaviter ekzofitiktir",
            "Adenomyozis: Myometrium içine gömülmüş gland ve stroma; diffüz büyüme",
            "Üç antite de menoraji yapabilir fakat patolojileri tamamen farklıdır"
        ],
        elements=[
            make_venn(
                title="Leiomyom vs Adenomyozis Ayırıcı Tanısı",
                label_a="Leiomyom",
                label_b="Adenomyozis",
                items=[
                    {"criterion": "Keskin sınırlı psödokapsül ile cerrahi olarak enüklee edilebilme", "correct": "A", "explanation": "Leiomyom çevre myometriumdan soyularak kolayca çıkarılabilir."},
                    {"criterion": "Myometrium içinde sınırları belirsiz diffüz kalınlaşma ve gland adacıkları", "correct": "B", "explanation": "Adenomyozis invaziv gland-stroma içerir; sınırları siliktir, enüklee edilemez."},
                    {"criterion": "Üreme çağındaki kadınlarda menoraji ve pelvik ağrıya yol açabilme", "correct": "both", "explanation": "Her iki antite de sık menoraji ve dismenore nedenidir."},
                    {"criterion": "Saf trofoblastik anaplastik hücrelerden oluşup koryon villusu içermeme", "correct": "neither", "explanation": "Bu koryokarsinomun özelliğidir; leiomyom ve adenomyozisle ilgisizdir."}
                ]
            ),
            make_quiz(
                question="Histerektomi materyalinde uterus duvarının diffüz kalınlaştığı, kesit yüzünde myometrium kas lifleri arasında küçük çökük kahverengi kanama odakları ve glandüler yarıklar izlendiği, ancak keskin sınırlı girdapsı bir nodülün bulunmadığı olguda öncelikli tanı hangisidir?",
                options=[
                    {"key": "A", "text": "İntramural leiomyom", "isCorrect": False, "explanation": "İntramural miyom keskin sınırlı, sert ve girdapsı nodüldür; diffüz bezli infiltrasyon yapmaz."},
                    {"key": "B", "text": "Adenomyozis", "isCorrect": True, "explanation": "Doğru. Sınırları belirsiz diffüz myometrial kalınlaşma ve kas içinde endometrial gland odakları adenomyozisin klasik patolojisidir."},
                    {"key": "C", "text": "Malign leiomyosarkom", "isCorrect": False, "explanation": "Leiomyosarkom yumuşak, nekrotik ve kanamalı soliter kitledir."},
                    {"key": "D", "text": "Komplet mol hidatiform", "isCorrect": False, "explanation": "Mol hidatiform gebelik ürünüdür; üzüm salkımı kistik veziküller içerir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Keskin sınırlı leiomyomun aksine, myometrium içine gömülen endometrial bez ve stromanın oluşturduğu adenomyozis lezyonları cerrahi olarak enüklee edilemez.",
                masked_term="adenomyozis",
                hint="Myometrium içine ektopik endometrium invazyonu tablosu"
            ),
            make_recall(
                question="Cerrahi myomektomi ameliyatında cerrahın miyomu çevre myometriumdan kolayca soyup çıkarabilmesini (enükleasyon) sağlayan anatomik özellik nedir?",
                answer="Tümörün çevre normal kas liflerini iterek oluşturduğu keskin sınırlı psödokapsül yapısıdır."
            )
        ]
    ))

    # Slide 64
    slides.append(make_slide(
        slide_num=64,
        title="Uterus Patolojisinde Ayırıcı Tanı: Leiomyosarkom vs Karsinosarkom",
        subtitle="Mezenkimal sarkom ile bifazik epitelyal-mezenkimal tümör ayrımı",
        clinical_focus="Malign mikst müllerian tümör (MMMT) ile saf sarkom ayrımı",
        narrative=(
            "Postmenopozal dönemde uterus kavitesinden kaynaklanan malign kitlelerde leiomyosarkomun en önemli ayırıcı tanılarından biri **karsinosarkomdur (malign mikst müllerian tümör - MMMT)**.\n\n"
            "- **Histogenetik Köken Farkı:** Leiomyosarkom saf bir mezenkimal düz kas sarkomudur; epitelyal komponent içermez. Karsinosarkom ise köken olarak yüksek dereceli bir endometriyal karsinomdur; epitelyal-mezenkimal transdiferansiasyon (EMT) geçirerek hem malign karsinom hem de malign sarkom (kıkırdak, kemik veya rabdomyoblast) alanları içeren **bifazik** bir tümördür.\n"
            "- **Metastaz Paternleri:** Leiomyosarkom lenfatikleri atlayıp doğrudan hematojen yolla akciğere gider. Karsinosarkom ise karsinom biyolojisine sahip olduğu için hem pelvik lenf nodlarına lenfatik yolla yayılır hem de periton içine karsinomatozis yapar.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyosarkom saf düz kas sarkomudur ve hematojen yayılır; karsinosarkom ise bifazik karsinom kökenli agresif bir tümör olup lenfatik yayılım da gösterir."
        ),
        bullets=[
            "Leiomyosarkom: Saf mezenkimal düz kas sarkomudur (monofazik)",
            "Karsinosarkom: Malign karsinom + malign sarkom içeren bifazik tümördür",
            "Karsinosarkom heterolog elemanlar (kıkırdak, iskelet kası) içerebilir",
            "Leiomyosarkom hematojen akciğer; karsinosarkom lenfatik ve peritoneal yayılır"
        ],
        elements=[
            make_quiz(
                question="Postmenopozal bir kadında histerektomi materyalinde uterus kavitesini dolduran kitlenin mikroskopisinde hem malign adenokarsinom glandları hem de malign kondrosarkom/rabdomyosarkom alanları içeren BİFAZİK tümör saptanması hangi tanıyı koydurur?",
                options=[
                    {"key": "A", "text": "Klasik soliter leiomyosarkom", "isCorrect": False, "explanation": "Leiomyosarkom saf düz kas sarkomudur; malign karsinom glandları içermez."},
                    {"key": "B", "text": "Gestasyonel koryokarsinom", "isCorrect": False, "explanation": "Koryokarsinom sito/sinsityotrofoblastlardan oluşur; kıkırdak veya karsinom glandı yapmaz."},
                    {"key": "C", "text": "Sellüler leiomyom", "isCorrect": False, "explanation": "Sellüler miyom benign selim düz kas neoplazmıdır."},
                    {"key": "D", "text": "Karsinosarkom (Malign Mikst Müllerian Tümör - MMMT)", "isCorrect": True, "explanation": "Doğru. Malign epitel ve malign mezenkimi bir arada barındıran bifazik tümör karsinosarkomdur (MMMT)."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Malign epitelyal glandlar ile heterolog malign mezenkimal dokuları bir arada içeren bifazik uterin neoplazma karsinosarkom denir.",
                masked_term="karsinosarkom",
                hint="Malign mikst müllerian tümör (MMMT) teriminin diğer adı"
            ),
            make_slider(
                left_title="Uterin Leiomyosarkom",
                right_title="Uterin Karsinosarkom (MMMT)",
                left_points=[
                    "Saf mezenkimal tümördür (monofazik düz kas sarkomu)",
                    "Malign epitelyal gland yapıları KESİNLİKLE içermez",
                    "Primer yayılım yolu hematojendir (en sık akciğer parankimi)"
                ],
                right_points=[
                    "Karsinom kökenli bifazik tümördür (epitelyal + mezenkimal)",
                    "Malign karsinom glandları ve malign sarkomatöz stroma içerir",
                    "Hem lenfatik lenf nodu hem de peritoneal yayılım gösterir"
                ]
            ),
            make_recall(
                question="Leiomyosarkomun mikroskopik kesitinde malign glandüler epitel veya malign kıkırdak odaklarının görülmesi tanıyı nasıl değiştirir?",
                answer="Tanıyı leiomyosarkomdan çıkarır; tümörün bifazik bir karsinosarkom (MMMT) olduğunu gösterir."
            )
        ]
    ))

    # Slide 65
    slides.append(make_slide(
        slide_num=65,
        title="Trofoblastik Hastalıklarda Genetik Poliploidi Karşılaştırması",
        subtitle="Diploidi (androgenez), triploidi (dispermi) ve anöploidi",
        clinical_focus="Molar antitelerin ve karsinomun sitogenetik mimarisi",
        narrative=(
            "Gestasyonel trofoblastik neoplazmlarda karyotip analizi, tümörün biyolojik davranışını ve köken aldığı döllenme kusurunu aydınlatan temel genetik kılavuzdur.\n\n"
            "- **Komplet Mol Genetiği:** Daima diploidtir (en sık 46,XX). Tüm nükleer kromozomlar paternal kaynaklıdır (androgenez). Maternal p57KIP2 gen ekspresyonu negatiftir.\n"
            "- **Parsiyel Mol Genetiği:** Daima triploidtir (en sık 69,XXY). Bir maternal takıma karşılık iki paternal takım mevcuttur. Maternal alel bulunduğu için p57KIP2 gen ekspresyonu pozitiftir.\n"
            "- **Koryokarsinom Genetiği:** Genellikle anöploid veya kompleks hiperdiploid/tetraploid karyotipe sahiptir. Yüksek oranda kromozomal instabilite, TP53 mutasyonları ve mikrosatellit instabilitesi eşlik edebilir.\n\n"
            "> [!NOTE]\n"
            "> Komplet mol diploid ve p57 negatiftir; parsiyel mol triploid ve p57 pozitiftir; bu immünohistokimyasal belirteç patolojide altın standarttır."
        ),
        bullets=[
            "Komplet mol: Diploid (46,XX), androgenetik, maternal p57KIP2 negatiftir",
            "Parsiyel mol: Triploid (69,XXY), dispermik, maternal p57KIP2 pozitiftir",
            "Koryokarsinom: Kompleks anöploid veya hiperdiploid genom",
            "p57KIP2 immünohistokimyası komplet ve parsiyel molü kesin ayırır"
        ],
        elements=[
            make_quiz(
                question="Maternal genom tarafından eksprese edilen ve komplet mol hidatiformda kesinlikle negatifken (ekspresyon yok), parsiyel molde maternal alel varlığı nedeniyle pozitif boyanan immünohistokimyasal belirteç hangisidir?",
                options=[
                    {"key": "A", "text": "Human koryonik gonadotropin (hCG)", "isCorrect": False, "explanation": "hCG her iki molde de sinsityotrofoblastlarda pozitiftir; ayrım yapmaz."},
                    {"key": "B", "text": "p57KIP2 (CDKN1C)", "isCorrect": True, "explanation": "Doğru. p57KIP2 anneden gelen (maternal) alelden eksprese edilir; maternal genomu olmayan komplet molde negatiftir, parsiyel molde pozitiftir."},
                    {"key": "C", "text": "Östrojen reseptörü (ER)", "isCorrect": False, "explanation": "ER trofoblastik ayırıcı tanıda kullanılmaz."},
                    {"key": "D", "text": "S-100 proteini", "isCorrect": False, "explanation": "S-100 nöral ve melanotik belirteçtir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Maternal genomun bulunmadığı komplet mol hidatiform olgularında sitotrofoblast ve villus stromasında p57KIP2 boyanması negatiftir.",
                masked_term="p57KIP2",
                hint="Maternal alel varlığını gösteren siklin bağımlı kinaz inhibitörü proteini"
            ),
            make_table(
                title="Trofoblastik Lezyonlarda Sitogenetik ve İmmün Belirteçler",
                headers=["Antite", "Kromozom Durumu", "p57KIP2 İHK Boyanması"],
                rows=[
                    [
                        {"text": "Komplet Mol", "isMasked": False},
                        {"text": "Diploid (46,XX)", "isMasked": True, "hint": "İki takım babadan gelen kromozom"},
                        {"text": "Negatif (maternal alel yok)", "isMasked": False}
                    ],
                    [
                        {"text": "Parsiyel Mol", "isMasked": False},
                        {"text": "Triploid (69,XXY)", "isMasked": True, "hint": "Üç takım dispermik kromozom"},
                        {"text": "Pozitif (maternal alel mevcut)", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Patolog komplet mol ile hidropik abortus veya parsiyel molü mikroskop altında ayırt etmekte zorlandığında hangi immünohistokimyasal boyamayı ister?",
                answer="p57KIP2 boyamasını ister; komplet molde nükleer p57 boyanması tamamen negatiftir."
            )
        ]
    ))

    # Slide 66
    slides.append(make_slide(
        slide_num=66,
        title="Uterus Düz Kas Tümörlerinde Dejenerasyon ve İskemi Mekanizması",
        subtitle="Miyom içi vasküler yetersizlik, nekroz tipleri ve ayırıcı tanı",
        clinical_focus="Leiomyom dejenerasyonunun koagülatif tümör nekrozuyla karışmaması",
        narrative=(
            "Leiomyomlar büyük boyutlara ulaştıklarında merkezdeki hücrelerin beslenmesi bozulur. Uterustaki düz kas tümörlerinin dejeneratif değişiklikleri malign nekrozla karıştırılmamalıdır.\n\n"
            "- **İskemik İnfarct Nekrozu (Hiyalin/Kırmızı Dejenerasyon):** Tümörün kan akımı kesildiğinde doku iskemik koagülasyona uğrar. Mikroskopide ölü kas lifleri çevresinde belirgin granülasyon dokusu, köpüksü histiyositler ve fibröz hiyalinizasyon izlenir. Bu selim bir süreçtir.\n"
            "- **Koagülatif Tümör Nekrozu (Malign Kriter):** Leiomyosarkomda görülen nekrozdur. Canlı atipik tümör hücreleri hiçbir granülasyon dokusu veya fibröz bant olmaksızın aniden nekrotik hücre gölgelerine dönüşür.\n"
            "- **Klinik Yansıma:** Gebelikteki kırmızı dejenerasyon akut ağrı yaparken, hiyalin dejenerasyon asemptomatik bir sertleşmeye yol açar.\n\n"
            "> [!IMPORTANT]\n"
            "> Granülasyon dokusu ve hiyalinleşmeyle sınırlı iskemik nekroz selim miyom bulgusudur; canlı atipik hücrelerden aniden nekroza geçiş ise leiomyosarkomun koagülatif tümör nekrozudur."
        ),
        bullets=[
            "Hızlı büyüyen miyomlarda santral vasküler yetersizlikle dejenerasyon gelişir",
            "İskemik nekroza granülasyon dokusu ve hiyalinizasyon eşlik eder (selim)",
            "Koagülatif tümör nekrozu canlı atipik hücreden aniden nekroza geçer (malign)",
            "Gebelikte kırmızı dejenerasyon akut karın ve lökositoz tablosu yapar"
        ],
        elements=[
            make_quiz(
                question="Bir uterin düz kas tümöründe izlenen nekroz alanlarının kenarında granülasyon dokusu, hemosiderin yüklü makrofajlar ve fibröz hiyalinizasyon bulunması öncelikle hangi durumu gösterir?",
                options=[
                    {"key": "A", "text": "Benign leiomyomun iskemik infarkt / dejenerasyon alanı", "isCorrect": True, "explanation": "Doğru. Granülasyon dokusu ve hiyalinizasyonla çevrili nekroz selim leiomyomun iskemik dejenerasyonudur."},
                    {"key": "B", "text": "Yüksek dereceli leiomyosarkomun koagülatif nekrozu", "isCorrect": False, "explanation": "Leiomyosarkom nekrozunda granülasyon dokusu ve hiyalinize sınır bulunmaz; geçiş anidir."},
                    {"key": "C", "text": "Koryokarsinom primer odak perforasyonu", "isCorrect": False, "explanation": "Koryokarsinomda trofoblastik kanama kitleleri olur; düz kas infarktı değildir."},
                    {"key": "D", "text": "Tubal rüptüre bağlı hematosalpinks", "isCorrect": False, "explanation": "Hematosalpinks tuba lümenindedir; miyom içi nekroz değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Selim leiomyomlarda izlenen iskemik nekroza granülasyon dokusu eşlik ederken, leiomyosarkomda canlı atipik hücrelerden aniden nekroza geçiş izlenir.",
                masked_term="granülasyon dokusu",
                hint="İyileşme ve tamir damar-bağ matriks reaksiyonu"
            ),
            make_slider(
                left_title="İskemik Dejenerasyon Nekrozu",
                right_title="Koagülatif Tümör Hücresi Nekrozu",
                left_points=[
                    "Benign leiomyomun vasküler yetersizliğinde görülür",
                    "Nekroz sınırında granülasyon dokusu ve hiyalinizasyon vardır",
                    "Komşu düz kas hücrelerinde sitolojik nükleer atipi bulunmaz"
                ],
                right_points=[
                    "Malign leiomyosarkomun karakteristik bulgusudur",
                    "Canlı tümörden nekroza tamir dokusu olmaksızın ani geçiş vardır",
                    "Komşu tümör hücrelerinde belirgin anaplastik nükleer atipi mevcuttur"
                ]
            ),
            make_recall(
                question="Patolog bir düz kas nekrozunu değerlendirirken 'tümör nekrozu' ile 'iskemik infarkt nekrozu' ayrımını hangi sınıra bakarak yapar?",
                answer="Canlı hücreler ile nekroz arasında granülasyon dokusu ve hiyalinizasyon varsa iskemik infarkt; ani geçiş varsa koagülatif tümör nekrozudur."
            )
        ]
    ))

    # Slide 67
    slides.append(make_slide(
        slide_num=67,
        title="Trofoblastik Hastalıklarda Akciğer Tutulumu: Emboli vs Gerçek Metastaz",
        subtitle="Mol villus embolisi ile koryokarsinom kanamalı kitleleri",
        clinical_focus="Akciğerde saptanan trofoblastik lezyonların klinik davranışı",
        narrative=(
            "Gestasyonel trofoblastik patolojilerde akciğerler en sık tutulan ekstrauterin organdır; ancak akciğere ulaşan lezyonun biyolojik niteliği antiteye göre tamamen değişir.\n\n"
            "- **Molar Villus Embolizasyonu:** Hem komplet mol hem de özellikle invaziv molde koryon villusları ve sinsityotrofoblastlar uterin venöz sinüslere girerek kan akımıyla akciğer kapiller yatağına sürüklenebilir (**trofoblastik emboli**). Bu villuslar akciğer parankimini destrükte edip karsinom gibi büyümezler; sıklıkla pulmoner damarlarda tıkanma, öksürük veya geçici dispne yaparlar ve zamanla kendiliğinden regrese olup kaybolurlar.\n"
            "- **Koryokarsinom Akciğer Metastazı:** Olguların %50'sinde izlenir. Gerçek otonom malign neoplazmdır. Akciğer parankimini ve bronşiyal damarları parçalayarak **multiple, kanamalı, kavitasyon gösteren kitleler (top güllesi lezyonları)** üretir; hemoptiziye yol açar ve kemoterapi verilmezse ölümcüldür.\n\n"
            "> [!NOTE]\n"
            "> İnvaziv molün akciğerdeki villusları embolik ve selimdir; koryokarsinomun akciğer lezyonları ise parankimi yıkan gerçek metastatik tümör kitleleridir."
        ),
        bullets=[
            "İnvaziv molde akciğere giden hidropik villuslar emboliktir ve regrese olabilir",
            "Molar embolizasyon gerçek yıkıcı metastatik kitle oluşturmaz",
            "Koryokarsinom akciğerde multiple kanamalı nekrotik metastazlar yapar (%50)",
            "Koryokarsinom akciğer metastazları hemoptizi ve toraks ağrısı ile prezente olur"
        ],
        elements=[
            make_quiz(
                question="İnvaziv mol olgularında bazen pelvik venler yoluyla akciğer damarlarına sürüklenen hidropik koryon villuslarının biyolojik davranışı hakkında hangisi doğrudur?",
                options=[
                    {"key": "A", "text": "Hemen akciğer karsinomuna dönüşerek tüm göğüs kafesini eritir.", "isCorrect": False, "explanation": "Mol villusları karsinoma dönüşmez; selim embolidir."},
                    {"key": "B", "text": "Bu lezyonlar gerçek agresif metastaz olmayıp embolik niteliktedir ve kendiliğinden regrese olabilir.", "isCorrect": True, "explanation": "Doğru. İnvaziv mol villusları akciğere mekanik embolizasyon yapabilir ancak koryokarsinom gibi agresif metastaz yapmazlar ve gerileyebilirler."},
                    {"key": "C", "text": "Akciğerde kemik metaplazisi başlatarak osteosarkom üretir.", "isCorrect": False, "explanation": "Osteosarkomla hiçbir ilişkisi yoktur."},
                    {"key": "D", "text": "Tümör dokusu olmayıp saf tüberküloz basilleridir.", "isCorrect": False, "explanation": "Trofoblastik villus dokusudur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnvaziv molde uterin venlere giren koryon villusları akciğere embolize olabilir ancak koryokarsinomun agresif metastatik potansiyelini göstermez.",
                masked_term="agresif metastatik potansiyelini",
                hint="Uzak organ dokularını istila edip tahrip eden habis yetenek"
            ),
            make_slider(
                left_title="İnvaziv Mol Pulmoner Embolisi",
                right_title="Koryokarsinom Pulmoner Metastazı",
                left_points=[
                    "Villuslar mekanik olarak venöz kanla taşınır (trofoblastik emboli)",
                    "Akciğer parankiminde ilerleyici yıkıcı tümör kitlesi yapmaz",
                    "Zamanla trombüs gibi organize olup rezorbe olabilir"
                ],
                right_points=[
                    "Gerçek agresif metastatik tümör hücre kolonizasyonudur",
                    "Parankim damarlarını aşındırarak multiple kanamalı kitleler yapar",
                    "Hemoptiziye yol açar; acil sistemik kemoterapi gerektirir"
                ]
            ),
            make_recall(
                question="Koryokarsinomun akciğer parankiminde oluşturduğu multiple kanamalı nodüller radyolojik grafilerde klasik olarak neye benzetilir?",
                answer="'Top güllesi' (cannonball) metastaz manzarasına benzetilir."
            )
        ]
    ))

    # Slide 68
    slides.append(make_slide(
        slide_num=68,
        title="Uterus Patolojisinde Hormon Yanıtları ve Endokrin Bağlantılar",
        subtitle="Östrojen, hCG, progesteron ve trofoblastik-miyometriyal etkileşim",
        clinical_focus="Myometrium ve trofoblast neoplazmlarında hormonal eksen",
        narrative=(
            "Uterus neoplazmları ve gestasyonel patolojiler endokrin hormonal sinyallerle sıkı sıkıya ilişkilidir.\n\n"
            "- **Leiomyom ve Östrojen:** Myometriumun düz kas hücreleri östrojen reseptörleri (ER) ve progesteron reseptörleri (PR) ile donatılmıştır. Over kaynaklı östrojen mitojenik büyüme faktörlerini (EGF, IGF-1) uyararak miyom büyümesini tetikler; menopozda hormon kesilince atrofiye uğrar.\n"
            "- **Trofoblastlar ve hCG:** Sinsityotrofoblastlar devasa miktarda hCG salgılar. hCG lüteinizan hormon (LH) benzeri etkiyle overdeki korpus luteumu uyararak progesteron üretimini devam ettirir; aşırı yüksek hCG overlerde bilateral **teka lutein kistlerine** yol açar.\n"
            "- **Leiomyosarkom ve Koryokarsinom Otonomisi:** Leiomyosarkom hormondan tamamen bağımsız olarak çoğalır; koryokarsinom ise hormon üretir ancak kendi büyümesi hormonal feed-back kontrolünden tamamen çıkmıştır.\n\n"
            "> [!NOTE]\n"
            "> Leiomyom östrojen bağımlı selim büyüme gösterir; mol hidatiform ve koryokarsinom ise devasa hCG salarak overlerde bilateral teka lutein kistlerine neden olabilir."
        ),
        bullets=[
            "Leiomyom östrojen ve progesteron bağımlı proliferasyon sergiler",
            "Postmenopozda östrojen çekilmesiyle miyomlar regrese olur",
            "Molar gebelikte aşırı hCG overlerde bilateral teka lutein kistleri yapar",
            "Leiomyosarkom ve koryokarsinom hormonal denetimden bağımsız otonom lezyonlardır"
        ],
        elements=[
            make_quiz(
                question="Molar gebelik veya koryokarsinomda trofoblastlar tarafından aşırı miktarda salgılanan hCG hormonunun overler üzerindeki gonadotropik uyarısı sonucu bilateral olarak gelişebilen selim kistik over lezyonları hangisidir?",
                options=[
                    {"key": "A", "text": "Seröz kistadenokarsinom", "isCorrect": False, "explanation": "Malign epitelyal over tümörüdür; hCG uyarısıyla oluşmaz."},
                    {"key": "B", "text": "Çikolata kistleri (endometrioma)", "isCorrect": False, "explanation": "Endometriozis kanamaları sonucu gelişir."},
                    {"key": "C", "text": "Teka lutein kistleri", "isCorrect": True, "explanation": "Doğru. Aşırı yüksek hCG seviyeleri overlerde bilateral multiple teka lutein kistlerine (hiperreaksiyo luteinalis) yol açar."},
                    {"key": "D", "text": "Brenner tümörleri", "isCorrect": False, "explanation": "Transizyonel epitelyal over tümörüdür."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Molar hastalıklarda aşırı yükselen hCG hormonunun ovaryan folikülleri uyarması sonucu bilateral teka lutein kistleri gelişebilir.",
                masked_term="teka lutein kistleri",
                hint="Yüksek gonadotropin uyarısıyla overde oluşan bilateral hiperreaksiyon keseleri"
            ),
            make_table(
                title="Uterus Lezyonlarında Hormonal İlişki Matrisi",
                headers=["Patolojik Antite", "İlişkili Majör Hormon", "Hedef Organ / Klinik Yansıma"],
                rows=[
                    [
                        {"text": "Leiomyom", "isMasked": False},
                        {"text": "Östrojen ve progesteron", "isMasked": True, "hint": "Over kaynaklı steroid hormonlar"},
                        {"text": "Miyom kitlesinde hipertrofi ve büyüme", "isMasked": False}
                    ],
                    [
                        {"text": "Mol Hidatiform & Koryokarsinom", "isMasked": False},
                        {"text": "Human koryonik gonadotropin (hCG)", "isMasked": True, "hint": "Sinsityotrofoblastik glikoprotein"},
                        {"text": "Overlerde bilateral teka lutein kistleri", "isMasked": False}
                    ],
                    [
                        {"text": "Leiomyosarkom", "isMasked": False},
                        {"text": "Hormondan bağımsız otonomi", "isMasked": False},
                        {"text": "Postmenopozal dönemde hızlı agresif büyüme", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Molar gebelik tanısı alan bir kadında ultrasonda her iki overde portakal büyüklüğünde kistler saptandığında bu kistlerin yönetimi nasıl olmalıdır?",
                answer="Cerrahi yapılmamalıdır; molar doku kürete edilip hCG seviyeleri düştüğünde bu teka lutein kistleri kendiliğinden spontan regrese olur."
            )
        ]
    ))

    # Slide 69
    slides.append(make_slide(
        slide_num=69,
        title="Uterus ve Trofoblast Tümörlerinde Onkolojik Prognoz Faktörleri",
        subtitle="Evre, derinlik, metastaz varlığı ve immünolojik yanıt sentezi",
        clinical_focus="Leiomyosarkom ve trofoblastik tümörlerde sağkalım parametreleri",
        narrative=(
            "Pelvik ve gestasyonel patolojilerde hastanın nihai prognozu tümörün hücresel tipine ve yayılım derecesine bağlıdır.\n\n"
            "- **Leiomyosarkomda Prognoz:** Sağkalımı belirleyen en kritik parametre cerrahi evre, tümör boyutu (>5 cm kötü) ve mitotik aktivitedir. Myometrium dışına taşmış veya uzak metastaz yapmış leiomyosarkom olgularında 5 yıllık sağkalım %15-20'lere kadar düşer.\n"
            "- **Gestasyonel Trofoblastik Neoplazilerde (GTN) Prognoz:** FIGO skorlama sistemine göre hastalar düşük risk ve yüksek risk olarak ayrılır. Karaciğer ve beyin metastazı olması, önceki başarısız kemoterapi öyküsü, term gebelikten sonra gelişmesi ve hCG'nin >100.000 mIU/mL olması yüksek risk kriterleridir.\n"
            "- **İmmünolojik Avantaj:** Yüksek riskli metastatik koryokarsinom hastalarında bile paternal antijenlerin varlığı sayesinde yoğun kombinasyon kemoterapileriyle %80-90'ın üzerinde kür elde edilir.\n\n"
            "> [!NOTE]\n"
            "> Leiomyosarkomda en önemli prognostik faktör evre ve boyuttur; gestasyonel trofoblastik tümörlerde ise FIGO risk skoru ve metastaz organıdır."
        ),
        bullets=[
            "Leiomyosarkomda tümör boyutu (>5 cm) ve evre en önemli prognostik faktördür",
            "Leiomyosarkom kemoterapiye dirençlidir; cerrahi eksizyon temeldir",
            "Koryokarsinomda beyin ve karaciğer metastazı yüksek risk kriteridir",
            "Koryokarsinom yüksek riskte dahi kemoterapiyle yüksek kür şansına sahiptir"
        ],
        elements=[
            make_quiz(
                question="Uterin leiomyosarkomlu bir hastada uzun dönem sağkalımı ve kür şansını belirleyen en kritik klinik-patolojik prognostik parametre hangisidir?",
                options=[
                    {"key": "A", "text": "Hastanın ten rengi ve saç rengi", "isCorrect": False, "explanation": "Prognostik parametre değildir."},
                    {"key": "B", "text": "Tümörün cerrahi evresi ve kitlenin boyutu", "isCorrect": True, "explanation": "Doğru. Leiomyosarkomda prognozu belirleyen en temel faktör tanı anındaki cerrahi evre ve tümör boyutudur (>5 cm kötü prognoz)."},
                    {"key": "C", "text": "Serum kalsiyum seviyesi", "isCorrect": False, "explanation": "Miyom veya sarkom prognozunda temel evreleme parametresi değildir."},
                    {"key": "D", "text": "Amniyon zarındaki skuamöz metaplazi miktarı", "isCorrect": False, "explanation": "Amniyon plasental yapıdır; sarkomla ilgisizdir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Uterin leiomyosarkomda klinik gidişi ve hastanın yaşam süresini belirleyen en önemli faktör tanı anındaki cerrahi evre olarak kabul edilir.",
                masked_term="cerrahi evre",
                hint="Tümörün anatomik yayılım derecesi"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Onkolojik Prognoz Faktörleri",
                items=[
                    {"text": "Leiomyosarkomda 5 cm'den büyük kitleler daha kötü klinik prognoza sahiptir.", "isLie": False, "explanation": "Doğru. Boyut majör parametredir."},
                    {"text": "Koryokarsinomda beyin ve karaciğer metastazları yüksek riskli hasta grubunu belirler.", "isLie": False, "explanation": "Doğru. FIGO risk skorunda bu organlar kritik puandır."},
                    {"text": "Metastatik gestasyonel koryokarsinomda paternal antijenler bulunması nedeniyle kemoterapi yanıtı leiomyosarkoma kıyasla kat kat üstündür.", "isLie": False, "explanation": "Doğru. İmmünolojik sinerji koryokarsinomda kürü sağlar."},
                    {"text": "Uterin leiomyosarkom olgularının %100'ü tek doz metotreksat kemoterapisi ile tamamen şifaya kavuşur.", "isLie": True, "explanation": "Tuzak! Metotreksat koryokarsinomun ilacıdır; leiomyosarkom kemoterapiye dirençli, cerrahi ağırlıklı agresif bir sarkomdur."}
                ]
            ),
            make_recall(
                question="Koryokarsinom FIGO prognostik skorlamasında en kötü prognozu işaret eden iki uzak metastaz organı hangisidir?",
                answer="Beyin ve karaciğer metastazlarıdır; intrakraniyal kanama ve hepatik yetmezlik riski nedeniyle yüksek risk kategorisindedir."
            )
        ]
    ))

    # Slide 70 - Checkpoint 7
    slides.append(make_slide(
        slide_num=70,
        title="[TEKRAR SAYFASI - CHECKPOINT 7] Myometrium Patolojisi ve İleri Ayırıcı Tanı",
        subtitle="Bölüm 7 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Miyom varyantları, STUMP, karsinosarkom, p57 belirteci ve prognoz özeti",
        narrative=(
            "Bu tekrar sayfası, 61-69. adımlarda işlenen Myometrium Düz Kas Varyantları ve İleri Trofoblastik Patoloji kazanımlarını konsolide etmek amacıyla hazırlanmıştır.\n\n"
            "- **Miyom Varyantları ve STUMP:** Sellüler ve atipik (bizar) leiomyomlar belirgin hücresel değişikliklere rağmen nekroz ve yüksek mitoz içermedikleri için selimdir. Sınırda kalan ara formlar STUMP olarak adlandırılır ve izlenir. Uterus karsinosarkomu (MMMT) bifazik bir karsinom türevidir.\n"
            "- **Genetik ve İmmün Belirteçler:** Komplet mol diploidtir ve maternal p57KIP2 negatiftir; parsiyel mol triploidtir ve p57 pozitiftir. Koryokarsinom anöploidtir ve paternal antijen taşır.\n"
            "- **Dejenerasyon ve Metastaz:** İskemik nekroza granülasyon dokusu eşlik ederken, sarkom nekrozu anidir. İnvaziv molün akciğer villusları emboliktir ve regrese olabilir; koryokarsinom akciğer metastazları ise yıkıcıdır ve %50 oranında görülür.\n"
            "- **Endokrin Etki:** Leiomyom östrojenle büyür; aşırı hCG overlerde bilateral teka lutein kistleri yapabilir.\n\n"
            "> [!NOTE]\n"
            "> Bizar atipiye rağmen nekroz yoksa bizar miyomdur; p57 negatifse komplet moldür; karsinosarkom bifaziktir; aşırı hCG overde teka lutein kistleri üretir."
        ),
        bullets=[
            "Atipik bizar miyom: Sitolojik atipi vardır fakat nekroz ve yüksek mitoz yoktur (selim)",
            "STUMP: Kriterlerin sınırda olduğu, izlem gerektiren belirsiz düz kas neoplazmıdır",
            "p57KIP2: Komplet molde negatif (maternal alel yok), parsiyelde pozitiftir",
            "Karsinosarkom (MMMT): Karsinom kökenli bifazik epitelyal-mezenkimal habis tümördür",
            "Aşırı hCG overlerde bilateral teka lutein kistleri uyarır; kordonda 2 arter 1 ven vardır"
        ],
        elements=[
            make_quiz(
                question="Myometrium düz kas lezyonları ve trofoblastik patolojilerle ilgili aşağıdaki ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "Atipik (bizar) leiomyom koagülatif nekroz ve 20 mitoz/10 BÜA içerdiği için kesin malign kabul edilir.", "isCorrect": False, "explanation": "Yanlış. Nekroz ve yüksek mitoz bizar miyomda bulunmaz; bulunursa leiomyosarkom olur."},
                    {"key": "B", "text": "p57KIP2 ekspresyonu komplet molde pozitif, parsiyel molde negatiftir.", "isCorrect": False, "explanation": "Yanlış. Tam tersi; komplet molde maternal alel olmadığı için p57 negatiftir."},
                    {"key": "C", "text": "Atipik bizar leiomyom belirgin pleomorfizme rağmen nekroz ve yüksek mitoz içermez; p57 ise komplet molde negatiftir.", "isCorrect": True, "explanation": "Doğru. Her iki önerme de patoloji ayırıcı tanısının altın kuralıdır."},
                    {"key": "D", "text": "STUMP tanısı alan hastalar kesin selim kabul edilip taburcu edilir, takibe gerek yoktur.", "isCorrect": False, "explanation": "Yanlış. STUMP olası geç nüks ve metastaz nedeniyle onkolojik takip gerektirir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Maternal alel taşımayan komplet mol hidatiform olgularında sitotrofoblast hücrelerinde p57KIP2 immünohistokimyasal boyanması negatiftir.",
                masked_term="p57KIP2",
                hint="Maternal ekspresyon gösteren ayırıcı tanı belirteci"
            ),
            make_table(
                title="Bölüm 7 İleri Patoloji Ayırıcı Tanı Özeti",
                headers=["Antite", "Karakteristik Ayırıcı Özellik", "Klinik / Onkolojik Davranış"],
                rows=[
                    [
                        {"text": "Atipik (Bizar) Leiomyom", "isMasked": False},
                        {"text": "Atipi var; nekroz ve yüksek mitoz yok", "isMasked": True, "hint": "Sitolojik pleomorfizme rağmen selim kriterler"},
                        {"text": "Tamamen selim seyir", "isMasked": False}
                    ],
                    [
                        {"text": "Karsinosarkom (MMMT)", "isMasked": False},
                        {"text": "Bifazik karsinom ve sarkom alanları", "isMasked": True, "hint": "İki farklı malign doku tipi birlikteliği"},
                        {"text": "Oldukça agresif; lenfatik ve peritoneal yayılım", "isMasked": False}
                    ],
                    [
                        {"text": "Komplet Mol Hidatiform", "isMasked": False},
                        {"text": "p57KIP2 negatif immün profil", "isMasked": True, "hint": "Maternal gen ekspresyonunun bulunmaması"},
                        {"text": "%10 invaziv mol, %2-3 koryokarsinom riski", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 7 Kontrol Önermeleri",
                items=[
                    {"text": "STUMP, kesin benign veya malign olarak adlandırılamayan ara kategoridir.", "isLie": False, "explanation": "Doğru. Sınırda düz kas neoplazmıdır."},
                    {"text": "Uterus karsinosarkomu saf mezenkimal bir sarkom olmayıp epitelyal karsinomdan türer.", "isLie": False, "explanation": "Doğru. Karsinom kökenli bifazik tümördür."},
                    {"text": "Komplet molde maternal genom varlığı nedeniyle p57KIP2 boyaması diffüz kuvvetli pozitiftir.", "isLie": True, "explanation": "Tuzak! Komplet molde maternal genom kayıptır; bu nedenle p57KIP2 boyanması negatiftir."},
                    {"text": "Molar gebelikteki aşırı hCG overlerde bilateral teka lutein kistlerini tetikleyebilir.", "isLie": False, "explanation": "Doğru. Hiperreaksiyo luteinalis tablosudur."}
                ]
            ),
            make_recall(
                question="Checkpoint 7: Komplet mol ile parsiyel molü patoloji laboratuvarında ayırt eden en kesin immünohistokimyasal boya hangisidir ve komplet molde boyanma nasıldır?",
                answer="p57KIP2 boyasıdır; komplet molde maternal alel bulunmadığı için boyanma tamamen negatiftir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=7
    ))
    
    return slides
