# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_7_slides():
    slides = []

    # Slide 61
    slides.append({
        "id": "k1-16-s61",
        "title": "Organa Özgü Ödem Morfolojisine Giriş: Dokusal Değişiklikler",
        "content": "Ödem vücudun herhangi bir dokusunda ortaya çıkabilmekle birlikte, klinik pratikte en sık ve en tehlikeli tabloları deri altı dokusu, akciğer ve beyinde sergiler:\n\n- **Makroskobik Özellikler:**\n  - Ödemli organlar belirgin şekilde şişkin, soluk ve normal ağırlığının iki ila üç katına çıkmış haldedir.\n  - Bıçakla kesildiğinde kesit yüzeyi ıslaktır ve berrak veya hafif pembe seröz sıvı sızar.\n- **Mikroskopik Morfoloji:**\n  - Ekstrasellüler matriks (ECM) lifleri aşırı sıvı birikimi nedeniyle birbirinden uzaklaşır (aralıkların açılması).\n  - Hücreler arasında soluk eozinofilik (pembe), amorf seröz boyanma gözlenir.\n  - İnce kollajen demetleri gevşer, kapillerler ve lenfatikler sıvı basıncıyla dilate görülür.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Parankim vs Ödemli Doku Histolojisi",
                "Normal Doku Histolojisi",
                "Hücreler ve kollajen lifleri birbiriyle sıkı ve düzenli temas halindedir; interstisyumda boşluk yoktur.",
                "Ödemli Doku Histolojisi",
                "Hücreler arası aralıklar genişlemiştir; soluk pembe seröz sıvı lifleri ayırır ve doku şiştir."
            ),
            make_cloze(
                "Histopatolojik kesitlerde ödem sıvısı ekstrasellüler aralıkta soluk eozinofilik boyanan amorf bir birikim olarak izlenir.",
                "eozinofilik",
                "Hematoksilen-eozin boyamasında pembe renkli boyanma özelliği"
            )
        ]
    })

    # Slide 62
    slides.append({
        "id": "k1-16-s62",
        "title": "Akciğer Ödeminin Etiyolojisi: Hemodinamik vs Mikrovasküler Hasar",
        "content": "Akciğer ödemi, gaz değişimini felç eden acil bir kardiyopulmoner tablodur (Sınav Spotu):\n\n- **1. Hemodinamik (Kardiyojenik) Akciğer Ödemi:**\n  - **En Sık Neden:** Sol ventrikül yetmezliğidir (akut MI, dekompanse hipertansif kalp hastalığı).\n  - Pulmoner venöz hipertansiyon kapiller hidrostatik basıncı (normalde ~8-10 mmHg) onkotik basıncın üzerine (>25-30 mmHg) çıkarır.\n  - Diğer hemodinamik nedenler: Böbrek yetmezliğine bağlı hacim yüklenmesi veya hipoalbüminemi.\n- **2. Mikrovasküler Hasara Bağlı Akciğer Ödemi (Non-Kardiyojenik / ARDS):**\n  - Alveol kapiller endotelinin veya alveolar epitelin doğrudan hasarlanmasıdır (akut respiratuar distres sendromu - ARDS).\n  - Nedenler: Ağır pnömoni, sepsis, toksik gaz inhalasyonu, mide içeriğinin aspirasyonu.\n  - Burada hidrostatik basınç normaldir; ancak vasküler geçirgenlik aşırı arttığı için alveollere protein ve fibrin zengini eksuda dolar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Akciğer Ödemi Tipi", "Başlıca Neden", "Kapiller Hidrostatik Basınç", "Sıvının Karakteri"],
                [
                    ["Hemodinamik (Kardiyojenik)", "Sol ventrikül yetmezliği, mitral darlığı", "Aşırı yüksek (>25 mmHg)", "Transuda (düşük proteinli seröz sıvı)"],
                    ["Geçirgenlik Artışı (ARDS)", "Sepsis, ağır pnömoni, aspirasyon", "Normal veya düşük", "Eksuda (yüksek proteinli, fibröz, hücresel)"]
                ]
            ),
            make_quiz(
                "Akut miyokard enfarktüsü sonrası aniden akciğer ödemi gelişen bir hastada bu tablonun primer patofizyolojik nedeni hangisidir?",
                [
                    {"key": "A", "text": "Sol ventrikül pompasının çökmesi sonucu pulmoner kapiller hidrostatik basıncın aşırı yükselmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sol kalp yetmezliğinde pulmoner venöz göllenme hidrostatik basıncı onkotik basıncın üzerine çıkararak alveolleri transuda ile doldurur."},
                    {"key": "B", "text": "Hastada akciğer tüberkülozu başlaması", "isCorrect": False, "explanation": "Tüberküloz kronik granülomatöz hastalıktır."},
                    {"key": "C", "text": "Trakeanın yabancı cisimle tam tıkanması", "isCorrect": False, "explanation": "Yabancı cisim atelektazi yapar, primer pulmoner hidrostatik ödem mekanizması değildir."},
                    {"key": "D", "text": "Karaciğerin aşırı safra salgılaması", "isCorrect": False, "explanation": "Safra salgısı akciğer ödemi yapmaz."}
                ]
            )
        ]
    })

    # Slide 63
    slides.append({
        "id": "k1-16-s63",
        "title": "Akciğer Ödeminin Makroskobik ve Mikroskobik Bulguları",
        "content": "Akciğer ödemi otopsi ve cerrahi patolojide çok tipik tanısal bulgular verir (Sınav Spotu):\n\n- **Makroskopi:**\n  - Normalde 300-400 gram olan akciğer ağırlığı **2-3 katına çıkar (bazen 1000 gramı aşar)**.\n  - Akciğerler ağır, ıslak ve elastikiyetini yitirmiştir.\n  - Kesit yüzeyine hafifçe bastırıldığında veya bronşlar kesildiğinde lümenden bol miktarda **köpüklü, seröz veya hafif kanlı (pembe köpük) sıvı** fışkırır.\n  - Sıvının köpüklü olması havanın seröz transudayla çalkalanmasından kaynaklanır.\n- **Mikroskopi:**\n  - Başlangıçta sıvı alveoler septalarda toplanır (interstisyel ödem).\n  - Basınç arttıkça sıvı alveol epiteli aralıklarından hava boşluklarına dökülür (intraalveoler ödem).\n  - Alveol lümenleri soluk pembe boyanan homojen proteinöz sıvı materyal ile tamamen dolar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Akciğer Parankimi vs Ağır Akciğer Ödemi",
                "Normal Akciğer",
                "Ağırlığı 350-400 gramdır; alveol lümenleri temiz hava doludur; kesitte köpük çıkmaz.",
                "Ağır Akciğer Ödemi",
                "Ağırlığı 1000 gramı aşabilir; alveoller pembe transuda ile doludur; kesitten pembe köpüklü sıvı akar."
            ),
            make_cloze(
                "Akciğer ödeminde kesit yüzünden ve ana bronşlardan dışarı sızan hava ile karışmış karakteristik sıvı köpüklü pembe sıvıdır.",
                "köpüklü",
                "Hava ile seröz sıvının karışması sonucu oluşan fiziksel görünüm"
            )
        ]
    })

    # Slide 64
    slides.append({
        "id": "k1-16-s64",
        "title": "Akciğer Ödeminin Klinik Önemi: Hipoksi ve Enfeksiyon Riski",
        "content": "Alveollerin hava yerine sıvıyla dolması hayatı dakikalar içinde tehdit eden zincirleme olayları başlatır:\n\n- **1. Gaz Değişiminin Durması:** Sıvıyla dolan alveollerde oksijen kapiller kana difüze olamaz. Hastada ağır hipoksemi ve hiperkapni gelişir.\n- **2. Şiddetli Dispne ve Boğulma Hissi:** Hasta nefes alamaz; oturur pozisyonda dik durmaya çalışır (ortopne); dudaklarında ve tırnaklarında santral siyanoz belirir.\n- **3. Raller (Steteskop Bulgusu):** Akciğer bazallerinde havanın sıvıyla köpürdüğü 'yaş raller' (krepitan raller) dinlenir.\n- **4. Sekonder Enfeksiyon Riski (Hipostatik Pnömoni):**\n  - Alveollerde biriken seröz sıvı bakteriler için mükemmel bir besi yeridir.\n  - Akciğer ödemi ve staz alanları hızla sekonder bakteriyel pnömoniye zemin hazırlar ve hastalar sıklıkla enfeksiyöz komplikasyonlarla kaybedilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_chain(
                "Akciğer Ödeminde Klinik Kötüleşme Basamakları",
                [
                    "1. Sıvı Alveollere Taşar: Transuda hava boşluklarını işgal eder.",
                    "2. Oksijen Difüzyonu Durur: Alveolokapiller membran geçirgenliği yetersizleşir.",
                    "3. Ağır Hipoksemi ve Siyanoz: Hasta hava açlığı yaşar ve pembe köpüklü balgam çıkarır.",
                    "4. Hipostatik Pnömoni: Alveoler sıvı bakteriyel enfeksiyon odağına dönüşür."
                ]
            ),
            make_quiz(
                "Kronik kalp yetmezliği veya uzun süreli akciğer ödemi olan bir hastada akciğer bazallerinde bakteriyel enfeksiyon gelişmesini kolaylaştıran temel faktör nedir?",
                [
                    {"key": "A", "text": "Alveollerde göllenen proteinli seröz sıvının bakteriler için ideal bir kültür ortamı oluşturması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Alveol içi durgun ödem sıvısı bakteri kolonizasyonuna ve hipostatik pnömoniye zemin hazırlar."},
                    {"key": "B", "text": "Akciğerin aşırı miktarda antibiyotik üretmesi", "isCorrect": False, "explanation": "Akciğer antibiyotik üretmez."},
                    {"key": "C", "text": "Hastanın sürekli spor yapması", "isCorrect": False, "explanation": "Ağır ödemli hasta egzersiz yapamaz."},
                    {"key": "D", "text": "Alveollerin tamamen kıkırdak dokuya dönüşmesi", "isCorrect": False, "explanation": "Alveoller kıkırdak dokuya dönüşmez."}
                ]
            )
        ]
    })

    # Slide 65
    slides.append({
        "id": "k1-16-s65",
        "title": "Beyin Ödemi Mekanizmaları: Vazojenik vs Sitotoksik Ödem",
        "content": "Beyin, kafatası gibi rijit ve esnemeyen kapalı kemik bir kutu içinde yer aldığı için ödemi en yıkıcı seyreden organdır (Sınav Spotu):\n\n- **1. Vazojenik Ödem (Ekstrasellüler Sıvı Artışı):**\n  - **Mekanizma:** Kan-beyin bariyerinin (astrosit ayakları ve sıkı endotel kavşakları) yapısal olarak bozulmasıdır.\n  - Vasküler geçirgenlik artar; protein ve sıvı damar dışına, beyin hücrelerinin arasındaki ekstrasellüler aralığa sızar.\n  - Nedenler: Beyin tümörleri (metastaz veya gliom), abseler, travma veya lokal enflamasyon.\n- **2. Sitotoksik Ödem (İntrasellüler Sıvı Artışı):**\n  - **Mekanizma:** Kan-beyin bariyeri başlangıçta intakt olabilir; ancak nöron ve glial hücrelerin (astrositlerin) kendi hücre zarı metabolizması bozulur.\n  - İskemi veya hipoksi sonucu Na+/K+ ATPaz pompası durur; hücre içine sodyum ve su dolarak hücreler balon gibi şişer.\n  - Nedenler: Akut iskemik inme (enfarktüs) veya toksik/metabolik hasarlar.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Ödem Tipi", "Sıvının Biriktiği Kompartman", "Temel Patolojik Bozukluk", "Tipik Klinik Neden"],
                [
                    ["Vazojenik Ödem", "Hücreler arası (ekstrasellüler) aralık", "Kan-beyin bariyerinin yıkılması ve artmış geçirgenlik", "Beyin tümörleri, abse, kontüzyon travması"],
                    ["Sitotoksik Ödem", "Hücrelerin kendi içi (intrasellüler)", "Hücre zarı iyon pompası yetmezliği ve hücresel şişme", "Akut iskemik inme, global serebral hipoksi"]
                ]
            ),
            make_quiz(
                "Akut iskemik inme geçiren bir hastada hipoksiye bağlı olarak nöronların zarlarındaki Na+/K+ pompasının çökmesi ve hücrelerin şişmesiyle karakterize beyin ödemi tipi hangisidir?",
                [
                    {"key": "A", "text": "Vazojenik ödem", "isCorrect": False, "explanation": "Vazojenik ödem kan-beyin bariyeri hasarı ve ekstrasellüler kaçaktır."},
                    {"key": "B", "text": "Sitotoksik ödem", "isCorrect": True, "explanation": "Doğru cevap B'dir: Sitotoksik ödem iskemik pompa çöküşüyle hücre içi sıvının artmasıdır."},
                    {"key": "C", "text": "İnterstisyel hidrosefali", "isCorrect": False, "explanation": "BOS dolaşım bozukluğudur."},
                    {"key": "D", "text": "Miksödem", "isCorrect": False, "explanation": "Hipotiroidiye bağlı glikozaminoglikan birikimidir."}
                ]
            )
        ]
    })

    # Slide 66
    slides.append({
        "id": "k1-16-s66",
        "title": "Beyin Ödeminin Morfolojisi: Girus ve Sulkus Değişiklikleri",
        "content": "Beyin parankiminde sıvı birikimi kafatası içinde hacim genişlemesi yaratır:\n\n- **Monro-Kellie Doktrini:** Kafatası esnemez. Beyin kütlesi, beyin-omurilik sıvısı (BOS) ve kan hacmi sabittir; ödemle beyin şişince BOS ve venöz kan boşaltılmaya çalışılır; kapasite dolunca kafa içi basınç (KİBA) fırlar.\n- **Makroskobik Beyin Morfolojisi (Sınav Spotu):**\n  - Beyin şişkin, ağır ve gergindir; kesit yüzeyi parlar.\n  - Kafatası kemiğine dayanan **giruslar basık ve düzleşmiştir (flattening)**.\n  - Giruslar arasındaki **sulkuslar aşırı derecede daralmış veya tamamen silinmiştir**.\n  - Beyin ventrikülleri (lateral ventriküller) çevreleyen ödemli parankimin dıştan baskısıyla **yarık şeklinde daralmış ve sıkışmıştır**.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Beyin Morfolojisi vs Ağır Beyin Ödemi",
                "Normal Beyin",
                "Giruslar belirgindir, sulkuslar açık ve derindir; lateral ventriküller simetrik ve açıktır.",
                "Ödemli Beyin",
                "Giruslar düzleşmiştir, sulkuslar tamamen silinmiştir; ventriküller komprese ve yarıktır."
            ),
            make_cloze(
                "Beyin ödeminde kafatası içi basınç artışı sonucu serebral giruslar düzleşir ve aralarındaki sulkuslar silinerek daralır.",
                "sulkuslar",
                "Beyin kıvrımları arasındaki anatomik oluklar"
            )
        ]
    })

    # Slide 67
    slides.append({
        "id": "k1-16-s67",
        "title": "Kafa İçi Basınç Artışı ve Ölümcül Beyin Herniasyonları",
        "content": "Beyin ödemi kontrol altına alınamazsa parankim kafatası içindeki anatomik deliklerden dışarı fıtıklaşır (herniasyon - Sınav Spotu):\n\n- **1. Subfalsin (Singulat) Herniasyon:** Singulat girusun faks serebrinin altından karşı tarafa kayması (anterior serebral arteri sıkıştırabilir).\n- **2. Uncal (Transtentoryal) Herniasyon:**\n  - Temporal lobun unkus kısmının tentorium serebelli kenarından aşağıya kaymasıdır.\n  - 3. Kranial siniri (okülomotor) sıkar $\\to$ ipsilateral pupil dilatasyonu (ışık refleksi kaybı).\n  - Posterior serebral arteri sıkar $\\to$ oksipital lob enfarktüsü.\n- **3. Tonsiller Herniasyon (Foramen Magnumdan Fıtıklaşma - En Ölümcül):**\n  - Serebellar tonsillerin foramen magnumdan aşağıya, omurilik kanalına doğru itilmesidir.\n  - **Ölüm Nedeni:** Beyin sapını (medulla oblangata) sıkıştırır; buradaki **solunum ve kardiyak merkezler basıya uğrar ve hasta dakikalar içinde arrest olarak ölür**.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Herniasyon Tipi", "Fıtıklaşan Beyin Bölgesi", "Basıya Uğrayan Yapı", "Kritik Klinik Belirti"],
                [
                    ["Subfalsin (Singulat)", "Singulat girus faks altından kayar", "Anterior serebral arter (ACA)", "Karşı bacakta motor/duyu kaybı"],
                    ["Uncal (Transtentoryal)", "Temporal unkus tentoriumdan aşağı iner", "Okülomotor sinir (CN III) ve PCA", "Aynı tarafta midriyazis (sabit dilate pupil)"],
                    ["Tonsiller (Foramen Magnum)", "Serebellar tonsiller foramen magnuma kayar", "Medulla oblangata (beyin sapı)", "Solunum/dolaşım durması ve ani ölüm"]
                ]
            ),
            make_quiz(
                "Ağır beyin ödeminde serebellar tonsillerin foramen magnumdan aşağıya fıtıklaşması sonucu hastanın dakikalar içinde ölümüne yol açan temel patoloji nedir?",
                [
                    {"key": "A", "text": "Beyin sapındaki (medulla oblangata) solunum ve kardiyak merkezlerin sıkışarak felç olması", "isCorrect": True, "explanation": "Doğru cevap A'dır: Tonsiller herniasyon beyin sapını sıkıştırarak solunum ve dolaşım merkezlerini durdurur ve ölüme yol açar."},
                    {"key": "B", "text": "Gözyaşı bezlerinin kuruyarak körlük yapması", "isCorrect": False, "explanation": "Gözyaşı kuruluğu ölümcül beyin sapı hasarıyla ilişkisizdir."},
                    {"key": "C", "text": "Mide duvarında ülser delinmesi", "isCorrect": False, "explanation": "Cushing ülseri görülebilir ama herniasyonun doğrudan ölüm mekanizması beyin sapı kompresyonudur."},
                    {"key": "D", "text": "Kafatasının aniden patlaması", "isCorrect": False, "explanation": "Yetişkinde kafatası kemikleri patlamaz."}
                ]
            )
        ]
    })

    # Slide 68
    slides.append({
        "id": "k1-16-s68",
        "title": "Deri Altı Ödeminin Klinik Etkileri: Doku Kırılganlığı ve Yara İyileşmesi",
        "content": "Deri altı (subkutan) ödem yalnızca kozmetik bir deformite değildir; doku fizyolojisini temelden bozar:\n\n- **1. Oksijen ve Besin Difüzyonunun Bozulması:**\n  - Kılcal damarlarla deri hücreleri arasındaki mesafe ödem sıvısıyla birkaç katına çıkar.\n  - Oksijen difüzyon mesafesi uzadığı için keratinositler ve fibroblastlar rölatif hipoksiye girer.\n- **2. Bozulmuş Yara İyileşmesi:**\n  - Ödemli dokuda cerrahi insizyonlar veya travmatik yaralar dikiş tutmaz; kollajen sentezi aksar, yara açılması (dehisens) riski çok yüksektir.\n- **3. Enfeksiyona Eğilim:**\n  - Lenfatik drenaj bozukluğu immün hücrelerin göçünü engeller; biriken seröz sıvı bakteriyel kolonizasyon için davetiyedir.\n  - Hafif bir sıyrık hızla yaygın flegmon, selülit ve deride trofik ülserlere dönüşebilir.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_slider(
                "Normal Sağlıklı Deri vs Şiddetli Ödemli Deri Altı",
                "Normal Deri Altı",
                "Kılcal damarlar hücrelere yakındır; oksijen difüzyonu hızlıdır, cerrahi yaralar kolayca kaynar.",
                "Şiddetli Ödemli Deri Altı",
                "Geniş sıvı göllenmesi difüzyonu engeller; doku gergindir, yara iyileşmesi bozulur ve ülser açılır."
            ),
            make_cloze(
                "Şiddetli deri altı ödeminde kapiller damar ile hücreler arasındaki difüzyon mesafesi uzadığı için yara iyileşmesi belirgin biçimde bozulur.",
                "yara iyileşmesi",
                "Doku tamir sürecinin aksamasını ifade eden klinik kavram"
            )
        ]
    })

    # Slide 69 - CHECKPOINT 7
    slides.append({
        "id": "k1-16-s69",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Organa Özgü Ödem ve Efüzyonlar",
        "content": "Bu checkpointte akciğer, beyin ve deri altı ödeminin morfolojik ve klinik sonuçlarını özetliyoruz:\n\n- **Akciğer Ödemi:** En sık sol ventrikül yetmezliğinde; akciğer ağırlığı 2-3 kat artar; kesitte köpüklü pembe sıvı fışkırır; alveoller transudayla dolar $\\to$ ağır hipoksi ve hipostatik pnömoni.\n- **Beyin Ödemi Tipleri:** Vazojenik (kan-beyin bariyeri hasarı, ekstrasellüler sıvı) vs Sitotoksik (iskemik hücre şişmesi, intrasellüler sıvı).\n- **Beyin Morfolojisi:** Giruslar düzleşir, sulkuslar silinir, lateral ventriküller yarık şeklinde daralır.\n- **Ölümcül Herniasyon:** Tonsiller herniasyonda serebellar tonsiller foramen magnumdan fıtıklaşır; beyin sapını ezerek solunum/kardiyak arrestle öldürür.\n- **Deri Altı Ödemi:** Oksijen difüzyonunu bozar, yara iyileşmesini geciktirir ve selülit/ülser riskini artırır.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_table(
                ["Organ", "Temel Morfolojik Özellik", "Kritik Klinik Komplikasyon"],
                [
                    ["Akciğer", "Ağırlık 2-3 kat artışı, pembe köpüklü sıvı, alveoler transuda", "Boğulma hissi (dispne), hipoksemi, hipostatik pnömoni"],
                    ["Beyin", "Düzleşmiş giruslar, silinmiş sulkuslar, daralmış ventriküller", "KİBA ve foramen magnumdan tonsiller herniasyonla ani ölüm"],
                    ["Deri Altı", "Gode bırakan şişlik, gergin soluk cilt, ekstrasellüler sıvı", "Bozulmuş yara iyileşmesi, dikiş açılması, selülit ve ülser"]
                ]
            ),
            make_chain(
                "Organa Özgü Ölümcül Komplikasyonlar Özeti",
                [
                    "1. Pulmoner Kaçak: Alveoler transuda difüzyonu keser $\\to$ Solunum arresti.",
                    "2. Kafatası İçi Hacim: Serebral ödem Monro-Kellie sınırını aşar $\\to$ KİBA.",
                    "3. Herniasyon Riski: Foramen magnuma doğru tonsil kayması $\\to$ Medulla ezilmesi.",
                    "4. Subkutan Doku Zafiyeti: Sıvı bariyeri enfeksiyona açar $\\to$ Trofik yara açılması."
                ]
            )
        ]
    })

    # Slide 70
    slides.append({
        "id": "k1-16-s70",
        "title": "Bölüm Özeti: Ödemden Kanama Patolojisine Geçiş",
        "content": "Bölüm 7 ile birlikte ödemin organ bazındaki histopatolojik morfolojisini ve hayati komplikasyonlarını tamamladık:\n\n- **Önemli Vurgu:** Akciğer ödemi ve beyin ödemi acil tıbbi müdahale gerektiren en kritik iki hemodinamik acildir.\n- **Sonraki Bölüm:** Bir sonraki bölümde damar dışına kan çıkışı anlamına gelen **kanama (hemoraji)** olgusunu, nedenlerini, hemorajik diyatezleri ve pıhtılaşma dengesini incelemeye başlayacağız.",
        "sourcePdf": "Kurul 1 - Ders 16: Ödem, Hiperemi, Konjesyon ve Kanama (Prof. Dr. Hikmet Keleş)",
        "elements": [
            make_recall(
                "Kafatasında serebral ödeme bağlı olarak serebellar tonsillerin aşağıya doğru kayarak beyin sapını ezdiği foramen neresidir?",
                "Foramen magnum",
                "Kafatası tabanındaki en büyük delik"
            ),
            make_quiz(
                "Akciğer ödeminde hastanın balgamında ve kesit yüzeyinde görülen sıvının köpüklü olmasının nedeni hangisidir?",
                [
                    {"key": "A", "text": "Alveollere dolan seröz transudanın solunan hava ile çalkalanıp köpürmesi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Alveollerdeki hava ve proteinli seröz sıvının mekanik karışımı köpük oluşturur."},
                    {"key": "B", "text": "Hastanın deterjan yutmuş olması", "isCorrect": False, "explanation": "Patofizyolojik pulmoner köpüğün nedeni deterjan değildir."},
                    {"key": "C", "text": "Akciğerin safra üretmeye başlaması", "isCorrect": False, "explanation": "Akciğer safra üretmez."},
                    {"key": "D", "text": "Tüm alveollerin kalsiyum gazıyla dolması", "isCorrect": False, "explanation": "Kalsiyum gaz oluşturmaz."}
                ]
            )
        ]
    })

    return slides
