"""
Deck 54 - Section 1: Leiomyom Biyolojisi ve Epidemiyolojisi (Slayt 1-10)
Slayt 10: Checkpoint 1
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide, make_quiz, make_cloze, make_table, make_chain,
    make_recall, make_spot_the_lie, make_slider, make_swipe, make_venn, make_branching
)

def get_sec1_slides():
    slides = []
    
    # Slide 1
    slides.append(make_slide(
        slide_num=1,
        title="Leiomyom: Giriş ve Epidemiyolojik Önemi",
        subtitle="Kadın genital sisteminin en sık benign neoplazmı",
        clinical_focus="Leiomyom prevalansı ve demografik yatkınlıklar",
        narrative=(
            "Leiomyom, myometriumdaki düz kas hücrelerinden köken alan selim karakterli bir mezenkimal neoplazmdır. "
            "Kadın genital traktusunda açık ara en sık izlenen benign tümördür ve reprodüktif çağdaki kadınların yaklaşık %30-50'sinde saptanır.\n\n"
            "- **Irksal ve Yaş Dağılımı:** Özellikle siyah ırka mensup kadınlarda beyaz ırka oranla hem daha erken yaşlarda başlar hem de 2-3 kat daha sık görülür.\n"
            "- **Klinik Yansıma:** Birçok olgu asemptomatik seyretse de uterus kavitesini veya komşu pelvik organları etkileyerek anormal kanamalara ve bası bulgularına yol açabilir.\n"
            "- **Malignite Potansiyeli:** Tamamen benign karakterdedir ve klinik takipleri bu selim doğa göz önüne alınarak planlanır.\n\n"
            "> [!NOTE]\n"
            "> Aktif doğurganlık döneminde her iki ya da üç kadından birinde mikroskobik veya makroskobik leiomyom odakları mevcuttur."
        ),
        bullets=[
            "Myometrium düz kasından köken alır",
            "Kadınlarda en sık görülen benign neoplazmdır",
            "Reprodüktif dönemde %30-50 sıklıkta izlenir",
            "Siyah ırkta prevalansı ve şiddeti belirgin yüksektir"
        ],
        elements=[
            make_quiz(
                question="Kadın genital sisteminde reprodüktif dönemde en sık saptanan benign tümör ve kaynaklandığı doku katmanı aşağıdakilerden hangisidir?",
                options=[
                    {"key": "A", "text": "Endometrial polip — Endometrium bazal tabakası", "isCorrect": False, "explanation": "Endometrial polip sık görülmekle birlikte myometrium kaynaklı leiomyom kadın genital traktusunun açık ara en sık benign tümörüdür."},
                    {"key": "B", "text": "Leiomyom — Myometrium düz kas tabakası", "isCorrect": True, "explanation": "Doğru. Leiomyomlar myometriumdaki düz kas hücrelerinden köken alır ve reprodüktif çağdaki kadınların %30-50'sinde saptanan en yaygın selim tümördür."},
                    {"key": "C", "text": "Adenomyom — Endometrium fonksiyonel tabakası", "isCorrect": False, "explanation": "Adenomyozis ektopik endometrial gland ve stromanın myometriuma invazyonudur; saf düz kas neoplazmı değildir."},
                    {"key": "D", "text": "Leiomyosarkom — Myometrium vasküler endoteli", "isCorrect": False, "explanation": "Leiomyosarkom nadir görülen, de novo gelişen malign bir tümördür; en sık benign lezyon leiomyomdur."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Reprodüktif dönemdeki kadınların yaklaşık yüzde 30-50 kadarında izlenen ve kadınlarda en sık görülen benign tümör leiomyom olarak tanımlanır.",
                masked_term="yüzde 30-50",
                hint="Doğurganlık çağındaki kadınların üçte biri ile yarısı arasındaki sıklık oranı"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Leiomyom Epidemiyolojisi",
                items=[
                    {"text": "Leiomyomlar kadın genital sisteminde en sık saptanan benign neoplazmdır.", "isLie": False, "explanation": "Doğru. Tüm jinekolojik benign tümörler arasında en yüksek prevalansa sahiptir."},
                    {"text": "Siyah ırktaki kadınlarda beyaz ırka kıyasla görülme insidansı belirgin olarak daha yüksektir.", "isLie": False, "explanation": "Doğru. Epidemiyolojik çalışmalarda siyah ırkta hem insidansın hem de semptom ağırlığının daha fazla olduğu kanıtlanmıştır."},
                    {"text": "Reprodüktif dönem kadınlarının yaklaşık %30-50'sinde mikroskobik veya makroskobik leiomyom bulunur.", "isLie": False, "explanation": "Doğru. Otopsi ve histerektomi serilerinde reprodüktif çağda %50'ye varan oranlar bildirilmektedir."},
                    {"text": "Leiomyomlar en sık prepubertal adolesan kız çocuklarında hormon bağımsız olarak ortaya çıkar.", "isLie": True, "explanation": "Tuzak! Leiomyomlar östrojen bağımlı neoplazmlar olup menarş öncesi prepubertal dönemde neredeyse hiç görülmez; pik insidansı aktif reprodüktif çağdadır."}
                ]
            ),
            make_recall(
                question="Leiomyomların kadın genital traktusundaki epidemiyolojik sıklık düzeyi ve etnik yatkınlığı nedir?",
                answer="Reprodüktif çağdaki kadınların %30-50'sinde izlenir ve siyah ırkta beyaz ırka göre belirgin olarak daha yüksek sıklıkta saptanır."
            )
        ]
    ))
    
    # Slide 2
    slides.append(make_slide(
        slide_num=2,
        title="Leiomyom: Sitogenetik ve Monoklonalite",
        subtitle="6. ve 12. kromozom translokasyonları ve klonal gelişim",
        clinical_focus="Leiomyomun moleküler temeli ve klonal ekspansiyon",
        narrative=(
            "Leiomyomlar monoklonal neoplazmlardır; yani her bir miyom odağı tek bir düz kas hücresinin genetik mutasyon geçirerek klonal çoğalması sonucu ortaya çıkar. "
            "Aynı uterusta birden fazla miyom bulunması metastaz veya multifokaliteyi değil, birbirinden bağımsız gelişen ayrı monoklonal transformasyonları yansıtır.\n\n"
            "- **Tekrarlayan Sitogenetik Bozukluklar:** Miyom dokularının yaklaşık %40-50'sinde spesifik sitogenetik anomaliler gösterilmiştir. En sık saptananlar 12q14-15 bölgesini (HMGA2 geni) ve 6p21 bölgesini (HMGA1 geni) içeren yeniden düzenlenmelerdir.\n"
            "- **Diğer Benign Tümörlerle Ortaklık:** Benzer kromozom 6 ve 12 anomalileri endometrial poliplerde ve lipomlarda da izlenmekte olup mezenkimal proliferasyon sinyallerini regüle eder.\n"
            "- **Klon Bağımsızlığı:** Tek bir hastadaki farklı miyom nodülleri farklı kromozomal anomalilere sahip olabilir.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyomların klonal analizi (G6PD izoenzim çalışmaları) her bir tümör nodülünün bağımsız bir tek öncül hücreden köken aldığını kesin olarak göstermiştir."
        ),
        bullets=[
            "Her nodül bağımsız monoklonal proliferasyondur",
            "Kromozom 6 ve 12 yeniden düzenlenmeleri karakteristiktir",
            "Endometrial polip ve lipomlarla ortak sitogenetik yolakları paylaşır",
            "Multiple miyom varlığı bağımsız primer klonları temsil eder"
        ],
        elements=[
            make_quiz(
                question="Leiomyom patogenezinde lipomlar ve endometrial poliplerle ortak olarak sıkça saptanan karakteristik sitogenetik bozukluk çifti hangisidir?",
                options=[
                    {"key": "A", "text": "Kromozom 1 ve 3 delesyonları", "isCorrect": False, "explanation": "1p ve 3p delesyonları renal karsinomlar veya nöroendokrin lezyonlarda görülür; leiomyomda tipik değildir."},
                    {"key": "B", "text": "Kromozom 7 ve 17 trizomileri", "isCorrect": False, "explanation": "7 ve 17 anöploidileri papiller böbrek tümörlerinde karakteristiktir."},
                    {"key": "C", "text": "Kromozom 6 ve 12 yeniden düzenlenmeleri", "isCorrect": True, "explanation": "Doğru. Leiomyomlarda, lipomlarda ve endometrial poliplerde 6. ve 12. kromozom translokasyonları (HMGA gen ailesi lokusları) karakteristik monoklonal anomalilerdir."},
                    {"key": "D", "text": "Kromozom 9 ve 22 translokasyonu (Philadelphia)", "isCorrect": False, "explanation": "t(9;22) BCR-ABL Kronik Myeloid Lösemi (KML) için patognomoniktir; mezenkimal benign uterin tümörlerle ilgisi yoktur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Endometrial polip ve lipomlarda da rastlanan 6. ve 12. kromozom yeniden düzenlenmelerini içeren sitogenetik anomaliler leiomyom gelişiminde monoklonalite mekanizmasını gösterir.",
                masked_term="6. ve 12. kromozom",
                hint="HMGA gen lokuslarının bulunduğu iki genetik yapı numarası"
            ),
            make_table(
                title="Leiomyom Sitogenetik ve Klonalite Parametreleri",
                headers=["Moleküler Parametre", "Gözlenen Özellik", "Klinik & Biyolojik Anlamı"],
                rows=[
                    [
                        {"text": "Klonal Yapı", "isMasked": False},
                        {"text": "Monoklonal ekspansiyon", "isMasked": True, "hint": "Tek bir kök düz kas hücresinden türeme"},
                        {"text": "Her nodül bağımsız bir hücreden türer", "isMasked": False}
                    ],
                    [
                        {"text": "Sık Kromozomal Anomali", "isMasked": False},
                        {"text": "Kromozom 6 ve 12 translokasyonu", "isMasked": True, "hint": "HMGA ailesi lokusları"},
                        {"text": "Polipler ve lipomlarla ortak mezenkimal yolak", "isMasked": False}
                    ],
                    [
                        {"text": "Multiple Nodül Biyolojisi", "isMasked": False},
                        {"text": "Bağımsız primer odaklar", "isMasked": False},
                        {"text": "Metastaz veya yayılım değil, ayrı mutasyonlardır", "isMasked": False}
                    ]
                ]
            ),
            make_chain(
                "Leiomyom Klonal Patogenez Zinciri",
                [
                    "1. Somatik Mutasyon: Myometriumdaki tek bir düz kas öncül hücresinde 6 veya 12. kromozom yeniden düzenlenmesi gerçekleşir.",
                    "2. Monoklonal Proliferasyon: Mutasyona uğrayan tek hücre diğer myositlerden bağımsız olarak çoğalarak klonal bir nodül oluşturur.",
                    "3. Matriks ve Doku Şekillenmesi: Klonal hücreler bol miktarda kollajenöz ekstrasellüler matriks sentezleyerek girdapsı düz kas demetlerini meydana getirir."
                ]
            ),
            make_recall(
                question="Bir uterusta birden fazla leiomyom izlenmesi metastaz mıdır, monoklonalite açısından nasıl açıklanır?",
                answer="Metastaz değildir; her bir miyom odağı birbirinden bağımsız hücrelerin ayrı ayrı monoklonal proliferasyonu ile gelişen primer selim lezyonlardır."
            )
        ]
    ))

    # Slide 3
    slides.append(make_slide(
        slide_num=3,
        title="Leiomyom: Hormonal Bağımlılık ve Dinamikler",
        subtitle="Östrojen-progesteron stimülasyonu ve postmenopozal regresyon",
        clinical_focus="Leiomyom boyut değişimlerinde hormonların belirleyici rolü",
        narrative=(
            "Leiomyomlar hormona son derece duyarlı neoplazmlardır. Büyümeleri ve hacimsel genişlemeleri başta östrojen olmak üzere over hormonları tarafından regüle edilir. "
            "Normal myometriuma kıyasla leiomyom dokusunda östrojen ve progesteron reseptör yoğunluğu belirgin olarak daha yüksektir.\n\n"
            "- **Reprodüktif Çağ ve Gebelik:** Gebelik sürecinde ve yüksek östrojenli durumlarda (oral kontraseptif kullanımı, anovulatuar sikluslar) hücresel hipertrofi ve mitoz artışıyla hızla büyüyebilirler.\n"
            "- **Postmenopozal Regresyon:** Menopozla birlikte over kaynaklı östrojen ve progesteron üretiminin sonlanması, leiomyomlarda atrofiye, kollajen hyalinizasyonuna ve hacimce küçülmeye (regresyona) yol açar.\n"
            "- **Postmenopozda Büyüme Alarmı:** Postmenopozal bir kadında önceden var olan veya yeni saptanan bir miyom kitlesinin hızla büyümesi kesinlikle normal regresyonla uyuşmaz ve akla sarkomu (leiomyosarkom) getirmelidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyomlar menopoz sonrasında fizyolojik olarak küçülür; postmenopozda büyüyen pelvik düz kas kitleleri malignite şüphesiyle tetkik edilmelidir."
        ),
        bullets=[
            "Östrojen ve progesteron reseptör yoğunluğu yüksektir",
            "Aktif reprodüktif dönemde ve gebelikte büyüme eğilimindedir",
            "Postmenopozal dönemde hormon çekilmesiyle küçülür (regrese olur)",
            "Postmenopozda büyüme malignite (leiomyosarkom) şüphesi doğurur"
        ],
        elements=[
            make_quiz(
                question="Leiomyomların hormonal yanıtı ve postmenopozal dönemdeki seyri ile ilgili aşağıdaki ifadelerden hangisi fizyopatolojik olarak doğrudur?",
                options=[
                    {"key": "A", "text": "Postmenopozal dönemde over östrojeninin çekilmesine bağlı olarak atrofiye uğrar ve küçülürler.", "isCorrect": True, "explanation": "Doğru. Leiomyomlar östrojen bağımlıdır; menopoz sonrası hormonal desteğin kesilmesiyle belirgin şekilde küçülürler."},
                    {"key": "B", "text": "Postmenopozal dönemde gonadotropinlerin (FSH/LH) artması nedeniyle hızla büyüme gösterirler.", "isCorrect": False, "explanation": "Yanlış. Büyümeyi sağlayan over steroidleridir (östrojen/progesteron); menopozda FSH artsa da over steroidleri düştüğü için miyomlar küçülür."},
                    {"key": "C", "text": "Gebelik sürecinde hormon konsantrasyonları artsa da leiomyomlar büyümez, boyutları sabit kalır.", "isCorrect": False, "explanation": "Yanlış. Gebelikteki yüksek östrojen ve progesteron miyom boyutlarında belirgin artışa yol açabilir."},
                    {"key": "D", "text": "Leiomyom dokusunda östrojen reseptörleri bulunmaz; büyüme tamamen paratiroid hormona bağlıdır.", "isCorrect": False, "explanation": "Yanlış. Leiomyom dokusunda östrojen ve progesteron reseptör konsantrasyonu normal myometriumdan bile daha yüksektir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Östrojen ve oral kontraseptif stimülasyonu ile büyüyen leiomyomlar, hormonal çekilmenin gerçekleştiği postmenapozal dönemde küçülürler.",
                masked_term="postmenapozal dönemde küçülürler",
                hint="Menopoz sonrası östrojenin kesilmesiyle tümör hacmindeki değişim yönü"
            ),
            make_slider(
                left_title="Reprodüktif Dönemde Leiomyom",
                right_title="Postmenopozal Dönemde Leiomyom",
                left_points=[
                    "Yüksek östrojen ve progesteron stimülasyonu mevcuttur",
                    "Düz kas hücrelerinde aktif proliferasyon ve boyut artışı izlenir",
                    "Gebelikte ve hormon replasmanında büyüme pik yapar"
                ],
                right_points=[
                    "Over steroidlerinin kesilmesiyle hormonal stimülasyon biter",
                    "Düz kas hücrelerinde atrofi ve hücresel hacim kaybı izlenir",
                    "Tümör nodülleri belirgin şekilde büzüşür ve küçülür"
                ]
            ),
            make_recall(
                question="Postmenopozal dönemde bir kadında takip edilen bir uterin myomun küçülmek yerine hızla büyümesi neyi düşündürür?",
                answer="Malign transformasyon veya de novo gelişen leiomyosarkom şüphesini doğurur; acil histopatolojik inceleme gerektirir."
            )
        ]
    ))

    # Slide 4
    slides.append(make_slide(
        slide_num=4,
        title="Leiomyom: Makroskobik Özellikler",
        subtitle="Keskin sınırlı, gri-beyaz, girdapsı kesit yüzeyi",
        clinical_focus="Leiomyomun tipik cerrahi ve patoloji makroskopi bulguları",
        narrative=(
            "Leiomyomların makroskobik görünümü patoloji pratiğinde en kolay tanınan morfolojilerden biridir. Çevre myometrium dokusundan belirgin ve keskin bir sınırla ayrılırlar; gerçek bir fibröz kapsülleri olmasa da çevre kas dokusunu iterek 'psödokapsül' oluştururlar.\n\n"
            "- **Renk ve Kıvam:** Tipik olarak sert-elastik kıvamda ve homojen gri-beyaz renktedir.\n"
            "- **Kesit Yüzeyi:** Bıçakla kesildiğinde lezyon çevre myometrium seviyesinden dışarı doğru kabarır. Kesit yüzeyinde birbirinin etrafında dönen kas liflerinin oluşturduğu patognomonik **girdapsı (whorled)** görünüm izlenir.\n"
            "- **Çok Odaklılık ve Boyut:** Çoğu zaman aynı uterusta birden fazla (multiple) nodül şeklinde yer alırlar. Boyutları birkaç milimetrelik küçük intramural tohumlardan, tüm batını dolduran 15-20 cm'lik dev kitlelere kadar değişkenlik gösterir.\n\n"
            "> [!NOTE]\n"
            "> Makroskopide keskin sınır ve gri-beyaz girdapsı desen, malign sarkomun yumuşak-nekrotik yapısından ayırt edici en temel morfolojik özelliktir."
        ),
        bullets=[
            "Keskin sınırlı, kapsülsüz fakat psödokapsüllü nodüllerdir",
            "Homojen gri-beyaz renkli ve sert-elastik kıvamdadır",
            "Kesit yüzünde karakteristik girdapsı (whorled) patern izlenir",
            "Tek olabilir ancak vakaların çoğunda multiple nodüller halindedir"
        ],
        elements=[
            make_quiz(
                question="Uterin bir kitlenin makroskobik incelemesinde çevre myometriumdan keskin sınırlı, sert-elastik kıvamda, gri-beyaz renkli ve kesit yüzü belirgin girdapsı (whorled) desende izlenmesi öncelikle hangi antiteyi destekler?",
                options=[
                    {"key": "A", "text": "Leiomyosarkom", "isCorrect": False, "explanation": "Leiomyosarkomlar yumuşak kıvamlı, sınırları belirsiz, yaygın kanamalı ve nekrotik kitlelerdir; sert-elastik girdapsı yapı göstermezler."},
                    {"key": "B", "text": "Endometrial stromal sarkom", "isCorrect": False, "explanation": "Endometrial stromal sarkom miyometriumu solucan benzeri (worm-like) infiltratif kordonlarla istila eder; keskin sınırlı girdapsı nodül yapmaz."},
                    {"key": "C", "text": "Leiomyom", "isCorrect": True, "explanation": "Doğru. Keskin sınır, gri-beyaz renk ve kesit yüzündeki girdapsı desen leiomyomun klasik patognomonik makroskobik bulgularıdır."},
                    {"key": "D", "text": "Koryokarsinom", "isCorrect": False, "explanation": "Koryokarsinom aşırı kanamalı, nekrotik ve bordo renkli bir kitle olup villus veya düz kas lifleri içermez."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Keskin sınırlı ve gri beyaz renkli olan leiomyomların makroskobik kesit yüzleri karakteristik olarak girdapsı şekillidir.",
                masked_term="girdapsı",
                hint="Düz kas liflerinin birbirini çevreleyerek oluşturduğu helezonik-whorled desen"
            ),
            make_table(
                title="Leiomyom Makroskopi Parametreleri",
                headers=["Özellik", "Makroskobik Bulgu", "Patolojik İpucu"],
                rows=[
                    [
                        {"text": "Dış Sınırlar", "isMasked": False},
                        {"text": "Keskin sınırlı psödokapsül", "isMasked": True, "hint": "Çevre dokuyu iterek oluşan yalancı hat"},
                        {"text": "Cerrahi enükleasyona imkan tanır", "isMasked": False}
                    ],
                    [
                        {"text": "Kesit Deseni", "isMasked": False},
                        {"text": "Girdapsı (whorled) patern", "isMasked": True, "hint": "Dairesel helezonik demet dizilimi"},
                        {"text": "Düz kas demetlerinin yönelimini yansıtır", "isMasked": False}
                    ],
                    [
                        {"text": "Renk ve Kıvam", "isMasked": False},
                        {"text": "Gri-beyaz ve sert-elastik", "isMasked": False},
                        {"text": "Nekroz ve kanama içermeyen selim matriks", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Leiomyomun kesit yüzeyi incelendiğinde patoloğun gördüğü en tipik mimari patern nedir?",
                answer="Birbiri etrafında helezonik dönen kas liflerinin oluşturduğu gri-beyaz renkli 'girdapsı' (whorled) desendir."
            )
        ]
    ))

    # Slide 5
    slides.append(make_slide(
        slide_num=5,
        title="Leiomyom: Anatomik Yerleşim Tipleri",
        subtitle="Submukoz, intramural ve subseröz dağılım",
        clinical_focus="Miyomun uterus duvarındaki derinliğine göre lokalizasyon sınıflaması",
        narrative=(
            "Leiomyomlar myometrium tabakası içindeki yerleşimlerine ve yönelimlerine göre üç ana anatomik grupta incelenir. Miyomun yerleşimi oluşturacağı klinik belirtileri doğrudan belirler.\n\n"
            "- **İntramural Leiomyom:** Myometriumun kas kitlesi içinde gömülü olan tiptir; en sık izlenen lokalizasyondur. Uterusun diffüz olarak büyümesine ve globüler hale gelmesine neden olur.\n"
            "- **Submukoz Leiomyom:** Endometrium tabakasının hemen altında yerleşen ve uterus kavitesi içine doğru protrüde olan tiptir. En az görülen (%5-10) fakat yüzeyel damarlanmayı bozduğu ve kaviteyi genişlettiği için en gürültülü kanamalara yol açan formdur.\n"
            "- **Subseröz Leiomyom:** Uterusun peritoneal dış yüzeyine doğru büyüyen formdur. Bazen ince bir sapla uterusa tutunabilir (pediküllü subseröz miyom) ve çevre organlara bası yapabilir.\n\n"
            "> [!NOTE]\n"
            "> Pediküllü subseröz miyomlar kendi etrafında dönerek akut torsiyon ve hemorajik enfarktüs tablosuna yol açabilir."
        ),
        bullets=[
            "İntramural tip en sık görülen yerleşimdir",
            "Submukoz tip kavite içine büyür ve en fazla kanama yapan formdur",
            "Subseröz tip periton altına yerleşir ve pelvik bası semptomları üretir",
            "Pediküllü formlar torsiyon riski taşır"
        ],
        elements=[
            make_quiz(
                question="Uterin kavite içine doğru çıkıntı yaparak endometrium mukozasını bozan ve en sık şiddetli menorajiye yol açan leiomyom tipi hangisidir?",
                options=[
                    {"key": "A", "text": "Subseröz leiomyom", "isCorrect": False, "explanation": "Subseröz miyomlar peritona doğru büyür; kanamadan ziyade mesane ve rektum basısı oluştururlar."},
                    {"key": "B", "text": "Submukoz leiomyom", "isCorrect": True, "explanation": "Doğru. Submukoz leiomyomlar endometrial kaviteye komşudur; endometrial yüzeyi artırarak ve damarları gererek ciddi menoraji ve metrorajiye sebep olurlar."},
                    {"key": "C", "text": "Parazitik leiomyom", "isCorrect": False, "explanation": "Parazitik miyomlar uterustan kopup omentum veya mezenterden beslenen nadir ekstrauterin lezyonlardır."},
                    {"key": "D", "text": "Servikal intramural leiomyom", "isCorrect": False, "explanation": "Servikal intramural miyomlar doğum kanalını tıkayabilir ancak kaviter kanamanın birincil kaynağı submukoz yerleşimdir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Uterus myometriumundaki anatomik yerleşimlerine göre leiomyomlar submukoz, intramural veya subseröz olmak üzere üç ana grupta sınıflandırılır.",
                masked_term="submukoz, intramural veya subseröz",
                hint="İç kavite, orta kas duvarı ve dış periton altı anatomik lokalizasyonları"
            ),
            make_venn(
                title="Submukoz vs Subseröz Leiomyom Karşılaştırması",
                label_a="Submukoz Leiomyom",
                label_b="Subseröz Leiomyom",
                items=[
                    {"criterion": "Endometrium kavitesi altına yerleşip şiddetli menoraji oluşturma", "correct": "A", "explanation": "Submukoz miyomlar kavite içine doğru büyür ve yoğun kanamaya yol açar."},
                    {"criterion": "Peritoneal örtü altına doğru dışa doğru büyüme", "correct": "B", "explanation": "Subseröz miyomlar uterus dış yüzeyine doğru gelişir."},
                    {"criterion": "Saplı (pediküllü) hale gelip torsiyone olabilme potansiyeli", "correct": "B", "explanation": "Subseröz pediküllü lezyonlar pelvik kavitede dönerek akut karın yapabilir."},
                    {"criterion": "Myometriumdaki düz kas hücrelerinin monoklonal neoplazmı olma", "correct": "both", "explanation": "Her iki tip de aynı selim histogenetik kökene ve 6/12 kromozom mutasyonlarına sahiptir."}
                ]
            ),
            make_recall(
                question="Boyutu küçük olmasına rağmen hastada en erken ve en şiddetli menoraji tablosunu oluşturan leiomyom yerleşimi hangisidir?",
                answer="Submukoz leiomyomdur; endometrial kaviteyi deforme ederek yüzey damarlanmasını bozar."
            )
        ]
    ))

    # Slide 6
    slides.append(make_slide(
        slide_num=6,
        title="Leiomyom: Parazitik Miyomlar ve Vasküler Sıyrılma",
        subtitle="Omentum veya çevre organlardan beslenen ekstrauterin lezyonlar",
        clinical_focus="Pediküllü subseröz miyomların uterus dışına göç mekanizması",
        narrative=(
            "Pediküllü subseröz leiomyomlar bazen çevre anatomik yapılara (özellikle omentum majus, mezenter veya pelvik periton) yapışarak bu organlardan yeni damar ağları (neovaskülarizasyon) devşirirler.\n\n"
            "- **Vasküler Sıyrılma ve Beslenme Göçü:** Zamanla tümörün uterusa bağlanan orijinal sapı mekanik traksiyon, torsiyon veya atrofi sonucu incelerek kopar. Uterusla bağlantısı tamamen kesilen bu tümör, kan akımını tümüyle yapıştığı ekstrauterin organdan sağlamaya başlar.\n"
            "- **Parazitik Leiomyom Tanımı:** Uterusla hiçbir doğrudan anatomik teması kalmayan, batın içi başka bir vasküler yataktan beslenen bu selim kitlelere **parazitik leiomyom** adı verilir.\n"
            "- **Ayırıcı Tanı Güçlüğü:** Cerrahi veya radyolojik değerlendirmede over kitleleri veya mezenterik stromal tümörlerle (GİST) karışabilir; ancak histolojisi tamamen selim düz kas liflerinden ibarettir.\n\n"
            "> [!NOTE]\n"
            "> Parazitik leiomyomlar malign bir implant veya metastaz değildir; mekanik olarak uterustan ayrılmış selim bir vasküler ototransplanttır."
        ),
        bullets=[
            "Pediküllü subseröz miyomun çevre dokuya yapışmasıyla başlar",
            "Omentum veya mezenterden ikincil damarlanma kazanır",
            "Uterus sapı kopunca tamamen ekstrauterin bağımsız kitleye dönüşür",
            "Malign metastaz değil, mekanik ve vasküler bir fenomenidir"
        ],
        elements=[
            make_quiz(
                question="Subseröz bir leiomyomun omentum veya mezenter peritonuna yapışıp ikincil damar ağı geliştirmesi ve ardından uterusla bağlantısının kopması sonucu oluşan antiteye ne ad verilir?",
                options=[
                    {"key": "A", "text": "İnvaziv leiomyom", "isCorrect": False, "explanation": "İnvaziv terimi malignite veya trofoblastik invazyon için kullanılır; miyomda invaziv tip yoktur."},
                    {"key": "B", "text": "Leiomyosarkom metastazı", "isCorrect": False, "explanation": "Miyom sarkoma dönüşmez; bu durum selim bir miyomun vasküler beslenme göçüdür."},
                    {"key": "C", "text": "Parazitik leiomyom", "isCorrect": True, "explanation": "Doğru. Uterusla bağlantısı kopup omentum veya diğer pelvik dokulardan beslenen miyomlara parazitik leiomyom denir."},
                    {"key": "D", "text": "Adenomyozis odağı", "isCorrect": False, "explanation": "Adenomyozis myometrium içi endometrial dokudur; parazitik kitleyle ilgisi yoktur."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Uterusla olan pedikül bağlantısını kaybederek omentum veya mezenterden beslenen ve çevre organlara yapışık kalan kitlelere parazitik leiomyom adı verilir.",
                masked_term="parazitik leiomyom",
                hint="Ekstrauterin kan akımıyla beslenen göç etmiş selim miyom formu"
            ),
            make_chain(
                "Parazitik Leiomyom Oluşum Basamakları",
                [
                    "1. Subseröz Pediküllenme: Subseröz yerleşimli leiomyom büyüdükçe periton boşluğuna doğru uzanır ve ince bir sapla uterusa bağlı kalır.",
                    "2. Komşu Dokuya Yapışma: Hareketli kitle omentum veya mezenter gibi komşu damarlı periton yapılarına yapışarak neovaskülarizasyon uyarır.",
                    "3. Pedikül Torsiyonu ve Ayrılma: Uterusa bağlayan orijinal pedikül atrofiye uğrar veya kopar; lezyon bağımsız parazitik kitle olarak yaşamını sürdürür."
                ]
            ),
            make_recall(
                question="Parazitik leiomyom gelişiminde tümörün uterustan ayrılması bir malign yayılım mıdır?",
                answer="Hayır; mekanik olarak pedikülün kopması ve omentumdan beslenmesiyle oluşan selim bir vasküler adaptasyondur."
            )
        ]
    ))

    # Slide 7
    slides.append(make_slide(
        slide_num=7,
        title="Leiomyom: Klinik Belirtiler ve Komplikasyonlar",
        subtitle="Menoraji, pelvik bası, palpabl kitle ve kısırlık",
        clinical_focus="Leiomyomun semptomatolojisi ve cerrahi endikasyonları",
        narrative=(
            "Leiomyomların önemli bir kısmı asemptomatiktir ve rutin jinekolojik pelvik muayene veya ultrasonda rastlantısal (insidental) olarak tespit edilir. Semptom veren olgularda klinik tablo tümörün sayısına, boyutuna ve lokalizasyonuna dayanır.\n\n"
            "- **En Sık Semptom:** En sık izlenen klinik bulgu, adet kanamasının aşırı miktarda ve uzun sürmesi olarak tanımlanan **menorajidir** (buna adet arası lekelenme tarzında **metroraji** de eşlik edebilir).\n"
            "- **Kitle ve Bası Etkisi:** Özellikle büyük intramural ve subseröz kitleler hastanın karnında palpe edilebilir. Öne doğru büyüyen kitleler mesaneye bası yaparak sık idrara çıkma (pollaküri), arkaya doğru büyüyenler ise rektuma bası yaparak kabızlık (konstipasyon) ve pelvik dolgunluk oluşturur.\n"
            "- **İnfertilite ve Ağrı:** Submukoz miyomlar embriyo implantasyonunu bozarak infertiliteye veya düşüklere yol açabilir. Genellikle ağrısızdır; şiddetli ağrı ancak torsiyon veya kırmızı dejenerasyon varlığında ortaya çıkar.\n\n"
            "> [!IMPORTANT]\n"
            "> Leiomyomun en karakteristik klinik prezentasyonu metrorajinin eşlik ettiği veya etmediği menorajidir; kronik demir eksikliği anemisine yol açabilir."
        ),
        bullets=[
            "En sık klinik bulgu menorajidir (aşırı adet kanaması)",
            "Metroraji (ara kanama) eşlik edebilir",
            "Büyük miyomlar batında palpabl kitle ve bası oluşturur",
            "Mesane basısıyla pollaküri, rektum basısıyla konstipasyon yapabilir"
        ],
        elements=[
            make_quiz(
                question="Semptomatik leiomyomlu bir kadında jinekoloji polikliniğine başvuruda en sık dile getirilen majör klinik şikayet hangisidir?",
                options=[
                    {"key": "A", "text": "Adet kanamalarının aşırı miktarda ve uzun sürmesi (menoraji)", "isCorrect": True, "explanation": "Doğru. Leiomyomların en yaygın klinik prezentasyonu menorajidir; buna bazen metroraji de eşlik eder."},
                    {"key": "B", "text": "Ani başlangıçlı fışkırır tarzda kusma ve sarılık", "isCorrect": False, "explanation": "Gastrointestinal/hepatobiliyer acil tablodur; leiomyomla hiçbir ilişkisi yoktur."},
                    {"key": "C", "text": "Postmenopozal dönemde pürülan akıntı", "isCorrect": False, "explanation": "Pürülan akıntı servisit veya pelvik enfeksiyon belirtisidir; miyomun tipik bulgusu değildir."},
                    {"key": "D", "text": "Her iki overde kistik kitleye bağlı virilizasyon", "isCorrect": False, "explanation": "Virilizasyon androjen salgılayan over tümörlerinde görülür; miyom düz kas kaynaklı selim kitle olup maskülinizasyon yapmaz."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Leiomyomların klinikte en sık izlenen semptomu metrorajinin eşlik ettiği veya etmediği menorajidir.",
                masked_term="menorajidir",
                hint="Adet kanamasının süre ve miktar olarak anormal artışı"
            ),
            make_branching(
                scenario="42 yaşında kadın hasta, son 6 aydır her adet döneminde aşırı kanama (günde 8-10 ped) ve halsizlik yakınmasıyla başvuruyor. Hemoglobin: 8.2 g/dL. Pelvik ultrasonda uterus kavitesini dolduran 4 cm çapında submukoz kitle izleniyor. Bu hastanın kliniğini açıklayan temel mekanizma nedir?",
                options=[
                    {"text": "Submukoz kitle endometrial yüzeyi ve komşu damar ağını bozarak hemostazı engeller ve menorajiye yol açar.", "isCorrect": True, "feedback": "Kesinlikle doğru. Submukoz leiomyomlar endometrium kavitesine bası yaparak yüzey alanını artırır ve aşırı menorajiye neden olur."},
                    {"text": "Miyom kitlesi karaciğerde pıhtılaşma faktörlerinin sentezini doğrudan bloke etmiştir.", "isCorrect": False, "feedback": "Hatalı. Miyom karaciğer protein sentezini etkilemez; kanama tamamen lokal endometrial damar bozukluğuna bağlıdır."},
                    {"text": "Tümör dokusu sistemik olarak fibrinolizisi aktive eden doku faktörü salgılamaktadır.", "isCorrect": False, "feedback": "Yanlış. Selim miyomlar sistemik fibrinoliz yapmaz; menoraji kaviter deformiteye bağlı mekanik bir sorundur."}
                ]
            ),
            make_recall(
                question="Büyük bir leiomyom kitlesinin pelviste öne doğru mesaneye, arkaya doğru rektuma bası yapması hangi iki semptomu üretir?",
                answer="Mesane basısıyla sık idrara çıkma (pollaküri/dizüri), rektum basısıyla konstipasyon (kabızlık) ve pelvik dolgunluk üretir."
            )
        ]
    ))

    # Slide 8
    slides.append(make_slide(
        slide_num=8,
        title="Leiomyom: Dejenerasyon Tipleri",
        subtitle="Hiyalin, kistik, kalsifik ve kırmızı (karneöz) dejenerasyon",
        clinical_focus="Hızlı büyüyen miyomlarda kanlanma yetersizliğine bağlı sekonder değişiklikler",
        narrative=(
            "Leiomyomlar kendi hacimleri hızla genişlediğinde veya kanlanmaları yetersiz kaldığında çeşitli sekonder dejeneratif değişikliklere uğrarlar. Bu değişiklikler biyolojik olarak malignleşme anlamına gelmez.\n\n"
            "- **Hiyalin Dejenerasyon:** En sık izlenen dejenerasyon tipidir. Düz kas hücrelerinin yerini homojen, pembe asellüler eozinofilik kollajenöz bağ dokusu alır.\n"
            "- **Kistik Dejenerasyon:** Hiyalinize alanların likefaksiyona (sıvılaşmaya) uğraması sonucu oluşur; kitle kesitinde kistik boşluklar belirir.\n"
            "- **Kırmızı (Karneöz) Dejenerasyon:** Özellikle gebelik döneminde hızla büyüyen miyomlarda venöz tromboza bağlı gelişen hemorajik enfarktüstür. Kitle kırmızı-kahverengi çiğ et rengini alır; akut karın ağrısı ve lökositoz tablosu oluşturur.\n"
            "- **Kalsifik Dejenerasyon:** Genellikle postmenopozal yaşlı kadınlarda iskemik nekroz alanlarında kalsiyum tuzlarının birikmesiyle (distrofik kalsifikasyon) oluşur; pelvik grafilerde taş benzeri radyoopak dansiteler verir.\n\n"
            "> [!NOTE]\n"
            "> Gebelikte ani başlayan şiddetli pelvik ağrının en sık benign patolojik nedenlerinden biri leiomyomun kırmızı (karneöz) dejenerasyonudur."
        ),
        bullets=[
            "Hiyalin dejenerasyon en sık izlenen formdur",
            "Kistik dejenerasyon likefaksiyon sonucu oluşur",
            "Kırmızı (karneöz) dejenerasyon gebelikte venöz oklüzyonla görülür",
            "Kalsifikasyon postmenopozda distrofik kireçlenmeyle gelişir"
        ],
        elements=[
            make_quiz(
                question="Gebelikte hızla büyüyen bir uterin leiomyomda venöz tromboz ve kanlanma yetersizliği sonucu gelişen, şiddetli akut karın ağrısı ve kitlede çiğ et renginde hemorajik enfarktüsle seyreden dejenerasyon tipi hangisidir?",
                options=[
                    {"key": "A", "text": "Hiyalin dejenerasyon", "isCorrect": False, "explanation": "Hiyalin dejenerasyon en sık görülen ağrısız, asellüler kollajen birikimidir; kırmızı enfarktüs yapmaz."},
                    {"key": "B", "text": "Kırmızı (karneöz) dejenerasyon", "isCorrect": True, "explanation": "Doğru. Kırmızı (karneöz) dejenerasyon gebelikte hızla büyüyen miyomun venöz göllenme ve iskemik hemorajiye uğramasıdır."},
                    {"key": "C", "text": "Mukoid dejenerasyon", "isCorrect": False, "explanation": "Mukoid dejenerasyon stromada miksoid sıvı birikimidir; akut ağrılı karneöz tablo yapmaz."},
                    {"key": "D", "text": "Distrofik kalsifikasyon", "isCorrect": False, "explanation": "Kalsifikasyon postmenopozal dönemde kalsiyum çökmesiyle taşlaşmadır; gebelikteki kırmızı et görünümüyle ilgisizdir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Leiomyomlarda en sık rastlanan sekonder değişiklik homojen eozinofilik bağ dokusu birikimiyle karakterize hiyalin dejenerasyondur.",
                masked_term="hiyalin dejenerasyondur",
                hint="Kollajenöz pembe homojen matriks birikimi"
            ),
            make_table(
                title="Leiomyom Dejenerasyon Tipleri ve Özellikleri",
                headers=["Dejenerasyon Tipi", "Görülme Şartı", "Histopatolojik Karakteristik"],
                rows=[
                    [
                        {"text": "Hiyalin Dejenerasyon", "isMasked": False},
                        {"text": "En sık görülen tip", "isMasked": True, "hint": "Tüm dejenerasyonlar arasında en yüksek oran"},
                        {"text": "Düz kas kaybı ve pembe homojen kollajen birikimi", "isMasked": False}
                    ],
                    [
                        {"text": "Kırmızı (Karneöz)", "isMasked": False},
                        {"text": "Özellikle gebelikte", "isMasked": True, "hint": "Fetal gelişim ve yüksek hormon döneminde"},
                        {"text": "Venöz tromboz, hemorajik enfarktüs ve çiğ et görünümü", "isMasked": False}
                    ],
                    [
                        {"text": "Kalsifik Dejenerasyon", "isMasked": False},
                        {"text": "Postmenopozal ileri yaşta", "isMasked": False},
                        {"text": "İskemik alanlarda distrofik kalsiyum tuzlarının birikmesi", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Leiomyomlarda en sık izlenen dejenerasyon tipi hangisidir?",
                answer="Düz kas lifleri arasında asellüler homojen pembe kollajen birikimiyle seyreden hiyalin dejenerasyondur."
            )
        ]
    ))

    # Slide 9
    slides.append(make_slide(
        slide_num=9,
        title="Leiomyom: Histopatolojik Görünüm",
        subtitle="Monoton iğsi düz kas demetleri ve mitotik sakinlik",
        clinical_focus="Leiomyomun mikroskopik tanı kriterleri ve hücresel mimarisi",
        narrative=(
            "Leiomyomun mikroskobik incelemesinde normal myometrium dokusunu mükemmel şekilde taklit eden bir düz kas mimarisi izlenir. Tümör, farklı açılardan kesilmiş ve birbirinin içine giren düz kas demetlerinden (fasiküller) meydana gelir.\n\n"
            "- **Hücresel Morfoloji:** Düz kas hücreleri uzun, iğsi (mekik) formdadır. Çekirdekleri tipik olarak oval veya eliptik olup her iki ucu küt, puro benzeri (cigar-shaped) kontura sahiptir.\n"
            "- **Sitoplazma:** Bol miktarda fibriler, eozinofilik (pembe) sitoplazma taşırlar.\n"
            "- **Mitoz ve Atipi Yokluğu:** Selim leiomyomun en kritik histolojik özelliği belirgin hücresel pleomorfizmin (atipinin) bulunmaması ve mitotik figürlerin son derece nadir olmasıdır (<5 mitoz / 10 BÜA). Tümör hücresi nekrozu (koagülatif tümör nekrozu) kesinlikle izlenmez.\n\n"
            "> [!IMPORTANT]\n"
            "> Puro biçimli küt uçlu nükleuslar, eozinofilik fibriler sitoplazma ve atipi/tümör nekrozu yokluğu klasik leiomyomun mikroskobik mihenk taşıdır."
        ),
        bullets=[
            "Farklı yönlerde uzanan düz kas demetleri (fasiküller)",
            "Küt uçlu, puro benzeri (cigar-shaped) oval nükleuslar",
            "Bol eozinofilik fibriler sitoplazma",
            "Belirgin sitolojik atipi ve koagülatif tümör nekrozu yoktur"
        ],
        elements=[
            make_quiz(
                question="Leiomyomun mikroskobik incelemesinde izlenen düz kas hücrelerinin nükleus morfolojisi patoloji literatüründe klasik olarak nasıl tanımlanır?",
                options=[
                    {"key": "A", "text": "Çentikli kahve çekirdeği görünümü", "isCorrect": False, "explanation": "Kahve çekirdeği nükleus granüloza hücreli over tümörleri ve Brenner tümöründe görülür."},
                    {"key": "B", "text": "Küt uçlu, puro benzeri (cigar-shaped) nükleus", "isCorrect": True, "explanation": "Doğru. Düz kas hücrelerinin nükleusları iki ucu kütleşmiş eliptik puro (cigar) şeklindedir."},
                    {"key": "C", "text": "Buzlu cam / Orphan Annie nükleus", "isCorrect": False, "explanation": "Orphan Annie gözü nükleuslar tiroid papiller karsinomunun patognomonik özelliğidir."},
                    {"key": "D", "text": "Araba tekerleği kromatin paterni", "isCorrect": False, "explanation": "Araba tekerleği (clock-face) kromatin plazma hücrelerinin çekirdek özelliğidir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Histolojik incelemede bu tümörler normal myometriumu taklit eden görünüme sahip düz kas demetleri ile karakterizedir.",
                masked_term="düz kas demetleri",
                hint="Myosit fasiküllerinin mikroskobik organizasyonu"
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Leiomyom Histopatolojisi",
                items=[
                    {"text": "Tümör hücreleri bol eozinofilik sitoplazmalı ve iğsi morfolojidedir.", "isLie": False, "explanation": "Doğru. Düz kas hücreleri klasik iğsi eozinofilik yapıdadır."},
                    {"text": "Hücre nükleusları iki ucu yuvarlaklaşmış, küt puro benzeri görünümdedir.", "isLie": False, "explanation": "Doğru. Cigar-shaped nükleuslar düz kas diferansiasyonunun temel bulgusudur."},
                    {"text": "Klasik benign leiomyom dokusunda yaygın koagülatif tümör hücresi nekrozu ve belirgin nükleer atipi izlenir.", "isLie": True, "explanation": "Tuzak! Koagülatif tümör nekrozu ve belirgin sitolojik atipi malign leiomyosarkom kriterleridir; klasik selim leiomyomda bulunmaz."},
                    {"text": "Düz kas demetleri birbirini farklı açılarda kesen fasiküller halinde organize olmuştur.", "isLie": False, "explanation": "Doğru. Fasiküler ve girdapsı organizasyon tipiktir."}
                ]
            ),
            make_recall(
                question="Leiomyom histolojisinde düz kas hücrelerini fibroblastlardan ve sinir kılıfı hücrelerinden ayıran nükleus özelliği nedir?",
                answer="Küt uçlu, eliptik puro benzeri (cigar-shaped) nükleus yapısıdır."
            )
        ]
    ))

    # Slide 10 - Checkpoint 1
    slides.append(make_slide(
        slide_num=10,
        title="[TEKRAR SAYFASI - CHECKPOINT 1] Leiomyom Biyolojisi ve Özellikleri",
        subtitle="Bölüm 1 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="Leiomyom epidemiyolojisi, klonalitesi, makroskopisi ve histolojisi özeti",
        narrative=(
            "Bu tekrar sayfası, geride bıraktığımız ilk 9 adımda işlenen Leiomyom Biyolojisi kazanımlarını konsolide etmek amacıyla hazırlanmıştır. "
            "Leiomyom, myometriumun düz kas hücrelerinden köken alan, kadınlarda en sık izlenen benign neoplazmdır ve reprodüktif dönem kadınlarının %30-50'sinde saptanır.\n\n"
            "- **Genetik ve Hormon:** Her bir nodül 6 ve 12. kromozom anomalilerini içeren bağımsız bir monoklonal proliferasyondur. Östrojen bağımlıdır; gebelikte büyürken postmenopozda küçülür.\n"
            "- **Makroskopi ve Yerleşim:** Keskin sınırlı, gri-beyaz, kesit yüzü girdapsı desenlidir. İntramural (en sık), submukoz (en çok kanayan) ve subseröz tipleri vardır; omentuma tutunup beslenenlere parazitik miyom denir.\n"
            "- **Klinik ve Morfoloji:** En sık semptom menorajidir. Mikroskopide küt puro nükleuslu düz kas fasikülleri izlenir; tümör nekrozu veya belirgin atipi barındırmaz.\n\n"
            "> [!NOTE]\n"
            "> Leiomyomlar kesinlikle sarkoma dönüşmezler ve multiple olmaları hastanın malignite riskini artırmaz."
        ),
        bullets=[
            "En sık benign kadın tümörü; reprodüktif dönemde %30-50",
            "Monoklonal; 6 ve 12. kromozom translokasyonları",
            "Östrojenle büyür, postmenopozda küçülür",
            "Keskin sınırlı, gri-beyaz, girdapsı makroskopi",
            "En sık semptom menoraji; histolojide puro nükleuslu düz kas demetleri"
        ],
        elements=[
            make_quiz(
                question="Leiomyomların biyolojik davranışı, klonal yapısı ve klinik özellikleri hakkında aşağıdaki ifadelerden hangisi doğru bir sınav spotudur?",
                options=[
                    {"key": "A", "text": "Leiomyomlar postmenopozal dönemde over hormonlarının kesilmesiyle küçülürler ve kesit yüzleri girdapsıdır.", "isCorrect": True, "explanation": "Doğru. Leiomyomlar östrojen bağımlı olup menopozda küçülürler ve kesit yüzeylerinde girdapsı patern izlenir."},
                    {"key": "B", "text": "Leiomyomlar birden fazla sayıda olduklarında hızla malign leiomyosarkoma dönüşürler.", "isCorrect": False, "explanation": "Yanlış. Leiomyomlar sarkoma dönüşmez; multiple olmaları riski artırmaz."},
                    {"key": "C", "text": "Tümör dokusu poliklonal olup uterusun her yerinde aynı anda senkronize karsinojenez başlar.", "isCorrect": False, "explanation": "Yanlış. Leiomyomlar monoklonaldir; her nodül bağımsız tek bir hücreden türer."},
                    {"key": "D", "text": "En sık klinik şikayet postmenopozal ani kanama olup prepubertal kızlarda en yüksek insidansa ulaşır.", "isCorrect": False, "explanation": "Yanlış. Prepubertal dönemde görülmez; reprodüktif çağda menoraji ile belirti verir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Kadın genital sisteminde en sık rastlanan benign tümör olan leiomyomlar reprodüktif çağdaki kadınların yaklaşık yüzde 30-50 kadarında izlenir.",
                masked_term="yüzde 30-50",
                hint="Üçte biri ile yarısı arasındaki görülme sıklığı"
            ),
            make_table(
                title="Bölüm 1 Temel Kazanımlar Özeti",
                headers=["Özellik", "Leiomyom Karakteristiği", "Klinik Önem"],
                rows=[
                    [
                        {"text": "Köken Hücre", "isMasked": False},
                        {"text": "Myometrium düz kası", "isMasked": True, "hint": "Uterus korpusunun orta mezenkimal duvarı"},
                        {"text": "En sık benign jinekolojik neoplazm", "isMasked": False}
                    ],
                    [
                        {"text": "Genetik Kusur", "isMasked": False},
                        {"text": "Kromozom 6 ve 12 translokasyonu", "isMasked": True, "hint": "HMGA ailesi lokusları"},
                        {"text": "Lipom ve endometrial poliplerle ortak", "isMasked": False}
                    ],
                    [
                        {"text": "Makroskobik Kesit", "isMasked": False},
                        {"text": "Gri-beyaz girdapsı desen", "isMasked": False},
                        {"text": "Sert-elastik, keskin sınırlı", "isMasked": False}
                    ],
                    [
                        {"text": "En Sık Klinik Belirti", "isMasked": False},
                        {"text": "Menoraji", "isMasked": True, "hint": "Aşırı ve uzun süren adet kanaması"},
                        {"text": "Özellikle submukoz yerleşimde belirgin", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 1 Leiomyom Kazanımları",
                items=[
                    {"text": "Leiomyomlar monoklonal neoplazmlar olup her nodül bağımsız bir transformasyonu yansıtır.", "isLie": False, "explanation": "Doğru. G6PD ve sitogenetik çalışmalar monoklonaliteyi kanıtlamıştır."},
                    {"text": "Submukoz leiomyomlar kavite içine doğru büyüyerek şiddetli menorajiye yol açarlar.", "isLie": False, "explanation": "Doğru. Yüzey damarlanmasını bozarak ciddi kanama üretirler."},
                    {"text": "Uterusunda 5'ten fazla leiomyom nodülü saptanan kadınlarda bu lezyonların sarkoma dönüşme riski %80'e çıkar.", "isLie": True, "explanation": "Tuzak! Leiomyomlar sarkoma dönüşmez ve lezyon sayısının çokluğu (multiple miyom) malignite riskini kesinlikle artırmaz."},
                    {"text": "Östrojen leiomyom büyümesini uyarırken postmenopozal dönemde kitleler hacimce küçülür.", "isLie": False, "explanation": "Doğru. Hormonal çekilme postmenopozda küçülmeyi sağlar."}
                ]
            ),
            make_recall(
                question="Checkpoint 1: Leiomyomların cerrahi kesit yüzeyinde izlenen ve tanıyı koyduran patognomonik desen nedir?",
                answer="Birbiri etrafında dönen düz kas fasiküllerinin oluşturduğu gri-beyaz 'girdapsı' (whorled) desendir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=1
    ))
    
    return slides
