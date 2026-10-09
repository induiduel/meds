# -*- coding: utf-8 -*-
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
        {
            "slideNumber": 1,
            "title": "Hücre Hasarı Kavramı ve Biyolojik Homeostaz",
            "subtitle": "Sağlıklı hücrenin kararlı iç ortamı ve hasarın tanımı",
            "badge": "Giriş",
            "badgeColor": "blue",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Biyolojik homeostaz, hücrenin fizyolojik fonksiyonlarını sürdürebilmesi için hücre içi "
                "iyon konsantrasyonlarını, enerji üretimini, pH dengesini ve makromolekül sentezini "
                "dar sınırlar içinde sabit tutma yeteneğidir. Normal hücre bu dengede sakin bir metabolizma "
                "yürütür. Ancak hücrenin fizyolojik sınırlarını aşan patolojik veya aşırı fizyolojik stresler "
                "meydana geldiğinde hücre doğrudan homeostazdan uzaklaşır.\n\n"
                "> [TEMEL İLKE] Hücre hasarı, hücrenin normal homeostazını sürdüremediği, hücresel "
                "fonksiyonların ve biyokimyasal dengelerin bozulduğu patolojik durumu ifade eder.\n\n"
                "Hücre hasarı klinikteki tüm organik hastalıkların ortak hücresel ve moleküler başlangıç "
                "noktasıdır. Hasarın niteliği, süresi ve hücrenin genetik yatkınlığı nihai klinik tabloyu belirler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Homeostaz", "desc": "Hücre içi ortamın dinamik ve dar sınırlar içinde dengede tutulmasıdır.", "isKey": True},
                    {"title": "Hücre Hasarı", "desc": "Zararlı etkenlerin homeostaz mekanizmalarını aşarak hücresel işlevi bozmasıdır.", "isKey": True},
                    {"title": "Klinik Yansıma", "desc": "Hücresel düzeydeki bozulmalar birikerek organ yetmezliği ve klinik semptomları doğurur.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Durumlar",
                    "headers": ["Durum", "Metabolik Denge", "Morfolojik Görünüm"],
                    "rows": [
                        ["Normal Homeostaz", "Dengeli bazal hız", "Tipik sağlıklı hücre yapısı"],
                        ["Hücresel Adaptasyon", "Yeni kararlı denge", "Hipertrofi, hiperplazi veya atrofi"],
                        ["Hücre Hasarı", "Homeostaz kaybı", "Şişme, vakuolizasyon veya nekroz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarı, hücrenin normal homeostaz sınırlarını koruyamadığı patolojik tablodur.",
                "📌 [YÜKSEK VERİM] Bütün edinsel hastalıkların patogenezi en nihayetinde hücresel düzeydeki hasara dayanır."
            ],
            "medicalTerms": [
                {"term": "Homeostaz", "explanation": "Hücrenin fizyolojik parametrelerini dar sınırlar içinde sabit tutma dinamizmidir."},
                {"term": "Hücre Hasarı", "explanation": "Hücresel adaptasyon sınırını aşan stresin neden olduğu fonksiyonel ve yapısal bozulmadır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Hücrenin normal iç dengesini ve metabolik fonksiyonlarını koruyamadığı patolojik duruma hücre hasarı adı verilir.",
                    "hücre hasarı",
                    "Temel Patoloji Kavramı"
                ),
                make_active_recall(
                    "Biyolojik homeostaz ile hücre hasarı arasındaki temel fark nedir?",
                    "Homeostaz hücrenin fizyolojik sınırlarını sabit tutabildiği dengedir; hücre hasarı ise stresin bu koruyucu kapasiteyi aşmasıyla ortaya çıkan yapısal ve işlevsel bozulmadır."
                )
            ]
        },
        {
            "slideNumber": 2,
            "title": "Hücrenin Zararlı Uyaranlara Yanıt Akışı",
            "subtitle": "Homeostazdan ölüme uzanan dinamik patolojik spektrum",
            "badge": "Mekanizma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücrenin karşılaştığı stres karşısında izlediği yol tekdüze değildir; zararlı uyarının "
                "şiddetine, süresine ve hücrenin tipine göre aşamalı bir spektrum izler. Normal bir hücre "
                "orta dereceli fizyolojik stres altında önce adaptasyon (hipertrofi, hiperplazi vb.) geliştirir. "
                "Eğer stres adaptasyon sınırını aşarsa veya adaptif yanıt yetersiz kalırsa hücre hasarı başlar.\n\n"
                "> [KRİTİK UYARI] Hafif ve geçici stres geri dönüşümlü hücre hasarı ile sonuçlanırken, "
                "şiddetli veya ilerleyici stres doğrudan geri dönüşümsüz hasara ve hücre ölümüne yol açar.\n\n"
                "Geri dönüşümlü evrede zararlı etken ortadan kalkarsa hücre yeniden sağlıklı homeostaza "
                "dönebilir. Ancak hasar uzarsa hücre intihar (apoptoz) veya feci bir yıkımla (nekroz) ölür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Adaptasyon Eşiği", "desc": "Hafif ve kronik yüklenmelerde ilk devreye giren yapısal savunmadır.", "isKey": True},
                    {"title": "Geri Dönüşümlü Evre", "desc": "Zararlı etken kaldırıldığında hasarın iz bırakmadan iyileşebildiği dönemdir.", "isKey": True},
                    {"title": "Geri Dönüşümsüz Evre", "desc": "Mitokondri ve membran fonksiyonlarının onarılamaz biçimde çöktüğü son evredir.", "isKey": True}
                ],
                "table": {
                    "title": "Stres Yanıt Spektrumu",
                    "headers": ["Aşama", "Geri Dönüş Olasılığı", "Temel Hücresel Olay"],
                    "rows": [
                        ["Adaptasyon", "Mükemmel", "Yeni kararlı durum oluşumu"],
                        ["Geri Dönüşümlü Hasar", "Var (etken kalkarsa)", "Hücresel şişme, yağlanma"],
                        ["Hücre Ölümü", "Yok (geri dönüşsüz)", "Nekroz veya apoptoz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sıralama: Normal hücre → Adaptasyon → Geri dönüşümlü hasar → Geri dönüşümsüz hasar → Hücre ölümü.",
                "🚨 [KRİTİK UYARI] Hücre ölümü iki ana yolla gerçekleşir: Nekroz (her zaman patolojik) ve Apoptoz (fizyolojik veya patolojik)."
            ],
            "medicalTerms": [
                {"term": "Geri Dönüşümlü Hasar", "explanation": "Zararlı uyarı sonlandığında hücrenin normal fonksiyonuna dönebildiği patolojik evredir."},
                {"term": "Hücre Ölümü", "explanation": "Hücrenin metabolik ve yapısal bütünlüğünü kalıcı olarak kaybettiği geri dönüşsüz durumdur."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hücresel Yanıt Aşamaları Zinciri",
                    [
                        "1. Homeostaz: Sağlıklı hücre dengeli iç metabolizmasını sürdürür.",
                        "2. Zararlı Stres: Fiziksel, kimyasal veya biyolojik etken hücreyi zorlar.",
                        "3. Geri Dönüşümlü Hasar: ATP azalır, hücresel şişme gelişir ancak membran bütünlüğü korunur.",
                        "4. Geri Dönüşümsüz Kriz: Stres sürerse mitokondri ve zarlar kalıcı parçalanır.",
                        "5. Hücre Ölümü: Hücre nekroz veya apoptoz yolağı ile canlılığını tamamen kaybeder."
                    ]
                ),
                make_cloze(
                    "Hafif ve geçici stres altında gelişen hücresel bozukluk geri dönüşümlü hasar olarak adlandırılır.",
                    "geri dönüşümlü hasar",
                    "Hücresel Faz"
                )
            ]
        },
        {
            "slideNumber": 3,
            "title": "Hastalık Gelişiminin Dört Temel Boyutu",
            "subtitle": "Etiyoloji, patogenez, morfolojik değişiklikler ve klinik bulgular",
            "badge": "Klinik Patoloji",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Patolojinin klinik tıbba temel teşkil etmesini sağlayan çekirdek yaklaşım, her hastalığı "
                "dört aşamalı mantıksal bir zincir üzerinden açıklamasıdır. Bu boyutlar sırasıyla etiyoloji "
                "(hastalığın nedeni), patogenez (hücresel ve moleküler mekanizma), morfolojik değişiklikler "
                "(yapısal değişimler) ve klinik anlamlılıktır (semptom ve bulgular).\n\n"
                "> [YÜKSEK VERİM] Patogenez, bir etkenin dokuya temas ettiği andan itibaren hastalığın tam "
                "klasik tablosuna ulaşmasına kadar geçen hücresel ve biyokimyasal basamaklar zinciridir.\n\n"
                "Morfolojik değişiklikler ise çıplak gözle (makroskopi) veya mikroskopla incelenen yapısal "
                "bozulmalardır; hekimin tanı koymasını ve hastanın prognozunu belirlemesini sağlar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Etiyoloji", "desc": "Hastalığı başlatan intrinsik (genetik) veya ekstrinsik (çevresel) nedendir.", "isKey": True},
                    {"title": "Patogenez", "desc": "Nedenin hücrede tetiklediği moleküler ve biyokimyasal reaksiyonlar dizisidir.", "isKey": True},
                    {"title": "Klinik Görünüm", "desc": "Fonksiyonel yetersizliğin hastada semptom ve bulgu olarak belirmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Hastalık Boyutları",
                    "headers": ["Boyut", "Kapsam", "Klinik Örnek (Miyokard Enfarktüsü)"],
                    "rows": [
                        ["Etiyoloji", "Başlatıcı neden", "Koroner arter aterosklerotik plak rüptürü"],
                        ["Patogenez", "Gelişim mekanizması", "İskemi → ATP tükenmesi → Membran hasarı"],
                        ["Morfoloji", "Yapısal değişiklik", "Koagülatif nekroz alanı, nötrofil infiltrasyonu"],
                        ["Klinik", "Semptom ve bulgu", "Göğüs ağrısı, troponin yüksekliği, kardiyojenik şok"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hastalık gelişimi: Etiyoloji → Patogenez → Morfolojik değişiklikler → Klinik bulgular.",
                "📌 [YÜKSEK VERİM] Patoloji, moleküler patogenez ile yatak başındaki klinik belirtiler arasındaki köprüdür."
            ],
            "medicalTerms": [
                {"term": "Etiyoloji", "explanation": "Bir hastalığın ortaya çıkmasına yol açan başlatıcı neden veya faktördür."},
                {"term": "Patogenez", "explanation": "Hastalığın başlangıcından nihai tablosuna kadar geçen hücresel gelişim mekanizmasıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Patolojide Temel Kavramlar",
                    "Etiyoloji (Neden)",
                    "Patogenez (Mekanizma)",
                    [
                        "Hastalığı başlatan ilk etkendir",
                        "Genetik veya edinsel olabilir",
                        "Örnek: Koroner arter trombozu"
                    ],
                    [
                        "Hücresel yanıt ve reaksiyonlar zinciridir",
                        "Biyokimyasal ve moleküler süreçtir",
                        "Örnek: ATP tükenmesi ve nekroz oluşumu"
                    ]
                ),
                make_cloze(
                    "Bir hastalığın başlangıcından tam klinik tablosuna kadar gelişen hücresel ve moleküler olaylar dizisine patogenez denir.",
                    "patogenez",
                    "Tıbbi Süreç"
                )
            ]
        },
        {
            "slideNumber": 4,
            "title": "Hücre Hasarının Nedenleri Spektrumu",
            "subtitle": "Fiziksel, kimyasal, biyolojik ve immünolojik hasar kaynakları",
            "badge": "Etiyoloji",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre hasarı çok çeşitli intrinsik (içsel) ve ekstrinsik (dışsal) nedenlerle tetiklenebilir. "
                "Tıbbi pratikte hücre hasarının en yaygın nedeni hipoksi ve iskemidir. Bununla birlikte "
                "toksik kimyasallar, enfeksiyon ajanları, otoimmün ve immünolojik reaksiyonlar, genetik "
                "kusurlar, beslenme dengesizlikleri ve fiziksel travmalar da hücreleri doğrudan zedeler.\n\n"
                "> [KLİNİK İPUCU] Aynı hücre hasarı tablosu, birden çok etiyolojik ajanın ortak bir hücresel "
                "yolağı (örneğin mitokondri hasarı veya serbest radikal üretimi) tetiklemesiyle gelişebilir.\n\n"
                "Her bir hasar etkeni hücrede kendine özgü bir duyarlılık ve patolojik süreç başlatır; "
                "bu süreçlerin ayrıntılı bilinmesi doğru tedavi stratejisinin kurulması için şarttır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Hipoksi & İskemi", "desc": "Klinikte en sık karşılaşılan oksijensizlik ve perfüzyon kaybı nedenidir.", "isKey": True},
                    {"title": "Toksinler", "desc": "İlaçlar, çevresel zehirler ve yaşam tarzı kaynaklı kimyasallardır.", "isKey": False},
                    {"title": "İmmün Reaksiyonlar", "desc": "Otoimmünite ve aşırı duyarlılık nedeniyle dokunun kendi savunmasınca yıkımıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Hasar Nedenleri ve Mekanizmaları",
                    "headers": ["Hasar Nedeni", "Tipik Örnek", "Hücresel Etki Mekanizması"],
                    "rows": [
                        ["Hipoksi / İskemi", "Miyokard enfarktüsü", "Oksidatif fosforilasyon durur, ATP tükenir"],
                        ["Toksinler", "Karbon tetraklorür (CCl4)", "Serbest radikallerle lipid peroksidasyonu"],
                        ["İmmün Reaksiyonlar", "Romatoid artrit", "Sitokinler ve komplemanla membran lizisi"],
                        ["Fiziksel Ajanlar", "Radyasyon, yanık", "DNA kırıkları ve protein denatürasyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarı ve nekrozun en sık görülen nedeni hipoksi ve iskemidir.",
                "📌 [YÜKSEK VERİM] İmmün sistem yabancı ajanları temizlerken sekonder olarak ağır doku hasarı oluşturabilir."
            ],
            "medicalTerms": [
                {"term": "İskemi", "explanation": "Dokuya gelen arteriyel kan akımının azalması veya tamamen kesilmesidir."},
                {"term": "Hipoksi", "explanation": "Dokularda hücresel solunum için gereken oksijen basıncının yetersiz olmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tıbbi patolojide ve klinik uygulamada hücre hasarı ve nekrozun en sık görülen nedeni aşağıdakilerden hangisidir?",
                    {
                        "A": "Beslenme dengesizlikleri ve vitamin fazlalığı",
                        "B": "Hipoksi ve iskemi",
                        "C": "İyonizan radyasyon maruziyeti",
                        "D": "Kalıtsal tek gen mutasyonları",
                        "E": "Mekanik travma ve künt yaralanmalar"
                    },
                    "B",
                    {
                        "A": "Beslenme bozuklukları önemlidir fakat en sık hasar nedeni değildir.",
                        "B": "Doğru cevap B'dir: Hipoksi ve iskemik vasküler tıkanmalar hücre hasarının en sık nedenidir.",
                        "C": "Radyasyon spesifik bir fiziksel hasar nedenidir, toplumda en sık değildir.",
                        "D": "Genetik mutasyonlar daha az sıklıkta görülür.",
                        "E": "Mekanik travma sık rastlansa da sistemik hücresel ölümlerin ana nedeni iskemidir."
                    }
                ),
                make_cloze(
                    "Klinik pratikte hücre hasarı ve nekrozun en sık rastlanan nedeni hipoksi ve iskemidir.",
                    "hipoksi ve iskemidir",
                    "En Sık Neden"
                )
            ]
        },
        {
            "slideNumber": 5,
            "title": "Hipoksi ile İskemi Arasındaki Kritik Ayırıcı Tanı",
            "subtitle": "Yalnızca oksijensizlik ile perfüzyon kaybının hücresel sonuçları",
            "badge": "Ayırıcı Tanı",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hipoksi ve iskemi tıp terminolojisinde sıklıkla birbirinin yerine kullanılsa da aralarında "
                "çok kritik patofizyolojik farklar vardır. Hipoksi, dokuya ulaşan oksijenin azalmasıdır; "
                "ancak glukoz gibi besin maddeleri damar yoluyla gelmeye ve toksik metabolik atıklar "
                "venöz yoldan uzaklaştırılmaya devam edebilir.\n\n"
                "> [KRİTİK UYARI] İskemi, kan akımının kesilmesidir; hücreye ne oksijen ne de glukoz gelebilir, "
                "üstelik laktik asit gibi metabolitler birikerek doku pH'ını hızla düşürür.\n\n"
                "Bu nedenle iskemi, saf hipoksiye kıyasla dokuları çok daha hızlı ve şiddetli biçimde "
                "zedeler. İskemik dokuda anaerobik glikoliz bile substrat yokluğundan ötürü erken çöker."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Hipoksi Tanımı", "desc": "Oksijen parsiyel basıncının veya oksijen taşıma kapasitesinin azalmasıdır.", "isKey": True},
                    {"title": "İskemi Tanımı", "desc": "Arteriyel tıkanma veya venöz drenaj yetersizliğiyle perfüzyonun durmasıdır.", "isKey": True},
                    {"title": "Hız Farkı", "desc": "İskemi besin akışını kestiği ve atıkları biriktirdiği için hipoksiden daha hızlı öldürür.", "isKey": True}
                ],
                "table": {
                    "title": "Hipoksi vs İskemi",
                    "headers": ["Özellik", "Hipoksi", "İskemi"],
                    "rows": [
                        ["Kan Akımı", "Korunmuş veya azalmış", "Kesilmiş veya kritik düzeyde düşmüş"],
                        ["Glikolitik Besin Temini", "Glukoz taşınabilir", "Glukoz girişi tamamen kesilir"],
                        ["Metabolit Uzaklaştırma", "Laktat kısmen yıkanır", "Laktat birikir, asidoz hızlanır"],
                        ["Hasar Hızı", "Rölatif olarak yavaş", "Çok daha hızlı ve yıkıcı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemi dokuyu hipoksiden daha hızlı zedeler; çünkü hem oksijensizliği hem de glukozsuzluğu ve asidozu içerir.",
                "🚨 [KRİTİK UYARI] Saf hipokside (ör. anemi, CO zehirlenmesi) kan akımı sürdüğü için anaerobik glikoliz bir süre daha çalışabilir."
            ],
            "medicalTerms": [
                {"term": "Perfüzyon", "explanation": "Kapiller yataktan doku hücrelerine doğru gerçekleşen arteriyel kan dolaşımıdır."},
                {"term": "Laktik Asidoz", "explanation": "Oksijensiz kalan hücrelerin anaerobik glikolizle ürettiği laktat birikimi sonucu pH düşüşüdür."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Hipoksi ve İskemi Karşılaştırması",
                    "Hipoksi (Oksijensizlik)",
                    "İskemi (Perfüzyon Yokluğu)",
                    [
                        "Kan akımı devam edebilir",
                        "Glukoz taşınması sürebilir",
                        "Metabolitler yıkanabilir",
                        "Hasar nispeten daha yavaş gelişir"
                    ],
                    [
                        "Kan akımı kesilmiştir",
                        "Glukoz ve besin desteği kesilir",
                        "Laktik asit birikir ve pH hızla düşer",
                        "Hücreler çok daha hızlı nekroza gider"
                    ]
                ),
                make_cloze(
                    "Kan akımının durması nedeniyle dokunun hem oksijensiz hem de glukozsuz kaldığı duruma iskemi denir.",
                    "iskemi",
                    "Dolaşım Bozukluğu"
                )
            ]
        },
        {
            "slideNumber": 6,
            "title": "Hipoksinin Başlıca Klinik Etyolojileri",
            "subtitle": "Arter tıkanması, solunum yetmezliği, anemi ve CO zehirlenmesi",
            "badge": "Etiyoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hipoksi klinik pratikte 5 ana mekanizmayla ortaya çıkar: 1) İskemik arteriyel tıkanmalar "
                "(en sık neden), 2) Akciğer hastalıkları (KOAH, pnömoni veya ARDS sonucu kanın "
                "oksijenlenmesinde azalma), 3) Anemi (hemoglobin konsantrasyonunun düşmesi), 4) Karbon "
                "monoksit (CO) zehirlenmesi (hemoglobine geri dönüşümsüz bağlanma) ve 5) Şok/ağır kan kaybı.\n\n"
                "> [SINAV SPOTU] Karbon monoksit hemoglobine oksijenden ~200 kat daha yüksek afiniteyle bağlanır "
                "ve karboksihemoglobin oluşturarak dokulara oksijen salınmasını engeller.\n\n"
                "Anemide arteriyel pO2 normal olmasına rağmen total oksijen içeriği azalmıştır; siyanoz "
                "oluşmazken dokular derin hipoksi yaşar. Bu etyolojilerin ayrımı acil tedavi seçimini belirler."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "İskemik Tıkanma", "desc": "Tromboz veya emboli sonucu lokal oksijen desteğinin kesilmesidir.", "isKey": True},
                    {"title": "Akciğer Patolojileri", "desc": "Alveolo-kapiller gaz difüzyonunun bozulmasıyla sistemik hipoksemi gelişmesidir.", "isKey": False},
                    {"title": "CO Zehirlenmesi", "desc": "Karboksihemoglobin oluşumuyla dokulara oksijen transferinin bloke edilmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Hipoksi Tipleri ve Mekanizmaları",
                    "headers": ["Hipoksi Tipi", "pO2 Düzeyi", "Oksijen Taşıma Kapasitesi", "Tipik Klinik Neden"],
                    "rows": [
                        ["Hipoksik Hipoksi", "Düşük", "Normal", "KOAH, yüksek irtifa, ARDS"],
                        ["Anemik Hipoksi", "Normal", "Düşük (Hb azlığı)", "Demir eksikliği anemisi, kanama"],
                        ["Toksik Hipoksi", "Normal", "Karboksihemoglobin yüksek", "Karbon monoksit inhalasyonu"],
                        ["İskemik Hipoksi", "Lokal sıfır", "Sistemik normal", "Arteriyel trombüs, emboli"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] CO zehirlenmesinde ve anemide arteriyel pO2 normal olabilir, ancak dokuya oksijen sunumu kritik derecede yetersizdir.",
                "📌 [KLİNİK İPUCU] CO zehirlenmesinde hastanın kanı vişne kırmızısı (kiraz kırmızısı) görünüm alabilir."
            ],
            "medicalTerms": [
                {"term": "Karboksihemoglobin", "explanation": "Karbon monoksitin hemoglobindeki demir atomuna sıkı bağlanmasıyla oluşan bileşiktir."},
                {"term": "Hipoksemi", "explanation": "Arteriyel kanda oksijen parsiyel basıncının (pO2) normalin altına düşmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Hipoksi Etyolojileri",
                    ["Mekanizma", "Primer Neden", "Klinik Özellik"],
                    [
                        [("İskemi", False), ("Tromboz veya emboli", False), ("En sık hasar nedeni", True, "Sıklık")],
                        [("Hipoksemi", False), ("Akciğer hastalığı (ARDS)", False), ("pO2 düşüktür", True, "Gaz Basıncı")],
                        [("Anemi", False), ("Hemoglobin azalması", False), ("pO2 normal, içerik az", True, "Laboratuvar")],
                        [("Toksisite", False), ("Karbon monoksit", False), ("Karboksihemoglobin artar", True, "Bağlanma")]
                    ]
                ),
                make_cloze(
                    "Karbon monoksit zehirlenmesinde hemoglobin ile birleşerek oksijen taşınmasını engelleyen bileşik karboksihemoglobindir.",
                    "karboksihemoglobindir",
                    "Toksik Bileşik"
                )
            ]
        },
        {
            "slideNumber": 7,
            "title": "Toksinler ve Kimyasal Ajanların Neden Olduğu Hasar",
            "subtitle": "Çevresel kirleticiler, ilaçlar ve serbest radikal aracılı zedelenme",
            "badge": "Toksikoloji",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Kimyasal ajanlar ve toksinler günlük yaşamda veya tıbbi tedaviler sırasında hücre zedelenmesine "
                "yol açan önemli etkenlerdir. Bazı kimyasallar doğrudan hücresel organellere bağlanarak "
                "hasar verir (örneğin civa, hücre membran sülfhidril gruplarına bağlanarak geçirgenliği bozar). "
                "Bazı toksinler ise sitokrom P-450 enzimleri tarafından metabolize edilerek aktif toksik "
                "serbest radikallere dönüştürülür.\n\n"
                "> [TEMEL İLKE] Karbon tetraklorür (CCl4) karaciğerde SER'de CCl3* serbest radikaline dönüşerek "
                "endoplazmik retikulum zarlarında hızlı lipid peroksidasyonuna yol açar.\n\n"
                "Terapötik ilaçlar (örneğin parasetamol/asetaminofen) aşırı dozda alındığında glutatyon "
                "depolarını tüketerek masif hepatosit nekrozuna ve akut karaciğer yetmezliğine yol açar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Direkt Hasar", "desc": "Kimyasalın doğrudan hücresel moleküllere bağlanarak fonksiyonu bozmasıdır.", "isKey": True},
                    {"title": "İndirekt Hasar", "desc": "Karaciğerde sitokrom P-450 ile toksik metabolitlere çevrilerek hasar vermesidir.", "isKey": True},
                    {"title": "Parasetamol Toksisitesi", "desc": "Aşırı dozda NAPQI metabolitinin glutatyonu tüketerek nekroz yapmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Toksik Hasar Mekanizmaları",
                    "headers": ["Toksin / Kimyasal", "Hasar Tipi", "Hücresel Hedef ve Sonuç"],
                    "rows": [
                        ["Civa klorür", "Doğrudan hasar", "Membran proteinlerindeki -SH grupları bloke olur"],
                        ["Karbon tetraklorür (CCl4)", "İndirekt (CCl3*)", "SER zarlarında lipid peroksidasyonu, yağlanma"],
                        ["Asetaminofen (Yüksek Doz)", "Reaktif ara ürün (NAPQI)", "Glutatyon tükenmesi, mitokondriyal çöküş"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] CCl4 karaciğerde sitokrom P-450 ile reaktif serbest radikale (CCl3*) dönüşerek membran lipid peroksidasyonu yapar.",
                "📌 [KLİNİK İPUCU] Terapötik dozda güvenli olan ilaçlar aşırı dozda veya sitokrom indükleyicileriyle birlikte ölümcül toksik hasar yapabilir."
            ],
            "medicalTerms": [
                {"term": "Lipid Peroksidasyonu", "explanation": "Serbest radikallerin membran lipidlerindeki doymamış çift bağlara saldırarak zarı parçalamasıdır."},
                {"term": "Sitokrom P-450", "explanation": "Karaciğer düz endoplazmik retikulumunda ilaç ve ksenobiyotikleri metabolize eden enzim sistemidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Karbon tetraklorürün düz endoplazmik retikulumda serbest radikale dönüşerek başlattığı yıkıcı reaksiyona lipid peroksidasyonu denir.",
                    "lipid peroksidasyonu",
                    "Membran Yıkımı"
                ),
                make_active_recall(
                    "CCl4 toksisitesinde lipid peroksidasyonu nasıl hücresel şişme ve steatoza yol açar?",
                    "SER membranlarının parçalanması protein sentezini (apoprotein) durdurur; hepatosit içine giren yağlar VLDL halinde salgılanamaz ve birikir, iyon pompaları bozularak şişme eklenir."
                )
            ]
        },
        {
            "slideNumber": 8,
            "title": "Enfeksiyonlar ve İmmünolojik Hücre Hasarı",
            "subtitle": "Bakteriyel toksinlerden otoimmün doku yıkımına uzanan patoloji",
            "badge": "İmmünopatoloji",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Enfeksiyöz mikroorganizmalar virüslerden helmintlere kadar geniş bir hasar yelpazesine sahiptir. "
                "Bakteriler endotoksin (LPS) veya ekzotoksin salgılayarak doğrudan membran delikleri açabilir "
                "veya hücre içi sinyalleri felç edebilir. Virüsler ise konak hücre içine yerleşerek konak "
                "protein sentezini durdurur veya doğrudan sitopatik lizise yol açar.\n\n"
                "> [KRİTİK UYARI] Çoğu enfeksiyonda esas doku hasarını mikroorganizmanın kendisi değil, "
                "konak bağışıklık sisteminin verdiği aşırı inflamatuar reaksiyon oluşturur.\n\n"
                "İmmünolojik reaksiyonlar, otoimmün hastalıklarda (ör. lupus, romatoid artrit) kendi antijenlerine "
                "saldırarak veya aşırı duyarlılık reaksiyonlarında masif hücre lizisine neden olur."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Bakteriyel Toksinler", "desc": "Hücre zarını perfore eden veya enzimatik aktiviteyi durduran proteinlerdir.", "isKey": True},
                    {"title": "Sitopatik Virüsler", "desc": "Hücre içinde çoğalarak konak hücrenin patlamasına yol açan viral ajanlardır.", "isKey": False},
                    {"title": "İmmün Yıkım", "desc": "Sitotoksik T hücreleri, kompleman ve reaktif oksijen ürünleriyle doku hasarıdır.", "isKey": True}
                ],
                "table": {
                    "title": "İmmünolojik Hasar Kalıpları",
                    "headers": ["Etken / Mekanizma", "Tipik Hastalık", "Doku Hasarı Sonucu"],
                    "rows": [
                        ["Sitotoksik T Lenfosit (CD8+)", "Viral Hepatit B/C", "Virüsle enfekte hepatositlerde apoptoz"],
                        ["İmmün Kompleks Birikimi", "Sistemik Lupus Eritematozus", "Damar duvarlarında vaskülit ve fibrinoid nekroz"],
                        ["Bakteriyel Ekzotoksin", "Gazlı Gangren (Clostridium)", "Masif koagülatif ve likefaksiyon nekrozu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Viral hepatitte hepatosit hasarının ana nedeni virüsün kendisi değil, konağın CD8+ sitotoksik T hücrelerinin enfekte hücreleri öldürmesidir.",
                "🚨 [KRİTİK UYARI] İmmün sistemin aşırı aktivasyonu, enfeksiyon ajanından daha yıkıcı doku nekrozuna yol açabilir."
            ],
            "medicalTerms": [
                {"term": "Sitopatik Etki", "explanation": "Virüs enfeksiyonu sonucu konak hücrede oluşan mikroskobik yapısal bozulma ve ölümdür."},
                {"term": "Otoimmünite", "explanation": "Bağışıklık sisteminin konağın kendi sağlıklı doku antijenlerini yabancı kabul edip saldırmasıdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Kronik Hepatit B hastasında karaciğer hasarının altında yatan immünolojik mekanizma senaryosu.",
                    [
                        {
                            "text": "Virüs doğrudan hepatositleri fagosite ederek mekanik olarak parçalar.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Virüsler fagositoz yapmaz."
                        },
                        {
                            "text": "Konağın CD8+ sitotoksik T lenfositleri, yüzeyinde viral antijen taşıyan hepatositleri yabancı görerek apoptoza ve nekroza sürükler.",
                            "isCorrect": True,
                            "feedback": "Doğru immünopatolojik mekanizma! Karaciğer hasarı virüsün toksisitesinden değil, konağın immün yanıtından kaynaklanır."
                        },
                        {
                            "text": "Virüs karaciğerdeki safra asitlerini kristalleştirip taş oluşturur.",
                            "isCorrect": False,
                            "feedback": "İlgisiz."
                        }
                    ]
                ),
                make_cloze(
                    "Viral hepatitte karaciğer hücre hasarı virüsün doğrudan etkisinden ziyade konağın sitotoksik T hücrelerinin immün yanıtıyla oluşur.",
                    "sitotoksik T hücrelerinin",
                    "Bağışıklık Hücresi"
                )
            ]
        },
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Homeostaz ve Hasar Spektrumu",
            "subtitle": "Hücre hasarı kavramı, etiyoloji, hipoksi vs iskemi ve toksinler",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 1,
            "synthesisNarrative": (
                "Bu ilk kontrol noktasında, hücrenin sağlıklı homeostaz halinden hasar ve ölüme uzanan temel "
                "fizyopatolojik seyrini pekiştiriyoruz. Sağlıklı bir hücre fizyolojik sınırlarını aşan stresle "
                "karşılaştığında önce adaptasyon dener; stres şiddetliyse geri dönüşümlü veya geri dönüşümsüz "
                "hasara sürüklenir.\n\n"
                "> [ÖZET VURGU] İskemi dokuyu saf hipoksiden çok daha hızlı öldürür; çünkü glukoz desteği de "
                "kesilir ve toksik asit metabolitleri dokuda birikir.\n\n"
                "Aşağıdaki 3 kritik akıl kartını gözden geçirerek temel kavramları tam olarak hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Homeostaz Kaybı", "desc": "Hücre hasarının başlangıç kriteri iç dengenin korunamamasıdır.", "isKey": True},
                    {"title": "İskemi Üstünlüğü", "desc": "İskemi = hipoksi + besinsizlik + metabolit birikimidir.", "isKey": True},
                    {"title": "Hasar Spektrumu", "desc": "Normal → Adaptasyon → Geri dönüşümlü hasar → Geri dönüşümsüz hasar → Ölüm.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 1 Sentez Tablosu",
                    "headers": ["Kavram", "Tanım", "En Kritik Sınav İlkesi"],
                    "rows": [
                        ["Homeostaz", "Dinamik fizyolojik iç denge", "Bozulması hücre hasarını başlatır"],
                        ["İskemi", "Arteriyel kan akımının kesilmesi", "Saf hipoksiden çok daha hızlı hasar yapar"],
                        ["Geri Dönüşümlü Hasar", "Membranın korunduğu evre", "Etken kalkarsa tam iyileşme mümkündür"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarının en sık nedeni hipoksi ve iskemidir.",
                "📌 [SINAV SPOTU] Sıralama: Homeostaz → Adaptasyon → Geri dönüşümlü hasar → Geri dönüşümsüz hasar → Hücre ölümü."
            ],
            "medicalTerms": [
                {"term": "Nekroz", "explanation": "Canlı dokuda hücre zarlarının parçalanmasıyla gelişen daima patolojik hücre ölümüdür."},
                {"term": "Apoptoz", "explanation": "İnflamasyon oluşturmadan gerçekleşen programlı ve düzenli hücresel intihar yolağıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-001",
                    "Hücre hasarı ile hücresel adaptasyon arasındaki temel ayrım çizgisi nedir?",
                    "Adaptasyonda hücre yeni bir kararlı duruma ulaşarak canlılığını fonksiyonel olarak sürdürür; hücre hasarında ise homeostaz mekanizmaları aşılır ve fonksiyon bozulur."
                ),
                make_flashcard(
                    "fc-k1-04-002",
                    "Neden iskemi saf hipoksiden çok daha hızlı ve şiddetli hücre hasarına yol açar?",
                    "Çünkü iskemide sadece oksijen değil, glukoz gibi anaerobik substratlar da kesilir ve laktik asit gibi metabolitler birikerek doku pH'ını hızla düşürür."
                ),
                make_flashcard(
                    "fc-k1-04-003",
                    "Karbon monoksit zehirlenmesinde arteriyel pO2 neden normal olduğu halde dokuda hipoksi gelişir?",
                    "CO hemoglobine çok yüksek afiniteyle bağlanıp oksijeni yerinden eder; kandaki çözünmüş oksijen basıncı (pO2) normal kalırken dokuya transfer edilen oksijen kritik olarak düşer."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 1 Sentezi: Bir dokuda geri dönüşümlü hasarın geri dönüşümsüz hasara dönüşmesindeki dönüm noktası nedir?",
                    "Mitokondri fonksiyonunun geri kazanılamaz biçimde çökmesi ve plazma/organel zarlarında kalıcı parçalanmaların meydana gelmesidir."
                ),
                make_cloze(
                    "Hücre içi organel zarlarının korunduğu ancak işlevin bozulduğu başlangıç evresine geri dönüşümlü hasar denir.",
                    "geri dönüşümlü hasar",
                    "Başlangıç Fazı"
                )
            ]
        }
    ]
