# -*- coding: utf-8 -*-
from .helpers import (
    make_cloze, make_quiz, make_chain, make_branching, make_table, make_slider, make_recall
)

def get_section_9_slides():
    slides = []

    # Slide 81
    slides.append({
        "id": "k1-18-s81",
        "title": "Alma-Ata Konferansı (1978): '2000 Yılında Herkese Sağlık'",
        "content": "6-12 Eylül 1978 tarihlerinde Kazakistan'ın Alma-Ata kentinde DSÖ ve UNICEF öncülüğünde toplanan konferans, küresel halk sağlığının manifestosudur (Sınav Spotu):\n\n- **Tarihi Çağrı ve Hedef:**\n  - Dünyanın 134 ülkesinin katıldığı konferansta **'2000 Yılında Herkese Sağlık' (Health for All by the Year 2000)** hedefi ilan edildi.\n- **Kritik Paradigma Değişimi:**\n  - Sağlığın gelişmiş ülkelerdeki devasa lüks hastaneler ve pahalı biyomedikal teknolojilerle kazanılamayacağı açıkça deklare edildi.\n  - Dünya kaynaklarının silahlara ve savaşlara değil, halkın sağlığına harcanması gerektiği vurgulandı.\n- **Çözüm Anahtarı:** 'Herkese Sağlık' hedefine ulaşmanın tek geçerli yolunun **'Temel Sağlık Hizmetleri' (Primary Health Care - PHC)** yaklaşımı olduğu tüm dünya tarafından oybirliğiyle kabul edildi.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Lüks Hastane Modeli vs Alma-Ata Temel Sağlık Modeli",
                "Lüks Hastane / Teknoloji Odaklı Model",
                "Bütçenin %90'ını yutan ancak nüfusun sadece %5'ine ulaşan pahalı tedavi edici tıp.",
                "Alma-Ata Temel Sağlık Hizmetleri Modeli",
                "Halkın ayağına giden, koruyucu, ucuz, eşitlikçi ve tüm toplumu kapsayan birinci basamak sağlığı."
            ),
            make_quiz(
                "1978 yılında DSÖ ve UNICEF ortaklığıyla toplanan ve '2000 Yılında Herkese Sağlık' hedefini ilan eden tarihi uluslararası halk sağlığı konferansı nerede yapılmıştır?",
                [
                    {"key": "A", "text": "Alma-Ata (Kazakistan)", "isCorrect": True, "explanation": "Doğru cevap A'dır: 1978 Alma-Ata Konferansı Temel Sağlık Hizmetleri'nin küresel manifestosudur."},
                    {"key": "B", "text": "Cenevre", "isCorrect": False, "explanation": "DSÖ merkezidir."},
                    {"key": "C", "text": "New York", "isCorrect": False, "explanation": "BM merkezidir."},
                    {"key": "D", "text": "Paris", "isCorrect": False, "explanation": "Pasteur Enstitüsü merkezidir."}
                ]
            )
        ]
    })

    # Slide 82
    slides.append({
        "id": "k1-18-s82",
        "title": "Temel Sağlık Hizmetleri (TSH - PHC) Kavramı ve 8 Ana Bileşeni",
        "content": "Alma-Ata Bildirgesi'nde Temel Sağlık Hizmetleri, toplumun tüm bireylerine evrensel olarak ulaştırılması gereken asgari 8 zorunlu bileşenle tanımlanmıştır (Sınav Spotu):\n\n- **1. Sağlık Eğitimi:** Yaygın sağlık sorunları ve bunlardan korunma yöntemleri konusunda halkın eğitilmesi.\n- **2. Beslenme ve Gıda Güvencesi:** Yeterli ve dengeli beslenmenin sağlanması, gıda güvenliği.\n- **3. Temiz Su ve Temel Sanitasyon:** Güvenli içme suyu sağlanması ve atıkların zararsızlaştırılması.\n- **4. Ana-Çocuk Sağlığı ve Aile Planlaması:** Gebe, anne ve bebek sağlığının korunması.\n- **5. Başlıca Bulaşıcı Hastalıklara Karşı Bağışıklama:** Aşı takviminin eksiksiz uygulanması.\n- **6. Endemik Hastalıkların Önlenmesi ve Kontrolü:** Bölgeye özgü salgınların kontrolü.\n- **7. Sık Görülen Hastalık ve Yaralanmaların Uygun Tedavisi:** Temel ayaktan tedavi.\n- **8. Temel İlaçların Sağlanması:** Hayati ilaçların kesintisiz ve ucuz temini.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["TSH'nin 8 Temel Bileşeni", "Halk Sağlığı Amacı", "Uygulama Alanı"],
                [
                    ["1. Sağlık Eğitimi", "Bireylere öz sorumluluk kazandırmak", "Okullar, sağlık ocakları, kitle iletişimi"],
                    ["2. Beslenme / Gıda", "Malnütrisyon ve eksiklikleri önlemek", "Gıda denetimi ve tarım politikaları"],
                    ["3. Temiz Su / Sanitasyon", "Kolera, tifo ve ishalleri durdurmak", "Su klorlama ve kanalizasyon altyapısı"],
                    ["4. Ana-Çocuk Sağlığı", "Bebek ve anne ölümlerini sıfırlamak", "Doğum öncesi izlem, aile planlaması"],
                    ["5. Bağışıklama", "Sürü bağışıklığı oluşturmak", "Genişletilmiş Bağışıklama Programı (GBP)"],
                    ["6. Endemik Kontrol", "Yerel salgınları söndürmek", "Vektör mücadelesi ve saha sürveyansı"],
                    ["7. Temel Tedavi", "Erken tanı ve basit müdahale", "Birinci basamak sağlık ocağı polikliniği"],
                    ["8. Temel İlaçlar", "Halkın ilaca adil erişimi", "Esansiyel ilaç listeleri ve ücretsiz temin"]
                ]
            ),
            make_cloze(
                "Alma-Ata Bildirgesi'nde tanımlanan Temel Sağlık Hizmetleri yaklaşımı toplumun tümüne ulaştırılması gereken asgari sekiz temel bileşenden oluşur.",
                "sekiz",
                "Temel Sağlık Hizmetleri'nin Alma-Ata'da sayılan ana bileşen adedi"
            )
        ]
    })

    # Slide 83
    slides.append({
        "id": "k1-18-s83",
        "title": "Halk Sağlığının Temel İlkeleri - I: Sağlık Temel Bir İnsanlık Hakkıdır",
        "content": "Çağdaş halk sağlığı biliminin üzerine inşa edildiği ilk ve en sarsılmaz anayasal ilke sağlık hakkıdır (Sınav Spotu):\n\n- **1. Temel İlke: Sağlık Bir İnsanlık Hakkıdır:**\n  - Sağlık doğuştan kazanılan vazgeçilmez, devredilemez en temel haktır.\n  - Bireylerin cinsiyetine, ırkına, inancına, siyasi görüşüne veya sosyoekonomik durumuna bakılmaksızın;\n  - **Herkes ihtiyacı olduğunda ve ihtiyacı olduğu kadar sağlık hizmeti almalı, hizmete erişimde eşit şansa sahip olmalıdır.**\n- **Hukuki Dayanaklar:**\n  - T.C. Anayasası (Madde 56: 'Herkes sağlıklı ve dengeli bir çevrede yaşama hakkına sahiptir. Devlet herkesin hayatını beden ve ruh sağlığı içinde sürdürmesini sağlar').\n  - DSÖ Anayasası ve İnsan Hakları Evrensel Beyannamesi.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Piyasa Malı Sağlık vs İnsan Hakkı Sağlık",
                "Piyasa Mantığı (Ayrıcalık)",
                "Sağlık parası olanın satın alabildiği, parası olmayanın mahrum kaldığı ticari bir hizmettir.",
                "Halk Sağlığı İlkesi (Evrensel Hak)",
                "Sağlık her yurttaşın devlet güvencesindeki doğuştan gelen en kutsal anayasal hakkıdır."
            ),
            make_quiz(
                "Türkiye Cumhuriyeti Anayasası'nın 56. maddesinde ve DSÖ Anayasası'nda güvence altına alınan en temel halk sağlığı ilkesi hangisidir?",
                [
                    {"key": "A", "text": "Sağlık temel bir insanlık hakkıdır ve devredilemez", "isCorrect": True, "explanation": "Doğru cevap A'dır: Sağlığın temel bir insan hakkı olması tüm halk sağlığı sisteminin birinci ilkesidir."},
                    {"key": "B", "text": "Hastanelerin yalnızca kar amaçlı anonim şirketlerce yönetilmesi", "isCorrect": False, "explanation": "Hak temelli yaklaşıma tamamen aykırıdır."},
                    {"key": "C", "text": "Yalnızca çalışan yetişkinlerin sağlık güvencesine sahip olması", "isCorrect": False, "explanation": "Çocuk ve yaşlıları dışlayamaz."},
                    {"key": "D", "text": "Sağlık hizmetinin yalnızca büyükşehir merkezlerinde verilmesi", "isCorrect": False, "explanation": "Erişim eşitliğine aykırıdır."}
                ]
            )
        ]
    })

    # Slide 84
    slides.append({
        "id": "k1-18-s84",
        "title": "Halk Sağlığının Temel İlkeleri - II: Koruma Tedaviden Üstündür",
        "content": "Halk sağlığı felsefesinin kalbini oluşturan en pragmatik ve ahlaki ilke koruma önceliğidir (Sınav Spotu):\n\n- **2. Temel İlke: Koruma Tedaviden Üstündür:**\n  - Devletin ve sağlık sisteminin birincil görevi insanların hasta olmasını bekleyip onları tedavi etmek değil; **kişilerin hiç hasta olmamasını sağlamaktır**.\n- **Üçlü Gerekçe:**\n  1. **İnsani Açıdan:** Hiçbir tedavi hastalanmanın getirdiği acıyı, iş gücü kaybını, sakatlık riskini ve ölüm korkusunu sıfırlayamaz; en iyi tedavi hiç hastalanmamaktır.\n  2. **Ekonomik Açıdan:** Bir kişiyi aşılamak veya içme suyunu klorlamak birkaç kuruş iken; o kişi tifo veya hepatit olup yoğun bakıma düştüğünde harcanan tedavi maliyeti binlerce kat daha fazladır.\n  3. **Toplumsal Açıdan:** Koruma toplumun genel refahını ve üretkenliğini yükseltir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Korumanın Tedaviye Karşı Üstünlük Döngüsü",
                [
                    "1. Koruyucu Müdahale: Aşı yapılır, su klorlanır ve sağlıklı beslenme eğitimi verilir.",
                    "2. Hastalık Engellenir: Bulaş zinciri kırılır ve birey sağlıklı kalır.",
                    "3. Maliyet Tasarrufu: İlaç ve yoğun bakım harcamaları sıfıra yaklaşır.",
                    "4. Toplumsal Refah: Kaynaklar sağlığı daha da geliştirmeye aktarılır."
                ]
            ),
            make_cloze(
                "Halk sağlığının en temel ilkesine göre devletin birincil görevi hastaları tedavi etmekten önce koruma tedaviden üstündür ilkesi gereği kişilerin hasta olmamasını sağlamaktır.",
                "koruma tedaviden üstündür",
                "Koruyucu hekimliğin tedavi edici hekimliğe önceliğini belirten altın ilke"
            )
        ]
    })

    # Slide 85
    slides.append({
        "id": "k1-18-s85",
        "title": "Halk Sağlığının Temel İlkeleri - III: Kişi Çevresiyle Bir Bütündür",
        "content": "İnsan canlısı çevresinden yalıtılmış steril bir fanusta yaşamaz; çevresinin doğrudan bir parçasıdır (Sınav Spotu):\n\n- **3. Temel İlke: Kişi Çevresiyle Bir Bütündür:**\n  - Çevredeki olumsuz faktörler (kirli su, hava kirliliği, nemli ev, radyasyon, gürültü, böcekler) düzeltilmeden hastalıklar asla kontrol altına alınamaz.\n- **4. Temel İlke: Hastalıkların Nedenleri Biyolojik, Fizik ve Sosyaldir:**\n  - Bir enfeksiyonun nedeni yalnızca mikrop (biyolojik) değildir.\n  - İklim, mevsim, coğrafya (fizik) ve gelir düzeyi, eğitim, barınma, çalışma koşulları (sosyal) hastalığın asıl belirleyicileridir.\n- **11. Temel İlke: Yaşam Doğum Öncesinden Ölüme Kadar Bir Bütündür:**\n  - Anne karnındaki fetüsün maruz kaldığı yetersiz beslenme veya toksinler, 50 yıl sonra o bireyde hipertansiyon, diyabet ve kalp hastalığı olarak ortaya çıkar.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Yalıtılmış Birey Yanılgısı vs Çevreyle Bütünlük İlkesi",
                "Yalıtılmış Birey Yanılgısı",
                "Hastaya ilaç verip aynı kirli suya, küflü eve ve stresli işe geri göndermek; hastalık kaçınılmaz olarak tekrarlar.",
                "Çevreyle Bütünlük İlkesi",
                "Bireyi tedavi ederken suyunu, evini, işini ve sosyal çevresini ıslah etmek; kalıcı sağlık sağlamak."
            ),
            make_quiz(
                "Halk sağlığının 'Kişi çevresiyle bir bütündür' ilkesi klinik hekimlik pratiğinde en somut olarak hangi yaklaşımı zorunlu kılar?",
                [
                    {"key": "A", "text": "Hastalıkların tedavisinde yalnızca ilaca odaklanmayıp ev, iş, su ve hava koşullarını da sorgulamayı ve düzeltmeyi", "isCorrect": True, "explanation": "Doğru cevap A'dır: Kişi çevresinden ayrılamaz; çevresel risk faktörleri düzeltilmeden kalıcı şifa sağlanamaz."},
                    {"key": "B", "text": "Hastanın tüm yakınlarıyla ilişkisini kesip steril bir odada yaşamasını", "isCorrect": False, "explanation": "Sosyal iyilik haline aykırıdır."},
                    {"key": "C", "text": "Yalnızca genetik tahlillerle teşhis koymayı", "isCorrect": False, "explanation": "Çevresel faktörleri dışlar."},
                    {"key": "D", "text": "Hastalara çevre vergisi kesmeyi", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 86
    slides.append({
        "id": "k1-18-s86",
        "title": "Halk Sağlığının Temel İlkeleri - IV: Hizmet En Yakına Götürülmelidir",
        "content": "Sağlık hizmetine fiziksel ve coğrafi erişilebilirlik halk sağlığının adalet ölçütüdür (Sınav Spotu):\n\n- **5. Temel İlke: Sağlık Hizmetleri Kişilerin En Yakınına Kadar Götürülmelidir:**\n  - Bir sağlık hizmeti ne kadar mükemmel olursa olsun, eğer halk ona ulaşmak için saatlerce dağ yolları aşmak, servet harcamak zorundaysa o hizmet 'yok' hükmündedir.\n  - Hizmet, insanların yaşadığı, çalıştığı ve çocukların okuduğu yerin merkezine (**köyde sağlık evi, mahallede sağlık ocağı / aile sağlığı merkezi**) kadar götürülmelidir.\n- **Kademeli Sevk Zinciri:**\n  - En yakındaki birinci basamak sorunların %80-90'ını yerinde çözer; çözülemeyen az sayıdaki vaka planlı bir sevk zinciriyle hastanelere aktarılır.\n  - Bu sayede hastanelerin gereksiz acil ve poliklinik yığılmaları önlenir.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Hizmet Basamağı", "Konumu", "Hizmet Türü", "Çözülen Sağlık Sorunu Oranı"],
                [
                    ["Birinci Basamak (Sağlık Ocağı / ASM)", "Köy ve mahalle (En yakın)", "Aşı, gebe izlem, çevre, ayaktan tanı ve tedavi", "Toplum sorunlarının %85-90'ı"],
                    ["İkinci Basamak (Devlet Hastanesi)", "İlçe / İl merkezi", "Uzman hekim muayenesi, yataklı tedavi, ameliyat", "Sorunların %10-12'si"],
                    ["Üçüncü Basamak (Üniversite Hastanesi)", "Büyükşehirler", "İleri uzmanlık, kanser, organ nakli, eğitim", "Sorunların %1-3'ü"]
                ]
            ),
            make_cloze(
                "Sağlık hizmetlerinin başarısı için hizmetin hastanelerde beklenmeyip kişilerin en yakınına kadar götürülmesi ve birinci basamakta çözülmesi esastır.",
                "en yakınına",
                "Halk sağlığında coğrafi erişilebilirlik ilkesi gereği hizmetin ulaştırılacağı yer"
            )
        ]
    })

    # Slide 87
    slides.append({
        "id": "k1-18-s87",
        "title": "Halk Sağlığının Temel İlkeleri - V: Önemli Hastalık ve Risk Grupları",
        "content": "Kısıtlı sağlık kaynaklarının en doğru ve adil biçimde dağıtılması önceliklendirme ilkelerine bağlıdır (Sınav Spotu):\n\n- **12. Temel İlke: Önemli Hastalıklara Öncelik:**\n  - Grotjahn kuralına dayanır: Kaynaklar **en çok öldüren, en sık görülen ve en çok sakat bırakan** hastalıklara tahsis edilmelidir.\n  - Gelişmekte olan ülkelerde enfeksiyonlar ve bebek ölümleri; gelişmiş ülkelerde ise kalp-damar hastalıkları, kanserler ve diyabet önceliklidir.\n- **Risk Gruplarına Öncelik İlkesi:**\n  - Toplumun tüm bireyleri aynı hastalık riskini taşımaz.\n  - Biyolojik veya sosyal olarak hastalığa ve ölüme en açık olan hassas gruplara öncelik verilmelidir:\n  1. **Gebe ve emziren anneler,**\n  2. **0-5 yaş arası bebek ve küçük çocuklar,**\n  3. **Yaşlılar ve kronik hastalığı olanlar,**\n  4. **Ağır ve tehlikeli iş kollarında çalışan işçiler,**\n  5. **Yoksullar ve sığınmacılar.**",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_slider(
                "Eşit Dağıtım (Herkes Aynı) vs Hakkaniyetli Dağıtım (Risk Gruplarına Öncelik)",
                "Mekanik Eşit Dağıtım",
                "Herkese ihtiyacına bakılmaksızın aynı ilacı ve bütçeyi vermek; risk altındaki gebeleri ve bebekleri korumasız bırakır.",
                "Hakkaniyetli Dağıtım (Risk Önceliği)",
                "Kaynakları en çok tehdit altında olan gebe, bebek, yaşlı ve işçilere yoğunlaştırarak ölümleri hızla önlemek."
            ),
            make_quiz(
                "Halk sağlığı planlamasında sağlık hizmetlerinin sunumunda öncelik tanınması gereken en temel biyolojik ve sosyal risk grupları hangileridir?",
                [
                    {"key": "A", "text": "Gebe-emziren anneler, 0-5 yaş bebekler, yaşlılar ve ağır sanayi işçileri", "isCorrect": True, "explanation": "Doğru cevap A'dır: Gebeler, bebekler, yaşlılar ve işçiler biyolojik/çevresel olarak en hassas risk gruplarıdır."},
                    {"key": "B", "text": "Yalnızca profesyonel sporcular ve dizi oyuncuları", "isCorrect": False, "explanation": "Halk sağlığı risk grubu değildir."},
                    {"key": "C", "text": "Yalnızca özel aracı olan yüksek gelirli yurttaşlar", "isCorrect": False, "explanation": "Tam tersine yoksullar önceliklidir."},
                    {"key": "D", "text": "Sadece tatil köylerinde kalan turistler", "isCorrect": False, "explanation": "İlgisizdir."}
                ]
            )
        ]
    })

    # Slide 88
    slides.append({
        "id": "k1-18-s88",
        "title": "Halk Sağlığının Temel İlkeleri - VI: Halkın Katılımı ve Ekip Hizmeti",
        "content": "Halk sağlığı yukarıdan aşağıya bürokratik emirlerle değil, toplumla omuz omuza yürütülür (Sınav Spotu):\n\n- **13. Temel İlke: Halkın Sağlık Hizmetlerine Katılımı Esastır:**\n  - Toplumun kültürüne, inançlarına, geleneklerine ve beklentilerine uymayan hiçbir sağlık programı kabul görmez.\n  - Sağlık politikaları masa başında değil; halkın, muhtarların, öğretmenlerin, din görevlilerinin ve ailelerin görüşleri alınarak planlanmalıdır.\n- **Ekip Hizmeti İlkesi:**\n  - Sağlık hizmeti tek başına 'süpermen' hekimlerin işi değildir.\n  - Hekim, hemşire, ebe, sağlık memuru, laborant, çevre sağlığı teknisyeni ve idari personelin bir bütün olarak çalıştığı **multidisipliner bir ekip çalışmasıdır**.\n- **10. Temel İlke: Herkes Kendi Sağlığından Sorumludur (Öz Sorumluluk):**\n  - Birey beslenmesine dikkat etmeli, sigara içmemeli ve koruyucu aşılarını yaptırmalıdır.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_chain(
                "Toplum Katılımı ile Sağlık Programı Başarı Zinciri",
                [
                    "1. Yerel İhtiyaç Tespiti: Köy veya mahalle halkının sorunları dinlenir.",
                    "2. Kanaat Önderleri İşbirliği: Muhtar, öğretmen ve aile büyükleriyle ortak dil kurulur.",
                    "3. Katılımcı Planlama: Hizmetin saatleri ve yeri halkın yaşam tarzına göre ayarlanır.",
                    "4. Yüksek Uyum ve Başarı: Aşılanma ve tarama oranları zirveye ulaşır."
                ]
            ),
            make_cloze(
                "Toplumun kültürel beklentilerine uymayan programların başarıya ulaşamayacağını belirten temel halk sağlığı kuralına göre halkın sağlık hizmetlerine katılımı esastır.",
                "halkın sağlık hizmetlerine katılımı",
                "Sağlık hizmetlerinin planlanması ve yürütülmesinde toplumun desteğini ifade eden ilke"
            )
        ]
    })

    # Slide 89 - CHECKPOINT 9
    slides.append({
        "id": "k1-18-s89",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Alma-Ata Bildirgesi ve Temel İlkeler",
        "content": "Bu checkpointte Alma-Ata Bildirgesi'ni ve halk sağlığının temel ilkelerini özetliyoruz:\n\n- **Alma-Ata (1978):** '2000 Yılında Herkese Sağlık' hedefini koydu; çözümün Temel Sağlık Hizmetleri (TSH) olduğunu ilan etti.\n- **TSH'nin 8 Bileşeni:** Sağlık eğitimi, beslenme, temiz su/sanitasyon, ana-çocuk sağlığı/aile planlaması, bağışıklama, endemik hastalık kontrolü, temel tedavi ve temel ilaç temini.\n- **1. İlke:** Sağlık temel bir insanlık hakkıdır (Anayasa m. 56).\n- **2. İlke:** Koruma tedaviden üstündür (daha insani, ucuz ve etkilidir).\n- **3. & 4. İlke:** Kişi çevresiyle bir bütündür; nedenler biyolojik, fizik ve sosyaldir.\n- **5. İlke:** Sağlık hizmeti kişilerin en yakınına (sağlık ocağı / ASM) götürülmelidir.\n- **Önemli Hastalık ve Risk Grupları:** En çok öldüren, sakat bırakan ve sık görülen hastalık önemlidir; gebeler, bebekler, yaşlılar ve işçiler önceliklidir.\n- **Halkın Katılımı ve Ekip:** Sağlık ekip işidir; toplumun katılımı olmadan programlar başarıya ulaşamaz.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_table(
                ["Halk Sağlığı İlkesi", "Temel Felsefe", "Uygulamadaki Karşılığı"],
                [
                    ["1. Sağlık İnsan Hakkıdır", "Erişimde tam adalet", "Zengin-yoksul ayrımı olmadan ücretsiz temel hizmet"],
                    ["2. Koruma Üstündür", "Hastalığı oluşmadan engelleme", "Aşı, temiz su ve sanitasyon önceliği"],
                    ["3. Çevreyle Bütünlük", "Biyolojik, fizik ve sosyal çevre", "Konut, işyeri ve su ıslahı"],
                    ["4. En Yakına Götürme", "Coğrafi erişilebilirlik", "Köyde sağlık evi, mahallede sağlık ocağı"],
                    ["5. Risk Gruplarına Öncelik", "Hakkaniyetli kaynak dağıtımı", "Gebe, bebek, yaşlı ve işçilerin özel izlemi"],
                    ["6. Halkın Katılımı", "Toplumsal işbirliği", "Yerel liderler ve halkla ortak planlama"]
                ]
            ),
            make_chain(
                "Alma-Ata Temel Sağlık Mantığı",
                [
                    "1. Hak Bildirisi: Sağlığın evrensel insan hakkı olarak kabulü.",
                    "2. Birinci Basamak Odaklılık: Pahalı hastaneler yerine en yakındaki sağlık ocağı.",
                    "3. 8 Asgari Hizmet: Aşı, temiz su, beslenme ve ana-çocuk sağlığı zorunluluğu.",
                    "4. Herkese Sağlık: 2000 yılı ve sonrasında adil, eşitlikçi sağlık düzeni."
                ]
            )
        ]
    })

    # Slide 90
    slides.append({
        "id": "k1-18-s90",
        "title": "Bölüm Özeti: Temel İlkelerden Korunma Düzeyleri ve Geleceğe Geçiş",
        "content": "Bölüm 9 boyunca Alma-Ata felsefesini, TSH'nin 8 bileşenini ve halk sağlığının kurucu ilkelerini inceledik:\n\n- **Özet:** Koruma esastır, sağlık haktır, kişi çevresiyle bütündür ve halkın katılımı olmadan başarı imkansızdır.\n- **Sonraki Bölüm (Bölüm 10):** Bu ilkelerin klinik ve epidemiyolojik uygulaması olan **Korunma Düzeylerini (Primordial, Birincil, İkincil ve Üçüncül korunma), tarama ilkelerini, halk sağlığı uzmanının görevlerini ve 21. yüzyıl gündemini** ele alacağız.",
        "sourcePdf": "Kurul 1 - Ders 18: Halk Sağlığı Tarihçesi (Doç. Dr. Nergiz Sevinç)",
        "elements": [
            make_recall(
                "1978 Alma-Ata Konferansı'nda tüm dünya ülkelerinin oybirliğiyle kabul ettiği tarihi küresel hedef sloganı nedir?",
                "2000 Yılında Herkese Sağlık (Health for All by the Year 2000)",
                "Alma-Ata'nın 2000 yılı vizyon sloganı"
            ),
            make_quiz(
                "Halk sağlığı anlayışında 'Kişilerin sağlığı ve hastalığı aynı zamanda toplumun sorunudur' ilkesinin en çarpıcı epidemiyolojik kanıtı hangisidir?",
                [
                    {"key": "A", "text": "Bulaşıcı bir hastalığa yakalanan tek bir bireyin aşılanmamış tüm toplumu enfekte edebilme ve salgın başlatabilme riski", "isCorrect": True, "explanation": "Doğru cevap A'dır: Bulaşıcı hastalıklarda tek bir vaka tüm toplumu tehdit eder; bu nedenle bireyin sağlığı toplumun sorunudur."},
                    {"key": "B", "text": "Hastalıkların yalnızca laboratuvarda teşhis edilebilmesi", "isCorrect": False, "explanation": "İlgisizdir."},
                    {"key": "C", "text": "Her hastanın kendi özel doktorunu seçme hakkının bulunması", "isCorrect": False, "explanation": "Bireysel tercihtir."},
                    {"key": "D", "text": "İlaç fiyatlarının döviz kuruna bağlı olması", "isCorrect": False, "explanation": "Ekonomik piyasa kuralıdır."}
                ]
            )
        ]
    })

    return slides
