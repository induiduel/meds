import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
decks_file = 'src/data/interactive_learning_decks.json'
meta_file = 'src/data/learning_decks_meta.json'
past_q_file = 'src/data/pastQuestions.json'

with open(decks_file, 'r', encoding='utf-8') as f:
    existing_decks = json.load(f)

with open(past_q_file, 'r', encoding='utf-8') as f:
    all_past_questions = json.load(f)

print(f"Loaded {len(existing_decks)} existing decks and {len(all_past_questions)} past questions.")

# High-yield real past questions on Urolithiasis (Taş Hastalığı)
matched_questions_dict = {
    'q_dusg_radiopacity': {
        'id': 'd3-k1-uro-008',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Radyoloji',
        'topic': 'Üriner Taşların Radyoopasite Özellikleri',
        'stem': 'Direkt üriner sistem grafisinde (DÜSG) belirgin radyoopak (gözle görülebilir beyaz radyoopasite) izlenen taş türü aşağıdakilerden hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Ürik asit taşı'},
            {'key': 'B', 'text': 'Kalsiyum oksalat taşı', 'isCorrect': True},
            {'key': 'C', 'text': 'Ksantin taşı'},
            {'key': 'D', 'text': 'İndinavir (ilaç) taşı'},
            {'key': 'E', 'text': 'Triamteren taşı'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Üriner sistem taşlarının en sık tipi olan kalsiyum tuzları (kalsiyum oksalat ve kalsiyum fosfat) yüksek kalsiyum içeriği nedeniyle DÜSG\'de belirgin şekilde RADYOOPAK görünür. Ürik asit, ksantin ve indinavir taşları ise RADYOLÜSENTTİR; konvansiyonel röntgende seçilemez, ancak kontrassız batın BT veya USG ile saptanabilir. Sistin ve strüvit taşları ise zayıf radyoopaktır.'
    },
    'q_struvite_urease': {
        'id': 'd3-k1-uro-009',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Tıbbi Mikrobiyoloji',
        'topic': 'Enfeksiyon (Strüvit) Taşları ve Üreaz Pozitif Bakteriler',
        'stem': 'Alkalik idrar pH\'sında (pH > 7.0-7.5) çökme eğilimi artan ve üreaz pozitif bakterilerin (özellikle Proteus mirabilis) enfeksiyonuyla oluşan enfeksiyon (strüvit) taşlarının temel bileşeni hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Magnezyum amonyum fosfat (Strüvit)', 'isCorrect': True},
            {'key': 'B', 'text': 'Ürik asit'},
            {'key': 'C', 'text': 'Sistin'},
            {'key': 'D', 'text': 'Kalsiyum oksalat monohidrat'},
            {'key': 'E', 'text': 'Ksantin'}
        ],
        'correctAnswer': 'A',
        'explanation': 'Üreaz üreten bakteriler (özellikle Proteus mirabilis, ayrıca Klebsiella, Pseudomonas, Serratia) üreyi hidroliz ederek amonyak ve bikarbonat açığa çıkarır; bu durum idrar pH\'sını belirgin şekilde bazikleştirir (pH > 7.2). Alkalik ortamda magnezyum amonyum fosfat (strüvit) ve karbonat apatit tuzları hızla çökerek toplayıcı sistemi dolduran geyik boynuzu (staghorn) taşlarını oluşturur. E. coli üreaz negatif olduğu için tipik olarak strüvit taşı yapmaz.'
    },
    'q_cystinuria_cola': {
        'id': 'd3-k1-uro-010',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Tıbbi Biyoloji ve Genetik',
        'topic': 'Sistünüri ve COLA Taşıyıcı Defekti',
        'stem': 'Genetik olarak proksimal renal tübül ve intestinal bazik aminoasit transport sistemindeki mutasyona bağlı gelişen sistinüride idrarla atılımı artan aminoasit grubu (COLA) aşağıdakilerden hangisinde eksiksiz verilmiştir?',
        'options': [
            {'key': 'A', 'text': 'Sistin, Ornitin, Lizin, Arginin', 'isCorrect': True},
            {'key': 'B', 'text': 'Sistin, Glisin, Alanin, Serin'},
            {'key': 'C', 'text': 'Sistin, Metiyonin, Triptofan, Tirozin'},
            {'key': 'D', 'text': 'Sistin, Fenilalanin, Valin, Lösin'},
            {'key': 'E', 'text': 'Sistin, Glutamin, Prolin, Histidin'}
        ],
        'correctAnswer': 'A',
        'explanation': 'Sistinüri, SLC3A1 ve SLC7A9 gen mutasyonlarına bağlı otozomal resesif geçişli bir transport bozukluğudur. Proksimal tübülde dibazik aminoasitlerin (Sistin, Ornitin, Lizin, Arginin - COLA) geri emilimi bozulur. İdrarda bu 4 aminoasidin atılımı artar; ancak ornitin, lizin ve arginin suda çözünürken sistin fizyolojik idrar pH\'sında oldukça zor çözünür ve hekzagonal (altıgen) kristaller oluşturarak rekürren sistin taşlarına yol açar.'
    },
    'q_uric_acid_ph': {
        'id': 'd3-k1-uro-011',
        'examYear': '2022-2025',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Tıbbi Biyokimya',
        'topic': 'Ürik Asit Taşı Patofizyolojisi ve İdrar pH İlişkisi',
        'stem': 'Ürik asit taşlarının patofizyolojisinde kristalleşmeyi ve taş oluşumunu tetikleyen EN KRİTİK ve birincil belirleyici etken aşağıdakilerden hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Aşırı ürik asit atılımı (Ağır hiperürikozüri)'},
            {'key': 'B', 'text': 'Sürekli düşük idrar pH\'sı (Asidik idrar, pH < 5.5)', 'isCorrect': True},
            {'key': 'C', 'text': 'Alkali idrar pH\'sı (pH > 7.5)'},
            {'key': 'D', 'text': 'Aşırı kalsiyum atılımı'},
            {'key': 'E', 'text': 'İdrar sitrat düzeyinin çok yüksek olması'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Ürik asidin pKa değeri yaklaşık 5.35\'tir. İdrar pH\'sı pKa\'nın altına indiğinde (pH < 5.5), ürik asit iyonize ürat formundan çözünmeyen serbest/nötral ürik asit formuna geçer ve çözünürlüğü dramatik şekilde düşer. Birçok hastada 24 saatlik idrar ürik asit miktarı normal olsa dahi, kalıcı asidik idrar (pH < 5.5) varlığında ürik asit taşları hızla oluşur. Tedavideki en etkili adım idrarın potasyum sitrat veya sodyum bikarbonat ile alkalinizasyonudur (hedef pH 6.5-7.0).'
    },
    'q_randall_plaque': {
        'id': 'd3-k1-uro-012',
        'examYear': '2023-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Tıbbi Patoloji',
        'topic': 'Randall Plak Teorisi ve Kalsiyum Oksalat Taşı Nükleasyonu',
        'stem': 'Alexander Randall plak teorisine göre kalsiyum oksalat taşlarının başlangıç çekirdeğini oluşturan interstisyel kalsiyum apatit birikintileri ilk olarak hangi anatomik yapının bazal membranında başlar?',
        'options': [
            {'key': 'A', 'text': 'Proksimal kıvrıntılı tübül fırçamsı kenarı'},
            {'key': 'B', 'text': 'Bowman kapsülü parietal yaprağı'},
            {'key': 'C', 'text': 'İnce Henle kulpunun iç medüller toplayıcı kanal komşuluğundaki bazal membranı', 'isCorrect': True},
            {'key': 'D', 'text': 'Mesane trigonu submukozası'},
            {'key': 'E', 'text': 'Üreteropelvik bileşke adventisyası'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Randall plak teorisinde taş oluşumunun başlangıç olayı, ince Henle kulpunun bazal membranında kalsiyum fosfat (karbonat apatit) kristallerinin çökmesidir. Bu birikintiler medüller interstisyum boyunca ilerleyerek renal papilla ucuna ulaşır, papiller ürotelyumu erode ederek idrarla temas eden sabit bir nidus yüzeyi oluşturur. Bu yüzey üzerine idrardaki kalsiyum oksalat kristalleri yapışarak (epitaksi) taşı büyütür.'
    }
}

# 20 Deep, Authoritative Slides Based on Official Lecture Note '2)Ürolitiyazis Patofizyolojisi.txt'
slides_batch2 = [
    # Slide 1
    {
        'slideNumber': 1,
        'title': 'Ürolitiyazis: Tanım, Epidemiyoloji ve Coğrafi Taş Kuşağı',
        'subtitle': 'Dünyada ve Türkiye\'de prevalans dinamikleri, demografik dağılım ve artış trendi',
        'badge': 'Epidemiyoloji & Demografi',
        'badgeColor': 'sky',
        'synthesisNarrative': '**Ürolitiyazis**, böbrek toplayıcı sisteminden üretra measına kadar üriner traktüsün herhangi bir anatomik seviyesinde taş (kalkülüs) oluşması tablosudur. Son dekadlarda yaşam tarzı, beslenme alışkanlıkları ve küresel ısınmaya ikincil olarak üriner taş hastalığının prevalansı dünya genelinde %1\'den %20\'lere ulaşan doğrusal bir artış göstermiştir. Türkiye, dünya coğrafyasında **"Taş Kuşağı (Stone Belt)"** olarak tanımlanan ve sıcak/kuru iklim özellikleriyle karakterize risk kuşağında yer almaktadır. Ülkemizde erişkin popülasyonda taş görülme sıklığı yaklaşık **%15** olarak tespit edilmiştir.',
        'flashcards': [
            {
                'id': 'uro-fc-01-01',
                'category': 'Epidemiyoloji',
                'front': 'Türkiye\'de üriner sistem taş hastalığı (ürolitiyazis) görülme prevalansı yaklaşık yüzde kaçtır?',
                'hint': 'Taş kuşağında yer alan ülkeler için tipik yüksek orandır.',
                'back': 'Türkiye\'de taş hastalığı görülme sıklığı yaklaşık **%15**\'tir. Türkiye, Akdeniz ve Orta Doğu coğrafyasını kapsayan küresel **"Taş Kuşağı (Stone Belt)"** içerisinde yer almaktadır.'
            },
            {
                'id': 'uro-fc-01-02',
                'category': 'Demografi',
                'front': 'Ürolitiyazis insidansı yaşamın hangi dekadlarında zirve (pik) yapar ve cinsiyet oranı nasıl değişmektedir?',
                'hint': 'Erişkin çalışma çağı ve erkek/kadın oranındaki son trend.',
                'back': 'Taş insidansı **4. ila 6. dekatta (30-60 yaş)** zirve yapar. Tarihsel olarak erkeklerde 2-3 kat daha sıktı; ancak son 20 yılda kadınlarda obezite ve metabolik sendrom artışıyla cinsiyet farkı hızla kapanmaktadır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Küresel Prevalans Artışı',
                    'desc': 'Gelişmiş ülkelerde (ABD, İsveç, Kanada) prevalans >%10 seviyesine ulaşmıştır.',
                    'isKey': True
                },
                {
                    'title': 'Türkiye Taş Kuşağında',
                    'desc': 'Sıcak iklim, genetik yatkınlık ve yüksek sodyum/hayvansal protein tüketimi nedeniyle prevalans %15\'tir.',
                    'isKey': True
                },
                {
                    'title': 'Pediatrik Popülasyon Uyarısı',
                    'desc': 'Genetik bozukluklar (sistinüri, primer hiperoksalüri) dışında 20 yaş öncesi nadirdir; ancak son 25 yılda çocuk ve ergenlerde taş sıklığı belirgin artmaktadır.'
                }
            ],
            'infographic': {
                'type': 'metrics',
                'items': [
                    {'label': 'Türkiye Prevalansı', 'value': '%15', 'detail': 'Taş kuşağı kuşağı risk bölgesi', 'color': 'red'},
                    {'label': 'Pik Yaş Aralığı', 'value': '40 - 60', 'detail': '4. ila 6. dekat zirvesi', 'color': 'amber'},
                    {'label': '5 Yıllık Nüks Oranı', 'value': '%50', 'detail': 'Metabolik tedavi verilmezse', 'color': 'indigo'}
                ]
            }
        },
        'spotPearls': [
            'Türkiye, taş kuşağı (stone belt) kuşağında olup toplumda her 7 kişiden 1\'inde taş öyküsü mevcuttur.',
            'Taş hastalığı tedavisiz bırakıldığında 5-10 yıl içinde %50 nüks oranına sahiptir.',
            'Erkek/kadın oranı tarihsel 3:1 düzeyinden günümüzde 1.3:1 düzeyine gerilemiştir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Türkiye neden taş kuşağı ülkesidir?',
            'Ürolitiyaziste yaş ve cinsiyet dinamikleri neden değişiyor?'
        ]
    },

    # Slide 2
    {
        'slideNumber': 2,
        'title': 'Çevresel, Mesleki ve Sistemik Risk Faktörleri',
        'subtitle': 'Dehidratasyon, mesleki ısı maruziyeti, metabolik sendrom ve Tip 2 DM etkileşimi',
        'badge': 'Risk Faktörleri & Metabolizma',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Taş patofizyolojisinde temel itici güç, idrar hacminin azalması ve tuz konsantrasyonunun artmasıdır. Sıcak ve kuru iklim koşulları ile fırıncı, döküm işçisi gibi aşırı sıcağa maruz kalan meslek gruplarında perspirasyon (terleme) yoluyla sıvı kaybı idrarı konsantre eder. Sistemik faktörler arasında **Obezite, Kilo Alımı ve Metabolik Sendrom** başı çeker. Özellikle **Tip 2 Diabetes Mellitus**, renal tübüler amonyum üretimini bozarak **düşük idrar pH\'sına (kalıcı asidik idrar)** yol açar ve ürik asit taşlarının en önemli zeminini hazırlar. Ayrıca hiperinsülinemi idrarla oksalat atılımını da artırarak kalsiyum oksalat riskini katlar.',
        'flashcards': [
            {
                'id': 'uro-fc-02-01',
                'category': 'Metabolik Sendrom',
                'front': 'Tip 2 Diabetes Mellitus ve insülin direnci varlığı en sık hangi taş türünün oluşumunu tetikler ve mekanizması nedir?',
                'hint': 'Renal amonyum üretimi bozulur ve idrar pH\'sı düşer.',
                'back': 'En sık **Ürik Asit Taşları**nı tetikler. İnsülin direnci proksimal tübülde amonyogenezi (NH4+ sentezini) bozar. İdrarda tamponlayıcı amonyum azalınca idrar pH\'sı kalıcı olarak asidikleşir (pH < 5.5); bu da ürik asidin kristalleşmesine zemin hazırlar.'
            },
            {
                'id': 'uro-fc-02-02',
                'category': 'Çevresel Faktörler',
                'front': 'Sıcak hava ve dehidratasyonun taş oluşumundaki temel fizyokimyasal etkisi nedir?',
                'hint': 'İdrar volümü ve tuz doygunluğu ilişkisi.',
                'back': 'Perspirasyon ile su kaybı oligüriye yol açar. Düşük idrar hacmi (<1.5-2 L/gün), taş yapıcı tuzların (Ca, Oksalat, Ürik asit) konsantrasyonunu artırarak **üriner süpersatürasyonu (aşırı doygunluk)** kritik eşiğin üzerine çıkarır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Dehidratasyon ve Düşük İdrar Hacmi',
                    'desc': 'Günde <1000-1500 mL idrar çıkışı en önemli tekil bağımsız risk faktörüdür.',
                    'isKey': True
                },
                {
                    'title': 'Metabolik Sendrom ve İnsülin Direnci',
                    'desc': 'Proksimal tübüler amonyogenez defekti -> Asidik idrar (pH < 5.5) -> Ürik asit taşları.',
                    'isKey': True
                },
                {
                    'title': 'Hiperürikemi ve Oksalat Artışı',
                    'desc': 'Obez bireylerde kalsiyum oksalat ve ürik asit aşırı satürasyonu belirgin derecede yüksektir.'
                }
            ],
            'table': {
                'title': 'Sistemik Hastalıklar ve İlişkili Taş Türleri',
                'headers': ['Sistemik Durum', 'Bozulan Mekanizma', 'Gelişen Taş Tipi'],
                'rows': [
                    ['Tip 2 DM / Metabolik Sendrom', 'Bozulmuş amonyogenez, düşük idrar pH (<5.5)', 'Ürik Asit Taşı'],
                    ['Obezite', 'Artmış kalsiyum, oksalat ve ürik asit ekskresyonu', 'CaOx ve Ürik Asit Taşı'],
                    ['Primer Hiperparatiroidizm', 'Aşırı kemik rezorpsiyonu, hiperkalsemi + hiperkalsiüri', 'Kalsiyum Fosfat / CaOx'],
                    ['Malabsorpsiyon (Crohn, Gastrik Bypass)', 'Serbest yağ asitlerinin Ca bağlaması (sabunlaşma)', 'Enterik Hiperoksalüri (CaOx)']
                ]
            }
        },
        'spotPearls': [
            'Günde en az 2.5 litre idrar çıkışı sağlamak (3 L sıvı alımı) taş profilaksisinin 1 numaralı kuralıdır.',
            'Diyabetik hastalarda taşların üçte birinden fazlası ürik asit kökenlidir.',
            'Kilo alımı ve vücut kitle indeksi (VKİ) artışı, kadınlarda taş riskini erkeklerden daha dramatik artırır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_uric_acid_ph']],
        'aiPromptSuggestions': [
            'Tip 2 DM ile ürik asit taşları arasındaki patofizyolojik bağlantı nedir?',
            'Obezite taş oluşumunu nasıl etkiler?'
        ]
    },

    # Slide 3
    {
        'slideNumber': 3,
        'title': 'Taş Etyolojisi & Mineralojik Kimyasal Bileşim',
        'subtitle': 'Whewellite, Weddellite, Apatit, Bruşit, Strüvit ve Organik taşların kimyası',
        'badge': 'Kimyasal Sınıflama & Mineraloji',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Böbrek taşları homojen kitleler olmayıp kristalize inorganik/organik tuzlar ve organik bir proteik matristen meydana gelir. En sık görülen taş grubu **Kalsiyum Oksalat** taşlarıdır (%70-80). Kalsiyum oksalat iki farklı mineral fazında bulunur: **Whewellite (Monohidrat - CaC2O4.H2O)** ve **Weddellite (Dihidrat - CaC2O4.2H2O)**. Whewellite koyu kahverengi, son derece sert ve hiperoksalüriye bağlı gelişen formdur. Kalsiyum fosfat ailesinde **Bruşit (CaHPO4.2H2O)** özel bir yere sahiptir; taş kırma (ESWL) tedavisine en dirençli kalsiyum taşıdır. Enfeksiyon zemininde oluşan **Strüvit (Magnezyum amonyum fosfat)** ise üreaz pozitif bakterilerle ilişkilidir.',
        'flashcards': [
            {
                'id': 'uro-fc-03-01',
                'category': 'Mineraloji',
                'front': 'Kalsiyum oksalat monohidrat ve dihidrat kristallerinin mineral adları nelerdir?',
                'hint': 'Alman mineralogların adıyla anılan Whewellite ve Weddellite.',
                'back': 'Kalsiyum oksalat monohidrat = **Whewellite** (daha sert, hiperoksalüriyle ilişkili). Kalsiyum oksalat dihidrat = **Weddellite** (daha kırılgan, hiperkalsiüriyle ilişkili).'
            },
            {
                'id': 'uro-fc-03-02',
                'category': 'Klinik Zorluk',
                'front': 'Kalsiyum taşları içerisinde ESWL (şok dalga litotripsi) ile kırılması en zor olan kalsiyum fosfat türü hangisidir?',
                'hint': 'Kalsiyum hidrojen fosfat dihidrat bileşimi.',
                'back': '**Bruşit (Kalsiyum hidrojen fosfat dihidrat - CaHPO4.2H2O)**. Yoğun ve sert kristal yapısı nedeniyle ESWL şok dalgalarına dirençlidir; sıklıkla endoskopik (URS/PNL) cerrahi gerektirir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Kalsiyum Taşları (%70-80)',
                    'desc': 'Kalsiyum oksalat (Whewellite, Weddellite) ve Kalsiyum fosfat (Apatit, Bruşit).',
                    'isKey': True
                },
                {
                    'title': 'Enfeksiyon Taşları (%10-15)',
                    'desc': 'Magnezyum amonyum fosfat (Strüvit), Karbonat apatit, Amonyum ürat.',
                    'isKey': True
                },
                {
                    'title': 'Ürik Asit Taşları (%5-10)',
                    'desc': 'Uricite (C5H4N4O3) - Asidik idrar zemininde oluşan radyolüsen taşlar.'
                },
                {
                    'title': 'Genetik & Nadir Taşlar (%1-2)',
                    'desc': 'Sistin (sistünüri), Ksantin (ksantinüri), 2,8-Dihidroksiadenin (APRT eksikliği).'
                }
            ],
            'table': {
                'title': 'Üriner Taşların Mineralojik ve Kimyasal İsimlendirmesi',
                'headers': ['Kimyasal Adı', 'Mineral Adı', 'Kimyasal Formül', 'Klinik Özellik'],
                'rows': [
                    ['Kalsiyum oksalat monohidrat', 'Whewellite', 'CaC2O4 · H2O', 'En sık, sert, hiperoksalüri'],
                    ['Kalsiyum oksalat dihidrat', 'Weddellite', 'CaC2O4 · 2H2O', 'Hiperkalsiüri, kırılgan'],
                    ['Kalsiyum hidrojen fosfat', 'Bruşit', 'CaHPO4 · 2H2O', 'ESWL\'ye en dirençli Ca taşı'],
                    ['Bazik kalsiyum fosfat', 'Apatit', 'Ca10(PO4)6(OH)2', 'Randall plak başlangıcı'],
                    ['Magnezyum amonyum fosfat', 'Strüvit', 'MgNH4PO4 · 6H2O', 'Üreaz (+) enfeksiyon, staghorn'],
                    ['Ürik asit', 'Uricite', 'C5H4N4O3', 'Radyolüsen, pH < 5.5'],
                    ['Sistin', 'Sistin', '[SCH2CH(NH2)COOH]2', 'Genetik COLA defekti, hekzagonal']
                ]
            }
        },
        'spotPearls': [
            'Tüm böbrek taşlarının yaklaşık %75\'i kalsiyum oksalat (Whewellite/Weddellite) içerir.',
            'Bruşit taşları alkali idrarda hızla büyür ve ESWL kırılma direnci en yüksek taştır.',
            'Strüvit taşları sadece üreaz pozitif bakteriyel enfeksiyon varlığında oluşabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity'], matched_questions_dict['q_struvite_urease']],
        'aiPromptSuggestions': [
            'Whewellite ile Weddellite arasındaki klinik farklar nelerdir?',
            'Bruşit taşı neden ESWL ile kırılamaz?'
        ]
    },

    # Slide 4
    {
        'slideNumber': 4,
        'title': 'Radyolojik Görüntüleme & Radyoopasite Sınıflaması',
        'subtitle': 'DÜSG radyoopasitesi, radyolüsen taşlar ve Taş Protokolü Kontrassız BT',
        'badge': 'Radyoloji & Tanı',
        'badgeColor': 'indigo',
        'synthesisNarrative': 'Taşların direkt üriner sistem grafisindeki (DÜSG) görünürlüğü, içerdikleri elementlerin atom numarasına ve kalsiyum yoğunluğuna bağlıdır. Kalsiyum atom numarası yüksek (Z=20) olduğu için **Kalsiyum Oksalat ve Kalsiyum Fosfat taşları belirgin şekilde RADYOOPAK** izlenir. Strüvit ve Sistin taşları ise kükürt ve magnezyum içerikleri nedeniyle **zayıf radyoopak (buzlu cam görünümü)** olarak seçilir. Buna karşılık **Ürik asit, Ksantin ve İndinavir (HIV ilacı) taşları tamamen RADYOLÜSENTTİR**; DÜSG röntgeninde asla görünmezler. Güncel üroloji kılavuzlarında taş tanısında altın standart, intravenöz kontrast gerektirmeyen **Kontrassız Düşük Doz Helikal BT (Taş BT)**\'dir.',
        'flashcards': [
            {
                'id': 'uro-fc-04-01',
                'category': 'Radyoopasite',
                'front': 'Direkt grafide (DÜSG) tamamen radyolüsen (görünmeyen) temel taşlar hangileridir?',
                'hint': 'Röntgende seçilemeyen 3 ana organik bileşen.',
                'back': '**Ürik Asit**, **Ksantin**, **2,8-Dihidroksiadenin** ve **İndinavir (ilaç)** taşları. Bu taşlar DÜSG\'de görünmez; tanı Kontrassız BT veya USG ile konur.'
            },
            {
                'id': 'uro-fc-04-02',
                'category': 'Altın Standart',
                'front': 'Şüpheli nefrolitiyazis ve üreteral kolik tablosunda güncel altın standart görüntüleme yöntemi nedir?',
                'hint': 'Kontrastsız, hızlı ve 1 mm kesitli tomografi.',
                'back': '**Kontrassız Düşük Doz Helikal Bilgisayarlı Tomografi (Taş BT)**. Duyarlılık ve özgüllüğü >%98\'dir. İndinavir hariç tüm radyolüsen taşları (ürik asit dahil) Hounsfield Unit (HU) dansitesiyle net gösterir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Radyoopak Taşlar (DÜSG\'de Net Beyaz)',
                    'desc': 'Kalsiyum oksalat monohidrat/dihidrat, Kalsiyum fosfatlar (Apatit, Bruşit).',
                    'isKey': True
                },
                {
                    'title': 'Zayıf Radyoopak Taşlar (Buzlu Cam)',
                    'desc': 'Magnezyum amonyum fosfat (Strüvit), Sistin.',
                    'isKey': True
                },
                {
                    'title': 'Radyolüsen Taşlar (Röntgende Görünmez)',
                    'desc': 'Ürik asit, Amonyum ürat, Ksantin, 2,8-Dihidroksiadenin, İndinavir taşları.',
                    'isKey': True
                },
                {
                    'title': 'İndinavir İstisnası',
                    'desc': 'İndinavir proteaz inhibitörü taşları kontrassız BT\'de dahi böbrek parankimiyle izodens olup görülemeyebilir; dolma defektiyle tanınır.'
                }
            ],
            'table': {
                'title': 'Üriner Taşların X-Işını (DÜSG) Radyoopasite Özellikleri',
                'headers': ['Radyoopak (Opak)', 'Zayıf Radyoopak', 'Radyolüsen (Lüsent)'],
                'rows': [
                    ['CaOx Monohidrat (Whewellite)', 'Strüvit (Mg-Amonyum-Fosfat)', 'Ürik Asit (Uricite)'],
                    ['CaOx Dihidrat (Weddellite)', 'Apatit (bazı formlar)', 'Amonyum Ürat'],
                    ['Kalsiyum Fosfat (Bruşit)', 'Sistin (kükürt içerir)', 'Ksantin'],
                    ['Kalsiyum Karbonat', '—', '2,8-Dihidroksiadenin'],
                    ['—', '—', 'İndinavir & Triamteren (İlaç)']
                ]
            }
        },
        'spotPearls': [
            'DÜSG\'de görünmeyen radyolüsen taşların başında ürik asit gelir; ancak BT\'de 300-500 HU dansiteyle rahatça seçilir.',
            'Sistin taşları kükürt (disülfit) bağı içerdiğinden DÜSG\'de hafif zayıf opaktır (mumsu görünüm).',
            'Kontrassız Taş BT, taşın tam boyutunu, üreter duvar kalınlaşmasını ve perinefritik stranding\'i gösteren altın standarttır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Hangi taşlar DÜSG\'de görülmez?',
            'İndinavir taşının radyolojik özellikleri nelerdir?'
        ]
    },

    # Slide 5
    {
        'slideNumber': 5,
        'title': 'Taş Oluşumunun Fizyokimyası: Süpersatürasyon (Aşırı Doygunluk)',
        'subtitle': 'Çözünürlük çarpımı (Ksp), Formasyon çarpımı (Kfp) ve Metastabil bölge dinamikleri',
        'badge': 'Fizyokimya & Termodinamik',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Üriner taş oluşumunun termodinamik ön koşulu **Üriner Süpersatürasyon (Aşırı Doygunluk - SS)** halidir. Çözeltideki iyonların aktivite ürünü (AP) ile termodinamik çözünürlük çarpımı (Ksp) arasındaki denge idrarın doygunluk durumunu belirler. İdrarda üç ana faz tanımlanır: **1) Doymamış Bölge (SS < 1)**: Kristaller çözünür, taş oluşamaz. **2) Metastabil (Yarı Kararlı) Bölge (1 < SS < ULM)**: İdrar doygundur ancak kendiliğinden de novo kristal oluşamaz. Fakat önceden var olan yabancı bir nidus üzerine heterojen çekirdeklenme gerçekleşebilir. **3) Kararsız (Unstabil) Bölge (SS > ULM)**: Metastabilitenin üst sınırı (ULM - Upper Limit of Metastability) aşılmıştır; spontan, de novo, homojen kristal çekirdeklenmesi kaçınılmazdır.',
        'flashcards': [
            {
                'id': 'uro-fc-05-01',
                'category': 'Termodinamik',
                'front': 'İdrar metastabil (yarı kararlı) bölgedeyken (1 < SS < ULM) taş oluşumu nasıl gerçekleşebilir?',
                'hint': 'De novo kristal oluşmaz, önceden var olan yüzey gerekir.',
                'back': 'Yalnızca **Heterojen Çekirdeklenme (Nükleasyon)** yoluyla. İdrarda mevcut olan bir nidus (epitel kalıntısı, hücre debritisi veya ürik asit kristali) üzerine kalsiyum oksalat kristalleri çökerek büyür.'
            },
            {
                'id': 'uro-fc-05-02',
                'category': 'Fizyokimya',
                'front': 'Üriner süpersatürasyon metastabilitenin üst sınırını (ULM) aştığında (SS > ULM) ne tür nükleasyon gerçekleşir?',
                'hint': 'Kendiliğinden, harici çekirdeğe ihtiyaç duymadan başlayan süreç.',
                'back': '**Homojen Çekirdeklenme (De novo nükleasyon)**. İdrar kararsız (unstabil) hale gelir ve hiçbir yabancı yüzeye gerek kalmadan çözünmüş iyonlar bir araya gelerek spontan kristal kafesleri oluşturur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Doymamış İdrar (SS < 1)',
                    'desc': 'Çözelti altı durum. Mevcut kristaller çözünür; taş oluşumu imkansızdır.',
                    'isKey': True
                },
                {
                    'title': 'Metastabil Bölge (1 < SS < ULM)',
                    'desc': 'Kristal çözünmez, de novo oluşmaz; ancak heterojen nükleasyon ve epitaksi ile büyüme olur.',
                    'isKey': True
                },
                {
                    'title': 'Kararsız / Aşırı Doygun Bölge (SS > ULM)',
                    'desc': 'Kendiliğinden (homojen) de novo kristalleşme ve hızlı presipitasyon başlar.',
                    'isKey': True
                }
            ],
            'formulaBox': {
                'title': 'Süpersatürasyon Oranı Formülü',
                'formula': 'SS = AP / Ksp  (AP: İyonik Aktivite Çarpımı, Ksp: Termodinamik Çözünürlük Çarpımı)',
                'explanation': 'SS > 1 ise çözelti doygundur. ULM (Formasyon Çarpımı - Kfp) aşıldığında homojen kristal çökmesi tetiklenir.'
            }
        },
        'spotPearls': [
            'Sağlıklı bireylerin idrarı da gün içinde sıklıkla metastabil bölgede bulunur; ancak inhibitörler sayesinde kristal kümelenmesi engellenir.',
            'Taş oluşumunu önlemenin en temel yolu bol sıvı tüketimiyle iyon konsantrasyonunu düşürerek idrarı doymamış bölgeye (SS < 1) çekmektir.',
            'Metastabilite üst sınırı (ULM), idrardaki inhibitörlerin varlığına göre yukarı veya aşağı kayabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Metastabil bölge ile kararsız bölge arasındaki fark nedir?',
            'Üriner süpersatürasyon nasıl ölçülür?'
        ]
    },

    # Slide 6
    {
        'slideNumber': 6,
        'title': 'Çekirdeklenme (Nükleasyon), Kristal Büyümesi ve Epitaksi',
        'subtitle': 'Homojen vs Heterojen çekirdeklenme ve farklı kristal kafesleri üzerinde büyüme',
        'badge': 'Kristalizasyon Mekanizması',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Kristalleşmenin ilk kritik adımı **Nükleasyon (Çekirdeklenme)** adımıdır. Termodinamik olarak kararsız idrarda iyonların serbest enerjisi kritik eşiği aştığında nükleus adı verilen minik kristal çekirdekleri doğar. Nükleasyon iki şekilde gerçekleşir: Saf çözeltideki **Homojen Nükleasyon** (yüksek enerji gerektirir) ve yabancı bir yüzey üzerinde gerçekleşen **Heterojen Nükleasyon** (çok daha düşük süpersatürasyonda tetiklenir). Klinik olarak en çarpıcı heterojen nükleasyon modeli **Epitaksi**dir. Epitaksi, benzer kristal kafes aralıklarına ve moleküler geometriye sahip farklı bir kristal yüzeyi üzerinde yeni bir kristal türünün büyümesidir. Bunun klasik örneği, ürik asit kristali nidusu üzerinde kalsiyum oksalat kristallerinin büyümesidir.',
        'flashcards': [
            {
                'id': 'uro-fc-06-01',
                'category': 'Epitaksi',
                'front': 'Epitaksi nedir ve nefrolitiyazisteki en tipik klinik örneği hangisidir?',
                'hint': 'Benzer kristal kafes yapısına sahip farklı kristal üzerinde büyüme.',
                'back': '**Epitaksi**, bir kristal türünün, kristal kafes parametreleri benzer olan farklı bir kristal yüzeyinde çekirdeklenip büyümesidir. En tipik örneği: **Ürik asit kristali nidusu üzerinde kalsiyum oksalat taşının büyümesi**dir.'
            },
            {
                'id': 'uro-fc-06-02',
                'category': 'Nükleasyon',
                'front': 'Heterojen çekirdeklenme neden homojen çekirdeklenmeden çok daha sık gerçekleşir?',
                'hint': 'Yüzey enerjisi bariyeri.',
                'back': 'Çünkü heterojen çekirdeklenmede yabancı yüzey (hücre artığı, matris, başka bir kristal) serbest enerji bariyerini dramatik şekilde düşürür. Böylece idrar aşırı kararsız hale gelmeden, daha düşük metastabil süpersatürasyonda bile kristalleşme başlar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Nükleasyon (İlk Adım)',
                    'desc': 'Çözünmüş iyonların bir araya gelerek stabil bir kristal embriyosu (nidus) oluşturması.',
                    'isKey': True
                },
                {
                    'title': 'Homojen vs Heterojen',
                    'desc': 'Homojen nükleasyon aşırı yüksek SS gerektirir; biyolojik sistemlerde taşlar neredeyse daima heterojen nükleasyonla başlar.',
                    'isKey': True
                },
                {
                    'title': 'Epitaksiyel Büyüme',
                    'desc': 'Kalsiyum oksalat taşlarının önemli bir kısmı mikroskopik ürik asit veya apatit çekirdekleri üzerinde epitaksiyel olarak büyür.'
                }
            ],
            'table': {
                'title': 'Homojen vs Heterojen Çekirdeklenme Karşılaştırması',
                'headers': ['Özellik', 'Homojen Çekirdeklenme', 'Heterojen Çekirdeklenme (Epitaksi Dahil)'],
                'rows': [
                    ['Gereken İdrar Durumu', 'Kararsız / Aşırı Doygun (SS > ULM)', 'Metastabil (1 < SS < ULM)'],
                    ['Enerji Bariyeri', 'Çok yüksek serbest aktivasyon enerjisi', 'Düşük enerji (yabancı yüzey enerjiyi düşürür)'],
                    ['Çekirdek Yüzeyi', 'Yabancı yüzey yok, saf iyon kümesi', 'Hücre debritisi, Randall plağı, ürik asit'],
                    ['Biyolojik Sıklık', 'Laboratuvar ortamında sık, vücutta nadir', 'Klinik taş hastalarında ana mekanizma']
                ]
            }
        },
        'spotPearls': [
            'Hiperürikozürili hastalarda ürik asit taşı yerine kalsiyum oksalat taşı gelişmesi epitaksi mekanizmasıyla açıklanır.',
            'Kristal büyümesi, nükleus oluştuktan sonra çözeltideki iyonların kristal yüzeyine eklenmesi sürecidir.',
            'Tübül sıvısının geçiş süresi (birkaç dakika) tek başına kristal büyümesiyle lümeni tıkamaya yetmez; agregasyon ve adhezyon şarttır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Epitaksi ile heterojen nükleasyon arasındaki ilişki nedir?',
            'Ürik asit kristalleri kalsiyum oksalat taşını nasıl başlatır?'
        ]
    },

    # Slide 7
    {
        'slideNumber': 7,
        'title': 'Kristal Agregasyonu ve Üriner Retansiyon Hipotezleri',
        'subtitle': 'Sabit partikül vs Serbest partikül hipotezi ve toplayıcı kanallarda staz',
        'badge': 'Kristal Biyofiziği',
        'badgeColor': 'purple',
        'synthesisNarrative': 'Tek başına bir kristalin tübül boyunca büyümesi, nefron lümeninden (ortalama 20-50 mikron) daha büyük bir çapa ulaşması için gereken süreden (saatler/günler) çok daha hızlıdır; çünkü idrar tübülleri birkaç dakika içinde terk eder. Taşın klinik kalkülüse dönüşebilmesi için iki zorunlu aşama gerekir: **Kristal Agregasyonu** ve **Kristal Retansiyonu (Tutulması)**. Agregasyon, yüzen çok sayıda minik kristalin birbirine yapışarak büyük kümeler oluşturmasıdır. Retansiyon için iki hipotez yarışır: **1) Serbest Partikül Hipotezi**: Kristal agregatları o kadar büyür ki toplayıcı kanalların ve Bellini duktusunun lümenini mekanik olarak tıkar. **2) Sabit Partikül Hipotezi**: Kristaller hasarlı renal tübül epitel hücrelerine adhezyon molekülleriyle yapışır ve idrar akımıyla atılamayarak yerinde büyür.',
        'flashcards': [
            {
                'id': 'uro-fc-07-01',
                'category': 'Fizyopatoloji',
                'front': 'Sabit Partikül Hipotezi ile Serbest Partikül Hipotezi arasındaki temel fark nedir?',
                'hint': 'Adhezyon (yapışma) vs Mekanik boyut takılması.',
                'back': '**Sabit Partikül Hipotezi**, kristallerin hasarlı tübül epitel yüzeyine spesifik olarak yapışarak (adhezyon) sabitlendiğini savunur. **Serbest Partikül Hipotezi** ise kristallerin lümende toplanıp (agregasyon) tübül çapından daha büyük kitle oluşturarak mekanik olarak takıldığını savunur.'
            },
            {
                'id': 'uro-fc-07-02',
                'category': 'Kristal Dinamiği',
                'front': 'Neden tek başına kristal büyümesi taş oluşumu için yetersizdir ve agregasyon gereklidir?',
                'hint': 'İdrar akış hızı ile kristal büyüme süresi arasındaki tezat.',
                'back': 'Çünkü glomerülden papilla ucuna idrar geçiş süresi yalnızca **5-10 dakika**dır. Bu sürede bir kristalin tek başına lümeni tıkayacak boyuta (200-500 mikron) büyümesi imkansızdır. Birçok kristalin saniyeler içinde birbirine yapışması (agregasyon) şarttır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Kristal Agregasyonu',
                    'desc': 'Taş boyutunun katlanarak artmasını sağlayan en kritik fizyokimyasal basamaktır.',
                    'isKey': True
                },
                {
                    'title': 'Sabit Partikül (Adhezyon)',
                    'desc': 'Epitel hasarı olan tübüllerde kristal tutunması dramatik artar (Randall plakları ve tübüler nekroz zemininde).',
                    'isKey': True
                },
                {
                    'title': 'Anatomik Staz',
                    'desc': 'UP darlık, kaliks divertikülü ve at nalı böbrek gibi durumlarda serbest parçacıkların atılamayıp çökmesi kolaylaşır.'
                }
            ],
            'infographic': {
                'type': 'process',
                'items': [
                    {'label': '1. Süpersatürasyon', 'value': 'SS > ULM', 'detail': 'İyon doygunluğu aşılır', 'color': 'sky'},
                    {'label': '2. Nükleasyon', 'value': 'Çekirdek', 'detail': 'Mikrokristal kafesi doğar', 'color': 'amber'},
                    {'label': '3. Agregasyon', 'value': 'Kümelenme', 'detail': 'Kristaller birbirine yapışır', 'color': 'rose'},
                    {'label': '4. Retansiyon', 'value': 'Sabitlenme', 'detail': 'Epitele yapışma veya lümen tıkacı', 'color': 'emerald'}
                ]
            }
        },
        'spotPearls': [
            'Sağlıklı bireylerde kristalüri (idrarda kristal varlığı) sık görülür; ancak agregasyon ve epitele tutunma olmadığı için taşlaşmadan atılır.',
            'Kristaller sağlıklı epitele tutunamaz; tübül hücresinde sitotoksik hasar veya bazal membran çıplaklaşması gerekir.',
            'İdrardaki doğal inhibitörler en güçlü etkilerini kristal agregasyonunu bloke ederek gösterirler.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Sabit partikül hipotezi günümüzde neden daha çok kabul görüyor?',
            'Kristal agregasyonu nasıl engellenir?'
        ]
    },

    # Slide 8
    {
        'slideNumber': 8,
        'title': 'Endojen Kristalizasyon İnhibitörleri I: Sitrat ve İnorganik İyonlar',
        'subtitle': 'Sitratın 4 aşamalı koruyucu mekanizması, Pirofosfat ve Magnezyum',
        'badge': 'İnhibitörler & Koruyucu Faktörler',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Normal insan idrarı günün belirli saatlerinde süpersatüre olmasına rağmen çoğu insanda taş oluşmamasının ana sebebi güçlü **Kristalizasyon İnhibitörleri**dir. Bu inhibitörlerin klinik olarak en önemlisi **SİTRAT**tır. Sitrat, taş oluşumunu **4 farklı yol** ile doğrudan engeller: **1) İyonize kalsiyum ile çözünür kompleks oluşturur** ve serbest kalsiyum miktarını azaltır. **2) Kalsiyum oksalatın kendiliğinden nükleasyonunu doğrudan inhibe eder**. **3) Kristal agregasyonunu ve aglomerasyonunu güçlü şekilde bloke eder**. **4) Monosodyum ürat kristalleri üzerinde CaOx\'ın heterojen çekirdeklenmesini (epitaksiyi) önler**. Diğer inorganik koruyucular arasında pirofosfat ve kalsiyumla yarışan magnezyum yer alır.',
        'flashcards': [
            {
                'id': 'uro-fc-08-01',
                'category': 'Sitrat Mekanizması',
                'front': 'İdrar sitratının kalsiyum taşlarını önlemedeki 4 temel mekanizması nelerdir?',
                'hint': 'Serbest Ca bağlama, nükleasyon inhibisyonu, agregasyon blokajı ve epitaksi önleme.',
                'back': '1) Serbest iyonize Ca2+ ile çözünür Ca-sitrat kompleksi oluşturarak Ca\'u bağlar.\n2) CaOx spontan çekirdeklenmesini doğrudan inhibe eder.\n3) Kristal agregasyonunu (kümelenmesini) önler.\n4) Monosodyum ürat üzerinde CaOx heterojen nükleasyonunu (epitaksiyi) bloke eder.'
            },
            {
                'id': 'uro-fc-08-02',
                'category': 'İnorganik İnhibitörler',
                'front': 'Magnezyum ve Pirofosfat iyonları taş oluşumunu nasıl engeller?',
                'hint': 'Oksalat ile yarışma ve kristal yüzeyine bağlanma.',
                'back': '**Magnezyum**, idrarda oksalat ile çözünür magnezyum-oksalat kompleksi oluşturarak kalsiyumun oksalatla bağlanmasını azaltır. **Pirofosfat** ise kalsiyum fosfat ve kalsiyum oksalat kristal yüzeylerine bağlanarak kristal büyümesini bloke eder.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Sitrat (Doğal Taş Kalkanı)',
                    'desc': 'Normal idrar atılımı >320 mg/gün olmalıdır; hipositratüri en sık metabolik risklerden biridir.',
                    'isKey': True
                },
                {
                    'title': 'Magnezyum Etkisi',
                    'desc': 'Oksalat ile yarışarak kalsiyum oksalat süpersatürasyonunu düşürür.',
                    'isKey': True
                },
                {
                    'title': 'Pirofosfat Etkisi',
                    'desc': 'Kristal yüzeyindeki büyüme basamaklarına adsorbe olarak kristal boyunun uzamasını engeller.'
                }
            ],
            'table': {
                'title': 'İdrardaki Doğal Taş İnhibitörleri ve Etki Hedefleri',
                'headers': ['İnhibitör Madde', 'Moleküler Yapı', 'Etki Ettiği Taş Tipi', 'Temel Etki Mekanizması'],
                'rows': [
                    ['Sitrat', 'Küçük Organik Anyon', 'Kalsiyum Oksalat & Fosfat', 'Ca bağlama, nükleasyon ve agregasyon blokajı'],
                    ['Magnezyum', 'İnorganik Katyon', 'Kalsiyum Oksalat', 'Oksalat bağlama, CaOx süpersatürasyonunu düşürme'],
                    ['Pirofosfat', 'İnorganik Anyon', 'Kalsiyum Fosfat & Oksalat', 'Kristal yüzeyine tutunup büyümeyi durdurma'],
                    ['Çinko', 'Eser Element', 'Kalsiyum Fosfat', 'Apatit kristal kafesini bozma']
                ]
            }
        },
        'spotPearls': [
            'Hipositratüri (<320 mg/gün), kalsiyum taşı oluşturan hastaların %20-60\'ında saptanan kritik bir bozukluktur.',
            'Sitrat tedavisi (potasyum sitrat), hem hipositratürik kalsiyum taşlarında hem de asidik ürik asit taşlarında birincil medikal ajandır.',
            'Limonata ve narenciye tüketimi doğal sitrat kaynağı olarak idrar sitrat düzeyini artırır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Sitratın 4 etki mekanizması sınavda nasıl sorulur?',
            'Hipositratüri neden kalsiyum taşı riskini artırır?'
        ]
    },

    # Slide 9
    {
        'slideNumber': 9,
        'title': 'Endojen Kristalizasyon İnhibitörleri II: Makromoleküller',
        'subtitle': 'Nefrokalsin, Osteopontin, GAGs ve Tamm-Horsfall Proteini (Uromodulin) ikilemi',
        'badge': 'Biyomoleküller & İnhibitörler',
        'badgeColor': 'teal',
        'synthesisNarrative': 'İdrardaki inorganik inhibitörlerin yanı sıra böbrek tübül epiteli tarafından sentezlenen büyük makromoleküller kristalleşme sürecini yönlendirir. **Nefrokalsin**, asidik bir glikoprotein olup kalsiyum oksalat agregasyonunun en güçlü inhibitörlerindendir (taş oluşturanlarda yapısı kusurludur). **Osteopontin**, kristallerin tübül epitel hücrelerine adhezyonunu ve büyümesini bloke eder. **Tamm-Horsfall Proteini (Uromodulin)** ise tıbbın en ilginç ikilemlerinden birini sergiler: **Alkali idrarda güçlü bir kalsiyum oksalat agregasyon inhibitörüyken; asidik idrarda, yüksek iyonik güçte veya kalsiyum fazlalığında polimerize jel kıvamına geçerek kristal agregasyonunu DESTEKLEYEN (promotör) bir ajana dönüşür**.',
        'flashcards': [
            {
                'id': 'uro-fc-09-01',
                'category': 'Dual Etki',
                'front': 'Tamm-Horsfall Proteini (Uromodulin) hangi koşullarda taş inhibitörü, hangi koşullarda taş promotörü (destekleyicisi) gibi davranır?',
                'hint': 'İdrar pH\'sı ve polimerizasyon durumu.',
                'back': '**Alkali idrarda** monomerik formdadır ve güçlü bir CaOx kristal agregasyon inhibitörüdür.\n**Asidik idrarda (düşük pH)**, yüksek iyonik güçte veya yüksek Ca derişiminde ise polimerize olarak jel kıvamına geçer ve kristal agregasyonunu DESTEKLEYEN (promotör) bir rol üstlenir.'
            },
            {
                'id': 'uro-fc-09-02',
                'category': 'Glikoproteinler',
                'front': 'Nefrokalsin glikoproteininin taş hastalarındaki patolojik özelliği nedir?',
                'hint': 'Gama-karboksiglutamik asit içeriği ve moleküler yapı.',
                'back': 'Taş oluşturmayan sağlıklı bireylerde nefrokalsin CaOx agregasyonunu güçlü şekilde inhibe eder. Ancak taş hastalarında sentezlenen nefrokalsinde **gama-karboksiglutamik asit içeriği eksiktir**; bu anormal form inhibitör özelliğini kaybeder ve kristal agregasyonunu önleyemez.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Nefrokalsin',
                    'desc': '4 izoformu bulunan asidik glikoprotein; normal formu CaOx kristal agregasyonunu güçlü engeller.',
                    'isKey': True
                },
                {
                    'title': 'Osteopontin (Uropontin)',
                    'desc': 'Kristal nükleasyonunu, büyümesini ve epitel hücresine yapışmasını (adhezyonunu) doğrudan bloke eder.',
                    'isKey': True
                },
                {
                    'title': 'Tamm-Horsfall (Uromodulin) İkilemi',
                    'desc': 'Alkali pH\'da inhibitör, asidik pH\'da polimerize jel halinde kristal toplayıcı promotör.',
                    'isKey': True
                },
                {
                    'title': 'Glikozaminoglikanlar (GAGs)',
                    'desc': 'Heparan sülfat, kondroitin sülfat ve hyaluronan kristal yüzeyini kaplayarak agregasyonu engeller.'
                }
            ],
            'table': {
                'title': 'İdrar Makromoleküler İnhibitörleri ve Fonksiyonları',
                'headers': ['Makromolekül', 'Sentez Yeri', 'Normal Fonksiyonu', 'Kusurundaki Klinik Durum'],
                'rows': [
                    ['Nefrokalsin', 'Proksimal tübül & Henle çıkan kol', 'CaOx agregasyonunu durdurma', 'Kusurlu yapı -> Agregasyon kontrolsüz artar'],
                    ['Osteopontin', 'Distal tübül & toplayıcı kanal', 'Epitel adhezyonunu ve nükleasyonu önleme', 'Eksikliğinde kristaller epitele yapışır'],
                    ['Tamm-Horsfall Proteini', 'Henle kulpu kalın çıkan kol', 'Alkali idrarda agregasyonu önleme', 'Asidik idrarda polimerize olup agregasyonu artırır'],
                    ['Üriner Protrombin Fragman 1', 'Renal tübül epiteli', 'CaOx monohidrat nükleasyonunu inhibe etme', 'İdrar atılımında azalma']
                ]
            }
        },
        'spotPearls': [
            'Tamm-Horsfall proteini insan idrarında en bol bulunan proteindir (günde 30-50 mg).',
            'Asidik idrar, sadece ürik asit kristalleşmesini kolaylaştırmaz; uromodulini polimerize ederek CaOx agregasyonunu da tetikler.',
            'Kronik tübüler hasarı olan böbreklerde osteopontin ve nefrokalsin üretimi düşer ve taş nüksü hızlanır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Tamm-Horsfall proteininin pH\'ya göre çift yönlü etkisi nedir?',
            'Nefrokalsin ve osteopontin taş oluşumunu nasıl engeller?'
        ]
    },

    # Slide 10
    {
        'slideNumber': 10,
        'title': 'Taş Matrisi ve Kalkülüs Oluşum Teorilerine Genel Bakış',
        'subtitle': 'Organik iskelet, enfeksiyon taşlarında matris artışı ve 5 temel patogenetik teori',
        'badge': 'Matris & Patogenez',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Böbrek taşları sadece mineral kristallerinden ibaret değildir; kristal ağının arasına gömülü organik bir **Taş Matrisi** içerir. Standart kalsiyum taşlarında matris taş ağırlığının yaklaşık **%2-3\'ünü** oluşturur ve kristaller için yapı iskelesi (nidus) görevi görür. Ancak kronik üreaz pozitif enfeksiyon zemininde gelişen taşlarda organik matris oranı **%65\'e kadar fırlar** (buna yumuşak hamurumsu "matris taşı" denir). Tıp tarihinde taş oluşumunun anatomik ve hücresel mekanizmasını açıklamak üzere 5 ana teori öne sürülmüştür: **1) Oksalat kaynaklı tübüler hasar teorisi**, **2) Randall plak teorisi**, **3) Vasküler hipotez**, **4) Nanobakteriler hipotezi**, **5) Anatomik staz ve inhibitör yetersizliği**.',
        'flashcards': [
            {
                'id': 'uro-fc-10-01',
                'category': 'Taş Matrisi',
                'front': 'Tipik bir kalsiyum taşında organik matris oranı ne kadardır, enfeksiyon taşlarında bu oran kaça kadar çıkabilir?',
                'hint': '%3 ile %65 arasındaki devasa fark.',
                'back': 'Tipik kalsiyum taşlarında matris taş ağırlığının yaklaşık **%2-3\'ünü** oluşturur. Kronik üriner enfeksiyon zemininde gelişen taşlarda ise matris oranı **%65\'e kadar** yükselebilir (radyolüsen matris taşları).'
            },
            {
                'id': 'uro-fc-10-02',
                'category': 'Teoriler',
                'front': 'Ürolitiyazis patogenezini açıklayan 5 ana kalkülüs oluşum teorisi hangileridir?',
                'hint': 'Hücresel hasar, papiller plak, damarsal akım, enfeksiyon ve staz.',
                'back': '1) Randall Plak Teorisi (en kabul gören)\n2) Oksalat Kaynaklı Tübüler Hasar Teorisi\n3) Vasküler Hipotez (Vasa recta endotel hasarı)\n4) Nanobakteriler Teorisi (tartışmalı)\n5) İnhibitör Yetersizliği ve Üriner Staz Hipotezi'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Organik Taş Matrisi',
                    'desc': 'Proteinler (%64), hekzozlar (%9), hekzozaminler (%5) ve sudan oluşur; kristallerin adsorbe olduğu nidustur.',
                    'isKey': True
                },
                {
                    'title': 'Matris Taşları (Matrix Calculi)',
                    'desc': 'Proteus enfeksiyonlu kadınlarda sık görülen, jelatinöz/balmumu kıvamında, DÜSG\'de tamamen radyolüsen taşlar.',
                    'isKey': True
                },
                {
                    'title': 'Patogenetik Hipotezlerin Birleşimi',
                    'desc': 'Kalsiyum oksalat taşlarının çoğunda Randall plağı başlangıç noktası iken, tübüler hasar süreci hızlandırır.'
                }
            ],
            'table': {
                'title': 'Kalkülüs Oluşum Teorilerinin Karşılaştırmalı Özeti',
                'headers': ['Teori Adı', 'Öne Sürülen Mekanizma', 'Başlangıç Alanı', 'Geçerlilik Durumu'],
                'rows': [
                    ['Randall Plak Teorisi', 'Henle bazal membranında apatit birikimi -> papiller erozyon', 'Renal papilla ucu', 'Günümüzde en kanıtlanmış teori'],
                    ['Oksalat Tübüler Hasar', 'Hiperoksalüri -> ROS üretimi -> epitel hasarı ve kristal yapışması', 'İç medüller toplayıcı kanal', 'Hücresel düzeyde güçlü kanıtlar'],
                    ['Vasküler Hipotez', 'Vasa recta türbülansı -> endotel hasarı ve kalsifikasyon', 'Medüller vasküler yatak', 'Destekleyen bulgular mevcut'],
                    ['Nanobakteriler', 'Kalsifiye nanopartiküllerin apatit çökeltmesi başlatması', 'İntratübüler / interstisyel', 'Halen tartışmalı ve şüpheli'],
                    ['Anatomik Staz', 'İdrar akım yavaşlığı -> kristallerin yıkanamayıp çökmesi', 'UPB, kaliks divertikülü', 'Sekonder kolaylaştırıcı faktör']
                ]
            }
        },
        'spotPearls': [
            'Matris taşları, mineral içeriği düşük (<%35) olduğu için direkt grafide (DÜSG) görünmez ve BT\'de yumuşak doku kitlesiyle karışabilir.',
            'Kristaller ve matris proteini birbirini karşılıklı olarak uyararak taşın katman katman (soğan zarı gibi) büyümesini sağlar.',
            'Enfeksiyon zemininde matris artışı, antibiyotiklerin taşın içine penetre olmasını engelleyerek relapslara yol açar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_struvite_urease']],
        'aiPromptSuggestions': [
            'Matris taşı nedir ve nasıl tedavi edilir?',
            'Kalkülüs oluşum teorileri tıp sınavlarında nasıl sorulur?'
        ]
    },

    # Slide 11
    {
        'slideNumber': 11,
        'title': 'Randall Plak Teorisi: İdiopatik CaOx Taşlarının Kökeni',
        'subtitle': 'Alexander Randall hipotezi, Henle kulpu bazal membranı ve papiller erozyon',
        'badge': 'Altın Standart Teori',
        'badgeColor': 'rose',
        'synthesisNarrative': '1937\'de Alexander Randall tarafından tanımlanan ve modern endoürolojik biyopsilerle doğrulanan **Randall Plak Teorisi**, idiopatik kalsiyum oksalat taşlarının patogenezini kusursuz şekilde açıklar. Süreç böbrek tübül lümeninde değil, **İnce Henle Kulpunun bazal membranında kalsiyum fosfat (karbonat apatit)** mikrokalsifikasyonları olarak başlar. Bu kalsiyum apatit kristalleri medüller interstisyum boyunca ilerleyerek **renal papilla ucunun subepitelyal alanına** göç eder. Zamanla büyüyen plak, üzerindeki papiller ürotelyumu erode ederek çıplaklaştırır. İdrarla temas eden bu çıplak apatit yüzeyi, idrardaki kalsiyum oksalat kristalleri için mükemmel bir heterojen nidus görevi görür ve taş papilla ucunda asılı halde büyür.',
        'flashcards': [
            {
                'id': 'uro-fc-11-01',
                'category': 'Randall Teorisi',
                'front': 'Randall plakları ilk olarak hangi anatomik yapıda ve hangi mineral bileşeniyle başlar?',
                'hint': 'Tübül lümeni değil, bazal membran ve kalsiyum fosfat.',
                'back': 'İlk olarak **İnce Henle Kulpunun bazal membranında** başlar. İlk çöken mineral bileşeni kalsiyum oksalat DEĞİL, **Kalsiyum Fosfat (Karbonat Apatit)** tuzlarıdır.'
            },
            {
                'id': 'uro-fc-11-02',
                'category': 'Patogenez',
                'front': 'Subepitelyal kalsiyum apatit plağı kalsiyum oksalat taşına nasıl dönüşür?',
                'hint': 'Papiller ürotelyum erozyonu ve çıplak yüzey teması.',
                'back': 'İnterstisyel apatit birikintisi büyüyerek papilla ucundaki ürotelyumu aşındırır (erozyon). İdrara açılan çıplak apatit yüzeyine idrardaki kalsiyum oksalat kristalleri epitaksi yoluyla yapışır ve taş kalikse doğru büyür.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Henle Kulpu Bazal Membranı',
                    'desc': 'Apatit kristallerinin ilk biriktiği mikroskopik başlangıç odağıdır.',
                    'isKey': True
                },
                {
                    'title': 'İnterstisyel Yayılım',
                    'desc': 'Toplayıcı kanalların dışındaki medüller bağ dokusunda papilla ucuna doğru ilerler.',
                    'isKey': True
                },
                {
                    'title': 'Ürotelyal Erozyon',
                    'desc': 'Papilla epiteli yırtılarak apatit plağı idrar havuzuna maruz kalır.',
                    'isKey': True
                },
                {
                    'title': 'CaOx Çökmesi',
                    'desc': 'Apatit nidusu üzerinde idrardaki kalsiyum oksalat taşlaşarak klinik taşı oluşturur.'
                }
            ],
            'infographic': {
                'type': 'process',
                'items': [
                    {'label': '1. Henle Membranı', 'value': 'Apatit Çökmesi', 'detail': 'İnce kulp bazal membranında', 'color': 'sky'},
                    {'label': '2. İnterstisyel Göç', 'value': 'Plak Büyümesi', 'detail': 'Papillaya doğru ilerler', 'color': 'amber'},
                    {'label': '3. Ürotelyal Erozyon', 'value': 'Çıplak Nidus', 'detail': 'Epitel aşınır, idrara açılır', 'color': 'rose'},
                    {'label': '4. CaOx Büyümesi', 'value': 'Klinik Taş', 'detail': 'Sabitlenmiş taş papilla ucunda büyür', 'color': 'emerald'}
                ]
            }
        },
        'spotPearls': [
            'Randall plağı başlangıçta kalsiyum FOSFATtır; ancak üzerine büyüyen taş kalsiyum OKSALATtır (en klasik kurul sorusu!).',
            'Üreteroskopide (f-URS) taş çıkarıldıktan sonra papilla ucunda görülen beyaz/sarı lekeler Randall plaklarıdır.',
            'Hiperkalsiürili hastalarda papiller Randall plak alanı normokalsiürik bireylere göre 3-5 kat daha geniştir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Randall plak teorisi kurul sınavında nasıl çeldirici olarak sorulur?',
            'Randall plağında ilk çöken tuz kalsiyum oksalat mıdır kalsiyum fosfat mıdır?'
        ]
    },

    # Slide 12
    {
        'slideNumber': 12,
        'title': 'Oksalat Tübüler Hasarı ve Vasküler Hipotez',
        'subtitle': 'ROS kaynaklı mitokondriyal hasar, hücre nekrozu ve vasa recta türbülansı',
        'badge': 'Hücre Hasarı & Vasküler',
        'badgeColor': 'purple',
        'synthesisNarrative': 'Kalsiyum oksalat taşlarının gelişiminde Randall plağını tamamlayan en önemli hücresel mekanizma **Oksalat Kaynaklı Tübüler Hasar Teorisi**dir. Yüksek konsantrasyondaki serbest oksalat tübül hücresine girdiğinde mitokondriyal elektron transportunu bozar ve **Reaktif Oksijen Türleri (ROS)** açığa çıkar. Oluşan oksidatif stres, tübül hücre zarında lipit peroksidasyonuna ve hücre nekrozuna yol açar. Hasarlanan hücreler apikal yüzeylerinde kristal bağlayıcı molekülleri (hyaluronan, osteopontin, CD44) aşırı eksprese eder; CaOx kristalleri sağlıklı hücreye yapışamazken bu hasarlı alanlara mıknatıs gibi tutunur. **Vasküler Hipotez** ise papilla ucundaki vasa recta saç tokası kıvrımındaki türbülanslı akımın endotel hasarı ve kalsifikasyon başlatarak Randall plağına zemin hazırladığını öne sürer.',
        'flashcards': [
            {
                'id': 'uro-fc-12-01',
                'category': 'Oksidatif Stres',
                'front': 'Hiperoksalürinin renal tübül epitelinde başlattığı patolojik kaskad nasıldır?',
                'hint': 'ROS oluşumu, membran hasarı ve kristal adhezyonu.',
                'back': 'Aşırı oksalat -> Mitokondriyal hasar -> **Reaktif Oksijen Türleri (ROS)** üretimi -> Lipit peroksidasyonu ve tübül nekrozu -> Kristal bağlayıcı makromoleküllerin (CD44, hyaluronan) yüzeye çıkması -> CaOx kristallerinin epitele sabitlenmesi.'
            },
            {
                'id': 'uro-fc-12-02',
                'category': 'Vasküler Hipotez',
                'front': 'Vasküler hipoteze göre renal papillada kalsifikasyonu başlatan hemodinamik faktör nedir?',
                'hint': 'Vasa recta kıvrımındaki akım özellikleri.',
                'back': 'Renal papilla ucundaki **vasa recta damarlarının firkete (saç tokası) dönüşündeki türbülanslı kan akışı**. Bu türbülans endotel hasarını ve mikrovasküler kalsifikasyonu tetikler; ateroskleroz benzeri bir süreçle Bellini duktusuna komşu plaklar doğar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Oksalat Sitotoksisitesi',
                    'desc': 'Oksalat kalsiyumdan çok daha toksiktir; tübül epitelinde doğrudan nekroz ve apoptozu tetikler.',
                    'isKey': True
                },
                {
                    'title': 'Kristal Reseptörleri (CD44 / Hyaluronan)',
                    'desc': 'Sağlıklı hücre polaritesinde bu moleküller bazaldedir; hasarda apikale göç edip kristali bağlarlar.',
                    'isKey': True
                },
                {
                    'title': 'Vasküler ve Aterosklerotik Benzerlik',
                    'desc': 'Metabolik sendromlu ve hipertansif hastalarda vasa recta endotel disfonksiyonu taş riskini artırır.'
                }
            ],
            'table': {
                'title': 'Sağlıklı Tübül vs Hasarlı Tübül Epitelinde Kristal Davranışı',
                'headers': ['Parametre', 'Sağlıklı Renal Tübül', 'Oksalat Hasarlı Tübül'],
                'rows': [
                    ['Hücre Zarı Bütünlüğü', 'İntakt, sağlam fırçamsı kenar', 'Lipit peroksidasyonu, membran blebleri'],
                    ['Yüzey Yükü ve Glikokaliks', 'Negatif yüklü sağlam glikokaliks', 'Glikokaliks kaybı, çıplak bazal membran'],
                    ['Adhezyon Molekülleri (CD44, HA)', 'Apikalde eksprese edilmez', 'Apikal yüzeye yoğun şekilde transloke olur'],
                    ['Kristal Tutunması (Adhezyon)', 'Kristaller kayar ve idrarla atılır', 'Kristaller güçlü kovalent/iyonik bağlarla tutunur']
                ]
            }
        },
        'spotPearls': [
            'Kalsiyum oksalat kristalleri sağlıklı intakt tübül epitel hücrelerine bağlanamaz.',
            'Antioksidan ajanlar (E vitamini, N-asetilsistein) deneysel modellerde oksalat kaynaklı kristal tutunmasını azaltmaktadır.',
            'Kardiyovasküler hastalıklar ile taş hastalığının ortak paydası endotel disfonksiyonu ve oksidatif strestir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_randall_plaque']],
        'aiPromptSuggestions': [
            'Oksalat hasarlı tübüle kristaller nasıl yapışır?',
            'Vasküler hipotez ile Randall plakları nasıl örtüşür?'
        ]
    },

    # Slide 13
    {
        'slideNumber': 13,
        'title': 'Kalsiyum Taşları ve Hiperkalsiüri Patofizyolojisi',
        'subtitle': 'Diyet, Absorptif (Tip I, II), Renal ve Primer Hiperparatiroidi ayrımı & Sarkoidoz',
        'badge': 'Metabolik Bozukluklar',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Kalsiyum taşlı hastaların yaklaşık **%50\'sinde** saptanan en yaygın metabolik anormallik **Hiperkalsiüri**dir. Resmi ders notuna göre geleneksel olarak sınıflandırılır: **1) Absorptif Hiperkalsiüri**: Bağırsaktan artmış kalsiyum emilimi. Tip I (kalsiyum kısıtlı diyette dahi idrar Ca yüksek kalır), Tip II (diyet kalsiyumu kısıtlandığında idrar Ca normale döner). **2) Renal Hiperkalsiüri**: Proksimal ve distal renal tübüllerden kalsiyumun yeniden emiliminin bozulması (renal kaçak; sekonder olarak PTH yükselir). **3) Rezorptif Hiperkalsiüri**: En sık paratiroid adenomuna bağlı gelişen **Primer Hiperparatiroidizm**dir. Klinik tanının EN ANLAMLI adımı **Primer Hiperparatiroidiyi diğerlerinden ayırt etmektir** (çünkü hem serum Ca hem PTH birlikte yüksektir). Hiperkalsemi ve hiperkalsiürinin diğer önemli nedeni **Sarkoidoz**dur; sarkoidozda PTH baskılanır, 1,25-dihidroksi D3 artar ve akciğer grafisinde hiler adenopati saptanır.',
        'flashcards': [
            {
                'id': 'uro-fc-13-01',
                'category': 'Hiperkalsiüri Tipleri',
                'front': 'Absorptif Hiperkalsiüri Tip I ile Tip II arasındaki en kritik klinik ve tanısal fark nedir?',
                'hint': 'Düşük kalsiyumlu diyete verilen yanıt.',
                'back': '**Tip I Absorptif Hiperkalsiüri**: Diyet kalsiyumu kısıtlansa bile idrar kalsiyumu yüksek kalır (yanıtsız).\n**Tip II Absorptif Hiperkalsiüri**: Diyet kalsiyumu kısıtlandığında idrar kalsiyumu normale döner (diyete tam yanıt).'
            },
            {
                'id': 'uro-fc-13-02',
                'category': 'Ayırıcı Tanı',
                'front': 'Primer Hiperparatiroidizm ile Granülomatöz Hastalıklar (Sarkoidoz) serum Ca, PTH ve tanısal testlerle nasıl ayırt edilir?',
                'hint': 'Her ikisi de hiperkalsemi ve hiperkalsiüri yapar; ancak PTH davranışı farklıdır.',
                'back': '• **Primer Hiperparatiroidizm**: Serum Ca YÜKSEK, PTH YÜKSEKTİR (otonom adenom).\n• **Sarkoidoz**: Serum Ca YÜKSEK, ancak PTH BASKILANIR (↓). Tanıda göğüs röntgeninde **hiler adenopati** aranır ve kontrol edilen **1,25-dihidroksi D vitamini** yüksek bulunur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Tanının En Anlamlı Adımı',
                    'desc': 'Primer hiperparatiroidiyi (yüksek Ca + yüksek PTH) diğer benign hiperkalsiürilerden ayırt etmektir.',
                    'isKey': True
                },
                {
                    'title': 'Geleneksel Hiperkalsiüri Sınıflaması',
                    'desc': 'Absorptif (barsaktan aşırı emilim), Renal (tübüler geri emilim bozukluğu) ve Rezorptif (paratiroid adenomu).',
                    'isKey': True
                },
                {
                    'title': 'Sarkoidoz Ayrımı',
                    'desc': 'Hiperkalsemi + hiperkalsiüri vardır fakat PTH baskılıdır; artmış 1,25-(OH)2-D3 ve bilateral hiler LAP tipiktir.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 33: Hiperkalsiüri Tipleri Ayırıcı Tanı Tablosu',
                'headers': ['Hiperkalsiüri Tipi', 'Random İdrar Ca', 'Diyet Kısıtlanmış İdrar Ca', 'Serum Kalsiyumu', 'Serum Parathormon (PTH)'],
                'rows': [
                    ['Diyet Kaynaklı', '↑ Yüksek', 'Normal (N)', 'Normal (N)', 'Normal (N)'],
                    ['Absorptif Tip I', '↑ Yüksek', '↑ Yüksek', 'Normal (N)', 'Normal veya ↓ Baskılı'],
                    ['Absorptif Tip II', '↑ Yüksek', 'Normal (N)', 'Normal (N)', 'Normal veya ↓ Baskılı'],
                    ['Renal Kaçak', '↑ Yüksek', '↑ Yüksek', 'Normal (N)', '↑ Yüksek (Sekonder)'],
                    ['Primer Hiperparatiroidi', '↑ Yüksek', '↑ Yüksek', '↑ Yüksek (Hiperkalsemi)', '↑ Yüksek (Primer Otonom)']
                ]
            }
        },
        'spotPearls': [
            'Primer hiperparatiroidiyi diğer hiperkalsiüri türlerinden ayırt etmek, klinik tanının en anlamlı adımıdır.',
            'Sarkoidozda makrofaj kaynaklı 1-alfa hidroksilaz aktivitesi nedeniyle 1,25-dihidroksi D3 artar; hiperkalsemiye rağmen PTH baskılanır.',
            'Diyet kaynaklı hiperkalsiüride kalsiyum kısıtlandığında idrar kalsiyumu hızla normale geriler; serum Ca ve PTH baştan beri normaldir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Absorptif Tip I ve Tip II hiperkalsiüri diyet kısıtlamasına nasıl yanıt verir?',
            'Primer hiperparatiroidi ile sarkoidoz laboratuvar olarak nasıl ayrılır?'
        ]
    },

    # Slide 14
    {
        'slideNumber': 14,
        'title': 'Hiperoksalüri Patofizyolojisi: Diyet, Birincil ve Enterik Tipler',
        'subtitle': 'Oxalobacter formigenes, AGXT/GRHPR/HOGA genetik defektleri ve Ca-Mg sabunlaşması',
        'badge': 'Oksalat & Genetik',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre **Hiperoksalüri** 3 temel grupta incelenir: **1) Diyet İlişkili Hiperoksalüri**: Oksalattan zengin besinler (fındık, çikolata, ıspanak, patates, demlenmiş çay) veya aşırı C vitamini (askorbik asit) alımıyla oluşur. Bağırsak oksalat emilimini belirleyen iki kritik faktör vardır: Diyetteki kalsiyum alımı ve bağırsağın substrat olarak oksalat kullanan, oksalatı indirgeyen koruyucu bakteri **Oxalobacter formigenes** ile kolonizasyonudur. **2) Birincil Hiperoksalüri (PH)**: Otozomal resesif glioksilat metabolizma bozukluğudur (idrar oksalatı >100 mg/gün, genç yaş, agresif tekrarlayan taşlar). **PH Tip I (%80, en ağır)**: Alanin-glioksilat aminotransferaz (AGXT) defekti, tedavisi karaciğer/böbrek kombine naklidir. **PH Tip II (daha az şiddetli)**: Glioksilat redüktaz / hidroksipirüvat redüktaz (GRHPR) kusuru, tedavisi genellikle izole böbrek naklidir. **PH Tip III (en az şiddetli)**: Mitokondriyal 4-hidroksi-2-oksoglutarat aldolaz (HOGA) kusuru, böbrek yetmezliği riski düşüktür. **3) Enterik Hiperoksalüri**: Malabsorpsiyon (Crohn, ülseratif kolit, çölyak) veya bariatrik cerrahide serbest yağ asitleri kalsiyum ve magnezyum ile **sabunlaşır**. Kalsiyumsuz kalan serbest oksalat ve safra tuzlarının artırdığı kolon geçirgenliği nedeniyle aşırı emilir. 24 saatlik idrarda: **↓ İdrar hacmi, ↓ pH, ↓ Ca, ↓ Na, ↓ Sitrat ve belirgin ↑ Oksalat** görülür!',
        'flashcards': [
            {
                'id': 'uro-fc-14-01',
                'category': 'Bağırsak Kolonizasyonu',
                'front': 'Ders notuna göre bağırsakta substrat olarak oksalat kullanan ve oksalatı indirgeyerek emilimini azaltan koruyucu bakteri hangisidir?',
                'hint': 'Oksalat parçalayan bağırsak kommensali.',
                'back': '**Oxalobacter formigenes**. Bağırsakta oksalatı parçalayarak lümendeki serbest oksalat miktarını ve kolonik emilimi belirgin şekilde düşürür; kolonizasyon kaybı hiperoksalüri riskini artırır.'
            },
            {
                'id': 'uro-fc-14-02',
                'category': 'Birincil Hiperoksalüri',
                'front': 'Birincil Hiperoksalüri Tip I ve Tip II enzim defektleri ve nakil (organ transplantasyon) stratejileri nelerdir?',
                'hint': 'Ders notu Sayfa 38: AGXT vs GRHPR ve KC/böbrek vs böbrek nakli.',
                'back': '• **PH Tip I (%80, en ağır)**: **Alanin:glioksalat aminotransferaz (AGXT)** enzim kusuru. Tedavisi **Karaciğer / Böbrek naklidir** (enzim karaciğer peroksizomundadır).\n• **PH Tip II**: **Glioksilat redüktaz / hidroksipirüvat redüktaz (GRHPR)** enzim kusuru. Tedavisi genellikle **izole böbrek naklidir**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Oxalobacter formigenes Kolonizasyonu',
                    'desc': 'Bağırsak oksalat emilimini modüle eden ana biyolojik faktör, oksalatı indirgeyen bu bakterinin varlığıdır.',
                    'isKey': True
                },
                {
                    'title': 'Birincil Hiperoksalüri Tipleri (Sayfa 38)',
                    'desc': 'Tip I (AGXT kusuru, KC/böbrek nakli), Tip II (GRHPR kusuru, izole böbrek nakli), Tip III (HOGA kusuru, böbrek yetmezliği riski düşük).',
                    'isKey': True
                },
                {
                    'title': 'Enterik Oksalüri ve Ca-Mg Sabunlaşması',
                    'desc': 'Yağ asitleri Ca ve Mg ile sabunlaşır -> Kalsiyum oksalatı bağlayamaz -> Serbest oksalat ve safra tuzları etkisiyle kolondan emilir.',
                    'isKey': True
                },
                {
                    'title': 'Enterik Oksalüride 24 Saatlik İdrar Profili',
                    'desc': 'Hacim ↓, pH ↓, Ca ↓, Na ↓, Sitrat ↓, fakat İdrar Oksalatı belirgin ↑ artmıştır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 36-39: Hiperoksalüri Sınıflaması ve Klinik Profili',
                'headers': ['Hiperoksalüri Grubu', 'Temel Etyoloji / Enzim Kusuru', 'Özgün Mekanizma', 'Tedavi / Organ Nakli'],
                'rows': [
                    ['Diyet İlişkili', 'Oksalattan zengin besinler (fındık, çikolata, ıspanak, çay) veya aşırı C vitamini', 'Diyet kalsiyum düşüklüğü ve Oxalobacter formigenes eksikliği', 'Diyet modifikasyonu, yeterli kalsiyum ve hidrasyon'],
                    ['Birincil Tip I (PH I - %80)', 'Alanin:glioksalat aminotransferaz (AGXT) kusuru', 'Otozomal resesif endojen oksalat aşırı üretimi (>100 mg/gün)', 'Karaciğer / Böbrek Nakli'],
                    ['Birincil Tip II (PH II)', 'Glioksilat redüktaz / hidroksipirüvat redüktaz kusuru', 'Glioksilat metabolizma defekti (daha az şiddetli)', 'Genellikle izole Böbrek Nakli'],
                    ['Birincil Tip III (PH III)', 'Mitokondriyal 4-hidroksi-2-oksoglutarat aldolaz (HOGA)', 'HOGA gen mutasyonu (en az şiddetli tip)', 'Konservatif tedavi (böbrek yetmezliği nadir)'],
                    ['Enterik Hiperoksalüri', 'Malabsorpsiyon (Crohn, ülseratif kolit, çölyak) veya cerrahi rezeksiyon', 'Yağ asitlerinin Ca ve Mg ile sabunlaşması, safra tuzlarının kolon geçirgenliğini artırması', 'Oral kalsiyum desteği (lümen bağlama), yağ kısıtlaması']
                ]
            }
        },
        'spotPearls': [
            'Ders notuna göre bağırsakta oksalatı substrat olarak kullanan koruyucu bakteri Oxalobacter formigenes\'tir.',
            'Enterik hiperoksalüride 24 saatlik idrarda hacim, pH, kalsiyum, sodyum ve sitrat DÜŞÜK iken idrar oksalatı BELİRGİN YÜKSEKTİR.',
            'Birincil hiperoksalüri Tip I karaciğer/böbrek kombine nakli gerektirirken, Tip II\'de izole böbrek nakli yeterli olabilmektedir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Oxalobacter formigenes hiperoksalüriyi nasıl engeller?',
            'Enterik hiperoksalüride Ca ve Mg sabunlaşmasının mekanizması nedir?'
        ]
    },

    # Slide 15
    {
        'slideNumber': 15,
        'title': 'Hipositratüri ve Distal Renal Tübüler Asidoz (Tip 1 dRTA)',
        'subtitle': 'İntrasellüler asidoz, sitrat geri emilimi, paradoksal alkali idrar ve nefrokalsinozis',
        'badge': 'Asit-Baz & Tübüler',
        'badgeColor': 'indigo',
        'synthesisNarrative': '**Hipositratüri (idrar sitratı <320 mg/gün)**, kalsiyum taşlarının patogenezinde en sık gözden kaçan metabolik kusurdur. Sitrat atılımının ana düzenleyicisi **İntrasellüler Asidoz**dur. Sistemik asidozda veya hipokalemide proksimal tübül hücre içi asidotik hale gelir; hücre bu asidozu tamponlamak için lümendeki sitratı sodyum-dikarboksilat kotransporterı (NaDC-1) ile neredeyse tamamen geri emer; idrar sitratsız kalır. Bu tablonun en dramatik klinik tablosu **Tip 1 Distal Renal Tübüler Asidoz (dRTA)**\'dır. Distal tübüldeki H+-ATPaz pompası lümene asit pompalayamaz. Sonuçta: **Sistemik metabolik asidoz + Paradoksal olarak ALKALİ idrar (pH > 5.5-6.0) + Ağır Hipositratüri + Hiperkalsiüri** gelişir. Bu dörtlü kombinasyon bilateral nefrokalsinozis ve rekürren Kalsiyum Fosfat taşlarına yol açar.',
        'flashcards': [
            {
                'id': 'uro-fc-15-01',
                'category': 'Distal RTA',
                'front': 'Tip 1 Distal Renal Tübüler Asidozda (dRTA) taş oluşumunu tetikleyen 4 temel metabolik özellik nedir?',
                'hint': 'Sistemik asidoza rağmen idrar pH\'sı ve sitrat durumu.',
                'back': '1) Sistemik hiperkloremik metabolik asidoz\n2) **Paradoksal alkali idrar (pH daima > 5.5-6.0)** (H+ atılamaz)\n3) **Ağır Hipositratüri** (asidoz nedeniyle sitrat tübüllere geri emilir)\n4) **Hiperkalsiüri ve Nefrokalsinozis** (kemik tamponlamasından Ca salınır).'
            },
            {
                'id': 'uro-fc-15-02',
                'category': 'Sitrat Regülasyonu',
                'front': 'Hipokalemi (potasyum eksikliği) neden hipositratüriye ve taş riskine yol açar?',
                'hint': 'K-H değişimi ve proksimal tübül hücre içi pH\'sı.',
                'back': 'Hipokalemide hücreler potasyumu korumak için dışarı verirken içeri hidrojen (H+) alır. Bu durum **proksimal tübül hücresinde intrasellüler asidoz** yaratır. Asidotik tübül hücresi NaDC-1 taşıyıcısını aktive ederek idrardaki tüm sitratı emer; sonuçta idrarda taş koruyucu sitrat tükenir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Sitrat Atılımının Ana Kuralı',
                    'desc': 'Sistemik veya intrasellüler asidoz -> İdrar sitratı düşer; Alkaloz -> İdrar sitratı artar.',
                    'isKey': True
                },
                {
                    'title': 'Tip 1 dRTA ve Kalsiyum Fosfat',
                    'desc': 'Alkali idrarda kalsiyum fosfat hızla çöker; dRTA hastalarında taşlar genellikle kalsiyum fosfat (apatit/bruşit) karakterindedir.',
                    'isKey': True
                },
                {
                    'title': 'Nefrokalsinozis Tablosu',
                    'desc': 'Renal medullada yaygın kalsifikasyon (medüller sünger böbrek ve dRTA\'da tipiktir).'
                }
            ],
            'table': {
                'title': 'Metabolik Durumların İdrar Sitrat Düzeyine Etkisi',
                'headers': ['Klinik Durum', 'Hücre İçi Asit-Baz Durumu', 'İdrar Sitratı', 'Taş Riski'],
                'rows': [
                    ['Distal RTA (Tip 1)', 'Ağır intrasellüler asidoz', 'Belirgin Düşük (<100 mg/gün)', 'Çok Yüksek (Nefrokalsinozis)'],
                    ['Hipokalemi (Diyare, Diüretik)', 'İntrasellüler asidoz (K-H şifti)', 'Düşük (<320 mg/gün)', 'Yüksek (CaOx taşları)'],
                    ['Kronik İshal / Malabsorpsiyon', 'Bikarbonat kaybına bağlı asidoz', 'Çok Düşük', 'Yüksek'],
                    ['Yüksek Hayvansal Proteinli Diyet', 'Sülfat/asit yükü -> asidoz', 'Düşük', 'Yüksek (CaOx + Ürik Asit)'],
                    ['Potasyum Sitrat Tedavisi', 'Sistemik alkalinizasyon', 'Yüksek (>500 mg/gün)', 'Düşük (Koruyucu etki)']
                ]
            }
        },
        'spotPearls': [
            'Sistemik asidozu olan bir hastada idrar pH\'sı 5.3\'ün altına indirilemiyorsa (daima >5.5 ise) akla ilk Tip 1 dRTA gelmelidir.',
            'Hipositratüri tedavisinde sodyum sitrat yerine potasyum sitrat tercih edilir; çünkü sodyum kalsiüriyi artırırken potasyum hücre içi asidozu düzeltir.',
            'Karbonik anhidraz inhibitörleri (Asetazolamid, Topiramat) edinsel dRTA tablosu yaratarak kalsiyum fosfat taşlarına yol açar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Tip 1 dRTA\'da neden kalsiyum oksalat değil kalsiyum fosfat taşı oluşur?',
            'Potasyum sitrat neden sodyum bikarbonattan üstündür?'
        ]
    },

    # Slide 16
    {
        'slideNumber': 16,
        'title': 'Ürik Asit Taşları: Asidik İdrar ve Pürin Metabolizması',
        'subtitle': 'Düşük idrar pH\'sının (<5.5) belirleyici rolü, pKa dinamiği ve medikal kemoliz',
        'badge': 'Ürik Asit & Çözünürlük',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Ürik asit taşları tüm üriner taşların %5-10\'unu oluşturur. Patofizyolojisindeki en kritik kavram: Taş oluşumundaki birincil belirleyici etken aşırı ürik asit atılımından (hiperürikozüri) ziyade **DÜŞÜK İDRAR pH\'SIdır (pH < 5.5)**. Ürik asidin pKa değeri **5.35 - 5.5**\'tir. İdrar pH\'sı pKa\'nın üzerine çıktığında çözünür iyonize ürat formuna geçer; ancak idrar pH\'sı 5.5\'in altına düştüğünde çözünürlüğü neredeyse sıfıra inen **serbest (nötral) ürik asit** baskın hale gelir ve hızla çöker. Hastaların çoğunda 24 saatlik idrar ürik asit miktarı tamamen normal sınırlardadır! Tip 2 DM, gut, miyeloproliferatif hastalıklar ve kronik ishal risk grubudur. Direkt grafide (DÜSG) tamamen **radyolüsenttir**. En önemli avantajı: **İdrar alkalinizasyonu (pH 6.5-7.0) ile medikal olarak tamamen eritilebilen (kemoliz) tek taş türüdür**.',
        'flashcards': [
            {
                'id': 'uro-fc-16-01',
                'category': 'Ürik Asit pH',
                'front': 'Ürik asit taşı patogenezinde en kritik faktör idrar ürik asit miktarı mıdır, idrar pH\'sı mıdır?',
                'hint': 'pKa 5.35 değeri ve çözünürlük dengesi.',
                'back': '**İdrar pH\'sıdır (Kalıcı asidik idrar, pH < 5.5)**. Birçok hastada 24 saatlik idrar ürik asit atılımı normaldir; ancak idrar pH\'sı asidik olduğu için ürik asit çözünemez ve çöker. Yüksek ürik asit atılımı olsa bile idrar alkali ise taş oluşmaz.'
            },
            {
                'id': 'uro-fc-16-02',
                'category': 'Medikal Kemoliz',
                'front': 'Ürik asit taşlarının medikal eritme (kemoliz) tedavisinde hedef idrar pH aralığı nedir ve neden pH > 7.2 istenmez?',
                'hint': 'Taş eritme hedefi ve kalsiyum fosfat çökme riski.',
                'back': 'Hedef idrar pH\'sı **6.5 - 7.0** arasıdır. pH\'nın 7.2 - 7.5\'in üzerine çıkması istenmez; çünkü aşırı alkalik idrarda bu kez **Kalsiyum Fosfat taşları çökmeye başlar** ve taşın yüzeyini kaplayarak erimesini durdurur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Kalıcı Asidik İdrar (pH < 5.5)',
                    'desc': 'Bozulmuş tübüler amonyogenez sonucu gelişir (Tip 2 DM ve metabolik sendromda tipik).',
                    'isKey': True
                },
                {
                    'title': 'Radyolüsent Karakter',
                    'desc': 'DÜSG röntgeninde görülmez; USG ve Kontrassız BT\'de net izlenir (HU: 300-500).',
                    'isKey': True
                },
                {
                    'title': 'Oral Kemoliz (Taş Eritme)',
                    'desc': 'Potasyum sitrat veya sodyum bikarbonat ile idrar pH\'sı 6.5-7.0\'a çıkarılarak taş cerrahisiz eritilebilir.',
                    'isKey': True
                },
                {
                    'title': 'Ksantin Oksidaz İnhibitörü (Allopurinol)',
                    'desc': 'Allopurinol, yalnızca eşlik eden hiperürisemi veya aşırı hiperürikozüri (>700-800 mg/gün) varlığında tedaviye eklenir.'
                }
            ],
            'table': {
                'title': 'İdrar pH Değişiminin Ürik Asit Çözünürlüğüne Etkisi',
                'headers': ['İdrar pH Değeri', 'Baskın Moleküler Form', 'Ürik Asit Çözünürlüğü', 'Klinik Sonuç'],
                'rows': [
                    ['pH < 5.0', 'Çözünmeyen Nötral Ürik Asit (>%85)', '< 100 mg/L', 'Masif taş çökmesi ve kristalüri'],
                    ['pH 5.35 - 5.5 (pKa)', '%50 Nötral Ürik Asit / %50 İyonize Ürat', '~ 200 mg/L', 'Kritik metastabil sınır'],
                    ['pH 6.5', 'Çözünür Ürat İyonu (>%90)', '~ 1200 mg/L', 'Taş erimeye başlar (Etkili kemoliz)'],
                    ['pH 7.0', 'Tamamen İyonize Ürat (>%98)', '> 2000 mg/L', 'Optimal medikal kemoliz sahası'],
                    ['pH > 7.5', 'İyonize Ürat', 'Çok Yüksek', 'Risk: Kalsiyum fosfat çökmesi başlar']
                ]
            }
        },
        'spotPearls': [
            'Ürik asit taşı, cerrahiye gerek kalmadan sadece ağızdan ilaçla (alkalinizasyon) tamamen eritilebilen tek taştır.',
            'DÜSG\'de taş görülmeyip USG veya BT\'de üreterde tıkanıklık yapan taş saptandığında ilk akla ürik asit gelmelidir.',
            'Kemoliz tedavisinde hasta günde 3-4 kez idrar stripi ile idrar pH\'sını ölçerek ilaç dozunu 6.5-7.0 aralığına ayarlar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_uric_acid_ph'], matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Ürik asit taşı nasıl eritilir?',
            'Ürik asit taşlarında allopurinol ne zaman başlanmalıdır?'
        ]
    },

    # Slide 17
    {
        'slideNumber': 17,
        'title': 'Sistin Taşları ve Sistinüri Patolojisi (COLA Defekti)',
        'subtitle': 'SLC3A1 / SLC7A9 mutasyonları, hekzagonal kristaller, sodyum ilişkisi ve nitroprussid testi',
        'badge': 'Genetik & Metabolizma',
        'badgeColor': 'rose',
        'synthesisNarrative': '**Sistinüri**, renal proksimal tübül ve ince bağırsak epitelinde yer alan dibazik aminoasit taşıyıcı sistemindeki mutasyonlara bağlı gelişen **otozomal resesif** bir hastalıktır. Genetik defekt **SLC3A1** (rBAT) veya **SLC7A9** (b0,+AT) genlerindedir. Taşıyıcı kusuru nedeniyle 4 dibazik aminoasidin idrarla atılımı aşırı artar: **Cystine, Ornithine, Lysine, Arginine (COLA)**. Bu grupta yer alan ornitin, lizin ve arginin fizyolojik pH\'da suda son derece çözünürken; **Sistin** fizyolojik idrar pH\'sında çok az çözünür ve erken yaşta iki taraflı rekürren taşlar yapar. Sistin çözünürlüğü artan idrar pH\'sı ile artar. Ders notunda özellikle vurgulanan hayati nokta: **"Sodyum sistin atılımını arttırır."** Bu nedenle sistinüri hastalarında tuz (sodyum) kısıtlaması birinci basamak koruyucu tedavidir. İdrar mikroskopisinde **patojenik hekzagonal (altıgen) kristaller** patognomoniktir. Tarama testi **Sodyum Siyanid Nitroprussid** testidir.',
        'flashcards': [
            {
                'id': 'uro-fc-17-01',
                'category': 'Genetik Defekt',
                'front': 'Sistinüride proksimal tübülden geri emilemeyip idrarla atılan 4 dibazik aminoasit (COLA) hangileridir?',
                'hint': 'Hastalığın adını veren aminoasit ve diğer üç bazik aminoasit.',
                'back': '**C**ystine (Sistin), **O**rnithine (Ornitin), **L**ysine (Lizin), **A**rginine (Arginin) = **COLA**. Yalnızca sistin çözünürlüğü düşük olduğu için taşlaşır; diğer üçü suda erir.'
            },
            {
                'id': 'uro-fc-17-02',
                'category': 'Sodyum ve Sistin İlişkisi',
                'front': 'Ders notuna göre sodyum alımının idrar sistin atılımı ve taş riski üzerindeki doğrudan etkisi nedir?',
                'hint': 'Sayfa 47: Sodyum sistin atılımını...',
                'back': 'Ders notuna göre: **"Sodyum sistin atılımını arttırır."** Yüksek sodyumlu diyet proksimal tübülde sistin atılımını kamçılar; bu nedenle hastalarda katı **tuz/sodyum kısıtlaması** taş nüksünü önlemede şarttır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Otozomal Resesif COLA Defekti',
                    'desc': 'SLC3A1 ve SLC7A9 mutasyonları; Sistin, Ornitin, Lizin ve Arginin atılımı artar.',
                    'isKey': True
                },
                {
                    'title': 'Sodyum Kısıtlaması Kuralı (Sayfa 47)',
                    'desc': 'Sodyum sistin atılımını arttırır; bu nedenle düşük sodyumlu diyet temel tedavi unsurudur.',
                    'isKey': True
                },
                {
                    'title': 'Alkalinizasyon (Hedef pH > 7.5)',
                    'desc': 'Sistin çözünürlüğü idrar pH\'sı arttıkça belirgin şekilde artar (potasyum sitrat kullanılır).',
                    'isKey': True
                },
                {
                    'title': 'Tiyol İçeren Şelatör İlaçlar',
                    'desc': 'D-Penisilamin ve Tiopronin (Alfa-MPG), sistin ile disülfit bağı kurarak suda çözünür kompleks oluşturur.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 47: Sistinüri Patolojisi ve Yönetimi',
                'headers': ['Alan', 'Özellik / Müdahale', 'Patofizyolojik Mekanizma', 'Klinik Önemi'],
                'rows': [
                    ['Genetik & Defekt', 'Otozomal Resesif', 'Dibazik aminoasit (COLA) taşıyıcı kusuru', 'Genç yaşta rekürren taşlar'],
                    ['Çözünürlük & pH', 'Asitte Çökme, Alkalide Çözünme', 'pH arttıkça iyonlaşma ve çözünürlük katlanır', 'Hedef idrar pH > 7.5'],
                    ['Diyet Sodyumu', 'Katı Sodyum Kısıtlaması', 'Sodyum sistin atılımını doğrudan artırır!', 'Tuz alımı kısıtlanmalıdır'],
                    ['Tanısal Test', 'Na-Siyanid Nitroprussid', 'Serbest sistin ile kırmızı-mor renk reaksiyonu', 'Hızlı idrar tarama testi'],
                    ['Mikroskopi', 'Hekzagonal (Altıgen) Kristaller', 'Sistin tuzunun karakteristik geometrik formu', 'Patognomoniktir']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 47: "Sodyum sistin atılımını arttırır" (bu nedenle tuz kısıtlaması en az hidrasyon kadar kritiktir).',
            'Sistin taşları kükürt içeriği nedeniyle DÜSG\'de hafif zayıf radyoopaktır (buzlu cam / mumsu opasite).',
            'Sistin taşları ESWL şok dalgalarına en dirençli taşlardandır; cerrahi gerektiğinde lazer litotripsi tercih edilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_cystinuria_cola'], matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Sistinüri tedavisinde sodyum kısıtlaması neden bu kadar önemlidir?',
            'Sistin taşlarında idrar pH hedefi neden ürik asitten daha yüksektir?'
        ]
    },

    # Slide 18
    {
        'slideNumber': 18,
        'title': 'Enfeksiyon Taşları (Strüvit / Magnezyum Amonyum Fosfat)',
        'subtitle': 'Proteus, Klebsiella, Staph. aureus/epidermidis, üreaz aktivitesi ve Staghorn taşları',
        'badge': 'Enfeksiyon & Üreaz',
        'badgeColor': 'emerald',
        'synthesisNarrative': '**Enfeksiyon Taşları**, üriner sistemin üreaz üreten bakterilerle kronik enfeksiyonu zemininde gelişir. Taş bileşenleri: **Magnezyum amonyum fosfat (Strüvit), Karbonat apatit ve Amonyum ürat**tır. Resmi ders notunda (Sayfa 49) üreaz enzimi oluşturan bakteriler açıkça belirtilmiştir: **Proteus mirabilis, Klebsiella pneumoniae, Staphylococcus aureus ve Staphylococcus epidermidis**. Üreaz enzimi ürenin amonyak ve karbondioksite dönüşümünü katalizler: `Üre -> NH3 + CO2`. Oluşan amonyak ortamdaki serbest hidrojenleri bağlar; alkali idrar yüksek düzeyde amonyum ve fosfat oluşumunu destekleyerek **Strüvit taş oluşumuna** yol açar. **ÇOK ÖNEMLİ KURUL BİLGİSİ: E. coli üreaz üretmez; dolayısıyla saf E. coli enfeksiyonu strüvit taşı yapmaz!** Strüvit taşları tüm kaliksleri kaplayarak devasa **Geyik Boynuzu (Staghorn)** taşlarına dönüşür.',
        'flashcards': [
            {
                'id': 'uro-fc-18-01',
                'category': 'Enfeksiyon Taşı',
                'front': 'Ders notuna göre üreaz enzimi oluşturarak strüvit taşına yol açan 4 temel bakteri hangisidir?',
                'hint': 'Sayfa 49: Proteus, Klebsiella ve iki Stafilokok türü.',
                'back': 'Ders notu Sayfa 49:\n1) **Proteus mirabilis** (en sık)\n2) **Klebsiella pneumoniae**\n3) **Staphylococcus aureus**\n4) **Staphylococcus epidermidis**\n(NOT: E. coli üreaz üretmez, tek başına strüvit taşı yapmaz!).'
            },
            {
                'id': 'uro-fc-18-02',
                'category': 'Üreaz Reaksiyonu',
                'front': 'Enfeksiyon taşlarının temel bileşenleri ve bakteriyel üreaz reaksiyonunun sonucu nedir?',
                'hint': 'Sayfa 49: 3 temel mineral bileşeni ve idrar pH etkisi.',
                'back': 'Bileşenler: **Magnezyum amonyum fosfat (Strüvit), Karbonat apatit ve Amonyum ürat**.\nÜreaz enzimi üreyi amonyak ve karbondioksite dönüştürür; açığa çıkan yüksek amonyum ve aşırı **alkali idrar** fosfat çökmesini destekleyerek strüvit taşını oluşturur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Ders Notundaki Üreaz (+) Bakteriler',
                    'desc': 'Proteus mirabilis, Klebsiella pneumoniae, Staphylococcus aureus ve Staphylococcus epidermidis.',
                    'isKey': True
                },
                {
                    'title': 'Enfeksiyon Taşı Bileşenleri (Sayfa 49)',
                    'desc': 'Magnezyum amonyum fosfat (Strüvit), Karbonat apatit ve Amonyum ürat.',
                    'isKey': True
                },
                {
                    'title': 'E. coli Üreaz Negatiftir!',
                    'desc': 'Toplumda en sık İYE etkeni olan E. coli üreaz üretmediği için tek başına strüvit taşı oluşturamaz.',
                    'isKey': True
                },
                {
                    'title': 'Geyik Boynuzu (Staghorn) ve Cerrahi',
                    'desc': 'Kolektör sistemi dolduran döküm taşlardır; tam cerrahi temizlik (PNL) ve antibiyoterapi zorunludur.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 49: Enfeksiyon Taşları ve Mikrobiyolojik Özellikleri',
                'headers': ['Bileşen / Bakteri Türü', 'Üreaz Enzim Durumu', 'İdrar pH Etkisi', 'Klinik Tablo'],
                'rows': [
                    ['Proteus mirabilis', 'Üreaz Pozitif (Güçlü)', 'Aşırı Alkali (pH > 7.2 - 8.0)', 'En sık enfeksiyon / Staghorn taşı etkeni'],
                    ['Klebsiella pneumoniae', 'Üreaz Pozitif', 'Alkali pH', 'Komplike taş oluşturan üropatojen'],
                    ['Staphylococcus aureus', 'Üreaz Pozitif', 'Alkali pH', 'Enfeksiyon taşı oluşturan gram (+) kok'],
                    ['Staphylococcus epidermidis', 'Üreaz Pozitif', 'Alkali pH', 'Enfeksiyon taşı oluşturan koagülaz (-) kok'],
                    ['Escherichia coli', 'Üreaz NEGATİF', 'Değişken / Asidik', 'Tek başına strüvit taşı yapmaz (Sınav tuzağı!)']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 49: Üreaz pozitif etkenler Proteus mirabilis, Klebsiella pneumoniae, Staphylococcus aureus ve Staphylococcus epidermidis\'tir.',
            'Enfeksiyon taşlarının 3 temel formu: Magnezyum amonyum fosfat, karbonat apatit ve amonyum ürattır.',
            'E. coli üreaz negatif olduğu için staghorn/strüvit taşı yapmaz; bu kural kurul sınavlarının en klasik sorusudur.'
        ],
        'relatedQuestions': [matched_questions_dict['q_struvite_urease'], matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Sayfa 49\'daki üreaz pozitif bakteriler hangileridir?',
            'E. coli neden strüvit taşı oluşturamaz?'
        ]
    },

    # Slide 19
    {
        'slideNumber': 19,
        'title': 'İlaç Kaynaklı Taşlar ve Nadir Taş Türleri',
        'subtitle': 'Asetazolamid, Topiramat, HCTZ, İndinavir, Ritonavir, Triamteren, Guaifenesin ve Efedrin',
        'badge': 'İlaçlar & Nadir Taşlar',
        'badgeColor': 'purple',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 51) **İlaç Kaynaklı Taşlar** iki grupta incelenir: **1) Metabolik Asidoz ve İdrar Kompozisyonunu Bozarak Taş Yapanlar**: **Karbonik Anhidraz İnhibitörleri (Asetazolamid ve Topiramat)**: İdrar pH\'sini artıran, idrar sitratını azaltan ve bazen hiperkalsiüriyi destekleyen bir metabolik asidoz tablosu yaratarak kalsiyum fosfat taşlarına yol açarlar. **Hidroklorotiyazid (HCTZ)**: Hipokalemi sonucu hücre içi asidoz yoluyla **hipositratüriye** neden olarak taş riskini tetikleyebilir. **2) Doğrudan İdrarda Taş Oluşturan İlaçlar**: Proteaz inhibitörleri (**İndinavir ve Ritonavir**), **Triamteren**, **Guaifenesin** ve **Efedrin**dir. İndinavir suda zor çözünür, idrarda doğrudan kristalleşir ve direkt grafide (DÜSG) tamamen **RADYOLÜSENTTİR**.',
        'flashcards': [
            {
                'id': 'uro-fc-19-01',
                'category': 'Doğrudan Taş Yapan İlaçlar',
                'front': 'Ders notu Sayfa 51\'e göre idrarda doğrudan kristalleşerek taş oluşturan ilaçlar hangileridir?',
                'hint': 'Proteaz inhibitörleri ve diğer üç aktif bileşik.',
                'back': 'Ders notu Sayfa 51\'e göre doğrudan taş oluşturan ilaçlar:\n• Proteaz inhibitörleri: **İndinavir** ve **Ritonavir**\n• **Triamteren**\n• **Guaifenesin**\n• **Efedrin**'
            },
            {
                'id': 'uro-fc-19-02',
                'category': 'İlaç Metabolizması',
                'front': 'Ders notuna göre Asetazolamid, Topiramat ve Hidroklorotiyazid hangi mekanizmalarla taş oluşumunu tetikler?',
                'hint': 'Karbonik anhidraz inhibisyonu vs hipokalemi / hücre içi asidoz.',
                'back': '• **Asetazolamid ve Topiramat**: Karbonik anhidraz inhibitörüdür; idrar pH\'sini artıran, idrar sitratını azaltan ve hiperkalsiüriyi destekleyen metabolik asidoz yaratırlar.\n• **Hidroklorotiyazid**: Hipokalemi sonucu hücre içi asidoz yoluyla **hipositratüriye** yol açabilir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Doğrudan Taş Yapan İlaçlar (Sayfa 51)',
                    'desc': 'Proteaz inhibitörleri (İndinavir ve Ritonavir), Triamteren, Guaifenesin ve Efedrin.',
                    'isKey': True
                },
                {
                    'title': 'Karbonik Anhidraz İnhibitörleri',
                    'desc': 'Asetazolamid ve Topiramat: İdrar pH\'sini artırır, idrar sitratını azaltır, hiperkalsiüriyi destekler.',
                    'isKey': True
                },
                {
                    'title': 'Hidroklorotiyazid Uyarısı',
                    'desc': 'Hipokalemiye bağlı hücre içi asidoz geliştirerek hipositratüriye neden olabilir.',
                    'isKey': True
                },
                {
                    'title': 'İndinavir Radyolüsensitesi',
                    'desc': 'DÜSG\'de ve kontrassız BT\'de görünmeyebilir; hidrasyon ve ilacın kesilmesiyle çözünür.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 51: İlaç Kaynaklı Taşlar ve Mekanizmaları',
                'headers': ['İlaç Grubu / İlaç Adı', 'Kullanım Endikasyonu', 'Ders Notundaki Patolojik Mekanizma', 'Oluşan Taş Tipi / Opasite'],
                'rows': [
                    ['İndinavir ve Ritonavir', 'HIV / Proteaz İnhibitörü', 'Doğrudan idrarda kristalleşme', 'Tamamen Radyolüsent'],
                    ['Triamteren', 'Potasyum tutucu diüretik', 'Doğrudan kristalleşen aktif bileşik', 'Radyolüsen / Zayıf opak'],
                    ['Guaifenesin', 'Ekspektoran öksürük ilacı', 'Doğrudan idrarda kristalleşme', 'Radyolüsent'],
                    ['Efedrin', 'Dekonjestan / Sempatomimetik', 'Doğrudan idrarda kristalleşme', 'Radyolüsent'],
                    ['Asetazolamid & Topiramat', 'Glokom, Migren, Epilepsi', 'İdrar pH ↑, Sitrat ↓, Hiperkalsiüri ↑ yaratan metabolik asidoz', 'Radyoopak (Kalsiyum fosfat)'],
                    ['Hidroklorotiyazid', 'Hipertansiyon, Hiperkalsiüri', 'Hipokalemi sonucu hücre içi asidoz -> Hipositratüri', 'Kalsiyum taşı riski']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 51: Doğrudan taş oluşturan ilaçlar İndinavir, Ritonavir, Triamteren, Guaifenesin ve Efedrin\'dir.',
            'Karbonik anhidraz inhibitörleri (asetazolamid, topiramat) idrar pH\'sini artırıp sitratı düşürerek kalsiyum fosfat taşı yaparlar.',
            'Hidroklorotiyazid hipokalemiye bağlı hücre içi asidoz geliştirirse sekonder hipositratüriye neden olabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_dusg_radiopacity']],
        'aiPromptSuggestions': [
            'Ders notundaki doğrudan taş oluşturan 5 ilaç hangisidir?',
            'Topiramat ve asetazolamid idrar parametrelerini nasıl bozar?'
        ]
    },

    # Slide 20
    {
        'slideNumber': 20,
        'title': 'Ürolitiyazis Sentez Özeti, Sınav Tuzakları ve Klinik Yaklaşım',
        'subtitle': 'pH-Taş haritası, acil dekompresyon endikasyonları ve kurul sınavı altın kuralları',
        'badge': 'Sentez & Sınav Stratejisi',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Ürolitiyazis patofizyolojisini kavramanın en pratik yolu **İdrar pH\'sı - Taş Türü Korelasyonu**nu bilmektir. **Asidik idrarda (pH < 5.5)** Ürik asit ve Sistin taşları çöker. **Nötr / Hafif asidik idrarda (pH 5.5 - 6.5)** Kalsiyum oksalat taşları oluşur. **Alkalik idrarda (pH > 7.0-7.2)** ise Strüvit (enfeksiyon), Karbonat apatit ve Kalsiyum fosfat taşları çöker. Klinik aciller açısından unutulmaması gereken altın kural: **Üriner Obstrüksiyon + Ateş/İnfeksiyon (piyonefroz/enfekte hidronefroz) = MUTLAK ÜROLOJİK ACİLDİR**. Bu hastalarda taş kırma veya litotripsi denenmez; toplayıcı sistem derhal Double-J stent veya Perkütan Nefrostomi ile acil dekomprese edilmeli ve sepsis önlenmelidir.',
        'flashcards': [
            {
                'id': 'uro-fc-20-01',
                'category': 'Sınav Özeti',
                'front': 'İdrar pH\'sına göre taşların dağılımı nasıldır (Asidik vs Nötr vs Alkalik)?',
                'hint': 'Hangi taş hangi pH aralığında çöker?',
                'back': '• **Asidik İdrar (pH < 5.5)**: Ürik Asit, Sistin.\n• **Nötr / Hafif Asit (pH 5.5 - 6.8)**: Kalsiyum Oksalat (pH\'dan görece bağımsızdır).\n• **Alkalik İdrar (pH > 7.0 - 7.5)**: Strüvit (Magnezyum amonyum fosfat), Karbonat Apatit, Kalsiyum Fosfat (Bruşit).'
            },
            {
                'id': 'uro-fc-20-02',
                'category': 'Ürolojik Acil',
                'front': 'Ürolitiyaziste acil dekompresyon (Double-J stent veya nefrostomi) gerektiren kesin endikasyonlar nelerdir?',
                'hint': 'Obstrüksiyonla birleşen hayatı tehdit edici tablolar.',
                'back': '1) **Obstrüksiyon + Enfeksiyon (ateş, sepsis, piyonefroz)** (Mutlak acil!)\n2) Soliter böbrekte obstrüksiyon\n3) Bilateral obstrüksiyon (akut böbrek hasarı)\n4) Medikal tedaviye dirençli refrakter ağrı ve inatçı kusma.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'İdrar pH Haritası',
                    'desc': 'Ürik asit ve sistin asitte; strüvit ve kalsiyum fosfat bazik idrarda çöker.',
                    'isKey': True
                },
                {
                    'title': 'Radyoopasite Özeti',
                    'desc': 'Radyoopak: CaOx, CaP. Zayıf opak: Strüvit, Sistin. Radyolüsen: Ürik asit, Ksantin, İndinavir.',
                    'isKey': True
                },
                {
                    'title': 'Randall Plağı Mantığı',
                    'desc': 'Apatit (CaP) plağı üzerinde CaOx taşı büyür.',
                    'isKey': True
                },
                {
                    'title': 'Enfekte Hidronefroz Kuralı',
                    'desc': 'Acil cerrahi drenaj yapılmadan antibiyotik tek başına etkisizdir (kapalı abse prensibi).',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Master Ürolitiyazis Karşılaştırma Matrisi (Sınav Özeti)',
                'headers': ['Taş Türü', 'İdrar pH Eğilimi', 'DÜSG Görünümü', 'En Sık Etyolojik Neden', 'Birincil Medikal Önlem'],
                'rows': [
                    ['CaOx Monohidrat (Whewellite)', 'Her pH (5.5-6.8)', 'Belirgin Radyoopak', 'Hiperoksalüri, dehidratasyon', 'Bol hidrasyon, oksalat kısıtlama'],
                    ['CaOx Dihidrat (Weddellite)', 'Her pH (5.5-6.8)', 'Belirgin Radyoopak', 'Hiperkalsiüri', 'Tiyazid diüretiği, tuz kısıtlaması'],
                    ['Kalsiyum Fosfat (Bruşit)', 'Alkali (>6.5)', 'Radyoopak (Çok Sert)', 'Distal RTA, Primer HPT', 'Altta yatan RTA/HPT tedavisi'],
                    ['Ürik Asit', 'Asidik (<5.5)', 'Tamamen Radyolüsen', 'Metabolik sendrom, Tip 2 DM, Gut', 'Potasyum Sitrat (pH 6.5-7.0 hedefi)'],
                    ['Sistin', 'Asidik (<6.5)', 'Zayıf Radyoopak', 'SLC3A1/SLC7A9 mutasyonu (COLA)', 'pH > 7.5 yapma, Tiopronin'],
                    ['Strüvit (Enfeksiyon)', 'Alkali (>7.2)', 'Zayıf/Orta Radyoopak (Staghorn)', 'Proteus mirabilis üreazı', 'Tam cerrahi temizlik (PNL) + antibiyotik']
                ]
            }
        },
        'spotPearls': [
            'Kalsiyum kısıtlaması paradoksal olarak kalsiyum oksalat taşını artırır (en sık düşülen sınav tuzağı!).',
            'E. coli üreaz negatif olduğu için staghorn/strüvit taşı yapmaz; etken aranırken Proteus ilk sırada düşünülür.',
            'Ürik asit taşı kontrassız BT\'de net görülür, DÜSG\'de görülmez ve potasyum sitrat ile eritilebilir.',
            'Randall plağı Henle kulpunda apatit olarak başlar, papilla ucunu erode eder ve üzerine CaOx çökmesiyle taşlaşır.'
        ],
        'relatedQuestions': [
            matched_questions_dict['q_dusg_radiopacity'],
            matched_questions_dict['q_struvite_urease'],
            matched_questions_dict['q_cystinuria_cola'],
            matched_questions_dict['q_uric_acid_ph'],
            matched_questions_dict['q_randall_plaque']
        ],
        'aiPromptSuggestions': [
            'Tüm taş tiplerinin idrar pH ve radyoopasite özetini ver.',
            'Acil ürolojik dekompresyon endikasyonları nelerdir?'
        ]
    }
]

# Build the complete deck object
batch2_deck = {
    'id': 'deck-urolithiasis-pathophysiology',
    'title': 'Ürolitiyazis Patofizyolojisi (Taş Hastalığı)',
    'shortTitle': 'Ürolitiyazis Patofizyolojisi',
    'discipline': 'Üroloji / Tıbbi Biyokimya & Patoloji',
    'committee': 'Kurul 1',
    'instructor': 'Dr. Fahrettin Şamil Uysal',
    'audioFile': '2)Ürolitiyazis Patofizyolojisi.mp3',
    'audioDuration': '55 dk',
    'confidence': '%99 (Resmi Ders Notu & Redakte Veri Sentezi)',
    'themeColor': 'amber',
    'matchedNoteId': 'knote-donem3-kurul1-urolitiyazis',
    'matchedNoteTitle': '2)Ürolitiyazis Patofizyolojisi.txt',
    'overview': 'Böbrek ve üriner sistem taşlarının epidemiyolojisi, süpersatürasyon termodinamiği, nükleasyon, agregasyon ve retansiyon basamakları; kristalizasyon inhibitörleri (sitrat, nefrokalsin, uromodulin); Randall plak teorisi; Kalsiyum, Ürik asit, Sistin ve Strüvit taşlarının patofizyolojisi, radyoopasite sınıflaması ve klinik sınav tuzakları.',
    'highYieldPearls': [
        'Türkiye taş kuşağı ülkesidir ve toplumda görülme sıklığı %15\'tir.',
        'Kalsiyum taşları en sık (%70-80), ürik asit taşları ikinci sırada (%5-10) gelir.',
        'DÜSG\'de radyoopak taşlar kalsiyum tuzlarıdır; ürik asit, ksantin ve indinavir ise tamamen radyolüsenttir.',
        'Randall plakları ince Henle kulpu bazal membranında kalsiyum apatit olarak başlar; erozyon sonrası üzerine CaOx kristalleri epitaksiyle çöker.',
        'Sitrat, serbest kalsiyumu bağlayarak, nükleasyonu, agregasyonu ve epitaksiyi bloke eden en güçlü 4 yönlü inhibitördür.',
        'Tamm-Horsfall proteini (uromodulin) alkali idrarda taş inhibitörüdür; ancak asidik idrarda polimerize olarak agregasyon promotörü olur.',
        'Tip 2 DM ve metabolik sendromda bozulmuş amonyogenez kalıcı asidik idrara (pH < 5.5) ve ürik asit taşına yol açar.',
        'Ürik asit taşında en kritik faktör pH < 5.5 olmasıdır; potasyum sitrat ile alkalinizasyon (pH 6.5-7.0) yapılarak eritilebilir.',
        'Sistinüri, SLC3A1/SLC7A9 mutasyonuna bağlı otozomal resesif COLA (Sistin, Ornitin, Lizin, Arginin) taşıyıcı defektidir; hekzagonal kristaller patognomoniktir.',
        'Strüvit (magnezyum amonyum fosfat) taşları üreaz (+) bakterilerin (Proteus mirabilis) üreyi parçalamasıyla idrar pH\'sı >7.2\'ye fırladığında oluşur. E. coli üreaz üretmez!',
        'Obstrüksiyon + Ateş/İnfeksiyon (enfekte hidronefroz) mutlak ürolojik acildir ve derhal Double-J stent veya nefrostomi ile dekomprese edilmelidir.'
    ],
    'slides': slides_batch2,
    'totalSlides': len(slides_batch2),
    'matchedPastQuestionsCount': 5
}

# Update or replace deck in existing_decks
# Remove any existing urolithiasis deck with id 'deck-urolithiasis-pathophysiology' or 'learn-urolitiyazis-patofizyolojisi'
filtered_decks = [d for d in existing_decks if d.get('id') not in ['deck-urolithiasis-pathophysiology', 'learn-urolitiyazis-patofizyolojisi']]

# Insert right after batch 1 (index 1)
filtered_decks.insert(1, batch2_deck)

with open(decks_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_decks, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(filtered_decks)} decks into {decks_file} (Batch 2 inserted at index 1).")

# Update meta_file
if os.path.exists(meta_file):
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta_list = json.load(f)
else:
    meta_list = []

batch2_meta = {
    'id': batch2_deck['id'],
    'title': batch2_deck['title'],
    'shortTitle': batch2_deck['shortTitle'],
    'discipline': batch2_deck['discipline'],
    'committee': batch2_deck['committee'],
    'instructor': batch2_deck['instructor'],
    'totalSlides': len(slides_batch2),
    'matchedQuestionsCount': len(matched_questions_dict),
    'totalFlashcardsCount': sum(len(s.get('flashcards', [])) for s in slides_batch2),
    'themeColor': '#d97706',
    'overview': batch2_deck['overview']
}

# Remove existing urolithiasis entries
filtered_meta = [m for m in meta_list if m.get('id') not in ['deck-urolithiasis-pathophysiology', 'learn-urolitiyazis-patofizyolojisi']]
filtered_meta.insert(1, batch2_meta)

with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_meta, f, ensure_ascii=False, indent=2)

print(f"Updated {meta_file} with {len(filtered_meta)} entries.")
