"""
Deck 54 Section 8: Gestasyonel Trofoblastik Hastalıkların Klinik ve Laboratuvar Yönetimi
Slides 71-80 (Checkpoint 8 at slide 80)
Focus:
- Molar tahliye sonrası seri beta-hCG takip algoritmaları ve plato/artış kriterleri
- Persistan trofoblastik hastalık ve invaziv mol ayrımı
- Koryokarsinomda erken metastaz taramaları (akciğer, vajina, beyin, karaciğer)
- Kemoterapi protokolleri ve kür oranları (metotreksat, aktinomisin D, EMA-CO)
- Paternal antijenlerin immünolojik avantajı ve gonad kaynaklı koryokarsinom farkı
- Trofoblastik hastalık sonrası gebelik planlaması ve kontrasepsiyon
- Postmolar teka lutein kistlerinin gerileme süreci
- Trofoblastik hastalıklarda acil kanama ve perforasyon yönetimi
- Plasental bölge trofoblastik tümörü (PSTT) morfolojisi ve düşük hCG üretimi
- Checkpoint 8
"""

from meds.scripts.deck_generators.deck54.deck54_helper import (
    make_slide,
    make_quiz,
    make_cloze,
    make_table,
    make_chain,
    make_recall,
    make_spot_the_lie,
    make_slider,
    make_swipe,
    make_branching,
    make_venn
)

def get_sec8_slides():
    slides = []

    # Slide 71
    slides.append(make_slide(
        slide_num=71,
        title="Molar Gebelik Tahliyesi Sonrası Beta-hCG İzlem Protokolü",
        subtitle="Haftalık seri titreler, plato kriteri ve persistan hastalık tanısı",
        clinical_focus="Komplet ve parsiyel mol sonrası malign sekel erken tanısı",
        narrative=(
            "Molar gebelik tanısı konup uterus kavitesi vakum küretaj ile boşaltıldıktan sonra hasta mutlaka sıkı bir biyokimyasal takip programına alınmalıdır.\n\n"
            "- **Takip Rutini:** Serum kantitatif beta-hCG düzeyi, değerler normale inene kadar **haftada bir kez** ölçülür. Normal sınırlara indikten sonra ardışık 3 hafta normal teyit edilir; ardından 6 ay boyunca ayda bir kez ölçüm sürdürülür.\n"
            "- **Persistan Hastalık ve Malignite Kriterleri (FIGO):** Birbirini izleyen en az 4 ölçümde (1, 7, 14 ve 21. günlerde) hCG düzeyinin plato çizmesi (değerin düşmemesi) veya ardışık 3 ölçümde (1, 7 ve 14. günlerde) %10 veya daha fazla artış göstermesi gestasyonel trofoblastik neoplazi (GTN) kanıtıdır.\n"
            "- **Histopatolojik Karşılık:** Bu biyokimyasal duraklama veya artış genellikle uterusta rezidüel invaziv mol veya erken evre koryokarsinom gelişimini işaret eder.\n\n"
            "> [!IMPORTANT]\n"
            "> Molar tahliye sonrası beta-hCG'nin plato çizmesi veya yükselmesi, klinik ve radyolojik kitle görülmese dahi persistan gestasyonel trofoblastik neoplazi tanısı koydurur."
        ),
        bullets=[
            "Vakum küretaj sonrası serum beta-hCG haftalık olarak titre edilir",
            "Değer normale indikten sonra 6 ay boyunca aylık kontrollerle izlenir",
            "Ardışık 4 ölçümde plato veya 3 ölçümde artış persistan GTN göstergesidir",
            "Molar doku kalıntısı, invaziv mol veya koryokarsinom erken saptanır"
        ],
        elements=[
            make_quiz(
                question="Komplet mol hidatiform nedeniyle vakum küretaj uygulanan 24 yaşındaki bir hastada, tahliye sonrası 3. ve 4. haftalarda bakılan serum beta-hCG düzeylerinin düşmeyip plato çizdiği ve 5. haftada yükseldiği saptanıyor. Bu klinik laboratuvar tablosu öncelikle hangisini işaret eder?",
                options=[
                    {"key": "A", "text": "Persistan gestasyonel trofoblastik neoplazi (invaziv mol / koryokarsinom)", "isCorrect": True, "explanation": "Doğru. Tahliye sonrası hCG'nin düşmeyip plato çizmesi veya yükselmesi persistan GTN'nin temel tanı kriteridir."},
                    {"key": "B", "text": "Normal fizyolojik korpus luteum toparlanması", "isCorrect": False, "explanation": "Korpus luteum hCG'yi artırmaz; hCG sinsityotrofoblastlardan gelir."},
                    {"key": "C", "text": "Myometriumda selim sellüler leiomyom büyümesi", "isCorrect": False, "explanation": "Sellüler miyom hCG salgılamaz."},
                    {"key": "D", "text": "Plasenta akreta gelişimi", "isCorrect": False, "explanation": "Akreta term gebelikte desidua yokluğudur; molar sekel değildir."}
                ],
                correct_key="A"
            ),
            make_cloze(
                sentence="Molar tahliye sonrası haftalık takipte beta-hCG düzeylerinin plato çizmesi veya yükselmesi persistan gestasyonel trofoblastik neoplazi lehinedir.",
                masked_term="persistan gestasyonel trofoblastik neoplazi",
                hint="Tahliye sonrası sebat eden habis koryonik kitle süreci"
            ),
            make_chain(
                title="Molar Tahliye Sonrası Biyokimyasal İzlem Algoritması",
                steps=[
                    "1. Müdahale: Uterus kavitesindeki molar veziküller vakum küretajla tamamen boşaltılır.",
                    "2. Seri Titrasyon: Maternal kanda kantitatif beta-hCG seviyesi her hafta düzenli ölçülür.",
                    "3. Normalizasyon: Değerin negatifleşmesi ardışık 3 hafta boyunca teyit edilir.",
                    "4. İdame Takip: Hasta 6 ay boyunca nüks ve GTN riskine karşı aylık hCG takibinde tutulur."
                ]
            ),
            make_recall(
                question="Molar gebelik tahliyesi sonrası takip süresince hastaya kesinlikle hangi koruyucu önlem önerilir ve nedeni nedir?",
                answer="En az 6 ay - 1 yıl güvenilir kontrasepsiyon (gebelikten korunma) önerilir; çünkü yeni bir gebelik hCG'yi yükselterek molar nüks ile karışır."
            )
        ]
    ))

    # Slide 72
    slides.append(make_slide(
        slide_num=72,
        title="Persistan Trofoblastik Hastalık ve İnvaziv Molün Klinik Yönetimi",
        subtitle="Myometriyal penetrasyon, kanama kontrolü ve medikal tedavi",
        clinical_focus="Küretajla temizlenemeyen derin myometriyal molar invazyon",
        narrative=(
            "Komplet mol olgularının yaklaşık %10'unda trofoblastik villuslar myometriumun derin katmanlarına ve hatta uterin damarlara invaze olur (**invaziv mol**).\n\n"
            "- **Klinik Tablo:** Hastada molar küretaj sonrasında durmayan veya tekrarlayan vajinal kanamalar, uterusta büyüme ve serum beta-hCG düzeylerinde inatçı sebat izlenir.\n"
            "- **Cerrahi Sınırlar:** İnvaziv mol koryon villusları myometrium içine derinlemesine gömülü olduğu için tekrarlayan küretajlarla asla temizlenemez; agresif küretaj denemeleri uterus perforasyonuna ve şiddetli kanamaya neden olur.\n"
            "- **Tedavi Protokolü:** İnvaziv mol olgularında histopatolojik piyes elde etmek için histerektomi yapılması şart değildir. Hastaların ezici çoğunluğu doğurganlığı koruyan tek ajanlı kemoterapi (**Metotreksat** veya **Aktinomisin D**) ile %100'e yakın kür elde edilerek tedavi edilir.\n\n"
            "> [!NOTE]\n"
            "> İnvaziv molde derin myometrial villuslar küretajla kazınamaz; aşırı küretaj rüptür yapar. Tedavinin omurgası sistemik kemoterapidir."
        ),
        bullets=[
            "Komplet mollerin %10'u myometrium derinliğine invaze olur (invaziv mol)",
            "Klinikte inatçı kanama ve düşmeyen beta-hCG düzeyleri ile seyreder",
            "Tekrarlayan küretajlar perforasyon riski taşır ve kür sağlamaz",
            "Tek ajanlı metotreksat veya aktinomisin D ile medikal kür sağlanır"
        ],
        elements=[
            make_quiz(
                question="Molar gebelik küretajı sonrası myometrium derinliğine invaze hidropik villusların bulunduğu ve kanama ile başvuran bir invaziv mol hastasında doğurganlığı korumak amacıyla öncelikli tedavi yaklaşımı ne olmalıdır?",
                options=[
                    {"key": "A", "text": "Uterus kavitesine her gün ardışık agresif küretaj uygulamak", "isCorrect": False, "explanation": "Agresif küretaj perforasyon ve masif kanama riski taşır; derin myometriyal dokuyu temizleyemez."},
                    {"key": "B", "text": "Acil radikal pelvik radyoterapi vermek", "isCorrect": False, "explanation": "İnvaziv molde primer tedavi radyoterapi değildir; over fonksiyonlarını yok eder."},
                    {"key": "C", "text": "Tek ajanlı sistemik kemoterapi (Metotreksat veya Aktinomisin D)", "isCorrect": True, "explanation": "Doğru. İnvaziv mol kemoterapiye son derece duyarlıdır; doğurganlığı koruyarak %100 kür sağlar."},
                    {"key": "D", "text": "Geniş spektrumlu antibiyotikle lezyonun kurumasını beklemek", "isCorrect": False, "explanation": "İnvaziv mol enfeksiyon değil trofoblastik neoplazidir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Myometrium derinliklerine ilerleyen invaziv mol olgularında doğurganlığı korumak amacıyla tek ajanlı kemoterapi uygulanır ve tam kür elde edilir.",
                masked_term="tek ajanlı kemoterapi",
                hint="Metotreksat veya aktinomisin D ile yapılan medikal onkolojik kür"
            ),
            make_branching(
                scenario="26 yaşında komplet mol tahliyesi yapılmış kadın hastada 4. haftada beta-hCG plato çiziyor; pelvik ultrasonda myometrium içinde 2 cm invaziv kitle odağı izleniyor.",
                options=[
                    {
                        "text": "Tekrar küretaj yaparak myometriumu derinlemesine kazımak",
                        "isCorrect": False,
                        "feedback": "Hatalı Karar: Myometrium içine gömülü villusları küretajla temizlemeye çalışmak uterus rüptürüne ve hayatı tehdit eden masif kanamalara yol açar."
                    },
                    {
                        "text": "Pelvik ve toraks metastaz taraması yapıp tek ajanlı sistemik kemoterapi planlamak",
                        "isCorrect": True,
                        "feedback": "Doğru Karar: İnvaziv molde primer yaklaşım metastaz taraması ve sistemik kemoterapidir (Metotreksat); doğurganlık korunarak tam kür sağlanır."
                    },
                    {
                        "text": "Hastaya hormon replasmanı başlayıp 6 ay sonra kontrole çağırmak",
                        "isCorrect": False,
                        "feedback": "Hatalı Karar: Persistan trofoblastik neoplazi tedavi edilmezse hızla koryokarsinoma ilerleyebilir."
                    }
                ]
            ),
            make_recall(
                question="İnvaziv mol olgularında cerrahi histerektomi yerine kemoterapi tercih edilmesinin en önemli hasta yararı nedir?",
                answer="Hastanın uterusu ve doğurganlık (fertilite) yeteneği korunur; gelecekte normal gebelik şansı devam eder."
            )
        ]
    ))

    # Slide 73
    slides.append(make_slide(
        slide_num=73,
        title="Koryokarsinomda Erken Metastaz Taramaları ve Hedef Organlar",
        subtitle="Akciğer (%50), vajina, karaciğer, beyin ve böbrek yayılımı",
        clinical_focus="Erken hematojen yayılımın klinik semptomları ve görüntüleme",
        narrative=(
            "Gestasyonel koryokarsinom, insan vücudundaki en anaplastik ve en hızlı damar invazyonu yapan tümörlerden biridir; primer uterin odak küçük veya tamamen nekrotik olsa dahi erken dönemde sistemik dolaşıma yayılır.\n\n"
            "- **En Sık Metastaz Yeri (Akciğer %50):** Tümör hücreleri vena kava yoluyla akciğer kapiller ağına oturur; parankim damarlarını parçalayarak kanamalı 'top güllesi' metastazları yapar. Klinik belirtisi öksürük, nefes darlığı ve **hemoptizidir (kan tükürme)**.\n"
            "- **Vajinal Metastazlar:** Pelvik venöz pleksusların ters akımıyla vajina ön duvarı ve fornikste **koyu mor-mavi renkli, frajil, kanamalı subepitelyal nodüller** oluşur. Biyopsi alınması masif kanamaya yol açabileceğinden biyopsiden kesinlikle kaçınılmalıdır.\n"
            "- **Beyin ve Karaciğer Yayılımı:** Yüksek riskli ileri evreyi tanımlar. Beyin metastazları intrakraniyal kanama, nöbet ve felç tablosuyla prezente olur.\n\n"
            "> [!IMPORTANT]\n"
            "> Vajinada mor-mavi kanamalı nodül görüldüğünde koryokarsinom şüphelenilmeli ve biyopsi ASLA alınmamalıdır; ölümcül kanama başlatabilir, tanı serum hCG ile konur."
        ),
        bullets=[
            "Koryokarsinom en sık hematojen yolla akciğere (%50) yayılır; hemoptizi yapar",
            "Vajinada mor-mavi, kolay kanayan vasküler metastatik nodüller oluşturur",
            "Vajinal metastaz nodülünden biyopsi alınmaz; masif kanama riski yüksektir",
            "Beyin ve karaciğer metastazları FIGO yüksek risk grubunu oluşturur"
        ],
        elements=[
            make_quiz(
                question="Doğumdan 4 ay sonra nefes darlığı ve hemoptizi şikayetiyle başvuran, jinekolojik muayenesinde vajina ön duvarında 2 cm çapında mor-mavi renkli, frajil, kanamalı bir nodül izlenen kadında tanısal yaklaşım nasıl olmalıdır?",
                options=[
                    {"key": "A", "text": "Hemen vajinal nodülden derin insizyonel kama biyopsi almak", "isCorrect": False, "explanation": "Vajinal koryokarsinom nodülüne biyopsi yapmak durdurulamayan masif kanamaya yol açar; kontrendikedir."},
                    {"key": "B", "text": "Serum beta-hCG ölçümü ve akciğer grafisi ile trofoblastik metastazı araştırmak", "isCorrect": True, "explanation": "Doğru. Mor-mavi vajinal nodül ve hemoptizi koryokarsinomun klasik metastaz bulgusudur; tanı serum beta-hCG ve toraks görüntülemesiyle non-invaziv konur."},
                    {"key": "C", "text": "Nodülü selim hemanjiyom kabul edip hastayı takipsiz taburcu etmek", "isCorrect": False, "explanation": "Hemoptizisi olan gebelik sonrası bir kadında bu bulgu malign koryokarsinom metastazıdır."},
                    {"key": "D", "text": "Sadece idrar tahlili yapıp antibiyotik başlamak", "isCorrect": False, "explanation": "Klinik tablo onkolojik gestasyonel acildir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Koryokarsinomun pelvik venöz geri akımla oluşturduğu mor-mavi vajinal metastaz nodüllerinden masif ölümcül kanama riski nedeniyle biyopsi alınmamalıdır.",
                masked_term="mor-mavi vajinal metastaz",
                hint="Alt genital kanalda oluşan hipervasküler trofoblastik yayılım lezyonu"
            ),
            make_table(
                title="Koryokarsinom Metastaz Organları ve Klinik Belirtileri",
                headers=["Metastaz Bölgesi", "Görülme Sıklığı", "Klasik Klinik Belirti / Risk"],
                rows=[
                    [
                        {"text": "Akciğer Parankimi", "isMasked": False},
                        {"text": "Olguların yaklaşık %50'si", "isMasked": True, "hint": "Tümörün en sık ulaştığı ilk kapiller organ"},
                        {"text": "Öksürük, dispne, kan tükürme (hemoptizi)", "isMasked": False}
                    ],
                    [
                        {"text": "Vajina (Alt Genital)", "isMasked": False},
                        {"text": "Sık izlenen pelvik bölge", "isMasked": False},
                        {"text": "Mor-mavi kanamalı nodüller; biyopsi kontrendikedir", "isMasked": True, "hint": "Aşırı damarlı yapı sebebiyle durdurulamayan hemostaz problemi"}
                    ],
                    [
                        {"text": "Beyin / Karaciğer", "isMasked": False},
                        {"text": "İleri evre yüksek risk", "isMasked": False},
                        {"text": "İntrakraniyal kanama, nörolojik defisit, sarılık", "isMasked": False}
                    ]
                ]
            ),
            make_recall(
                question="Gestasyonel koryokarsinomda vajina duvarındaki şüpheli metastaz odağından patolojik biyopsi alınması neden kesinlikle önerilmez?",
                answer="Tümör aşırı vasküler ve damar yıkıcı olduğu için biyopsi yeri cerrahi olarak durdurulamayan masif kanamaya yol açabilir; tanı kanda beta-hCG ile teyit edilir."
            )
        ]
    ))

    # Slide 74
    slides.append(make_slide(
        slide_num=74,
        title="Gestasyonel Trofoblastik Neoplazilerde FIGO Risk Skorlama Sistemi",
        subtitle="Düşük risk (tek ajan) vs yüksek risk (kombine kemoterapi)",
        clinical_focus="Tedavi rejiminin seçiminde prognostik skorlama",
        narrative=(
            "Gestasyonel trofoblastik neoplazi (GTN) saptanan hastalarda tedavi şeması Dünya Sağlık Örgütü (DSÖ) ve FIGO tarafından geliştirilen prognostik skorlama sistemine göre belirlenir.\n\n"
            "- **Skorlama Parametreleri:** Hastanın yaşı (>40 yaş yüksek puan), önceki gebeliğin tipi (term gebelik mol gebeliğe göre daha yüksek puan), gebelik ile tedavi arası süre (>4 ay), başlangıç serum beta-hCG düzeyi (>100.000 mIU/mL), tümör boyutu (>5 cm), metastaz sayısı ve yeri (karaciğer ve beyin en yüksek puan), önceki başarısız kemoterapi öyküsü değerlendirilir.\n"
            "- **Düşük Risk Grubu (Skor 0-6):** Tek ajanlı kemoterapi (**Metotreksat** veya **Aktinomisin D**) ile tedavi edilir. Kür oranı %100'e yakındır.\n"
            "- **Yüksek Risk Grubu (Skor ≥7):** Çoklu kombinasyon kemoterapisi gerektirir. Standart rejim **EMA-CO** (Etopozid, Metotreksat, Aktinomisin D, Siklofosfamid, Vinkristin/Onkovin) protokolüdür.\n\n"
            "> [!NOTE]\n"
            "> FIGO skoru ≤6 ise tek ajan metotreksat; skor ≥7 ise kombine EMA-CO protokolü uygulanır."
        ),
        bullets=[
            "FIGO prognostik skoru yaş, hCG düzeyi, metastaz yeri ve gebelik tipine bakar",
            "Term gebelik sonrası gelişen koryokarsinom, mole göre daha yüksek risklidir",
            "Düşük riskli olgularda (skor ≤6) tek ajan metotreksat ile tam kür sağlanır",
            "Yüksek riskli olgularda (skor ≥7) çoklu kombinasyon EMA-CO rejimi uygulanır"
        ],
        elements=[
            make_quiz(
                question="Term normal doğumdan 8 ay sonra çoklu akciğer ve karaciğer metastazları saptanan, serum beta-hCG düzeyi 250.000 mIU/mL olan ve FIGO prognostik skoru 9 (yüksek risk) hesaplanan koryokarsinomlu hastada en uygun kemoterapi protokolü hangisidir?",
                options=[
                    {"key": "A", "text": "Tek ajan oral folik asit takviyesi", "isCorrect": False, "explanation": "Folik asit kemoterapi değildir; tümör büyümesini bile besleyebilir."},
                    {"key": "B", "text": "Düşük doz tek ajan metotreksat", "isCorrect": False, "explanation": "Metotreksat tek başına sadece düşük riskli (skor ≤6) olgularda verilir; yüksek riskte direnç gelişir."},
                    {"key": "C", "text": "Çoklu kombinasyon kemoterapisi (EMA-CO rejimi)", "isCorrect": True, "explanation": "Doğru. FIGO skoru ≥7 olan yüksek riskli koryokarsinom hastalarında standart rejim çoklu kemoterapi olan EMA-CO protokolüdür."},
                    {"key": "D", "text": "Sadece lezyonlu akciğer lobunun cerrahi rezeksiyonu", "isCorrect": False, "explanation": "Sistemik metastatik trofoblastik tümörlerde tek başına cerrahi kür sağlamaz."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="FIGO risk skoru 7 ve üzerinde olan yüksek riskli gestasyonel trofoblastik neoplazi olgularında çoklu kemoterapi protokolü olan EMA-CO rejimi uygulanır.",
                masked_term="EMA-CO rejimi",
                hint="Etopozid, metotreksat, aktinomisin D, siklofosfamid ve onkovin kombinasyonu"
            ),
            make_slider(
                left_title="Düşük Riskli GTN (FIGO Skoru ≤6)",
                right_title="Yüksek Riskli GTN (FIGO Skoru ≥7)",
                left_points=[
                    "Genellikle molar gebeliği kısa süre içinde izler",
                    "hCG düzeyi nispeten düşüktür; metastaz yok veya sadece akciğerdedir",
                    "Tek ajanlı Metotreksat veya Aktinomisin D ile %100 kür sağlanır"
                ],
                right_points=[
                    "Term gebelik sonrası gelişebilir; beyin/karaciğer tutulumu olabilir",
                    "hCG düzeyi çok yüksektir (>100.000 mIU/mL) ve metastazlar yaygındır",
                    "Çoklu kombinasyon kemoterapisi (EMA-CO) gerektirir; kür %85-90'dır"
                ]
            ),
            make_recall(
                question="Bir koryokarsinom olgusunun term (zamanında) bir normal gebelikten sonra ortaya çıkması neden molar gebelikten sonra çıkmasına kıyasla daha kötü prognoz puanı alır?",
                answer="Term gebelik sonrası koryokarsinom tanısı genellikle semptomlar geç fark edildiği için gecikir, metastazlar yaygınlaşır ve genetik yapısı daha agresiftir."
            )
        ]
    ))

    # Slide 75
    slides.append(make_slide(
        slide_num=75,
        title="Gestasyonel vs Non-Gestasyonel Koryokarsinom: İmmünolojik Paradoks",
        subtitle="Paternal antijenlerin kemoterapi duyarlılığına etkisi",
        clinical_focus="Plasental kökenli tümörlerin gonad tümörlerinden dramatik kür farkı",
        narrative=(
            "Koryokarsinom hem gebelik dokusundan (gestasyonel) hem de over veya testis germ hücrelerinden (non-gestasyonel) kaynaklanabilir. Mikroskop altında her iki tümör de birbirinin tamamen aynısıdır; anaplastik sito ve sinsityotrofoblastlardan oluşur ve koryon villusu içermez. Ancak klinik yanıtları taban tabana zıttır.\n\n"
            "- **Gestasyonel Koryokarsinom:** Babaya ait (paternal) kromozomları taşır. Bu paternal antijenler anne bağışıklık sistemi için yabancı bir **allogreft** gibidir. Kemoterapi tümör hücrelerini öldürmeye başladığında, maternal immün sistem açığa çıkan yabancı paternal antijenlere karşı güçlü bir sitotoksik yanıt başlatır. Bu immünolojik sinerji sayesinde metastatik hastalıkta dahi **%90-100 oranında tam kür** sağlanır.\n"
            "- **Non-Gestasyonel Koryokarsinom:** Hastanın kendi germ hücrelerinden köken alır; paternal antijen taşımaz (otojeniktir). Maternal bağışıklık sistemi tümörü yabancı olarak tanıyamaz. Bu nedenle kemoterapiye dirençlidir ve prognozu son derece kötüdür.\n\n"
            "> [!IMPORTANT]\n"
            "> Gestasyonel koryokarsinom babadan gelen (paternal) yabancı antijenler sayesinde kemoterapiyle %100'e varan kür şansına sahiptir; gonad kaynaklı olanlar bu antijenlerden yoksun olduğu için kemoterapiye dirençlidir."
        ),
        bullets=[
            "Gestasyonel koryokarsinom allogreft niteliğindedir; paternal antijenler taşır",
            "Maternal bağışıklık sistemi paternal antijenleri yabancı görerek saldırır",
            "İmmünite ile kemoterapinin sinerjisi %100'e yakın kür elde edilmesini sağlar",
            "Gonadal (over/testis) koryokarsinom paternal antijen taşımaz; kemoterapiye dirençlidir"
        ],
        elements=[
            make_quiz(
                question="Aynı histopatolojik morfolojiye (anaplastik trofoblastlar, koryon villusu yokluğu) sahip olmalarına rağmen, gebelik kökenli gestasyonel koryokarsinomun kemoterapiyle kür oranı %100'e yakınken, over veya testis kökenli koryokarsinomun kemoterapiye belirgin dirençli ve ölümcül olmasının temel biyolojik nedeni nedir?",
                options=[
                    {"key": "A", "text": "Gestasyonel koryokarsinomda bakteriyel enfeksiyon bulunması", "isCorrect": False, "explanation": "Koryokarsinom bakteriyel değil neoplastik bir antitedir."},
                    {"key": "B", "text": "Gonad tümörlerinin kan damarı içermemesi", "isCorrect": False, "explanation": "Her iki tümör de aşırı vasküler ve kanamalıdır."},
                    {"key": "C", "text": "Gestasyonel formun paternal (babadan gelen) yabancı antijenler taşıması ve maternal immün yanıtı tetiklemesi", "isCorrect": True, "explanation": "Doğru. Paternal antijenler anne için yabancı allogreft görevi görür; kemoterapinin açtığı hücresel yıkımla maternal immün sistem sinerji oluşturarak tümörü tamamen temizler."},
                    {"key": "D", "text": "Gestasyonel koryokarsinomun hiç beta-hCG üretmemesi", "isCorrect": False, "explanation": "Aksine, gestasyonel koryokarsinom devasa miktarda beta-hCG üretir."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Gestasyonel koryokarsinomun kemoterapiye olağanüstü yüksek yanıt vermesini sağlayan temel faktör paternal antijenlerin varlığıdır.",
                masked_term="paternal antijenlerin varlığıdır",
                hint="Babadan gelen yabancı doku proteinlerinin maternal immüniteyi uyarması"
            ),
            make_slider(
                left_title="Gestasyonel Koryokarsinom (Uterus/Plasenta)",
                right_title="Non-Gestasyonel Koryokarsinom (Over/Testis)",
                left_points=[
                    "Fertilize gebelik ürününden kaynaklanır",
                    "Paternal (babadan gelen) yabancı antijenler eksprese eder",
                    "Kemoterapi + maternal immün sinerji ile kür oranı %90-100'dür"
                ],
                right_points=[
                    "Bireyin kendi totipotent germ hücrelerinden köken alır",
                    "Yabancı paternal antijen taşımaz; konakla tamamen izojeniktir",
                    "Kemoterapiye yanıtı son derece zayıftır; klinik seyri ölümcüldür"
                ]
            ),
            make_recall(
                question="Non-gestasyonel gonadal koryokarsinom ile gestasyonel uterin koryokarsinomun mikroskopik kesitlerine bakan bir patolog bunları sadece morfolojik görüntüyle ayırt edebilir mi?",
                answer="Hayır, mikroskopik morfolojileri (sito/sinsityotrofoblastik atipik tabakalar ve villus yokluğu) tamamen özdeştir; ayrım klinik öykü ve genetik paternal analizle yapılır."
            )
        ]
    ))

    # Slide 76
    slides.append(make_slide(
        slide_num=76,
        title="Trofoblastik Hastalıklarda Acil Obstetrik Komplikasyonlar",
        subtitle="Uterin perforasyon, intraperitoneal kanama ve akut respiratuar distres",
        clinical_focus="İnvaziv mol ve koryokarsinomun hayatı tehdit eden acil tabloları",
        narrative=(
            "Gestasyonel trofoblastik tümörler yoğun damar istilası ve litik enzim salgılama yetenekleri nedeniyle hayatı tehdit eden ani cerrahi ve medikal acillere yol açabilir.\n\n"
            "- **Uterin Perforasyon ve Hemoperitoneum:** İnvaziv mol koryon villusları veya koryokarsinom hücreleri myometriumu tam kat eriterek serozayı delebilir. Bu durum dakikalar içinde masif intraabdominal kanamaya, akut batın bulgularına ve hipovolemik şoka neden olur. Bu hastalarda acil laparotomi ve kanama kontrolü (sıklıkla acil histerektomi) hayat kurtarıcıdır.\n"
            "- **Trofoblastik Pulmoner Emboli ve ARDS:** Molar küretaj esnasında veya kendiliğinden büyük miktarda trofoblastik dokunun uterin venöz sinüslere dökülmesi, yaygın pulmoner mikroemboliye, ani dispneye ve respiratuar distres tablosuna (ARDS) yol açabilir.\n"
            "- **Metastatik İntrakraniyal Kanama:** Beyin metastazı olan koryokarsinom hastalarında tümör içi ani kanama ölümcül herniasyon yapabilir.\n\n"
            "> [!NOTE]\n"
            "> Uterusu delen invaziv mol masif hemoperitoneum ve şok yapar; acil laparotomi gerektirir. Molar küretaj sırasında akut solunum sıkıntısı trofoblastik emboliyi düşündürmelidir."
        ),
        bullets=[
            "İnvaziv mol veya koryokarsinom myometriumu delerek hemoperitoneum yapabilir",
            "Uterin rüptür gelişen olgularda acil laparotomi ve kanama kontrolü gerekir",
            "Molar küretajda venöz sinüslere villus dökülmesi trofoblastik emboli yapabilir",
            "Trofoblastik emboli akut solunum yetmezliği ve göğüs ağrısıyla prezente olur"
        ],
        elements=[
            make_quiz(
                question="Komplet mol nedeniyle takip edilmekte olan 30 yaşındaki bir kadında aniden şiddetli alt karın ağrısı, taşikardi, hipotansiyon (tansiyon 70/40 mmHg) ve periton irritasyon bulguları gelişiyor. Parasentezde batın içinde pıhtılaşmayan taze kan aspire ediliyor. Bu acil klinik tablonun en olası mekanizması hangisidir?",
                options=[
                    {"key": "A", "text": "Basit korpus luteum kisti rüptürü", "isCorrect": False, "explanation": "Molar hastada derin şok ve masif kanama trofoblastik perforasyondur."},
                    {"key": "B", "text": "İnvaziv molün myometriumu tam kat eriterek uterusu perfore etmesi ve masif hemoperitoneum", "isCorrect": True, "explanation": "Doğru. İnvaziv mol myometrium duvarını eritebilir; serozayı aştığında intraabdominal kanama ve hipovolemik şok tablosu gelişir."},
                    {"key": "C", "text": "Submuköz leiomyomun pedikül torsiyonu", "isCorrect": False, "explanation": "Pediküllü submuköz miyom torsiyonu kaviter nekroz yapar; batın içine masif taze kanama yapmaz."},
                    {"key": "D", "text": "Plasenta perkreta zemininde term doğum başlaması", "isCorrect": False, "explanation": "Hasta term gebe değil, molar hastalık takibindedir."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="İnvaziv mol olgularında myometriumun tam kat destrüksiyonu sonucu gelişen uterin perforasyon hayatı tehdit eden masif karın içi kanamaya yol açar.",
                masked_term="uterin perforasyon",
                hint="Uterus duvarının kitle tarafından delinmesi durumu"
            ),
            make_chain(
                title="İnvaziv Mol Rüptürü ve Hemoperitoneum Patofizyolojik Akışı",
                steps=[
                    "1. Myometriyal Derinleşme: Hidropik molar villuslar myometriumun dış tabakalarına doğru litik olarak ilerler.",
                    "2. Transmural Delinme: Uterus seroza tabakası ve uterin arter dalları destrükte olarak perfore olur.",
                    "3. Karın İçi Kanama: Pelvik kaviteye ve batın içine litrelerce serbest kan dökülür (hemoperitoneum).",
                    "4. Hipovolemik Kollaps: Hastada taşikardi, derin hipotansiyon ve acil cerrahi gerektiren akut şok gelişir."
                ]
            ),
            make_recall(
                question="Molar tahliye işlemi sırasında anestezi altındaki hastada aniden siyanoz, taşikardi ve satürasyon düşüşü (akut dispne) gelişirse öncelikle hangi patolojik emboli düşünülmelidir?",
                answer="Trofoblastik doku embolisi (molar villusların ve sinsityotrofoblastların uterin venler yoluyla akciğer damarlarına kaçması) düşünülmelidir."
            )
        ]
    ))

    # Slide 77
    slides.append(make_slide(
        slide_num=77,
        title="Postmolar Teka Lutein Kistlerinin Takibi ve Spontan Rezolüsyonu",
        subtitle="Hiperreaksiyo luteinalis, ovaryan büyüme ve konservatif yaklaşım",
        clinical_focus="Gereksiz over cerrahisinden kaçınma prensibi",
        narrative=(
            "Molar gebeliklerin ve koryokarsinomun en dramatik jinekolojik bulgularından biri overlerin aşırı büyümesidir (**hiperreaksiyo luteinalis**).\n\n"
            "- **Mekanizma:** Aşırı miktarda salgılanan trofoblastik hCG, lüteinizan hormon (LH) reseptörlerine çapraz bağlanarak teka interna hücrelerinde masif luteinizasyona ve bilateral multipl kistik kitlelere yol açar. Overler bazen 10-15 cm boyutlara ulaşarak pelviste palpabl kitle oluşturur.\n"
            "- **Klinik Yaklaşım:** Bu kistler neoplastik değildir. En önemli klinik kural **gereksiz ooforektomi veya kistektomiden kesinlikle kaçınmaktır**. Molar doku tahliye edilip hCG seviyeleri düştükçe, bu devasa kistler haftalar ve aylar içinde kendiliğinden büzüşerek tamamen **spontan rezolüsyona** uğrar.\n"
            "- **Komplikasyon İstisnası:** Tek cerrahi endikasyon, aşırı büyümüş overin kendi etrafında dönmesi (**ovaryan torsiyon**) veya kist rüptürüne bağlı masif kanama gelişmesidir.\n\n"
            "> [!IMPORTANT]\n"
            "> Teka lutein kistleri hCG uyarısıyla oluşan selim kistlerdir; neoplastik değildir. Molar tahliye sonrası hCG düştükçe kendiliğinden kaybolurlar, cerrahi çıkarım yapılmaz."
        ),
        bullets=[
            "Teka lutein kistleri aşırı yüksek hCG uyarısıyla bilateral gelişir",
            "Overler 10-15 cm boyutlara ulaşabilir; teka interna luteinizasyonu izlenir",
            "Neoplastik değildir; cerrahi kistektomi veya ooforektomi yapılmamalıdır",
            "Molar doku temizlenip hCG gerilediğinde kistler spontan olarak küçülür"
        ],
        elements=[
            make_quiz(
                question="Komplet mol hidatiform nedeniyle vakum küretaj yapılan ve her iki overinde ultrasonda 10'ar cm çapında çok odacıklı kistler (teka lutein kistleri) izlenen asemptomatik bir hastada over lezyonlarına yönelik en doğru klinik yaklaşım nedir?",
                options=[
                    {"key": "A", "text": "Malign over karsinomu şüphesiyle acil bilateral ooforektomi yapmak", "isCorrect": False, "explanation": "Teka lutein kistleri habis değildir; ooforektomi hastayı gereksiz kastre eder."},
                    {"key": "B", "text": "Overlere lokal radyasyon vererek kistleri yakmak", "isCorrect": False, "explanation": "Radyoterapi endikasyonu yoktur; fertiliteyi yok eder."},
                    {"key": "C", "text": "Hastalara over ponksiyonu yapıp sıvıları aspire etmek", "isCorrect": False, "explanation": "Ponksiyon enfeksiyon ve torsiyon riski taşır; endike değildir."},
                    {"key": "D", "text": "Overleri cerrahi olarak ellememek; beta-hCG düştükçe kistlerin kendiliğinden küçülmesini takip etmek", "isCorrect": True, "explanation": "Doğru. Teka lutein kistleri hCG uyarısına bağlı selim hiperreaksiyondur; molar tahliye sonrası hormon çekilince kendiliğinden tamamen geriler."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Molar gebelikte saptanan devasa teka lutein kistleri hCG seviyeleri normale indikçe cerrahi müdahaleye gerek kalmadan kendiliğinden spontan rezolüsyona uğrar.",
                masked_term="spontan rezolüsyona",
                hint="Tıbbi veya cerrahi müdahalesiz kendi kendine gerileyip kaybolma süreci"
            ),
            make_venn(
                title="Teka Lutein Kisti vs Endometrioma (Çikolata Kisti)",
                label_a="Teka Lutein Kisti",
                label_b="Endometrioma (Çikolata Kisti)",
                items=[
                    {"criterion": "Aşırı yüksek serum hCG uyarısıyla bilateral multipl luteinize kistler şeklinde gelişme", "correct": "A", "explanation": "Teka lutein kisti trofoblastik hormon fazlalığına sekonderdir."},
                    {"criterion": "Ektopik endometrial gland ve stromanın siklik kanamalarıyla çikolata renkli kist oluşturması", "correct": "B", "explanation": "Endometrioma endometriozis zemininde gelişir; hemosiderin yüklü makrofajlar içerir."},
                    {"criterion": "Pelvik muayene veya ultrasonda kistik ovaryan kitle olarak saptanabilme", "correct": "both", "explanation": "Her iki antite de overde kistik kitle manzarası oluşturur."},
                    {"criterion": "Myometrium düz kas liflerinin monoklonal mutasyonu sonucu girdapsı nodül yapma", "correct": "neither", "explanation": "Bu leiomyomun özelliğidir; over kisti değildir."}
                ]
            ),
            make_recall(
                question="Bilateral teka lutein kisti olan bir molar gebelik hastasında bu kistlere cerrahi müdahale yapılması gereken tek acil durum nedir?",
                answer="Kistin ağırlığı nedeniyle overin kendi pedikülü etrafında dönmesi (akut ovaryan torsiyon) veya batın içine rüptüre olup kanamasıdır."
            )
        ]
    ))

    # Slide 78
    slides.append(make_slide(
        slide_num=78,
        title="Plasental Bölge Trofoblastik Tümörü (PSTT)",
        subtitle="İntermediate trofoblast neoplazmı, human plasental laktojen (hPL) ve kemorezistans",
        clinical_focus="Koryokarsinomdan farklı trofoblastik neoplazinin ayırıcı özellikleri",
        narrative=(
            "Gestasyonel trofoblastik hastalık spektrumunun nadir fakat özgün bir üyesi **Plasental Bölge Trofoblastik Tümörüdür (Placental Site Trophoblastic Tumor - PSTT)**.\n\n"
            "- **Köken:** Sito veya sinsityotrofoblastlardan değil, plasenta yatağındaki **intermediate (ara) trofoblastlardan** köken alır.\n"
            "- **Biyokimyasal Profil:** Sinsityotrofoblastlar az olduğu için koryokarsinomun aksine **beta-hCG seviyeleri oldukça düşüktür**. Buna karşılık intermediate trofoblastların temel hormonu olan **human plasental laktojen (hPL)** immünohistokimyasal olarak diffüz kuvvetli pozitiftir.\n"
            "- **Biyolojik Davranış ve Tedavi Farkı:** Koryokarsinomun aksine standart kemoterapiye (metotreksat/EMA-CO) **oldukça dirençlidir**. Lenfatik yayılım gösterebilir. Bu nedenle PSTT olgularında primer ve en etkili küratif tedavi cerrahidir (**histerektomi**).\n\n"
            "> [!IMPORTANT]\n"
            "> PSTT intermediate trofoblastlardan köken alır; beta-hCG düşük, hPL yüksektir; koryokarsinomun aksine kemoterapiye dirençlidir ve tedavisi histerektomidir."
        ),
        bullets=[
            "PSTT intermediate (ara) trofoblast hücrelerinden köken alan nadir GTN'dir",
            "Serum beta-hCG seviyeleri düşüktür; human plasental laktojen (hPL) pozitiftir",
            "Koryokarsinomdan farklı olarak standart kemoterapiye belirgin dirençlidir",
            "Primer ve en etkili tedavi yaklaşımı cerrahi histerektomidir"
        ],
        elements=[
            make_quiz(
                question="Normal doğumdan aylar sonra hafif vajinal kanama ile başvuran, serum beta-hCG düzeyi hafif yüksek (sadece 150 mIU/mL) bulunan, biyopside damarları infiltre eden intermediate trofoblastlar saptanan ve hPL (human plasental laktojen) boyası kuvvetli pozitif gelen hastada kemoterapiye direnç beklenmektedir. Bu hastada öncelikli küratif tedavi hangisidir?",
                options=[
                    {"key": "A", "text": "Tek ajanlı metotreksat kemoterapisi", "isCorrect": False, "explanation": "PSTT kemoterapiye dirençlidir; metotreksat ile kür sağlanamaz."},
                    {"key": "B", "text": "Cerrahi histerektomi", "isCorrect": True, "explanation": "Doğru. Plasental bölge trofoblastik tümörü (PSTT) kemoterapiye dirençli olduğundan primer küratif tedavi cerrahi histerektomidir."},
                    {"key": "C", "text": "Pelvik radyoterapi", "isCorrect": False, "explanation": "Radyoterapi primer tedavi değildir."},
                    {"key": "D", "text": "Hormon replasman tedavisi", "isCorrect": False, "explanation": "Hormon replasmanı tümörü tedavi etmez."}
                ],
                correct_key="B"
            ),
            make_cloze(
                sentence="Plasental bölge trofoblastik tümörü intermediate trofoblastlardan köken alır ve immünohistokimyasal incelemede belirgin hPL pozitifliği gösterir.",
                masked_term="hPL pozitifliği",
                hint="Human plasental laktojen hormonunun hücresel boyanması"
            ),
            make_slider(
                left_title="Gestasyonel Koryokarsinom",
                right_title="Plasental Bölge Trofoblastik Tümörü (PSTT)",
                left_points=[
                    "Sito ve sinsityotrofoblastların bifazik proliferasyonudur",
                    "Serum beta-hCG düzeyleri devasa boyutlarda yüksektir",
                    "Kemoterapiye son derece duyarlıdır (%100 kür; histerektomi şart değil)"
                ],
                right_points=[
                    "Yalnızca intermediate (ara) trofoblast hücrelerinden köken alır",
                    "Beta-hCG düşüktür; human plasental laktojen (hPL) diffüz pozitiftir",
                    "Kemoterapiye dirençlidir; primer küratif tedavi cerrahi histerektomidir"
                ]
            ),
            make_recall(
                question="Bir trofoblastik tümör olgusunda serum beta-hCG düzeyinin beklenmedik şekilde çok düşük kalması fakat patolojide intermediate trofoblastların görülmesi hangi antiteyi işaret eder?",
                answer="Plasental Bölge Trofoblastik Tümörünü (PSTT) işaret eder; intermediate trofoblastlar hPL salgılar, hCG üretimleri çok kısıtlıdır."
            )
        ]
    ))

    # Slide 79
    slides.append(make_slide(
        slide_num=79,
        title="Trofoblastik Hastalıklarda Tedavi Sonrası Gelecek Gebelikler ve Fertilite",
        subtitle="Kemoterapi sonrası reprodüktif sonuçlar ve tekrarlama riski",
        clinical_focus="Kür sağlanan genç kadınlarda over rezervi ve gebelik prognozu",
        narrative=(
            "Gestasyonel trofoblastik hastalıklar genç reprodüktif çağdaki kadınlarda görüldüğü için, tedavi sonrası fertilite beklentisi ve sonraki gebeliklerin güvenliği en sık sorulan klinik sorulardır.\n\n"
            "- **Over Fonksiyonları ve Fertilite:** Tek ajan (metotreksat) veya kombine kemoterapi (EMA-CO) alan kadınların ezici çoğunluğunda over fonksiyonları korunur. Tedavi tamamlandıktan sonra düzenli menstrüel sikluslar geri döner ve hastalar doğal yolla gebe kalabilir.\n"
            "- **Konsepsiyon Zamanlaması:** Kemoterapinin oositler üzerindeki olası mutajenik etkilerini ekarte etmek ve hCG takibini karıştırmamak için kemoterapiden sonra en az **12 ay boyunca** güvenilir kontrasepsiyon önerilir.\n"
            "- **Molar Tekrarlama Riski:** Bir kez mol hidatiform geçiren kadında genel popülasyona göre sonraki gebelikte mol riski hafif artar (%1-2); ancak olguların %98'inden fazlasında sonraki gebelikler tamamen sağlıklı ve normal seyreder.\n\n"
            "> [!NOTE]\n"
            "> Trofoblastik hastalık nedeniyle kemoterapi alan kadınlarda over rezervi korunur; 1 yıllık takip sonrasında sağlıklı normal gebelik şansı %98'in üzerindedir."
        ),
        bullets=[
            "Metotreksat veya EMA-CO sonrası over fonksiyonları ve doğurganlık korunur",
            "Tedavi bitiminden sonra 12 ay boyunca gebelik ertelenmelidir",
            "Önceki mol öyküsü sonraki gebelikte mol riskini sadece %1-2'ye çıkarır",
            "Hastaların %98'inde sonraki gebelikler komplikasyonsuz term doğumla sonuçlanır"
        ],
        elements=[
            make_quiz(
                question="Koryokarsinom tanısıyla sistemik kemoterapi alarak tam remisyona giren 25 yaşındaki bir kadın hastanın gelecekteki doğurganlık beklentisi ve sonraki gebelik planlaması hakkında en doğru bilgilendirme hangisidir?",
                options=[
                    {"key": "A", "text": "Kemoterapi nedeniyle hasta kalıcı kısırdır; asla gebe kalamaz.", "isCorrect": False, "explanation": "Yanlış. Trofoblastik kemoterapiler over rezervini yok etmez; fertilite korunur."},
                    {"key": "B", "text": "Tedavi biter bitmez aynı ay içinde korunmasız gebe kalmalıdır.", "isCorrect": False, "explanation": "Yanlış. En az 1 yıl kontrasepsiyon şarttır (oosit sağlığı ve nüks takibi)."},
                    {"key": "C", "text": "Sonraki tüm gebelikleri kesinlikle koryokarsinoma dönüşecektir.", "isCorrect": False, "explanation": "Yanlış. Tekrarlama riski son derece düşüktür (%1-2)."},
                    {"key": "D", "text": "Over fonksiyonları korunmuştur; 12 aylık nükssüz remisyon ve kontrasepsiyon döneminden sonra güvenle sağlıklı gebelik planlanabilir.", "isCorrect": True, "explanation": "Doğru. 1 yıllık takip sonrası hastaların %98'den fazlası sağlıklı normal çocuk sahibi olur."}
                ],
                correct_key="D"
            ),
            make_cloze(
                sentence="Kemoterapi ile tam kür sağlanan koryokarsinom hastalarında over fonksiyonları korunur ve bir yıllık nükssüz takip sonrasında sağlıklı gebelik elde edilebilir.",
                masked_term="sağlıklı gebelik",
                hint="Fertilitenin korunması sonucu normal term bebek doğurma durumu"
            ),
            make_swipe(
                title="Trofoblastik Tedavi Sonrası Klinik Doğrular ve Yanılgılar",
                left_category="Klinik Doğru Yaklaşım",
                right_category="Tıbbi Yanılgı / Hatalı İnanış",
                cards=[
                    {"text": "Kemoterapi bitiminden sonra en az 12 ay etkin kontrasepsiyon uygulanmalıdır", "category": "left", "explanation": "Nüks takibi ve oosit toparlanması için 1 yıl beklenir."},
                    {"text": "Koryokarsinom atlatan bir kadının gelecekteki tüm gebelikleri mol olmak zorundadır", "category": "right", "explanation": "Sonraki gebeliklerde tekrarlama riski sadece %1-2'dir; %98 normaldir."},
                    {"text": "Molar tahliye sonrası düşen hCG'yi izlemek için hasta hemen gebe kalmamalıdır", "category": "left", "explanation": "Erken gebelik hCG'yi yükselterek nüksle karışır."},
                    {"text": "Metotreksat tedavisi alan her genç kadın kalıcı olarak menopoza girer", "category": "right", "explanation": "Genç kadınlarda over fonksiyonları korunur; menopoz gelişmez."}
                ]
            ),
            make_recall(
                question="Koryokarsinom kemoterapisi sonrası hastaya neden 12 ay boyunca kesin gebelik yasağı (kontrasepsiyon) verilir?",
                answer="Erken bir gebelikte artacak olan fizyolojik beta-hCG'nin, olası bir tümör nüksüyle karışmasını önlemek ve oositlerin toksisiteden arınmasını sağlamak için."
            )
        ]
    ))

    # Slide 80 - Checkpoint 8
    slides.append(make_slide(
        slide_num=80,
        title="[TEKRAR SAYFASI - CHECKPOINT 8] Trofoblastik Hastalıkların Klinik ve Onkolojik Yönetimi",
        subtitle="Bölüm 8 Kapsamlı Pekiştirme ve Kazanım Kontrolü",
        clinical_focus="hCG takibi, metastaz yönetimi, kemoterapi yanıtı, PSTT ve acil durumlar",
        narrative=(
            "Bu tekrar sayfası, 71-79. adımlarda incelenen Gestasyonel Trofoblastik Hastalıkların Klinik, Laboratuvar ve Onkolojik Yönetimi kazanımlarını pekiştirmek için düzenlenmiştir.\n\n"
            "- **Beta-hCG İzlemi ve Persistan GTN:** Molar küretaj sonrası haftalık hCG değerlerinin plato çizmesi veya artması persistan GTN göstergesidir; invaziv mol veya koryokarsinoma işaret eder.\n"
            "- **Metastaz Yönetimi:** Koryokarsinom en sık akciğere (%50, hemoptizi) ve vajinaya yayılır. Mor-mavi vajinal nodüllerden biyopsi kontrendikedir (masif kanama riski). Beyin/karaciğer yüksek risk skorudur.\n"
            "- **Kemoterapi ve İmmünoloji:** Düşük riskte tek ajan metotreksat; yüksek riskte EMA-CO verilir. Paternal yabancı antijenler sayesinde koryokarsinom kemoterapi ile %100 kür şansına sahiptir.\n"
            "- **Özel Formlar ve Aciller:** Teka lutein kistleri selimdir, cerrahi yapılmaz ve spontan geriler. İnvaziv mol uterin rüptür ve şok yapabilir. PSTT intermediate trofoblast kökenlidir, beta-hCG düşük, hPL yüksek olup cerrahiyle tedavi edilir.\n\n"
            "> [!NOTE]\n"
            "> Vajinal nodülden biyopsi alınmaz; teka lutein kistine cerrahi dokunulmaz; koryokarsinom paternal antijenlerle %100 kür olur; PSTT intermediate trofoblast kökenli olup cerrahi tedavi edilir."
        ),
        bullets=[
            "Beta-hCG platosu/artışı: Persistan trofoblastik neoplazi kanıtıdır",
            "Vajinal koryokarsinom nodülü: Biyopsi kontrendikedir, kanama öldürücü olabilir",
            "Paternal antijenler: Koryokarsinoma kemoterapide devasa immün avantaj sağlar",
            "Teka lutein kistleri: Cerrahi gerektirmez; hCG düştükçe spontan rezolüsyona uğrar",
            "PSTT: Kemoterapiye dirençli, hPL pozitif intermediate trofoblast tümörüdür (histerektomi)"
        ],
        elements=[
            make_quiz(
                question="Gestasyonel trofoblastik hastalıkların klinik ve onkolojik yönetimi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                options=[
                    {"key": "A", "text": "Vajina ön duvarındaki mor-mavi koryokarsinom şüpheli nodülden kesin tanı için derin insizyonel biyopsi alınmalıdır.", "isCorrect": False, "explanation": "Yanlış. Vajinal lezyona biyopsi masif ölümcül kanama başlatır; tanı kanda beta-hCG ve radyoloji ile konur."},
                    {"key": "B", "text": "Molar gebelikte saptanan 10 cm'lik bilateral teka lutein kistlerine acil kistektomi yapılmalıdır.", "isCorrect": False, "explanation": "Yanlış. Teka lutein kistleri hormon çekilince kendiliğinden spontan geriler; dokunulmaz."},
                    {"key": "C", "text": "PSTT intermediate trofoblast kökenli olup hCG düşüktür ve kemorezistan olduğu için primer tedavisi histerektomidir.", "isCorrect": True, "explanation": "Doğru. PSTT intermediate trofoblastlardan köken alır, hPL pozitiftir, kemoterapiye dirençlidir ve cerrahi ile tedavi edilir."},
                    {"key": "D", "text": "Koryokarsinom tedavisinde paternal antijenlerin varlığı maternal immün sistemin tümörü korumasına neden olur.", "isCorrect": False, "explanation": "Yanlış. Paternal antijenler tümörü anneye yabancı kılarak immün yıkımı ve kemoterapi başarısını artırır."}
                ],
                correct_key="C"
            ),
            make_cloze(
                sentence="Plasental bölge trofoblastik tümörü kemoterapiye dirençli olduğu için primer tedavi yaklaşımı cerrahi histerektomidir.",
                masked_term="histerektomidir",
                hint="Uterusun operasyonla tamamen çıkarılması ameliyatı"
            ),
            make_table(
                title="Bölüm 8 Gestasyonel Trofoblastik Yönetim Matrisi",
                headers=["Klinik Tablo", "Tanısal / Biyolojik Özellik", "Temel Yönetim Prensibi"],
                rows=[
                    [
                        {"text": "Persistan Trofoblastik Hastalık", "isMasked": False},
                        {"text": "Beta-hCG plato çizmesi veya yükselmesi", "isMasked": True, "hint": "Ardışık haftalık ölçümlerde hormonal duraklama"},
                        {"text": "Metastaz taraması ve sistemik kemoterapi", "isMasked": False}
                    ],
                    [
                        {"text": "Teka Lutein Kistleri", "isMasked": False},
                        {"text": "Yüksek hCG'ye bağlı selim luteinizasyon", "isMasked": False},
                        {"text": "Cerrahi yapılmaz; spontan gerileme izlenir", "isMasked": True, "hint": "Hormon düşünce kistlerin kendi kendine küçülmesini bekleme"}
                    ],
                    [
                        {"text": "PSTT (Plasental Bölge)", "isMasked": False},
                        {"text": "Intermediate trofoblast; hPL pozitif", "isMasked": True, "hint": "Ara hücre tipi ve laktojenik hormon profili"},
                        {"text": "Cerrahi histerektomi (kemorezistandır)", "isMasked": False}
                    ]
                ]
            ),
            make_spot_the_lie(
                topic="Aşağıdaki önermelerden hangisi yanlıştır (tuzaktır)? Odak: Bölüm 8 Kontrol Önermeleri",
                items=[
                    {"text": "İnvaziv mol olgularında myometrium perforasyonu masif hemoperitoneum yapabilir.", "isLie": False, "explanation": "Doğru. Transmural erozyon intraabdominal kanama yapar."},
                    {"text": "Gestasyonel koryokarsinom paternal antijenler sayesinde kemoterapiyle %100'e yakın kür oranına sahiptir.", "isLie": False, "explanation": "Doğru. Allogreft immün sinerjisi kürü sağlar."},
                    {"text": "Plasental bölge trofoblastik tümörü (PSTT) devasa beta-hCG salgılar ve tek doz metotreksat ile tamamen iyileşir.", "isLie": True, "explanation": "Tuzak! PSTT'de beta-hCG düşüktür (hPL yüksektir) ve kemoterapiye dirençlidir; tedavisi histerektomidir."},
                    {"text": "Molar küretaj sonrası hastaya en az 6-12 ay güvenilir kontrasepsiyon önerilir.", "isLie": False, "explanation": "Doğru. Erken gebelik hCG takibini bozar."}
                ]
            ),
            make_recall(
                question="Checkpoint 8: Vajina duvarında koryokarsinoma ait mor-mavi nodül saptanan bir hastada neden kesinlikle doku biyopsisi alınmaz ve tanı nasıl kesinleştirilir?",
                answer="Tümör aşırı vasküler ve damar aşındırıcı olduğu için biyopsi durdurulamayan masif kanamaya yol açar; tanı kanda beta-hCG ve radyolojik görüntülemeyle invaziv girişim yapılmadan kesinleştirilir."
            )
        ],
        is_checkpoint=True,
        checkpoint_number=8
    ))

    return slides
