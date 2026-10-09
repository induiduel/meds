# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-12-s61",
        "title": "Membran Atak Kompleksi (MAC / C5b-9) ve Neisseria Duyarlılığı",
        "content": "Kompleman aktivasyonunun son aşaması, hedef hücre zarını doğrudan delerek parçalayan **Membran Atak Kompleksinin (MAC / C5b-9)** montajıdır. C5 konvertaz C5'i kestikten sonra süreç enzimatik olmaktan çıkıp tamamen fiziksel bir polimerizasyon reaksiyonuna dönüşür:\n\n1. **Montaj:** C5b önce C6 ve C7'ye bağlanır; oluşan C5b-7 kompleksi hidrofobik bir bölge kazanarak mikrop lipid çift katmanına gömülür. Ardından C8 katılır ve zarı delmeye başlar.\n2. **Por Oluşumu:** C5b-8 kompleksi katalizörlük yaparak 10 ila 16 adet **C9 molekülünün** halka şeklinde polimerize olmasını sağlar. Zarda 10 nanometre çapında devasa, kontrolsüz bir transmembran su kanalı (por) açılır.\n3. **Ozmotik Lizis:** Hücre dışındaki su ve sodyum kontrolsüzce içeri hücum eder, hücre içi ozmotik denge çöker ve mikrop patlayarak ölür.\n\nİnsan vücudunda MAC oluşumu özellikle ince hücre duvarına sahip **Neisseria (N. meningitidis ve N. gonorrhoeae)** bakterilerine karşı vazgeçilmezdir. Terminal kompleman bileşenleri (C5, C6, C7, C8 veya C9) eksik olan bireylerde tekrarlayan ölümcül meninkokoksik menenjit atakları görülür.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Terminal kompleman bileşenleri olan C5b-9 eksikliğinde özellikle Neisseria türü bakteriyel enfeksiyonlara yatkınlık belirgin şekilde artar.",
                "Neisseria",
                "MAC eksikliğinde tekrarlayan menenjit yapan bakteri cinsi"
            ),
            make_quiz(
                "Membran Atak Kompleksi (MAC) polimerizasyonunda hücre zarında 10 nm çapında silindirik poru oluşturan temel terminal polimer molekülü hangisidir?",
                [
                    {"key": "A", "text": "C9 proteini polimerleri (10-16 adet)", "explanation": "A seçeneği DOĞRUDUR: C9 molekülleri C5b-8 etrafında halka şeklinde polimerize olarak lüminal poru açar."},
                    {"key": "B", "text": "C1q alt birimleri", "explanation": "B seçeneği yanlıştır: Klasik yol başlangıç molekülüdür."},
                    {"key": "C", "text": "Faktör B parçacıkları", "explanation": "C seçeneği yanlıştır: Alternatif yol bileşenidir."},
                    {"key": "D", "text": "Bradikinin peptitleri", "explanation": "D seçeneği yanlıştır: Kinin sistemine aittir."},
                    {"key": "E", "text": "Fibrinojen polimerleri", "explanation": "E seçeneği yanlıştır: Fibrin pıhtısı oluşturur."}
                ],
                "A"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-12-s62",
        "title": "Kompleman Düzenleyici Proteinler: Konak Hücrelerini Koruma İlkeleri",
        "content": "Kompleman sistemi son derece yıkıcı, litik ve amplifiye olabilen bir proteolitik güçtür. Eğer kontrolsüz bırakılırsa kendi sağlıklı konak hücrelerimizi (eritrositler, endotel vb.) dakikalar içinde parçalayabilir. Bu nedenle organizmada sağlıklı hücreleri koruyan ve komplemanı frenleyen güçlü **düzenleyici proteinler (regülatörler)** evrimleşmiştir:\n\n1. **Plazma Düzenleyicileri:** Dolaşımda serbest gezen ve aşırı aktivasyonu durduran C1 İnhibitörü (C1-INH), Faktör H, Faktör I ve C4b-bağlayıcı proteindir (C4BP).\n2. **Membran Düzenleyicileri:** Yalnızca kendi konak hücrelerimizin zarına yerleşmiş olan DAF (Decay-Accelerating Factor / CD55), CD59 (Protectin / MIRL) ve MCP (CD46) proteinleridir.\n\nBakteriler ve mantarlar bu insan regülatör proteinlerini taşımazlar; bu sayede kompleman yabancı mikropları hızla yok ederken kendi sağlıklı dokularımıza dokunmaz.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Kompleman Düzenleyicilerinin Anatomik Ayrımı",
                "Çözünebilir Plazma Düzenleyicileri",
                "C1-INH, Faktör H ve Faktör I; dolaşımdaki spontan aktivasyonu ve sıvı faz kaskadını sınırlar.",
                "Hücre Membran Düzenleyicileri",
                "DAF (CD55) ve CD59; konak hücre zarında yerleşerek kendi hücrelerimizi kompleman lizisinden korur."
            ),
            make_recall(
                "Sağlıklı konak hücrelerinin yüzeyinde bulunarak kompleman saldırısını engelleyen regülatör proteinler hangi hücrelerde BULUNMAZ?",
                "Bakteriler, mantarlar ve yabancı mikrobiyal patojenlerde bulunmaz.",
                "Komplemanın hedef aldığı mikroorganizma yüzeyleri"
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-12-s63",
        "title": "C1 İnhibitörü (C1-INH) ve Kalıtsal Anjiyoödem (HAE)",
        "content": "C1 İnhibitörü (C1-INH), serpin (serin proteaz inhibitörü) ailesinden bir plazma proteinidir. Klasik kompleman yolundaki aktif C1r ve C1s proteazlarını kovalent olarak bağlayıp inaktive eder. Ancak C1-INH'nin tıbbi açıdan en kritik ikinci görevi, kallikrein-kinin sistemindeki **aktif plazma kallikreinini ve Faktör XIIa'yı inhibe etmektir**.\n\n- **Kalıtsal Anjiyoödem (Herediter Anjiyoödem / HAE):** SERPING1 genindeki mutasyon sonucu otozomal dominant kalıtılan **C1-INH eksikliği veya disfonksiyonudur**.\n- **Patofizyoloji:** C1-INH eksik olduğunda plazma kallikreini kontrolsüzce aktifleşir ve yüksek molekül ağırlıklı kininojenden masif miktarda **Bradikinin** üretir.\n- **Klinik Tablo:** Hastalarda ürtiker (kaşıntı ve kızarıklık) OLMAKSIZIN, yüzde, dudaklarda, larinkste ve bağırsak duvarında ani, tekrarlayan, derin anjiyoödem atakları gelişir. Larinks ödemi dakikalar içinde asfiksi ile boğulmaya; bağırsak ödemi ise akut batını taklit eden şiddetli karın kramplarına yol açar. Atakların primer suçlusu kompleman değil, **aşırı bradikinin birikimidir**.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kalıtsal Anjiyoödem (HAE) Patogenez Zinciri",
                [
                    "1. Genetik Defekt: SERPING1 mutasyonu ile C1-INH proteininin eksikliği",
                    "2. Kallikrein Freninin Kalkması: Plazma kallikreininin serbestçe kontrolsüz çalışması",
                    "3. Masif Bradikinin Üretimi: Kininojenden sürekli bradikinin salınması",
                    "4. Ağır Anjiyoödem: Kaşıntısız derin mukozal ödem, asfiksi ve bağırsak krampları"
                ]
            ),
            make_quiz(
                "Kalıtsal anjiyoödem (HAE) hastalarında tekrarlayan ve larinks ödemiyle hayatı tehdit eden anjiyoödem ataklarının doğrudan sorumlusu olan primer mediyatör hangisidir?",
                [
                    {"key": "A", "text": "Bradikinin", "explanation": "A seçeneği DOĞRUDUR: C1-INH eksikliğinde kallikrein kontrolsüz çalışarak masif bradikinin üretir; atakların nedeni histamin değil bradikinindir."},
                    {"key": "B", "text": "Histamin", "explanation": "B seçeneği yanlıştır: HAE histamin bağımlı değildir, bu yüzden antihistaminiklere yanıt vermez."},
                    {"key": "C", "text": "Lökotrien B4", "explanation": "C seçeneği yanlıştır: Nötrofil kemoatraktanıdır."},
                    {"key": "D", "text": "İnterferon-gama", "explanation": "D seçeneği yanlıştır: Makrofaj aktivatörüdür."},
                    {"key": "E", "text": "Tromboksan A2", "explanation": "E seçeneği yanlıştır: Trombosit agregasyonunu yönetir."}
                ],
                "A"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-12-s64",
        "title": "Membran Düzenleyicileri: DAF (CD55) ve CD59 (MIRL) Fonksiyonları",
        "content": "Sağlıklı konak hücre membranlarında kompleman aktivasyonunu durduran iki kilit yüzey glikoproteini bulunur:\n\n1. **DAF (Decay-Accelerating Factor / CD55):** C3 konvertaz enzim kompleksinin (C4b2a veya C3bBb) alt birimlerini birbirinden hızla ayrıştırarak (dissosiasyon) enzimi inaktive eder. Böylece konak hücresi üzerinde C3 parçalanmasını ve opsonizasyonu en baştan durdurur.\n2. **CD59 (Protectin / MIRL - Membrane Inhibitor of Reactive Lysis):** Montaj halindeki C5b-8 kompleksine bağlanır ve **C9 moleküllerinin polimerizasyonunu fiziksel olarak engeller**. Membranda delik (por) açılmasını durdurarak konak hücresini ozmotik lizisten korur.\n\nBu iki proteinin en kritik ortak biyokimyasal özelliği, hücre membranına doğrudan bir transmembran peptit ile değil, özel bir glikolipid çapa olan **GPI (Glikozilfosfatidilinositol)** çapası ile tutunmuş olmalarıdır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Membran Regülatörü", "Moleküler Görevi", "Membran Bağlantı Tipi"],
                [
                    [
                        {"text": "DAF (CD55)", "isMasked": False, "hint": ""},
                        {"text": "C3 konvertazı parçalayarak C3 bölünmesini engeller", "isMasked": True, "hint": "Konvertaz ayrıştırıcı faktör"},
                        {"text": "GPI (Glikozilfosfatidilinositol) çapası", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "CD59 (Protectin)", "isMasked": False, "hint": ""},
                        {"text": "C9 polimerizasyonunu engelleyerek MAC porunu durdurur", "isMasked": True, "hint": "Membran atak kompleksini frenleme"},
                        {"text": "GPI (Glikozilfosfatidilinositol) çapası", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Konak hücresi üzerinde C9 polimerizasyonunu engelleyerek Membran Atak Kompleksi oluşumunu durduran koruyucu protein CD59 dur.",
                "CD59 dur",
                "Protectin veya MIRL adıyla bilinen kompleman freni"
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-12-s65",
        "title": "DAF / CD59 Eksikliği: Paroksismal Noktürnal Hemoglobinüri (PNH)",
        "content": "Hematopoietik kök hücrelerde X kromozomu üzerinde yer alan **PIGA geninde** edinsel somatik bir mutasyon meydana geldiğinde, glikolipid **GPI çapası** sentezlenemez. GPI çapası üretilemediğinde, bu çapaya muhtaç olan **DAF (CD55) ve CD59** proteinleri kök hücreden türeyen eritrosit, lökosit ve trombositlerin zarına yerleşemez:\n\n- **Kompleman Duyarlılığı:** Yüzeyinde CD55 ve CD59 bulunmayan eritrositler, plazmadaki bazal kompleman aktivasyonuna karşı tamamen savunmasız kalır.\n- **İntravasküler Hemoliz:** Özellikle gece uykusunda hafif hipoventilasyon ve asidoz komplemanı aktive ettiğinde, eritrosit zarlarında kontrolsüz Membran Atak Kompleksleri (MAC) açılır ve alyuvarlar damar içinde patlar.\n- **Klinik Tablo:** Hastalar sabah ilk idrarlarının koyu kırmızı/kahverengi olması (**hemoglobinüri**), kronik hemolitik anemi ve trombosit yüzeyindeki kompleman aktivasyonuna bağlı derin ven trombozları (Budd-Chiari sendromu vb.) ile başvururlar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "32 yaşında kadın hasta, sabahları idrar renginin koyu çay rengi olması, kronik halsizlik, sarılık ve karaciğer ven trombozu (Budd-Chiari) ile başvuruyor. Yapılan akım sitometrisinde eritrosit ve granülosit yüzeyinde CD55 ve CD59 proteinlerinin bulunmadığı saptanıyor.",
                "Bu klinik tablonun (PNH) altta yatan temel moleküler patogenezi nedir?",
                [
                    {
                        "text": "PIGA gen mutasyonuna bağlı GPI çapa sentez defekti sonucu eritrositlerin CD55 ve CD59'dan yoksun kalarak kompleman aracılı intravasküler lizise uğramasıdır.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. PNH'de GPI çapası yokluğu nedeniyle CD55/CD59 yerleşemez ve kontrolsüz MAC lizisi gelişir."
                    },
                    {
                        "text": "Böbrek tübüllerinin idrara aşırı miktarda taze eritrosit dökmesidir.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Tablo glomerüler hematüri değil intravasküler hemolizdir."
                    },
                    {
                        "text": "Dalakta makrofajların aşırı demir biriktirerek patlamasıdır.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. PNH primer bir kompleman membran düzenleyici defektidir."
                    }
                ]
            ),
            make_recall(
                "Paroksismal noktürnal hemoglobinüride CD55 ve CD59'un hücre zarına bağlanamamasına yol açan gen mutasyonu hangisidir?",
                "PIGA gen mutasyonudur (fosfatidilinositol glikan sınıf A).",
                "GPI çapasını kodlayan X'e bağlı gen"
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-12-s66",
        "title": "Faktör H ve Faktör I: Alternatif Yol Regülasyonu ve Atipik HÜS",
        "content": "Alternatif kompleman yolunun sıvı fazdaki ve konak endotel yüzeyindeki en kritik koruyucusu **Faktör H ve Faktör I** ikilisidir:\n\n- **Faktör H:** Plazmada dolaşan glikoproteindir. Konak hücre yüzeyindeki sialik asit ve glikozaminoglikanları tanıyarak oradaki C3b moleküllerine bağlanır. Alternatif C3 konvertazdaki Bb parçasını uzaklaştırır (decay-accelerating) ve Faktör I proteazı için kofaktör görevi yapar.\n- **Faktör I:** Faktör H veya MCP yardımıyla aktif C3b'yi keserek inaktif **iC3b** haline getirir; böylece konvertaz kurulumunu kalıcı olarak söndürür.\n- **Atipik Hemolitik Üremik Sendrom (aHÜS):** Faktör H geninde konjenital mutasyon veya otoantikor varlığında renal mikrovasküler endotel kompleman ataklarına karşı korunamaz. Endotel hasarı yaygın mikroanjiyopatik trombosit tıkacına, mikroanjiyopatik hemolitik anemiye, trombositopeniye ve akut böbrek yetmezliğine yol açar. Benzer şekilde Faktör H polimorfizmleri yaşa bağlı maküler dejenerasyon (AMD) riskini artırır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Faktör H ve Faktör I İşbirliği",
                "Faktör H (Kofaktör ve Ayrıştırıcı)",
                "Konak sialik asitlerini tanır, C3 konvertazı dağıtır ve Faktör I'in kesim yapması için C3b'yi tutar.",
                "Faktör I (Serin Proteaz)",
                "Faktör H'nin sunduğu aktif C3b'yi proteolitik olarak keserek inaktif iC3b formuna dönüştürür."
            ),
            make_cloze(
                "Alternatif yol düzenleyicisi olan Faktör H mutasyonları renal endotel hasarı ve trombotik mikroanjiyopati ile giden atipik hemolitik üremik sendrom tablosuna yol açar.",
                "atipik hemolitik üremik sendrom",
                "aHÜS kısaltmasının tam Türkçe adı"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-12-s67",
        "title": "Kallikrein-Kinin Sistemi: Faktör XII Teması ve Prekallikrein",
        "content": "Kallikrein-kinin sistemi, enflamasyon ile pıhtılaşma sisteminin ortak moleküler köprüsünü kuran plazma kaynaklı bir kaskaddır. Tüm sistemin ateşleyicisi **Hageman Faktörüdür (Faktör XII)**:\n\n1. **Temas Aktivasyonu:** Damar hasarı sonucu kan plazması subendotelyal negatif yüklü yüzeylerle (kollajen, bazal membran veya bakteriyel LPS) temas ettiğinde inaktif Faktör XII hızla **aktif Faktör XIIa'ya** dönüşür.\n2. **Prekallikrein Dönüşümü:** Faktör XIIa, plazmada yüksek molekül ağırlıklı kininojen (HMWK) ile kompleks halinde dolaşan inaktif prekallikreini proteolitik olarak keserek aktif **Kallikrein** enzimine dönüştürür.\n3. **Pozitif Geri Bildirim:** Aktif kallikrein bir taraftan daha fazla Faktör XII'yi aktive ederek kaskadı büyütürken, diğer taraftan plazminojeni plazmine çevirerek kompleman C3'ü doğrudan parçalayabilir (çapraz aktivasyon).\n4. **Kinin Üretimi:** Aktif kallikrein kininojen substratını keserek nihai biyoaktif peptid olan **Bradikinini** serbest bırakır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Kallikrein-Kinin Aktivasyon Kaskadı",
                [
                    "1. Negatif Yüzey Teması: Endotel hasarı ve subendotelyal kollajen ile Faktör XII teması",
                    "2. XIIa Oluşumu: Hageman faktörünün proteolitik aktif forma geçmesi",
                    "3. Prekallikrein Kesimi: Faktör XIIa'nın prekallikreini aktif kallikreine çevirmesi",
                    "4. Bradikinin Salınımı: Kallikreinin kininojenden bradikinin peptitini koparması"
                ]
            ),
            make_recall(
                "Kallikrein-kinin sistemini ve pıhtılaşma kaskadını negatif yüklü yüzey temasıyla başlatan ortak faktör hangisidir?",
                "Faktör XII'dir (Hageman Faktörü).",
                "Temas aktivasyonunun anahtar koagülasyon faktörü"
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-12-s68",
        "title": "Bradikinin: Vasküler Geçirgenlik, Düz Kas ve Ağrı Mekanizması",
        "content": "Kallikrein tarafından yüksek molekül ağırlıklı kininojenden (HMWK) koparılan **Bradikinin**, 9 amino asitlik (nonapeptid) son derece güçlü bir doku mediyatörüdür. Hedef hücrelerde B2 kinin reseptörleri üzerinden şu kardinal etkileri sergiler:\n\n1. **Arterioler Vazodilatasyon:** Endotelden Nitrik Oksit ve Prostasiklin salınımını uyararak lokal arteriolleri şiddetle genişletir; kan basıncını düşürür.\n2. **Venüler Permeabilite Artışı:** Histamine benzer şekilde postkapiller venül endotelini büzüştürerek dokuya masif sıvı ve protein sızdırır (ödem oluşumu).\n3. **Düz Kas Kasılması:** Vasküler olmayan düz kasları (bronşlar ve bağırsak düz kasları) kasar; bronkospazm ve kramp tarzı karın ağrısı yapar.\n4. **Şiddetli Ağrı (Dolor):** Bradikinin enflamasyonda doğrudan **ağrı oluşturan en güçlü kimyasal mediyatördür**. C lifleri üzerindeki B2 reseptörlerine bağlanarak ağrı aksiyon potansiyelini ateşler; PGE2 ile birleştiğinde ağrı hissi katlanarak artar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Enflamasyon odağında nosiseptif duyusal sinir uçlarını doğrudan uyararak şiddetli ağrı oluşturan ve venüler geçirgenliği artıran dokuz amino asitlik plazma kaynaklı peptit hangisidir?",
                [
                    {"key": "A", "text": "Bradikinin", "explanation": "A seçeneği DOĞRUDUR: Bradikinin doğrudan ağrı üreten ve geçirgenliği artıran majör kinin peptitidir."},
                    {"key": "B", "text": "Serotonin", "explanation": "B seçeneği yanlıştır: Trombosit kaynaklı vazokonstriktördür."},
                    {"key": "C", "text": "Faktör VIII", "explanation": "C seçeneği yanlıştır: Hemofili A faktörüdür."},
                    {"key": "D", "text": "İnterlökin-10", "explanation": "D seçeneği yanlıştır: Anti-inflamatuardır."},
                    {"key": "E", "text": "Lipoksin B4", "explanation": "E seçeneği yanlıştır: Enflamasyonu yatıştırır."}
                ],
                "A"
            ),
            make_cloze(
                "Enflamasyon sahasında nosiseptörleri uyararak doğrudan ağrı oluşturan kinin ailesi üyesi bradikinindir.",
                "bradikinindir",
                "9 amino asitli majör ağrı oluşturan peptit"
            )
        ]
    })

    # Slide 69 (CHECKPOINT 7)
    slides.append({
        "id": "k1-12-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Kompleman Düzenleyicileri, Genetik Hastalıklar ve Kinin Sistemi",
        "content": "Kompleman regülasyonu, ilişkili patolojiler ve kinin sisteminin temel sentezi:\n\n1. **Membran Atak Kompleksi (MAC):** C5b-9 polimeridir; zarda 10 nm por açarak ozmotik lizis yapar. Eksikliğinde **Neisseria** enfeksiyonları tavan yapar.\n2. **C1-INH:** C1r/C1s ve kallikreini baskılar. Eksikliği **Kalıtsal Anjiyoödem (HAE)** tablosudur; aşırı bradikinin üretimiyle kaşıntısız derin ödem ve larinks asfiksisine yol açar.\n3. **DAF (CD55) ve CD59:** GPI çapasıyla zara tutunur; CD55 konvertazı dağıtır, CD59 MAC porunu engeller. PIGA mutasyonuyla GPI çapası kaybolursa **PNH (Paroksismal Noktürnal Hemoglobinüri)** ve intravasküler hemoliz gelişir.\n4. **Faktör H / I:** Alternatif yolu kapatır; Faktör H mutasyonu **atipik HÜS'e** yol açar.\n5. **Kallikrein-Kinin:** Faktör XII temasıyla başlar; kallikrein kininojenden **Bradikinin** koparır.\n6. **Bradikinin:** Vazodilatasyon, venül geçirgenliği ve doğrudan nosiseptif **ağrı** oluşturur.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Genetik / Edinilmiş Defekt", "Eksik Olan Molekül", "Klinik Tablo"],
                [
                    [
                        {"text": "Kalıtsal Anjiyoödem (HAE)", "isMasked": False, "hint": ""},
                        {"text": "C1 İnhibitörü (C1-INH)", "isMasked": True, "hint": "Kallikrein ve C1 kontrolörü"},
                        {"text": "Bradikinin aracılı tekrarlayan larinks ve doku ödemi", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Paroksismal Noktürnal Hemoglobinüri", "isMasked": False, "hint": ""},
                        {"text": "GPI çapası (CD55 ve CD59 yokluğu)", "isMasked": True, "hint": "Membran kompleman kalkanı kaybı"},
                        {"text": "Kompleman aracılı intravasküler hemoliz ve tromboz", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Tekrarlayan Neisseria Enfeksiyonu", "isMasked": False, "hint": ""},
                        {"text": "C5, C6, C7, C8 veya C9 (Terminal yol)", "isMasked": True, "hint": "Membranda por açan bileşenler"},
                        {"text": "Meningokoksik menenjit atakları", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_recall(
                "Kalıtsal anjiyoödemde aşırı bradikinin üretimini engelleyemeyen ve HAE hastalığına yol açan eksik plazma proteini nedir?",
                "C1 İnhibitörüdür (C1-INH).",
                "Serpin ailesi klasik yol ve kallikrein regülatörü"
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-12-s70",
        "title": "Bradikinin Yıkımı: Anjiyotensin Dönüştürücü Enzim (ACE / Kininaz II)",
        "content": "Bradikinin dokularda çok güçlü etkiler ürettiği için ömrü saniyelerle sınırlıdır; dolaşımdaki özelleşmiş kininaz enzimleri tarafından süratle parçalanır. Bu yıkımı gerçekleştiren en önemli enzim akciğer vasküler endotelinde yüksek konsantrasyonda bulunan **Kininaz II'dir; bu enzim kardiyolojideki Anjiyotensin Dönüştürücü Enzim (ACE) ile birebir aynı moleküldür**.\n\n- **ACE'nin İkili Rolü:** ACE bir taraftan Anjiyotensin I'i vazokonstriktör Anjiyotensin II'ye çevirirken, diğer taraftan vazodilatatör Bradikinini inaktif peptidlere parçalayarak yok eder.\n- **ACE İnhibitörleri ve Klinik Yan Etki:** Hipertansiyon veya kalp yetmezliği için hastaya ACE İnhibitörü (ramipril, enalapril vb.) verildiğinde, bradikinin yıkılamaz ve hava yollarında birikir. Akciğerlerde biriken aşırı bradikinin ve madde P, sensoryal C liflerini uyararak hastaların yaklaşık %10-20'sinde medikal tedaviye dirençli **inatçı kuru öksürüğe** ve nadiren ölümcül **anjiyoödeme** yol açar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "62 yaşında hipertansiyon tanılı hasta, ramipril (ACE inhibitörü) başlandıktan 3 hafta sonra başlayan, balgamsız, boğazda gıcıklanma tarzında inatçı kuru öksürük yakınmasıyla başvuruyor. Akciğer grafisi tamamen normaldir.",
                "Bu öksürük yan etkisinin altında yatan temel kimyasal mediyatör birikimi hangisidir?",
                [
                    {
                        "text": "ACE enziminin (Kininaz II) bloke edilmesi sonucu akciğer dokusunda bradikinin ve nöropeptitlerin parçalanamayıp birikmesidir.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. ACE aynı zamanda Kininaz II'dir; inhibisyonu bradikinin birikimine ve inatçı öksürüğe yol açar."
                    },
                    {
                        "text": "Histamin H2 reseptörlerinin aşırı uyarılmasıyla akciğerde asit birikmesidir.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. ACE inhibitörü öksürüğü histaminle ilişkili değildir."
                    },
                    {
                        "text": "Akciğerlere yerleşen tüberküloz basilinin oluşturduğu kavitasyondur.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. İlaç yan etkisidir, grafi normaldir ve ACEİ kesilince düzelir."
                    }
                ]
            ),
            make_cloze(
                "Bradikinini inaktif peptidlere parçalayan Kininaz II enzimi pulmoner vasküler yataktaki anjiyotensin dönüştürücü enzim ile aynıdır.",
                "anjiyotensin dönüştürücü enzim",
                "ACE kısaltmasının açılımı olan kardiyovasküler enzim"
            )
        ]
    })

    return slides
