# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 21: Enfeksiyon Hastalıklarında Genel Kavramlar ve Temel Özellikler
(Uz. Dr. Merve Kaçar - Enfeksiyon Hastalıkları ve Klinik Mikrobiyoloji ABD)
Bölüm 6: Enfeksiyon Gelişimini Etkileyen Faktörler (Slayt 51 - 60)
Checkpoint 6: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_6_slides():
    slides = []

    # Slayt 51: Patojen-Konak Etkileşimi ve Enfeksiyon Denklemi
    slides.append({
        "id": "k1-21-s51",
        "title": "Patojen-Konak Etkileşimi: Enfeksiyonun Matematiksel Denklemi",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 51,
        "narrative": (
            "Bir mikroorganizmanın insan vücudu ile karşılaşmasından sonra enfeksiyon hastalığı gelişip gelişmeyeceğini "
            "belirleyen dinamik, enfeksiyon tıbbında meşhur bir **matematiksel orantı (enfeksiyon denklemi)** ile modellenir: "
            "**Enfeksiyon Hastalığı Riski = (Mikroorganizma Sayısı / Doz x Virülans) / Konağın Bağışıklık Direnci**. "
            "Bu denklem klinik tablonun seyrini üç temel parametreye bağlar: "
            "1. **Mikroorganizma Sayısı (İnfeksiyöz Doz):** Vücuda giren mikrop miktarıdır. Örneğin Vibrio cholerae için mide asidini geçebilmek "
            "adına 100 milyon bakteri gerekirken, Shigella dysenteriae için sadece 10-100 bakteri tek başına kanlı dizanteri başlatabilir! "
            "2. **Patojenin Virülansı:** Etkenin salgıladığı toksinler, kapsülü, enzim gücü ve doku invazyon yeteneğidir. "
            "3. **Konağın Direnci:** Deri ve mukoza bariyerleri, doğal (doğuştan) bağışıklık elemanları (fagositoz, kompleman) "
            "ve edinsel immün yanıtın (antikorlar, sitotoksik T hücreleri) toplam gücüdür. "
            "Direnci çökmüş bir konakta (örneğin nötropenik bir lösemi hastasında) son derece düşük doz ve zayıf virülanslı "
            "bir flora bakterisi dahi öldürücü sepsise yol açabilir."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Enfeksiyon hastalığı gelişim olasılığı mikrop sayısı ve virülans ile doğru konak direnci ile ters orantılıdır.",
                "ters orantılıdır",
                "Bağışıklık gücü arttıkça hastalık riskinin azalmasını ifade eden matematiksel ilişki"
            ),
            make_table(
                ["Denklem Bileşeni", "Klinik / Biyolojik Parametre", "Hastalık Riskine Etkisi"],
                [
                    ["Mikroorganizma Dozu", "Giriş yapan inokülum büyüklüğü (ID50)", "Doz arttıkça hastalık gelişme riski katlanır"],
                    [
                        "Patojen Virülansı",
                        {"text": "Toksinler, enzimler ve kapsül gücü", "isMasked": True, "hint": "Patojenitenin şiddet derecesi"},
                        "Virülans arttıkça daha küçük dozla ağır hasar oluşur"
                    ],
                    ["Konağın Bağışıklık Direnci", "Nötrofiller, antikorlar, anatomik bariyerler", "Direnç düştükçe fırsatçı etkenler dahi öldürücü olur"]
                ]
            ),
            make_micro_quiz(
                "Mide asiditesi tam olan sağlıklı bir insanda kolera hastalığı başlatmak için yüz milyon bakteri gerekirken, antasit kullanan veya mide rezeksiyonu geçiren bir bireyde yalnızca on bin bakteri ile kolera gelişmesinin nedeni nedir?",
                {
                    "A": "Bakterinin genetik yapısının midede mutasyona uğraması",
                    "B": "Mide asiditesi bariyerinin ortadan kalkmasıyla konak direncinin düşmesi ve infeksiyöz doz eşiğinin azalması",
                    "C": "Kolera toksininin sadece bazik ortamda aktifleşebilmesi",
                    "D": "Hastanın kan grubunun değişmesi",
                    "E": "Antasitlerin doğrudan Vibrio çoğalmasını uyarması"
                },
                "B",
                {
                    "A": "A seçeneği yanlıştır; bakterinin mutasyonuyla ilişkili değildir.",
                    "B": "B seçeneği doğrudur: Mide asidi (pH < 2) çok güçlü bir primer konak savunma bariyeridir; asit kalktığında konak direnci çöker ve hastalık için gereken mikrop dozu dramatik şekilde düşer.",
                    "C": "C seçeneği yanlıştır; toksin ince bağırsakta etki eder.",
                    "D": "D seçeneği imkansızdır.",
                    "E": "E seçeneği yanlıştır."
                }
            )
        ]
    })

    # Slayt 52: Mikroorganizma Virülans Faktörleri: Adezinler ve İnvazyon
    slides.append({
        "id": "k1-21-s52",
        "title": "Virülans Faktörleri: Adezinler ve Mukozal Kolonizasyon",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 52,
        "narrative": (
            "Bir patojenin insan vücudunda enfeksiyon başlatabilmesi için aşması gereken ilk basamak, "
            "vücut sıvıları (idrar akımı, mukus akıntısı, bağırsak peristaltizmi) tarafından mekanik olarak yıkanıp "
            "dışarı atılmayı engellemektir. Bu hayati tutunma sürecini sağlayan moleküllere **adezinler** adı verilir: "
            "1. **Fimbriyalar / Pili:** Bakteri yüzeyinden uzanan protein yapılı tüycüklerdir. "
            "Örneğin; üropatojenik Escherichia coli (UPEC) taşıdığı **Tip 1 fimbriyalar** ile mesane üroepitelindeki mannoza, "
            "**P-fimbriyaları (Pap pili)** ile ise böbrek tübül epiteli ve renal pelvis yüzeyindeki digalaktozit reseptörlerine tutunur. "
            "P-fimbriyası taşımayan E. coli suşları akut piyelonefrit yapamaz, idrarla atılır! "
            "2. **Afimbriyal Adezinler:** Hücre duvarına gömülü yüzey proteinleridir. "
            "Bordetella pertussis (boğmaca) flamentöz hemaglütinin (FHA) ile solunum silier epiteline; "
            "Streptococcus pyogenes **M proteini** ve lipoteikoik asit ile farenks keratinositlerine sıkıca yapışır. "
            "Tutunmayı başaran bakteri mukozada hızla mikrokoloniler kurarak biyofilm ve invazyon aşamasına geçer."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Üropatojenik E. coli bakterisinin böbrek parankimine tutunarak akut piyelonefrit yapmasını sağlayan özgül adezin organeli P-fimbriyası organelidir.",
                "P-fimbriyası",
                "Renal pelvis digalaktozit reseptörlerine bağlanan bakteriyel fimbriya türü"
            ),
            make_causal_chain(
                "Mukozal Adezyondan Doku Kolonizasyonuna Geçiş",
                [
                    "1. Mukozal Temas: Bakteri mukus tabakasını geçerek epitel hücre yüzeyine yaklaşır.",
                    "2. Spesifik Reseptör Tanıma: Bakteriyel adezin epiteldeki glikoprotein reseptörüne kilitlenir.",
                    "3. Yıkanmaya Direnç: İdrar veya peristaltizmin sürükleyici mekanik kuvvetine karşı ankoraj sağlanır.",
                    "4. Mikrokoloni Oluşumu: Tutunan bakteri ikili fizyonla çoğalarak epitel üzerinde kümelenir.",
                    "5. İnvazyon Enzimleri: Salınan proteaz ve toksinlerle epitel hücre içine veya submukozaya penetre olunur."
                ]
            ),
            make_active_recall(
                "Streptococcus pyogenes (A grubu streptokok) bakterisinin hem farenks epiteline adezyonunu sağlayan hem de fagositozu engelleyen majör virülans yüzey proteini hangisidir?",
                "M proteinidir (Tip spesifik M proteini).",
                "Romatizmal ateş patogenezinde moleküler taklit yapan streptokok proteini"
            )
        ]
    })

    # Slayt 53: Bakteriyel Toksinler: Ekzotoksinler vs Endotoksin
    slides.append({
        "id": "k1-21-s53",
        "title": "Bakteriyel Toksinler: Ekzotoksinler ile Endotoksin Karşılaştırması",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 53,
        "narrative": (
            "Bakterilerin doku hasarı oluşturmak ve konağı felç etmek için ürettikleri en ölümcül silahlar toksinlerdir. "
            "Toksinler yapısal ve biyolojik özelliklerine göre iki temel sınıfa ayrılır: "
            "1. **Ekzotoksinler:** Canlı bakteriler (hem Gram-pozitif hem Gram-negatif) tarafından sentezlenip dış çevreye aktif olarak salgılanan "
            "**protein yapılı** moleküllerdir. Genellikle iki kısımdan (A-B toksinleri: B bağlanan, A aktif enzim) oluşurlar. "
            "Isıya duyarlıdırlar (termolabil). Formalin ile muamele edildiklerinde toksisitelerini kaybedip antijenisitelerini korurlar; "
            "bu zararsız formlarına **toksoid** denir ve çok başarılı koruyucu aşılar (Tetanoz ve Difteri aşıları) üretilir! "
            "En ölümcül zehirlerdir (Botulinum toksininin 1 gramı milyonlarca insanı öldürebilir). "
            "2. **Endotoksin (LPS Lipid A):** Yalnızca **Gram-negatif bakterilerin dış membranında** bulunan yapısal bir bileşendir. "
            "Bakteri canlıyken salgılanmaz; bakteri lizise uğradığında veya çoğalırken açığa çıkar. "
            "Lipid yapılı olduğundan **ısıya son derece dirençlidir** (otoklavla bile yıkılamaz). "
            "Makrofajlardaki TLR4 reseptörünü uyararak masif sitokin patlaması (TNF-alfa, IL-1) yapar; "
            "**toksoidi yapılamaz ve aşısı yoktur**; yüksek dozda irreversible septik şok, DIC ve çoklu organ yetmezliğine yol açar."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Ekzotoksinlerin formalin ile muamele edilerek toksisitesi giderilmiş ancak aşı amacıyla kullanılan immünojenik formuna toksoid adı verilir.",
                "toksoid",
                "Tetanoz ve difteri aşılarının hazırlandığı inaktive toksin formu"
            ),
            make_before_after(
                "Ekzotoksinler ile Endotoksinin Temel Farkları",
                "Ekzotoksinler (Örn. Tetanoz, Difteri)",
                [
                    "Canlı bakteri tarafından dış ortama aktif olarak salgılanır",
                    "Protein yapılıdır, ısıya son derece duyarlıdır (termolabil)",
                    "Formalinle toksoid aşı haline getirilebilir",
                    "Geri dönüşümlü spesifik hücre reseptörlerine bağlanır, son derece ölümcüldür"
                ],
                "Endotoksin (LPS Lipid A)",
                [
                    "Yalnızca Gram-negatif dış membranında yer alır, lizisle açığa çıkar",
                    "Lipopolisakkarit (Lipid A) yapılıdır, ısıya son derece dirençlidir",
                    "Toksoidi yapılamaz, etkili bir aşısı bulunmaz",
                    "TLR4 üzerinden pirojenik ateş, hipotansiyon ve septik şok tetikler"
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki özelliklerden hangisi bakteriyel 'Endotoksin' (LPS) için doğru, 'Ekzotoksinler' için yanlıştır?",
                {
                    "A": "Protein yapısında olması ve ribozomlarda sentezlenmesi",
                    "B": "Isıya son derece dirençli olması ve formalinle toksoid aşı yapılamaması",
                    "C": "Canlı bakteri hücresinden dış çevreye aktif olarak salgılanması",
                    "D": "Genellikle A-B alt birim yapısında organize olması",
                    "E": "Hem Gram-pozitif hem Gram-negatif bakterilerce üretilebilmesi"
                },
                "B",
                {
                    "A": "A seçeneği ekzotoksinlerin özelliğidir; endotoksin lipid-polisakkarittir.",
                    "B": "B seçeneği doğrudur: Endotoksin ısıya dayanıklıdır ve toksoidi üretilemez; ekzotoksinler ise ısıyla denatüre olur ve toksoid aşısı yapılabilir.",
                    "C": "C seçeneği ekzotoksinlerin özelliğidir.",
                    "D": "D seçeneği ekzotoksinlerin özelliğidir.",
                    "E": "E seçeneği ekzotoksinlerin özelliğidir; endotoksin sadece Gram-negatiflerdedir."
                }
            )
        ]
    })

    # Slayt 54: Doku İnvazyon ve Yayılma Enzimleri
    slides.append({
        "id": "k1-21-s54",
        "title": "Doku İnvazyon Enzimleri: Yayılma ve Doku Sindirimi",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 54,
        "narrative": (
            "Patojen bakteriler konak bağ dokusu engellerini aşmak, doku planları boyunca hızla yayılmak "
            "ve kan pıhtılarını eriterek serbestleşmek için çeşitli ekstrasellüler enzimler salgılarlar: "
            "1. **Hyaluronidaz ('Yayılma Faktörü' / Spreading Factor):** Bağ dokusunun temel maddesi olan hücreler arası hyaluronik asidi parçalar. "
            "Streptococcus pyogenes ve Staphylococcus aureus doku aralıklarında hızla yayılarak flegmon ve selülit oluşturur. "
            "2. **Kollajenaz:** Kas ve tendonlardaki kollajen liflerini parçalar. "
            "Clostridium perfringens kas planlarını sindirerek ölümcül **gazlı gangren (miyonekroz)** tablosuna yol açar. "
            "3. **Streptokinaz (Fibrinolizin):** Plazminojeni aktif plazmine çevirerek konağın bakteriyi hapsetmek için ördüğü fibrin bariyerlerini eritir; "
            "streptokokların dokuda sınırlandırılamayan yaygın selülit yapmasının temel nedenidir. "
            "4. **Koagülaz:** S. aureus'a özgüdür; plazmadaki fibrinojeni fibrine çevirerek bakterinin etrafına yalancı bir fibrin kalkanı örer; "
            "bakteriyi fagositozdan koruyarak lokalize apseler (çıban, fronkül) oluşturmasını sağlar. "
            "5. **Lesitinaz (Fosfolipaz C / Alfa Toksin):** Hücre zarlarındaki lesitini parçalayarak eritrositleri, lökositleri ve kas hücrelerini hızla lize eder."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bağ dokusunun zemin maddesini parçalayarak mikroorganizmanın doku planlarında hızla yayılmasını sağlayan enzime hyaluronidaz denir.",
                "hyaluronidaz",
                "Spreading factor olarak bilinen hücreler arası matriks sindirici enzim"
            ),
            make_table(
                ["İnvazyon Enzimi", "Bakteriyel Kaynak", "Etki Mekanizması ve Klinik Sonucu"],
                [
                    ["Hyaluronidaz", "S. pyogenes, S. aureus", "Hücreler arası hyaluronik asidi sindirerek selülit yayılımı sağlar"],
                    [
                        "Kollajenaz",
                        {"text": "Clostridium perfringens", "isMasked": True, "hint": "Gazlı gangren yapan anaerop basil"},
                        "Kas ve fasya kollajenini eriterek miyonekroz ve gangren yapar"
                    ],
                    ["Koagülaz", "Staphylococcus aureus", "Fibrin kalkanı örerek bakteriyi fagositozdan korur ve apse yapar"],
                    ["Streptokinaz", "Streptococcus pyogenes", "Fibrin pıhtılarını eriterek sınırlandırmayı bozar ve hızla yayılır"]
                ]
            ),
            make_micro_quiz(
                "Staphylococcus aureus'u diğer stafilokoklardan ayıran, plazmayı pıhtılaştırarak bakterinin çevresinde fagositozu engelleyen bir fibrin zırhı oluşturan anahtar enzim hangisidir?",
                {
                    "A": "Katalaz",
                    "B": "Koagülaz",
                    "C": "Streptokinaz",
                    "D": "Amilaz",
                    "E": "Elastaz"
                },
                "B",
                {
                    "A": "A seçeneği tüm stafilokoklarda pozitiftir, S. aureus'a özgü fibrin kalkanı yapmaz.",
                    "B": "B seçeneği doğrudur: Koagülaz S. aureus'un temel virülans ve tanımlama enzimidir; fibrinojeni pıhtılaştırarak koruyucu bariyer kurar.",
                    "C": "C seçeneği streptokoklardadır ve pıhtıyı eritir.",
                    "D": "D seçeneği karbonhidrat sindirir.",
                    "E": "E seçeneği elastini parçalar."
                }
            )
        ]
    })

    # Slayt 55: Biyofilm Oluşumu ve Antimikrobiyal Direnç
    slides.append({
        "id": "k1-21-s55",
        "title": "Biyofilm Oluşumu: Yabancı Cisimler ve Tedavi Direnci",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 55,
        "narrative": (
            "Biyofilm; mikroorganizmaların canlı bir doku veya cansız bir yabancı cisim yüzeyine yapışarak "
            "kendi salgıladıkları yapışkan bir **Ekstrasellüler Polimerik Matriks (EPS - glikokaliks/balçık)** içine "
            "gömüldükleri organize çok hücreli mikrobiyal topluluklardır. "
            "Bakteriler biyofilm içinde tek tek yüzen planktonik formlarından tamamen farklı davranırlar; "
            "birbirleriyle kimyasal sinyallerle haberleşirler (**Quorum Sensing / Çoğunluk Algılaması**). "
            "Biyofilmler modern hastane enfeksiyonlarının en büyük kabusudur: "
            "Santral venöz kateterler, idrar sondaları, endotrakeal tüpler, ortopedik eklem protezleri ve yapay kalp kapakları "
            "biyofilm oluşumunun prototipik alanlarıdır. "
            "En klasik biyofilm üreticileri **Staphylococcus epidermidis** ve **Pseudomonas aeruginosa**'dır. "
            "Biyofilm içindeki bakteriler standart antibiyotik konsantrasyonlarına karşı **100 ila 1000 kat daha dirençlidir**; "
            "çünkü EPS matrisi antibiyotiklerin içeri sızmasını engeller, içerideki bakteriler yavaş bölünür (metabolik uyku) "
            "ve nötrofiller kalın biyofilm örtüsünü fagosite edemez. Çoğu zaman tek kesin çözüm yabancı cismin cerrahi olarak çıkarılmasıdır!"
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Bakterilerin biyofilm içinde nüfus yoğunluğunu algılayıp haberleşerek virülans genlerini aktive etmesine quorum sensing denir.",
                "quorum sensing",
                "Bakteriyel çoğunluk algılaması ve kimyasal iletişim mekanizması"
            ),
            make_causal_chain(
                "Yabancı Cisim Üzerinde Biyofilm Gelişim Süreci",
                [
                    "1. Reversible Tutunma: Planktonik S. epidermidis protez yüzeyine van der Waals kuvvetleriyle yaklaşır.",
                    "2. İrreversible Ankoraj: Bakteriyel adezinler yabancı cisim yüzeyindeki fibronektine sıkıca kilitlenir.",
                    "3. EPS Salgısı: Bakteriler polisakkarit interselüler adezin (PIA) salgılayarak balçık matriksi örer.",
                    "4. Olgun Biyofilm: Matriks içinde besin kanalları ve quorum sensing ile organize koloniler oluşur.",
                    "5. Antibiyotik Direnci ve Kopma: İlaçlar içeri giremez; kopan bakteriler aralıklı bakteriyemi atakları yapar."
                ]
            ),
            make_micro_quiz(
                "Yapay kalp kapağı veya ortopedik kalça protezi takılan bir hastada gelişen biyofilm ilişkili yabancı cisim enfeksiyonlarında en sık izole edilen ve EPS salgılayan mikroorganizma hangisidir?",
                {
                    "A": "Staphylococcus epidermidis",
                    "B": "Streptococcus pneumoniae",
                    "C": "Neisseria meningitidis",
                    "D": "Clostridium tetani",
                    "E": "Shigella sonnei"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Koagülaz-negatif stafilokok olan S. epidermidis plastik ve metal yabancı cisimlere güçlü biyofilm yaparak protez enfeksiyonlarının 1 numaralı nedenidir.",
                    "B": "B seçeneği protez enfeksiyonu yapmaz.",
                    "C": "C seçeneği menenjit etkenidir.",
                    "D": "D seçeneği toprak kaynaklı anaeroptur.",
                    "E": "E seçeneği dizanteri etkenidir."
                }
            )
        ]
    })

    # Slayt 56: Konak İmmün Savunmasından Kaçış Stratejileri
    slides.append({
        "id": "k1-21-s56",
        "title": "Konak İmmün Savunmasından Kaçış Stratejileri",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 56,
        "narrative": (
            "Başarılı patojenler, konak bağışıklık sisteminin ölümcül tuzaklarından kurtulabilmek için "
            "evrimsel süreçte son derece sofistike mekanizmalar geliştirmişlerdir: "
            "1. **Fagositozun Engellenmesi:** Polisakkarit **kapsül** nötrofil ve makrofajların bakteriyi yakalamasını engeller (S. pneumoniae, N. meningitidis, H. influenzae). "
            "Bazı bakteriler yüzey proteinleriyle kompleman C3b opsonizasyonunu bloke eder (S. pyogenes M proteini). "
            "2. **İntrasellüler Yaşam (Fagozom-Lizozom Füzyonunu Engelleme):** Fagosite edilen bakteri lizozomla kaynaşmayı önleyerek "
            "makrofajın içinde canlı kalır ve çoğalır (Mycobacterium tuberculosis, Legionella pneumophila, Chlamydia). "
            "Listeria monocytogenes ise listeriyolizin O ile fagozom zarını parçalayıp sitoplazmaya kaçar ve aktin kuyruğu yaparak komşu hücreye geçer! "
            "3. **Antijenik Varyasyon:** Yüzey proteinlerini sürekli değiştirerek mevcut antikorları işlevsiz kılma "
            "(Neisseria gonorrhoeae pilin gen değişimi, Borrelia recurrentis değişken yüzey antijenleri, İnfluenza virüsü antijenik drift/shift). "
            "4. **İmmünglobulin A (IgA) Proteaz Salgılanması:** Mukoza savunmasının kilit antikorunu (sekretuvar IgA) "
            "menteşe bölgesinden keserek mukozal kolonizasyonu kolaylaştırma (S. pneumoniae, H. influenzae, N. meningitidis üçlüsü!)."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Mukozal yüzeyleri kolonize eden S. pneumoniae ve N. meningitidis gibi bakteriler konak sekretuvar antikorunu parçalamak için IgA proteaz enzimi salgılarlar.",
                "IgA proteaz",
                "Mukozal antikorları inaktive eden bakteriyel virülans enzimi"
            ),
            make_table(
                ["İmmün Kaçış Mekanizması", "Kullanılan Bakteriyel Faktör", "Prototip Mikroorganizmalar"],
                [
                    ["Fagositozdan Kaçış", "Polisakkarit kapsül zırhı", "Streptococcus pneumoniae, Neisseria meningitidis"],
                    [
                        "Fagozom-Lizozom Blokajı",
                        {"text": "Hücre içi sağkalım molekülleri", "isMasked": True, "hint": "Makrofaj içinde yaşam stratejisi"},
                        "Mycobacterium tuberculosis, Legionella pneumophila"
                    ],
                    ["Sitoplazmaya Kaçış", "Listeriyolizin O (por oluşturan toksin)", "Listeria monocytogenes"],
                    ["Mukozal Antikor Yıkımı", "Sekretuvar antikor menteşe kesimi", "IgA proteaz üreten kapsüllü menenjit etkenleri"],
                    ["Antijenik Varyasyon", "Pilin gen kaset rekombinasyonu", "Neisseria gonorrhoeae, Borrelia recurrentis"]
                ]
            ),
            make_micro_quiz(
                "Aşağıdaki mikroorganizmalardan hangisi makrofaj tarafından fagosite edildikten sonra fagozom zarını 'listeriyolizin O' enzimiyle delip parçalayarak sitoplazmaya kaçar ve hücreden hücreye aktin kuyruğuyla yayılır?",
                {
                    "A": "Listeria monocytogenes",
                    "B": "Streptococcus pneumoniae",
                    "C": "Vibrio cholerae",
                    "D": "Clostridium tetani",
                    "E": "Mycoplasma pneumoniae"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Listeria monocytogenes fagozomdan sitoplazmaya listeriyolizin O ile kaçarak intrasellüler motilite (aktin roketleri) sergiler.",
                    "B": "B seçeneği hücre dışı kapsüllü bakteridir.",
                    "C": "C seçeneği bağırsak lümeninde kalır.",
                    "D": "D seçeneği ekzotoksin salgılar, hücre içi yayılmaz.",
                    "E": "E seçeneği epitele yüzeyden yapışır."
                }
            )
        ]
    })

    # Slayt 57: Konak Duyarlılık Faktörleri I: Yaş Uçları ve Malnütrisyon
    slides.append({
        "id": "k1-21-s57",
        "title": "Konak Duyarlılık Faktörleri I: Yaş Uçları ve Beslenme",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 57,
        "narrative": (
            "Enfeksiyon gelişim denkleminde mikroorganizma kadar konağın fizyolojik durumu da belirleyicidir. "
            "Yaşamın iki uç dönemi enfeksiyonlara en açık savunmasız pencerelerdir: "
            "1. **Yenidoğan ve Erken Süt Çocukluğu Dönemi:** İmmün sistem henüz olgunlaşmamıştır (immatürite). "
            "Kompleman düzeyleri düşüktür, nötrofil kemotaksisi zayıftır ve endojen antikor yapımı yetersizdir. "
            "Annede bulunan IgG antikorları plasenta yoluyla bebeğe geçerek ilk aylarda koruma sağlar; "
            "ancak **3-6. aylarda maternal IgG'lerin tükenmesiyle** bebekte geçici bir hipogammaglobulinemi penceresi oluşur. "
            "Yenidoğanlarda özellikle **Grup B Streptokoklar (Streptococcus agalactiae)**, **Escherichia coli** ve **Listeria monocytogenes** "
            "ölümcül menenjit ve sepsis etkenleridir. "
            "2. **İleri Yaş (Geriatrik Dönem / İmmünosenesans):** Timus involüsyonuna bağlı naif T hücre üretimi durur, "
            "antikor yanıtları zayıflar, mukosiliyer klirens yavaşlar ve öksürük refleksi körelir. Bu durum yaşlılarda lober pnömoni ve ürosepsisi tetikler. "
            "3. **Malnütrisyon:** Protein-enerji malnütrisyonu (kuvaşiorkor, marasmus) lenfoid organ atrofisi yaparak hücresel bağışıklığı felç eder; "
            "A vitamini eksikliği mukozal epitel bütünlüğünü bozar, çinko eksikliği ise lenfosit proliferasyonunu durdurur."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Yenidoğan menenjiti ve sepsisinin en sık etkeni olan bakteri annenin doğum kanalından bulaşan Grup B Streptokok bakterisidir.",
                "Grup B Streptokok",
                "Streptococcus agalactiae olarak da bilinen neonatal sepsis etkeni"
            ),
            make_before_after(
                "Yenidoğan ile Geriatrik Konak İmmün Yetersizlik Farkları",
                "Yenidoğan İmmün İmmatüritesi",
                [
                    "Kompleman sentezi ve fagositoz kemotaksisi henüz yetersizdir",
                    "Doğumda maternal IgG var; 3-6. ayda tükenerek boşluk oluşur",
                    "Kapsüllü bakterilere karşı T-bağımsız polisakkarit antikor üretemez",
                    "En sık tehditler: Grup B Streptokok, E. coli K1, Listeria"
                ],
                "Geriatrik İmmünosenesans",
                [
                    "Timus dokusu yağlanmıştır; yeni naif T lenfosit üretimi durur",
                    "Bellek T hücreleri disfonksiyoneldir, aşı yanıtları düşüktür",
                    "Mukosiliyer yürüyen merdiven bozulur, mikroaspirasyon artar",
                    "En sık tehditler: Pnömokok pnömonisi, Ürosepsis, Zona reaktivasyonu"
                ]
            ),
            make_micro_quiz(
                "Yenidoğan döneminde (ilk 28 gün) gelişen menenjit ve sepsis tablolarında en sık karşılaşılan üç majör bakteriyel etken hangisinde eksiksiz verilmiştir?",
                {
                    "A": "Grup B Streptokok (S. agalactiae), Escherichia coli, Listeria monocytogenes",
                    "B": "Neisseria meningitidis, Streptococcus pneumoniae, Haemophilus influenzae",
                    "C": "Staphylococcus aureus, Pseudomonas aeruginosa, Klebsiella pneumoniae",
                    "D": "Mycobacterium tuberculosis, Treponema pallidum, Borrelia burgdorferi",
                    "E": "Clostridium tetani, Bacillus anthracis, Corynebacterium diphtheriae"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Yenidoğan sepsisi ve menenjitinin klasik üçlüsü Grup B streptokoklar, E. coli ve Listeria'dır.",
                    "B": "B seçeneği 1 ay - 50 yaş arası çocuk ve erişkin menenjitlerinin ana etkenleridir.",
                    "C": "C seçeneği hastane kökenli nozokomiyal etkenlerdir.",
                    "D": "D seçeneği kronik/spiroketal hastalıklardır.",
                    "E": "E seçeneği toksin aracılı hastalıklardır."
                }
            )
        ]
    })

    # Slayt 58: Konak Duyarlılık Faktörleri II: Komorbiditeler ve İmmünsüpresyon
    slides.append({
        "id": "k1-21-s58",
        "title": "Konak Duyarlılık Faktörleri II: Komorbidite ve İmmünsüpresyon",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 58,
        "narrative": (
            "Konağın altta yatan kronik hastalıkları ve immün yetmezlik tabloları, spesifik patojenlere karşı dramatik bir yatkınlık yaratır: "
            "1. **Diyabetes Mellitus:** Hiperglisemi nötrofillerin kemotaksisini, fagositozunu ve intrasellüler öldürme yeteneğini bozar; "
            "mikrovasküler iskemi doku perfüzyonunu azaltır. Diyabetiklerde S. aureus ayak ülserleri, Pseudomonas malign otitis eksterna "
            "ve rinoserebral **Mukormikoz** riski katlanarak artar. "
            "2. **Aspleni (Dalağı Olmayan Bireyler):** Dalak, kandan kapsüllü bakterileri süzen ve opsonin üreten en kritik filtredir. "
            "Splenektomili veya orak hücreli anemili hastalarda kapsüllü bakteriler (**Streptococcus pneumoniae**, **Neisseria meningitidis**, **Haemophilus influenzae**) "
            "saatler içinde fatal **Ezici Post-Splenektomi Enfeksiyonuna (OPSI)** yol açar; bu hastalar mutlaka aşılanmalıdır! "
            "3. **Nötropeni (Mutlak Nötrofil Sayısı < 500 /mm³):** Kemoterapi veya lösemi zemininde gelişir; "
            "Pseudomonas aeruginosa sepsisi ve invaziv küf mantarları (Aspergillus) için en yüksek risk grubudur. "
            "4. **Hücresel İmmün Yetmezlik (HIV / CD4 < 200, İntravenöz Steroid):** İntrasellüler patojenlere "
            "(Pneumocystis jirovecii, Cryptococcus, Toxoplasma, CMV, Mycobacterium) karşı savunma tamamen çöker."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Dalağı cerrahi olarak çıkarılmış asplenik hastalarda kapsüllü bakterilere bağlı gelişen fulminan tabloya ezici post-splenektomi enfeksiyonu denir.",
                "post-splenektomi",
                "Dalak yokluğunda saatler içinde ölüme götüren fulminan sepsis tablosu"
            ),
            make_table(
                ["İmmün Defekt / Komorbidite", "Bozulan Savunma Mekanizması", "Predispoze Olunan Kritik Patojenler"],
                [
                    ["Aspleni (Dalak yokluğu)", "Dolaşımdaki opsonize bakterilerin süzülememesi", "S. pneumoniae, N. meningitidis, H. influenzae (Kapsüllüler)"],
                    [
                        "Ağır Nötropeni (ANS < 500)",
                        {"text": "Bakteriyel ve fungal fagositoz yokluğu", "isMasked": True, "hint": "Nötrofil sayısının kritik düzeye inmesi"},
                        "Pseudomonas aeruginosa, Candida, Aspergillus fumigatus"
                    ],
                    ["Hücresel İmmün Defekt (AIDS)", "CD4 T yardımcı hücre kaybı ve sitokin çöküşü", "Pneumocystis jirovecii, Cryptococcus, Toksoplazma"],
                    ["Diyabetes Mellitus", "Nötrofil fagositoz bozukluğu ve doku hipoksisi", "S. aureus, Rinoserebral Mukor, Malign eksternal otit"]
                ]
            ),
            make_micro_quiz(
                "Trafik kazası nedeniyle acil splenektomi (dalak çıkarılması) yapılan 30 yaşındaki bir hastada gelecekteki ezici post-splenektomi enfeksiyonunu (OPSI) önlemek için taburculuk öncesi mutlaka uygulanması gereken aşı grubu hangisidir?",
                {
                    "A": "Yalnızca canlı atenüe kızamık-kızamıkçık-kabakulak aşısı",
                    "B": "Pnömokok, Meningokok ve Haemophilus influenzae tip b kapsül aşıları",
                    "C": "Kuduz ve tetanoz toksoid aşıları",
                    "D": "Oral canlı polio ve kolera aşıları",
                    "E": "Yalnızca Hepatit A ve Hepatit B aşıları"
                },
                "B",
                {
                    "A": "A seçeneği viral aşıdır, asplenik kapsüllü sepsisini önlemez.",
                    "B": "B seçeneği doğrudur: Asplenik bireyler kapsüllü bakterilere (S. pneumoniae, N. meningitidis, Hib) aşırı duyarlıdır; bu üç aşı hayat kurtarır.",
                    "C": "C seçeneği endikasyon varsa yapılır, aspleniye spesifik profilaksi değildir.",
                    "D": "D seçeneği yetersizdir.",
                    "E": "E seçeneği viral hepatit aşılarıdır."
                }
            )
        ]
    })

    # Slayt 59: [TEKRAR SAYFASI - CHECKPOINT 6]
    slides.append({
        "id": "k1-21-s59",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Enfeksiyon Gelişim Faktörleri ve Virülans",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 59,
        "narrative": (
            "Bu altıncı checkpoint sayfasında enfeksiyonun matematiksel denklemini, "
            "ekzotoksinler ile endotoksin arasındaki temel farmakolojik ve biyokimyasal farkları, "
            "biyofilm oluşumunun yabancı cisim enfeksiyonlarında yarattığı devasa antibiyotik direncini "
            "3 adet yüksek verimli aktif hatırlama kartı üzerinden pekiştiriyoruz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_flashcard(
                "fc-k1-21-cp6-1",
                "Bakteriyel ekzotoksinler ile endotoksin (LPS Lipid A) arasındaki temel yapısal ve aşılanma farkları nelerdir?",
                "Ekzotoksinler protein yapılıdır, canlı bakteriden dışarı salgılanır, ısıyla denatüre olur ve formalinle toksoid aşı haline getirilebilir. Endotoksin ise Gram-negatif dış membranındaki Lipid A parçasıdır; ısıya çok dirençlidir, toksoidi yapılamaz ve aşısı yoktur.",
                "Aktif sentezlenen polipeptit ile lizis sonrası dökülen çeper fraksiyonunun mukayesesi",
                "Bakteriyel Toksinler"
            ),
            make_flashcard(
                "fc-k1-21-cp6-2",
                "Kateter ve protez gibi yabancı cisimler üzerinde gelişen biyofilmler neden standart antibiyotik tedavilerine aşırı dirençlidir?",
                "Bakterilerin salgıladığı ekstrasellüler polimerik matriks (EPS) antibiyotik geçişini bloke eder; içerideki bakteriler yavaş bölünerek metabolik uykuya geçer ve nötrofil fagositozundan korunur.",
                "Mukoid kalkanın medikal difüzyonu engellemesi ve hücresel persistan fazı",
                "Biyofilm Patolojisi"
            ),
            make_flashcard(
                "fc-k1-21-cp6-3",
                "Dalağı cerrahi olarak çıkarılmış (asplenik) bireylerde en ölümcül sepsislere yol açan bakteri grubu hangisidir ve neden?",
                "Kapsüllü bakterilerdir (Streptococcus pneumoniae, Neisseria meningitidis, Haemophilus influenzae). Dalak kandan opsonize kapsüllü bakterileri temizleyen ana filtre organ olduğu için dalak yokluğunda fulminan sepsis gelişir.",
                "Retiküloendotelyal süzme mekanizmasının yoksunluğu ve polisakkarit kılıflı patojenler",
                "Konak Savunması"
            )
        ]
    })

    # Slayt 60: Anatomik Bariyerler ve Bölüm Özeti
    slides.append({
        "id": "k1-21-s60",
        "title": "Anatomik Bariyerler ve Enfeksiyon Faktörleri Özeti",
        "section": "Enfeksiyon Gelişim Faktörleri",
        "slideNumber": 60,
        "narrative": (
            "Mikroorganizma ile konak arasındaki ilk ve en kritik savaş cephesi **anatomik bariyerlerdir**. "
            "Sağlam deri, çok katlı yassı keratinize epiteli, ter bezlerinin salgıladığı yağ asitleri (pH 5.5) "
            "ve antimikrobiyal peptitleri (defensinler) ile aşılamaz bir kale duvarıdır. "
            "Geniş yanıklar bu koruyucu deriyi ortadan kaldırdığında, Pseudomonas aeruginosa ve S. aureus saniyeler içinde ölümcül bakteriyemiye yol açar. "
            "Solunum yollarındaki **mukosiliyer yürüyen merdiven (klirens)**, partikülleri yutulmak üzere yukarı taşır; "
            "sigara, viral enfeksiyonlar veya entübasyon tüpleri siliaları felç ettiğinde bakteriler doğrudan akciğer parankimine inerek pnömoni yapar. "
            "İdrar akımının mekanik yıkayıcı kuvveti, üriner epiteli steril tutar; idrar sondası (Foley kateter) takılması "
            "bu akımı bozarak kateter ilişkili üriner enfeksiyonların kapısını aralar. "
            "Özetle; enfeksiyon patojenin saldırı gücü ile konağın savunma gücü arasındaki dengedir. "
            "Peki vücudumuzun dış dünyaya açık yüzeylerinde bizimle barış içinde yaşayan trilyonlarca dost mikroorganizma bu denklemde nerede durur? "
            "Yedinci bölümümüzde **normal mikrobiyotayı ve steril vücut bölgelerini** inceleyeceğiz."
        ),
        "sourcePdf": "Enfeksiyon Hastalıkları ABD - Enfeksiyon Hastalıklarında Genel Kavramlar",
        "interactiveElements": [
            make_cloze(
                "Solunum yolu epitelinde partikülleri ve bakterileri yukarıya süpüren savunma mekanizmasına mukosiliyer klirens adı verilir.",
                "mukosiliyer klirens",
                "Silialı silindirik epitelin mekanik akciğer temizleme sistemi"
            ),
            make_table(
                ["Anatomik Bariyer", "Fizyolojik Savunma Mekanizması", "Bariyer İhlalinde Görülen Enfeksiyon"],
                [
                    ["Stratum Korneum (Deri)", "Kuru keratin tabakası, asidik ter yağ asitleri", "Yanık ve cerrahi insizyonda S. aureus ve Pseudomonas sepsisi"],
                    [
                        "Mukosiliyer Asansör",
                        {"text": "Siliaların ritmik yukarı süpürme hareketi", "isMasked": True, "hint": "Solunum yolundaki temizleyici epitel"},
                        "Sigara ve entübasyon zemininde nosokomiyal pnömoni"
                    ],
                    ["İdrar Akımı (Washout)", "Tek yönlü mekanik yıkayıcı hidrolik basınç", "Foley kateter takılmasında asendan üriner enfeksiyon"]
                ]
            ),
            make_micro_quiz(
                "Geniş vücut yanığı olan bir hastada yanık yüzeyinden kaynaklanan, mavi-yeşil renkli piyosiyanin pigmenti salgılayan ve ektima gangrenozum lezyonlarıyla seyreden en olası hastane patojeni hangisidir?",
                {
                    "A": "Pseudomonas aeruginosa",
                    "B": "Streptococcus pneumoniae",
                    "C": "Treponema pallidum",
                    "D": "Helicobacter pylori",
                    "E": "Mycoplasma pneumoniae"
                },
                "A",
                {
                    "A": "A seçeneği doğrudur: Pseudomonas aeruginosa yanık enfeksiyonlarının prototipik etkenidir; mavi-yeşil pigment (piyosiyanin/piyoverdin) ve nekrotik lezyonlar yapar.",
                    "B": "B seçeneği solunum patojenidir.",
                    "C": "C seçeneği sifilis etkenidir.",
                    "D": "D seçeneği mide patojenidir.",
                    "E": "E seçeneği atipik pnömoni etkenidir."
                }
            )
        ]
    })

    return slides
