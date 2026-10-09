# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 20: Tromboz Patofizyolojisi (Prof. Dr. Hikmet Keleş)
Bölüm 8: Trombüs Morfolojisi, Zahn Çizgileri ve Trombüs Tipleri (Slayt 71 - 80)
Checkpoint 8: Slayt 79
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Trombüsün Morfolojik Tanımı ve Büyüme Yönü
    slides.append({
        "id": "k1-20-s71",
        "title": "Trombüsün Makroskobik Yapısı ve Büyüme Dinamiği",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 71,
        "narrative": (
            "Trombüs, canlı bir organizmada kardiyovasküler sistem lümeni içinde oluşan, damar veya "
            "endokard yüzeyine tutunmuş katı bir intravasküler kitledir. Trombüsün en karakteristik "
            "morfolojik özelliklerinden biri, başlangıçtaki endotel hasarı veya nidasus noktasına odaksal "
            "olarak yapışık olması ve oradan lümen boyunca uzanım (propagasyon) göstermesidir. "
            "Propagasyon yönü damar tipine göre farklılık gösterse de evrensel kural şudur: **Trombüsler daima kalbe doğru büyür!** "
            "Arteriyel sistemde kan akımı kalpten çevreye doğru olduğundan, arteriyel trombüs kan akımına zıt yönde (retrograd) kalbe doğru ilerler. "
            "Venöz sistemde ise kan akımı zaten kalbe doğru olduğundan, venöz trombüs akım yönünde (antegrad) kalbe doğru uzanır. "
            "Trombüsün damar duvarına tutunan 'kuyruk' kısmı akım yönünde dalgalanabilir ve koparak emboli oluşturma riski taşır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Arteriyel sistemde trombüsler kan akımına karşı retrograd yönde ilerlerken her iki sistemde de trombüsler daima kalbe doğru büyür.",
                "kalbe doğru",
                "Trombüsün arter ve venlerdeki ortak büyüme hedefi olan merkezi organ yönü"
            ),
            make_causal_chain(
                "Trombüs Büyümesi ve Kopma Mekanizması",
                [
                    "1. Endotel Hasarı: Damar duvarında fokal endotel denudasyonu ve trombosit agregasyonu başlar.",
                    "2. Nidasus Tutunması: Trombüs tabanı damar intimasına sıkıca ankoraj sağlar.",
                    "3. Propagasyon: Trombosit ve fibrin birikimiyle trombüs kitlesi kalbe doğru lümen boyunca uzanır.",
                    "4. Serbest Kuyruk: Akım içinde serbestçe salınan frajil kuyruk kısmı oluşur.",
                    "5. Embolizasyon Riski: Yüksek kayma gerilimi altında kuyruktan kopan fragmanlar distal dolaşıma sürüklenir."
                ]
            ),
            make_micro_quiz(
                "Arteriyel ve venöz trombüslerin büyüme yönü (propagasyon) ile ilgili hangisi doğrudur?",
                {
                    "A": "Arteriyel trombüsler akım yönünde, venöz trombüsler akıma zıt yönde büyür.",
                    "B": "Her iki trombüs tipi de daima periferik dokulara doğru uzanım gösterir.",
                    "C": "Arteriyel trombüs akıma zıt (retrograd), venöz trombüs akım yönünde (antegrad) olmak üzere ikisi de kalbe doğru büyür.",
                    "D": "Venöz trombüsler yerçekimi etkisiyle daima ayak bileğine doğru yayılım gösterir.",
                    "E": "Trombüsün büyüme yönü damar çapına bağlı olup akım yönünden bağımsızdır."
                },
                "C",
                {
                    "A": "A seçeneği yanlıştır; arterde akıma zıt, vende akım yönünde uzanır.",
                    "B": "B seçeneği yanlıştır; periferik dokulara değil, merkezi dolaşıma yani kalbe doğru büyürler.",
                    "C": "C seçeneği doğrudur: Arterde kan kalpten çıktığı için kalbe doğru büyüme retrograttır; vende kan kalbe gittiği için kalbe doğru büyüme antegrattır. Sonuçta ikisi de kalbe doğru uzanır.",
                    "D": "D seçeneği yanlıştır; venöz trombüsler yerçekimi yönünde değil, venöz akım doğrultusunda kalbe doğru ilerler.",
                    "E": "E seçeneği yanlıştır; propagasyon yönü hemodinamik akım vektörleri ile doğrudan ilişkilidir."
                }
            )
        ]
    })

    # Slayt 72: Zahn Çizgileri (Lines of Zahn)
    slides.append({
        "id": "k1-20-s72",
        "title": "Zahn Çizgileri (Lines of Zahn) ve Mikroskobik Katmanlaşma",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 72,
        "narrative": (
            "Trombüslerin hem makroskobik hem de mikroskobik incelemesinde saptanan en karakteristik "
            "yapısal özellik **Zahn Çizgileri (Lines of Zahn)** olarak adlandırılan laminasyonlardır. "
            "Bu çizgiler, açık ve koyu renkli tabakaların ritmik bir şekilde ardışık olarak dizilmesiyle oluşur. "
            "Açık renkli soluk katmanlar, aktive olmuş trombositler ve bunları saran fibrin ağlarından meydana gelir. "
            "Koyu renkli kırmızı katmanlar ise fibrin ağları arasına hapsolmuş eritrositlerden zengindir. "
            "Zahn çizgilerinin oluşabilmesi için ortamda mutlaka **akan bir kan akımı (hemodinamik kayma gerilimi)** bulunmalıdır. "
            "Bu nedenle Zahn çizgileri adli patoloji ve otopsi uygulamalarında hayati bir öneme sahiptir: "
            "Zahn çizgilerinin varlığı, pıhtının ölümden önce, yani dolaşımın aktif olduğu canlı evrede oluştuğunu kesin olarak kanıtlar! "
            "Ölüm sonrası (postmortem) durağan kanda gelişen pıhtılarda Zahn çizgileri asla izlenmez."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Zahn çizgilerinin açık renkli tabakaları trombosit ve fibrin ağlarından oluşurken koyu tabakaları eritrosit birikimini temsil eder.",
                "trombosit ve fibrin",
                "Açık renkli pıhtı katmanının hücresel ve protein yapısı"
            ),
            make_before_after(
                "Zahn Çizgilerinin Katman Özellikleri",
                "Açık Renkli Katmanlar",
                [
                    "Esas bileşen: Trombosit agregatları ve fibrin lifleri",
                    "Görünüm: Soluk pembe-beyaz laminasyonlar",
                    "Oluşum: Akım altındaki yüzeye primer trombosit tutunması"
                ],
                "Koyu Renkli Katmanlar",
                [
                    "Esas bileşen: Eritrosit zengini hücresel alanlar",
                    "Görünüm: Koyu kırmızı-kahverengi laminasyonlar",
                    "Oluşum: Fibrin ağları arasına pasif eritrosit sekestrasyonu"
                ]
            ),
            make_active_recall(
                "Bir damar lümenindeki intravasküler kitlenin ölümden önce (antemortem) oluştuğunu kesinleştiren temel histopatolojik bulgu nedir?",
                "Zahn çizgilerinin (ardışık trombosit-fibrin ve eritrosit katmanlarının) saptanmasıdır.",
                "Akan kan laminasyonu morfolojik belirtisi"
            )
        ]
    })

    # Slayt 73: Arteriyel Trombüsler (Beyaz Pıhtı)
    slides.append({
        "id": "k1-20-s73",
        "title": "Arteriyel Trombüsler: Beyaz Trombüsün Patolojik Nitelikleri",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 73,
        "narrative": (
            "Arteriyel trombüsler tipik olarak yüksek hızlı ve yüksek basınçlı akım alanlarında, "
            "endotel hasarı ve türbülans zemininde gelişir. En sık aterosklerotik plak rüptürü veya erozyonu "
            "sonucunda koroner arterler, serebral arterler (örneğin orta serebral arter) ve femoral arterlerde görülür. "
            "Yüksek akım hızları nedeniyle eritrositlerin pıhtı içine hapsolması güçtür; bu yüzden arteriyel trombüsler "
            "temel olarak trombosit agregatları ve sıkı fibrin ağlarından oluşur. Bu morfolojik özelliklerinden ötürü "
            "arteriyel trombüslere sıklıkla **beyaz trombüs** adı verilir. "
            "Arteriyel trombüsler genellikle damar duvarına sıkıca yapışık olup lümeni kısmen veya tamamen tıkayarak (oklüzyon) "
            "besledikleri distal parankimde akut iskemik enfarktüslere (örneğin akut miyokard enfarktüsü veya iskemik inme) yol açarlar. "
            "Tedavide antiplatelet ajanların (aspirin, P2Y12 blokerleri) ön planda olmasının nedeni de arteriyel trombüslerin trombosit zengin yapısıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_table(
                ["Arteriyel Trombüs Özelliği", "Patolojik Detay", "Klinik Yansıması"],
                [
                    ["Predispozan Faktör", "Endotel hasarı ve ateroskleroz", "Akut koroner sendrom ve inme riski"],
                    [
                        "Bileşim Yapısı",
                        {"text": "Trombosit ve fibrin zengin", "isMasked": True, "hint": "Beyaz pıhtı lakabını veren hücresel yapı"},
                        "Antiplatelet tedavilere yüksek yanıt"
                    ],
                    ["Makroskobik Renk", "Soluk gri-beyaz ve sert kıvam", "Lümene sıkıca ankoraj yapmış kitle"],
                    ["Akım Dinamiği", "Yüksek basınçlı, hızlı akım", "Retrograd kalbe doğru yavaş uzanım"]
                ]
            ),
            make_micro_quiz(
                "Arteriyel trombüslerin patogenezi ve morfolojisi ile ilgili hangisi yanlıştır?",
                {
                    "A": "En sık aterosklerotik plak zemininde endotel hasarı sonucu oluşur.",
                    "B": "Bileşiminde trombosit ve fibrin baskın olduğu için beyaz trombüs olarak anılır.",
                    "C": "Koroner ve serebral arterlerde distal doku iskemisine yol açar.",
                    "D": "Oluşumunda temel faktör venöz staz olup eritrosit içeriği venöz trombüsten yüksektir.",
                    "E": "Trombüs kitlesi damar duvarına sıkıca yapışıktır."
                },
                "D",
                {
                    "A": "A seçeneği doğrudur; aterosklerotik plak yırtılması arteriyel trombozun 1 numaralı nedenidir.",
                    "B": "B seçeneği doğrudur; trombosit agregatları soluk-beyaz rengi verir.",
                    "C": "C seçeneği doğrudur; oklüzyon kalp kasında veya beyinde enfarktüse yol açar.",
                    "D": "D seçeneği yanlıştır: Arteriyel trombüslerin temel nedeni venöz staz değil endotel hasarıdır; eritrosit içeriği venöz trombüsten belirgin şekilde düşüktür.",
                    "E": "E seçeneği doğrudur; hasarlı endotel ve subendotelyal matrikse sıkıca ankoraj yapmıştır."
                }
            )
        ]
    })

    # Slayt 74: Venöz Trombüsler (Kırmızı Pıhtı / Staz Trombüsü)
    slides.append({
        "id": "k1-20-s74",
        "title": "Venöz Trombüsler: Kırmızı Trombüs ve Flebotromboz",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 74,
        "narrative": (
            "Venöz trombüsler (flebotromboz), düşük basınçlı ve yavaş akımlı venöz sistemde, "
            "neredeyse değişmez bir şekilde **staz ve hiperkoagülabilite** zemininde meydana gelir. "
            "Olguların %90'ından fazlası alt ekstremite derin venlerinde (femoral, popliteal ve iliak venler) ortaya çıkar. "
            "Venöz dolaşımdaki akım hızı son derece düşük olduğundan, aktive olan pıhtılaşma kaskadı boyunca "
            "geniş fibrin ağları örülür ve bu ağların arasına muazzam miktarda eritrosit hapsolur. "
            "Bu nedenle venöz trombüsler koyu kırmızı, jelatinimsi-nemli bir görünüme sahiptir ve **kırmızı trombüs (staz pıhtısı)** olarak adlandırılır. "
            "Venöz trombüsler neredeyse daima ven lümenini tamamen tıkayıcı (oklüziv) niteliktedir. "
            "Pıhtının kuyruk kısmı venöz akım yönünde (kalbe doğru) serbestçe uzanır; bu gevşek uzantının kopması "
            "ölümcül pulmoner tromboembolizm tablosuna zemin hazırlar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Venöz trombüsler düşük akım hızı nedeniyle yoğun eritrosit sekestrasyonu içerdiğinden kırmızı trombüs olarak adlandırılır.",
                "kırmızı trombüs",
                "Staz zemininde gelişen venöz pıhtının makroskobik adı"
            ),
            make_before_after(
                "Arteriyel Trombüs ile Venöz Trombüs Karşılaştırması",
                "Arteriyel Trombüs (Beyaz)",
                [
                    "Başlatıcı faktör: Endotel hasarı ve türbülans",
                    "Temel bileşen: Trombosit agregatları ve fibrin",
                    "Akım özellikleri: Yüksek hızlı, yüksek basınçlı akım",
                    "Temel klinik sonuç: Distal doku enfarktüsü (MI, inme)"
                ],
                "Venöz Trombüs (Kırmızı)",
                [
                    "Başlatıcı faktör: Venöz staz ve hiperkoagülabilite",
                    "Temel bileşen: Eritrosit zengin, gevşek fibrin ağı",
                    "Akım özellikleri: Yavaş, düşük basınçlı staz akımı",
                    "Temel klinik sonuç: Pulmoner emboli ve staz ödemi"
                ]
            ),
            make_active_recall(
                "Venöz trombüslerin en sık yerleştiği vasküler yatak neresidir?",
                "Alt ekstremite derin venleridir (özellikle vena femoralis ve vena poplitea).",
                "DVT'nin en tipik anatomik lokalizasyonu"
            )
        ]
    })

    # Slayt 75: Mural Trombüsler
    slides.append({
        "id": "k1-20-s75",
        "title": "Mural Trombüsler: Kardiyak Odacıklar ve Aortik Yerleşim",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 75,
        "narrative": (
            "Geniş lümenli kardiyak boşlukların veya aort gibi dev damarların duvarına yapışık, "
            "lümeni tamamen tıkamayan ancak duvar üzerinde kitle oluşturan trombüslere **mural trombüs** denir. "
            "Mural trombüs gelişiminde iki temel kardiyak zemin bulunur: "
            "Birincisi, transmural miyokard enfarktüsü (MI) sonrasında apikal ventrikül duvarında gelişen diskinezi/akinezi "
            "ve buna eşlik eden endokardiyal hasarlanmadır (sol ventrikül mural trombüsü). "
            "İkincisi, atriyal fibrilasyon veya mitral kapak darlığına bağlı sol atriyal dilatasyon ve kan stazıdır (özellikle sol atriyal apendikste). "
            "Vasküler sistemde ise ileri derecede aterosklerotik abdominal aort anevrizmalarında ve asendan aort anevrizmalarında "
            "oluşan dev türbülans girdapları mural trombüslere zemin hazırlar. "
            "Mural trombüslerin en korkulan klinik sonucu, üzerlerinden kopan parçaların sistemik arteriyel dolaşıma karatarak "
            "beyin, böbrek, dalak ve ekstremitelerde embolik enfarktüslere yol açmasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Miyokard enfarktüsü sonrası sol ventrikül apeksinde duvar disfonksiyonu ve hasarlı endokard üzerinde mural trombüs gelişir.",
                "mural trombüs",
                "Kalp odacığı veya aort duvarına yapışık kitle oluşturan trombüs tipi"
            ),
            make_causal_chain(
                "Sol Ventrikül Mural Trombüsü Patogenezi",
                [
                    "1. Anterior MI: Sol ön inen arter oklüzyonu ile ventrikül apeksinde transmural enfarktüs gelişir.",
                    "2. Akinezi ve Hasar: Apeksteki miyokard kasılamaz (akinezi) ve endokard örtüsü nekroze olur.",
                    "3. Kan Stazı: Apeks apeksinde akım girdabı duraklar ve trombosit adezyonu tetiklenir.",
                    "4. Mural Kitle: Endokard yüzeyine geniş tabanlı mural trombüs yerleşir.",
                    "5. Sistemik Emboli: Trombüsten kopan embolus karotis sistemi üzerinden beyne ulaşarak inmeye yol açar."
                ]
            ),
            make_micro_quiz(
                "Mural trombüslerin gelişimi için en karakteristik predispozan klinik durum hangisidir?",
                {
                    "A": "Derin ven kapak yetersizliği",
                    "B": "Akut anterior miyokard enfarktüsü ve sol ventrikül akinetik apeksi",
                    "C": "Von Willebrand hastalığı",
                    "D": "Primer trombositopenik purpura",
                    "E": "Karaciğer yetmezliğine bağlı hipoalbüminemi"
                },
                "B",
                {
                    "A": "A seçeneği venöz trombüslere zemin hazırlar, mural kardiyak trombüs oluşturmaz.",
                    "B": "B seçeneği doğrudur: Transmural enfarktüs endokard hasarı ve ventrikül akinezisi yaratarak sol ventrikül apeksinde mural trombüs oluşumunun prototipik nedenidir.",
                    "C": "C seçeneği kanama diyatezidir, trombozu kolaylaştırmaz.",
                    "D": "D seçeneğinde trombositopeni mevcuttur, mural tromboz tipi görülmez.",
                    "E": "E seçeneği asit ve ödem yapar, mural trombüsle doğrudan ilişkili değildir."
                }
            )
        ]
    })

    # Slayt 76: Kalp Kapağı Vejetasyonları
    slides.append({
        "id": "k1-20-s76",
        "title": "Kalp Kapağı Vejetasyonları: Enfektif, Marantik ve Libman-Sacks",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 76,
        "narrative": (
            "Kalp kapakları üzerinde oluşan trombotik kitlelere **vejetasyon** adı verilir. "
            "Vejetasyonlar etiyolojik, mikrobiyolojik ve immünolojik özelliklerine göre 3 temel gruba ayrılır: "
            "1. **Enfektif Endokardit:** Bakteriyel veya fungal etkenlerin hasarlı veya sağlam kapağa yerleşmesiyle oluşur. "
            "Büyük, düzensiz, frajil kitlelerdir; mikroorganizma kolonileri içerir ve kapak dokusunda belirgin destrüksiyona (yırtılma, perforasyon) neden olur. "
            "2. **Non-Bakteriyel Trombotik Endokardit (NBTE / Marantik Endokardit):** İlerlemiş kanser (özellikle müsin üreten adenokarsinomlar) "
            "veya kronik tükenmişlik (kaşeksi) durumlarındaki hiperkoagülabilite zemininde gelişir. Kapanma çizgisi boyunca dizilen, steril, küçük ve kapak hasarı yapmayan kitlelerdir. "
            "3. **Libman-Sacks Endokarditi:** Sistemik Lupus Eritematozus (SLE) ve antifosfolipid sendromunda görülür. "
            "En belirgin ayırt edici özelliği, **kapak yaprakçıklarının her iki yüzünde (hem inflow hem outflow yüzeylerinde)** "
            "ve korda tendinea üzerinde küçük, steril, verrüköz nodüller şeklinde yerleşmesidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_table(
                ["Vejetasyon Tipi", "Etiyoloji ve Mikrobiyoloji", "Kapak Tutulumu ve Morfoloji"],
                [
                    ["Enfektif Endokardit", "Bakteri veya mantar kolonizasyonu", "Büyük, frajil, kapağı tahrip eden destrüktif kitle"],
                    [
                        "Marantik (NBTE)",
                        {"text": "Müsinöz karsinom ve kaşeksi", "isMasked": True, "hint": "Trousseau sendromu ile ilişkili durum"},
                        "Steril, kapanma çizgisinde küçük trombotik nodüller"
                    ],
                    ["Libman-Sacks", "SLE ve antifosfolipid sendromu", "Steril, kapağın her iki yüzünde verrüköz lezyonlar"]
                ]
            ),
            make_micro_quiz(
                "Sistemik Lupus Eritematozus (SLE) hastasında kapak yaprakçıklarının hem alt hem üst yüzeylerinde saptanan steril vejetasyon tipi hangisidir?",
                {
                    "A": "Akut bakteriyel endokardit",
                    "B": "Subakut bakteriyel endokardit",
                    "C": "Libman-Sacks endokarditi",
                    "D": "Marantik endokardit",
                    "E": "Romatizmal kapak tutulumu"
                },
                "C",
                {
                    "A": "A seçeneğinde bakteriyel kolonizasyon ve kapak destrüksiyonu vardır, lezyonlar steril değildir.",
                    "B": "B seçeneği Streptococcus viridans kaynaklı mikrobiyal enfeksiyondur.",
                    "C": "C seçeneği doğrudur: Libman-Sacks endokarditi SLE hastalarında görülür ve kapağın her iki yüzünü tutan steril verrüköz vejetasyonlarla karakterizedir.",
                    "D": "D seçeneğinde vejetasyonlar sadece kapağın kapanma çizgisi boyunca dizilir, iki yüzde birden görülmez.",
                    "E": "E seçeneğinde Asheroff cisimcikleri ve kapanma çizgisi boyunca küçük nodüller izlenir."
                }
            )
        ]
    })

    # Slayt 77: Gerçek Trombüs vs Ölüm Sonrası (Postmortem) Pıhtı Ayrımı
    slides.append({
        "id": "k1-20-s77",
        "title": "Gerçek Trombüs ile Postmortem (Ölüm Sonrası) Pıhtı Ayrımı",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 77,
        "narrative": (
            "Otopsi ve adli patoloji uygulamalarında lümen içindeki bir kitlenin ölümden önce mi (antemortem trombüs) "
            "yoksa ölümden sonra kanın durağanlaşmasıyla mı (postmortem pıhtı) oluştuğunun ayrımı hayati önem taşır. "
            "Bu ayrımda 4 temel kriter kullanılır: "
            "1. **Duvara Tutunma:** Gerçek trombüs hasarlı endotel zemininde başladığı için damar duvarına sıkıca ankoraj yapmıştır, "
            "sıyrılmaya çalışıldığında endotelde yırtılma veya pürüzlü taban bırakır. Postmortem pıhtı ise duvara asla tutunmaz; damar açıldığında lümenden kalıp gibi kolayca sıyrılır. "
            "2. **Kıvam ve Yüzey:** Gerçek trombüs kuru, granüler ve kırılgandır. Postmortem pıhtı ise yumuşak, jelatinöz ve elastiktir. "
            "3. **Laminasyon (Zahn Çizgileri):** Gerçek trombüste akım altında oluşan açık/koyu Zahn çizgileri mevcuttur. Postmortem pıhtıda Zahn çizgisi bulunmaz. "
            "4. **Renk ve Tabakalaşma:** Postmortem pıhtıda yerçekimiyle eritrositler tabana çöker (**frenk üzümü jölesi / currant jelly**), "
            "üstte berrak fibrinojen-plazma tabakası kalır (**tavuk yağı / chicken fat**). Gerçek trombüste bu tabakalaşma görülmez."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Postmortem pıhtılarda yerçekimiyle eritrositlerin çökmesi alt kısımda frenk üzümü jölesi üst kısımda tavuk yağı görünümü oluşturur.",
                "tavuk yağı",
                "Postmortem pıhtının üst sarımtırak plazma katmanının makroskobik adı"
            ),
            make_before_after(
                "Antemortem Trombüs ile Postmortem Pıhtı Ayrımı",
                "Antemortem Trombüs (Canlıda)",
                [
                    "Damar duvarına ankoraj: Sıkıca yapışık, ayrılırken tabanda hasar bırakır",
                    "Kıvam ve yüzey: Kuru, mat, granüler ve frajil yapı",
                    "İç laminasyon: Belirgin Zahn çizgileri (eritrosit/fibrin tabakaları)",
                    "Sedimantasyon: Yerçekimine bağlı tabakalaşma göstermez"
                ],
                "Postmortem Pıhtı (Ölüm Sonrası)",
                [
                    "Damar duvarına ankoraj: Duvara yapışmaz, lümenden kalıp gibi kolayca çıkar",
                    "Kıvam ve yüzey: Nemli, parlak, elastik ve jelatinöz yapı",
                    "İç laminasyon: Zahn çizgileri tamamen negatiftir",
                    "Sedimantasyon: Alt kısım 'frenk üzümü jölesi', üst kısım 'tavuk yağı' tabakalı"
                ]
            ),
            make_active_recall(
                "Otopsi sırasında femoral venden çıkarılan bir kitlenin duvara yapışmadığı, jelatinöz kıvamda olduğu ve üst kısmının tavuk yağı renginde olduğu saptanmıştır. Bu kitle nedir?",
                "Ölüm sonrası gelişen postmortem pıhtıdır (antemortem trombüs değildir).",
                "Durağan kanda sedimantasyonla oluşan pıhtı tanısı"
            )
        ]
    })

    # Slayt 78: Trombüs ve Vejetasyon Komplikasyonları
    slides.append({
        "id": "k1-20-s78",
        "title": "Trombüslerin Sistemik Komplikasyonları ve Klinik Sonuçları",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 78,
        "narrative": (
            "İntravasküler trombüsler ve kardiyak vejetasyonlar insan vücudunda iki ana patolojik mekanizma üzerinden ağır hasarlara yol açar: "
            "Birincisi, damar lümenini yerel olarak tamamen tıkamaları (vasküler obstrüksiyon) sonucunda ilgili organ veya dokunun kanlanmasını durdurarak "
            "iskemik nekroz ve enfarktüse neden olmalarıdır. Miyokard enfarktüsü ve iskemik inme bu tablonun en yaygın örnekleridir. "
            "İkincisi ise trombüsün frajil parçalarının kan akımının kinetik kuvvetiyle koparak distal damar ağlarına taşınmasıdır (tromboembolizm). "
            "Sol kalp boşlukları, aorta veya karotis arterlerdeki trombüslerden kopan emboluslar sistemik arteriyel dolaşıma karatarak "
            "serebral arterleri, mezenterik damarları, renal arterleri ve alt ekstremite periferik arterlerini tıkayarak yaygın organ yetmezliklerine yol açar. "
            "Sağ kalp veya periferik derin venlerdeki trombüsler ise pulmoner arter ağını tıkayarak ani sağ kalp yetmezliği ve ölüme neden olur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Sol ventrikül mural trombüsünden kopan embolus sistemik arteriyel dolaşıma katılarak sıklıkla serebral arterleri tıkayıp inmeye yol açar.",
                "sistemik arteriyel",
                "Sol kalpten çıkan embolusların izlediği vasküler dolaşım yolu"
            ),
            make_causal_chain(
                "Kardiyak Trombüsten Sistemik Enfarktüse Zincir",
                [
                    "1. Sol Atriyal Apendiks Stazı: Atriyal fibrilasyonda kan göllenmesiyle trombüs oluşur.",
                    "2. Fragmantasyon: Trombüsten makroembolus koparak sol ventriküle geçer.",
                    "3. Aortik Fırlatma: Embolus çıkan aorta ve arkus aortadan karotis sistemine atılır.",
                    "4. Serebral Oklüzyon: Sol orta serebral arter dalında ani mekanik tıkanma gerçekleşir.",
                    "5. İskemik Enfarktüs: İlgili beyin parankiminde sıvılaşma nekrozu ve hemipleji gelişir."
                ]
            ),
            make_branching_logic(
                "Atriyal fibrilasyon öyküsü olan 72 yaşındaki hastada ani başlayan sağ kol ve bacakta güçsüzlük ve konuşma bozukluğu gelişmiştir. Beyin BT'de sol orta serebral arter sulama alanında akut enfarktüs saptanmıştır.",
                "Bu tablonun en olası patolojik mekanizması ve kaynağı nedir?",
                [
                    {
                        "key": "A",
                        "text": "Sol atriyal mural trombüsten kopan sistemik kardiyoembolizm",
                        "isCorrect": True,
                        "explanation": "Doğru karar: Atriyal fibrilasyonda sol atriyal apendikste oluşan trombüs sistemik dolaşıma embolize olarak serebral enfarktüse yol açar."
                    },
                    {
                        "key": "B",
                        "text": "Derin ven trombozundan kaynaklanan pulmoner embolizm",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: DVT'den kopan embolus pulmoner dolaşıma gider, intrakardiyak şant yoksa sol kalbe ve beyne geçemez."
                    },
                    {
                        "key": "C",
                        "text": "Asendan aorta mural trombüsünün pulmoner vene retrograd kaçışı",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: Aorttaki pıhtı pulmoner vene retrograd geçmez."
                    },
                    {
                        "key": "D",
                        "text": "Sağ ventrikül yetmezliğine bağlı venöz konjesyon",
                        "isCorrect": False,
                        "explanation": "Yanlış karar: Sağ ventrikül yetmezliği fokal fokal iskemik kortikal enfarktüs yapmaz."
                    }
                ]
            )
        ]
    })

    # Slayt 79: [TEKRAR SAYFASI - CHECKPOINT 8]
    slides.append({
        "id": "k1-20-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Trombüs Morfolojisi ve Tipleri",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 79,
        "narrative": (
            "Bu tekrar sayfasında trombüslerin makroskobik ve mikroskobik morfolojik niteliklerini, "
            "Zahn çizgilerinin ayırıcı tanıdaki adli ve histopatolojik değerini, "
            "arteriyel (beyaz) ve venöz (kırmızı) trombüslerin temel farklarını ve postmortem pıhtı ayrımını "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-20-cp8-1",
                "Zahn çizgileri histopatolojik olarak hangi iki tabakanın ardışık diziliminden oluşur ve klinik anlamı nedir?",
                "Açık renkli trombosit-fibrin katmanları ile koyu renkli eritrosit katmanlarının ardışık dizilimidir. Pıhtının akan kanda ve antemortem (canlıda) oluştuğunu kanıtlar.",
                "Soluk ve eritrositer katmanlar ile dolaşım canlılığı ilişkisi",
                "Trombüs Morfolojisi"
            ),
            make_flashcard(
                "fc-k1-20-cp8-2",
                "Postmortem pıhtıyı gerçek antemortem trombüsten ayıran en belirgin makroskobik özellikler nelerdir?",
                "Postmortem pıhtı duvara yapışmaz, jelatinöz-nemlidir, Zahn çizgisi içermez; yerçekimiyle çöken alt kırmızı (frenk üzümü) ve üst sarı plazma (tavuk yağı) tabakası gösterir.",
                "Duvara tutunmama ve tavuk yağı görünümü",
                "Otopsi ve Adli Patoloji"
            ),
            make_flashcard(
                "fc-k1-20-cp8-3",
                "SLE hastalarında görülen Libman-Sacks endokarditini marantik endokardit ve enfektif endokarditten ayıran temel morfolojik özellik nedir?",
                "Kapak yaprakçıklarının her iki yüzünde (hem üst hem alt yüzeyinde) yerleşen küçük, verrüköz ve steril vejetasyonlar olmasıdır.",
                "Çift yüzey tutulumlu steril verrüköz odaklar",
                "Kapak Patolojisi"
            )
        ]
    })

    # Slayt 80: Bölüm Özeti ve Akıbete Geçiş
    slides.append({
        "id": "k1-20-s80",
        "title": "Trombüs Morfolojisi Özeti: Dinamiklerden Trombüsün Akıbetine",
        "section": "Trombüs Morfolojisi ve Tipleri",
        "slideNumber": 80,
        "narrative": (
            "Özetle; trombüsler damar intimasına veya endokarda tutunmuş, lümen içine doğru büyüyen patolojik intravasküler kitlelerdir. "
            "Arteriyel trombüsler endotel hasarı zemininde hızla akan kanda trombosit-fibrin agregatlarıyla (beyaz pıhtı) oluşurken; "
            "venöz trombüsler staz ve hiperkoagülabilite zemininde yavaş akımda eritrosit sekestrasyonuyla (kırmızı pıhtı) meydana gelir. "
            "Her iki sistemde de trombüsler daima kalbe doğru büyüme eğilimi gösterir. "
            "Mural trombüsler kalp boşluklarında ve anevrizmalarda kitle oluşturarak ölümcül sistemik embolilere yol açabilir. "
            "Kalp kapaklarında gelişen vejetasyonlar ise enfeksiyöz destrüksiyon veya immünolojik kompleksler (Libman-Sacks) sonucu ortaya çıkar. "
            "Bir damar veya kalp odacığında oluşan bir trombüsün ömrü statik değildir; bir sonraki bölümde inceleyeceğimiz üzere "
            "trombüs büyüyecek, embolize olacak, lizise uğrayacak veya organize olarak damar duvarına kaynaşacaktır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Tromboz Patofizyolojisi Ders Notları",
        "interactiveElements": [
            make_cloze(
                "Trombüsler ister arterde akıma zıt ister vende akım yönünde olsun daima kalbe doğru uzanım gösterir.",
                "kalbe doğru",
                "Tüm trombüslerin evrensel anatomik yayılım hedefi"
            ),
            make_table(
                ["Patolojik Trombüs Tipi", "Başlatıcı Zemin", "Temel Komplikasyon"],
                [
                    ["Koroner Arter Trombüsü", "Aterom plak rüptürü ve trombosit aktivasyonu", "Transmural Miyokard Enfarktüsü"],
                    [
                        "Derin Ven Trombüsü (DVT)",
                        {"text": "Venöz staz ve hiperkoagülabilite", "isMasked": True, "hint": "Virchow triyadının staz ve kan bileşimi ayağı"},
                        "Ölümcül Masif Pulmoner Emboli"
                    ],
                    ["Sol Ventrikül Mural Trombüsü", "MI sonrası apikal akinezi ve endokard hasarı", "Serebral ve Periferik Sistemik Embolizm"]
                ]
            ),
            make_micro_quiz(
                "Trombüs morfolojisi ve tipleriyle ilgili aşağıdaki ifadelerden hangisi tamamen doğrudur?",
                {
                    "A": "Venöz trombüslerde eritrosit oranı arteriyel trombüslere göre çok düşüktür.",
                    "B": "Postmortem pıhtılarda Zahn çizgileri antemortem trombüslere göre çok daha belirgindir.",
                    "C": "Arteriyel trombüsler akıma zıt yönde, venöz trombüsler akım yönünde kalbe doğru uzanır.",
                    "D": "Marantik endokardit vejetasyonları yüksek derecede bakteriyel mikrokoloni içerir.",
                    "E": "Mural trombüsler daima venöz kapak ceplerinde oluşur."
                },
                "C",
                {
                    "A": "A seçeneği yanlıştır; venöz trombüsler eritrositten çok zengindir.",
                    "B": "B seçeneği yanlıştır; postmortem pıhtıda Zahn çizgisi hiç bulunmaz.",
                    "C": "C seçeneği doğrudur: İki sistemde de yayılım yönü merkezi dolaşıma yani kalbe doğrudur.",
                    "D": "D seçeneği yanlıştır; marantik endokardit (NBTE) lezyonları sterildir.",
                    "E": "E seçeneği yanlıştır; mural trombüsler kalp odacıkları ve geniş arterlerde duvara yapışık gelişir."
                }
            )
        ]
    })

    return slides
