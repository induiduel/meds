#!/usr/bin/env python3
"""Comprehensive Enrichment Elements Generator for k1-07 Deck (Hücre İçi Birikimler ve Kalsifikasyonlar)"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.k1_07_deck_data.helpers import (
    make_micro_quiz, make_branching_logic, make_causal_chain,
    make_before_after, make_table
)

def get_15_quizzes():
    return {
        7: make_micro_quiz(
            "Lizozomal enzim eksikliği sonucu glukoserebrozid birikimiyle seyreden ve 'buruşuk sigara kağıdı' sitoplazmalı makrofajlarla tanınan hastalık hangisidir?",
            {"A": "Tay-Sachs", "B": "Niemann-Pick", "C": "Gaucher Hastalığı", "D": "von Gierke", "E": "Pompe"},
            "C",
            {
                "A": "Tay-Sachs hastalığında GM2 gangliozid birikir ve makulada kiraz kırmızısı benek görülür.",
                "B": "Niemann-Pick sfingomiyelinaz eksikliğidir ve köpüksü sitoplazma yapar.",
                "C": "Doğru cevap C'dir: Glukoserebrozidaz eksikliğinde Gaucher hücreleri 'buruşuk sigara kağıdı' görünümü alır.",
                "D": "von Gierke glikoz-6-fosfataz eksikliğidir.",
                "E": "Pompe asit maltaz eksikliğidir."
            }
        ),
        15: make_micro_quiz(
            "Alkol dehidrogenaz ve aldehit dehidrogenaz reaksiyonları sırasında sitozolde biriken hangi metabolik faktör hepatik lipogenezi tetikler?",
            {"A": "Artmış ATP/ADP oranı", "B": "Yüksek NADH/NAD+ oranı", "C": "Azalmış serbest yağ asitleri", "D": "Glukagon aşırılığı", "E": "Düşük laktat düzeyi"},
            "B",
            {
                "A": "ATP fazlalığı primer neden değildir.",
                "B": "Doğru cevap B'dir: Alkolün metabolize edilmesiyle ortaya çıkan yüksek NADH/NAD+ oranı beta-oksidasyonu durdurur ve yağ asidi sentezini uyarır.",
                "C": "Yağ asitleri azalmaz, aksine artar.",
                "D": "Glukagon değil insülin/lipogenez dengesizliği vardır.",
                "E": "Laktat düzeyi yükselir."
            }
        ),
        25: make_micro_quiz(
            "Ailesel hiperkolesterolemi tanısı alan homozigot bir hastada LDL reseptör genindeki temel bozukluğun hücresel patolojisi nedir?",
            {"A": "Apolipoprotein B sentezlenememesi", "B": "Reseptör aracılı endositozun yapılamaması sonucu plazma LDL'sinin temizlenememesi", "C": "Kolesterolün safra asidine çevrilememesi", "D": "Lizozomal asit lipaz yokluğu", "E": "Lipoprotein lipazın genetik yokluğu"},
            "B",
            {
                "A": "ApoB sentezi normaldir.",
                "B": "Doğru cevap B'dir: LDL reseptör mutasyonu kanda LDL'nin hepatositler tarafından alınmasını engeller ve masif hiperkolesterolemi yapar.",
                "C": "Safra asidi sentez kusuru değildir.",
                "D": "Wolman hastalığı ile ilgilidir.",
                "E": "Şilomikron metabolizması ile ilgilidir."
            }
        ),
        35: make_micro_quiz(
            "Alkolik hepatit tanılı bir hastanın karaciğer biyopsisinde görülen Mallory-Denk cisimciklerinin ana iskelet bileşeni hangisidir?",
            {"A": "Aktin mikroflamanları", "B": "Sitokeratin 8 ve 18 ara filamanları", "C": "Tubulin mikrotübülleri", "D": "Kollajen tip I lifleri", "E": "İmmünoglobulin hafif zincirleri"},
            "B",
            {
                "A": "Aktin kasılma filamanıdır.",
                "B": "Doğru cevap B'dir: Mallory-Denk cisimcikleri bozulmuş sitokeratin 8 ve 18 ara filamanlarının ubiquitin ile kümelenmesidir.",
                "C": "Mikrotübül proteini tubulindir ancak Mallory agregatını oluşturmaz.",
                "D": "Kollajen ekstrasellülerdir.",
                "E": "Russell cisimciği içeriğidir."
            }
        ),
        45: make_micro_quiz(
            "Alfa-1 antitripsin eksikliğinde karaciğer biyopsisinde görülen eozinofilik kürelerin histokimyasal tanısında hangi boya kombinasyonu kullanılır?",
            {"A": "PAS pozitif ve diyastaz dirençli boyanma", "B": "Prusya mavisi pozitif boyanma", "C": "Kongo kırmızısı ile çift kırıcılık", "D": "Grocott gümüşleme", "E": "Fontana-Masson boyası"},
            "A",
            {
                "A": "Doğru cevap A'dır: A1AT globülleri glikoprotein olduğundan PAS pozitif boyanır ve amilaz/diyastaz ile sindirilmeye dirençlidir.",
                "B": "Prusya mavisi demiri boyar.",
                "C": "Kongo kırmızısı amiloidi boyar.",
                "D": "Gümüşleme mantarları boyar.",
                "E": "Fontana-Masson melanini boyar."
            }
        ),
        55: make_micro_quiz(
            "Glikoz-6-fosfataz enzim eksikliği olan Tip I glikojen depo hastalığında (von Gierke) karaciğer parankiminde biriken temel molekül hangisidir?",
            {"A": "Trigliserid", "B": "Normal yapıda glikojen", "C": "Anormal dallı amilopektin", "D": "Sfingomiyelin", "E": "Kolesterol kristalleri"},
            "B",
            {
                "A": "Steatozda trigliserid birikir.",
                "B": "Doğru cevap B'dir: von Gierke hastalığında glikojenin moleküler yapısı normaldir ancak glikoza hidrolize edilemediği için aşırı depolanır.",
                "C": "Tip IV Andersen hastalığında dallanma kusurlu glikojen birikir.",
                "D": "Niemann-Pick lipididir.",
                "E": "Aterom plağında görülür."
            }
        ),
        65: make_micro_quiz(
            "Akciğer parankiminde kömür tozu birikimi olan bir hastada gelişen antrakozisin kömür işçisi pnömokonyozuna (CWP) ilerlemesindeki kritik eşik nedir?",
            {"A": "Karbonun Prusya mavisi ile boyanmaya başlaması", "B": "Makrofajlardan salınan sitokinlerin fibroblast aktivasyonu ile ilerleyici fibrozis başlatması", "C": "Tirozinaz enzim aktivasyonu", "D": "Serum kalsiyumunun 12 mg/dL'yi aşması", "E": "Alfa-1 antitripsin polimerleşmesi"},
            "B",
            {
                "A": "Karbon Prusya mavisi ile boyanmaz.",
                "B": "Doğru cevap B'dir: Yoğun partikül yükü makrofajları aktive ederek PDGF ve TGF-beta salgılatır; bu da masif kollajen birikimine ve PMF'ye yol açar.",
                "C": "Melanin yolağıdır.",
                "D": "Metastatik kalsifikasyon eşiğidir.",
                "E": "Genetik mutasyondur."
            }
        ),
        75: make_micro_quiz(
            "Kronik pulmoner konjesyon zemininde gelişen kalp yetmezliği hücreleri hangi hücre tipinin hemosiderin ile dolmasıyla oluşur?",
            {"A": "Tip II pnömositler", "B": "Alveoler makrofajlar", "C": "Bronş epitel hücreleri", "D": "Endotel hücreleri", "E": "İnterstisyel fibroblastlar"},
            "B",
            {
                "A": "Tip II hücreler sürfaktan üretir.",
                "B": "Doğru cevap B'dir: Alveollere sızan eritrositleri fagosite edip hemoglobini hemosiderine çeviren hücreler alveoler makrofajlardır (siderofajlar).",
                "C": "Bronş epiteli silialıdır, fagositoz yapmaz.",
                "D": "Endotel damar iç döşemesidir.",
                "E": "Fibroblast kollajen üretir."
            }
        ),
        85: make_micro_quiz(
            "Aterosklerotik plağın nekrotik merkezinde gelişen kalsifikasyonun distrofik kalsifikasyon olarak tanımlanmasının temel gerekçesi hangisidir?",
            {"A": "Hastada PTH yüksekliği olması", "B": "Serum kalsiyumunun normal olması ve birikimin ölü hücre artıkları üzerinde gerçekleşmesi", "C": "Mide mukozasında da kalsiyum birikmesi", "D": "Kalsiyumun sadece elastik laminada bulunması", "E": "Böbrek yetmezliği ile birlikte seyretmesi"},
            "B",
            {
                "A": "PTH yüksekliği metastatik kalsifikasyona yol açar.",
                "B": "Doğru cevap B'dir: Normokalsemi varlığında nekrotik hücre debrisleri üzerinde kalsiyum-fosfat kristallenmesi distrofik kalsifikasyonun tanımıdır.",
                "C": "Mide tutulumu metastatik kalsifikasyonun hedefidir.",
                "D": "Elastik laminaya sınırlı değildir.",
                "E": "Böbrek yetmezliği metastatiktir."
            }
        ),
        95: make_micro_quiz(
            "Sarkoidoz hastalarında sistemik metastatik kalsifikasyona yol açan hiperkalseminin hücresel kaynağı nedir?",
            {"A": "Paratiroid adenomu gelişmesi", "B": "Granülomlardaki mononükleer fagositlerin 1-alfa hidroksilaz sentezlemesi", "C": "Kemik iliğinde multipl miyelom odakları", "D": "Böbrek tübüllerinin kalsiyumu tutamaması", "E": "Karaciğerde albumin sentezinin durması"},
            "B",
            {
                "A": "Sarkoidoz paratiroid adenomu yapmaz.",
                "B": "Doğru cevap B'dir: Sarkoid granülomundaki epitelioid histiyositler denetimsiz 1-alfa hidroksilaz üreterek D vitaminini aşırı aktive eder.",
                "C": "Miyelom farklı bir malignitedir.",
                "D": "Kalsiyum tutulur.",
                "E": "Albumin düşüklüğü hiperkalsemi yapmaz."
            }
        ),
        12: make_micro_quiz(
            "Hepatosteatozda trigliseridlerin karaciğerden plazmaya salınabilmesi için hangi lipoprotein yapısına paketlenmesi zorunludur?",
            {"A": "HDL", "B": "VLDL", "C": "Şilomikron", "D": "LDL", "E": "Albümin"},
            "B",
            {
                "A": "HDL ters kolesterol taşır.",
                "B": "Doğru cevap B'dir: Hepatositler trigliseridleri ApoB-100 ile birleştirerek VLDL partikülleri şeklinde kana verir.",
                "C": "Şilomikron bağırsaktan emilen diyet lipidlerini taşır.",
                "D": "LDL periferik dokulara kolesterol götürür.",
                "E": "Albümin serbest yağ asitlerini taşır ancak lipoprotein değildir."
            }
        ),
        22: make_micro_quiz(
            "Aterogenez sırasında intimaya giren LDL'nin köpük hücreler tarafından kontrolsüzce yutulabilmesi için hangi modifikasyona uğraması gerekir?",
            {"A": "Glikozilasyon", "B": "Oksidasyon (ox-LDL)", "C": "Fosforilasyon", "D": "Metilasyon", "E": "Ubiquitinasyon"},
            "B",
            {
                "A": "Diyabette glikozilasyon olur ancak köpük hücre için anahtar oksidasyondur.",
                "B": "Doğru cevap B'dir: Reaktif oksijen türleri tarafından oksitlenen ox-LDL çöpçü (scavenger) reseptörlerle negatif geri bildirimsiz yutulur.",
                "C": "Fosforilasyon hücre içi sinyaldir.",
                "D": "Metilasyon epigenetiktir.",
                "E": "Ubiquitinasyon proteazom yıkımı içindir."
            }
        ),
        32: make_micro_quiz(
            "Nefrotik sendromda böbrek proksimal tübül hücrelerinde biriken eozinofilik damlacıkların kimyasal doğası nedir?",
            {"A": "Trigliserid", "B": "Geri emilen albümin ve plazma proteinleri", "C": "Lipofuksin", "D": "Kalsiyum fosfat kristalleri", "E": "Glikojen"},
            "B",
            {
                "A": "Lipid değildir.",
                "B": "Doğru cevap B'dir: Glomerülden sızan aşırı filtre edilmiş albümin proksimal tübül epiteli tarafından pinositozla geri emilir ve damlacıklar yapar.",
                "C": "Lipofuksin yaşlanma pigmentidir.",
                "D": "Kalsifikasyon değildir.",
                "E": "Diyabette glikojen birikir."
            }
        ),
        42: make_micro_quiz(
            "Endoplazmik retikulumda aşırı katlanmamış protein birikimi hücre içi adaptasyon kapasitesini aştığında apoptozu başlatan organel spesifik molekül hangisidir?",
            {"A": "Kaspaz-12 ve CHOP proteini", "B": "Kollajenaz", "C": "Amilaz", "D": "Lipaz", "E": "Tirozin kinaz"},
            "A",
            {
                "A": "Doğru cevap A'dır: ER stresinde UPR başarısız olunca CHOP indüklenir ve ER ilişkili kaspaz-12 üzerinden intrensek apoptoz aktive edilir.",
                "B": "Kollajenaz matriks eritir.",
                "C": "Amilaz nişasta sindirir.",
                "D": "Lipaz lipid yıkar.",
                "E": "Tirozin kinaz büyüme faktörü reseptörüdür."
            }
        ),
        82: make_micro_quiz(
            "Meme biyopsisinde şüpheli kitle kesitinde yağ nekrozu alanında tebeşir beyazı odaklar görülüyor. Bu lezyondaki kalsiyum tuzlarının oluşum mekanizması nedir?",
            {"A": "Metastatik hiperkalsemik çökme", "B": "Serbest yağ asitlerinin kalsiyumla sabunlaşması (saponifikasyon)", "C": "Melanosit hiperplazisi", "D": "Amiloidoz birikimi", "E": "Glikojen depo reaksiyonu"},
            "B",
            {
                "A": "Serum kalsiyumu normaldir.",
                "B": "Doğru cevap B'dir: Yağ nekrozunda açığa çıkan yağ asitleri kalsiyumu bağlayarak çözünmeyen kalsiyum sabunları oluşturur (distrofik kalsifikasyon).",
                "C": "Melanositle ilgisi yoktur.",
                "D": "Amiloidozis kalsiyum sabunu yapmaz.",
                "E": "Karbonhidrat metabolizması ile ilgisizdir."
            }
        )
    }

def get_15_chains():
    return {
        3: make_causal_chain(
            "Yağlı Karaciğerde Lipoprotein Sentez Felci Zinciri",
            [
                "1. Toksin Girişi: Karbon tetraklorür (CCl4) veya ağır toksin hepatosite girer.",
                "2. Serbest Radikal: Toksik serbest radikaller granüllü ER membranını peroksitler.",
                "3. Translasyon Felci: Ribozomlar ER'den kopar ve apoprotein sentezi kilitlenir.",
                "4. Yağ Hapsi: Trigliseridler VLDL'ye paketlenemediği için sitoplazmada birikir."
            ]
        ),
        13: make_causal_chain(
            "Alkol Metabolizması ve Hepatik Trigliserid Birikimi",
            [
                "1. Alkol Alımı: Etanol hepatositte sitozolik alkol dehidrogenaz ile asetaldehite döner.",
                "2. Koenzim Kayması: Bu basamakta NAD+ tükenerek yoğun NADH üretilir.",
                "3. Oksidasyon Bloku: Yüksek NADH mitokondriyal yağ asidi beta-oksidasyonunu felç eder.",
                "4. Gliserofosfat Artışı: Fazla hidrojen gliserol-3-fosfatı artırarak trigliserid sentezini katlar.",
                "5. Steatoz: Karaciğer lobüllerinde iri lipid vakuolleri birikir."
            ]
        ),
        23: make_causal_chain(
            "Köpük Hücre Oluşumu ve Aterom Plağı Nekrozu",
            [
                "1. LDL Alımı: Makrofaj çöpçü reseptörleri ox-LDL'yi doymaksızın yutar.",
                "2. Kolesterol Deposu: Sitoplazma kolesteril ester damlacıklarıyla silme dolar.",
                "3. Sitotoksisite: Aşırı serbest kolesterol ER stresini tetikler.",
                "4. Hücre Lizisi: Köpük hücre apoptoza giderek parçalanır.",
                "5. Kolesterol Kleftleri: Ekstrasellüler matrikste sivri kolesterol kristalleri çöker."
            ]
        ),
        33: make_causal_chain(
            "Plazma Hücresinde Russell Cisimciği Oluşumu",
            [
                "1. Aşırı Stimülasyon: Kronik inflamasyonda plazma hücresi yoğun immünoglobulin üretir.",
                "2. Sekresyon Engeli: Hatalı katlanma veya aşırı yük nedeniyle Ig salgılanamaz.",
                "3. gER Şişmesi: Granüllü endoplazmik retikulum sisternleri proteinle gerilir.",
                "4. Küresel Agregat: Sitoplazmada parlak pembe yuvarlak Russell cisimciği oluşur."
            ]
        ),
        43: make_causal_chain(
            "Alfa-1 Antitripsin PiZZ Hepatosit Hasar Zinciri",
            [
                "1. Genetik Mutasyon: SERPINA1 genindeki Glu342Lys değişimi proteini bozar.",
                "2. Polimerizasyon: Mutant PiZ monomerleri hepatosit ER'sinde birbirine kilitlenir.",
                "3. Kalite Kontrol Takılması: Polimerler ER'den Golgi'ye transfer edilemez.",
                "4. Kronik ER Stresi: Genişleyen ER sisternleri kaspaz kaskadını tetikler.",
                "5. Fibrozis ve Siroz: Apoptoza giden hepatositler yerini perisinüzoidal kollajene bırakır."
            ]
        ),
        53: make_causal_chain(
            "von Gierke Hastalığında Metabolik Kriz Zinciri",
            [
                "1. Enzim Eksikliği: Hepatositlerde glikoz-6-fosfataz aktivitesi sıfırdır.",
                "2. Glikoz Hapsi: Karaciğerde glikojen yıkılsa da serbest glikoz kana salınamaz.",
                "3. Açlık Hipoglisemisi: Beyin ve çevre dokularda glikoz krizi gelişir.",
                "4. Şant Aktivasyonu: Biriken fosfatlı şekerler heksoz monofosfata ve laktata kayar.",
                "5. Sistemik Asidoz: Ağır laktik asidoz ve pürin yıkımıyla hiperürisemi (gut) oturur."
            ]
        ),
        63: make_causal_chain(
            "Solunan Karbonun Hiler Lenf Düğümüne Ulaşım Zinciri",
            [
                "1. İnspirasyon: Şehir havasındaki karbon partikülleri alveollere ulaşır.",
                "2. Çöpçü Yakalama: Alveoler makrofajlar karbon parçacıklarını fagosite eder.",
                "3. Lenfatik Drenaj: Partikül yüklü makrofajlar lenf kanallarına sızar.",
                "4. Hiler Filtrasyon: Trakeobronşiyal ve hiler lenf düğümlerinde filtre edilir.",
                "5. Antrakozis: Lenf bezleri kömür karası renge bürünerek kalıcı olarak işaretlenir."
            ]
        ),
        73: make_causal_chain(
            "Herediter Hemokromatozda Bronz Diyabet Gelişim Zinciri",
            [
                "1. HFE Mutasyonu: Hepatositlerden hepsidin hormonu salgısı durur.",
                "2. Aşırı Emilim: Bağırsak enterositlerinden kontrolsüz demir plazmaya akar.",
                "3. Demir Yükü: Transferrin doygunluğu %100'e çıkar, serbest demir dokulara çöker.",
                "4. Fenton Hasarı: Pankreas Langerhans adacıkları serbest radikallerle tahrip olur.",
                "5. Diyabet: İnsülin sekresyon yetmezliği ve cilt hiperpigmentasyonu (Bronz Diyabet) tablosu oturur."
            ]
        ),
        83: make_causal_chain(
            "Distrofik Kalsifikasyonun Kristallenme Zinciri",
            [
                "1. Hücresel Nekroz: Doku hasarıyla hücre zarlarının bariyer fonksiyonu biter.",
                "2. Kalsiyum Girişi: Ekstrasellüler kalsiyum nekrotik hücre mitokondrisine akar.",
                "3. Membran Fosfolipitleri: Hasarlı zarlardaki asidik fosfolipitler kalsiyumu şelatlar.",
                "4. Fosfataz Etkisi: Membran enzimleri lokal inorganik fosfat konsantrasyonunu artırır.",
                "5. Hidroksiapatit: Kalsiyum fosfat kristalleri büyüyerek mor bazofilik çökelti yapar."
            ]
        ),
        93: make_causal_chain(
            "Primer Hiperparatiroidide Metastatik Kalsifikasyon Zinciri",
            [
                "1. Adenom Gelişimi: Paratiroid bezinde fonksiyonel otonom adenom oluşur.",
                "2. Kontrolsüz PTH: Yüksek PTH kemikten osteoklastik kalsiyum salınımını kamçılar.",
                "3. Ağır Hiperkalsemi: Serum kalsiyumu 13-14 mg/dL seviyelerine tırmanır.",
                "4. Çözünürlük Çarpımı: [Ca x P] çarpımı doku çökelme eşiğini aşar.",
                "5. Mide ve Akciğer Tutulumu: Asit kaybeden alkali organların bazal zarlarına kalsiyum çöker."
            ]
        ),
        16: make_causal_chain(
            "Lipotoksisiteden Steatohepatite İlerleyiş Zinciri",
            [
                "1. Aşırı Trigliserid: Hepatosit sitoplazmasında serbest yağ asitleri birikir.",
                "2. Toksik Ara Ürünler: Diasilgliserol ve seramidler organel membranlarını zedeler.",
                "3. ROS Patlaması: Mitokondriyal elektron kaçağı reaktif oksijen radikalleri üretir.",
                "4. Hepatosit Balonlaşması: Hücre iskeleti dağılır ve sitokin salgısıyla nötrofiller çekilir.",
                "5. Steatohepatit: İnflamasyon zemininde nekroz ve stellat hücre aktivasyonu başlar."
            ]
        ),
        26: make_causal_chain(
            "Kolesterolozis (Çilek Safra Kesesi) Patogenez Zinciri",
            [
                "1. Aşırı Doygun Safralanma: Karaciğer safraya aşırı miktarda kolesterol salgılar.",
                "2. Epitelyal Emilim: Safra kesesi mukozası lümendeki kolesterolü pinositozla emer.",
                "3. Lamina Propriaya Aktarım: Epitel hücreleri kolesterolü submukozal alana pompalar.",
                "4. Histiyosit Fagositozu: Lamina propriadaki makrofajlar kolesterolü yutarak köpük hücreye döner.",
                "5. Çilek Kesesi: Kırmızı mukoza üzerinde sarı noktalı kolesterolozis deseni belirir."
            ]
        ),
        36: make_causal_chain(
            "Alzheimer Hastalığında Nörofibriler Yumak Oluşumu",
            [
                "1. Kinaz Aktivasyonu: Patolojik sinyaller tau protein kinazlarını aşırı uyarır.",
                "2. Hiperfosforilasyon: Tau proteini normalden kat kat fazla fosfat grubu bağlar.",
                "3. Mikrotübül Dağılması: Fonksiyonunu yitiren tau mikrotübüllerden ayrılır.",
                "4. İkili Helikal Filamanlar: Serbest fosforile tau molekülleri sarmal lifler halinde birleşir.",
                "5. Nörofibriler Yumak: Nöron perikaryonunda alev şekilli çözünmeyen yumaklar birikir."
            ]
        ),
        76: make_causal_chain(
            "Akut Pankreatitte Saponifikasyon Zinciri",
            [
                "1. Duktal Tıkanma / Toksisite: Asiner hücrelerde zimojen granülleri erken aktive olur.",
                "2. Lipaz Kaçağı: Aktif pankreatik lipaz retroperitona ve periton boşluğuna sızar.",
                "3. Adiposit Lizisi: Lipaz omentum ve mezenterdeki nötral yağları parçalar.",
                "4. Yağ Asidi Ayrışması: Serbest yağ asitleri lokal mikroçevrede yoğunlaşır.",
                "5. Kalsiyum Bağlanması: Plazma kalsiyumu yağ asitleriyle tuz oluşturarak tebeşir beyazı sabun yapar."
            ]
        ),
        96: make_causal_chain(
            "Kronik Böbrek Yetmezliğinde Kalsifilaksi Zinciri",
            [
                "1. GFR Düşüşü: Nefron kaybı nedeniyle inorganik fosfat böbrekten atılamaz.",
                "2. Hiperfosfatemi: Kanda yükselen fosfat kalsiyumu bağlar ve hipokalsemi yapar.",
                "3. Sekonder Hiperparatiroidizm: Düşük kalsiyum paratiroidleri sürekli uyararak PTH'yı fırlatır.",
                "4. Yüksek [Ca x P]: Kemikten kalsiyum çekilmesiyle kalsiyum-fosfat çarpımı 70'i aşar.",
                "5. Deri Damar Kireçlenmesi: Küçük arterioller kalsifiye olup tıkanır ve gangrenöz deri nekrozu gelişir."
            ]
        )
    }

def get_15_sliders():
    return {
        4: make_before_after(
            "Yetersiz Klirens ile Katlanma Hatası Karşılaştırması",
            "Yetersiz Klirens (Steatoz)",
            "Molekül yapısı normaldir; sentez hızı klirens kapasitesini aştığı için birikir.",
            "Katlanma Hatası (A1AT Eksikliği)",
            "Molekül yapısı genetik mutasyonla bozuktur; ER kalite kontrolünden geçemediği için birikir."
        ),
        14: make_before_after(
            "Mikroveziküler ile Makroveziküler Steatoz Karşılaştırması",
            "Mikroveziküler Steatoz (Reye)",
            "Sitoplazmada minik damlacıklar vardır; çekirdek ortada kalır, mitokondri toksisitesiyle ilişkilidir.",
            "Makroveziküler Steatoz (Alkol)",
            "Birleşen iri yağ kisti çekirdeği hücre kenarına iter ve taşlı yüzük hücresi görünümü verir."
        ),
        24: make_before_after(
            "Ateroskleroz ile Ksantom Arasındaki Kolesterol Dağılımı",
            "Ateroskleroz Plağı",
            "Büyük arterlerin intimasında köpük hücreler, nekrotik kor ve sivri kolesterol kristalleri bulunur.",
            "Tendon Ksantomu",
            "Deri ve tendon bağ dokusunda köpük hücre kümeleri toplanır; sarı benign nodüller yapar."
        ),
        34: make_before_after(
            "Russell Cisimciği ile Dutcher Cisimciği Karşılaştırması",
            "Russell Cisimciği",
            "Granüllü endoplazmik retikulumda biriken sitoplazmik eozinofilik immünoglobulin küresidir.",
            "Dutcher Cisimciği",
            "İmmünoglobulin dolu veziküllerin nükleus membranını itmesiyle oluşan psödonükleer inklüzyondur."
        ),
        44: make_before_after(
            "Normal PiMM Genotipi ile PiZZ Genotipinin Karaciğer Görünümü",
            "Normal PiMM Genotipi",
            "A1AT karaciğerden hızla salgılanır; hepatosit sitoplazması berrak ve homojendir.",
            "Mutant PiZZ Genotipi",
            "A1AT polimerleri ER sisternlerinde birikir; PAS pozitif ve diyastaz dirençli dev globüller yapar."
        ),
        54: make_before_after(
            "Hepatik Glikojenoz (Tip I) ile Miyopatik Glikojenoz (Tip V)",
            "von Gierke Hastalığı (Hepatik)",
            "Glikoz-6-fosfataz eksiktir; derin açlık hipoglisemisi, laktik asidoz ve masif hepatomegali vardır.",
            "McArdle Hastalığı (Miyopatik)",
            "Kas fosforilazı eksiktir; kan şekeri normaldir ancak egzersiz krampı ve miyoglobinüri görülür."
        ),
        64: make_before_after(
            "Basit Antrakozis ile Progresif Masif Fibrozis (PMF)",
            "Basit Antrakozis",
            "Alveoler makrofajlarda zararsız karbon pigmenti; doku mimarisi ve solunum fonksiyonu korunur.",
            "Progresif Masif Fibrozis",
            "Aşırı karbon-silika yüküyle oluşan 2 cm'den büyük yoğun kollajen skarlar ve fatal dispne."
        ),
        74: make_before_after(
            "Lipofuksin ile Hemosiderin Karşılaştırması",
            "Lipofuksin (Aşınma)",
            "Lipid peroksidasyonundan kaynaklanır; Prusya mavisi negatiftir ve UV ışıkta otofloresans verir.",
            "Hemosiderin (Demir)",
            "Eritrosit yıkımından kaynaklanır; Prusya mavisi ile parlak mavi boyanır ve otofloresans vermez."
        ),
        84: make_before_after(
            "Distrofik Kalsifikasyon ile Metastatik Kalsifikasyon Temel Ayrımı",
            "Distrofik Kalsifikasyon",
            "Serum kalsiyumu normaldir; hasarlı, nekrotik veya sklerotik dokuda lokal kireçlenme olur.",
            "Metastatik Kalsifikasyon",
            "Serum kalsiyumu yüksektir; önceden sağlıklı olan canlı dokularda (mide, böbrek, akciğer) yaygın çöker."
        ),
        94: make_before_after(
            "Mide Mukozası ile Akciğer Alveolünün Metastatik Kalsifikasyon Duyarlılığı",
            "Mide Mukozası",
            "Lümene hidroklorik asit salgılayarak hücresel ortamını alkaliye kaydırır ve kalsiyum tuzlarını çöktürür.",
            "Akciğer Alveol Septaları",
            "Karbondioksiti (asit) dışarı üfleyerek interstisyel pH'yı yükseltir ve kalsiyum fosfat kristallerini çeker."
        ),
        17: make_before_after(
            "Normal Karaciğer Parankimi ile Steatotik Karaciğer Parankimi",
            "Normal Karaciğer",
            "Kırmızımsı kahverengi, keskin kenarlı ve düzenli kordonlar oluşturan poligonal hepatositler.",
            "Steatotik Karaciğer",
            "Büyümüş, sarı, yağlı kesit yüzlü karaciğer ve sitoplazmaları dev yağ kistleriyle dolu hücreler."
        ),
        27: make_before_after(
            "Ksantelazma ile Ksantom Lezyonlarının Dağılımı",
            "Ksantelazma",
            "Özellikle göz kapaklarının iç kantusunda subkutan yerleşen yumuşak sarı plaklar.",
            "Tendon Ksantomu",
            "Aşil tendonu ve parmak ekstansör tendonlarında kemik gibi sert palpe edilen derin nodüller."
        ),
        47: make_before_after(
            "Kistik Fibrozis (CFTR) ile A1AT Eksikliği Arasındaki Protein Akıbeti",
            "Kistik Fibrozis (CFTR)",
            "Mutant protein endoplazmik retikulumda proteazomlar tarafından hızla yıkılarak yok edilir.",
            "Alfa-1 Antitripsin (PiZZ)",
            "Mutant protein proteazomlarca yıkılamaz; ER içinde polimerleşerek dev inklüzyonlar yapar."
        ),
        67: make_before_after(
            "Melanositik Nevus ile Malign Melanom Karşılaştırması",
            "Melanositik Nevus (Ben)",
            "Simetrik, düzgün sınırlı, homojen pigmentli ve dermiste derinleştikçe olgunlaşan benign yuvalar.",
            "Malign Melanom",
            "Asimetrik, sınırları girintili çıkıntılı, alacalı renk dağılımlı ve kontrolsüz invaziv atipik hücreler."
        ),
        87: make_before_after(
            "Psammom Cisimciği ile Aterom Plağı Kalsifikasyonu",
            "Psammom Cisimciği",
            "Tek bir apoptotik tümör hücresi etrafında konsantrik soğan zarı tabakaları şeklinde lameller kireçlenme.",
            "Aterom Plağı Kalsifikasyonu",
            "Nekrotik lipid korunda yaygın amorf, parçalı ve kırılgan distrofik kalsiyum kabuğu."
        )
    }

def get_15_branchings():
    return {
        6: make_branching_logic(
            "40 yaşında asemptomatik bir erkeğin rutin kan tahlilinde karaciğer enzimleri hafif yüksek bulunuyor. Ultrasonografide karaciğer ekojenitesi artmış ve parlak izleniyor. Hastanın haftada 4 gün ağır alkol tükettiği öğreniliyor. Öncelikli yaklaşımınız nedir?",
            [
                {"text": "Acil karaciğer transplantasyon listesine almak", "isCorrect": False, "feedback": "Erken evre steatozda cerrahi endikasyon yoktur."},
                {"text": "Alkolün tamamen kesilmesini sağlamak ve tablonun reversibl olduğunu bilerek 3 ay sonra enzimleri tekrarlamak", "isCorrect": True, "feedback": "Mükemmel klinik yaklaşım! Alkolik steatoz etken kesildiğinde tamamen geri dönüşümlü bir patolojidir."},
                {"text": "Demir birikimini önlemek için hemen flebotomi uygulamak", "isCorrect": False, "feedback": "Alkolik steatoz tedavisinde flebotominin yeri yoktur."}
            ]
        ),
        18: make_branching_logic(
            "Diyabetik bir hastanın böbrek biyopsisinde tübül epitel hücreleri sitoplazmasında berrak boşluklar görülüyor. Bu boşlukların yağ mı yoksa glikojen mi olduğunu kanıtlamak için hangi basamak izlenmelidir?",
            [
                {"text": "Kongo kırmızısı boyası uygulamak", "isCorrect": False, "feedback": "Kongo kırmızısı amiloidoz içindir."},
                {"text": "Dondurulmuş kesitte Oil Red O ve parafinde PAS-Diyastaz boyalarını karşılaştırmalı uygulamak", "isCorrect": True, "feedback": "Kusursuz laboratuvar kararı! Oil Red O lipidleri kırmızı boyarken, PAS pozitif ve diyastazla sindirilen alanlar glikojeni kesinleştirir."},
                {"text": "Prusya mavisi ile demir aramak", "isCorrect": False, "feedback": "Demir pigmenti berrak boşluk yapmaz."}
            ]
        ),
        28: make_branching_logic(
            "28 yaşında bir erkeğin topuk arkasında sert ağrısız nodül saptanıyor. Biyopside köpük hücre kümeleri ve kolesterol yarıkları görülüyor. Hastanın birinci derece akrabalarında erken kalp krizi öyküsü var. En olası tanı nedir?",
            [
                {"text": "Niemann-Pick Tip C hastalığı", "isCorrect": False, "feedback": "Nörolojik bulgular ve organomegali ön plandadır."},
                {"text": "Ailesel Hiperkolesterolemiye bağlı Aşil tendonu ksantomu", "isCorrect": True, "feedback": "Tam isabet! Genç yaşta Aşil tendon ksantomu ve ailede erken koroner hastalık öyküsü Ailesel Hiperkolesterolemi için patognomoniktir."},
                {"text": "Distrofik kalsifikasyonlu gut tofüsü", "isCorrect": False, "feedback": "Gut tofüsünde ürat kristalleri ve yabancı cisim dev hücreleri bulunur."}
            ]
        ),
        38: make_branching_logic(
            "Kemik iliği biyopsisinde bol miktarda plazma hücresi ve sitoplazmalarında eozinofilik küresel cisimcikler (Russell cisimcikleri) izleniyor. Bu hastada şüphelenilmesi gereken temel hematolojik patoloji hangisidir?",
            [
                {"text": "Multipl Miyelom veya monoklonal gamapati", "isCorrect": True, "feedback": "Doğru teşhis! Russell cisimciklerinin aşırı arttığı Mott hücreleri plazma hücre neoplazilerinin tipik bulgusudur."},
                {"text": "Kronik miyeloid lösemi", "isCorrect": False, "feedback": "KML miyeloid serinin granülositik neoplazisidir."},
                {"text": "Demir eksikliği anemisi", "isCorrect": False, "feedback": "Demir eksikliğinde plazma hücre inklüzyonları görülmez."}
            ]
        ),
        48: make_branching_logic(
            "30 yaşında hiç sigara içmemiş bir hastada ilerleyici dispne saptanıyor ve akciğer grafisinde alt loblarda belirgin panasinöz amfizem görülüyor. Karaciğer enzimlerinde de hafif yükseklik var. En olası tanı nedir?",
            [
                {"text": "Sigaraya bağlı sentriasiner amfizem", "isCorrect": False, "feedback": "Hasta hiç sigara içmemiştir ve amfizem alt loblardadır (panasinöz)."},
                {"text": "Alfa-1 antitripsin eksikliği (PiZZ fenotipi)", "isCorrect": True, "feedback": "Mükemmel tanısal sentez! Genç yaşta sigara içmeyen bireyde alt lob panasinöz amfizemi ve karaciğer tutulumu A1AT eksikliğinin klasik sunumudur."},
                {"text": "Kistik fibrozis", "isCorrect": False, "feedback": "Kistik fibroziste bronşiektazi ve üst lob tutulumu belirgindir."}
            ]
        ),
        58: make_branching_logic(
            "Ağır fiziksel egzersiz sonrası şiddetli kas krampları ve idrarında bordo-kahverengi renk değişikliği ile başvuran genç bir atlette iskemik önkol testinde laktat artışı saptanmıyor. Tanınız nedir?",
            [
                {"text": "Tip I GSD (von Gierke)", "isCorrect": False, "feedback": "von Gierke karaciğer tutulumu ve laktik asidoz yapar."},
                {"text": "Tip V GSD (McArdle Hastalığı)", "isCorrect": True, "feedback": "Doğru tanı! Kas glikojen fosforilaz eksikliği egzersiz krampı, laktat artış yokluğu ve rabdomiyolize bağlı miyoglobinüri ile seyreder."},
                {"text": "Pompe Hastalığı", "isCorrect": False, "feedback": "Pompe infantil kardiyomegali yapar."}
            ]
        ),
        68: make_branching_logic(
            "Genç bir kadının el sırtında ve ağız çevresinde keskin sınırlı tebeşir beyazı renk açılmaları görülüyor. Deri biyopsisinde bazal tabakada melanositlerin tamamen kaybolduğu izleniyor. Tanınız nedir?",
            [
                {"text": "Okülokutanöz Albinizm", "isCorrect": False, "feedback": "Albinizmde melanosit sayısı normaldir, tirozinaz çalışmaz."},
                {"text": "Vitiligo", "isCorrect": True, "feedback": "Tebrikler! Melanositlerin otoimmün yıkımı sonucu histolojide melanosit yokluğu vitiligonun kesin kriteridir."},
                {"text": "Pitriyazis versikolor", "isCorrect": False, "feedback": "Mantar enfeksiyonudur, melanosit kaybı yapmaz."}
            ]
        ),
        78: make_branching_logic(
            "60 yaşında diyabetik bir erkekte ciltte koyulaşma, eklem ağrıları ve karaciğer yetmezliği bulguları gelişiyor. Karaciğer biyopsisinde hepatositlerde altın sarısı granüller izleniyor. Tanıyı kesinleştirmek için ilk basamak ne olmalıdır?",
            [
                {"text": "Kesite Prusya mavisi boyaması yaparak demir (hemosiderin) varlığını araştırmak", "isCorrect": True, "feedback": "Harika patoloji kararı! Bronz diyabet tablosunda Prusya mavisi ile hemosiderin saptanması hemokromatozu kanıtlar."},
                {"text": "Hemen cerrahi rezeksiyon planlamak", "isCorrect": False, "feedback": "Metabolik hastalıklarda cerrahi rezeksiyon yapılmaz."},
                {"text": "Sarkoidoz yönünden ACE düzeyine bakmak", "isCorrect": False, "feedback": "Bronz diyabet ve karaciğer pigmentasyonu hemokromatoz için tipiktir."}
            ]
        ),
        88: make_branching_logic(
            "45 yaşında bir kadının tiroid nodülü ince iğne aspirasyon biyopsisinde nükleer yarıklar, buzlu cam benzeri nükleuslar ve konsantrik kalsifiye psammom cisimcikleri saptanıyor. Tanınız nedir?",
            [
                {"text": "Tiroidin foliküler adenomu", "isCorrect": False, "feedback": "Foliküler adenomda psammom cisimciği ve Orphan Annie nükleusu görülmez."},
                {"text": "Papiller tiroid karsinomu", "isCorrect": True, "feedback": "Kesin tanı! Psammom cisimcikleri ve nükleer özellikler papiller tiroid karsinomu için diagnostiktir."},
                {"text": "Metastatik kalsifikasyonlu tiroidit", "isCorrect": False, "feedback": "Psammom cisimcikleri distrofik lameller kireçlenmedir."}
            ]
        ),
        98: make_branching_logic(
            "Akciğerinde yaygın interstisyel kalsifikasyon saptanan bir hastanın laboratuvarında serum kalsiyumu 13.8 mg/dL ve fosfatı normal bulunuyor. Boyun ultrasonografisinde sağ alt paratiroid lojunda 2 cm nodül görülüyor. Bu kalsifikasyonun tipi ve mekanizması nedir?",
            [
                {"text": "Distrofik kalsifikasyon; tüberküloz kazeöz nekrozuna bağlı", "isCorrect": False, "feedback": "Hiperkalsemi varlığında distrofik denilemez."},
                {"text": "Metastatik kalsifikasyon; primer hiperparatiroidizme bağlı sistemik hiperkalsemi sonucu", "isCorrect": True, "feedback": "Mükemmel sentez! Paratiroid adenomu hiperkalsemiye, hiperkalsemi de normal dokuda metastatik kalsifikasyona yol açmıştır."},
                {"text": "Dövme pigmentine sekonder akciğer birikimi", "isCorrect": False, "feedback": "Dövme pigmenti kalsiyum yüksekliği yapmaz."}
            ]
        ),
        5: make_branching_logic(
            "Bir patoloji asistanı karaciğer kesitinde soluk hepatosit sitoplazmaları görüyor. Bu görünümün glikojen mi yoksa lipid mi olduğunu ışık mikroskobunda en hızlı nasıl ayırt eder?",
            [
                {"text": "Sadece H&E boyasına bakarak karar verir.", "isCorrect": False, "feedback": "Rutin takipte her iki madde de eriyip boşluk bıraktığı için H&E ile güvenle ayırt edilemez."},
                {"text": "PAS boyası uygular; glikojen PAS ile parlak macenta boyanırken lipid boyanmaz.", "isCorrect": True, "feedback": "Doğru laboratuvar yaklaşımı! PAS glikojeni pozitif boyarken nötral lipidleri boyamaz."},
                {"text": "Kongo kırmızısı ile polarize mikroskoba bakar.", "isCorrect": False, "feedback": "Kongo kırmızısı amiloidozis içindir."}
            ]
        ),
        62: make_branching_logic(
            "Kömür madeni işçisinin akciğer biyopsisinde bronşiyol çevresinde siyah pigment odakları ve fokal amfizem görülüyor; ancak büyük fibröz kitle saptanmıyor. Evreleme ve yaklaşımınız ne olmalıdır?",
            [
                {"text": "Basit kömür işçisi pnömokonyozu (CWP); toz maruziyeti sonlandırılmalı ve takibe alınmalıdır.", "isCorrect": True, "feedback": "Çok doğru! Büyük skarların olmaması basit CWP evresini gösterir; ilerlemeyi önlemek için maden tozu kesilmelidir."},
                {"text": "Progresif masif fibrozis; hasta acil cerrahiye verilmelidir.", "isCorrect": False, "feedback": "PMF'de 2 cm'den büyük yoğun fibrozis kitleleri bulunur."},
                {"text": "Malign mezotelyoma; acil kemoterapi başlanmalıdır.", "isCorrect": False, "feedback": "Antrakozis karbon birikimidir, mezotelyoma asbestle ilişkilidir."}
            ]
        ),
        72: make_branching_logic(
            "Otopsi yapılan 88 yaşındaki bir kadının kalbinin belirgin küçülmüş (180 gram) ve renginin koyu kahverengi olduğu görülüyor. Mikroskopide miyosit nükleus kutuplarında ince granüller saptanıyor. Bu durumun patolojik adı nedir?",
            [
                {"text": "Kardiyak amiloidoz", "isCorrect": False, "feedback": "Amiloidoz kalbi büyütür (kardiyomegali) ve sertleştirir."},
                {"text": "Kahverengi atrofi (Lipofuksin birikimi)", "isCorrect": True, "feedback": "Tebrikler! İleri yaşlılıkta organ küçülmesi ve perinükleer lipofuksin depolanması klasik kahverengi atrofidir."},
                {"text": "Kalsifik aort stenozu", "isCorrect": False, "feedback": "Kapak taşlaşması ile ilgilidir."}
            ]
        ),
        82: make_branching_logic(
            "Tüberküloz öyküsü olan bir hastanın akciğer grafisinde sağ hiler bölgede 1.5 cm çapında kireçlenmiş sert bir nodül saptanıyor. Serum kalsiyumu 9.1 mg/dL (normal). Bu kalsifikasyonun tipi nedir?",
            [
                {"text": "Metastatik kalsifikasyon", "isCorrect": False, "feedback": "Serum kalsiyumu normaldir, metastatik olamaz."},
                {"text": "Ghon odağı zemininde distrofik kalsifikasyon", "isCorrect": True, "feedback": "Kusursuz yorum! Tüberküloz kazeöz nekroz alanlarının normokalsemik zemininde kireçlenmesi distrofik kalsifikasyondur."},
                {"text": "Kalsifilaksi lezyonu", "isCorrect": False, "feedback": "Kalsifilaksi böbrek yetmezliğinde damar kireçlenmesidir."}
            ]
        ),
        92: make_branching_logic(
            "Kronik böbrek yetmezliği nedeniyle hemodiyalize giren bir hastanın bacaklarında ağrılı iskemik deri ülserleri gelişiyor. Biyopside subkutan arteriollerin lümeninde tromboz ve duvarında kalsiyum çökmesi saptanıyor. Tanınız nedir?",
            [
                {"text": "Senil aort stenozu", "isCorrect": False, "feedback": "Kapak patolojisidir."},
                {"text": "Kalsifilaksi (Kalsifik üremik arteriolopati)", "isCorrect": True, "feedback": "Kesin klinik tanı! Yüksek [Ca x P] çarpımına bağlı küçük damar kireçlenmesi ve nekrotik ülserler kalsifilaksinin dramatik tablosudur."},
                {"text": "Hiyalin arteriyoloskleroz", "isCorrect": False, "feedback": "Hiyalin arteriyolosklerozda plazma proteini sızar, kalsiyum çökmesi ve nekroz bu boyutta olmaz."}
            ]
        )
    }

def get_15_tables():
    return {
        8: make_table(
            ["Hücre İçi Birikim Türü", "Tipik Morfolojik Özellik", "Karakteristik Klinik Örnek"],
            [
                [("Trigliserid (Steatoz)", False, ""), ("Berrak lipid vakuolleri", True, "Hepatosit sitoplazmasında birikim")],
                [("Kolesterol (Köpük Hücre)", False, ""), ("Köpüksü sitoplazmalı makrofaj", True, "Aterom plağı ve ksantom")],
                [("Protein (Russell Cisimciği)", False, ""), ("Parlak pembe eozinofilik küre", True, "Plazma hücresi ER sisternleri")]
            ]
        ),
        21: make_table(
            ["Lipid Birikim Lezyonu", "Temel Biriken Lipid", "Predileksiyon Anatomik Bölgesi"],
            [
                [("Hepatik Steatoz", False, ""), ("Trigliserid", True, "Karaciğer parankim hücreleri")],
                [("Aterom Plağı", False, ""), ("Kolesteril esterleri ve kristaller", True, "Büyük arter intimal tabakası")],
                [("Kolesterolozis", False, ""), ("Köpüksü makrofaj kolesterolü", True, "Safra kesesi lamina propriası")]
            ]
        ),
        31: make_table(
            ["Protein İnklüzyonu", "Temel Protein İçeriği", "İlişkili Hastalık Tablosu"],
            [
                [("Russell Cisimciği", False, ""), ("İmmünoglobulin molekülleri", True, "Plazma hücre neoplazileri ve miyelom")],
                [("Mallory-Denk Cisimciği", False, ""), ("Sitokeratin 8 ve 18 ara filamanları", True, "Alkolik hepatit ve steatohepatit")],
                [("Nörofibriler Yumak", False, ""), ("Hiperfosforile tau proteini", True, "Alzheimer demansı")]
            ]
        ),
        41: make_table(
            ["Genetik Hastalık", "Mutant Protein", "Hücresel Akıbet ve Hasar"],
            [
                [("Kistik Fibrozis", False, ""), ("CFTR proteini", True, "Proteazomal erken yıkım ve klor kanal yokluğu")],
                [("Alfa-1 Antitripsin Eksikliği", False, ""), ("PiZ proteini", True, "ER'de polimer birikimi, apoptoz ve siroz")],
                [("Creutzfeldt-Jakob", False, ""), ("Prion PrP proteini", True, "Beta-kırmalı konformasyon ve spongiform dejenerasyon")]
            ]
        ),
        51: make_table(
            ["Glikojenoz Tipi", "Eksik Enzim", "En Ağır Etkilenen Organ"],
            [
                [("Tip I (von Gierke)", False, ""), ("Glikoz-6-fosfataz", True, "Karaciğer ve böbrek")],
                [("Tip II (Pompe)", False, ""), ("Lizozomal asit maltaz", True, "Kalp kası (kardiyomegali)")],
                [("Tip V (McArdle)", False, ""), ("Kas glikojen fosforilazı", True, "İskelet kası lifleri")]
            ]
        ),
        61: make_table(
            ["Pigment Adı", "Eksojen / Endojen Köken", "Işık Mikroskobik Rengi"],
            [
                [("Karbon (Antrakozis)", False, ""), ("Eksojen (Solunum yolu)", True, "Kömür karası siyah granüller")],
                [("Lipofuksin", False, ""), ("Endojen (Lipid peroksidasyonu)", True, "Altın sarısı-kahverengi ince granüller")],
                [("Hemosiderin", False, ""), ("Endojen (Hemoglobin demiri)", True, "Altın sarısı-kahverengi kaba kitleler")]
            ]
        ),
        71: make_table(
            ["Demir Depo Formu", "Kimyasal Özellik", "Histolojik Boyanma Davranışı"],
            [
                [("Ferritin", False, ""), ("Apoferritin proteini ile çevrili demir çekirdeği", True, "Sitozolde çözünür, ışık mikroskobunda görünmez")],
                [("Hemosiderin", False, ""), ("Ferritinin lizozomal kaba agregatı", True, "Prusya mavisi ile parlak mavi boyanır")],
                [("Lipofuksin", False, ""), ("Okside lipid ve protein polimerleri", True, "Prusya mavisi ile kesinlikle boyanmaz")]
            ]
        ),
        81: make_table(
            ["Kalsifikasyon Türü", "Serum Kalsiyum Düzeyi", "Tipik Doku Örneği"],
            [
                [("Distrofik Kalsifikasyon", False, ""), ("Tamamen Normal (Normokalsemi)", True, "Aterom plağı, senil aort stenozu, Ghon kompleksi")],
                [("Metastatik Kalsifikasyon", False, ""), ("Daima Yüksek (Hiperkalsemi)", True, "Böbrek tübülleri (nefrokalsinoz), mide, akciğer")],
                [("Saponifikasyon", False, ""), ("Sıklıkla sekonder hipokalsemi", True, "Akut pankreatit omentum yağ nekrozu")]
            ]
        ),
        91: make_table(
            ["Hiperkalsemi Nedeni", "Temel Patofizyolojik Mekanizma", "Klinik Özellik"],
            [
                [("Primer Hiperparatiroidi", False, ""), ("Paratiroid adenomundan kontrolsüz PTH salgısı", True, "Kemik rezorpsiyonu ve nefrokalsinoz")],
                [("Multipl Miyelom", False, ""), ("Sitokinler aracılığıyla osteolitik kemik yıkımı", True, "Kemik ağrısı, anemi ve böbrek yetmezliği")],
                [("Sarkoidoz", False, ""), ("Granülom makrofajlarında 1-alfa hidroksilaz aktivasyonu", True, "D vitamininin denetimsiz aşırı sentezi")]
            ]
        ),
        11: make_table(
            ["Karaciğer Hasar Evresi", "Histopatolojik Temel Bulgu", "Geri Dönüşümlülük (Reversibilite)"],
            [
                [("Yalın Steatoz", False, ""), ("Hepatositlerde izole lipid damlacıkları", True, "Tamamen reversibl (normale döner)")],
                [("Steatohepatit", False, ""), ("Balonlaşma, nötrofil infiltrasyonu, Mallory cisimcikleri", True, "Kısmen reversibl (tedaviyle gerileyebilir)")],
                [("Mikronodüler Siroz", False, ""), ("Rejenerasyon nodülleri ve yaygın bağ dokusu septaları", True, "İrreversibl (geri dönüşümsüz kalıcı hasar)")]
            ]
        ),
        37: make_table(
            ["Hiyalin Değişim Alanı", "Anatomik Lokalizasyon", "Biriken Temel İçerik"],
            [
                [("Tübüler Hiyalin", False, ""), ("Proksimal tübül epitel sitoplazması", True, "Geri emilen albümin damlacıkları")],
                [("Hiyalin Arteriyoloskleroz", False, ""), ("Arteriyol duvarı (intima-media)", True, "Lümenden sızan plazma proteinleri")],
                [("Eski Skar Dokusu", False, ""), ("İnterstisyel ekstrasellüler matriks", True, "Homojenleşmiş asellüler kollajen demetleri")]
            ]
        ),
        49: make_table(
            ["Konformasyonel Bozukluk", "Hedef Organ / Doku", "Etkilenen Temel Hücre Tipi"],
            [
                [("Retinitis Pigmentosa", False, ""), ("Retina fotoreseptör tabakası", True, "Rod ve koni fotoreseptör hücreleri")],
                [("Creutzfeldt-Jakob", False, ""), ("Serebral korteks ve bazal ganglionlar", True, "Merkezi sinir sistemi nöronları")],
                [("Alfa-1 Antitripsin", False, ""), ("Karaciğer lobülleri ve akciğer alveolleri", True, "Hepatositler ve alveol septumu")]
            ]
        ),
        69: make_table(
            ["Deri Pigment Anomalisi", "Melanosit Sayısı Durumu", "Klinik Morfoloji"],
            [
                [("Efelid (Çil)", False, ""), ("Normal melanosit sayısı (üretim artışı)", True, "Güneşte koyulaşan minik pigmente lekeler")],
                [("Vitiligo", False, ""), ("Melanositler tamamen yok olmuştur", True, "Otoimmün tebeşir beyazı keskin maküller")],
                [("Albinizm", False, ""), ("Normal melanosit sayısı (tirozinaz eksik)", True, "Tüm vücutta yaygın renksizlik")]
            ]
        ),
        79: make_table(
            ["Hemosideroz Formu", "Demir Birikim Alanı", "Organ Fonksiyon Bozukluğu"],
            [
                [("Lokal Hemosideroz", False, ""), ("Eski hematom alanı makrofajları", True, "Yoktur (tamamen zararsız)")],
                [("Sistemik Hemosideroz", False, ""), ("Dalak, karaciğer Kupffer hücreleri ve kemik iliği", True, "Erken evrede organ hasarı yapmaz")],
                [("Hemokromatoz", False, ""), ("Hepatositler, kalp miyositleri, pankreas adacıkları", True, "Ağır parankimal siroz ve kalp yetmezliği")]
            ]
        ),
        89: make_table(
            ["Psammom Cisimciği Neoplazisi", "Histolojik Tümör Deseni", "Kalsifikasyon Niteliği"],
            [
                [("Papiller Tiroid Kanseri", False, ""), ("Papiller yapılar ve Orphan Annie nükleusları", True, "Konsantrik lameller mikroküreler")],
                [("Seröz Over Kanseri", False, ""), ("Kistik papiller over malignitesi", True, "Tümör papillasında distrofik çökelti")],
                [("Menenjiyom", False, ""), ("Girdapsı meningotelyal hücre yuvaları", True, "Dura mater ilişkili distrofik kalsifikasyon")]
            ]
        )
    }
