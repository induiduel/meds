#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 1: Patolojinin Tanımı, Kapsamı ve Fizyopatoloji İlişkisi (Adımlar 1 - 9)
Ders: Tıbbi Patoloji - Patolojiye Giriş
Öğretim Üyesi: Prof. Dr. Hikmet Keleş
"""

from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        # Adım 1
        {
            "slideNumber": 1,
            "title": "Patoloji Kavramı: Tanımı, Etimolojisi ve Tıptaki Anlamı",
            "subtitle": "Hastalık bilimi olarak patoloji; etiyoloji, patogenez, morfoloji ve klinik sonuçların bütüncül incelemesidir.",
            "badge": "Temel Kavram",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Patoloji**, etimolojik kökenini Yunanca **pathos** (hastalık) ve **logos** (bilim) sözcüklerinden alan, kelime anlamıyla ==hastalık bilimi== anlamına gelen bağımsız tıp dalıdır.

Klasik tıp nosolojisinde patoloji dört temel boyutu inceler: Hastalığı başlatan nedenler (**etiyoloji**), hücre ve dokularda tetiklenen moleküler ve biyokimyasal basamaklar (**patogenez**), organ düzeyinde beliren yapısal değişiklikler (**morfoloji**) ve bu hasarın yol açtığı fonksiyonel bozukluklar (**klinikopatolojik sonuç**). Patoloji, temel tıp bilimleri ile klinik branşlar arasında köprü kurarak kesin tanıyı koyar ve hedefe yönelik tedaviyi yönlendirir.

> [TEMEL İLKE] Patoloji; hücresel anomalilerden organ disfonksiyonuna kadar tüm hastalık sürecini etiyoloji, patogenez, morfoloji ve klinik sonuç ekseninde aydınlatır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Etimoloji", "desc": "Pathos (hastalık/ıstırap) ve logos (bilim) köklerinden türemiştir.", "isKey": True},
                    {"title": "Dört Temel Boyut", "desc": "Etiyoloji, patogenez, morfolojik değişiklikler ve klinik sonuçlar eksiksiz incelenir.", "isKey": True},
                    {"title": "Köprü Fonksiyonu", "desc": "Temel tıp bilimleri (anatomi, histoloji, biyokimya) ile klinik branşlar arasında tanısal köprüdür.", "isKey": False}
                ],
                "table": {
                    "title": "Patolojinin Dört Temel İnceleme Boyutu",
                    "headers": ["Boyut", "Kapsam", "Klinik Karşılık"],
                    "rows": [
                        ["Etiyoloji", "Hastalığı başlatan intrinsik veya ekstrinsik nedenler", "Genetik mutasyon, enfeksiyöz patojen, toksik madde"],
                        ["Patogenez", "Hücre ve dokularda gelişen biyolojik olaylar zinciri", "İskemi, inflamatuvar kaskat, apoptoz, nekroz"],
                        ["Morfoloji", "Organ ve dokuda gözlenen yapısal/görsel değişim", "Makroskobik kitle, mikroskobik hücresel atipi"],
                        ["Klinik Sonuç", "Yapısal hasarın hastada oluşturduğu belirti ve bulgular", "Ağrı, sarılık, organ yetmezliği, laboratuvar sapmaları"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patoloji sözcüğü pathos (hastalık) ve logos (bilim) kelimelerinden türer ve hastalık bilimi demektir.",
                "📌 [SINAV SPOTU] Patolojinin dört temel inceleme ayağı: Etiyoloji, patogenez, morfolojik değişiklik ve klinik sonuçtur.",
                "🚨 [KRİTİK UYARI] Patoloji sadece ölü dokuları değil; yaşayan hastadan alınan cerrahi biyopsileri de kesin tanı amacıyla inceler."
            ],
            "medicalTerms": [
                {"term": "Etiyoloji", "explanation": "Bir hastalığın ortaya çıkışına yol açan genetik veya çevresel başlangıç nedenidir."},
                {"term": "Patogenez", "explanation": "Etiyolojik etkenin hücresel hasar oluşturana dek tetiklediği biyolojik olaylar zinciridir."},
                {"term": "Morfoloji", "explanation": "Hastalık sürecinde doku ve hücrelerde gözlenen yapısal ve biçimsel değişikliklerdir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patolojinin incelediği temel süreçler göz önüne alındığında, aşağıdakilerden hangisi patolojinin dört ana bileşeninden biri değildir?",
                    {
                        "A": "Hastalığın başlangıç nedenlerini araştıran etiyoloji",
                        "B": "Moleküler ve hücresel mekanizmalar zinciri olan patogenez",
                        "C": "Hücre ve doku düzeyindeki yapısal biçimsel değişimleri gösteren morfoloji",
                        "D": "Hastalığın toplumsal sigorta maliyetini hesaplayan aktüeryal analiz",
                        "E": "Yapısal hasarın hastada doğurduğu işlevsel ve klinik sonuçlar"
                    },
                    "D",
                    {
                        "A": "Etiyoloji hastalığın genetik veya çevresel nedenini araştıran temel ayaktır.",
                        "B": "Patogenez nedenden sonuca uzanan biyolojik gelişim mekanizmasını tanımlar.",
                        "C": "Morfoloji hücre ve doku düzeyindeki yapısal biçimsel değişimleri inceler.",
                        "D": "Doğru: Aktüeryal analiz sağlık sigortacılığına ait olup patolojinin konusu değildir.",
                        "E": "Klinikopatolojik sonuçlar morfolojik hasarın hastadaki yansımalarını açıklar."
                    }
                ),
                make_cloze(
                    "Patoloji kelimesi Yunanca hastalık ve ıstırap anlamına gelen [pathos] ile bilim ve akıl anlamına gelen logos sözcüklerinin birleşiminden oluşmuştur.",
                    "pathos",
                    "Hastalık ve acı anlamına gelen Grekçe kök"
                )
            ]
        },

        # Adım 2
        {
            "slideNumber": 2,
            "title": "Patolojinin Düzeyleri: Molekülden Tüm Organizmaya Bütüncül Bakış",
            "subtitle": "Patolojik süreçler genetik ve moleküler düzeyde başlar, hücresel ve dokusal düzeyde ilerleyerek tüm organizmayı etkiler.",
            "badge": "Hiyerarşik Düzeyler",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojinin inceleme sahası tek bir mikroskobik büyütme ile sınırlı olmayıp biyolojik organizasyonun tüm basamaklarını kapsayan ==hiyerarşik bir inceleme zinciridir==.

Süreç en temelde DNA hasarı ve mutasyonları kapsayan **moleküler ve genetik düzeyde** başlar; ardından mitokondriyal hasar ve apoptoz gibi **hücresel düzeye** yansır. Hücrelerin oluşturduğu **doku düzeyinde** inflamasyon, nekroz ve neoplazi şekillenir. Doku hasarı ilerlediğinde organ büyümesi veya parankim yıkımıyla **organ düzeyi** ve nihayet organ yetmezliğine bağlı sistemik bozukluklarla **tüm organizma düzeyi** etkilenir. Modern patoloji, mikroskobik morfolojiyi moleküler testlerle birleştirerek bu hiyerarşiyi eksiksiz değerlendirir.

> [KLİNİK İPUCU] Patolojik süreçler molekülden başlayıp tüm organizmaya yayılan hiyerarşik bir hasar zinciri izler.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Moleküler Düzey", "desc": "Gen mutasyonları, epigenetik susturma ve protein sentez kusurları incelenir.", "isKey": True},
                    {"title": "Hücresel Düzey", "desc": "Hücre zedelenmesi, inklüzyonlar, apoptoz ve nekroz morfolojisi değerlendirilir.", "isKey": True},
                    {"title": "Doku ve Organ Düzeyi", "desc": "İnflamasyon, granülom, tümöral infiltrasyon ve organ boyut/kıvam değişimleri saptanır.", "isKey": True}
                ],
                "table": {
                    "title": "Patolojik İnceleme Basamakları ve Klinik Örnekler",
                    "headers": ["Organizasyon Düzeyi", "Patolojik İnceleme Yöntemi", "Klinik Patoloji Örneği"],
                    "rows": [
                        ["Moleküler Düzey", "PCR, NGS, Floresan In Situ Hibridizasyon (FISH)", "Akciğer adenokarsinomunda EGFR ekzon 19 delesyonu"],
                        ["Hücresel Düzey", "Işık mikroskopisi, İİAS, Transmisyon Elektron Mikroskobu", "Karaciğer hepatositinde hidropik şişme ve balonlaşma"],
                        ["Doku Düzeyi", "Rutin Hematoksilen-Eozin ve özel histokimya boyamaları", "Tüberküloz lenfadenitinde kazeifiye granülomatöz inflamasyon"],
                        ["Organ Düzeyi", "Makroskobik disseksiyon ve cerrahi patoloji incelemesi", "Kronik piyelonefritte böbrek korteksinde U şeklinde skar dokusu"],
                        ["Tüm Organizma", "Klinik otopsi ve adli ölüm muayenesi", "Aort disseksiyonu rüptürüne bağlı kardiyak tamponad ve şok"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojinin inceleme basamakları: Moleküler $\\to$ Hücresel $\\to$ Doku $\\to$ Organ $\\to$ Tüm organizma zinciridir.",
                "📌 [SINAV SPOTU] Tümörlerin moleküler sınıflaması (hedefe yönelik tedavi) patolojinin moleküler düzeydeki başarısıdır.",
                "🚨 [KRİTİK UYARI] Makroskobik inceleme yapılmadan mikroskobik incelemeye geçilemez; organ düzeyindeki lezyonun haritası makroskopide çıkarılır."
            ],
            "medicalTerms": [
                {"term": "Hücresel Adaptasyon", "explanation": "Hücrenin strese karşı geliştirdiği hipertrofi, atrofi veya metaplazi yanıtıdır."},
                {"term": "Parankim", "explanation": "Bir organın kendine özgü temel görevini yürüten fonksiyonel hücresel bileşenidir."},
                {"term": "Stroma", "explanation": "Parankimi destekleyen damar, sinir ve bağ dokusundan zengin destek çatısıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Patolojik Sürecin Hiyerarşik İlerleme Kaskadı",
                    [
                        "1. Moleküler Başlangıç: DNA mutasyonu veya metabolik bozukluğun ortaya çıkması",
                        "2. Hücresel Yanıt: Membran hasarı ve ATP kaybıyla hücresel dejenerasyon gelişimi",
                        "3. Doku Düzeyi: İnflamatuvar infiltrasyon ve parankimal nekrozun şekillenmesi",
                        "4. Organ Düzeyi: Fonksiyonel rezerv kaybı ve doku mimarisinin bozulması",
                        "5. Organizma Düzeyi: Sistemik yetmezlik tablosu ve klinik semptomların belirmesi"
                    ]
                ),
                make_active_recall(
                    "Patolojide bir organın fonksiyonel hücreleri (parankim) ile onları destekleyen bağ dokusu (stroma) arasındaki ayırım neden hayati önem taşır?",
                    "Primer hastalık süreçleri çoğunlukla fonksiyonel parankimde başlarken; fibrozis, tamir ve bağışıklık yanıtı stromada şekillenir. Ayrıca tümörlerin invazyon ve yayılım davranışını parankim ile stroma arasındaki dinamik etkileşim belirler."
                )
            ]
        },

        # Adım 3
        {
            "slideNumber": 3,
            "title": "Patoloji ve Fizyopatoloji: Morfoloji ile Fonksiyonun Dansı",
            "subtitle": "Patoloji yapısal ve morfolojik anomalilere, fizyopatoloji ise organların fonksiyonel bozulmalarına odaklanır.",
            "badge": "Ayırıcı Tanım",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Patoloji** ve **fizyopatoloji** birbirini tamamlayan iki temel tıp disiplinidir.

Patoloji, hastalıklarda hücre ve dokuların ==morfolojik ve yapısal değişikliklerine== (şekil, boyut, mimari) odaklanırken; fizyopatoloji organ sistemlerinin ==fonksiyonel sapmalarını== ve mekanik-biyokimyasal bozulmalarını inceler. Klinik pratikte morfolojik ve fonksiyonel hasar her zaman eşzamanlı ortaya çıkmaz. Örneğin erken miyokard enfarktüsünde fonksiyonel EKG sapmaları dakikalar içinde başlarken, mikroskopta koagülasyon nekrozunun belirmesi saatler alır. Tersine, geniş bir tümör kitlesi organ rezervi tükenene dek uzun süre belirgin fonksiyon bozukluğu yaratmayabilir.

> [TEMEL İLKE] Morfolojik yapı incelemesi ile fonksiyonel değerlendirme birleştiğinde doğru ve eksiksiz tanıya ulaşılır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Patoloji Odağı", "desc": "Morfolojik, görsel ve histolojik yapısal bozuklukları temel alır.", "isKey": True},
                    {"title": "Fizyopatoloji Odağı", "desc": "Organların işleyişindeki fonksiyonel ve biyokimyasal sapmaları temel alır.", "isKey": True},
                    {"title": "Zamanlama Farkı", "desc": "Fizyopatolojik bozukluk genellikle dakikalar içinde başlarken, morfolojik hasarın belirmesi saatler veya günler alabilir.", "isKey": False}
                ],
                "table": {
                    "title": "Patoloji ve Fizyopatoloji Karşılaştırması",
                    "headers": ["Parametre", "Patoloji Disiplini", "Fizyopatoloji Disiplini"],
                    "rows": [
                        ["Ana Odak", "Yapısal ve morfolojik değişiklikler", "İşlevsel ve fonksiyonel sapmalar"],
                        ["Kullanılan Araçlar", "Işık/elektron mikroskobu, histokimya, İHK, moleküler testler", "Elektrofizyoloji, hemodinamik monitorizasyon, biyokimya"],
                        ["İnceleme Materyali", "Biyopsi, rezeksiyon materyali, sitoloji, otopsi dokusu", "Kan gazı, klerens testleri, EKG, basınç ölçümleri"],
                        ["Örnek Patoloji", "Aterom plağının fibröz kılıfı ve lipid çekirdeği", "Damar lümeninin daralmasına bağlı koroner kan akımı azalması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patoloji morfoloji ve yapı ağırlıklıdır; fizyopatoloji fonksiyonel ve işlevsel bozukluk ağırlıklıdır.",
                "🚨 [KRİTİK UYARI] Morfolojik değişiklik her zaman fonksiyonel bozuklukla eşzamanlı ortaya çıkmaz; iskemi sonrası EKG dakikalar içinde bozulurken ışık mikroskobunda koagülasyon nekrozu en erken 4-12 saatte seçilir.",
                "📌 [SINAV SPOTU] Günümüz modern tıbbında morfoloji ile fonksiyonun birleştiği kavrama 'Entegre Patoloji' adı verilir."
            ],
            "medicalTerms": [
                {"term": "Fizyopatoloji", "explanation": "Hastalık durumunda organ ve sistemlerin fonksiyonel bozukluklarını inceleyen bilim dalıdır."},
                {"term": "Subklinik Dönem", "explanation": "Hastalığın başladığı ancak henüz belirgin klinik belirti vermediği sessiz evredir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Patoloji ve Fizyopatolojinin Klinik Perspektifleri",
                    "Patoloji (Morfolojik Odak)",
                    "Fizyopatoloji (Fonksiyonel Odak)",
                    [
                        "Doku mimarisi ve hücresel yapı incelenir",
                        "Nekroz, inflamasyon, displazi saptanır",
                        "Statik kesitler üzerinden kalıcı hasar haritalanır"
                    ],
                    [
                        "Organ sistemlerinin işlevsel kapasitesi incelenir",
                        "Filtrasyon, debi, iletim bozukluğu ölçülür",
                        "Dinamik süreçler ve fizyolojik denge izlenir"
                    ]
                ),
                make_cloze(
                    "Organlarda meydana gelen fonksiyonel ve işlevsel bozulmaları inceleyen disipline [fizyopatoloji], yapısal ve morfolojik değişiklikleri inceleyen bilim dalına ise patoloji adı verilir.",
                    "fizyopatoloji",
                    "İşlevsel ve fonksiyonel mekanizmaları araştıran disiplin"
                )
            ]
        },

        # Adım 4
        {
            "slideNumber": 4,
            "title": "Entegre Patoloji: Morfoloji, Moleküler Genetik ve Bilişimin Sentezi",
            "subtitle": "Modern patoloji; klasik histomorfolojiyi genomik mutasyonlar ve klinik parametrelerle birleştirerek entegre tanı üretir.",
            "badge": "Modern Yaklaşım",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """21. yüzyıl tıbbında patoloji, klasik mikroskopi ile sınırlı kalmayıp ==Entegre Patoloji (Integrated Pathology)== modeline evrilmiştir.

Entegre patoloji; ışık mikroskobundan elde edilen histomorfolojik bulguları, immünohistokimyasal belirteçleri ve yeni nesil dizileme (NGS) gibi moleküler genetik verileri tek bir sentez raporda birleştirir. Bu yaklaşım onkolojide kişiselleştirilmiş tedavinin temelini oluşturur. Örneğin akciğer adenokarsinomunda histolojik tip belirlendikten sonra EGFR mutasyonu ve PD-L1 ekspresyonu taranarak hedefe yönelik akıllı ilaç seçimi yapılır. Böylece patoloji raporu, doğrudan hastanın tedavi protokolünü belirleyen kılavuz haline gelir.

> [YÜKSEK VERİM] Entegre patoloji; morfoloji ile moleküler verileri birleştirerek kişiselleştirilmiş tedaviyi yönlendirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Histomorfoloji", "desc": "Tümörün doku tipi, diferansiyasyon derecesi ve invazyon derinliği belirlenir.", "isKey": True},
                    {"title": "İmmünohistokimya", "desc": "Tümör hücrelerinin köken aldığı doku ve protein ekspresyonları saptanır.", "isKey": True},
                    {"title": "Moleküler Genetik", "desc": "DNA mutasyonları, kromozomal translokasyonlar ve füzyon genleri haritalanır.", "isKey": True}
                ],
                "table": {
                    "title": "Klasik Patoloji ile Entegre Patolojinin Karşılaştırılması",
                    "headers": ["Ölçüt", "Klasik Patoloji Yaklaşımı", "Modern Entegre Patoloji"],
                    "rows": [
                        ["Tanı Düzeyi", "Yalnızca ışık mikroskobunda histolojik tip", "Histomorfoloji + İHK + Moleküler mutasyon profili"],
                        ["Tedaviye Katkı", "Kemoterapi / Radyoterapi için genel yönlendirme", "Biyobelirteç bazlı hedefe yönelik akıllı ilaç seçimi"],
                        ["Prognostik Güç", "Sınırlı (evre ve dereceye bağımlı)", "Yüksek (genomik risk skorları ve klonalite analizi)"],
                        ["Klinik Örnek", "'Akciğer karsinomu'", "'EGFR Ekzon 19 delesyonlu Akciğer Adenokarsinomu'"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Entegre patoloji; morfolojik, immünohistokimyasal ve moleküler genetik bilginin tek bir tanısal raporda birleşmesidir.",
                "📌 [SINAV SPOTU] Moleküler patoloji testleri (EGFR, KRAS, BRAF, HER2) hastaya özel hedefe yönelik tedavi planlanmasını sağlar.",
                "🚨 [KRİTİK UYARI] Moleküler testler tek başına yeterli değildir; tümör hücresi oranını ve doku kalitesini teyit eden ilk basamak daima histopatolojik incelemedir."
            ],
            "medicalTerms": [
                {"term": "Entegre Tanı", "explanation": "Histomorfolojik bulguların moleküler ve klinik verilerle sentezlenerek raporlanmasıdır."},
                {"term": "Prediktif Biyobelirteç", "explanation": "Hastanın hedefe yönelik tedaviye yanıt verme olasılığını gösteren moleküler belirteçtir."},
                {"term": "Prognostik Biyobelirteç", "explanation": "Tedaviden bağımsız olarak hastalığın genel sağkalım ve nüks seyrini öngören belirteçtir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Entegre Tanı Protokolü ve Onkolojik Karşılıkları",
                    ["Tümör Grubu", "Histolojik Tip", "Kritik İHK Belirteci", "Moleküler Hedef Gen"],
                    [
                        [("Akciğer Kanseri", False), ("Adenokarsinom", False), ("TTF-1 Pozitif", False), ("EGFR / ALK / ROS1", True, "TKI hedefi")],
                        [("Meme Kanseri", False), ("İnvaziv Duktal Karsinom", False), ("Östrojen / Progesteron Reseptörü", False), ("HER2 / ERBB2 Amplifikasyonu", True, "Trastuzumab hedefi")],
                        [("Kolon Kanseri", False), ("Adenokarsinom", False), ("CDX2 Pozitif", False), ("KRAS / NRAS / BRAF Mutasyonu", True, "Anti-EGFR yanıtı")],
                        [("Melanom", False), ("Malign Melanom", False), ("Melan-A / HMB-45", False), ("BRAF V600E Mutasyonu", True, "Vemurafenib hedefi")]
                    ]
                ),
                make_branching_logic(
                    "Akciğerinde kitle saptanan 62 yaşındaki bir hastanın bronkoskopik biyopsisinde adenokarsinom tanısı konuluyor. Onkolog hedefe yönelik akıllı ilaç başlayabilmek için patoloji raporunda hangi ek bilginin bulunmasını talep eder?",
                    [
                        {"text": "Tümör dokusunda EGFR mutasyonları, ALK translokasyonu ve PD-L1 ekspresyon düzeyini içeren moleküler patoloji analizi", "isCorrect": True, "feedback": "Mükemmel klinik karar! Entegre patoloji raporunda EGFR, ALK ve PD-L1 durumu belirtildiğinde hastaya tirozin kinaz inhibitörü veya immünoterapi başlanabilir."},
                        {"text": "Yalnızca hastanın rutin kan biyokimyası ve sedimentasyon hızı", "isCorrect": False, "feedback": "Hatalı yaklaşım. Kan testleri tümörün hedefe yönelik moleküler yapısını gösteremez."},
                        {"text": "Hastadan tekrar açık akciğer ameliyatı yapılıp organın tamamının çıkarılması", "isCorrect": False, "feedback": "Gereksiz invaziv girişim. Bronkoskopik biyopsi materyalinden moleküler testler başarıyla çalışılabilir."}
                    ]
                )
            ]
        },

        # Adım 5
        {
            "slideNumber": 5,
            "title": "Patolojinin Tıptaki Üçlü Rolü: Bilimsel, Uygulamalı ve Eğitsel Güç",
            "subtitle": "Patoloji hem temel bilim araştırmalarını besler, hem hastaya kesin tanı koyar, hem de hekim yetiştirir.",
            "badge": "Tıptaki Rolü",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojinin modern tıp hiyerarşisindeki yeri ==üç temel sacayağı== üzerine oturmuştur: Bilimsel rol, uygulamalı (klinik) rol ve eğitsel rol.

**Bilimsel rolüyle** patoloji, hastalıkların altında yatan moleküler ve hücresel mekanizmaları araştırarak yeni tedavi hedeflerini aydınlatır. **Uygulamalı klinik rolüyle**, canlı hastadan alınan biyopsi ve ameliyat materyallerini inceleyerek altın standart kesin tanıyı koyar, cerrahi sınırları ve evreyi belirler. **Eğitsel rolüyle** ise hekimlerin patofizyolojik düşünme yeteneğini geliştirir ve vaka konseyleriyle klinik karar kalitesini güvenceye alır.

> [KLİNİK İPUCU] Patoloji; kesin tanıyı koyan, cerrahi sınırları denetleyen ve klinik kaliteyi garanti eden temel disiplindir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Bilimsel Boyut", "desc": "Hastalıkların moleküler ve hücresel nedenlerini açığa çıkarır.", "isKey": True},
                    {"title": "Uygulamalı Boyut", "desc": "Klinik tanı, evreleme, cerrahi sınır ve tedavi protokolünü belirler.", "isKey": True},
                    {"title": "Eğitsel Boyut", "desc": "Tüm branşlardaki hekimlerin hastalık mekanizması kavrayışını şekillendirir.", "isKey": False}
                ],
                "table": {
                    "title": "Patolojinin Üç Temel Rolünün Karşılaştırmalı Özeti",
                    "headers": ["Rol Boyutu", "Birincil Hedef", "Gerçekleştirilen Tıbbi Faaliyet"],
                    "rows": [
                        ["Bilimsel Rol", "Hastalık mekanizmalarını anlamak", "Kanser modelleri, translasyonel araştırmalar, yeni biyobelirteç keşfi"],
                        ["Uygulamalı Rol", "Hastaya doğru ve kesin tanı koymak", "Biyopsi incelemesi, frozen kesit, evreleme, cerrahi sınır tayini"],
                        ["Eğitsel Rol", "Klinik düşünceyi ve kaliteyi artırmak", "Klinikopatolojik vaka toplantıları, tıp eğitimi, mortalite denetimi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojinin tıptaki üç temel rolü: Bilimsel, uygulamalı (klinik tanı) ve eğitsel rollerdir.",
                "📌 [SINAV SPOTU] Neoplazilerde ve cerrahi sınırlarda patolojik inceleme tartışmasız altın standarttır.",
                "🚨 [KRİTİK UYARI] Patoloji sadece retrospektif bir kayıt alanı değil; hastanın tedavi rotasını çizen aktif prospektif bir klinik disiplindir."
            ],
            "medicalTerms": [
                {"term": "Cerrahi Sınır", "explanation": "Rezeksiyon sınırında tümör hücresi varlığını araştıran mikroskobik inceleme hattıdır."},
                {"term": "Evreleme (Staging)", "explanation": "Malign bir tümörün vücuttaki anatomik yayılım genişliğini (TNM) belirleme sürecidir."},
                {"term": "Derecelendirme (Grading)", "explanation": "Tümör hücrelerinin köken aldığı dokuya benzerlik derecesinin mikroskopta puanlanmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patolojinin tıptaki rolleri değerlendirildiğinde, aşağıdakilerden hangisi patolojinin 'uygulamalı (klinik)' rolüne doğrudan örnek oluşturur?",
                    {
                        "A": "Meme kitlesi ameliyatında çıkarılan dokunun cerrahi sınırlarının temiz olduğunu raporlayarak cerrahiyi sonlandırmak",
                        "B": "Laboratuvarda fare modellerinde yeni bir karsinojenez yolağını aydınlatmak",
                        "C": "Dönem 3 tıp öğrencilerine inflamasyon mekanizmalarını teorik olarak anlatmak",
                        "D": "Tıp fakültesi amfisinde mikroskop slaytlarının tarihsel gelişimini sunmak",
                        "E": "Tıp kongresinde geleceğin yapay zeka algoritmalarını tartışmak"
                    },
                    "A",
                    {
                        "A": "Doğru: Ameliyat sırasında cerrahi sınır değerlendirmesi doğrudan klinik uygulamaya örnektir.",
                        "B": "Fare modellerinde araştırma yapmak patolojinin bilimsel rolüne aittir.",
                        "C": "Öğrencilere mekanizma anlatmak patolojinin eğitsel rolü kapsamındadır.",
                        "D": "Tarihsel sunum yapmak patolojinin eğitsel rolüne aittir.",
                        "E": "Kongre tartışması bilimsel araştırma platformuna aittir."
                    }
                ),
                make_cloze(
                    "Bir malign tümörün köken aldığı normal dokuya ne derece benzediğini hücresel atipiye göre belirlemeye derecelendirme (grading), vücuttaki anatomik yayılım genişliğini belirlemeye ise [evreleme] adı verilir.",
                    "evreleme",
                    "Tümörün boyutu ve yayılımını (TNM) belirleyen klinik basamak"
                )
            ]
        },

        # Adım 6
        {
            "slideNumber": 6,
            "title": "Temel ve Klinik Bilimler Arasında Patolojinin Köprü Fonksiyonu",
            "subtitle": "Anatomi, histoloji ve biyokimyadan aldığı temel bilgiyi dahiliye ve cerrahiye aktaran kilit kavşak patolojidir.",
            "badge": "Köprü Disiplin",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patoloji, ==temel tıp bilimleri ile klinik bilimler arasındaki en stratejik köprüdür==.

Hekimlikte hastalıkları kavramak için önce anatomi ve histoloji ile normal yapıyı, biyokimya ve fizyoloji ile normal işleyişi öğrenmek gerekir. Patoloji, bu normal zemin üzerinde doku ve hücrelerin ==hangi mekanizmalarla bozulduğunu== somutlaştırarak cerrahi ve dahili branşlara rehberlik eder. Bir cerrah kitle çıkarırken ya da bir gastroenterolog biyopsi alırken patolojinin kesin tanısına dayanarak tedaviye karar verir. Klinik branşlar kesin tanıya ancak patoloji köprüsünden geçerek ulaşır.

> [TEMEL İLKE] Patoloji; temel bilimlerdeki teorik mekanizmaları klinikte somut tanı ve tedavi kararına dönüştürür.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Temel Bilimler Kaynağı", "desc": "Anatomi, histoloji, biyokimya ve mikrobiyolojiden beslenir.", "isKey": True},
                    {"title": "Klinik Branşlar Hedefi", "desc": "Dahiliye, cerrahi, onkoloji ve jinekolojiye kesin teşhis sunar.", "isKey": True},
                    {"title": "Tanısal Kesinlik", "desc": "Klinik ön tanıların doğrulanması veya çürütülmesinde nihai hakemdir.", "isKey": False}
                ],
                "table": {
                    "title": "Patolojinin Temel Bilimlerden Kliniğe Bilgi Akış Köprüsü",
                    "headers": ["Temel Bilim Temeli", "Patolojinin Yorumu (Köprü)", "Klinik Yansıma ve Karar"],
                    "rows": [
                        ["Normal Kolon Histolojisi (Tek katlı silindirik epitel)", "Displastik epitel proliferasyonu ve invazyon (Adenokarsinom)", "Genişletilmiş hemikolektomi cerrahisi"],
                        ["Normal Böbrek Anatomisi (Glomerül ve tübüller)", "İmmün kompleks birikimi ve hilal formasyonu (Kresentik GN)", "Acil plazmaferez ve pulse steroid tedavisi"],
                        ["Normal Kemik İliği (Hematopoetik seriler)", "Blast oranının %20'yi aşması (Akut Lösemi)", "İndüksiyon kemoterapisi ve kemik iliği nakli"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patoloji, temel tıp bilimleri (anatomi, histoloji) ile klinik tıp bilimleri arasında entegratif köprü kuran bağımsız bir temel bilimdir.",
                "📌 [SINAV SPOTU] Bir klinik ön tanı ne kadar güçlü olursa olsun, neoplastik lezyonlarda tedaviye başlamadan önce histopatolojik doğrulama şarttır.",
                "🚨 [KRİTİK UYARI] Patoloji histolojinin devamı değil; histolojinin zedeleyici etkenler altındaki patolojik metamorfozudur."
            ],
            "medicalTerms": [
                {"term": "Displazi", "explanation": "Hücrelerin şekil ve mimarisinde bazal membranı aşmayan neoplazi öncesi yapısal bozulmadır."},
                {"term": "İnvazyon", "explanation": "Malign hücrelerin bazal membranı aşarak çevre dokulara ve stromaya yayılmasıdır."},
                {"term": "Metaplazi", "explanation": "Diferansiye bir hücre tipinin strese dayanıklı başka bir hücre tipine dönüşmesidir."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Tıp eğitiminde patolojinin anatomi ve histoloji ile klinik bilimler arasında köprü kurması ne anlama gelir?",
                    "Anatomi ve histoloji normal doku mimarisini öğretirken; patoloji bu mimarinin hastalık etkenleriyle nasıl bozulduğunu hücresel ve moleküler düzeyde açıklar. Böylece klinisyenin hastada gördüğü semptomları biyolojik temele bağlayarak kesin tanı ve rasyonel tedavi seçimini sağlar."
                ),
                make_cloze(
                    "Kronik tahriş karşısında diferansiye bir hücre tipinin yerini o basınca daha dayanıklı başka bir diferansiye hücre tipine bırakmasına [metaplazi] adı verilir.",
                    "metaplazi",
                    "Hücresel adaptasyon türü olan geriye dönüşlü doku tipi dönüşümü"
                )
            ]
        },

        # Adım 7
        {
            "slideNumber": 7,
            "title": "Klinik Pratikte Morfolojik Belirsizlikler ve Erken Evre Lezyonlar",
            "subtitle": "Hastalıkların her evresinde belirgin morfolojik değişiklik görülmeyebilir; klinik-patolog teması hayat kurtarır.",
            "badge": "Klinik Tuzak",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Klinik pratikte ==morfolojik değişiklikler her zaman erken evrede belirgin olmayabilir==.

Örneğin akut miyokard enfarktüsünde hücresel düzeyde iskemi anında başlasa da, standart ışık mikroskobunda koagülasyon nekrozunun netleşmesi en erken 4 ila 12 saati bulur. Hasta ilk saatlerde kaybedilirse otopside belirgin nekroz saptanamayabilir. Benzer şekilde Minimal Değişiklik Hastalığında glomerüller ışık mikroskobunda tamamen normal görünür; podosit hasarını yakalamak için elektron mikroskobu zorunludur. Klinisyen hastanın masif proteinüri bilgisini iletmezse biyopsi hatalı olarak normal yorumlanabilir.

> [KRİTİK UYARI] Morfolojinin normal görünmesi hastalığı dışlamaz; hasarın moleküler düzeyde veya mikroskop sınırının altında olduğunu gösterebilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Zaman Pencereleri", "desc": "Biyokimyasal hasar anında başlar; morfolojik yapısal lezyonun belirmesi zaman alır.", "isKey": True},
                    {"title": "Mikroskop Sınırları", "desc": "Işık mikroskobu organel düzeyindeki ultrastrüktürel hasarları (podosit silinmesi) göremez.", "isKey": True},
                    {"title": "İletişim Şartı", "desc": "Klinik şüphe patoloğa bildirilmezse erken lezyonlar atlanabilir.", "isKey": False}
                ],
                "table": {
                    "title": "Işık Mikroskobunda Görünmeyen Erken Patolojiler ve Çözüm Araçları",
                    "headers": ["Klinik Durum", "Işık Mikroskobu Görünümü", "Gerçek Patoloji ve Çözüm Aracı"],
                    "rows": [
                        ["Minimal Değişiklik Hastalığı (Nefrotik Sendrom)", "Tamamen normal glomerüller", "Elektron mikroskobunda podosit ayaksı çıkıntılarında silinme"],
                        ["Erken Miyokard Enfarktüsü (<2 saat)", "Normal miyokard lifleri", "İmmünohistokimya / kardiyak troponin ve EKG bulguları"],
                        ["Erken Toksik Karaciğer Hasarı", "Belirgin nekroz izlenmez", "Biyokimyasal enzim yüksekliği (AST/ALT) ve ultrastrüktürel şişme"],
                        ["İntraepitelyal Neoplazi Başlangıcı", "Hafif nükleer düzensizlik", "İHK ile Ki-67 proliferasyon indeksi ve p53 aşırı ekspresyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Minimal Değişiklik Hastalığında ışık mikroskobu tamamen normaldir; tanı elektron mikroskobunda podosit ayaklarının silinmesiyle konur.",
                "🚨 [KRİTİK UYARI] Akut iskemik hasarda ışık mikroskobunda koagülasyon nekrozunun ilk belirgin histolojik bulguları 4-12 saatten önce oluşmaz.",
                "📌 [SINAV SPOTU] Morfolojik lezyonun belirgin olmadığı durumlarda klinisyen-patolog iletişimi tanının en kritik garantisidir."
            ],
            "medicalTerms": [
                {"term": "Elektron Mikroskobu (EM)", "explanation": "Organelleri ve nanometrik yapısal hasarları inceleyen yüksek çözünürlüklü mikroskoptur."},
                {"term": "Podosit", "explanation": "Glomerül filtrasyon bariyerini oluşturan özelleşmiş visseral epitelyal hücredir."},
                {"term": "Koagülasyon Nekrozu", "explanation": "İskemi sonucu proteinlerin denatüre olduğu ancak doku mimarisinin korunduğu hücre ölümüdür."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Ağır nefrotik sendrom (masif proteinüri ve anazarka ödemi) olan 4 yaşındaki bir çocuğun böbrek biyopsisinde ışık mikroskobunda glomerüller tamamen normal izleniyor. Bir patolog olarak sonraki tanısal adımınız ne olmalıdır?",
                    [
                        {"text": "Biyopsi materyalini elektron mikroskobu ile inceleyerek podosit ayaksı çıkıntılarındaki silinmeyi araştırmak", "isCorrect": True, "feedback": "Mükemmel klinik yaklaşım! Çocuklardaki Minimal Değişiklik Hastalığında ışık mikroskobu tamamen normaldir, tanı elektron mikroskobunda podosit ayaksı çıkıntıların silinmesiyle kesinleşir."},
                        {"text": "'Böbrek tamamen sağlıklıdır, hastalık yoktur' diye raporlayıp olguyu kapatmak", "isCorrect": False, "feedback": "Ölümcül hata! Masif proteinüri varlığında glomerülün ışık mikroskobunda normal görünmesi Minimal Değişiklik Hastalığının tipik özelliğidir."},
                        {"text": "Hastaya acil böbrek nakli yapılmasını önermek", "isCorrect": False, "feedback": "Tamamen endikasyonsuz ve hatalı yaklaşım. Minimal Değişiklik Hastalığı steroid tedavisine çok iyi yanıt verir."}
                    ]
                ),
                make_cloze(
                    "Çocukluk çağı nefrotik sendromunun en sık nedeni olan ve ışık mikroskobunda glomerüllerin normal göründüğü hastalık [Minimal Değişiklik] hastalığıdır.",
                    "Minimal Değişiklik",
                    "Glomerüllerin ışık mikroskobunda normal olduğu podositopati"
                )
            ]
        },

        # Adım 8
        {
            "slideNumber": 8,
            "title": "Klinisyen-Patolog İletişimi: Ortak Dil ve Karşılıklı Konsültasyon",
            "subtitle": "Klinik bilgi olmadan patoloji mikroskop camındaki gölgelerden ibarettir; patolog klinisyenin konsültanıdır.",
            "badge": "İletişim İlkeleri",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolog, klinisyenin teşhis ve tedavi sürecindeki ==en kritik konsültan hekimidir==.

Bir doku örneğinin doğru yorumlanabilmesi için hastanın yaşı, cinsiyeti, lezyon lokalizasyonu, radyolojik bulguları ve geçirdiği tedaviler (radyoterapi, kemoterapi) istek formuna eksiksiz yazılmalıdır. Örneğin radyoterapi almış dokulardaki atipik fibroblastlar mikroskopta sarkom ile kolayca karışabilir (radyasyon atipisi). Klinik öykü bilinmediğinde hastaya yanlış kanser tanısı konulabilir. Bu nedenle modern tıpta hekimler tümör konseylerinde bir araya gelerek hastaları ortak akılla değerlendirir.

> [TEMEL İLKE] Eksik klinik bilgiyle incelenen biyopsi, tanısal hata ve yanlış tedavi riskini doğrudan artırır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İstek Formu", "desc": "Hastanın anamnezi, cerrahi girişim türü ve radyolojik bulguları mutlaka yazılmalıdır.", "isKey": True},
                    {"title": "Konsültan Rol", "desc": "Patolog sadece rapor yazmaz; klinisyene ayırıcı tanı ve biyobelirteç rehberliği sunar.", "isKey": True},
                    {"title": "Tümör Konseyleri", "desc": "Patolog, cerrah, medikal onkolog ve radyoloğun ortak vaka toplantılarıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Klinik Bilgi Eksikliğinde Karşılaşılan Tanısal Tuzaklar",
                    "headers": ["Verilmeyen Klinik Bilgi", "Patologda Oluşabilecek Hatalı Yorum", "Doğru Klinikopatolojik Yaklaşım"],
                    "rows": [
                        ["Geçirilmiş Radyoterapi Öyküsü", "Pleomorfik hücreler nedeniyle malign sarkom sanılması", "Beningn reaktif radyasyon fibroblastı atipisi tanısı"],
                        ["Kullanılan İlaç Öyküsü (ör. Metotreksat)", "İdiyopatik hepatit veya siroz sanılması", "İlaca bağlı karaciğer toksisitesi tanısı"],
                        ["Lezyonun Anatomik Derinliği", "Deri tümöründe derin invazyonun atlanması", "Rezeksiyon derinliğine göre doğru patolojik T evrelemesi"],
                        ["Daha Önceki Biyopsi Raporu", "Yeni lezyonun bağımsız primer tümör sanılması", "Eski tümörün nüksü veya metastazı olarak doğrulanması"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolog klinisyen için bir laborant değil; teşhis ve tedavi planını belirleyen konsültan hekimdir.",
                "🚨 [KRİTİK UYARI] Radyoterapiye bağlı hücresel atipi malignite ile karışabilir; hastanın tedavi öyküsü istek formuna mutlaka yazılmalıdır.",
                "📌 [SINAV SPOTU] Patoloji ve klinik arasında uyumsuzluk olduğunda klinisyen ve patoloğun doğrudan görüşmesi (konsültasyon) tıbbi zorunluluktur."
            ],
            "medicalTerms": [
                {"term": "Radyasyon Atipisi", "explanation": "Radyasyona maruz kalan bağ dokusu hücrelerinin maligniteyi taklit eden nükleer büyümesidir."},
                {"term": "Tümör Konseyi (Tumor Board)", "explanation": "Farklı branş hekimlerinin kanser hastasının tanı ve tedavisini tartıştığı ortak kuruldur."},
                {"term": "Klinikopatolojik Uyumsuzluk", "explanation": "Klinik bulgular ile patoloji raporunun çelişmesi ve konsültasyon gerektirmesi durumudur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Klinisyen-patolog iletişimi ile ilgili olarak aşağıdakilerden hangisi klinik pratikte tıbbi hata riskini en aza indiren doğru bir tutumdur?",
                    {
                        "A": "Biyopsi kabına sadece hastanın adını yazıp klinik bilgi kısmını boş bırakmak",
                        "B": "Patoloğun önyargısız karar vermesi için daha önce geçirilmiş kanser ve radyoterapi öyküsünü gizlemek",
                        "C": "Patoloji istek formuna hastanın yaşını, lezyon lokalizasyonunu, önceki tedavilerini ve klinik ön tanılarını eksiksiz yazmak",
                        "D": "Patoloji raporu klinik tabloyla çeliştiğinde patoloğu aramadan doğrudan hastayı taburcu etmek",
                        "E": "Tümör konseylerine katılmayıp sadece patoloji raporunun son satırını okumakla yetinmek"
                    },
                    "C",
                    {
                        "A": "Klinik bilgisiz biyopsi göndermek yanlış tanı riskini ciddi oranda artırır.",
                        "B": "Öyküyü gizlemek reaktif hücrelerin kanser sanılması gibi vahim hatalara yol açar.",
                        "C": "Doğru: Yaş, lokalizasyon ve tedavi öyküsünün iletilmesi doğru tanının temel koşuludur.",
                        "D": "Uyumsuzluk durumunda patolog ile konsültasyon yapılması tıbbi zorunluluktur.",
                        "E": "Tümör konseylerine katılmamak multidisipliner tedavi kalitesini düşürür."
                    }
                ),
                make_before_after(
                    "İstek Formunun Doldurulma Kalitesi ve Tanısal Sonuç",
                    "Eksik Klinik Bilgi ile Gönderilen Biyopsi",
                    "Eksiksiz Klinikopatolojik İstek Formu",
                    [
                        "Radyoterapi öyküsü belirtilmemiş",
                        "Lezyonun tam derinliği bilinmiyor",
                        "Yanlış sarkom tanısı ve gereksiz cerrahi riski"
                    ],
                    [
                        "3 ay önce 50 Gy radyoterapi aldığı yazılı",
                        "Cilt altı yerleşim ve klinik öntanı verilmiş",
                        "Doğru benign radyasyon atipisi tanısı ve organ korunması"
                    ]
                )
            ]
        },

        # Adım 9 (CHECKPOINT 1)
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Patolojinin Tanımı, Kapsamı ve Klinik İlkeler",
            "subtitle": "Bölümün kilit sınav spotlarını, etimolojik temellerini ve kliniko-patolojik kurallarını akıl kartlarıyla pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 1,
            "synthesisNarrative": """Bu kontrol noktası, patolojinin temel ilkelerini özetlemektedir. **Pathos** ve **logos** köklerinden türeyen patoloji; hastalıkları etiyoloji, patogenez, morfolojik değişiklikler ve klinik sonuçlar olmak üzere dört eksende inceler.

Patoloji hücresel ve yapısal morfolojiye odaklanırken, fizyopatoloji fonksiyonel bozulmaları ele alır. Günümüzde bu yaklaşımlar moleküler analizlerle birleşerek **Entegre Patoloji** modelini oluşturmuştur. Erken evrelerde morfolojik bulgular belirsiz olabileceğinden, klinisyen ile patolog arasındaki kesintisiz konsültasyon ve tümör konseyleri doğru teşhisin temel güvencesidir.

> [BÖLÜM ÖZETİ] Patoloji; moleküler hasardan organ lezyonuna kadar tüm basamakları klinik tabloyla entegre eden temel tıp disiplinidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dört Temel Boyut", "desc": "Etiyoloji, patogenez, morfoloji ve klinik sonuç birbirini tamamlar.", "isKey": True},
                    {"title": "Entegre Patoloji", "desc": "Morfoloji + İmmünohistokimya + Moleküler Genetik sentezidir.", "isKey": True},
                    {"title": "Konsültan Hekimlik", "desc": "Patolog klinisyenin tanı ve tedavi ortağıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 1 Temel Kavramlar Sentezi",
                    "headers": ["Kavram", "Tanım ve Kapsam", "Sınav Kritik Vurgusu"],
                    "rows": [
                        ["Patoloji", "Hastalık bilimi (etiyoloji, patogenez, morfoloji, sonuç)", "Neoplazilerde kesin tanının altın standardıdır"],
                        ["Fizyopatoloji", "Fonksiyonel ve işlevsel bozukluklar bilimi", "Morfoloji normal olsa da fizyopatoloji bozuk olabilir"],
                        ["Entegre Patoloji", "Morfoloji, İHK ve moleküler testlerin birleşimi", "Kişiselleştirilmiş akıllı ilaç tedavisinin kılavuzudur"],
                        ["Tümör Konseyi", "Patolog, cerrah, onkolog ve radyoloğun ortak kurulu", "Klinikopatolojik korelasyonun sağlandığı merkezdir"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojinin dört ayağı: Etiyoloji, patogenez, morfoloji ve klinik sonuçtur.",
                "📌 [SINAV SPOTU] Minimal Değişiklik Hastalığında ışık mikroskobu normaldir; tanı elektron mikroskobuyla konur.",
                "🚨 [KRİTİK UYARI] Patolojiye gönderilen materyalde klinik bilgi eksikliği en sık tanısal hata nedenidir."
            ],
            "medicalTerms": [
                {"term": "Entegre Patoloji", "explanation": "Histomorfoloji ile moleküler genetik analizlerin tek raporda sentezlenmesidir."},
                {"term": "Klinikopatolojik Korelasyon", "explanation": "Mikroskobik bulguların hastanın klinik ve laboratuvar tablosuyla eşleştirilmesidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-p1-1",
                    "Patoloji ile fizyopatoloji arasındaki en temel odaklanma farkı nedir?",
                    "Patoloji hücre ve dokuların morfolojik ve yapısal değişikliklerine odaklanırken; fizyopatoloji organların işlevsel ve fonksiyonel bozukluklarına odaklanır.",
                    "Morfoloji vs Fonksiyon",
                    "Temel Patoloji"
                ),
                make_flashcard(
                    "fc-p1-2",
                    "Hastalık sürecini oluşturan dört temel öğe hangi sıra ile ilerler?",
                    "1. Etiyoloji (neden) -> 2. Patogenez (biyolojik mekanizmalar zinciri) -> 3. Morfolojik değişiklikler (yapısal hasar) -> 4. Fonksiyonel ve klinik sonuçlar (semptom ve bulgular).",
                    "Dört temel öğe",
                    "Hastalık Süreci"
                ),
                make_flashcard(
                    "fc-p1-3",
                    "Modern onkolojide 'Entegre Patoloji' kavramı neyi ifade eder?",
                    "Klasik histomorfolojik tümör tanısının; immünohistokimyasal belirteçler ve moleküler genetik mutasyon analizleri (EGFR, KRAS, BRAF, ALK) ile birleştirilerek hedefe yönelik tedavi rehberi oluşturulmasını ifade eder.",
                    "Kişiselleştirilmiş tıp",
                    "Modern Patoloji"
                )
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölüm 1'de ele alınan patoloji ve tıp ilişkisi ilkeleri dikkate alındığında, aşağıdakilerden hangisi yanlıştır?",
                    {
                        "A": "Patoloji bağımsız bir temel bilimdir ve temel bilimler ile klinik bilimler arasında köprü kurar.",
                        "B": "Morfolojik değişiklikler her zaman hastalığın en başında belirgin olmayabilir.",
                        "C": "Neoplastik hastalıklarda cerrahi sınırların değerlendirilmesinde patoloji altın standarttır.",
                        "D": "Patolog klinisyen için yalnızca laboratuvar testi üreten bir teknikerdir, klinik karar sürecinde yeri yoktur.",
                        "E": "Entegre patoloji raporları doğrudan hedefe yönelik moleküler ilaç seçimini yönlendirir."
                    },
                    "D",
                    {
                        "A": "Doğru: Patoloji temel bilimler ile klinik branşlar arasında köprü kurar.",
                        "B": "Doğru: Erken miyokard enfarktüsünde ilk saatlerde ışık mikroskobu normaldir.",
                        "C": "Doğru: Cerrahi sınır negatifliği ameliyat başarısını kanıtlayan altın standarttır.",
                        "D": "Yanlış (aranan cevap): Patolog bir tekniker değil; tanı ve tedaviyi yönlendiren konsültan doktordur.",
                        "E": "Doğru: Moleküler mutasyonlar hedefe yönelik akıllı ilaç seçimini belirler."
                    }
                ),
                make_active_recall(
                    "Bir cerrahın rezeksiyon materyali gönderirken patoloji istek formuna lezyonun kesin anatomik lokalizasyonunu ve klinik ön tanısını yazması neden hayati bir zorunluluktur?",
                    "Morfolojik olarak benzer görünen reaktif lezyonlar ile maligniteler klinik öykü olmadan kolayca karışabilir. Klinik bilgi ve anatomik lokalizasyon, patoloğun doğru ayırıcı tanıya ulaşmasını sağlayan vazgeçilmez rehberdir."
                )
            ]
        }
    ]
