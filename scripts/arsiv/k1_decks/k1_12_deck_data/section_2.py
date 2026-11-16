# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_2_slides():
    slides = []

    # Slide 11
    slides.append({
        "id": "k1-12-s11",
        "title": "Araşidonik Asit Metabolizması ve Eikozanoidlerin Biyokimyasal Kökeni",
        "content": "Akut ve kronik enflamasyonda vasküler tonusu, lökosit trafiğini, trombosit fonksiyonlarını ve ağrı-ateş iletimini yöneten en kapsamlı mediyatör ailesi **eikozanoidlerdir** (Yunanca eikosi = yirmi kelimesinden türemiştir). Tüm eikozanoidlerin ortak biyokimyasal prekürsörü, hücre membranındaki fosfolipidlerin sn-2 pozisyonunda esterleşmiş olarak bulunan **20 karbonlu çoklu doymamış bir yağ asidi olan Araşidonik Asittir (AA)** (5,8,11,14-eikozatetraenoik asit). Hücre istirahat halindeyken serbest araşidonik asit düzeyi neredeyse sıfırdır; yağ asidi membran lipid havuzunda hapsedilmiştir. Enflamatuar bir uyarı (mekanik stres, kimyasal travma, antijen teması veya kompleman aktivasyonu) geldiğinde hücresel kalsiyum artışı özelleşmiş fosfolipaz enzimlerini tetikler ve araşidonik asit membran çift katmanından serbestleşerek metabolik dönüşüm yolaklarına girer.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Eikozanoidlerin ana biyokimyasal öncülü hücre zarı fosfolipidlerinden serbestleşen yirmi karbonlu araşidonik asittir.",
                "araşidonik asittir",
                "Eikozanoid sentezinin 20 karbonlu yağ asidi kaynağı"
            ),
            make_quiz(
                "Eikozanoid ailesi mediyatörlerinin (prostaglandinler, lökotrienler, lipoksinler) ortak biyokimyasal öncülü olan araşidonik asit kaç karbonlu bir yağ asididir?",
                [
                    {"key": "A", "text": "20 karbonlu", "explanation": "A seçeneği DOĞRUDUR: Eikozanoid ismi 'eikosi' (yirmi) kelimesinden gelir ve araşidonik asit 20 karbonlu çoklu doymamış bir yağ asididir."},
                    {"key": "B", "text": "6 karbonlu", "explanation": "B seçeneği yanlıştır: Bu glukoz gibi heksozların karbon sayısıdır."},
                    {"key": "C", "text": "12 karbonlu", "explanation": "C seçeneği yanlıştır: Orta zincirli yağ asididir."},
                    {"key": "D", "text": "30 karbonlu", "explanation": "D seçeneği yanlıştır: Skualen veya kolesterol prekürsörüdür."},
                    {"key": "E", "text": "2 karbonlu", "explanation": "E seçeneği yanlıştır: Asetattır."}
                ],
                "A"
            )
        ]
    })

    # Slide 12
    slides.append({
        "id": "k1-12-s12",
        "title": "Fosfolipaz A2 (PLA2) Enziminin Rolü ve Aktivasyonu",
        "content": "Eikozanoid biyosentezinde tüm sürecin hız kısıtlayıcı ve ilk basamağını yöneten enzim **Fosfolipaz A2'dir (PLA2)**. PLA2, hücre membranındaki fosfatidilkolin ve fosfatidiletanolamin gibi fosfolipidlerin sn-2 açil bağını hidrolize ederek araşidonik asidi serbest bırakır. Enzimin aktivasyonu intraselüler kalsiyum artışı ve mitojenle aktive olan protein kinaz (MAPK) kaskadı tarafından tetiklenir. Çeşitli fiziksel uyarılar, C5a anafilatoksini, bradikinin, trombin ve fagositoz sinyalleri PLA2'yi uyarır. Serbest kalan araşidonik asit saniyeler içinde iki ana enzimatik otoyoldan birine girer:\n\n1. **Siklooksijenaz (COX) Yolağı:** Prostaglandinler ve Tromboksan üretir.\n2. **Lipoksijenaz (LOX) Yolağı:** Lökotrienler ve Lipoksinler üretir.\n\nKortikosteroid ilaçlar lipokortin/anneksin proteinlerini indükleyerek doğrudan PLA2'yi bloke eder ve böylece eikozanoid üretimini en tepeden keserler.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Eikozanoid Sentezinin Başlangıç Zinciri",
                [
                    "1. Membran Uyarısı: Kimyasal, mekanik veya immünolojik stresin hücreye çarpması",
                    "2. Kalsiyum Girişi: Sitoplazmik serbest kalsiyum iyonlarının tepe yapması",
                    "3. PLA2 Aktivasyonu: Fosfolipaz A2 enziminin membran fosfolipidlerini hidroliz etmesi",
                    "4. Araşidonik Asit Salınımı: Serbest yağ asidinin COX ve LOX enzimlerine sunulması"
                ]
            ),
            make_recall(
                "Membran fosfolipidlerinden araşidonik asidi serbestleştiren ve kortikosteroidler tarafından en tepeden inhibe edilen enzim hangisidir?",
                "Fosfolipaz A2'dir (PLA2).",
                "Eikozanoid yolunun ilk hız kısıtlayıcı lipaz enzimi"
            )
        ]
    })

    # Slide 13
    slides.append({
        "id": "k1-12-s13",
        "title": "Siklooksijenaz (COX) Yolağı ve PGG2 / PGH2 Ara Ürünleri",
        "content": "Serbestleşen araşidonik asit endoplazmik retikulum ve nükleer zar üzerinde yer alan **Siklooksijenaz (Prostaglandin Endoperoksit Sentaz)** enzimi ile reaksiyona girer. Siklooksijenaz bifonksiyonel bir enzimdir; yapısında hem bir siklooksijenaz hem de bir peroksidaz aktif bölgesi barındırır. İki basamaklı enzimatik reaksiyonda:\n\n1. Araşidonik aside iki molekül moleküler oksijen (O2) eklenerek siklik bir endoperoksit köprüsü kurulur ve kararsız **Prostaglandin G2 (PGG2)** sentezlenir.\n2. Ardından enzimin peroksidaz aktivitesi PGG2'yi indirgeyerek **Prostaglandin H2'ye (PGH2)** dönüştürür.\n\nPGH2 tüm prostaglandin serisinin ortak anahtar kavşak molekülüdür. Dokularda bulunan hücreye özgü izomeraz ve sentaz enzimleri PGH2'yi substrat olarak kullanarak son ürünleri üretir: Mast hücrelerinde PGD2, endotelde PGI2, trombositlerde TXA2, fibroblast ve makrofajlarda PGE2 sentezlenir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Basamak", "Enzimatik Aktivite", "Oluşan Ara Ürün"],
                [
                    [
                        {"text": "1. Oksijenasyon", "isMasked": False, "hint": ""},
                        {"text": "İki molekül O2 eklenmesi ve halkalaşma", "isMasked": True, "hint": "Siklooksijenaz aktif bölgesi reaksiyonu"},
                        {"text": "Prostaglandin G2 (PGG2)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "2. Peroksidasyon", "isMasked": False, "hint": ""},
                        {"text": "Endoperoksitin hidroksiye indirgenmesi", "isMasked": True, "hint": "Enzimin peroksidaz cebindeki reaksiyon"},
                        {"text": "Prostaglandin H2 (PGH2)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "3. Doku Dağılımı", "isMasked": False, "hint": ""},
                        {"text": "Özgül doku sentazlarının devreye girmesi", "isMasked": True, "hint": "Hücre tipine göre son ürün sentezi"},
                        {"text": "PGE2, PGD2, PGI2, TXA2", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Siklooksijenaz yolağında tüm prostaglandin ve tromboksanların sentezlendiği ortak kararsız anahtar ara ürün prostaglandin H ikidir.",
                "prostaglandin H ikidir",
                "PGH2 ara bileşiğinin tam açılımı"
            )
        ]
    })

    # Slide 14
    slides.append({
        "id": "k1-12-s14",
        "title": "COX-1 ve COX-2 İzoenzimlerinin Moleküler ve Fonksiyonel Ayrımı",
        "content": "Siklooksijenaz enziminin organizmada iki farklı gen tarafından kodlanan iki majör izoformu bulunur ve aralarındaki fark farmakolojinin en temel taşıdır:\n\n- **COX-1 (Konstitütif İzoform):** Vücuttaki dokuların çoğunda (özellikle mide mukozası, böbrekler, trombositler ve vasküler endotel) bazal olarak sürekli eksprese edilir. Görevi normal homeostatik fizyolojik dengeleri korumaktır: Mide mukozasında koruyucu bikarbonat ve mukus salgısını sürdürür, renal kan akımını ve medüller perfüzyonu regüle eder, trombosit hemostazını sağlar.\n- **COX-2 (İndüklenebilir İzoform):** Normal istirahat dokularında ya hiç yoktur ya da çok düşük düzeydedir (böbrek ve santral sinir sistemi hariç). İnflamatuar sitokinler (özellikle **IL-1 ve TNF**), büyüme faktörleri ve endotoksinler (LPS) tarafından inflamasyon sahasında gen transkripsiyonu ile **hızla indüklenir**. Enflamatuar ağrı, ateş ve eksüdanın ana mimarıdır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "COX İzoenzimleri Karşılaştırması",
                "COX-1 (Konstitütif)",
                "Doku homeostazı, mide mukoza koruması, renal perfüzyon ve trombosit agregasyonunda süreklidir.",
                "COX-2 (İndüklenebilir)",
                "İnflamatuar sitokinler ve LPS ile uyarılır; enflamasyon, ağrı ve ateş yanıtından sorumludur."
            ),
            make_quiz(
                "Normal sağlıklı dokularda homeostatik fonksiyonları (mide mukozası koruması, renal kan akımı) sürdürmek için konstitütif (sürekli) olarak eksprese edilen siklooksijenaz izoformu hangisidir?",
                [
                    {"key": "A", "text": "COX-1", "explanation": "A seçeneği DOĞRUDUR: COX-1 konstitütiftir, homeostazı korur; COX-2 ise inflamasyonla indüklenir."},
                    {"key": "B", "text": "COX-2", "explanation": "B seçeneği yanlıştır: COX-2 esas olarak inflamatuar uyarıyla indüklenen izoformdur."},
                    {"key": "C", "text": "5-Lipoksijenaz", "explanation": "C seçeneği yanlıştır: Lökotrien sentez enzimidir."},
                    {"key": "D", "text": "Fosfolipaz C", "explanation": "D seçeneği yanlıştır: İnozitol fosfat yolak enzimidir."},
                    {"key": "E", "text": "Tromboksan sentaz", "explanation": "E seçeneği yanlıştır: Yalnız trombositlerde son basamak enzimidir."}
                ],
                "A"
            )
        ]
    })

    # Slide 15
    slides.append({
        "id": "k1-12-s15",
        "title": "Prostaglandin D2 (PGD2): Mast Hücresi ve Alerjik Enflamasyon",
        "content": "Prostaglandin D2 (PGD2), eikozanoid ailesi içinde **başlıca mast hücreleri** tarafından yüksek miktarlarda üretilen temel prostaglandin türüdür. Mast hücresindeki hematopoietik PGD sentaz (H-PGDS) enzimi PGH2'yi hızla PGD2'ye çevirir. PGD2'nin temel biyolojik etkileri:\n\n1. **Vasküler Etkiler:** Güçlü bir arterioler vazodilatatördür ve postkapiller venüllerde vasküler permeabilite artışına (ödem oluşumuna) belirgin katkı sağlar.\n2. **Lökosit Kemotaksisi:** DP2 (CRTH2) reseptörleri üzerinden eozinofiller, bazofiller ve Th2 yardımcı T lenfositleri için güçlü bir kemoatraktandır; onları enflamasyon bölgesine toplar.\n3. **Solunum Sistemi:** Akciğer düz kaslarında bronkokonstriksiyona neden olarak astım ataklarının patogenezinde rol oynar.\n\nBu özellikleriyle PGD2, alerjik astım, alerjik rinit ve ürtiker gibi Tip I aşırı duyarlılık tablolarında mast hücresi degranülasyonunu takip eden ikinci vasküler dalganın lideridir.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_cloze(
                "Eikozanoidler içinde baslıca mast hücreleri tarafından üretilen ve alerjik yanıtta rol oynayan prostaglandin PGD ikidir.",
                "PGD ikidir",
                "Mast hücresine özgü temel prostaglandin türü"
            ),
            make_recall(
                "Mast hücreleri kaynaklı PGD2'nin vasküler sistem ve bronşlar üzerindeki iki temel etkisi nedir?",
                "Vazodilatasyon (permeabilite artışı) ve bronkokonstriksiyondur.",
                "Damarları genişletici, bronşları daraltıcı iki kardinal etki"
            )
        ]
    })

    # Slide 16
    slides.append({
        "id": "k1-12-s16",
        "title": "Prostaglandin E2 (PGE2): Ateş, Ağrı Sensitizasyonu ve Vazodilatasyon",
        "content": "Prostaglandin E2 (PGE2), klinik tıpta enflamasyonun sistemik ve lokal kardinal bulgularından en yaygın sorumlu olan eikozanoiddir. Doku makrofajları, vasküler endotel ve fibroblastlar tarafından yoğun şekilde sentezlenir. Dört farklı EP reseptörü (EP1-EP4) üzerinden şu üç kritik fizyopatolojik işlevi yönetir:\n\n1. **Hipotalamik Ateş (Pirojenik Etki):** Dolaşımdaki ekzojen pirojenler (LPS) veya endojen sitokinler (IL-1, TNF), hipotalamus preoptik alanındaki endotel hücrelerinde COX-2 ve mikrozomal PGE sentaz-1'i uyarır. Sentezlenen **PGE2**, termosensitif nöronları uyararak vücut sıcaklık ayar noktasını (set-point) yukarı çeker ve **ateş** tablosunu başlatır.\n2. **Ağrı Sensitizasyonu (Hiperaljezi):** PGE2 nosiseptif C lifleri ve A-delta sinir uçlarındaki iyon kanallarını fosforilleyerek ağrı eşiğini düşürür (sensitizasyon). Tek başına hafif ağrı yapsa da, bradikinin ve histaminin ağrı yapıcı gücünü kat kat artırır.\n3. **Lokal Vazodilatasyon:** Mikrodolaşımda arteriolleri genişleterek lokal kan akımını (kızarıklık ve sıcaklık) artırır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["PGE2 Etki Alanı", "Moleküler Hedef ve Mekanizma", "Klinik Yansıma"],
                [
                    [
                        {"text": "Hipotalamus", "isMasked": False, "hint": ""},
                        {"text": "Preoptik alanda termostat ayar noktasını yükseltme", "isMasked": True, "hint": "Sistemik ateş mekanizması"},
                        {"text": "Sistemik ateş (febris)", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Duyusal Sinir Uçları", "isMasked": False, "hint": ""},
                        {"text": "Nosiseptörlerde ağrı eşiğini düşürme (hiperaljezi)", "isMasked": True, "hint": "Bradikininle sinerjik ağrı hassasiyeti"},
                        {"text": "Ağrı duyarlılığı ve zonklama", "isMasked": False, "hint": ""}
                    ],
                    [
                        {"text": "Mikrovasküler Arteriol", "isMasked": False, "hint": ""},
                        {"text": "Vasküler düz kas gevşemesi ve perfüzyon artışı", "isMasked": True, "hint": "Arteriol çapının genişlemesi"},
                        {"text": "Lokal kızarıklık ve sıcaklık (eritem)", "isMasked": False, "hint": ""}
                    ]
                ]
            ),
            make_cloze(
                "Enflamasyonda hipotalamusta vücut ısı ayar noktasını yükselterek ateşe yol açan primer eikozanoid prostaglandin E ikidir.",
                "prostaglandin E ikidir",
                "Ateş ve ağrı duyarlılığının ana prostaglandini"
            )
        ]
    })

    # Slide 17
    slides.append({
        "id": "k1-12-s17",
        "title": "Prostasiklin (PGI2): Endotel Kaynağı ve Antitrombosit Etki",
        "content": "Prostasiklin (PGI2), başlıca **vasküler endotel hücreleri** tarafından PGI sentaz enzimi aracılığıyla üretilen son derece güçlü bir homeostatik ve enflamatuar koruyucudur. Endotelyal PGI2 trombositler ve damar düz kası üzerinde bulunan IP reseptörlerine bağlanır ve adenilat siklazı uyararak hücre içi cAMP düzeylerini yükseltir. Bunun sonucunda iki majör fizyolojik eylem gerçekleştirir:\n\n1. **Güçlü Vazodilatasyon:** Vasküler düz kası gevşeterek kan basıncını düşürür ve doku perfüzyonunu korur.\n2. **Trombosit Agregasyonunun Güçlü İnhibisyonu:** Trombosit içi cAMP artışı kalsiyum salınımını baskılar; trombositlerin aktive olmasını, yüzeye yapışmasını ve kümeleşmesini engeller. Bu sayede damar içi pıhtılaşmayı (tromboz) önleyen en kritik endojen antikoagülan kalkandır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Prostasiklin ve Tromboksan Görev Ayrımı",
                "Prostasiklin (PGI2 - Endotel)",
                "Güçlü vazodilatasyon yapar, trombosit agregasyonunu şiddetle inhibe eder (antitrombotik).",
                "Tromboksan A2 (TXA2 - Trombosit)",
                "Güçlü vazokonstriksiyon yapar, trombosit agregasyonunu kuvvetle uyarır (protrombotik)."
            ),
            make_recall(
                "Vasküler endotelden salınarak vazodilatasyon yapan ve trombosit agregasyonunu güçlü şekilde inhibe eden eikozanoid hangisidir?",
                "Prostasiklindir (PGI2).",
                "Endotelin temel antitrombotik koruyucu prostaglandini"
            )
        ]
    })

    # Slide 18
    slides.append({
        "id": "k1-12-s18",
        "title": "Tromboksan A2 (TXA2): Trombosit Kaynağı ve Protrombotik Rol",
        "content": "Prostasiklinin fizyolojik zıttı ve dengi olan molekül **Tromboksan A2'dir (TXA2)**. TXA2 başlıca **trombositler (kan pulcukları)** tarafından Tromboksan Sentaz enzimi aracılığıyla üretilir. Trombositler çekirdeksiz hücreler oldukları için yeni enzim sentezleyemezler ve sitoplazmalarında yalnızca konstitütif **COX-1** enzimini taşırlar. Doku hasarı veya endotel yırtılması olduğunda trombositler subendotelyal kollajene yapışır, aktive olur ve masif miktarda TXA2 salgılarlar. TXA2 hedef hücrelerdeki TP reseptörlerine bağlanarak fosfolipaz C'yi aktive eder ve hücre içi serbest kalsiyumu fırlatır:\n\n- **Güçlü Trombosit Agregasyonu:** Komşu trombositleri hızla rekrüte ederek birbirine bağlar ve primer hemostatik trombosit tıkacını oluşturur.\n- **Güçlü Vazokonstriksiyon:** Hasarlı damarın lümenini büzerek kanamayı durdurmaya çalışır.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "TXA2 Aracılı Trombosit Tıkacı Oluşumu",
                [
                    "1. Endotel Hasarı: Subendotelyal matrikse temas eden trombositlerin uyarılması",
                    "2. COX-1 Aktivasyonu: Trombosit içinde serbest AA'dan hızla PGH2 ve TXA2 üretimi",
                    "3. TP Reseptör Uyarımı: TXA2'nin parakrin/otokrin etkiyle hücre içi kalsiyumu artırması",
                    "4. Agregasyon ve Vazokonstriksiyon: Trombositlerin kümeleşmesi ve damarın büzüşmesi"
                ]
            ),
            make_quiz(
                "Trombositlerden salınarak güçlü trombosit agregasyonu ve lokal vazokonstriksiyona neden olan temel eikozanoid hangisidir?",
                [
                    {"key": "A", "text": "Tromboksan A2 (TXA2)", "explanation": "A seçeneği DOĞRUDUR: TXA2 trombosit kaynaklıdır; agregasyon ve vazokonstriksiyon yapar."},
                    {"key": "B", "text": "Prostasiklin (PGI2)", "explanation": "B seçeneği yanlıştır: PGI2 tam tersine agregasyonu engeller ve damarı genişletir."},
                    {"key": "C", "text": "Lökotrien B4 (LTB4)", "explanation": "C seçeneği yanlıştır: Nötrofil kemoatraktanıdır."},
                    {"key": "D", "text": "Bradikinin", "explanation": "D seçeneği yanlıştır: Plazma kaynaklı kinindir."},
                    {"key": "E", "text": "Lipoksin A4", "explanation": "E seçeneği yanlıştır: Anti-inflamatuardır."}
                ],
                "A"
            )
        ]
    })

    # Slide 19 (CHECKPOINT 2)
    slides.append({
        "id": "k1-12-s19",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Siklooksijenaz Yolağı, Prostaglandinler ve Tromboksan",
        "content": "Araşidonik asit ve siklooksijenaz metabolizmasının kilit ilkeleri:\n\n1. **Prekürsör:** 20 karbonlu araşidonik asit (AA), PLA2 enzimiyle membran fosfolipidlerinden serbestleşir; kortikosteroidler PLA2'yi en tepeden bloke eder.\n2. **COX İzoenzimleri:** COX-1 konstitütiftir (mide, böbrek, trombosit homeostazı); COX-2 ise sitokinlerle (IL-1, TNF) indüklenen enflamatuar enzimdir.\n3. **Ortak Ara Ürün:** Tüm prostaglandin ve tromboksanlar kararsız PGG2/PGH2 üzerinden sentezlenir.\n4. **PGD2:** Mast hücresi ürünüdür; vazodilatasyon ve bronkokonstriksiyon yapar.\n5. **PGE2:** Ateş (hipotalamusta set-point yükselmesi), ağrı eşiği düşmesi (sensitizasyon) ve vazodilatasyon yapar.\n6. **PGI2 vs TXA2:** Endotelyal PGI2 vazodilatasyon + agregasyon inhibisyonu yaparken; trombosit kaynaklı TXA2 vazokonstriksiyon + agregasyon uyarımı yapar.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_quiz(
                "Siklooksijenaz yolağı ürünleri ve hücresel kaynaklarıyla ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                [
                    {"key": "A", "text": "PGD2: Başlıca mast hücreleri tarafından üretilir.", "explanation": "A seçeneği doğrudur: Alerjik yanıtta mast hücresi majör üreticisidir."},
                    {"key": "B", "text": "PGE2: Hipotalamusta vücut ısısını yükselterek ateşe yol açar.", "explanation": "B seçeneği doğrudur: Pirojenik ateşi yönetir."},
                    {"key": "C", "text": "PGI2: Trombositler tarafından sentezlenerek damarları büzer.", "explanation": "C seçeneği YANLIŞTIR: PGI2 endotel tarafından üretilir, damarları genişletir ve agregasyonu engeller; trombositler TXA2 üretir."},
                    {"key": "D", "text": "TXA2: Trombositler tarafından üretilerek agregasyonu uyarır.", "explanation": "D seçeneği doğrudur: Protrombotiktir."},
                    {"key": "E", "text": "COX-1: Mide mukozasında koruyucu bariyeri sürdüren konstitütif enzimdir.", "explanation": "E seçeneği doğrudur: Fizyolojik homeostazı sağlar."}
                ],
                "C"
            ),
            make_cloze(
                "Endotelden salınan PGI2 ile trombositten salınan TXA2 arasındaki hassas denge vasküler tromboz gelişimini engeller.",
                "TXA2 arasındaki",
                "Prostasiklinin karşıtı olan trombosit kaynaklı protrombotik molekül"
            )
        ]
    })

    # Slide 20
    slides.append({
        "id": "k1-12-s20",
        "title": "TXA2 / PGI2 Homeostatik Dengesi ve Vasküler Tromboz Patogenezi",
        "content": "Sağlıklı bir kardiyovasküler sistemde endotel kaynaklı **Prostasiklin (PGI2)** ile trombosit kaynaklı **Tromboksan A2 (TXA2)** dinamik bir denge (homeostaz) içindedir. Normalde sağlam endotelin ürettiği PGI2 üstün gelerek trombositlerin damar duvarına yapışmasını önler ve kanın akışkanlığını korur. Ancak endotel hasar gördüğünde (ateroskleroz, sigara, hipertansiyon veya seçici COX-2 inhibitörü kullanımı) bu denge TXA2 lehine bozulur. Trombosit agregasyonu tetiklenir, vazokonstriksiyon gelişir ve lümende tıkayıcı arteriyel trombüs (miyokard enfarktüsü veya inme) meydana gelir.\n\n> [!CRITICAL]\n> Düşük doz aspirin (75-100 mg), çekirdeksiz trombositlerdeki COX-1'i geri dönüşümsüz olarak asetilleyip TXA2 üretimini ömür boyu (7-10 gün) sıfırlarken; çekirdekli endotel hücreleri yeni COX enzimi üreterek PGI2 sentezini sürdürebilir. Bu sayede düşük doz aspirin kanı sulandırır ve kalp krizini önler.",
        "sourcePdf": "Kurul 1 - Ders 12: Enflamasyonun Kimyasal Mediyatörleri (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_branching(
                "Koroner arter hastalığı olan bir hastaya miyokard enfarktüsünü önlemek amacıyla günde 100 mg düşük doz aspirin başlanıyor. Laboratuvarda hastanın kanama zamanının uzadığı ve trombosit agregasyonunun baskılandığı gösteriliyor.",
                "Düşük doz aspirinin bu koruyucu antitrombotik etkisinin moleküler temeli nedir?",
                [
                    {
                        "text": "Trombositlerdeki COX-1'i geri dönüşümsüz asetilleyerek TXA2 sentezini durdurur; çekirdekli endotel ise yeni COX üreterek antitrombotik PGI2 sentezini korur.",
                        "isCorrect": True,
                        "feedback": "Doğrudur. Trombosit çekirdeksiz olduğundan yeni enzim yapamaz ve TXA2 sıfırlanır; endotel ise PGI2 üretmeye devam eder."
                    },
                    {
                        "text": "Karaciğerdeki tüm pıhtılaşma faktörlerinin genetik transkripsiyonunu tamamen siler.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. Aspirin karaciğer protein sentezini silmez; siklooksijenaz asetilasyonu yapar."
                    },
                    {
                        "text": "Lökotrien B4 sentezini 1000 kat artırarak pıhtıyı eritir.",
                        "isCorrect": False,
                        "feedback": "Yanlıştır. LTB4 nötrofil kemoatraktanıdır, pıhtı eritme görevi yoktur."
                    }
                ]
            ),
            make_recall(
                "Düşük doz aspirinin trombositlerde TXA2 üretimini trombositin tüm ömrü boyunca (7-10 gün) durdurmasının hücresel nedeni nedir?",
                "Trombositlerin çekirdeksiz olması ve yeni enzim sentezleyememesidir.",
                "Kan pulcuklarının organel ve nükleus eksikliği özelliği"
            )
        ]
    })

    return slides
