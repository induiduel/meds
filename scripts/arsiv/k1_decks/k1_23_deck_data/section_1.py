# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 1: Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi (Slayt 1 - 10)
Checkpoint 1: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_1_slides():
    slides = []

    # Slayt 1: Ana-Çocuk Sağlığı (AÇS) Hizmetlerinin Tanımı ve Kapsamı
    slides.append({
        "id": "k1-23-s01",
        "title": "Ana-Çocuk Sağlığı (AÇS) Hizmetlerinin Tanımı ve Kapsamı",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 1,
        "narrative": (
            "Ana-Çocuk Sağlığı (AÇS); anne adaylarının, gebelerin, lohusaların, bebeklerin ve çocukların "
            "bedensel, ruhsal ve sosyal yönden tam bir iyilik haline ulaşmasını hedefleyen en temel halk sağlığı disiplinidir. "
            "AÇS hizmetleri yalnızca hastalıkların tedavi edilmesini değil, koruyucu hekimlik ilkeleri doğrultusunda "
            "risk gruplarının önceden belirlenmesini, periyodik sağlık izlemlerini, aşılamayı, beslenme danışmanlığını "
            "ve üreme sağlığı hizmetlerini entegre bir bütün olarak sunar. "
            "Bir toplumda ana ve çocuk sağlığı düzeyinin yüksek olması; o ülkenin sosyoekonomik gelişmişliğinin, "
            "sağlık hizmetlerine erişim gücünün ve insan haklarına verilen değerin en hassas göstergesidir. "
            "Bu nedenle modern tıp sistemlerinde birinci basamak sağlık örgütlenmesinin omurgasını AÇS izlemleri oluşturur."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Ana-çocuk sağlığı hizmetleri koruyucu hekimlik yaklaşımıyla risk altındaki kadın ve çocukların periyodik izlemini esas alır.",
                "periyodik izlemini",
                "Düzenli aralıklarla yapılan sağlık kontrolleri süreci"
            ),
            make_micro_quiz(
                "Halk sağlığı disiplininde Ana-Çocuk Sağlığı (AÇS) hizmetlerinin temel felsefesi ve hedefi aşağıdakilerden hangisidir?",
                {
                    "A": "Yalnızca hastaneye yatan kritik gebe ve çocukların tedavisini yürütmek",
                    "B": "Toplumdaki tüm kadın ve çocukların periyodik izlemlerle sağlığını korumak ve geliştirmek",
                    "C": "Sadece 65 yaş üstü geriatrik nüfusun evde bakımını planlamak",
                    "D": "Tüm doğumların evde geleneksel yöntemlerle gerçekleşmesini sağlamak",
                    "E": "Çocukluk çağı aşılarını tamamen isteğe bağlı hale getirmek"
                },
                "B",
                {
                    "A": "Yanlıştır; AÇS birinci basamakta koruyucu ve periyodik izlem odaklıdır.",
                    "B": "Doğrudur; AÇS toplumdaki kadın ve çocukların periyodik izlemlerle korunmasını ve geliştirilmesini hedefler.",
                    "C": "Yanlıştır; Geriatrik bakım AÇS kapsamı dışındadır.",
                    "D": "Yanlıştır; Hastanede ve eğitimli sağlık personeliyle doğum esastır.",
                    "E": "Yanlıştır; Rutin aşılama AÇS'nin en temel zorunlu koruyucu bileşenidir."
                }
            ),
            make_active_recall(
                "Bir toplumun sosyoekonomik gelişmişlik düzeyini ve sağlık altyapısının kalitesini yansıtan en duyarlı iki demografik sağlık göstergesi grubu hangisidir?",
                "Anne ölüm oranı ile bebek ve çocuk ölüm hızlarıdır.",
                "Maternal ve pediatrik mortalite göstergeleri"
            )
        ]
    })

    # Slayt 2: Neden Kadınlar ve Çocuklar En Kritik Risk Grubudur?
    slides.append({
        "id": "k1-23-s02",
        "title": "Neden Kadınlar ve Çocuklar En Kritik Risk Grubudur?",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 2,
        "narrative": (
            "Koruyucu hekimliğin en temel aksiyomu, kaynakların öncelikle 'risk altındaki gruplara' yönlendirilmesidir. "
            "Toplumda kadınlar ve çocuklar iki büyük biyolojik ve sosyal gerekçeyle en kırılgan grubu teşkil eder: "
            "1. **Bebek ve Çocuklar:** Hayatlarını kendi başlarına sürdürebilme yetisine sahip değillerdir; beslenme, hijyen ve "
            "fiziksel korunma açısından tamamen bakıcılarına bağımlıdırlar. İmmün sistemleri ve organ rezervleri immatür olduğundan "
            "yetersiz bakım durumunda enfeksiyon, malnütrisyon ve ölüm riski katlanarak artar. "
            "2. **Kadınlar:** Doğurganlık çağında gebelik, doğum ve lohusalık gibi fizyolojik açıdan son derece ağır metabolik ve "
            "hemodinamik yükler taşırlar. Her gebelik potansiyel bir kanama, preeklampsi ve enfeksiyon riski barındırır. "
            "Bu iki grubun periyodik takibi, önlenebilir ölümlerin neredeyse tamamını engeller."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Bebek ve çocuklar kendi başlarına yaşamlarını sürdüremedikleri ve immün sistemleri immatür olduğu için yüksek risk grubundadır.",
                "yüksek risk grubundadır",
                "Koruyucu izlemlerin öncelikle odaklandığı kırılgan popülasyon kategorisi"
            ),
            make_before_after(
                "Koruyucu İzlem Yapılan vs Yapılmayan Topluluklarda Risk Grupları",
                "İzlemsiz ve Düzensiz Takip",
                "Gebelik komplikasyonları ve konjenital anomaliler ancak kriz anında fark edilir; bebek ölüm hızı ve anne ölümleri tavan yapar.",
                "Periyodik Sağlık İzlemi",
                "Risk faktörleri gebelik öncesinde veya ilk trimesterde saptanır; komplikasyonlar önlenir ve mortalite minimuma iner.",
                "Periyodik izlemin koruyucu gücü"
            ),
            make_active_recall(
                "Kadınların doğurganlık çağında (15-49 yaş) en yüksek biyolojik ve tıbbi risk altına girdikleri üç kritik fizyolojik evre hangisidir?",
                "Gebelik, doğum eylemi ve doğum sonrasındaki lohusalık (puerperium) dönemleridir.",
                "Maternal biyolojik risk evreleri"
            )
        ]
    })

    # Slayt 3: Dünya ve Türkiye Demografisi: Kadın ve Çocuk Nüfus Payı
    slides.append({
        "id": "k1-23-s03",
        "title": "Dünya ve Türkiye Demografisi: Kadın ve Çocuk Nüfus Payı",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 3,
        "narrative": (
            "Demografik veriler incelendiğinde kadın ve çocukların toplumun azınlığı değil, neredeyse **yarısını** oluşturduğu görülür: "
            "1. **Küresel Tablo (2025, Dünya Nüfusu ~8.2 Milyar):** Dünya nüfusunun **%24'ünü 0-14 yaş grubu çocuklar**, "
            "**%24.5'ini ise 15-49 yaş doğurganlık çağındaki kadınlar** oluşturur. İkisi toplandığında küresel nüfusun yaklaşık %48.5'ine ulaşır. "
            "2. **Türkiye Tablosu (TÜİK 2025):** Ülkemiz nüfusunun **%20.3'ünü 0-14 yaş çocuklar**, **%25.4'ünü ise 15-49 yaş kadınlar** oluşturmaktadır. "
            "Toplumun yaklaşık %46'sını kapsayan bu devasa kitleye yönelik sağlık hizmetleri aksarsa tüm toplumun sağlığı çöker. "
            "Bu nedenle AÇS hizmetleri sağlık bütçelerinin ve birinci basamak iş gücünün en büyük kısmını talep eder."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "TÜİK verilerine göre Türkiye nüfusunun yaklaşık yüzde yirmi beşini on beş kırk dokuz yaş grubu kadınlar oluşturur.",
                "on beş kırk dokuz yaş",
                "Doğurganlık çağı kadın nüfusunun yaş sınırları"
            ),
            make_table(
                "Dünya ve Türkiye Demografik Nüfus Dağılımı Karşılaştırması",
                ["Nüfus Grubu", "Dünya Genel Oranı (2025)", "Türkiye Oranı (TÜİK 2025)", "AÇS Hizmetlerindeki Önemi"],
                [
                    ["0-14 Yaş Çocuk Nüfusu", "%24.0", "%20.3", "Büyüme-gelişme ve aşılama hedef kitlesi"],
                    [
                        "15-49 Yaş Kadın Nüfusu",
                        "%24.5",
                        {"text": "%25.4", "isMasked": True, "hint": "Türkiye'deki doğurganlık çağı kadın oranı"},
                        "Üreme sağlığı ve doğum öncesi bakım hedef kitlesi"
                    ],
                    ["Toplam AÇS Hedef Kitlesi", "~%48.5", "~%45.7", "Toplum nüfusunun neredeyse yarısını oluşturma"]
                ]
            ),
            make_micro_quiz(
                "TÜİK ve küresel halk sağlığı verilerine göre Türkiye'de 15-49 yaş kadınlar ve 0-14 yaş çocukların toplam nüfustaki payı yaklaşık ne kadardır?",
                {
                    "A": "Yaklaşık %10",
                    "B": "Yaklaşık %20",
                    "C": "Yaklaşık %46",
                    "D": "Yaklaşık %75",
                    "E": "Yaklaşık %90"
                },
                "C",
                {
                    "A": "Yanlıştır; %10 çok düşüktür.",
                    "B": "Yanlıştır; %20 yalnızca çocuk nüfusu payına yakındır.",
                    "C": "Doğrudur; %20.3 çocuk ve %25.4 kadın nüfusuyla toplam pay yaklaşık %46'dır.",
                    "D": "Yanlıştır; %75 erişkin ve yaşlıları da kapsar.",
                    "E": "Yanlıştır; Nüfusun tamamına yakını değildir."
                }
            )
        ]
    })

    # Slayt 4: Koruyucu Hekimlikte Periyodik İzlem Felsefesi
    slides.append({
        "id": "k1-23-s04",
        "title": "Koruyucu Hekimlikte Periyodik İzlem Felsefesi",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 4,
        "narrative": (
            "Periyodik sağlık izlemi; sağlıklı görünen bireylerin belirli yaş ve biyolojik dönemlere özgü aralıklarla "
            "standart muayene, tarama ve danışmanlık protokollerinden geçirilmesidir. "
            "AÇS'de periyodik izlemin iki temel stratejik amacı vardır: "
            "1. **Sorunların Ortaya Çıkmadan Önlenmesi (Primer Koruma):** Gebeye tetanoz aşısı yapılması, demir/folik asit verilmesi, "
            "bebeğe D vitamini profilaksisi ve anne sütü teşviki. "
            "2. **Sorunların Semptom Vermeden Erken Tespiti (Sekonder Koruma):** Asemptomatik bakteriüri, gestasyonel diyabet, "
            "hafif preeklampsi, konjenital kalça çıkığı veya fenilketonüri gibi durumların erken evrede yakalanarak kalıcı hasarın engellenmesi. "
            "İzlem takvimleri gelişigüzel değil, patolojilerin en sık ortaya çıktığı kritik haftalar ve aylara göre bilimsel olarak dizayn edilmiştir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Asemptomatik bakteriüri veya preeklampsinin belirti vermeden erken evrede yakalanması sekonder koruma kapsamındadır.",
                "sekonder koruma",
                "Erken tanı ve tarama odaklı koruyucu hekimlik düzeyi"
            ),
            make_causal_chain(
                "Periyodik İzlemin Komplikasyon Önleme Mekanizması",
                [
                    "1. Zamanında Başvuru: Gebe ilk trimesterde (0-14. hafta) aile hekimine izleme gelir.",
                    "2. Rutin Tarama: Tam idrar tahlili ile asemptomatik bakteriüri veya hafif tansiyon yüksekliği saptanır.",
                    "3. Erken Müdahale: Preeklampsi veya akut piyelonefrit gelişmeden tedavi planlanır.",
                    "4. Sağlıklı Doğum: Erken doğum, düşük doğum ağırlığı ve maternal ölüm riski bertaraf edilir."
                ]
            ),
            make_active_recall(
                "Gebelikte tetanoz aşısı uygulanması ve profilaktik folik asit desteği verilmesi hangi koruyucu hekimlik basamağına örnektir?",
                "Hastalık veya anomali ortaya çıkmadan önce uygulandığı için Primer (Birincil) Koruma basamağına örnektir.",
                "Hastalık öncesi önleme basamağı"
            )
        ]
    })

    # Slayt 5: Bebek ve Çocuk Ölümlülüğünü Artıran Maternal Risk Faktörleri
    slides.append({
        "id": "k1-23-s05",
        "title": "Bebek ve Çocuk Ölümlülüğünü Artıran Maternal Risk Faktörleri",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 5,
        "narrative": (
            "Epidemiyolojik araştırmalar, bebek ve çocuk ölümlerinin önemli bir kısmının anneye ait doğurganlık özellikleriyle doğrudan "
            "bağlantılı olduğunu kanıtlamıştır. Tıbbi literatürde ve TNSA raporlarında 'Maternal Yüksek Risk Faktörleri' üç başlıkta özetlenir: "
            "1. **Anne Yaşının 18'den Küçük Olması (Adölesan Gebelik):** Pelvis kemik çatısının immatüritesi, yetersiz beslenme ve "
            "sosyoekonomik hazırlıksızlık nedeniyle erken doğum, düşük doğum ağırlığı ve bebek ölümü riski 2-3 kat artar. "
            "2. **Dört ve Daha Fazla Doğum (Büyük Parite):** Uterus kas liflerinin yorulması, plasenta anomalileri ve anne bedeninin tükenmesi "
            "bebek ölüm oranını dramatik yükseltir. "
            "3. **Kısa Doğum Aralığı (<2 Yıl):** İki gebelik arasında en az 24 ay süre bırakılmadığında annenin demir, kalsiyum ve folat "
            "depoları yenilenemez; intrauterin büyüme geriliği ve fetal kayıp riski tavan yapar."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "İki gebelik arasındaki sürenin iki yıldan kısa olması annenin biyolojik depolarının tükenmesine bağlı fetal ölüm riskini artırır.",
                "iki yıldan kısa",
                "Maternal depoların yenilenmesi için gereken minimum güvenli aralık sınırı"
            ),
            make_table(
                "Bebek ve Çocuk Ölümünü Artıran Maternal Risk Faktörleri",
                ["Maternal Risk Faktörü", "Kritik Eşik Değer", "Yarattığı Temel Biyolojik Patoloji"],
                [
                    ["Adölesan Anne Yaşı", "< 18 Yaş", "Pelvik immatürite, düşük doğum ağırlığı ve prematürite"],
                    [
                        "İleri Doğum Sayısı",
                        {"text": "4 ve daha fazla doğum", "isMasked": True, "hint": "Çok doğum yapmanın getirdiği tükenmişlik eşiği"},
                        "Uterus atonisi, malnütrisyon ve plasenta yerleşim kusurları"
                    ],
                    ["Kısa Doğum Aralığı", "< 24 Ay (2 Yıl)", "Maternal mikro besin tükenmesi ve büyüme geriliği"]
                ]
            ),
            make_micro_quiz(
                "Bebek ve çocuk ölümlülüğünü artıran anne kaynaklı biyolojik risk faktörleri arasında aşağıdakilerden hangisi yer almaz?",
                {
                    "A": "Doğumda anne yaşının 18'den küçük olması",
                    "B": "Annenin 4 ve daha fazla doğum yapmış olması",
                    "C": "Doğumlar arasındaki sürenin 2 yıldan kısa olması",
                    "D": "İki gebelik arasında 3-4 yıllık sağlıklı aralık bırakılması",
                    "E": "Annenin 35 yaşın üzerinde ileri anne yaşında gebe kalması"
                },
                "D",
                {
                    "A": "Risk faktörüdür; Adölesan gebelik infant mortalitesini katlar.",
                    "B": "Risk faktörüdür; 4+ doğum yüksek parite riskidir.",
                    "C": "Risk faktörüdür; Kısa doğum aralığı depoları tüketir.",
                    "D": "Risk Faktörü Değildir; 3-4 yıllık aralık depoların tamamen yenilendiği en ideal fizyolojik süredir.",
                    "E": "Risk faktörüdür; İleri anne yaşı kromozomal anomali ve toksemi riskini artırır."
                }
            )
        ]
    })

    # Slayt 6: AÇS Hizmetlerinin Sosyoekonomik Belirleyicileri ve Cinsiyet Eşitliği
    slides.append({
        "id": "k1-23-s06",
        "title": "AÇS Hizmetlerinin Sosyoekonomik Belirleyicileri ve Cinsiyet Eşitliği",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 6,
        "narrative": (
            "Ana-çocuk sağlığı yalnızca biyomedikal girişimlerle açıklanamaz; doğrudan **sağlığın sosyal belirleyicilerine** bağlıdır. "
            "Dünya Sağlık Örgütü raporlarına göre anne ve çocuk sağlığını belirleyen en güçlü üç sosyal faktör şunlardır: "
            "1. **Annenin Eğitim Düzeyi:** Eğitimli annelerin bebeklerini aşılama, temiz su kullanma, emzirme ve acil tehlike işaretlerinde "
            "hastaneye başvurma oranları belirgin yüksektir. Annenin eğitimi arttıkça bebek ölüm hızı doğrudan düşer. "
            "2. **Toplumsal Cinsiyet Eşitliği ve Kadının Statüsü:** Kadının aile içinde karar alma süreçlerine katılabildiği, kendi bedeni "
            "ve sağlık hizmeti alma konusunda söz sahibi olduğu toplumlarda anne ölümleri en düşük düzeydedir. "
            "3. **Sağlık Hizmetlerine Coğrafi ve Ekonomik Erişim:** Kırsal bölgelerde yol, ulaşım ve maddi imkan yetersizliği "
            "acil obstetrik bakım gecikmelerine (üç gecikme modeli) yol açarak ölümleri tetikler."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Toplumda kadının statüsünün yükselmesi ve eğitim düzeyinin artması bebek ve anne ölüm oranlarını doğrudan düşürür.",
                "eğitim düzeyinin artması",
                "Sağlık okuryazarlığını ve doğru sağlık davranışını güçlendiren sosyal faktör"
            ),
            make_branching_logic(
                "Kırsal bir bölgede görev yapan bir aile hekimi, köydeki kadınların gebelik izlemlerine gelmediğini ve doğumları evde geleneksel ebelerle yaptığını fark ediyor.",
                "Bu toplumda anne ölümlerini önlemek için hekimin atması gereken en doğru ve sürdürülebilir ilk halk sağlığı adımı hangisidir?",
                [
                    {
                        "text": "Köyün kadınları ve aile büyükleriyle güven ilişkisi kurarak gebelik izlemlerinin ve hastanede doğumun hayat kurtarıcı önemini anlatan eğitimler düzenlemek ve mobil izlem planlamak",
                        "isCorrect": True,
                        "feedback": "Kusursuz Halk Sağlığı Kararı: Sağlık inançlarını dönüştürmek, güven inşa etmek ve hizmeti ayağa götürmek geleneksel bariyerleri yıkarak hastane doğumlarını artırır."
                    },
                    {
                        "text": "Evde doğum yapan tüm kadınlara ağır para cezaları kestirmek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Cezalandırıcı yaklaşım kadınların sağlık sisteminden tamamen kaçmasına ve ölümlerin gizlenmesine yol açar."
                    },
                    {
                        "text": "Sorunun kader olduğunu kabul edip sadece polikliniğe başvuranlarla ilgilenmek",
                        "isCorrect": False,
                        "feedback": "Hatalı: Koruyucu hekimlik pasif değil, proaktif olarak riskli gruplara ulaşmayı gerektirir."
                    }
                ]
            ),
            make_active_recall(
                "Bebek ölüm hızını düşürmede modern tıbbi cihazlardan ve ilaçlardan bile daha güçlü korelasyon gösteren temel sosyal gösterge nedir?",
                "Annenin eğitim düzeyi ve okuryazarlık oranıdır.",
                "Maternal eğitim düzeyi faktörü"
            )
        ]
    })

    # Slayt 7: Aile Planlaması ve Doğurganlığın Düzenlenmesinin Çocuk Sağlığına Etkisi
    slides.append({
        "id": "k1-23-s07",
        "title": "Aile Planlaması ve Doğurganlığın Düzenlenmesinin Çocuk Sağlığına Etkisi",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 7,
        "narrative": (
            "Aile planlaması (üreme sağlığı / doğurganlığın düzenlenmesi), çiftlerin istedikleri zamanda, bakabilecekleri sayıda "
            "ve sağlıklı aralıklarla çocuk sahibi olmalarını sağlayan temel bir insan hakkıdır. "
            "Aile planlaması bir nüfus kısıtlama aracı değil, doğrudan bir **ana ve çocuk hayatı kurtarma stratejisidir**: "
            "1. İstenmeyen ve yüksek riskli gebelikleri (çok genç, çok yaşlı, çok sayıda ve çok sık) önler. "
            "2. Yasadışı, güvensiz düşükleri ve buna bağlı maternal kanama ve sepsisi sıfırlar. "
            "3. İki doğum arasındaki aralığı en az 2-3 yıla çıkararak anneye fizyolojik toparlanma ve önceki bebeği 2 yaşına kadar "
            "kesintisiz emzirme fırsatı sunar. "
            "4. Aile bütçesinin bölünmesini engelleyerek doğan her çocuğun yeterli beslenmesini ve eğitim almasını garantiye alır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Etkili aile planlaması hizmetleri istenmeyen gebelikleri ve sağlıksız düşükleri önleyerek anne ölümlerini belirgin azaltır.",
                "istenmeyen gebelikleri",
                "Plansız ve riskli şartlarda başlayan fertilizasyon olguları"
            ),
            make_before_after(
                "Aile Planlaması Hizmetlerinin Çocuk Sağlığına Etkisi",
                "Plansız ve Sık Doğumlar",
                "Bebekler henüz 1 yaşına basmadan yeni kardeş doğar; anne sütü erken kesilir, ailede yetersiz beslenme ve bodurluk patlak verir.",
                "Planlı ve Aralıklandırılmış Doğumlar",
                "Her çocuk en az 2 yaşına kadar anne sütü alır; anne depoları doludur, bebek sağlıklı büyür ve mortalite asgari düzeye iner.",
                "Doğum aralığının çocuk sağlığına etkisi"
            ),
            make_micro_quiz(
                "Aile planlaması hizmetlerinin anne ve çocuk sağlığına sağladığı doğrudan klinik yararlar arasında hangisi YER ALMAZ?",
                {
                    "A": "İki doğum arasındaki aralığı uzatarak önceki bebeğin emzirilme süresini artırması",
                    "B": "Güvensiz koşullarda yapılan yasadışı düşükleri ve buna bağlı sepsis ölümlerini önlemesi",
                    "C": "Adölesan gebelikleri azaltarak düşük doğum ağırlıklı bebek oranını düşürmesi",
                    "D": "Genetik hastalıklı tüm bebeklerin doğumunu biyolojik olarak imkansız kılması",
                    "E": "Annenin demir ve kalsiyum depolarının iki gebelik arasında yenilenmesini sağlaması"
                },
                "D",
                {
                    "A": "Yarardır; Emzirme süresi uzar.",
                    "B": "Yarardır; Güvensiz düşük ölümleri engellenir.",
                    "C": "Yarardır; Erken yaş gebelikleri önlenir.",
                    "D": "Böyle Bir Etkisi Yoktur; Aile planlaması gebelik sayısını ve zamanını düzenler, genetik mutasyonları yok edemez.",
                    "E": "Yarardır; Maternal depolar toparlanır."
                }
            )
        ]
    })

    # Slayt 8: Birinci Basamak Sağlık Hizmetleri ve Aile Hekimliği Uygulama Yönetmeliği
    slides.append({
        "id": "k1-23-s08",
        "title": "Birinci Basamak Sağlık Hizmetleri ve Aile Hekimliği Uygulama Yönetmeliği",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 8,
        "narrative": (
            "Türkiye'de Ana-Çocuk Sağlığı izlemlerinin yasal ve kurumsal çatısı **Aile Hekimliği Uygulama Yönetmeliği** ile belirlenmiştir. "
            "Bu mevzuata göre her aile hekimi, kendisine kayıtlı nüfusun tüm koruyucu sağlık hizmetlerini yürütmekle yükümlüdür: "
            "1. **Hedef Nüfus İzlemleri:** Gebe izlemleri, lohusa izlemleri, 15-49 yaş kadın izlemleri, yenidoğan taramaları, "
            "bebek ve çocuk periyodik izlemleri aile hekiminin birincil performans kriterleridir. "
            "2. **Aşılama ve Profilaksi:** Genişletilmiş Bağışıklama Programı (GBP) kapsamındaki aşıların soğuk zincir kurallarına uygun "
            "yapılması ve D vitamini/demir damlalarının ücretsiz dağıtılması. "
            "3. **Taramalar:** Fenilketonüri, konjenital hipotiroidi, kistik fibrozis, SMA topuk kanı taramaları ve gelişimsel kalça displazisi izlemi. "
            "Bu sistem sayesinde Türkiye'de DÖB alma oranı %90'ın, aşılama kapsayıcılığı %95'in üzerine çıkmıştır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Aile hekimliği sisteminde gebe, lohusa, bebek ve çocuk periyodik izlemleri birinci basamak koruyucu performans kriteridir.",
                "birinci basamak koruyucu performans kriteridir",
                "Hekimin düzenli yapmakla yükümlü olduğu temel halk sağlığı sorumluluğu"
            ),
            make_table(
                "Aile Hekimliği Kapsamında İzlenen Temel AÇS Grupları ve Aralıkları",
                ["İzlem Grubu", "Hedef Popülasyon", "Önerilen Minimum İzlem Sıklığı", "Temel İçerik"],
                [
                    ["Gebe İzlemi", "Tüm gebeler", "Gebelik boyunca en az 4 kez", "Fizik muayene, laboratuvar, FKS ve aşı"],
                    ["Lohusa İzlemi", "Doğum yapan kadınlar", "Doğum sonrası toplam 3 kez", "Kanama, sepsis, emzirme ve psikoloji"],
                    [
                        "15-49 Yaş Kadın İzlemi",
                        "Gebe/lohusa olmayan kadınlar",
                        {"text": "Yılda 2 kez (6 ayda bir)", "isMasked": True, "hint": "Ocak-Haziran ve Temmuz-Aralık dönemlerinde birer kez"},
                        "Üreme sağlığı, aile planlaması ve kanser taraması"
                    ],
                    ["Çocuk İzlemi", "1-5 Yaş arası çocuklar", "Toplam 7 izlem", "Büyüme-gelişme, aşı ve görme/işitme"]
                ]
            ),
            make_active_recall(
                "Aile hekimliği sisteminde gebe ve lohusa olmayan 15-49 yaş kadınların periyodik izlemi yılda kaç kez ve hangi dönemlerde yapılır?",
                "Yılda 2 kez; 1. dönem Ocak-Haziran, 2. dönem Temmuz-Aralık aylarında birer kez olmak üzere yapılır.",
                "Yıllık izlem frekansı ve takvim dönemleri"
            )
        ]
    })

    # Slayt 9: [TEKRAR SAYFASI - CHECKPOINT 1] AÇS Epidemiyolojisi ve Demografik Temeller
    slides.append({
        "id": "k1-23-s09",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] AÇS Epidemiyolojisi ve Demografik Temeller",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 9,
        "narrative": (
            "Bu birinci checkpoint sayfasında, ana-çocuk sağlığının epidemiyolojik ve demografik temellerini özetliyoruz: "
            "1. **Hedef Kitle Büyüklüğü:** Türkiye'de nüfusun %20.3'ünü 0-14 yaş çocuklar, %25.4'ünü 15-49 yaş kadınlar oluşturur (toplam ~%46). "
            "2. **Risk Grubu Mantığı:** Çocuklar biyolojik bağımlılık ve immatürite; kadınlar gebelik/doğum yükü nedeniyle en kırılgan gruptur. "
            "3. **Mortaliteyi Artıran Üçlü Maternal Risk:** Anne yaşının <18 olması (adölesan), 4 ve daha fazla doğum ve <2 yıl doğum aralığı. "
            "4. **Sosyal Belirleyiciler:** Annenin eğitim düzeyi ve kadının statüsü mortaliteyi düşüren en güçlü faktörlerdir. "
            "5. **Aile Planlaması:** Doğum aralığını uzatarak anne depolarını yeniler ve çocuk mortalitesini azaltır. "
            "6. **Aile Hekimliği:** Gebe (en az 4), lohusa (3 kez) ve 15-49 yaş kadın izlemlerini (yılda 2 kez) yasal olarak yürütür."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s09-1",
                "TÜİK verilerine göre Türkiye'de doğurganlık çağındaki (15-49 yaş) kadınların toplam nüfus içindeki payı yaklaşık yüzde kaçtır?",
                "Yaklaşık yüzde yirmi beş buçuktur (%25.4).",
                "Dörtte bir oranındaki demografik pay",
                "Demografik Göstergeler"
            ),
            make_flashcard(
                "k1-23-fc-s09-2",
                "Bebek ve çocuk ölümlülüğünü artıran anne kaynaklı üç temel biyolojik risk faktörü hangileridir?",
                "Anne yaşının 18'den küçük olması, dört ve daha fazla doğum yapılması ve iki doğum arasındaki sürenin iki yıldan kısa olmasıdır.",
                "Erken gebelik, yüksek parite ve sık aralıklı fertilizasyon üçlüsü",
                "Maternal Risk Faktörleri"
            ),
            make_flashcard(
                "k1-23-fc-s09-3",
                "Aile hekimliği mevzuatına göre gebe veya lohusa olmayan 15-49 yaş kadınların periyodik sağlık izlemi yılda kaç kez yapılır?",
                "Yılda iki kez (altı ayda bir) yapılır.",
                "Ocak-Haziran ve Temmuz-Aralık dönemlerinde birer kontrol",
                "Sağlık Mevzuatı ve İzlem"
            )
        ],
        "interactiveElements": [
            make_table(
                "AÇS Temel Kavramlar ve Kritik Göstergeler Özeti",
                ["Gösterge / Kavram", "Değer / İlke", "Halk Sağlığı Önemi"],
                [
                    ["15-49 Yaş Kadın Nüfusu", "%25.4 (Türkiye)", "Üreme sağlığı hedef kitlesi"],
                    ["0-14 Yaş Çocuk Nüfusu", "%20.3 (Türkiye)", "Pediatrik koruyucu izlem kitlesi"],
                    [
                        "Maternal Risk Yaşı",
                        {"text": "< 18 Yaş (Adölesan)", "isMasked": True, "hint": "Yüksek riskli erken yaş gebeliği sınırı"},
                        "Düşük doğum ağırlığı ve prematürite riski"
                    ],
                    ["Minimum Doğum Aralığı", "En az 24 Ay (2 Yıl)", "Maternal depoların yenilenmesi"],
                    ["15-49 Yaş Kadın İzlemi", "Yılda 2 kez", "Erken tanı ve aile planlaması"]
                ]
            )
        ]
    })

    # Slayt 10: Bölüm Özeti: Demografik Göstergelerden Anne Ölümü Kavramına Geçiş
    slides.append({
        "id": "k1-23-s10",
        "title": "Bölüm Özeti: Demografik Göstergelerden Anne Ölümü Kavramına Geçiş",
        "section": "Ana-Çocuk Sağlığının Temel İlkeleri, Epidemiyoloji ve Demografi",
        "slideNumber": 10,
        "narrative": (
            "İlk bölümümüzde ana-çocuk sağlığı hizmetlerinin felsefesini, nüfus içindeki devasa payını (~%46) ve "
            "kadın ile çocukların neden öncelikli risk grubu olduğunu inceledik. "
            "Adölesan gebelikler (<18 yaş), sık doğumlar (<2 yıl aralık) ve yüksek parite (≥4 doğum) "
            "bebek ve çocuk ölümlerini tetikleyen en ağır maternal risk faktörleridir. "
            "Bu risklerin yönetilmesinde aile hekimliği sistemi ve periyodik izlemler anahtar rol oynar. "
            "Ancak AÇS hizmetlerinin başarısını ölçen en kritik, en trajik ve en hassas gösterge **Anne Ölüm Oranı'dır (AÖO)**. "
            "Bir kadının yeni bir can dünyaya getirirken hayatını kaybetmesi, sağlık sisteminin alarm sinyalidir. "
            "İkinci bölümümüzde, **'Anne Ölümünün Tanımı (42 Gün Kuralı), Hesaplama Yöntemi, Doğrudan/Dolaylı Nedenler "
            "ve Türkiye'deki Güncel Durum (11.5 / 100.000)'** konularını derinlemesine inceleyeceğiz."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Bir ülkedeki obstetrik sağlık hizmetlerinin kalitesini, hastaneye erişimi ve acil müdahale gücünü ölçen en temel uluslararası gösterge nedir?",
                "Anne Ölüm Oranıdır (Maternal Mortality Ratio).",
                "100 bin canlı doğumda ifade edilen obstetrik ölüm göstergesi"
            ),
            make_branching_logic(
                "İl Sağlık Müdürlüğü AÇS şubesinde çalışan bir hekim, bölgesindeki anne ölümlerinin Türkiye ortalamasının 2 katı olduğunu saptıyor.",
                "Bu tabloyu düzeltmek için atılması gereken en öncelikli epidemiyolojik eylem hangisidir?",
                [
                    {
                        "text": "Maternal surveyans sistemiyle tüm anne ölümlerini inceleme komisyonuna sevk ederek doğrudan/dolaylı nedenleri tespit etmek ve acil obstetrik bakım sevk zincirini denetlemek",
                        "isCorrect": True,
                        "feedback": "Mükemmel Epidemiyolojik Yaklaşım: Nedenler bilinmeden önlem alınamaz; surveyans ve komisyon incelemesi eksik basamakları ortaya çıkarır."
                    },
                    {
                        "text": "Bölgedeki tüm gebelerin gebeliklerini sonlandırmasını tavsiye etmek",
                        "isCorrect": False,
                        "feedback": "Kabul edilemez ve etik dışı bir öneridir."
                    },
                    {
                        "text": "Verileri gizleyerek bakanlığa bildirmemek",
                        "isCorrect": False,
                        "feedback": "Yasal suçtur ve anne ölümlerinin devam etmesine yol açar."
                    }
                ]
            )
        ]
    })

    return slides
