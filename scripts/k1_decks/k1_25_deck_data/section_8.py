# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 8: Primer İmmün Yetmezlik Sendromları (Slayt 71 - 80)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_8_slides():
    slides = []

    # Slayt 71: Primer İmmün Yetmezliklerin Genel Sınıflandırması
    slides.append({
        "id": "k1-25-s71",
        "title": "Primer İmmün Yetmezliklerin Genel Sınıflandırması ve Klinik İpuçları",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 71,
        "narrative": (
            "Primer immün yetmezlikler, bağışıklık sisteminin gelişimini ve fonksiyonunu yöneten genlerdeki "
            "doğuştan (konjenital) mutasyonlar sonucu ortaya çıkan kalıtsal hastalıklardır: "
            "1. **Maternal Antikor Kalkanı (İlk 6 Ay):** Yenidoğan bebek ilk 6 ay boyunca plasentadan geçen maternal IgG "
            "antikorları sayesinde korunur. Bu nedenle hümoral (B hücresi) kusurları genellikle 6. aydan sonra, "
            "maternal antikorlar tükendiğinde tekrarlayan enfeksiyonlarla klinik verir. "
            "2. **Patojen İpuçları:** "
            "- **B Hücre / Antikor Kusurları:** Kapsüllü piyojenik bakteriler (Streptococcus pneumoniae, Haemophilus influenzae) "
            "ve enterovirüslerle rekürren sinopulmoner enfeksiyonlar (otit, sinüzit, pnömoni). "
            "- **T Hücre Kusurları:** Fırsatçı mantarlar (Candida, Pneumocystis jirovecii), hücre içi virüsler (CMV, HSV) ve mikobakteriler. "
            "- **Fagosit Kusurları:** Katalaz pozitif bakterilerle cilt ve organ apseleri."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "İmmün Yetmezlik Tipine Göre Patojen Dağılımı",
                ["Kusurlu İmmün Bileşen", "Karakteristik Patojen Ajanlar", "Tipik Enfeksiyon Tablosu", "Başlangıç Zamanı"],
                [
                    ["B Lenfositleri (Antikorlar)", "S. pneumoniae, H. influenzae, Enterovirüsler", "Tekrarlayan sinüzit, otitis media, pnömoni", "6. aydan sonra (Maternal IgG bitince)"],
                    [
                        "T Lenfositleri (Hücresel)",
                        "Pneumocystis jirovecii, Candida, CMV, Mikobakteri",
                        {"text": "Fırsatçı enfeksiyonlar, inatçı moniliyazis", "isMasked": True, "hint": "Hücresel bağışıklık çöküşünde ortaya çıkan fırsatçı mantar/virüs tablosu"},
                        "Erken yenidoğan dönemi (İlk aylar)"
                    ],
                    ["Fagositler (Nötrofiller)", "S. aureus, Aspergillus, Serratia, Pseudomonas", "Tekrarlayan derin organ apseleri, granülomlar", "Erken çocukluk"],
                    ["Kompleman (MAC / C5-9)", "Neisseria meningitidis ve N. gonorrhoeae", "Tekrarlayan fulminan meningokoksemi", "Her yaşta"]
                ]
            ),
            make_active_recall(
                "Konjenital B hücresi ve antikor eksikliği olan bebeklerde klinik enfeksiyonların doğumdan hemen sonra değil, genellikle 6. aydan sonra başlamasının nedeni nedir?",
                "Plasenta yoluyla geçen maternal IgG antikorlarının ilk 6 ay koruyuculuk sağlamasıdır.",
                "Anne karnından bebeğe aktarılan pasif hümoral koruma kalkanı"
            )
        ]
    })

    # Slayt 72: B Hücre Kusurları 1: X'e Bağlı Agamaglobulinemi (Bruton Hastalığı)
    slides.append({
        "id": "k1-25-s72",
        "title": "B Hücre Kusurları 1: X'e Bağlı Agamaglobulinemi (Bruton Hastalığı)",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 72,
        "narrative": (
            "Bruton agamaglobulinemisi, B lenfosit olgunlaşmasının pre-B evresinde kilitlendiği klasik X'e bağlı hastalıktır: "
            "1. **Genetik Defekt:** Xq22 lokusunda yer alan **Bruton Tirozin Kinaz (BTK)** gen mutasyonudur (yalnızca erkek çocuklarda görülür). "
            "BTK enzimi pre-B hücre reseptöründen gelen olgunlaşma sinyalini iletemez; pre-B hücreleri matür B lenfositlerine dönüşemez. "
            "2. **İmmünopatoloji ve Laboratuvar:** "
            "- Periferik kanda matür B lenfositleri (**CD19 ve CD20 pozitif hücreler**) ve dokularda plazma hücreleri **tamamen YOKTUR**. "
            "- Serumda tüm immünoglobulin sınıfları (**IgG, IgA, IgM, IgE**) sıfıra yakındır. "
            "3. **Morfoloji:** Lenf nodu korteksinde germinal merkezler gelişemez; dalak folikülleri ve tonsiller hipoplastiktir (bademcikler yoktur). "
            "4. **Klinik:** 6. aydan sonra tekrarlayan kapsüllü bakteri pnömonileri ve Giardia diyareleri görülür; hücresel T immünitesi intakttır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Bruton Hastalığı Gelişim Zinciri",
                [
                    "1. BTK Gen Mutasyonu: X kromozomundaki sitoplazmik tirozin kinaz enziminin fonksiyonunu yitirmesi",
                    "2. Pre-B Hücre Blokajı: Kemik iliğinde B öncüllerinin matür B hücresine diferansiye olamaması",
                    "3. Dolaşımda B Hücre Yokluğu: Kanda CD19/CD20 pozitif B hücrelerinin ve plazma hücrelerinin sıfırlanması",
                    "4. Pan-hipogamaglobulinemi: Tüm antikorların yokluğu, tonsil aplazisi ve rekürren piyojenik enfeksiyonlar"
                ]
            ),
            make_cloze(
                "X'e bağlı Bruton agamaglobulinemisinde B hücre olgunlaşmasını durduran genetik defekt BTK tirozin kinaz enzimi mutasyonudur.",
                "BTK",
                "Bruton tirozin kinaz geninin standart tıbbi kısaltması"
            )
        ]
    })

    # Slayt 73: B Hücre Kusurları 2: Yaygın Değişken İmmün Yetmezlik (CVID)
    slides.append({
        "id": "k1-25-s73",
        "title": "B Hücre Kusurları 2: Yaygın Değişken İmmün Yetmezlik (CVID)",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 73,
        "narrative": (
            "Yaygın Değişken İmmün Yetmezlik (CVID), klinik olarak Bruton'a benzeyen ancak hücresel temeli farklı heterojen bir tablodur: "
            "1. **Başlangıç Yaşı (Genç Erişkinlik):** Bruton'un aksine bebeklikte değil; kadın ve erkeklerde eşit oranda, "
            "genellikle **20 ile 30'lu yaşlarda** teşhis edilir. "
            "2. **Hücresel Paradoks:** Periferik kanda B lenfosit (CD19/CD20) sayısı **NORMALDİR**. Ancak bu B lenfositleri "
            "antikor salgılayan plazma hücrelerine farklılaşamaz; sonuçta masif **hipogamaglobulinemi** (özellikle IgG ve IgA düşüklüğü) gelişir. "
            "3. **Klinik Tablo:** Tekrarlayan sinopulmoner enfeksiyonlar ve geri dönüşümsüz bronşiektazi. "
            "4. **Yüksek Otoimmünite ve Malignite:** Hastaların %20'sinde otoimmün hastalıklar (Otoimmün Hemolitik Anemi, ITP, romatoid artrit) "
            "görülür; ayrıca B hücreli lenfoma ve mide karsinomu riski belirgin şekilde yüksektir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Bruton Hastalığı vs CVID Karşılaştırması",
                "Bruton Agamaglobulinemisi",
                "Erkek çocukta (X'e bağlı), kanda B lenfositleri ve plazma hücreleri SIFIRDIR, tonsiller küçüktür",
                "Yaygın Değişken İmmün Yetmezlik (CVID)",
                "Genç erişkinde (K=E), kanda B lenfosit sayısı NORMALDİR fakat plazma hücresine dönüşemez, lenfoma riski yüksektir"
            ),
            make_micro_quiz(
                "Yirmi beş yaşında tekrarlayan pnömoni ve bronşiektazi atakları geçiren bir hastada serum IgG ve IgA düzeyleri ileri derecede düşük bulunuyor. Akım sitometrisinde periferik kanda CD19+ B lenfosit sayısının NORMAL olduğu saptanıyor. En olası tanı hangisidir?",
                {
                    "A": "Yaygın Değişken İmmün Yetmezlik (CVID)",
                    "B": "X'e bağlı Bruton Agamaglobulinemisi",
                    "C": "Şiddetli Kombine İmmün Yetmezlik (SCID)",
                    "D": "DiGeorge Sendromu",
                    "E": "Wiskott-Aldrich Sendromu"
                },
                "A",
                {
                    "A": "Doğrudur; genç erişkinde normal B lenfosit sayısı ile giden hipogamaglobulinemi tablosu CVID'in klasik tanımıdır.",
                    "B": "Yanlış; Bruton'da kanda B lenfositleri tamamen sıfırdır.",
                    "C": "Yanlış; SCID bebeklikte fatal hücresel ve hümoral çöküştür.",
                    "D": "Yanlış; DiGeorge T hücresi eksikliğidir.",
                    "E": "Yanlış; Wiskott-Aldrich'te mikrotrombositopeni ve egzama ön plandadır."
                }
            )
        ]
    })

    # Slayt 74: B Hücre Kusurları 3: İzole IgA Eksikliği ve Transfüzyon Anafilaksisi
    slides.append({
        "id": "k1-25-s74",
        "title": "B Hücre Kusurları 3: İzole IgA Eksikliği ve Transfüzyon Anafilaksisi",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 74,
        "narrative": (
            "İzole IgA eksikliği, tıp pratiğinde **en sık karşılaşılan primer immün yetmezliktir** (Batı toplumlarında yaklaşık 1/600): "
            "1. **İmmünolojik Durum:** Mukozal ve serum IgA düzeyleri son derece düşüktür (<7 mg/dL); buna karşılık IgG ve IgM düzeyleri "
            "ve T lenfosit fonksiyonları tamamen normaldir. B lenfositlerinin IgA üreten plazma hücrelerine sınıf değişimi bloke olmuştur. "
            "2. **Klinik Yelpaze:** Hastaların büyük çoğunluğu asemptomatiktir. Semptomatik bireylerde mukozal savunma zayıfladığı için "
            "tekrarlayan sinüzit, bronşit ve intestinal Giardia lamblia enfeksiyonları izlenir; çölyak hastalığı sıklığı artmıştır. "
            "3. **Ölümcül Transfüzyon Riski (Anti-IgA):** Bu hastaların bazılarında vücut IgA'yı hiç görmediği için kanda **anti-IgA antikorları** "
            "gelişir. Bu kişilere normal kan veya plazma transfüzyonu yapıldığında, donör kanındaki IgA'ya karşı **masif anafilaktik şok** "
            "ve kardiyorespiratuar arrest gelişebilir! Yıkanmış eritrosit süspansiyonu verilmelidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Ameliyat sırasında kan transfüzyonu yapılan bir hastada transfüzyonun ilk 5. dakikasında şiddetli hırıltılı solunum, laringeal stridor ve hipotansiyon gelişiyor. Hastanın geçmişinde tekrarlayan hafif sinüzit öyküsü olduğu öğreniliyor.",
                [
                    {
                        "text": "İzole IgA eksikliği zemininde donör IgA'sına karşı gelişen Tip I transfüzyon anafilaksisi tanısıyla derhal transfüzyonu durdurmak ve epinefrin uygulamak",
                        "isCorrect": True,
                        "explanation": "Mükemmel Acil ve İmmünolojik Karar: İzole IgA eksikliği olan hastalar donör plazmasındaki IgA'ya karşı anti-IgA antikorlarıyla öldürücü anafilaksi geliştirebilir."
                    },
                    {
                        "text": "Reaksiyonun sadece soğuk kan verilmesine bağlı olduğunu düşünerek transfüzyon hızını artırmak",
                        "isCorrect": False,
                        "explanation": "Ölümcül hata! Anafilaktik şokta transfüzyon sürdürülürse hasta dakikalar içinde kaybedilir."
                    }
                ]
            ),
            make_cloze(
                "İnsan toplumlarında en sık görülen primer immün yetmezlik sendromu izole IgA eksikliğidir.",
                "IgA",
                "Mukozal salgılarda ve gözyaşında yer alan primer dimerik immünoglobulin sınıfı"
            )
        ]
    })

    # Slayt 75: T Hücre Kusurları: DiGeorge Sendromu (Timik Hipoplazi)
    slides.append({
        "id": "k1-25-s75",
        "title": "T Hücre Kusurları: DiGeorge Sendromu (Timik Hipoplazi)",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 75,
        "narrative": (
            "DiGeorge sendromu, 3. ve 4. faringeal ceplerin embriyolojik gelişim bozukluğu sonucu ortaya çıkan konjenital tablodur: "
            "1. **Genetik Temel:** Hastaların %90'ından fazlasında **22q11.2 mikrodelesyonu** saptanır (TBX1 gen kaybı). "
            "2. **Dörtlü Patolojik Spektrum (CATCH-22):** "
            "- **Timus Aplazisi / Hipoplazisi:** T lenfositleri olgunlaşamaz; periferik kanda CD3+ T hücreleri ileri derecede düşüktür. "
            "Lenf nodlarının T zonu olan **parakortikal alan** boştur. Viral, fungal ve intraselüler mikobakteriyel enfeksiyonlara yatkınlık doğar. "
            "- **Paratiroid Aplazisi:** Paratiroid bezleri gelişemez; parathormon (PTH) sıfırdır. Yenidoğanda derin hipokalsemi ve inatçı **hipokalsemik tetani/nöbetler** görülür. "
            "- **Konotrunkal Kalp Defektleri:** Fallot tetralojisi, trunkus arteriyozus ve aort koarktasyonu. "
            "- **Fasiyal Dismorfizm:** Düşük kulaklar, mikrognati, hipertelorizm ve yarık damak."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "DiGeorge Sendromunun Embriyolojik ve Klinik Mimarisi",
                ["Embriyolojik Yapı", "Gelişemeyen Anatomik Organ", "Histopatolojik / Biyokimyasal Bulgu", "Klinik Tablo"],
                [
                    ["3. ve 4. Faringeal Cep", "Timus bezi", "Lenf nodunda parakorteks boşluğu, T hücresi yokluğu", "Fırsatçı mantar ve virüs enfeksiyonları"],
                    [
                        "3. ve 4. Faringeal Cep",
                        "Paratiroid bezleri",
                        {"text": "PTH sıfır, derin hipokalsemi ve hiperfosfatemi", "isMasked": True, "hint": "Kalsiyum regülasyonunun çökmesiyle ortaya çıkan biyokimyasal tablo"},
                        "Yenidoğan döneminde tetani ve kasılmalar"
                    ],
                    ["Kardiyak Nöral Krest", "Aortikopulmoner septum", "Büyük damar transpozisyonu, Fallot tetralojisi", "Konjenital siyanoz ve kalp yetmezliği"],
                    ["1. ve 2. Faringeal Arkus", "Maksillofasiyal kemikler", "Mikrognati, yarık damak, düşük kulak", "Karakteristik dismorfik yüz görünümü"]
                ]
            ),
            make_active_recall(
                "DiGeorge sendromunda timus gelişim kusuruna bağlı olarak lenf nodu biyopsisinde boş ve hipoplastik görülen spesifik T lenfosit zonu neresidir?",
                "Parakortikal alandır (Parakorteks).",
                "Korteks ile medülla arasında yer alan derin T hücre bağımlı lenf nodu bölgesi"
            )
        ]
    })

    # Slayt 76: Şiddetli Kombine İmmün Yetmezlik (SCID): En Ağır Pediatrik Kriz
    slides.append({
        "id": "k1-25-s76",
        "title": "Şiddetli Kombine İmmün Yetmezlik (SCID): En Ağır Pediatrik Kriz",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 76,
        "narrative": (
            "Şiddetli Kombine İmmün Yetmezlik (SCID), hem hücresel (T hücresi) hem hümoral (B hücresi) bağışıklığın "
            "aynı anda çöktüğü en ölümcül pediatrik immünolojik acildir: "
            "1. **İki Ana Genetik Tip:** "
            "- **X'e Bağlı SCID (En Sık - %50):** Sitokin reseptör **ortak gama zinciri (gammac / IL-2RG)** mutasyonudur. "
            "IL-2, IL-4, IL-7, IL-9, IL-15 ve IL-21 reseptörleri çalışamaz. Özellikle IL-7 çalışmadığı için T hücresi, "
            "IL-15 çalışmadığı için NK hücresi hiç üretilemez (T- B+ NK- fenotipi). "
            "- **Otozomal Resesif SCID (%40):** **Adenozin Deaminaz (ADA)** enzim eksikliğidir. Pürin yıkımı durur; "
            "biriken deoksiadenozin lenfosit öncülleri için aşırı toksiktir ve tüm lenfositleri (T, B ve NK) öldürür (T- B- NK-). "
            "2. **Histopatoloji:** Timus embriyonik düzeyde kalmıştır (**Fetal timus**); lobülasyon yoktur, lenfosit içermez "
            "ve Hassall cisimcikleri bulunmaz. Tedavi edilmezse ilk 1 yılda sepsis veya canlı aşılarla (BCG) ölüm kaçınılmazdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "SCID İki Temel Moleküler Formunun Karşılaştırması",
                ["Genetik Tip", "Kusurlu Enzim / Reseptör", "Kalıtım Şekli", "Hücresel Fenotip"],
                [
                    ["Sitokin Reseptör Kusuru", "Ortak gama zinciri (IL-2RG)", "X'e Bağlı Resesif (Erkek)", "T(-) B(+) NK(-) fenotipi"],
                    [
                        "Pürin Metabolizma Kusuru",
                        "Adenozin Deaminaz (ADA)",
                        {"text": "Otozomal Resesif (Kız/Erkek)", "isMasked": True, "hint": "Akraba evliliklerinde sık görülen enzim eksikliği kalıtımı"},
                        "T(-) B(-) NK(-) tüm lenfositlerin ölümü"
                    ]
                ]
            ),
            make_active_recall(
                "X'e bağlı şiddetli kombine immün yetmezlikte (SCID) T ve NK hücrelerinin gelişimini durduran mutasyon hangi reseptör zincirindedir?",
                "Sitokin reseptör ortak gama zincirindedir (IL-2RG / gammac).",
                "Çoklu interlökin reseptörlerinin paylaştığı ortak sinyal iletim alt birimi"
            )
        ]
    })

    # Slayt 77: Wiskott-Aldrich Sendromu ve Ataksi-Telenjiektazi
    slides.append({
        "id": "k1-25-s77",
        "title": "Wiskott-Aldrich Sendromu ve Ataksi-Telenjiektazi",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 77,
        "narrative": (
            "Kombine immün yetmezliklerin diğer iki klasik üyesi özgül sendromik bulgularla ayrılır: "
            "1. **Wiskott-Aldrich Sendromu (WASP Mutasyonu):** "
            "- **Genetik:** X kromozomunda yer alan ve aktin hücre iskeletini yöneten **WASP** geni mutasyonudur. "
            "- **Klasik Triad:** "
            "1) Trombositopeni ve **anormal küçük trombositler (mikrotrombositopeni)** nedeniyle peteşi, purpura ve sünnet kanamaları, "
            "2) Şiddetli dirençli **egzama** (atopik dermatit), "
            "3) Tekrarlayan enfeksiyonlar (özellikle kapsüllü bakteriler). Serumda IgM düşük, IgA ve IgE yüksektir. "
            "2. **Ataksi-Telenjiektazi (ATM Mutasyonu):** "
            "- **Genetik:** Otozomal resesif **ATM** gen mutasyonudur; DNA çift iplik kırıklarını tamir edemez. "
            "- **Klinik Triad:** Progresif serebellar ataksi (yürüme bozukluğu), konjonktiva ve deride **telenjiektaziler** "
            "ve tekrarlayan sinopulmoner enfeksiyonlar. Hastalarda radyasyona masif duyarlılık ve lösemi/lenfoma riski vardır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Wiskott-Aldrich vs Ataksi-Telenjiektazi Triadları",
                ["Sendrom", "Genetik Kusur", "Karakteristik Klinik Triad", "Spesifik Laboratuvar Damgası"],
                [
                    [
                        "Wiskott-Aldrich Sendromu",
                        "WASP geni (Aktin iskeleti)",
                        {"text": "Mikrotrombositopeni, egzama, tekrarlayan enfeksiyon", "isMasked": True, "hint": "Küçük trombositlerle kanama, alerjik cilt ve immün yetmezlik üçlüsü"},
                        "Düşük IgM, yüksek IgA/IgE, mikrotrombositler"
                    ],
                    ["Ataksi-Telenjiektazi", "ATM geni (DNA çift zincir tamiri)", "Serebellar ataksi, okülokutanöz telenjiektazi, enfeksiyon", "Yüksek alfa-fetoprotein (AFP), radyasyon duyarlılığı"]
                ]
            ),
            make_active_recall(
                "Erkek çocukta mikrotrombositopeni (küçük trombositli kanama diyatezi), egzama ve tekrarlayan enfeksiyon triadı ile seyreden X'e bağlı sendrom hangisidir?",
                "Wiskott-Aldrich sendromudur.",
                "Aktin hücre iskeleti düzenleyici WASP gen mutasyonu hastalığı"
            )
        ]
    })

    # Slayt 78: Lökosit ve Fagositer Kusurlar: Kronik Granülomatöz Hastalık
    slides.append({
        "id": "k1-25-s78",
        "title": "Lökosit ve Fagositer Kusurlar: Kronik Granülomatöz Hastalık ve Chédiak-Higashi",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 78,
        "narrative": (
            "Fagositer hücrelerin (nötrofil ve makrofaj) mikropları yutma veya sindirme aşamasındaki kalıtsal arızalarıdır: "
            "1. **Kronik Granülomatöz Hastalık (CGD):** "
            "- **Mekanizma:** Fagozom zarındaki **NADPH oksidaz** enzim kompleksinin (en sık X'e bağlı gp91phox) genetik yokluğudur. "
            "Nötrofil bakteriyi yutar ancak 'respiratuar patlama' yapamaz; süperoksit ve hidrojen peroksit (H2O2) üretemez. "
            "- **Katalaz Pozitif Mikroplar:** Katalaz negatif bakteriler kendi ürettikleri H2O2 ile intihar ederken; **katalaz pozitif "
            "mikroplar (Staphylococcus aureus, Aspergillus, Serratia, Burkholderia, Nocardia)** kendi H2O2'lerini nötralize eder "
            "ve nötrofil içinde canlı kalır. Vücut mikrobu sınırlamak için her yerde masif **granülomlar ve apseler** örer. "
            "- **Tanı:** Nitroblue Tetrazolium (NBT) indirgenme testi veya dihidrorodamin (DHR) akım sitometrisi. "
            "2. **Chédiak-Higashi Sendromu (LYST Mutasyonu):** Fagozom ile lizozom kaynaşamaz. Nötrofillerde **dev lizozomal granüller**, "
            "melanositlerde defekt nedeniyle **parsiyel albinizm** ve periferik nöropati izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Fagositer Kusurların Hücresel Karşılaştırması",
                "Kronik Granülomatöz Hastalık (CGD)",
                "NADPH oksidaz eksikliği, respiratuar patlama yokluğu, katalaz pozitif bakterilerle masif granülomlar",
                "Chédiak-Higashi Sendromu",
                "LYST mutasyonu, lizozom füzyon defekti, sitoplazmada dev granüller ve parsiyel albinizm"
            ),
            make_micro_quiz(
                "Tekrarlayan Staphylococcus aureus ve Aspergillus apseleri nedeniyle araştırılan bir erkek çocuğun nötrofillerinde fagositoz sonrası respiratuar patlamanın (oksidatif patlama) gerçekleşmediği saptanıyor. Bu hastada kusurlu olan enzim kompleksi hangisidir?",
                {
                    "A": "NADPH oksidaz enzim kompleksi",
                    "B": "Miyeloperoksidaz (MPO)",
                    "C": "Adenozin Deaminaz (ADA)",
                    "D": "Bruton Tirozin Kinaz (BTK)",
                    "E": "Glukoz-6-Fosfat Dehidrogenaz"
                },
                "A",
                {
                    "A": "Doğrudur; NADPH oksidaz yokluğu Kronik Granülomatöz Hastalığın (CGD) temel nedenidir ve katalaz pozitif enfeksiyonlar yapar.",
                    "B": "Yanlış; MPO eksikliğinde solunum patlaması intakttır.",
                    "C": "Yanlış; ADA eksikliği SCID yapar.",
                    "D": "Yanlış; BTK mutasyonu Bruton hastalığı yapar.",
                    "E": "Yanlış; G6PD eritrosit hemolizidir."
                }
            )
        ]
    })

    # Slayt 79: Checkpoint 8
    slides.append({
        "id": "k1-25-s79",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Primer İmmün Yetmezlikler ve Genetik Temelleri",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 79,
        "narrative": (
            "Bu sekizinci kontrol noktasında, primer immün yetmezlik sendromlarının kilit patolojik özelliklerini özetliyoruz: "
            "1. **Bruton:** X'e bağlı BTK mutasyonu; kanda B hücresi sıfırdır, tonsil yoktur, pan-hipogamaglobulinemi görülür. "
            "2. **CVID:** Genç erişkinde B hücre sayısı normaldir fakat plazma hücresine dönüşemez; lenfoma riski taşır. "
            "3. **İzole IgA:** En sık primer yetmezliktir; kanda anti-IgA varsa transfüzyon sırasında ölümcül anafilaksi gelişebilir. "
            "4. **DiGeorge:** 22q11.2 delesyonu, 3/4 faringeal cep; timus yokluğu (parakorteks boş), hipokalsemik tetani ve Fallot tetralojisi. "
            "5. **SCID:** Ortak gama zinciri (X'e bağlı) veya ADA eksikliği; T ve B hücrelerinin ikisi birden çöker (fetal timus). "
            "6. **CGD:** NADPH oksidaz defekti; katalaz pozitif bakteriler öldürülemez ve granülomlar oluşur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s79-1",
                "Erkek çocuklarda B hücre gelişimini pre-B basamağında durdurarak periferik kanda CD19 ve CD20 hücrelerini sıfırlayan genetik mutasyon nedir?",
                "Bruton tirozin kinaz (BTK) mutasyonudur.",
                "X kromozomuna bağlı agamaglobulinemiye yol açan sitoplazmik sinyal enzimi defekti",
                "BTK ve Bruton"
            ),
            make_flashcard(
                "k1-25-fc-s79-2",
                "Primer immün yetmezlikler arasında en sık görülen ve transfüzyon esnasında donör plazmasındaki antijene karşı anafilaksi riski taşıyan tablo nedir?",
                "İzole IgA yetersizliği tablosudur.",
                "Mukozal salgılarda yer alan antikor izotipinin selektif yokluğu sendromu",
                "İzole IgA Eksikliği"
            ),
            make_flashcard(
                "k1-25-fc-s79-3",
                "Kronik Granülomatöz Hastalıkta (CGD) lökositlerin respiratuar patlama yapmasını engelleyerek katalaz pozitif bakterilere yatkınlık oluşturan enzim nedir?",
                "NADPH oksidaz kompleksi enzimidir.",
                "Fagozom membranında süperoksit anyonu üreten elektron transfer mekanizması",
                "NADPH Oksidaz ve CGD"
            )
        ],
        "interactiveElements": [
            make_table(
                "Primer İmmün Yetmezlikler Checkpoint Büyük Özeti",
                ["Sendrom", "Temel Genetik Defekt", "Etkilenen İmmün Kol", "Ayırt Edici Klinik / Laboratuvar Damgası"],
                [
                    ["Bruton (XLA)", "BTK mutasyonu", "B hücresi (Hümoral)", "Kanda B hücresi SIFIR, tonsil yok, erkek çocuk"],
                    ["CVID", "B hücre diferansiasyon kusuru", "B hücresi (Hümoral)", "B hücresi NORMAL fakat antikor yok, lenfoma riski"],
                    ["İzole IgA Eksikliği", "IgA sınıf değişim kusuru", "İzole IgA", "En sık yetmezlik, transfüzyon anafilaksisi"],
                    [
                        "DiGeorge Sendromu",
                        "22q11.2 mikrodelesyonu",
                        {"text": "T hücresi (Timik aplazi)", "isMasked": True, "hint": "Timus ve paratiroid gelişememesiyle giden 3/4 faringeal cep sendromu"},
                        "Hipokalsemik tetani, Fallot tetralojisi, parakorteks boş"
                    ],
                    ["SCID", "IL-2RG (gammac) veya ADA", "T ve B hücresi (Kombine)", "Fetal timus, ilk 1 yılda kemik iliği nakli şart"],
                    ["CGD", "NADPH oksidaz mutasyonu", "Fagositer hücreler", "Katalaz pozitif apseler, granülomlar, anormal NBT"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki immün yetmezlik sendromu ve karakteristik patolojik bulgu eşleştirmelerinden hangisi YANLIŞTIR?",
                {
                    "A": "Bruton agamaglobulinemisi - Kanda CD19+ B hücresi yokluğu",
                    "B": "DiGeorge sendromu - Lenf nodunda parakortikal alan hipoplazisi",
                    "C": "SCID - Hassall cisimciği içermeyen fetal timus",
                    "D": "Kronik Granülomatöz Hastalık - Fagozomda NADPH oksidaz eksikliği",
                    "E": "CVID - Periferik kanda B hücre sayısının tamamen sıfırlanması"
                },
                "E",
                {
                    "A": "Doğrudur; Bruton'da B hücresi sıfırdır.",
                    "B": "Doğrudur; DiGeorge'da T zonu olan parakorteks boştur.",
                    "C": "Doğrudur; SCID'de timus displaziktir.",
                    "D": "Doğrudur; CGD NADPH oksidaz kusurudur.",
                    "E": "YANLIŞTIR; CVID'de B hücre sayısı sıfır DEĞİL, NORMALDİR; plazma hücresine diferansiasyon bozuktur."
                }
            )
        ]
    })

    # Slayt 80: Bölüm Özeti: Primer İmmün Yetmezliklerden HIV/AIDS ve Amiloidoza Geçiş
    slides.append({
        "id": "k1-25-s80",
        "title": "Bölüm Özeti: HIV/AIDS ve Amiloidoza Geçiş",
        "section": "Primer İmmün Yetmezlik Sendromları",
        "slideNumber": 80,
        "narrative": (
            "Genetik kökenli primer immün yetmezliklerin ardından, modern tıbbın karşılaştığı en yıkıcı "
            "edinsel (sekonder) immün yetmezlik HIV/AIDS pandemisidir: "
            "1. **HIV/AIDS:** İnsan İmmün Yetmezlik Virüsü (HIV), bağışıklık sisteminin orkestra şefi olan "
            "**CD4+ T yardımcı lenfositlerini** selektif olarak enfekte eder ve tüketir. "
            "CD4 sayısı <200/mikrolitreye düştüğünde fırsatçı enfeksiyonlar (Pneumocystis jirovecii, Cryptococcus) "
            "ve viral neoplaziler (Kaposi sarkomu, lenfomalar) patlak verir. "
            "2. **Amiloidoz:** Kronik inflamasyonların veya plazma hücresi diskrazilerinin nihai patolojik sonucu ise, "
            "yanlış katlanmış proteinlerin dokularda çözünmeyen **beta-kırmalı tabakalar (amiloid fibrilleri)** halinde birikmesidir. "
            "Bölüm 9'da HIV patogenezini ve amiloid protein biyolojisini inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Primer vs Sekonder İmmün Yetmezlik",
                "Primer İmmün Yetmezlikler",
                "Doğuştan kalıtsal genetik mutasyonlar (Bruton, SCID, DiGeorge) ve erken çocuklukta ortaya çıkış",
                "Sekonder İmmün Yetmezlik (HIV/AIDS)",
                "Edinsel retroviral enfeksiyonla CD4+ T hücrelerinin selektif yıkımı ve erişkinde fatal immün yetmezlik"
            ),
            make_active_recall(
                "İnsan İmmün Yetmezlik Virüsünün (HIV) kılıf glikoproteini gp120 ile bağlanarak selektif olarak enfekte ettiği ve yok ettiği temel bağışıklık hücresi hangisidir?",
                "CD4+ T yardımcı (helper) lenfositidir.",
                "Hücresel immün yanıtın koordinatörü olan dört pozitif T hücresi"
            )
        ]
    })

    return slides
