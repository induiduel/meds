# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 25: Aşırı Duyarlılık ve Otoimmünite
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 4: İmmünolojik Toleransın Moleküler Temeli ve Otoimmünite Gelişimi (Slayt 31 - 40)
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_before_after,
    make_table, make_causal_chain, make_active_recall,
    make_branching_logic, make_flashcard
)

def get_section_4_slides():
    slides = []

    # Slayt 31: İmmünolojik Tolerans Kavramı ve İki Temel Düzey
    slides.append({
        "id": "k1-25-s31",
        "title": "İmmünolojik Tolerans Kavramı ve İki Temel Düzey",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 31,
        "narrative": (
            "İmmünolojik tolerans, bağışıklık sisteminin konağın kendi antijenlerine (öz antijenler / self-antigens) "
            "karşı spesifik olarak yanıtsız kalması ve kendi dokularını tahrip etmesini engelleyen yaşamsal savunma frenidir: "
            "1. **Toleransın Zorunluluğu:** Lenfosit reseptör çeşitliliği V(D)J rekombinasyonu ile rastgele üretildiğinden, "
            "oluşan klonların önemli bir kısmı kaçınılmaz olarak kendi vücut bileşenlerimize afinite gösterir. "
            "Bu otoreaktif hücreler ortadan kaldırılmazsa otoimmün hastalıklar patlak verir. "
            "2. **İki Aşamalı Kontrol Ağı:** "
            "- **Santral Tolerans:** Olgunlaşmamış lenfositlerin birincil (generatif) lenfoid organlarda (T hücreleri için **timus**, "
            "B hücreleri için **kemik iliği**) kendi antijenleriyle karşılaşıp elenmesi veya modifiye edilmesidir. "
            "- **Periferik Tolerans:** Santral denetimden kaçan otoreaktif klonların ikincil lenfoid dokularda ve periferik organlarda "
            "susturulması (anerji), baskılanması (Treg) veya apoptozla silinmesidir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Santral ve Periferik Tolerans Karşılaştırması",
                ["Özellik", "Santral Tolerans", "Periferik Tolerans"],
                [
                    ["Anatomik Konum", "Birincil lenfoid organlar (Timus, Kemik iliği)", "İkincil lenfoid organlar (Dalak, Lenf nodu) ve dokular"],
                    ["Hedef Hücre Evresi", "İmmatür (gelişmekte olan) lenfositler", "Matür (dolaşımdaki olgun) lenfositler"],
                    [
                        "Temel Mekanizmalar",
                        "Klonal delesyon (apoptoz) ve reseptör düzenlemesi",
                        {"text": "Anerji, Treg süpresyonu ve Fas/FasL apoptozu", "isMasked": True, "hint": "Periferde otoreaktif hücreleri susturan üçlü güvenlik bariyeri"}
                    ],
                    ["Genetik Bozukluk Sonucu", "APECED sendromu (AIRE eksikliği)", "IPEX sendromu (FoxP3) ve ALPS sendromu (Fas)"]
                ]
            ),
            make_active_recall(
                "T lenfositlerinin kendi doku antijenlerini tanıyan otoreaktif klonlarının timusta apoptozla yok edilmesi sürecine ne ad verilir?",
                "Negatif seleksiyon (Klonal delesyon) denir.",
                "Timik medullada yüksek afiniteli hücrelerin elenmesi olayı"
            )
        ]
    })

    # Slayt 32: T Hücre Santral Toleransı: Negatif Seleksiyon ve AIRE Geni
    slides.append({
        "id": "k1-25-s32",
        "title": "T Hücre Santral Toleransı: Negatif Seleksiyon ve AIRE Geni",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 32,
        "narrative": (
            "T hücreleri timusta iki aşamalı bir sınavdan geçer; kendi antijenlerine yüksek afinite gösterenler elenir: "
            "1. **Negatif Seleksiyon (Klonal Delesyon):** Timik korteks ve medullada gelişen timositler, kendi MHC moleküllerine "
            "bağlı öz peptitleri aşırı güçlü tanırsa apoptoza sevk edilerek silinir. "
            "2. **AIRE Geni ve Ektopik Ekspresyon:** Timusta sadece timik proteinler değil; pankreas insülini, tiroit tiroglobulini, "
            "adrenal enzimler gibi perifere özgü organ antijenleri de sunulmalıdır. Medüller timik epitel hücrelerinde (mTEC) bu periferik "
            "antijenlerin transkripsiyonunu sağlayan anahtar gen **AIRE (Autoimmune Regulator)** genidir. "
            "3. **APECED / APS-1 Sendromu:** AIRE gen mutasyonunda periferik antijenler timusta sunulamaz; otoreaktif T hücreleri perifere kaçar. "
            "Sonuçta hipoparatiroidizm, adrenal yetmezlik (Addison) ve kronik mukokutanöz kandidiyazis ile seyreden otoimmün sendrom doğar."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "AIRE Geni ve Santral Tolerans Yolağı",
                [
                    "1. Timik Epitelde AIRE İfadesi: Medüller hücrelerde perifere özgü doku antijen genlerinin açılması",
                    "2. Ektopik Antijen Sunumu: İnsülin, tiroglobulin ve adrenal peptitlerin MHC üzerinde timosite gösterilmesi",
                    "3. Yüksek Afinite Tanıması: Otoreaktif T hücresinin bu organ peptitlerine kuvvetle bağlanması",
                    "4. Negatif Seleksiyon: Hücre içi Bim/Bax yolağıyla otoreaktif klonun timusta apoptozla silinmesi"
                ]
            ),
            make_cloze(
                "Timus medullasındaki epitel hücrelerinde perifere özgü organ antijenlerinin ekspresyonunu sağlayarak santral toleransı yöneten transkripsiyon faktörü geni AIRE genidir.",
                "AIRE",
                "Otoimmün regülatör proteininin standart medikal kısaltması"
            )
        ]
    })

    # Slayt 33: B Hücre Santral Toleransı: Reseptör Düzenlemesi ve Delesyon
    slides.append({
        "id": "k1-25-s33",
        "title": "B Hücre Santral Toleransı: Reseptör Düzenlemesi ve Delesyon",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 33,
        "narrative": (
            "Kemik iliğinde olgunlaşan immatür B lenfositleri kendi antijenleriyle karşılaştığında T hücrelerinden farklı "
            "bir kurtarma mekanizmasına sahiptir: "
            "1. **Reseptör Düzenlemesi (Receptor Editing):** İmmatür B hücresinin yüzey IgM antikoru kemik iliğindeki öz antijene "
            "yüksek afiniteyle bağlanırsa hücre hemen apoptoza gitmez. "
            "2. **Hafif Zincir Rekombinasyonu:** Hücre **RAG-1 ve RAG-2** genlerini yeniden aktive eder. İmmünoglobulin hafif zincir "
            "genini (özellikle kappa zincirini kapatıp lambda zincirini) yeniden rekombine eder. "
            "3. **Yeni Spesifite:** Düzenleme başarılı olursa B hücresi artık kendi antijenini tanımaz ve periferik olgun B havuzuna katılır. "
            "4. **Klonal Delesyon ve Anerji:** Eğer reseptör düzenlemesi başarısız kalırsa veya antijen zayıf çözünür formdaysa "
            "B hücresi apoptozla yok edilir (klonal delesyon) ya da yüzey IgM'sini kaybederek anerjiye girer."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "T Hücresi vs B Hücresi Santral Tolerans Ayrımı",
                "T Lenfosit Santral Toleransı",
                "Yüksek afiniteli timositler için ikinci bir şans yoktur; doğrudan negatif seleksiyonla apoptoza gönderilir",
                "B Lenfosit Santral Toleransı",
                "Otoreaktif B hücreleri RAG genlerini yeniden açarak hafif zinciri değiştirir (Reseptör Düzenlemesi) ve kurtulabilir"
            ),
            make_active_recall(
                "Kemik iliğindeki immatür B hücrelerinin kendi antijenini tanıdığında RAG genlerini açarak immünoglobulin hafif zincirini yeniden düzenlemesi sürecine ne ad verilir?",
                "Reseptör düzenlemesi (Receptor editing) denir.",
                "B lenfositinin otoimmüniteden kaçmak için antikor spesifitesini değiştirmesi"
            )
        ]
    })

    # Slayt 34: Periferik Tolerans Mekanizma 1: Anerji ve Kostimülasyon Yokluğu
    slides.append({
        "id": "k1-25-s34",
        "title": "Periferik Tolerans Mekanizma 1: Anerji ve İnhibitör Reseptörler",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 34,
        "narrative": (
            "Santral denetimden kaçan otoreaktif T hücrelerinin periferde uyarılmasını engelleyen ilk mekanizma anerjidir: "
            "1. **İki Sinyal Hipotezi:** Bir T hücresinin tam olarak aktive olabilmesi için iki zorunlu sinyal gerekir: "
            "- **Sinyal 1 (Antijen Sinyali):** TCR'nin APC üzerindeki MHC-peptit kompleksini tanıması. "
            "- **Sinyal 2 (Kostimülatör Sinyal):** APC yüzeyindeki **B7 (CD80/CD86)** molekülünün T hücresindeki **CD28**'e bağlanması. "
            "2. **Anerji Gelişimi:** Sağlıklı dokularda istirahat halindeki APC'lerde kostimülatör B7 molekülleri bulunmaz veya çok azdır. "
            "T hücresi Sinyal 1'i alır fakat Sinyal 2'yi alamazsa kalıcı bir fonksiyonel yanıtsızlık durumuna (**anerji**) girer. "
            "3. **Frenleyici Reseptörler (CTLA-4 ve PD-1):** **CTLA-4**, B7 molekülüne CD28'den çok daha yüksek afiniteyle bağlanarak "
            "aktivasyon sinyalini bloke eder; **PD-1** ise TCR sinyal yolundaki kinazları defosforile ederek hücreyi susturur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "T Hücresi Aktivasyonu vs Anerji Koşulları",
                ["Durum", "Sinyal 1 (TCR - MHC)", "Sinyal 2 (B7 - CD28)", "İnhibitör Reseptör (CTLA-4)", "T Hücre Akıbeti"],
                [
                    ["Enfeksiyöz Aktivasyon", "Var (MHC-mikrop)", "Güçlü (APC'de B7 var)", "Düşük / İnaktif", "Proliferasyon ve sitokin fırtınası"],
                    [
                        "Ototolerans (Anerji)",
                        "Var (MHC-öz peptit)",
                        {"text": "YOK (İstirahat APC'de B7 yok)", "isMasked": True, "hint": "Hücrenin aktivasyon yerine kalıcı suskunluğa girmesine yol açan eksiklik"},
                        "Devre dışı",
                        "Kalıcı yanıtsızlık (Anerji)"
                    ],
                    ["İmmün Kontrol (Fren)", "Var", "Yarışmalı blokaj", "Yüksek (B7'yi CD28'den çalar)", "Aktivasyonun durdurulması"]
                ]
            ),
            make_micro_quiz(
                "T lenfositlerinin yüzeyinde yer alan, B7 (CD80/CD86) molekülüne CD28'den kat kat yüksek afiniteyle bağlanarak lenfosit aktivasyonunu güçlü şekilde frenleyen inhibitör kontrol noktası reseptörü hangisidir?",
                {
                    "A": "CTLA-4 (CD152)",
                    "B": "CD40 Ligand",
                    "C": "FcepsilonRI",
                    "D": "Toll-benzeri Reseptör 4",
                    "E": "CD3 kompleksi"
                },
                "A",
                {
                    "A": "Doğrudur; CTLA-4 B7'ye bağlanarak T hücresini negatif olarak regüle eder ve toleransı sürdürür.",
                    "B": "Yanlış; CD40L B hücre aktivasyonunu sağlayan pozitif moleküldür.",
                    "C": "Yanlış; bu mast hücresi IgE reseptörüdür.",
                    "D": "Yanlış; TLR-4 endotoksin reseptörüdür.",
                    "E": "Yanlış; CD3 TCR sinyal ileticisidir."
                }
            )
        ]
    })

    # Slayt 35: Periferik Tolerans Mekanizma 2: Düzenleyici T Hücreleri (Treg)
    slides.append({
        "id": "k1-25-s35",
        "title": "Periferik Tolerans Mekanizma 2: Düzenleyici T Hücreleri (Treg)",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 35,
        "narrative": (
            "Periferik toleransın en aktif bekçileri, otoreaktif hücreleri doğrudan baskılayan düzenleyici T lenfositleridir (Treg): "
            "1. **Treg Hücresel Kimliği:** Treg hücreleri yüzeylerinde **CD4** ve yüksek afiniteli IL-2 reseptör alfa zinciri olan **CD25**'i taşır. "
            "Hücrenin gelişimi ve baskılayıcı fonksiyonu için mutlak gerekli çekirdek transkripsiyon faktörü **FoxP3**'tür. "
            "2. **Baskılama Mekanizmaları:** "
            "- **İnhibitör Sitokin Salınımı:** Güçlü immünsüpresif sitokinler olan **İnterlökin-10 (IL-10)** ve **Transforme Edici Büyüme Faktörü-beta (TGF-beta)** salgılarlar. "
            "- **IL-2 Tüketimi:** Aşırı miktarda CD25 taşıdıkları için ortamdaki büyüme faktörü IL-2'yi adeta sünger gibi emerler; efektör hücreleri aç bırakırlar. "
            "- **APC Modülasyonu:** Yüzeylerindeki CTLA-4 ile APC'lerdeki B7 moleküllerini sökerek antijen sunumunu köreltirler. "
            "3. **IPEX Sendromu:** FoxP3 gen mutasyonunda Treg'ler üretilemez; yenidoğanda ölümcül poliendokrinopati, neonatal diyabet ve enterit gelişir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_causal_chain(
                "Treg Hücresi İmmünsüpresyon Mekanizması",
                [
                    "1. FoxP3 İfadesi: CD4+ CD25+ T hücresinde anahtar regülatör transkripsiyon faktörünün açılması",
                    "2. Sitokin Üretimi: Doku mikroçevresine bol miktarda IL-10 ve TGF-beta pompalanması",
                    "3. IL-2 Deprivasyonu: Yüksek afiniteli CD25 reseptörleriyle büyüme faktörünün emilerek tüketilmesi",
                    "4. Otoreaktif Hücre Felci: Çevredeki otoreaktif T hücrelerinin bölünmesinin ve sitotoksisitesinin durdurulması"
                ]
            ),
            make_cloze(
                "Düzenleyici T lenfositlerinin (Treg) gelişimini ve fonksiyonunu yöneten ve mutasyonunda IPEX sendromuna yol açan transkripsiyon faktörü FoxP3 proteinidir.",
                "FoxP3",
                "Treg hücrelerinin nükleer anahtar transkripsiyon faktörü"
            )
        ]
    })

    # Slayt 36: Periferik Tolerans Mekanizma 3: Apoptoz ve Fas/FasL Yolağı
    slides.append({
        "id": "k1-25-s36",
        "title": "Periferik Tolerans Mekanizma 3: Apoptoz ve Fas/FasL Yolağı",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 36,
        "narrative": (
            "Periferik dokularda kendi antijeniyle sürekli ve aralıksız karşılaşan lenfositler aktif bir intihar programına girer: "
            "1. **Aktivasyonun İndüklediği Hücre Ölümü (AICD):** Tekrarlayan öz antijen uyarımı alan matür T hücreleri "
            "membranlarında eşzamanlı olarak hem ölüm reseptörü **Fas (CD95)** hem de onun ligandı olan **FasL (CD178)** eksprese eder. "
            "2. **Ölüm Kompleksi (DISC):** FasL bitişik hücredeki veya aynı hücredeki Fas reseptörüne bağlanır; intraselüler FADD "
            "adaptör proteini aracılığıyla **prokaspaz-8** aktive edilir. Kaspaz kaskadı tetiklenir ve otoreaktif hücre hızla apoptozla silinir. "
            "3. **ALPS Sendromu (Otoimmün Lenfoproliferatif Sendrom):** Fas, FasL veya kaspaz-8/10 gen mutasyonlarında lenfositler "
            "apoptoza gidemez. Vücutta otoreaktif T ve B hücreleri birikir; masif splenomegali, lenfadenopati ve otoimmün sitopeniler izlenir."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "Fas/FasL Yolağı ve ALPS Sendromu Özellikleri",
                ["Bileşen", "Biyolojik Fonksiyonu", "Mutasyonundaki Patoloji", "Klinik Görünüm"],
                [
                    ["Fas (CD95)", "Ölüm reseptörü (TNF reseptör ailesi)", "Apoptoza dirençli otoreaktif lenfositler", "Otoimmün lenfoproliferasyon"],
                    [
                        "FasL (CD178)",
                        "Fas reseptörünü çapraz bağlayan ligand",
                        {"text": "Aktivasyonun indüklediği hücre ölümünün çökmesi", "isMasked": True, "hint": "Tekrarlayan uyarıya rağmen T hücresinin ölememesi"},
                        "Lenf nodlarında masif büyüme"
                    ],
                    ["Kaspaz-8", "Başlatıcı kaspaz enzimi", "Ölüm sinyalinin nükleusa iletilememesi", "Otoimmün hemolitik anemi ve trombositopeni"]
                ]
            ),
            make_active_recall(
                "Fas (CD95) veya FasL genlerindeki mutasyonlar sonucu otoreaktif lenfositlerin apoptoza gidememesiyle karakterize otoimmün lenfoproliferatif tabloya ne ad verilir?",
                "ALPS sendromu (Otoimmün Lenfoproliferatif Sendrom) denir.",
                "Ölüm reseptörü defektine bağlı masif lenfadenopati ve splenomegali hastalığı"
            )
        ]
    })

    # Slayt 37: İmmünolojik Ayrıcalıklı Dokular ve Sekestre Antijenler
    slides.append({
        "id": "k1-25-s37",
        "title": "İmmünolojik Ayrıcalıklı Dokular ve Sekestre Antijenler",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 37,
        "narrative": (
            "Vücudun bazı anatomik bölgeleri evrimsel olarak lenfosit dolaşımından tamamen gizlenmiş ve yalıtılmıştır: "
            "1. **İmmünolojik Ayrıcalıklı (Privileged) Alanlar:** Gözün ön kamarası ve retina, testis, beyin ve plasenta "
            "bu özel bölgelerin başında gelir. Bu dokularda kan-doku bariyeri bulunur, lenfatik drenaj yoktur ve hücre zarlarında "
            "bol miktarda **FasL** ile **TGF-beta** sentezlenerek yaklaşan lenfositler derhal öldürülür veya susturulur. "
            "2. **Sekestre Antijenlerin Açığa Çıkışı:** Bu bölgelerdeki antijenler embriyogenezde timusa hiç gitmediği için bağışıklık "
            "sistemi bunlara karşı santral tolerans geliştirmemiştir. "
            "3. **Sempatik Oftalmi:** Bir göze delici travma geldiğinde intraoküler antijenler kana ve lenf nodlarına sızar. T hücreleri "
            "duyarlılaşır; haftalar sonra antikor ve T hücreleri **sağlam olan diğer göze de saldırarak** bilateral otoimmün körlük oluşturur."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_branching_logic(
                "Sağ gözüne delici metal cisim yaralanması geçiren bir hastada başarılı cerrahi sonrası 3 hafta sonra sol (yaralanmamış sağlam) gözünde ani görme kaybı, fotofobi ve üveit başlıyor.",
                [
                    {
                        "text": "Sekestre oküler antijenlerin açığa çıkmasıyla gelişen Sempatik Oftalmi tanısıyla acil yüksek doz sistemik kortikosteroid tedavisi planlamak",
                        "isCorrect": True,
                        "explanation": "Mükemmel Patolojik ve Klinik Değerlendirme: Travma sekestre göz antijenlerini dolaşıma döker; duyarlılaşan lenfositler diğer sağlam göze saldırır (sempatik oftalmi)."
                    },
                    {
                        "text": "Yalnızca göz damlası verip hastanın semptomlarının psikolojik olduğunu söylemek",
                        "isCorrect": False,
                        "explanation": "Ölümcül hata! Sempatik oftalmi acil immünsüpresyon yapılmazsa bilateral kalıcı körlükle sonuçlanır."
                    }
                ]
            ),
            make_cloze(
                "Delici göz travması sonrası sekestre oküler antijenlerin kana karışarak sağlam diğer gözde otoimmün körlük oluşturması tablosuna sempatik oftalmi denir.",
                "sempatik oftalmi",
                "Bir gözün yaralanmasıyla diğer gözün immünolojik olarak tahrip olduğu sendrom"
            )
        ]
    })

    # Slayt 38: Otoimmünite Gelişiminde Genetik ve Çevresel Faktörler
    slides.append({
        "id": "k1-25-s38",
        "title": "Otoimmünite Gelişiminde Genetik ve Çevresel Faktörler: Moleküler Benzerlik",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 38,
        "narrative": (
            "Otoimmün hastalıklar tek bir nedene bağlı değildir; genetik yatkınlık ile çevresel tetikleyicilerin bileşkesidir: "
            "1. **HLA Gen Birliği (En Güçlü Genetik Bağ):** "
            "- **HLA-B27:** Ankilozan Spondilit gelişme riskini 90 kattan fazla artırır! "
            "- **HLA-DR4:** Romatoid Artrit ve Tip 1 Diabetes Mellitus ile ilişkilidir. "
            "- **HLA-DR2 ve DR3:** Sistemik Lupus Eritematozus (SLE) yatkınlığı oluşturur. "
            "2. **Non-HLA Genler:** PTPN22 (tirozin fosfataz), NOD2 (Crohn hastalığı), CTLA4 ve CD25 polimorfizmleri. "
            "3. **Enfeksiyonlar ve Moleküler Benzerlik (Molecular Mimicry):** Bir mikroorganizmanın epitopu, konak dokusundaki bir antijene "
            "yapısal olarak çok benzerse, mikropa karşı üretilen antikor ve T hücreleri mikrobu yok ettikten sonra konak dokusuna saldırır. "
            "En klasik örnek; Streptococcus pyogenes M proteinine karşı oluşan antikorların kalp miyozinine saldırarak **Akut Romatizmal Ateş** yapmasıdır."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_table(
                "HLA Allelleri ve İlişkili Otoimmün Hastalıklar",
                ["HLA Alleli", "İlişkili Otoimmün Patoloji", "Göreceli Risk Katsayısı (RR)", "Klinik Özellik"],
                [
                    ["HLA-B27", "Ankilozan Spondilit", "Yaklaşık 90 - 100 Kat", "Sakroiliak eklem ankilozu, bambu kamışı omurga"],
                    [
                        "HLA-DR4",
                        "Romatoid Artrit / Tip 1 DM",
                        {"text": "Yaklaşık 4 - 6 Kat", "isMasked": True, "hint": "Romatoid artritte kıkırdak yıkımıyla ilişkili sınıf II doku grubu"},
                        "Sinovyal pannus oluşumu ve beta hücre nekrozu"
                    ],
                    ["HLA-DR3", "Sistemik Lupus Eritematozus / Sjögren", "Yaklaşık 3 - 5 Kat", "Antinükleer otoantikorlar ve vaskülit"],
                    ["HLA-DQ2 / DQ8", "Çölyak Hastalığı", "Yüksek Duyarlılık", "Gluten peptitlerine karşı ince bağırsak atrofisi"]
                ]
            ),
            make_active_recall(
                "Bir mikrobiyal antijen ile konak doku proteini arasındaki yapısal benzerlik nedeniyle enfeksiyon sonrası otoimmün doku hasarı gelişmesi mekanizmasına ne ad verilir?",
                "Moleküler benzerlik (Moleküler taklit / Molecular mimicry) denir.",
                "Streptokok M proteini ile miyokard miyozini arasındaki antijenik benzerlik fenomeni"
            )
        ]
    })

    # Slayt 39: Checkpoint 4
    slides.append({
        "id": "k1-25-s39",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Santral ve Periferik Tolerans Mekanizmaları",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 39,
        "narrative": (
            "Bu dördüncü kontrol noktasında, immünolojik tolerans ve otoimmünite mekanizmalarını özetliyoruz: "
            "1. **Santral Tolerans:** Timusta negatif seleksiyon (AIRE geni mutasyonunda APECED sendromu); "
            "kemik iliğinde B hücrelerinde reseptör düzenlemesi (RAG genleri) ve delesyon. "
            "2. **Anerji:** B7-CD28 kostimülasyonu yokluğunda Sinyal 1 alan T hücresi anerjiye girer; CTLA-4 ve PD-1 frenler. "
            "3. **Treg Hücreleri:** CD4+ CD25+ FoxP3+ hücrelerdir; IL-10 ve TGF-beta salar, IL-2'yi emer (mutasyonunda IPEX). "
            "4. **Fas/FasL Apoptozu:** Sürekli uyarılan lenfositlerin AICD ile intiharıdır (mutasyonunda ALPS sendromu). "
            "5. **Sekestre Antijenler:** İmmünolojik ayrıcalıklı göz travmasında sempatik oftalmi gelişir. "
            "6. **Moleküler Benzerlik:** Streptokok M proteini ve kalp miyozini çapraz reaksiyonu (ARA prototipi)."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "flashcards": [
            make_flashcard(
                "k1-25-fc-s39-1",
                "Timus medullasında periferik doku antijenlerinin sunumunu yöneten ve delesyonunda APECED sendromuna yol açan kritik regülatör gen nedir?",
                "AIRE genidir.",
                "Medüller timik epitel dokusunda ektopik transkripsiyonu yöneten otoimmün regülatör",
                "AIRE Geni"
            ),
            make_flashcard(
                "k1-25-fc-s39-2",
                "Düzenleyici T lenfositlerinin (Treg) çekirdeğinde yer alan ve mutasyonunda IPEX sendromuna yol açan anahtar transkripsiyon faktörü nedir?",
                "FoxP3 proteinidir.",
                "CD4 pozitif ve CD25 pozitif regülatör lenfositlerin nükleer yönetim bileşeni",
                "FoxP3 ve IPEX"
            ),
            make_flashcard(
                "k1-25-fc-s39-3",
                "Ankilozan spondilit hastalığı ile arasında 90 kattan fazla relatif risk birlikteliği bulunan ana doku uygunluk kompleksi (HLA) alleli hangisidir?",
                "HLA-B27 lokusudur.",
                "Seronegatif spondiloartropatilerle en kuvvetli genetik bağı kuran birinci sınıf majör histokompatibilite proteini",
                "HLA-B27 Alleli"
            )
        ],
        "interactiveElements": [
            make_table(
                "Tolerans Genetik Kusurları ve Klinik Sendromlar",
                ["Kusurlu Gen / Molekül", "Etkilenen Tolerans Mekanizması", "Gelişen Klinik Sendrom", "Temel Patolojik Bulgular"],
                [
                    ["AIRE", "Timik santral negatif seleksiyon", "APECED / APS-1", "Hipoparatiroidizm, Addison, kandidiyazis"],
                    ["FoxP3", "Treg periferik süpresyonu", "IPEX Sendromu", "Neonatal Tip 1 DM, inatçı enterit, egzama"],
                    [
                        "Fas / FasL (CD95)",
                        "Aktivasyonun indüklediği hücre ölümü",
                        {"text": "ALPS Sendromu", "isMasked": True, "hint": "Apoptoza gidemeyen lenfositlerin lenf düğümlerini şişirdiği sendrom"},
                        "Masif splenomegali ve otoimmün sitopeniler"
                    ],
                    ["C1q / C2 / C4", "İmmün kompleks ve apoptotik klirens", "SLE (Lupus)", "Antinükleer antikorlar, glomerulonefrit"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki genetik mutasyon ve otoimmün sendrom eşleştirmelerinden hangisi YANLIŞTIR?",
                {
                    "A": "AIRE geni mutasyonu - APECED sendromu",
                    "B": "FoxP3 geni mutasyonu - IPEX sendromu",
                    "C": "Fas (CD95) geni mutasyonu - ALPS sendromu",
                    "D": "HLA-B27 alleli - Ankilozan spondilit",
                    "E": "FoxP3 geni mutasyonu - Bruton agamaglobulinemisi"
                },
                "E",
                {
                    "A": "Doğrudur; AIRE eksikliği APECED yapar.",
                    "B": "Doğrudur; FoxP3 eksikliği IPEX yapar.",
                    "C": "Doğrudur; Fas mutasyonu ALPS yapar.",
                    "D": "Doğrudur; HLA-B27 ankilozan spondilit ile çok güçlü ilişkilidir.",
                    "E": "YANLIŞTIR; Bruton agamaglobulinemisi FoxP3 mutasyonuyla DEĞİL, B hücre tirozin kinaz (BTK) mutasyonuyla gelişir."
                }
            )
        ]
    })

    # Slayt 40: Bölüm Özeti: Tolerans Çöküşünden Sistemik Lupus Eritematozusa Geçiş
    slides.append({
        "id": "k1-25-s40",
        "title": "Bölüm Özeti: Tolerans Çöküşünden Sistemik Lupus Eritematozusa Geçiş",
        "section": "İmmünolojik Tolerans ve Otoimmünite Gelişimi",
        "slideNumber": 40,
        "narrative": (
            "İmmünolojik toleransın hücresel ve moleküler mekanizmaları anlaşıldığında, otoimmün hastalıkların prototipi "
            "olan Sistemik Lupus Eritematozus (SLE) mükemmel bir zemin kazanır: "
            "1. **Toleransın Çoklu İflası:** SLE hastalarında hem santral hem periferik tolerans çökmüştür. "
            "Apoptoza uğrayan hücrelerin nükleer kalıntıları (DNA, histonlar, ribonükleoproteinler) kandan temizlenemez. "
            "2. **Antinükleer Antikor (ANA) Fırtınası:** B hücreleri kendi hücre çekirdeğine karşı masif antikor üretir. "
            "Oluşan DNA-antiDNA kompleksleri tüm vücut damarlarına ve glomerüllere çökerek Tip III vaskülit ve lupus nefriti yapar. "
            "Bölüm 5'te SLE'nin otoantikor spektrumunu (ANA, anti-dsDNA, anti-Smith, anti-fosfolipid), ISN/RPS sınıflamasına göre "
            "lupus nefritini ve Libman-Sacks endokarditini inceleyeceğiz."
        ),
        "sourcePdf": "Tıbbi Patoloji ABD - Aşırı Duyarlılık ve Otoimmünite (Prof. Dr. Hikmet Keleş)",
        "interactiveElements": [
            make_before_after(
                "Otoimmün Yelpazenin Zirvesi",
                "Organ Spesifik Otoimmünite",
                "Hashimoto tiroiditi veya Tip 1 DM gibi hasarın tek bir organ parankimiyle sınırlı kaldığı tablolar",
                "Sistemik Otoimmünite (SLE)",
                "Tüm hücre çekirdeklerine karşı antikor üretilen, böbrek, eklem, deri ve kalbi tutan multiorgan hastalığı"
            ),
            make_active_recall(
                "Nükleer otoantijenlere karşı kontrolsüz poliklonal antikor üretimi ve yaygın immün kompleks vaskülitiyle seyreden prototip sistemik otoimmün hastalık hangisidir?",
                "Sistemik Lupus Eritematozustur (SLE).",
                "Kelebek döküntüsü ve nefritle seyreden sistemik otoimmün bozukluk"
            )
        ]
    })

    return slides
