# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 23: Ana-Çocuk Sağlığı Düzeyinin İzlenmesi
(Doç. Dr. Nergiz Sevinç - Halk Sağlığı ABD)
Bölüm 3: Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi (Slayt 21 - 30)
Checkpoint 3: Slayt 29
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic, make_flashcard
)

def get_section_3_slides():
    slides = []

    # Slayt 21: Doğum Öncesi Bakım (DÖB) Tanımı, Felsefesi ve Temel Hedefleri
    slides.append({
        "id": "k1-23-s21",
        "title": "Doğum Öncesi Bakım (DÖB) Tanımı, Felsefesi ve Temel Hedefleri",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 21,
        "narrative": (
            "Doğum Öncesi Bakım (DÖB; Antenatal Care); gebe kadının ve karnındaki fetüsün tüm gebelik süreci boyunca, "
            "eğitimli sağlık personeli (hekim ve ebe) tarafından düzenli aralıklarla izlenmesi, muayene edilmesi, "
            "gerekli laboratuvar taramalarından geçirilmesi ve koruyucu danışmanlık hizmetlerinin sunulmasıdır. "
            "DÖB'ün temel felsefesi şunları hedefler: "
            "1. Anne ve bebek ölümlerini (mortalite) ve hastalıklarını (morbidite) en aza indirmek, "
            "2. Ölü doğumları, düşük doğum ağırlıklı (DDA) bebekleri ve prematüriteyi önlemek, "
            "3. Gebelikte anneye bağışıklama (tetanoz), beslenme, hijyen ve psikolojik destek sağlamak, "
            "4. Doğumun nerede, nasıl ve kim tarafından yaptırılacağını önceden planlayarak acil obstetrik krizleri engellemektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Doğum öncesi bakım anne ve fetüsün tüm gebelik boyunca eğitimli sağlık personeli tarafından düzenli aralıklarla izlenmesidir.",
                "eğitimli sağlık personeli",
                "Hekim ve ebe gibi diplomalı sağlık profesyonelleri koşulu"
            ),
            make_micro_quiz(
                "Aşağıdakilerden hangisi Doğum Öncesi Bakım (DÖB) hizmetlerinin temel halk sağlığı hedefleri arasında YER ALMAZ?",
                {
                    "A": "Maternal ve perinatal ölümleri en aza indirmek",
                    "B": "Düşük doğum ağırlığı ve prematürite oranlarını azaltmak",
                    "C": "Gebeliğe eşlik eden hipertansiyon ve diyabeti erken evrede saptamak",
                    "D": "Tüm gebelerin mutlaka cerrahi sezaryen ile doğurtulmasını sağlamak",
                    "E": "Gebelere tetanoz aşısı ve demir desteği sağlamak"
                },
                "D",
                {
                    "A": "Temel hedeftir; Mortaliteyi azaltır.",
                    "B": "Temel hedeftir; Fetal gelişimi korur.",
                    "C": "Temel hedeftir; Sekonder koruma sağlar.",
                    "D": "Kesinlikle Hedef Değildir; DÖB normal vajinal doğumu özendirir, gereksiz sezaryeni önlemeyi hedefler.",
                    "E": "Temel hedeftir; Rutin profilaksidir."
                }
            ),
            make_active_recall(
                "Doğum öncesi bakımın (DÖB) bebek sağlığı açısından önlediği en kritik iki olumsuz perinatal sonuç nedir?",
                "Ölü doğumlar ile düşük doğum ağırlığı (ve prematürite) sıklığıdır.",
                "Fetal kayıp ve yetersiz kilo komplikasyonları"
            )
        ]
    })

    # Slayt 22: Dünyada DÖB'ün Doğuşu: 20. Yüzyıl Başı ve Johns Hopkins (1915)
    slides.append({
        "id": "k1-23-s22",
        "title": "Dünyada DÖB'ün Doğuşu: 20. Yüzyıl Başı ve Johns Hopkins (1915)",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 22,
        "narrative": (
            "Modern tıp tarihinde gebelik takibi oldukça yeni bir kavramdır; 19. yüzyıla kadar hekimler kadınları yalnızca "
            "doğum eylemi başladığında veya ölümcül bir komplikasyon (kanama, eklampsi) çıktığında görürdü. "
            "Dünyada DÖB'ün gelişimi şu kilometre taşlarıyla şekillenmiştir: "
            "1. **20. Yüzyıl Başı (ABD):** İlk olarak konjenital malformasyonları ve erken bebek ölümlerini önlemek amacıyla ortaya atıldı. "
            "Boston Hemşireler Birliği (Instructive District Nursing Association) 1901'de gebeleri evlerinde ziyaret etmeye başladı. "
            "2. **Johns Hopkins Hastanesi (1915):** 1915 yılında Johns Hopkins Hastanesi'nde yapılan çığır açıcı bilimsel çalışma, "
            "doğum öncesinde düzenli takip edilen gebelerde **prematüriteye ve enfeksiyona bağlı bebek ölümlerinin dramatik azaldığını** "
            "ilk kez kanıta dayalı olarak dünyaya duyurdu ve DÖB tüm tıp merkezlerinde zorunlu bir protokole dönüştü."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "1915 yılında Johns Hopkins Hastanesi doğum öncesi bakımın özellikle prematüriteye bağlı bebek ölümlerini belirgin azalttığını kanıtlamıştır.",
                "prematüriteye",
                "Erken doğuma bağlı gelişen neonatal komplikasyonlar"
            ),
            make_causal_chain(
                "Dünyada Doğum Öncesi Bakımın Tarihsel Evrimi",
                [
                    "1. Reaktif Dönem: 19. yüzyılda hekimler gebeyi sadece doğum anında veya krizde görürdü.",
                    "2. Boston Hemşireleri (1901): Gebelerin evlerinde rutin ziyaret edilmesiyle ilk koruyucu DÖB adımları atıldı.",
                    "3. Johns Hopkins Kanıtı (1915): Düzenli DÖB'ün prematürite ölümlerini düşürdüğü bilimsel olarak ispatlandı.",
                    "4. Küresel Standart: DSÖ ve ulusal sağlık sistemleri DÖB'ü zorunlu birinci basamak protokolü haline getirdi."
                ]
            ),
            make_active_recall(
                "Tıp tarihinde 1915 yılında doğum öncesi bakımın özellikle hangi nedene bağlı bebek ölümlerini azalttığını kanıtlayan ünlü akademik hastane hangisidir?",
                "Johns Hopkins Hastanesi (prematüriteye bağlı ölümleri azalttığını kanıtlamıştır).",
                "Dünya tıp literatürünün öncü Amerikan tıp merkezi"
            )
        ]
    })

    # Slayt 23: Türkiye'de DÖB Tarihçesi: 1961 Tarihli 224 Sayılı Kanun
    slides.append({
        "id": "k1-23-s23",
        "title": "Türkiye'de DÖB Tarihçesi: 1961 Tarihli 224 Sayılı Kanun",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 23,
        "narrative": (
            "Türkiye'de Ana-Çocuk Sağlığı ve Doğum Öncesi Bakımın kurumsal ve yasal miladı **1961 yılında çıkarılan 224 Sayılı "
            "'Sağlık Hizmetlerinin Sosyalleştirilmesine Dair Kanun'dur** (Ord. Prof. Dr. Nusret Fişek öncülüğünde): "
            "1. **Sağlık Ocakları Modeli:** Bu kanunla Türkiye genelinde kırsaldan kente piramidal bir birinci basamak ağı kuruldu. "
            "Gebe, lohusa, bebek ve çocuk takipleri sağlık ocaklarına ve köy sağlık evlerindeki ebelere birincil görev olarak verildi. "
            "2. **Evde ve Sahada Takip:** Sağlık ocağı personeli kendi bölgesindeki tüm haneleri periyodik ev ziyaretleriyle tarayarak "
            "gebeleri erken dönemde tespit edip kayıt altına aldı. "
            "3. **Entegre Hizmet:** Aşı, gebe takibi, aile planlaması ve beslenme aynı çatı altında ücretsiz sunuldu; "
            "Türkiye'nin anne ve bebek ölüm hızlarındaki ilk büyük tarihi düşüş bu 224 sayılı kanunla başladı."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Türkiye'de gebe, bebek ve çocuk takiplerini sağlık ocaklarına görev olarak veren kanun 1961 tarihli 224 sayılı kanundur.",
                "224 sayılı",
                "Sağlık hizmetlerinin sosyalleştirilmesine dair kanunun numarası"
            ),
            make_micro_quiz(
                "Türkiye'de gebe, bebek ve çocuk izlemlerini sağlık ocaklarının asli koruyucu görevi haline getiren ve sağlık hizmetlerinin sosyalleştirilmesini sağlayan 1961 tarihli kanun hangisidir?",
                {
                    "A": "1593 Sayılı Umumi Hıfzıssıhha Kanunu",
                    "B": "224 Sayılı Sağlık Hizmetlerinin Sosyalleştirilmesine Dair Kanun",
                    "C": "3359 Sayılı Sağlık Hizmetleri Temel Kanunu",
                    "D": "5258 Sayılı Aile Hekimliği Kanunu",
                    "E": "657 Sayılı Devlet Memurları Kanunu"
                },
                "B",
                {
                    "A": "Yanlıştır; 1930 tarihli Umumi Hıfzıssıhha genel halk sağlığı kanunudur.",
                    "B": "Doğrudur; 1961 tarihli 224 sayılı kanun sağlık ocaklarını ve DÖB görevini kuran sosyalleştirme kanunudur.",
                    "C": "Yanlıştır; 1987 tarihli temel kanundur.",
                    "D": "Yanlıştır; 2004 tarihli aile hekimliği kanunudur.",
                    "E": "Yanlıştır; Memur özlük kanunudur."
                }
            ),
            make_active_recall(
                "1961 yılında çıkarılan 224 sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi Kanunu'nun mimarı olan ünlü Türk halk sağlığı hocası kimdir?",
                "Prof. Dr. Nusret Fişek'tir.",
                "Hacettepe Halk Sağlığı kurucusu ordinaryüs hekim"
            )
        ]
    })

    # Slayt 24: Tarihsel Dönemlere Göre Gebe İzlem Sayısı Evrimi (13'ten 4'e)
    slides.append({
        "id": "k1-23-s24",
        "title": "Tarihsel Dönemlere Göre Gebe İzlem Sayısı Evrimi (13'ten 4'e)",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 24,
        "narrative": (
            "Türkiye'de sağlık politikalarının ve bilimsel kanıtların ışığında önerilen rutin gebe izlem sayıları tarihsel olarak değişmiştir: "
            "1. **1961 Sosyalleştirme Dönemi (224 Sayılı Kanun):** Toplam **13 KEZ** izlem önerilirdi. "
            "Takvim: Gebeliğin 7. ay sonuna kadar ayda 1 kez (7 izlem), 8. ayda 15 günde bir (2 izlem), 9. ayda haftada 1 kez (4 izlem) = Toplam 13 izlem. "
            "Bu rejim son derece yoğundu ancak sağlık personeli eksikliği ve gebe uyumsuzluğu nedeniyle sahada tam uygulanamadı. "
            "2. **2001 Yönergesi:** DSÖ'nün maliyet-etkinlik modelleri doğrultusunda izlem sayısı **6 KEZ** olarak revize edildi. "
            "3. **2009 Aile Hekimliği DÖB Yönetim Rehberi ve Güncel Dönem:** Rutin düşük riskli gebelikte **EN AZ 4 KEZ** izlem altın standart oldu. "
            "Araştırmalar, nitelikli yapılan 4 izlemin anne ve bebek mortalitesini önlemede 13 izlem kadar başarılı olduğunu kanıtlamıştır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "1961 yılı 224 sayılı kanun döneminde bir gebeye toplam 13 kez izlem yapılması önerilmekteydi.",
                "13 kez",
                "Sosyalleştirme döneminde 7. aya kadar ayda bir, 8. ayda iki haftada bir ve 9. ayda haftalık izlem toplamı"
            ),
            make_table(
                "Türkiye'de Tarihsel Dönemlere Göre Önerilen Rutin Gebe İzlem Sayısı",
                ["Tarihsel Dönem / Mevzuat", "Önerilen Gebe İzlem Sayısı", "Uygulama Takvimi Detayı"],
                [
                    [
                        "1961 Sosyalleştirme (224 Sayılı Kanun)",
                        {"text": "13 kez", "isMasked": True, "hint": "Ayda bir, on beş günde bir ve haftalık takvim toplamı"},
                        "7. aya kadar ayda 1, 8. ayda 15 günde 1, 9. ayda haftada 1"
                    ],
                    ["2001 Bakanlık Yönergesi", "6 kez", "Kritik haftalara odaklı ara model"],
                    ["2009 Aile Hekimliği Rehberi ve Güncel", "En az 4 kez", "0-14, 18-24, 28-32 ve 36-38. haftalar"]
                ]
            ),
            make_micro_quiz(
                "Türkiye'de 1961 tarihli 224 sayılı Sosyalleştirme Kanunu döneminde bir gebenin doğumuna kadar toplam kaç kez izlenmesi öngörülmekteydi?",
                {
                    "A": "2 kez",
                    "B": "4 kez",
                    "C": "6 kez",
                    "D": "13 kez",
                    "E": "20 kez"
                },
                "D",
                {
                    "A": "Yanlıştır; Yetersiz izlemdir.",
                    "B": "Yanlıştır; Günümüzdeki standarttır.",
                    "C": "Yanlıştır; 2001 yönergesi sayısıdır.",
                    "D": "Doğrudur; 224 sayılı kanun döneminde 7 aya kadar ayda 1 (7), 8. ayda 2, 9. ayda 4 olmak üzere toplam 13 izlem öngörülürdü.",
                    "E": "Yanlıştır; Fazladır."
                }
            )
        ]
    })

    # Slayt 25: 2003 Sağlıkta Dönüşüm Programı ve Aile Hekimliği DÖB Rehberi
    slides.append({
        "id": "k1-23-s25",
        "title": "2003 Sağlıkta Dönüşüm Programı ve Aile Hekimliği DÖB Rehberi",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 25,
        "narrative": (
            "2003 yılında başlatılan **Sağlıkta Dönüşüm Programı (SDP)**, Türkiye'de ana-çocuk sağlığı hizmetlerinde devrimsel bir sıçrama yarattı: "
            "1. **Bireye Yönelik Koruyucu Hizmet:** Sağlık ocaklarının coğrafi nüfus yapısından, 'kişiye kayıtlı Aile Hekimliği Modeli'ne geçildi. "
            "Gebe ve bebek takipleri aile hekiminin maaşına doğrudan etki eden **pozitif/negatif performans kriteri** yapıldı. "
            "İzlem yapılmadığında hekimin maaşından kesinti yapılması, sahadaki gebe kaçaklarını neredeyse sıfıra indirdi. "
            "2. **2009 DÖB Yönetim Rehberi:** Sağlık Bakanlığı, kanıta dayalı tıp ilkeleriyle DÖB'ü standardize etti. "
            "Gebe izlemleri 4 basamağa ayrıldı, her basamağın laboratuvar testleri, ultrason endikasyonları, "
            "sevk kriterleri ve danışmanlık şablonları algoritmik hale getirildi. "
            "Bu sayede Türkiye'de 4+ DÖB alma oranı %50'lerden %90'ın üzerine tırmandı."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "2003 Sağlıkta Dönüşüm Programı ile gebe ve bebek izlemleri aile hekiminin performans kriterleri arasına alınarak izlem oranları artırılmıştır.",
                "performans kriterleri",
                "Hekimin hizmet sunum kalitesini ve takibini denetleyen yönetsel mekanizma"
            ),
            make_before_after(
                "DÖB Kapsayıcılığı: Sağlıkta Dönüşüm Öncesi vs Sonrası",
                "Dönüşüm Öncesi (2000'lerin Başı)",
                "4 ve üzeri DÖB alma oranı yüzde ellilerdedir; kayıt dışı gebelikler yaygındır, kırsal alanda izlem kaçağı büyüktür.",
                "Dönüşüm Sonrası (Güncel Dönem)",
                "4 ve üzeri DÖB alma oranı yüzde doksanı aşmıştır; MERNİS ve Bakanlık elektronik takip sistemiyle gebe kaçağı minimize edilmiştir.",
                "DÖB kapsayıcılık oranlarındaki tarihsel sıçrama"
            ),
            make_active_recall(
                "Türkiye'de aile hekimliği sisteminde gebe izlemlerinin aksatılmadan yapılmasını sağlayan en güçlü yönetsel motivasyon aracı nedir?",
                "Gebe ve bebek izlemlerinin hekimin aylık maaşına doğrudan yansıyan negatif performans kriteri olmasıdır.",
                "Hekim denetim ve performans mekanizması"
            )
        ]
    })

    # Slayt 26: Kessner İndeksi Nedir? Bakım Kalitesinin Ölçülmesi
    slides.append({
        "id": "k1-23-s26",
        "title": "Kessner İndeksi Nedir? Bakım Kalitesinin Ölçülmesi",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 26,
        "narrative": (
            "Uluslararası epidemiyolojide doğum öncesi bakımın sadece yapılıp yapılmadığını değil, **bakımın nitelik ve yeterliliğini** "
            "ölçmek için geliştirilmiş en saygın indeks **Kessner İndeksi'dir (Kessner Index)**. "
            "Kessner İndeksi bir gebenin aldığı bakımın yeterliliğini 3 temel parametrenin kombinasyonuyla hesaplar: "
            "1. **DÖB'ün Hangi Gebelik Ayında Başladığı:** Bakımın ilk trimesterde (ilk 3 ayda) başlaması esastır; geç başlayan bakım kalitesizdir. "
            "2. **Doğuma Kadar Kaç Kez İzlendiği (İzlem Sayısı):** Gestasyonel yaşa göre yapılan toplam vizit sayısı (en az 4 ve üzeri). "
            "3. **Bakımın Yapıldığı Yer ve Veren Kişi:** Bakımın ruhsatlı bir sağlık kuruluşunda eğitimli sağlık personeli (doktor/ebe) tarafından verilmesi. "
            "Bu üç kritere göre gebeler: **'Yeterli Bakım Alanlar'**, **'Orta Düzey Bakım Alanlar'** ve **'Yetersiz Bakım Alanlar'** olarak kategorize edilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Doğum öncesi bakımın kalitesini izlemin başlama ayı, izlem sayısı ve bakımın yapıldığı yere göre değerlendiren ölçüt Kessner indeksidir.",
                "Kessner indeksi",
                "DÖB yeterlilik ve nitelik düzeyini sınıflandıran uluslararası endeks"
            ),
            make_table(
                "Kessner İndeksi Yeterlilik Sınıflaması Parametreleri",
                ["Kessner Bileşeni", "Yeterli Bakım Kriteri", "Yetersiz Bakım Kriteri", "Klinik Değerlendirme"],
                [
                    [
                        "İzleme Başlama Zamanı",
                        "İlk 3 ay içinde (Trimester 1)",
                        {"text": "İkinci veya üçüncü trimesterde", "isMasked": True, "hint": "Gebeliğin 4. ayından sonra geç başvuru"},
                        "Erken anomali ve risk tespit kabiliyeti"
                    ],
                    ["Toplam İzlem Sayısı", "Gestasyonel haftaya göre tam (≥4)", "3 veya daha az izlem", "Periyodik komplikasyon yakalama gücü"],
                    ["Bakımı Veren / Yer", "Sağlık personeli / Sağlık tesisi", "Geleneksel uygulayıcı / Ev ortamı", "Tıbbi müdahale ve hijyen kalitesi"]
                ]
            ),
            make_micro_quiz(
                "Doğum öncesi bakımın yeterliliğini değerlendiren Kessner İndeksi'nin hesaplanmasında aşağıdaki parametrelerden hangisi KULLANILMAZ?",
                {
                    "A": "DÖB'ün hangi gebelik ayında başladığı",
                    "B": "Doğuma kadar kaç kez izlem yapıldığı",
                    "C": "Bakımın yapıldığı yer ve sağlık personeli tarafından verilip verilmediği",
                    "D": "Bebeğin doğum anında hangi kan grubunda doğduğu",
                    "E": "Gestasyonel yaşa uygun izlem sıklığının sağlanması"
                },
                "D",
                {
                    "A": "Kullanılır; Başlama ayı temel kriterdir.",
                    "B": "Kullanılır; İzlem sayısı temel kriterdir.",
                    "C": "Kullanılır; Hizmet ortamı ve personel temel kriterdir.",
                    "D": "Kullanılmaz; Bebeğin kan grubu Kessner yeterlilik indeksi parametresi değildir.",
                    "E": "Kullanılır; Gestasyonel yaşa göre izlem uyumu değerlendirilir."
                }
            )
        ]
    })

    # Slayt 27: Yeterli Bakım Almanın Üçlü Altın Kuralı (Sınav Spotu)
    slides.append({
        "id": "k1-23-s27",
        "title": "Yeterli Bakım Almanın Üçlü Altın Kuralı (Sınav Spotu)",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 27,
        "narrative": (
            "Halk sağlığı sınavlarında ve tıp kurullarında en sık sorgulanan çekirdek bilgi **'Yeterli Doğum Öncesi Bakım Alma Ölçütleri'dir**. "
            "Sağlık Bakanlığı ve uluslararası kılavuzlara göre bir gebenin 'Yeterli Bakım Aldı' sayılabilmesi için "
            "şu **ÜÇ ŞARTIN BİRDEN EKSİKSİZ SAĞLANMASI** zorunludur: "
            "1. **Şart 1 (Yetkin Personel):** Bakımın diplomalı ve eğitimli sağlık personeli (doktor veya ebe) tarafından verilmesi. "
            "2. **Şart 2 (Zamanında Başlama):** İzlemin **gebeligin ilk 3 ayı (ilk trimester / 0-14. hafta) içinde başlamış olması**. "
            "Eğer bir kadın gebeliğin 4. veya 5. ayında doktora gitmişse, sonrasında 10 kez gitse bile 'Yeterli Bakım' ölçütünü KARŞILAMAZ! "
            "3. **Şart 3 (Yeterli Sayı):** Gebelik boyunca **en az 4 kez** nitelikli izlem yapılmış olmasıdır. "
            "Bu üç şarttan biri eksikse bakım 'Orta' veya 'Yetersiz' olarak tescil edilir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "Sağlık Bakanlığı kriterlerine göre yeterli doğum öncesi bakım almanın ilk zamansal kuralı izlemin gebeliğin ilk üç ayında başlamasıdır.",
                "ilk üç ayında",
                "Birinci trimesteri kapsayan zamansal eşik kuralı"
            ),
            make_micro_quiz(
                "Sağlık Bakanlığı ve halk sağlığı standartlarına göre aşağıdakilerden hangisi 'Doğum Öncesinde Yeterli Bakım Alma' kriterlerinden biri DEĞİLDİR? [Kurul 1 Çıkmış Soru]",
                {
                    "A": "İzlemin sağlık personeli (hekim/ebe) tarafından yapılması",
                    "B": "İzlemin gebeliğin ilk 3 ayı içinde başlamış olması",
                    "C": "Gebelik boyunca en az 4 kere izlem yapılmış olması",
                    "D": "İzlemin gebeliğin 2. veya 3. ayında başlamış olması",
                    "E": "İzlemin gebeliğin 5. ayında başlamış olması"
                },
                "E",
                {
                    "A": "Kriterdir; Sağlık personeli şarttır.",
                    "B": "Kriterdir; İlk 3 ayda başlama altın kuraldır.",
                    "C": "Kriterdir; En az 4 izlem zorunludur.",
                    "D": "Kriterdir; 2 veya 3. ay ilk 3 ayın içindedir, yeterlidir.",
                    "E": "Kriter Değildir (Çıkmış Soru Doğru Cevabı); 5. ayda başlayan izlem geç başlamıştır; sonrasında çok izlem yapılsa bile 'yeterli bakım' kriterini bozmuş olur."
                }
            ),
            make_active_recall(
                "Bir gebenin gebeliği boyunca toplam 8 kez kadın doğum uzmanına muayene olmasına rağmen 'Yeterli Bakım Aldı' sınıfına girememesinin en olası nedeni nedir?",
                "İlk muayenesine gebeliğin ilk 3 ayından sonra (örneğin 4. veya 5. ayda) çok geç başlamış olmasıdır.",
                "Geç başvuru ve yeterli bakım kriteri kaybı"
            )
        ]
    })

    # Slayt 28: Türkiye'de Durum (TNSA-2018 Verileri) ve Sezaryen Sorunu (%52)
    slides.append({
        "id": "k1-23-s28",
        "title": "Türkiye'de Durum (TNSA-2018 Verileri) ve Sezaryen Sorunu (%52)",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 28,
        "narrative": (
            "Türkiye Nüfus ve Sağlık Araştırması (TNSA-2018) ülkemizdeki obstetrik bakımın hem başarılarını hem de ciddi yapısal sorunlarını ortaya koymaktadır: "
            "1. **Büyük Başarılar:** "
            "- Uzman sağlık personelinden DÖB alma oranı **%96'nın üzerindedir**, "
            "- En az 4 kez DÖB alma oranı Türkiye genelinde **%90'dır** (kentsel %92, kırsal %84), "
            "- Sağlık kuruluşunda ve uzman yardımıyla doğum oranı **%99'dur** (geleneksel doğumlar marjinalleşmiştir), "
            "- Gebelikte demir desteği ve tetanoz aşısı alma oranı **%81'dir**. "
            "2. **Ciddi Halk Sağlığı Sorunu: SEZARYEN (%52):** "
            "Dünya Sağlık Örgütü tıbbi olarak kabul edilebilir sezaryen oranının **%10-15** arasında olması gerektiğini bildirir. "
            "Türkiye'de ise tüm doğumların **%52'si sezaryen ile gerçekleşmektedir**; bu oranla dünyada ilk sıralardadır. "
            "Bu sezaryenlerin büyük kısmı tıbbi zorunluluktan değil, mediko-legal korkular, hekim konforu ve elektif taleplerden kaynaklanmaktadır."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_cloze(
                "TNSA-2018 verilerine göre Türkiye'de sezaryen doğum oranı yüzde elli iki olup DSÖ'nün önerdiği yüzde on beş sınırının çok üzerindedir.",
                "yüzde elli iki",
                "Türkiye'deki toplam sezaryen doğum yüzdesi"
            ),
            make_table(
                "TNSA-2018 Türkiye Doğum Öncesi ve Doğum Göstergeleri",
                ["Obstetrik Gösterge", "TNSA-2018 Değeri", "Halk Sağlığı Yorumu"],
                [
                    ["Uzman Sağlık Personelinden DÖB", "> %96", "Hizmete erişim mükemmel"],
                    ["En Az 4 Kez DÖB Alma Oranı", "~%90 (Kırsal %84)", "DÖB kapsayıcılığı ulusal standartta"],
                    ["Hastanede / Sağlık Tesisinde Doğum", "%99", "Ev doğumları ve enfeksiyon sıfıra yakın"],
                    [
                        "Toplam Sezaryen Doğum Oranı",
                        {"text": "%52", "isMasked": True, "hint": "Tüm doğumların yarıdan fazlasına denk gelen ameliyat oranı"},
                        "Aşırı yüksek; DSÖ önerisinin (%10-15) üç katından fazla"
                    ],
                    ["İlk 41 Saatte Doğum Sonrası Bakım", "İlk doğumda %97, sonrakilerde %90", "Erken lohusalık takibi güçlü"]
                ]
            ),
            make_micro_quiz(
                "TNSA-2018 verilerine göre Türkiye'deki doğum hizmetleri ile ilgili aşağıdakilerden hangisi endişe verici bir halk sağlığı sorunudur?",
                {
                    "A": "Sağlık kuruluşunda doğum oranının %50'nin altına düşmesi",
                    "B": "Sezaryen oranının tüm doğumların %52'sine ulaşarak DSÖ normlarının kat kat üzerine çıkması",
                    "C": "Gebelerde tetanoz aşılama oranının %10'a gerilemesi",
                    "D": "DÖB hizmetlerinin sadece özel hastanelerde ücretli verilmesi",
                    "E": "Doğumların çoğunun diplomasız mahalle ebelerince yaptırılması"
                },
                "B",
                {
                    "A": "Yanlıştır; Hastanede doğum %99 ile rekor düzeydedir.",
                    "B": "Doğrudur; %52 sezaryen oranı medikal açıdan aşırı yüksektir ve ciddi bir halk sağlığı sorunudur.",
                    "C": "Yanlıştır; Tetanoz aşılama oranı %81'dir.",
                    "D": "Yanlıştır; Birinci basamakta ve devlet hastanelerinde tamamen ücretsizdir.",
                    "E": "Yanlıştır; Uzman sağlık personeli eşliğinde doğum %99'dur."
                }
            )
        ]
    })

    # Slayt 29: [TEKRAR SAYFASI - CHECKPOINT 3] DÖB Tarihçesi ve Kessner İndeksi
    slides.append({
        "id": "k1-23-s29",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 3] DÖB Tarihçesi ve Kessner İndeksi",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 29,
        "narrative": (
            "Bu üçüncü checkpoint sayfasında, doğum öncesi bakımın tarihsel köklerini, Kessner indeksini ve yeterlilik kurallarını özetliyoruz: "
            "1. **Tarihçe:** 1915 Johns Hopkins çalışması DÖB'ün prematürite ölümlerini düşürdüğünü kanıtladı. "
            "2. **Türkiye'de Sosyalleştirme:** 1961 tarihli 224 sayılı kanunla DÖB sağlık ocaklarına verildi; o dönemde toplam 13 izlem önerilirdi. "
            "3. **İzlem Evrimi:** 1961'de 13 izlem $\\rightarrow$ 2001'de 6 izlem $\\rightarrow$ 2009 ve günümüzde en az 4 izlem. "
            "4. **Kessner İndeksi:** İzleme başlama ayı, toplam izlem sayısı ve bakım yeri/personeli bileşenlerinden oluşur. "
            "5. **Yeterli DÖB Üçlü Kuralı:** Sağlık personeli + gebeliğin İLK 3 AYINDA başlama + EN AZ 4 İZLEM (5. ayda başlayan yetersizdir!). "
            "6. **TNSA-2018:** 4+ DÖB %90, hastanede doğum %99, ancak sezaryen oranı %52 ile kabul edilemez yüksekliktedir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "flashcards": [
            make_flashcard(
                "k1-23-fc-s29-1",
                "Bir gebenin doğum öncesinde 'Yeterli Bakım Aldı' kabul edilebilmesi için izlemin en geç gebeliğin kaçıncı ayında başlamış olması şarttır?",
                "Gebeliğin ilk üç ayı içinde başlamış olması şarttır.",
                "Erken gestasyonel doksan günlük süre sınırı",
                "DÖB Yeterlilik Kriterleri"
            ),
            make_flashcard(
                "k1-23-fc-s29-2",
                "Türkiye'de 1961 yılında çıkarılan 224 sayılı kanun döneminde bir gebeye doğumuna kadar toplam kaç izlem önerilmekteydi?",
                "Toplam on üç kez izlem yapılması önerilmekteydi.",
                "Sosyalleştirme mevzuatının öngördüğü periyodik kontrol adedi",
                "AÇS Tarihçesi"
            ),
            make_flashcard(
                "k1-23-fc-s29-3",
                "TNSA-2018 verilerine göre Türkiye'de Dünya Sağlık Örgütü'nün kabul edilebilir sınırının kat kat üzerinde olan sezaryen doğum oranı yüzde kaçtır?",
                "Tüm doğumların yüzde elli ikisidir (%52).",
                "Yarısından fazlasına denk gelen cerrahi operasyon sıklığı",
                "Obstetrik İstatistikler"
            )
        ],
        "interactiveElements": [
            make_table(
                "Özet Karşılaştırma: DÖB Yeterlilik Ölçütleri",
                ["Ölçüt Kriteri", "Yeterli Bakım Standardı", "Yetersiz Bakım Durumu"],
                [
                    ["Bakımı Veren Personel", "Hekim veya Ebe (Yetkili personel)", "Geleneksel uygulayıcı veya akraba"],
                    [
                        "İzleme Başlama Zamanı",
                        {"text": "İlk 3 ay içinde (Trimester 1)", "isMasked": True, "hint": "Kessner indeksine göre erken başvuru süresi"},
                        "Gebeliğin 4. ayı veya daha geç başvuru"
                    ],
                    ["Toplam İzlem Adedi", "Gebelik boyunca en az 4 izlem", "3 veya daha az izlem"],
                    ["Sezaryen Oranı", "DSÖ normu %10 - 15", "Türkiye güncel düzeyi %52"]
                ]
            )
        ]
    })

    # Slayt 30: Bölüm Özeti: DÖB İlkelerinden Gebe İzlem Protokollerine Geçiş
    slides.append({
        "id": "k1-23-s30",
        "title": "Bölüm Özeti: DÖB İlkelerinden Gebe İzlem Protokollerine Geçiş",
        "section": "Doğum Öncesi Bakım (DÖB): Tarihçe, Yeterlilik ve Kessner İndeksi",
        "slideNumber": 30,
        "narrative": (
            "DÖB'ün tarihsel serüveni ve Kessner indeksinin ortaya koyduğu gibi, gebelik takibinde asıl belirleyici olan "
            "vizitlerin sayısı kadar doğru zamanda ve doğru içerikle yapılmasıdır. "
            "İlk trimesterde başlayan, yetkin sağlık personeliyle yürütülen ve en az 4 izlemi içeren bir DÖB modeli; "
            "anne ve fetüsü ölümcül risklerden korur. "
            "Türkiye'de Sağlık Bakanlığı'nın yayımladığı **Doğum Öncesi Bakım Yönetim Rehberi**, "
            "gebelik sürecini 4 kritik izleme bölerek her vizitte yapılacak öykü, fizik muayene, laboratuvar testleri "
            "ve risk taramalarını adım adım standardize etmiştir. "
            "Dördüncü bölümümüzde, **'1. Gebe İzlemi (0-14. Hafta) ve 2. Gebe İzleminin (18-24. Hafta) "
            "Ayrıntılı İçeriği, Fetal Kalp Sesleri (FKS), İndirekt Coombs ve Glukoz Taraması'** incelenecektir."
        ),
        "sourcePdf": "Halk Sağlığı ABD - Ana-Çocuk Sağlığı Düzeyinin İzlenmesi",
        "interactiveElements": [
            make_active_recall(
                "Sağlık Bakanlığı Aile Hekimliği DÖB Yönetim Rehberi'ne göre düşük riskli bir gebelikte rutin olarak önerilen standart izlem sayısı kaçtır?",
                "Gebelik boyunca toplam 4 kez (en az 4 izlem) yapılmasıdır.",
                "Güncel ulusal gebe izlem sayısı standardı"
            ),
            make_branching_logic(
                "32 haftalık gebe olan bir kadın aile hekimine ilk kez başvuruyor. Daha önce hiçbir sağlık kuruluşuna gitmediğini, bu ilk kontrolü olduğunu belirtiyor.",
                "Bu gebenin Kessner İndeksi ve DÖB yeterlilik değerlendirmesi hangisidir?",
                [
                    {
                        "text": "Yetersiz Bakım: Gebeliğin ilk 3 ayı çoktan geçmiş ve 32. haftaya kadar hiçbir izlem almamıştır; bundan sonra sık izlense dahi Kessner indeksine göre yetersiz bakım kategorisindedir",
                        "isCorrect": True,
                        "feedback": "Doğru Epidemiyolojik Yargı: İlk trimester kaçırılmıştır ve izlem sayısı yetersizdir; Kessner indeksine göre bakım kesinlikle yetersizdir."
                    },
                    {
                        "text": "Mükemmel Bakım: Doğuma henüz 8 hafta olduğu için tüm testler hızlıca yapılarak yeterli bakıma çevrilebilir",
                        "isCorrect": False,
                        "feedback": "Hatalı: İlk trimester anomali ve risk taramaları geri döndürülemez biçimde kaçırılmıştır."
                    },
                    {
                        "text": "Orta Düzey Bakım: 30 haftadan sonra gelen her gebe otomatikman orta düzey sayılır",
                        "isCorrect": False,
                        "feedback": "Hatalı: 32. haftada ilk kez gelen gebe yetersiz bakım kategorisindedir."
                    }
                ]
            )
        ]
    })

    return slides
