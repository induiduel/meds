"""
Section 9: Besin Algılama Yolakları: IGF-1, mTOR, Sirtuinler ve Kalori Kısıtlaması (Slayt 81 - 90)
"""
from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-08-s81",
        "title": "Hücresel Besin Algılama: Büyüme ve Onarım Dengesi",
        "subtitle": "Hücrenin besin bolluğunda anabolizmayı, kıtlıkta ise DNA bakımı ve otofajiyi seçmesi",
        "badge": "Metabolik Biyoloji",
        "badgeColor": "amber",
        "coreContent": {
            "text": (
                "Hücreler çevresel besin ve enerji düzeyini son derece hassas moleküler sensörlerle izler.\n\n"
                "İki zıt metabolik program:\n"
                "1. **Besin Bolluğu (Anabolik Program):** Yüksek glukoz ve aminoasit varlığında **IGF-1 ve mTOR** uyarılır; "
                "hücre büyür, protein sentezler ve bölünür (hücresel onarım arka plana atılır -> yaşlanma hızlanır).\n"
                "2. **Besin Kıtlığı (Bakım/Onarım Programı):** Düşük kalori koşullarında **AMPK ve Sirtuinler** aktive olur; "
                "büyüme durdurulur, tüm enerji ==DNA onarımı, mitofaji ve otofajiye== tahsis edilir (yaşlanma yavaşlar)."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Besin kıtlığı koşullarında aktive olarak hücreyi bakım ve otofaji programına geçiren sensörler AMPK ve Sirtuinler olarak bilinir.",
                "AMPK ve Sirtuinler",
                "Enerji düşüklüğünü algılayan koruyucu moleküler sensörler"
            ),
            make_active_recall(
                "Besin bolluğu ve aşırı kalori alımı hücre düzeyinde yaşlanmayı neden hızlandırır?",
                "Sürekli IGF-1 ve mTOR aktivasyonu yaratarak otofajiyi ve hücresel temizliği baskılar; ayrıca mitokondriyal elektron yükünü ve ROS üretimini artırarak hasarı katlar."
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-08-s82",
        "title": "İnsülin ve IGF-1 Sinyal Yolağı (IIS): Yaşlanmanın Gaz Pedalı",
        "subtitle": "Büyüme hormonunun yaşlanma üzerindeki evrimsel baskısı",
        "badge": "Endokrin Patoloji",
        "badgeColor": "red",
        "coreContent": {
            "text": (
                "İnsülin benzeri büyüme faktörü-1 (**IGF-1**), karaciğerde büyüme hormonu (GH) etkisiyle sentezlenir.\n\n"
                "Solucanlardan (C. elegans) farelere kadar yapılan genetik çalışmalarda, **IGF-1 reseptörü baskılanmış mutant canlıların "
                "normalden 2 kat daha uzun yaşadığı** kanıtlanmıştır.\n\n"
                "Sürekli yüksek IGF-1 sinyali FOXO transkripsiyon faktörlerini inaktive eder; antioksidan enzim ve DNA onarım genlerinin çalışmasını engeller.\n\n"
                "> IGF-1 eksikliği olan cüce fareler (Laron cüceliği benzeri) olağanüstü uzun yaşar ve kansere yakalanmazlar."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Deneysel hayvan modellerinde baskılandığında yaşam süresini en belirgin uzatan büyüme yolağı IGF-1 yolağıdır.",
                "IGF-1",
                "İnsülin benzeri büyüme faktörü-1 kısaltması"
            ),
            make_causal_chain(
                "Yüksek IGF-1 Sinyalinden Erken Yaşlanmaya Giden Yol",
                [
                    "1. Aşırı Besin: Karbonhidrattan zengin diyet insülin ve IGF-1'i yükseltir.",
                    "2. Reseptör Aktivasyonu: Tirozin kinaz kaskadı ile Akt kinaz uyarılır.",
                    "3. FOXO İnhibisyonu: Akt FOXO'yu fosforilleyip çekirdek dışına sürer.",
                    "4. Savunma Çöküşü: SOD, katalaz ve DNA onarım genlerinin üretimi durur.",
                    "5. Erken Yaşlanma: Korunamayan somatik dokular hızla senesense sürüklenir."
                ]
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-08-s83",
        "title": "mTOR: Protein Sentezinin Efendisi ve Otofajinin Düşmanı",
        "subtitle": "Besin ve aminoasit fazlalığında ribozomal biyogenez ve lizozomal blokaj",
        "badge": "Kinaz Sinyali",
        "badgeColor": "purple",
        "coreContent": {
            "text": (
                "**mTOR** (Mechanistic Target of Rapamycin), hücrenin aminoasit ve enerji düzeyini algılayan serin/treonin kinazdır.\n\n"
                "Besin bol olduğunda **mTORC1** kompleksi aktive olur:\n\n"
                "- S6K ve 4E-BP1'i fosforilleyerek translasyonu ve protein sentezini kamçılar.\n"
                "- **ULK1 kompleksini baskılayarak otofajiyi tamamen durdurur**.\n\n"
                "> mTOR'un sürekli açık kalması yaşlanmanın motorudur; mTOR baskılandığında otofaji devreye girerek hücreyi çöplerinden arındırır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Aminoasit fazlalığında aktive olarak otofajiyi doğrudan bloke eden anahtar kinaz kompleksi mTORC1 kompleksidir.",
                "mTORC1",
                "Rapamisin ile inhibe edilen besin duyarlı multiprotein kinaz kompleksi"
            ),
            make_before_after(
                "Aktif mTOR Durumu ile İnhibe Edilmiş mTOR Durumu",
                "Aktif mTOR (Besin Bolluğu)",
                "Masif protein sentezi, lipid biyogenezi, hücre büyümesi ve kilitlenmiş inaktif otofaji.",
                "İnhibe mTOR (Açlık / Rapamisin)",
                "Protein sentezi durur; otofagozomlar açılır, hasarlı protein ve mitokondriler hızla sindirilir."
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-08-s84",
        "title": "Sirtuinler (SIRT1-7): NAD+ Bağımlı Genom Koruyucuları",
        "subtitle": "Histon deasetilasyonu, PGC-1alfa aktivasyonu ve epigenetik susturma",
        "badge": "Genom Koruma",
        "badgeColor": "blue",
        "coreContent": {
            "text": (
                "**Sirtuinler** (Silent Information Regulator ailesi), aktiviteleri doğrudan hücredeki ==NAD+ düzeyine== bağlı olan "
                "yedi üyeli (SIRT1 - SIRT7) deasetilaz enzim ailesidir.\n\n"
                "Açlıkta NAD+/NADH oranı yükseldiğinde **SIRT1** aktive olur:\n\n"
                "- Histonları deasetilleyerek gevşeyen kromatin alanlarını susturur (epigenetik kararlılık).\n"
                "- **p53'ü deasetilleyerek** gereksiz apoptozu engeller.\n"
                "- **PGC-1alfa'yı deasetilleyerek** mitokondriyal biyogenezi uyarır."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Sirtuin enzimlerinin hücresel fonksiyonlarını sürdürebilmesi için mutlak koenzim NAD+ molekülüdür.",
                "NAD+",
                "Hücresel enerji düşüklüğünde yükselen okside nikotinamid adenin dinükleotid"
            ),
            make_active_recall(
                "SIRT1 enziminin yaşlanmayı yavaşlatmadaki üç temel moleküler hedefi nedir?",
                "1) Histonları deasetilleyerek heterokromatin stabilitesini korur, 2) p53'ü deasetilleyerek aşırı apoptozu frenler, 3) PGC-1alfa'yı aktive ederek taze mitokondri yapımını uyarır."
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-08-s85",
        "title": "AMPK: Hücrenin Yakıt Göstergesi ve Enerji Bekçisi",
        "subtitle": "AMP/ATP oranı artışıyla tetiklenen katabolik adaptasyon ve otofaji",
        "badge": "Enerji Sensörü",
        "badgeColor": "orange",
        "coreContent": {
            "text": (
                "**AMPK** (AMP ile aktive olan protein kinaz), hücrenin birincil enerji yakıt göstergesidir.\n\n"
                "Hücrede ATP tükendiğinde **AMP/ATP oranı fırlar**; AMP allosterik olarak AMPK'yı bağlar ve fosforilasyonla aktive eder.\n\n"
                "Aktif AMPK'nın etkileri:\n"
                "- ATP tüketen anabolik yolları (lipid ve glikojen sentezi) kapatır.\n"
                "- ATP üreten katabolik yolları (yağ asidi beta-oksidasyonu ve glukoz alımı) açar.\n"
                "- **mTOR'u doğrudan inhibe eder** ve ULK1'i uyararak ==otofajiyi patlatır==."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Hücrede ATP seviyesi düşüp AMP yükseldiğinde aktive olarak otofajiyi başlatan anahtar kinaz AMPK enzimidir.",
                "AMPK",
                "AMP-activated protein kinase kısaltması"
            ),
            make_table(
                ["Metabolik Sensör", "Hücresel Uyaranı", "Yaşlanma Üzerindeki Etkisi"],
                [
                    [("mTORC1", False, ""), ("Aminoasitler ve büyüme faktörleri", False, ""), ("Yaşlanmayı hızlandırır (otofajiyi baskılar)", True, "Anabolik büyüme ekseni ve atık birikimi")],
                    [("AMPK", False, ""), ("Yüksek AMP/ATP oranı (enerji düşüşü)", False, ""), ("Yaşlanmayı yavaşlatır (otofajiyi uyarır)", True, "Enerji krizinde hücresel temizlik yanıtı")],
                    [("SIRT1", False, ""), ("Yüksek NAD+ seviyeleri (açlık/egzersiz)", False, ""), ("Yaşlanmayı yavaşlatır (DNA tamirini destekler)", True, "Deasetilaz yoluyla genom stabilizasyonu")]
                ]
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-08-s86",
        "title": "Kalori Kısıtlaması (Caloric Restriction): Evrensel Uzun Ömür",
        "subtitle": "Malnütrisyon olmaksızın kalori alımının %30 azaltılmasının biyolojik mucizesi",
        "badge": "Kanıtlanmış Müdahale",
        "badgeColor": "emerald",
        "coreContent": {
            "text": (
                "**Kalori kısıtlaması (CR)**, temel vitamin ve mineraller eksiksiz verilerek günlük kalori alımının %30-40 azaltılmasıdır.\n\n"
                "Mayadan iplik kurduna, sinekten fareye ve primatlara kadar test edilen **istisnasız tüm türlerde yaşam süresini %30-50 uzatan** "
                "yegane kanıtlanmış non-genetik müdahaledir.\n\n"
                "Sadece ömrü uzatmakla kalmaz; kanser, diyabet, katarakt ve nörodejenerasyon insidansını yarı yarıya düşürür."
            )
        },
        "interactiveElements": [
            make_cloze(
                "Yetersiz beslenme olmadan kalori alımının azaltılarak tüm türlerde ömrün uzatılmasına kalori kısıtlaması denir.",
                "kalori kısıtlaması",
                "Caloric restriction teriminin Türkçe karşılığı"
            ),
            make_active_recall(
                "Kalori kısıtlaması (CR) ile açlık (starvation/malnütrisyon) arasındaki temel fark nedir?",
                "Kalori kısıtlamasında esansiyel vitamin, mineral ve mikrobesinler eksiksiz verilirken sadece enerji (kalori) kısıtlanır; açlıkta ise vücut yapısal elemanlarını kaybederek kaşeksiye girer."
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-08-s87",
        "title": "Kalori Kısıtlamasının Moleküler Mekanizması",
        "subtitle": "IGF-1 ve mTOR düşüşü, SIRT1 ve AMPK aktivasyonu, otofaji patlaması",
        "badge": "Moleküler Ağ",
        "badgeColor": "cyan",
        "coreContent": {
            "text": (
                "Kalori kısıtlaması hücrenin tüm besin sensörlerini aynı anda senkronize eder:\n\n"
                "1. **IGF-1 ve İnsülin Düşer:** FOXO serbest kalarak antioksidan savunmayı artırır.\n"
                "2. **mTORC1 Baskılanır:** Gereksiz protein translasyonu durur, ER yükü hafifler.\n"
                "3. **AMPK ve SIRT1 Tavan Yapar:** PGC-1alfa ile taze mitokondriler üretilir.\n"
                "4. **Otofaji Zirve Yapar:** Hücre birikmiş toksik protein agregatlarını ve hasarlı organelleri yakarak enerjiye çevirir."
            )
        },
        "interactiveElements": [
            make_causal_chain(
                "Kalori Kısıtlamasından Yaşam Süresi Artışına",
                [
                    "1. Diyet Kısıtlaması: Kalori alımı dengeli olarak %30 azaltılır.",
                    "2. Sensör Kayması: İnsülin/mTOR düşer, NAD+/AMPK fırlar.",
                    "3. Otofaji Uyarımı: Lizozomal sindirim hücre içi atıkları temizler.",
                    "4. Mitokondri Yenilenmesi: Oksidatif fosforilasyon verimi artıp kaçaklar azalır.",
                    "5. Fenotipik Gençleşme: DNA hasarı geriler ve organizma ömrü belirgin uzar."
                ]
            ),
            make_cloze(
                "Kalori kısıtlaması sırasında lizozomal sindirimi zirveye taşıyarak hücreyi temizleyen temel süreç otofaji sürecidir.",
                "otofaji",
                "Hücrenin kendi hasarlı parçalarını yutarak yenilenmesi"
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-08-s88",
        "title": "Kalori Kısıtlama Mimetikleri: Rapamisin, Metformin ve Resveratrol",
        "subtitle": "Diyet yapmadan kalori kısıtlamasının moleküler faydalarını taklit eden ilaçlar",
        "badge": "Farmakoloji",
        "badgeColor": "rose",
        "coreContent": {
            "text": (
                "İnsanların ömür boyu %30 kalori kısıtlaması uygulaması pratik olarak çok zordur; bu nedenle **mimetik ilaçlar** geliştirilmektedir:\n\n"
                "- **Rapamisin (Sirolimus):** mTORC1'i doğrudan ve selektif olarak inhibe eder; memeli deneylerinde ömrü en tutarlı uzatan moleküldür.\n"
                "- **Metformin:** Kompleks I'i hafif inhibe ederek AMPK'yı aktive eder; diyabetiklerde kardiyovasküler mortaliteyi ve kanseri azaltır.\n"
                "- **Resveratrol:** Kırmızı üzüm kabuğunda bulunan, SIRT1'i allosterik olarak uyaran doğal bir polifenoldür."
            )
        },
        "interactiveElements": [
            make_table(
                ["İlaç / Molekül", "Temel Moleküler Hedefi", "Yaşlanma Karşıtı Etki Mekanizması"],
                [
                    [("Rapamisin", False, ""), ("mTORC1 İnhibisyonu", False, ""), ("Otofajiyi tetikleme ve protein sentezini yavaşlatma", True, "Anabolizmayı frenleyip organel temizliğini açma")],
                    [("Metformin", False, ""), ("AMPK Aktivasyonu", False, ""), ("İnsülin duyarlılığı ve mitokondri koruması", True, "Glukoz dengesi ve organel fonksiyonu")],
                    [("Resveratrol", False, ""), ("SIRT1 Aktivasyonu", False, ""), ("NAD+ deasetilaz üzerinden DNA onarımı", True, "Polifenolik ömür uzatıcı yolak")]
                ]
            ),
            make_cloze(
                "mTORC1 kompleksini doğrudan bloke ederek deneysel hayvan modellerinde ömrü uzatan immünsüpresif ilaç Rapamisin ilacıdır.",
                "Rapamisin",
                "Sirolimus adıyla da bilinen bakteriyel makrolid bileşiği"
            )
        ]
    })

    # Slide 89 (CHECKPOINT 9)
    slides.append({
        "id": "k1-08-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Besin Algılama, mTOR, Sirtuinler ve Kalori Kısıtlaması",
        "subtitle": "Bölüm 9 IIS, mTOR, AMPK, SIRT1, Kalori Kısıtlaması ve Mimetikler",
        "badge": "Checkpoint 9",
        "badgeColor": "teal",
        "isCheckpoint": True,
        "checkpointNumber": 9,
        "coreContent": {
            "text": (
                "Dokuzuncu kontrol noktasında metabolik yaşlanma mekanizmalarını toparlıyoruz:\n\n"
                "1. **Büyüme vs Onarım:** Besin bolluğu (IGF-1/mTOR) yaşlandırır; besin kıtlığı (AMPK/SIRT1) gençleştirir.\n"
                "2. **mTOR:** Protein sentezini uyarır, otofajiyi kilitler; rapamisin ile baskılanabilir.\n"
                "3. **Sirtuinler:** NAD+ bağımlı deasetilazlar; kromatini susturur, PGC-1alfa'yı açar.\n"
                "4. **AMPK:** Düşük ATP / yüksek AMP ile aktive olan hücresel yakıt bekçisi.\n"
                "5. **Kalori Kısıtlaması:** Tüm canlı türlerinde ömrü uzattığı kanıtlanmış yegane fizyolojik müdahaledir."
            )
        },
        "interactiveElements": [
            make_micro_quiz(
                "Aşağıdaki sinyal moleküllerinden hangisinin aktivitesinin KISMEN BASKILANMASI deneysel modellerde yaşam süresini uzatmaktadır?",
                {
                    "A": "AMPK",
                    "B": "SIRT1",
                    "C": "mTOR",
                    "D": "SOD2",
                    "E": "Katalaz"
                },
                "C",
                {
                    "A": "AMPK aktivasyonu ömrü uzatır (baskılanması değil).",
                    "B": "SIRT1 aktivasyonu ömrü uzatır.",
                    "C": "Doğru cevap C'dir: mTOR büyüme sinyalidir; kısmen baskılandığında hücre onarım ve otofajiye geçerek ömrü uzatır.",
                    "D": "SOD2 antioksidandır, baskılanması hasar yapar.",
                    "E": "Katalaz koruyucudur."
                }
            ),
            make_active_recall(
                "Kalori kısıtlamasının hayvan modellerinde ömrü uzatırken aynı zamanda kanser insidansını dramatik düşürmesinin temel nedeni nedir?",
                "Hücre çoğalma hızını (mitoz) ve IGF-1/mTOR büyüme sinyallerini azaltması, DNA onarım kapasitesini artırması ve mutasyon birikimini asgariye indirmesidir."
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-08-s90",
        "title": "İnsanda Kalori Kısıtlaması ve Geleceğin Gerontolojisi",
        "subtitle": "CALERIE çalışmaları, aralıklı oruç (Intermittent Fasting) ve klinik gerçekler",
        "badge": "Klinik Geriatri",
        "badgeColor": "slate",
        "coreContent": {
            "text": (
                "İnsanlarda yapılan **CALERIE** klinik araştırmalarında, %12-15 kalori kısıtlamasının bile kan basıncını düşürdüğü, "
                "insülin direncini yok ettiği ve sistemik inflamasyon belirteçlerini (hs-CRP) gerilettiği gösterilmiştir.\n\n"
                "Aşırı katı kalori kısıtlamasının hipotermi, kemik mineral yoğunluğunda azalma ve libido kaybı gibi yan etkileri nedeniyle günümüzde "
                "==Aralıklı Oruç (Intermittent Fasting)== ve kalori kısıtlama mimetikleri (Metformin) klinik odak noktası haline gelmiştir."
            )
        },
        "interactiveElements": [
            make_cloze(
                "İnsanda kalori kısıtlamasının metabolik biyobelirteçlerini test eden en kapsamlı klinik çalışma CALERIE çalışmasıdır.",
                "CALERIE",
                "Comprehensive Assessment of Long-term Effects of Reducing Intake of Energy kısaltması"
            ),
            make_branching_logic(
                "55 yaşında prediyabetik ve hafif obez bir hasta metabolik yaşlanmayı yavaşlatmak için bilimsel öneri istiyor. Hangi strateji en güvenilir ve kanıta dayalıdır?",
                [
                    {"text": "Açlık grevine girerek günde 200 kalori ile yaşamak", "isCorrect": False, "feedback": "Ağır malnütrisyon, kardiyak aritmi ve kas erimesi yapar."},
                    {"text": "Akdeniz tipi dengeli beslenme, aralıklı oruç yaklaşımı ve düzenli aerobik egzersiz ile insülin/mTOR eksenini sakinleştirmek", "isCorrect": True, "feedback": "Kusursuz klinik rehberlik! Dengeli kalori kontrolü ve egzersiz insanda AMPK/SIRT1'i aktive eden en güvenli yoldur."},
                    {"text": "Kontrolsüz steroid ve testosteron hormonları enjekte etmek", "isCorrect": False, "feedback": "Kardiyovasküler mortaliteyi artırır."}
                ]
            )
        ]
    })

    return slides
