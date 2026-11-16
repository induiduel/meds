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

# Matched real past questions for UTI
matched_questions_dict = {
    'q_etiology_ecoli': {
        'id': 'd3-k1-enf-039',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Tıbbi Mikrobiyoloji',
        'topic': 'ÜSE Mikrobiyolojisi ve E. coli',
        'stem': 'Toplum kökenli üriner sistem enfeksiyonlarına (akut sistit ve piyelonefrit) en sık sebep olan mikroorganizma aşağıdakilerden hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Streptococcus agalactiae'},
            {'key': 'B', 'text': 'Staphylococcus epidermidis'},
            {'key': 'C', 'text': 'Escherichia coli', 'isCorrect': True},
            {'key': 'D', 'text': 'Enterobacter aerogenes'},
            {'key': 'E', 'text': 'Pseudomonas aeruginosa'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Toplum kökenli komplike olmayan üriner sistem enfeksiyonlarının (akut sistit ve akut piyelonefrit) yaklaşık %75-90\'ından üropatojenik Escherichia coli (UPEC) sorumludur. Genç cinsel aktif kadınlarda ikinci sırada Staphylococcus saprophyticus (%5-15) gelir. Nozokomiyal veya komplike İYE\'lerde E. coli sıklığı %30-50\'ye gerilerken Klebsiella, Proteus, Enterococcus ve Pseudomonas oranları artar.'
    },
    'q_complicated_uti': {
        'id': 'd3-k1-enf-042',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Enfeksiyon Hastalıkları',
        'topic': 'Komplike Üriner Sistem Enfeksiyonu Kriterleri',
        'stem': 'Aşağıdakilerden hangisi bir üriner sistem enfeksiyonunu (ÜSE) \'komplike\' kılan predispozan faktörlerden biri DEĞİLDİR?',
        'options': [
            {'key': 'A', 'text': 'Hastada ateş yüksekliği olması', 'isCorrect': True},
            {'key': 'B', 'text': 'Hastanın erkek cinsiyette olması'},
            {'key': 'C', 'text': 'Nefrolitiyazis (böbrek taşı) varlığı'},
            {'key': 'D', 'text': 'Nörojenik mesane fonksiyon bozukluğu'},
            {'key': 'E', 'text': 'Kontrolsüz Diabetes Mellitus varlığı'}
        ],
        'correctAnswer': 'A',
        'explanation': 'Komplike ÜSE tanımı; tedavi başarısızlığına, dirençli suşlara veya doku hasarına zemin hazırlayan anatomik (taş, obstrüksiyon, darlık), fonksiyonel (nörojenik mesane, VUR) veya metabolik/konak faktörlerini (erkek cinsiyet, gebelik, diyabet, immünsüpresyon, kateterizasyon) ifade eder. Ateş yüksekliği sistemik tutulumu (örneğin akut piyelonefriti) gösteren bir semptomdur; tek başına anatomik/yapısal bir \'komplike edici zemin\' faktörü değildir. Genç, gebe olmayan, anatomik kusuru bulunmayan bir kadında gelişen piyelonefrit \'akut komplike olmayan piyelonefrit\' olarak adlandırılır.'
    },
    'q_relapse_reinfection': {
        'id': 'd3-k1-enf-050',
        'examYear': '2022-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Enfeksiyon Hastalıkları',
        'topic': 'Tekrarlayan İYE: Relaps vs Reenfeksiyon Ayrımı',
        'stem': 'Başarılı bir antibakteriyel tedavi bitiminden 2 hafta sonra veya aylar içinde farklı bir bakteri suşu ile yeniden üriner sistem enfeksiyonu gelişmesine ne ad verilir?',
        'options': [
            {'key': 'A', 'text': 'Ko-enfeksiyon'},
            {'key': 'B', 'text': 'Reenfeksiyon', 'isCorrect': True},
            {'key': 'C', 'text': 'Bakteriyel persistans (Relaps)'},
            {'key': 'D', 'text': 'Süperenfeksiyon'},
            {'key': 'E', 'text': 'Asemptomatik bakteriüri'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Tekrarlayan İYE ikiye ayrılır: 1) Reenfeksiyon: Tedavi bitiminden >2 hafta sonra genellikle FARKLI bir bakteriyle (veya aynı bakterinin farklı suşuyla) dış ortamdan/bağırsaktan yeniden bulaşma sonucu gelişir (tekrarlayan olguların %80-90\'ı böyledir). 2) Relaps (Bakteriyel persistans): Tedavi bitiminden sonraki İLK 2 HAFTA İÇİNDE, AYNI bakteriyle nükseder; böbrek taşı, kaval enfekte odak, prostatit veya yetersiz tedavi süresine bağlıdır.'
    },
    'q_asb_definition': {
        'id': 'd3-k1-enf-046',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Enfeksiyon Hastalıkları',
        'topic': 'Asemptomatik Bakteriüri Tanımı ve Kass Kriteri',
        'stem': 'Üriner enfeksiyon semptomu bulunmayan bir kişide, uygun şartlarda birer gün arayla alınan iki ardışık orta akım idrar kültüründe aynı üropatojenin en az kaç CFU/mL düzeyinde saptanması \'Asemptomatik Bakteriüri\' olarak tanımlanır?',
        'options': [
            {'key': 'A', 'text': '≥ 10^2 CFU/mL'},
            {'key': 'B', 'text': '≥ 10^3 CFU/mL'},
            {'key': 'C', 'text': '≥ 10^4 CFU/mL'},
            {'key': 'D', 'text': '≥ 10^5 CFU/mL', 'isCorrect': True},
            {'key': 'E', 'text': '≥ 10^7 CFU/mL'}
        ],
        'correctAnswer': 'D',
        'explanation': 'Asemptomatik Bakteriüri (ASB); hastada dizüri, polaküri, ateş gibi hiçbir enfeksiyon semptomu yokken, temiz orta akım idrarında ≥10^5 CFU/mL (kob/mL) konsantrasyonda saf bakteri üremesidir. Kadınlarda kontaminasyonu dışlamak için birer gün arayla alınmış 2 ardışık kültürde aynı bakterinin ≥10^5 üremesi şartı aranır; erkeklerde ise tek bir örnekte ≥10^5 üreme tanı koydurur.'
    },
    'q_asb_indications': {
        'id': 'd3-k1-enf-040',
        'examYear': '2022-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Kadın Doğum',
        'topic': 'Asemptomatik Bakteriüride Kesin Tedavi Endikasyonları',
        'stem': 'Aşağıdaki klinik durumların hangisinde saptanan asemptomatik bakteriüri için MUTLAK tarama ve antibakteriyel tedavi endikasyonu vardır?',
        'options': [
            {'key': 'A', 'text': 'Diabetes Mellitus tanılı yaşlı kadın'},
            {'key': 'B', 'text': 'Gebelik', 'isCorrect': True},
            {'key': 'C', 'text': 'Kalıcı üretral sonda takılı yatalak hasta'},
            {'key': 'D', 'text': 'Aralıklı temiz kateterizasyon (TAK) uygulayan nörojen mesaneli hasta'},
            {'key': 'E', 'text': 'Premenopozal asemptomatik sağlıklı kadın'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Asemptomatik bakteriüri genel popülasyonda (diyabetik kadınlar, yaşlılar, kateterli bireyler, omurilik felçlileri) kesinlikle taranmaz ve tedavi EDİLMEZ (tedavi edilmesi dirençli süperenfeksiyonlara yol açar). Ancak iki hasta grubunda ASB mutlak taranır ve tedavi edilir: 1) GEBELER (tedavi edilmezse %20-40 akut piyelonefrit, düşük doğum ağırlığı ve preterm eyleme yol açar), 2) Mukoza kanamasına yol açabilecek İNVAZİV ÜROLOJİK GİRİŞİM yapılacak hastalar (TUR-P, endoüroloji öncesi sepsis riski nedeniyle).'
    },
    'q_culture_indications': {
        'id': 'd3-k1-uro-013',
        'examYear': '2023-2026',
        'committeeId': 'Kurul 1',
        'discipline': 'Üroloji / Enfeksiyon',
        'topic': 'İdrar Kültürü Endikasyonları ve Basit Sistit Yönetimi',
        'stem': 'Aşağıdaki klinik tablolardan hangisinde semptomatik ampirik tedavi öncesinde kantitatif idrar kültürü yapılması MUTLAK ŞART DEĞİLDİR?',
        'options': [
            {'key': 'A', 'text': 'Akut piyelonefrit şüphesi olan hastalar'},
            {'key': 'B', 'text': 'Tüm gebe kadınlarda asemptomatik veya semptomatik durumlar'},
            {'key': 'C', 'text': 'Genç, gebe olmayan, sağlıklı kadınlarda izlenen akut komplike olmayan sistit', 'isCorrect': True},
            {'key': 'D', 'text': 'Diyabetik veya immünsüprese hastalarda gelişen İYE'},
            {'key': 'E', 'text': 'Ateşli üriner enfeksiyon geçiren erkek veya çocuk hastalar'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Genç, gebe olmayan, anatomik kusuru bulunmayan sağlıklı kadınlarda gelişen tipik akut sistitte (dizüri, sık idrar, aciliyet) etken %80-90 UPEC olduğundan rutin idrar kültürü yapılmasına gerek yoktur; ampirik fosfomisin veya nitrofurantoin başlanması yeterlidir. Ancak piyelonefrit şüphesinde, gebelerde, erkeklerde, çocuklarda, refrakter nükslerde ve komplike İYE\'lerde kültür mutlak şarttır.'
    },
    'q_nitrofurantoin_pharma': {
        'id': 'd3-k3-far-010',
        'examYear': '2023-2026',
        'committeeId': 'Kurul 1 & Kurul 3',
        'discipline': 'Tıbbi Farmakoloji / Üroloji',
        'topic': 'Nitrofurantoin Farmakolojisi, Spektrumu ve Kısıtlılıkları',
        'stem': 'Komplike olmayan alt üriner sistem enfeksiyonlarında (sistit) birinci basamak oral ajan olarak kullanılan Nitrofurantoin ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?',
        'options': [
            {'key': 'A', 'text': 'Pseudomonas aeruginosa ve Proteus mirabilis enfeksiyonlarında ilk seçenektir'},
            {'key': 'B', 'text': 'Akut piyelonefrit ve renal parankim enfeksiyonlarında çok yüksek doku konsantrasyonu sağlar'},
            {'key': 'C', 'text': 'Kreatinin klirensi <30-60 mL/dk olan böbrek yetmezlikli hastalarda idrara geçemez ve sistemik toksisite riski nedeniyle kontrendikedir', 'isCorrect': True},
            {'key': 'D', 'text': 'İdrar pH\'sı aşırı alkali olduğunda antibakteriyel etkinliği belirgin şekilde artar'},
            {'key': 'E', 'text': 'Gebelikte hiçbir trimesterde kullanılamayan X kategorisi bir ilaçtır'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Nitrofurantoin serumda ve böbrek parankiminde terapötik düzeye ulaşmaz; glomerüler filtrasyonla hızla idrara atılarak mesanede konsantre olur. Bu yüzden piyelonefritte ve ürosepsiste KULLANILMAZ. GFR < 30-60 mL/dk olduğunda idrara süzülemez, idrar konsantrasyonu yetersiz kalır ve serumda birikerek periferik nöropati yapar; bu nedenle böbrek yetmezliğinde kontrendikedir. Asidik idrarda etkinliği artar. Proteus ve Pseudomonas türleri nitrofurantoine doğal olarak dirençlidir.'
    }
}

# The 21 Structured Slides matching Dr. Özer Baran's 87-page lecture note
slides_batch3 = [
    # Slide 1
    {
        'slideNumber': 1,
        'title': 'Üriner Sistem Enfeksiyonları: Tanım ve Giriş',
        'subtitle': 'Üriner traktusun anatomik kompartmanları ve bakteriyel invazyon kavramı',
        'badge': 'Giriş & Tanım',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Resmi ders notuna göre **Üriner Sistem Enfeksiyonu (ÜSE)**; üretra meatusundan böbrek parankimine kadar üriner traktusun herhangi bir anatomik yapısının mikroorganizmalar (özellikle bakteriler) tarafından kolonize edilmesi ve doku invazyonu sonucu ortaya çıkan klinik tablodur. ÜSE terimi hem alt üriner sistemi (üretra, mesane, prostat) hem de üst üriner sistemi (üreter, toplayıcı sistem, böbrek parankimi) kapsayan şemsiye bir ifadedir. Normal şartlarda üretra distali hariç tüm üriner traktus ve idrar sterildir. Enfeksiyonun gelişmesi; patojen mikroorganizmanın virülansı ile konağın anatomik, immünolojik ve fizyokimyasal savunma mekanizmaları arasındaki dengenin bozulmasına dayanır.',
        'flashcards': [
            {
                'id': 'uti-fc-01-01',
                'category': 'Temel Tanım',
                'front': 'Resmi ders notuna göre Üriner Sistem Enfeksiyonunun (ÜSE) tıbbi tanımı nedir?',
                'hint': 'Üriner yapıların mikrobiyal durumu.',
                'back': 'Üriner traktusun bir veya birden fazla anatomik yapısının (üretra, mesane, üreter, böbrek) mikroorganizmalar (çoğunlukla bakteriler) tarafından invazyonu ve buna bağlı inflamatuvar reaksiyon gelişmesidir.'
            },
            {
                'id': 'uti-fc-01-02',
                'category': 'Sterilite Kuralı',
                'front': 'Fizyolojik şartlarda üriner traktusun hangi anatomik seviyesi fizyolojik kommensal flora barındırır?',
                'hint': 'Dış ortama açılan distal bölüm.',
                'back': 'Yalnızca **üretra distal 1/3\'lük kısmı ve meatus çevresi** kommensal cilt/perineal flora ile kolonizedir; mesane lümeni, üreterler ve böbrekler normalde tamamen sterildir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Şemsiye Terim',
                    'desc': 'ÜSE; üretrit, sistit, prostatit ve akut piyelonefriti kapsayan genel anatomik bir ifadedir.',
                    'isKey': True
                },
                {
                    'title': 'Bakteriyel İnvazyon',
                    'desc': 'Üriner traktusta bakterilerin sadece varlığı değil, mukozal adhezyon ve doku yanıtı oluşturması esastır.',
                    'isKey': True
                },
                {
                    'title': 'Klinik Spektrum',
                    'desc': 'Asemptomatik bakteriüriden hayatı tehdit eden ürosepsise kadar çok geniş bir ağırlık aralığı gösterir.'
                }
            ],
            'table': {
                'title': 'Ders Notu: Üriner Sistem Enfeksiyonlarının Anatomik Dağılımı',
                'headers': ['Anatomik Bölge', 'Spesifik Klinik Tablo', 'Etkilenen Temel Organlar', 'Karakteristik Klinik İpucu'],
                'rows': [
                    ['Alt Üriner Sistem', 'Akut Sistit', 'Mesane mukozası (Ürotelyum)', 'Dizüri, polaküri, sıkışma, suprapubik ağrı (ateş yoktur)'],
                    ['Alt Üriner Sistem', 'Akut Üretrit', 'Üretra epiteli', 'Üretral akıntı, meatal yanma (sıklıkla CYBH etkenleri)'],
                    ['Alt Üriner Sistem', 'Akut Prostatit', 'Prostat glandı asinüsleri', 'Pelvik ağrı, disüri, rektal tuşede aşırı hassas ödemli prostat'],
                    ['Üst Üriner Sistem', 'Akut Piyelonefrit', 'Renal pelvis, kaliksler ve parankim', 'Yüksek ateş, titreme, yan ağrısı ve kostovertebral açı hassasiyeti (KVAH)']
                ]
            }
        },
        'spotPearls': [
            'Normal idrar ve üst üriner traktus fizyolojik olarak sterildir; yalnızca distal üretra kolonizedir.',
            'Alt üriner sistem enfeksiyonlarında (sistit) tipik olarak sistemik ateş izlenmez; ateş varlığı parankimal tutulumu (piyelonefrit/prostatit) gösterir.',
            'ÜSE insanların hekime başvurmasına en sık yol açan bakteriyel enfeksiyon grubudur.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Alt ve üst üriner sistem enfeksiyonları klinik olarak nasıl ayrılır?',
            'Üriner sistemde hangi anatomik bölge normalde floraya sahiptir?'
        ]
    },

    # Slide 2
    {
        'slideNumber': 2,
        'title': 'Epidemiyoloji ve Yaş-Cinsiyet Dinamikleri',
        'subtitle': 'ABD verileri, kadın üstünlüğü ve neonatal dönem istisnası',
        'badge': 'Epidemiyoloji',
        'badgeColor': 'blue',
        'synthesisNarrative': 'Ders notuna göre (Sayfa 3-6) ÜSE, toplumda hekime başvuru gereksinimi yaratan en sık bakteriyel enfeksiyondur. ABD\'de her yıl 7 milyondan fazla ÜSE atağı görülmekte ve bu hastaların %21\'i doğrudan acil servise başvurmaktadır. Tanı alan hastaların **%67.5\'i kadındır**. Kadınların **%50\'si yaşamları boyunca en az bir kez** ÜSE geçirir. Ancak yaş ve cinsiyet insidansında çok kritik bir kurul sınavı detayı vardır: **Neonatal dönemde ÜSE erkek bebeklerde daha sıktır (Erkek/Kız oranı: 1.5/1)**. Bunun nedeni doğumsal üriner anomalilerin erkeklerde daha sık görülmesi ve sünnetsiz prepusyum kolonizasyonudur. 1 yaşından 50 yaşına kadar kadınlarda ezici bir üstünlük görülürken, **50 yaşından sonra Benign Prostat Hiperplazisi (BPH)** ve obstrüksiyona bağlı olarak erkeklerde sıklık yeniden dramatik şekilde artar.',
        'flashcards': [
            {
                'id': 'uti-fc-02-01',
                'category': 'Epidemiyoloji',
                'front': 'Hangi yaşam döneminde ÜSE erkeklerde kız çocuklarına göre daha sık görülür (Erkek/Bayan: 1.5/1)?',
                'hint': 'Doğumdan hemen sonraki ilk haftalar.',
                'back': '**Neonatal Dönem (Yenidoğan Dönemi)**. Doğumsal ürogenital anomaliler ve sünnetsiz prepusyum kolonizasyonu nedeniyle yenidoğanda ÜSE erkeklerde 1.5 kat daha sıktır.'
            },
            {
                'id': 'uti-fc-02-02',
                'category': 'Cinsiyet Dağılımı',
                'front': 'Erkeklerde 50 yaşından sonra ÜSE insidansının aniden artmasının temel patofizyolojik nedeni nedir?',
                'hint': 'Prostat büyümesi ve infravezikal obstrüksiyon.',
                'back': '**Benign Prostat Hiperplazisi (BPH)** ve buna bağlı gelişen infravezikal çıkım obstrüksiyonu, mesanede rezidüel idrar birikmesi ve idrar akım dinamiklerinin bozulmasıdır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Yaşam Boyu Kadın Riski',
                    'desc': 'Kadınların %50\'si hayatında en az bir kez ÜSE geçirir; hastaların %67.5\'i kadındır.',
                    'isKey': True
                },
                {
                    'title': 'Neonatal Erkek İstisnası (Sayfa 6)',
                    'desc': 'Yenidoğan döneminde erkek/kız oranı 1.5/1 ile erkek lehinedir (en klasik sınav sorusu!).',
                    'isKey': True
                },
                {
                    'title': '50 Yaş Dönüm Noktası',
                    'desc': '50 yaş sonrası erkekte BPH obstrüksiyonu nedeniyle cinsiyetler arası insidans farkı kapanır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 6: Yaşam Dönemlerine Göre ÜSE Prevalansı ve Cinsiyet Dağılımı',
                'headers': ['Yaşam Dönemi', 'Tahmini Prevalans', 'Erkek / Kadın Oranı', 'Baskın Etyopatogenetik Faktör'],
                'rows': [
                    ['Neonatal Dönem', '%1', '1.5 / 1 (Erkek > Kız)', 'Doğumsal anomaliler, prepusyum kolonizasyonu'],
                    ['1 - 5 Yaş (Çocukluk)', '%1 - 3', '1 / 10 (Kız >> Erkek)', 'Kısa üretra, tuvalet eğitimi, VUR'],
                    ['Doğurganlık Çağı (15-50 yaş)', '%2 - 5', '1 / 30 - 50 (Kadın ezici üstünlük)', 'Cinsel ilişki, kısa üretra, vajinal anatomi'],
                    ['İleri Yaş (>60 yaş)', '%10 - 20', '1 / 2 (Fark belirgin azalır)', 'Erkekte BPH obstrüksiyonu, kadında östrojen kaybı']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 6: ÜSE insidansının erkeklerde kadınlardan yüksek olduğu TEK dönem neonatal (yenidoğan) dönemdir.',
            'Kadınların anatomik olarak kısa üretraya (3-4 cm) sahip olması ve meatusun anüse yakınlığı enfeksiyon sıklığının ana nedenidir.',
            'Kadınlarda yaşam boyu ÜSE geçirme riski %50 iken, hastaların yaklaşık üçte birinde tekrarlayan ataklar görülür.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Yenidoğanda ÜSE neden erkeklerde daha sıktır?',
            'Yaşla birlikte erkek ve kadın ÜSE oranları nasıl değişir?'
        ]
    },

    # Slide 3
    {
        'slideNumber': 3,
        'title': 'Risk Faktörleri ve Predispozan Nedenler',
        'subtitle': 'Kateterizasyon, obstrüksiyon, sistemik hastalıklar ve pre/postmenopozal dinamikler',
        'badge': 'Risk Faktörleri',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 8-11) ÜSE gelişimine zemin hazırlayan predispozan faktörler lokal ve sistemik olarak ikiye ayrılır: **1) Sistemik Faktörler**: Diabetes mellitus (nöropati ve lökosit disfonksiyonu), immünsüpresyon, malnütrisyon. **2) Lokal Faktörler**: Organik veya fonksiyonel obstrüksiyon (taş, tümör, üretral darlık), vezikoüreteral reflü (VUR) ve **üretral kateterizasyon** (nozokomiyal İYE\'lerin %80\'inden sorumludur; kateter kaldığı her gün enfeksiyon riski %3-7 artar). Kadınlarda premenopozal dönemde en önemli risk faktörleri **cinsel ilişki sıklığı, spermisid kullanımı ve genetik yatkınlık (Lewis kan grubu non-sekretör fenotipi)** iken; postmenopozal dönemde **östrojen eksikliği** sonucu vajinal laktobasillerin kaybolması ve vajen pH\'sının bazikleşmesidir. Erkeklerde <50 yaşta **sünnet olmama**, >50 yaşta **prostat büyümesi** öne çıkar.',
        'flashcards': [
            {
                'id': 'uti-fc-03-01',
                'category': 'Risk Faktörleri',
                'front': 'Premenopozal genç kadınlarda ÜSE gelişimini en çok tetikleyen 2 davranışsal ve korunma faktörü nedir?',
                'hint': 'Sayfa 10: Cinsel aktivite ve kontrasepsiyon.',
                'back': '1) **Cinsel ilişki (koit)** sıklığı (balayı sistiti)\n2) **Spermisid kullanımı** (normal koruyucu vajinal florayı yok ederek UPEC kolonizasyonunu kolaylaştırır).'
            },
            {
                'id': 'uti-fc-03-02',
                'category': 'Postmenopozal Mekanizma',
                'front': 'Postmenopozal kadınlarda östrojen kaybı hangi mekanizmayla ÜSE riskini katlar?',
                'hint': 'Vajinal glikojen, laktobasil ve vajen pH ilişkisi.',
                'back': 'Östrojen eksikliği -> Vajen epitelinde glikojen azalır -> Koruyucu **Laktobasiller kaybolur** -> Vajen pH\'sı alkaliye kayar (pH > 4.5) -> Enterobakteriler perineum ve üretrada kolayca kolonize olur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Üretral Kateterizasyon',
                    'desc': 'Hastanede kazanılan (nozokomiyal) ÜSE\'lerin %80\'inden sorumludur; biyofilm oluşumuna yol açar.',
                    'isKey': True
                },
                {
                    'title': 'Genetik Yatkınlık (Lewis Kan Grubu)',
                    'desc': 'Non-sekretör fenotipteki kadınların ürotelyumunda E. coli için daha fazla adezyon reseptörü bulunur.',
                    'isKey': True
                },
                {
                    'title': 'Sünnetin Koruyuculuğu (<50 yaş)',
                    'desc': 'Sünnetsiz erkeklerde prepusyumun iç yüzeyi UPEC için rezervuar oluşturarak riski artırır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 8-11: Cinsiyete ve Döneme Göre ÜSE Risk Faktörleri Matrisi',
                'headers': ['Popülasyon Grubu', 'Birincil Risk Faktörleri', 'Patofizyolojik Mekanizma'],
                'rows': [
                    ['Premenopozal Kadınlar', 'Cinsel ilişki, spermisid, yeni partner, anne öyküsü', 'Üretraya mekanik bakteri inokülasyonu, floranın bozulması'],
                    ['Postmenopozal Kadınlar', 'Östrojen eksikliği, sistosel, artık idrar, inkontinans', 'Laktobasil kaybı, vajinal atrofi, mesane tam boşalamaması'],
                    ['Genç Erkekler (<50 yaş)', 'Sünnet olmama, eşcinsel ilişki, üretral darlık', 'Prepusyal UPEC kolonizasyonu, retrograd yayılım'],
                    ['İleri Yaş Erkekler (>50 yaş)', 'BPH, üretral kateterizasyon, prostat taşları', 'İnfravezikal obstrüksiyon, yüksek rezidüel idrar hacmi'],
                    ['Tüm Hastalar (Genel)', 'Üriner taş, VUR, diabetes mellitus, kateter', 'Yabancı cisim reaksiyonu, nüks odağı, immün yetersizlik']
                ]
            }
        },
        'spotPearls': [
            'Nozokomiyal enfeksiyonların en sık nedeni üriner kateterlerdir; kateter takılı her gün bakteriüri riski %3-7 artar.',
            'Spermisid kullanımı vajinal koruyucu laktobasilleri öldürerek E. coli kolonizasyonunu 4-5 kat artırır.',
            'Diyabetik hastalarda hem lökosit kemotaksis kusuru hem de glikozüri bakteriyel proliferasyonu hızlandırır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_complicated_uti']],
        'aiPromptSuggestions': [
            'Spermisid kullanımı neden idrar yolu enfeksiyonu riskini artırır?',
            'Postmenopozal dönemde vajinal östrojen verilmesi enfeksiyonu nasıl engeller?'
        ]
    },

    # Slide 4
    {
        'slideNumber': 4,
        'title': 'Enfeksiyon Patogenezi ve Bulaş Yolları',
        'subtitle': 'Asendan (%99), hematojen (<%2) ve lenfatik yayılım mekanizmaları',
        'badge': 'Patogenez',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 12-14) mikroorganizmaların üriner sisteme ulaşmasında 3 anatomik yol tanımlanmıştır: **1) Asendan Yol (%99)**: En sık, en önemli ve klinik olguların neredeyse tamamını oluşturan yoldur. Fekal floradaki Enterobacteriaceae üyeleri perineal ve periüretral bölgeyi kolonize eder; kısa kadın üretrasından mesaneye tırmanır. Mesanede çoğalan bakteriler vezikoüreteral reflü veya tübüler motilite ile üreterler boyunca böbrek parankimine kadar yükselir. **2) Hematojen Yol (<%2)**: Nadirdir; vücudun başka bir odağındaki primer enfeksiyondan bakteriyemi ile böbrek korteksine mikroorganizma ekilmesiyle oluşur. Hematojen yolla en sık etken **Staphylococcus aureus bakteriyemisi** (endokardit, osteomiyelit kaynaklı renal abseler) ve **Mycobacterium tuberculosis**tir. Gram negatif basiller hematojen yolla böbreğe çok nadir oturur. **3) Lenfatik Yol**: Bağırsak ve genital organ lenfatikleri ile renal lenfatikler arasındaki bağlantılarla teorik olarak bildirilmiş olup klinik önemi ihmal edilebilir düzeydedir.',
        'flashcards': [
            {
                'id': 'uti-fc-04-01',
                'category': 'Patogenez',
                'front': 'Üriner sistem enfeksiyonlarının %99\'u hangi bulaş yoluyla gelişir?',
                'hint': 'Aşağıdan yukarıya tırmanan anatomik yol.',
                'back': '**Asendan (Yükselen) Yol (%99)**. Fekal kökenli enterik basillerin perineal bölgeden üretraya, oradan mesaneye ve üreterler aracılığıyla böbreğe tırmanmasıdır.'
            },
            {
                'id': 'uti-fc-04-02',
                'category': 'Hematojen Yol',
                'front': 'Hematojen yolla (<%2) böbrekte enfeksiyon ve abse oluşturan en tipik mikroorganizmalar hangileridir?',
                'hint': 'Gram negatif basiller değil, bir gram (+) kok ve bir asidorezistan basil.',
                'back': '**Staphylococcus aureus** (bakteriyemi, enfektif endokardit sonucu kortikal mikroabseler) ve **Mycobacterium tuberculosis** (renal tüberküloz).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Asendan Yolun Ezici Hakimiyeti (%99)',
                    'desc': 'Enterobacteriaceae ailesinin perineal kolonizasyonunu takiben retrograd tırmanışı.',
                    'isKey': True
                },
                {
                    'title': 'Hematojen Yolun Özgüllüğü (<%2)',
                    'desc': 'S. aureus sepsislerinde renal kortikal abse; M. tuberculosis ve Candida fungemisi.',
                    'isKey': True
                },
                {
                    'title': 'Lenfatik Yol',
                    'desc': 'Kolon ve mesane lenfatikleri arasında deneysel geçiş gösterilmiş ancak pratikte nadirdir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 12-14: ÜSE Bulaş Yolları Karşılaştırması',
                'headers': ['Bulaş Yolu', 'Görülme Oranı', 'En Sık Etken Mikroorganizmalar', 'Karakteristik Klinik Tablo'],
                'rows': [
                    ['Asendan (Yükselen) Yol', '%99 (En sık)', 'E. coli, Proteus, Klebsiella, Enterococcus', 'Sistit, asendan akut piyelonefrit'],
                    ['Hematojen (Hematojen yayılım)', '<%2 (Nadir)', 'Staphylococcus aureus, M. tuberculosis, Candida', 'Renal kortikal abse (karbunkül), tüberküloz, kandidüri'],
                    ['Lenfatik Yol', 'Çok nadir', 'Bilinmiyor / Polimikrobiyal', 'Şiddetli retroperitoneal cerrahi/obstrüksiyon durumları']
                ]
            }
        },
        'spotPearls': [
            'Gram negatif enterik basiller (E. coli vb.) hemen daima ASENDAN yolla gelir; hematojen yolla İYE yapmazlar.',
            'İdrar kültüründe saf Staphylococcus aureus üremesi aksi kanıtlanana kadar bir bakteriyemi / enfektif endokardit odağını düşündürmelidir.',
            'Kadın üretrasının anatomik kısalığı (3-4 cm) asendan bulaşın temel fiziksel nedenidir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Hematojen yolla gelişen böbrek enfeksiyonlarında en sık etken nedir?',
            'Asendan yolun aşamaları nelerdir?'
        ]
    },

    # Slide 5
    {
        'slideNumber': 5,
        'title': 'Konağın Savunma Mekanizmaları',
        'subtitle': 'İdrar akımı, üromodulin, ozmolarite, GAG tabakası ve mukozal immünite',
        'badge': 'Konak Savunması',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Ders notuna göre (Sayfa 15) üriner traktus mikroorganizma invazyonuna karşı çok katmanlı savunma bariyerlerine sahiptir: **1) İdrar Akımı ve Miksiyon**: Konağın en güçlü ve en birincil mekanik savunmasıdır; idrarın düzenli olarak dışarı atılması bakterilerin ürotelyuma tutunmasına fırsat vermeden onları mekanik olarak yıkar ve dışarı atar. Rezidüel idrar kalması bu savunmayı felç eder. **2) İdrarın Fizyokimyasal Özellikleri**: Aşırı yüksek ozmolarite, yüksek üre konsantrasyonu ve asidik idrar pH\'sı birçok bakterinin çoğalmasını inhibe eder. **3) Mukozal Glikozaminoglikan (GAG) Tabakası**: Mesane ürotelyumunu bir örtü gibi sararak bakterilerin epitel hücre reseptörlerine doğrudan temasını fiziksel olarak engeller. **4) Tamm-Horsfall Proteini (Uromodulin)**: Henle kulpu çıkan kolunda üretilir; üzerinde bol miktarda mannoz kalıntısı taşır. Bakterilerin Tip 1 fimbriyalarını adeta bir tuzak gibi kendine bağlayarak bakterinin mesane epitelindeki mannoza tutunmasını engeller ve idrarla atılmasını sağlar. **5) Mukozal Salgısal IgA ve PMN Lökositler**.',
        'flashcards': [
            {
                'id': 'uti-fc-05-01',
                'category': 'Konak Savunması',
                'front': 'Konağın üriner sistemdeki EN ÖNEMLİ ve birincil mekanik savunma mekanizması nedir?',
                'hint': 'Mesanenin periyodik boşalması.',
                'back': '**İdrar akımı ve düzenli miksiyon**. Bakterilerin mesane duvarına yapışmasını engelleyerek lümendeki mikroorganizmaları mekanik yıkama (washout) etkisiyle dışarı atar.'
            },
            {
                'id': 'uti-fc-05-02',
                'category': 'Moleküler Savunma',
                'front': 'Tamm-Horsfall proteini (uromodulin) E. coli bakterisini nasıl etkisiz hale getirir?',
                'hint': 'Mannoz tuzak mekanizması.',
                'back': 'Uromodulin bol miktarda **mannoz** içerir. E. coli\'nin Tip 1 fimbriyaları mesane epiteli yerine uromodulindeki mannoza bağlanır; bakteri yakalanarak idrar akımıyla atılır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Mekanik Yıkama (Washout)',
                    'desc': 'Normal miksiyon bakteriyel inokülümü seyreltir ve mesaneden temizler.',
                    'isKey': True
                },
                {
                    'title': 'Tamm-Horsfall Proteini (Uromodulin)',
                    'desc': 'Tip 1 fimbriyayı bağlayan fizyolojik anti-adhezyon tuzağıdır.',
                    'isKey': True
                },
                {
                    'title': 'Mukozal GAG Bariyeri',
                    'desc': 'Ürotelyumu kaplayan anti-adherent bariyer bakteriyel teması engeller.',
                    'isKey': True
                },
                {
                    'title': 'İdrar Kimyası',
                    'desc': 'Yüksek üre, yüksek ozmolarite ve asit pH bakterisidal / bakteriyostatik etki gösterir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 15: Konağın Üriner Savunma Katmanları',
                'headers': ['Savunma Seviyesi', 'Bileşen / Mekanizma', 'İnhibe Edici Fonksiyonu'],
                'rows': [
                    ['Mekanik', 'Miksiyon / İdrar Akımı', 'Bakterilerin tutunmasını önleme ve dışarı süpürme'],
                    ['Kimyasal / Çözünür', 'Tamm-Horsfall Proteini (Uromodulin)', 'Mannoz reseptör taklidi ile Tip 1 pilileri bağlama'],
                    ['Fizyokimyasal', 'Yüksek üre + hiperozmolarite + düşük pH', 'Bakteriyel replikasyonu ve metabolizmayı baskılama'],
                    ['Anatomik / Epitelyal', 'Ürotelyal Glikozaminoglikan (GAG) Örtüsü', 'Epitel yüzeyini örterek adhezyon alanlarını maskeleme'],
                    ['İmmünolojik', 'Sekretuvar IgA ve Lökosit Yanıtı', 'Opsonizasyon, nötralizasyon ve lokal fagositoz']
                ]
            }
        },
        'spotPearls': [
            'Mesanede rezidüel idrar kalması idrar akımının mekanik süpürme (washout) etkisini sıfırlar.',
            'Tamm-Horsfall proteini insan idrarında en bol bulunan fizyolojik proteindir ve doğal bir UPEC tuzağıdır.',
            'Vajinal floradaki Lactobacillus türleri ürettikleri laktik asit ve hidrojen peroksit ile patojenlerin üretraya tırmanmasını bloke eder.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Konağın idrar yolu savunma mekanizmaları nelerdir?',
            'Uromodulin bakteriyel adhezyonu nasıl engeller?'
        ]
    },

    # Slide 6
    {
        'slideNumber': 6,
        'title': 'Bakteriyel Virülans Faktörleri: Tip 1 ve P Fimbriya',
        'subtitle': 'Mannoz duyarlı sistit adezyonu vs Mannoz dirençli pyelonefrit adezyonu',
        'badge': 'Virülans Faktörleri',
        'badgeColor': 'purple',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 16) Üropatojenik Escherichia coli (UPEC) suşlarını fekal kommensal E. coli suşlarından ayıran en önemli özellik **artmış virülans faktörleri ve spesifik adhezinleridir**. En kritik virülans faktörleri fimbriyalardır (pili): **1) Tip 1 Fimbriya (Mannoz Duyarlı)**: Bakteri ucundaki FimH proteini ürotelyum yüzeyindeki mannozillenmiş üroplakin reseptörlerine bağlanır. Bu bağlanma ekzojen mannoz verilmesiyle inhibe edilebildiği için \'mannoza duyarlı\' adını alır. **Akut sistit patogenezinden sorumludur**; mesane mukozasına tutunmayı sağlar. **2) P Fimbriya (Pyelonefrit İlişkili Pili / PapG - Mannoz Dirençli)**: Böbrek toplayıcı tübül ve renal pelvis epiteli ile eritrositlerin P kan grubu antijeni üzerinde bulunan **alfa-D-galaktozil-(1-4)-beta-D-galaktozid (Gal-Gal)** reseptörlerine yüksek afiniteyle bağlanır. Mannoz ile bloke edilemez (\'mannoza dirençli\'). **Akut piyelonefrit patogenezinden sorumlu EN TEMEL virülans faktörüdür!** Diğer faktörler: Kapsül (K antijeni - fagositozu önler), Hemolizin (doku nekrozu yapar), Aerobaktin (demir bağlar) ve LPS (endotoksin).',
        'flashcards': [
            {
                'id': 'uti-fc-06-01',
                'category': 'P Fimbriya',
                'front': 'UPEC suşlarında akut piyelonefrit oluşumundan ve renal tübül tutulumundan sorumlu mannoz-dirençli adhezin hangisidir?',
                'hint': 'Böbrekteki Gal-Gal reseptörlerine bağlanan pili.',
                'back': '**P Fimbriya (Pap pili)**. Renal tübül hücreleri yüzeyindeki Gal-Gal (galaktozil-galaktozit) reseptörlerine bağlanarak bakterinin idrar akımına karşı böbreğe tutunmasını ve piyelonefrit yapmasını sağlar.'
            },
            {
                'id': 'uti-fc-06-02',
                'category': 'Tip 1 Fimbriya',
                'front': 'Akut sistit gelişiminde mesane ürotelyumundaki üroplakinlere bağlanan mannoz-duyarlı virülans yapısı nedir?',
                'hint': 'FimH adhezini taşıyan yüzey uzantısı.',
                'back': '**Tip 1 Fimbriya**. Mannoz duyarlıdır; mesane ürotelyumuna yapışmayı sağlar ve sistit gelişiminde birincil rol oynar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Tip 1 Fimbriya (Sistit)',
                    'desc': 'Mannoza duyarlıdır; mesane yüzeyindeki üroplakinlere tutunarak sistit başlatır.',
                    'isKey': True
                },
                {
                    'title': 'P Fimbriya (Piyelonefrit - Sınav Sorusu!)',
                    'desc': 'Mannoza dirençlidir; böbrek parankimindeki Gal-Gal reseptörlerine bağlanır ve piyelonefrit yapar.',
                    'isKey': True
                },
                {
                    'title': 'K Kapsül Antijeni',
                    'desc': 'Kompleman aracılı litik aktiviteyi ve nötrofil fagositozunu engeller.',
                    'isKey': True
                },
                {
                    'title': 'Hemolizin ve Aerobaktin',
                    'desc': 'Hemolizin tübül hücrelerini parçalar; aerobaktin demir şelasyonu yaparak bakteriyi besler.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 16: UPEC Fimbriya Tipleri Karşılaştırması (Kritik Kurul Tablosu)',
                'headers': ['Özellik', 'Tip 1 Fimbriya', 'P Fimbriya (Pap)'],
                'rows': [
                    ['Mannoz Duyarlılığı', 'Mannoz Duyarlı (Mannozla inhibe olur)', 'Mannoz Dirençli (Mannozla inhibe olmaz)'],
                    ['Bağlandığı Reseptör', 'Üroplakin IA ve IB (Mannoz kalıntıları)', 'Gal-Gal (alfa-Gal-(1-4)-beta-Gal)'],
                    ['Baskın Olduğu Bölge', 'Mesane Ürotelyumu', 'Böbrek Toplayıcı Tübül ve Parankim'],
                    ['Neden Olduğu Tablo', 'Akut Komplike Olmayan Sistit', 'Akut Piyelonefrit ve Ürosepsis'],
                    ['UPEC Suşlarında Sıklık', 'Sistit suşlarının %90\'ında', 'Piyelonefrit suşlarının >%80\'inde']
                ]
            }
        },
        'spotPearls': [
            'Piyelonefrit suşlarında P fimbriya varlığı %80\'in üzerindedir; sistit suşlarında ise Tip 1 fimbriya baskındır.',
            'Kranberi (turna yemişi) içeriğindeki proantosiyanidinler, bakterilerin P fimbriyalarını bloke ederek adhezyonu azaltır.',
            'Bakteriyel LPS (endotoksin) üreteral peristaltizmi paralize ederek bakterinin böbreğe asendan tırmanışını kolaylaştırır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'P fimbriya ile Tip 1 fimbriya arasındaki farklar nelerdir?',
            'UPEC virülans faktörleri nasıl etki gösterir?'
        ]
    },

    # Slide 7
    {
        'slideNumber': 7,
        'title': 'Mikrobiyolojik Etkenler: Komplike Olmayan vs Komplike Spektrum',
        'subtitle': 'UPEC hakimiyeti, S. saprophyticus, Proteus, Klebsiella ve nozokomiyal patojenler',
        'badge': 'Mikrobiyoloji',
        'badgeColor': 'indigo',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 17-18) ÜSE etkenleri enfeksiyonun kazanıldığı ortama (toplum kökenli vs nozokomiyal) ve konak yapısına (komplike olmayan vs komplike) göre belirgin farklılık gösterir. **1) Akut Komplike Olmayan İYE**: Tek bir mikroorganizma sorumludur (%95). Açık ara en sık etken **Escherichia coli\'dir (%75 - 90)**. İkinci sırada genç, cinsel yönden aktif kadınlarda görülen koagülaz-negatif bir stafilokok olan **Staphylococcus saprophyticus (%5 - 15)** yer alır. Kalan olgularda Klebsiella pneumoniae, Proteus mirabilis ve Enterococcus faecalis görülür. **2) Komplike ve Nozokomiyal İYE**: E. coli oranı **%30 - 50\'ye** geriler! Çoklu antibiyotik direnci gösteren hastane patojenleri ön plana çıkar: **Proteus mirabilis** (üreaz üretir, strüvit taşı yapar), **Pseudomonas aeruginosa** (kateterli hastalarda tipik), **Klebsiella pneumoniae**, **Enterobacter**, **Serratia**, **Enterococcus faecalis/faecium** ve fungal etken olarak **Candida albicans**.',
        'flashcards': [
            {
                'id': 'uti-fc-07-01',
                'category': 'Mikrobiyoloji',
                'front': 'Genç, cinsel aktif kadınlarda akut komplike olmayan sistitte E. coli\'den sonra ikinci en sık etken nedir?',
                'hint': 'Novobiyosine dirençli koagülaz negatif stafilokok.',
                'back': '**Staphylococcus saprophyticus (%5-15)**. Cinsel aktif genç kadınlarda balayı sistitinin E. coli\'den sonraki ikinci en sık nedenidir.'
            },
            {
                'id': 'uti-fc-07-02',
                'category': 'Komplike Patojenler',
                'front': 'Komplike veya kateter ilişkili nozokomiyal İYE\'lerde E. coli sıklığı azalırken hangi dirençli bakterilerin oranı artar?',
                'hint': 'Sayfa 17: Dört temel nozokomiyal bakteri.',
                'back': '**Pseudomonas aeruginosa, Proteus mirabilis, Klebsiella pneumoniae, Serratia ve Enterococcus faecalis** (ayrıca Candida türleri).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'E. coli Mutlak Hakimiyeti',
                    'desc': 'Toplum kökenli sistit ve piyelonefritlerin %75-90\'ından UPEC sorumludur.',
                    'isKey': True
                },
                {
                    'title': 'Staph. saprophyticus Sıklığı',
                    'desc': 'Cinsel yönden aktif genç kadınlarda %15\'e varan oranda ikinci sıradadır.',
                    'isKey': True
                },
                {
                    'title': 'Nozokomiyal İYE\'de Spektrum Kayması',
                    'desc': 'E. coli %30-50\'ye düşer; Pseudomonas, Proteus ve Enterokoklar belirgin artar.',
                    'isKey': True
                },
                {
                    'title': 'Monobakteriyel Doğa',
                    'desc': 'Akut komplike olmayan İYE\'lerin %95\'inde tek bir mikrobiyal etken izole edilir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 17-18: İYE Tiplerine Göre Mikrobiyolojik Etken Dağılımı',
                'headers': ['Patojen Mikroorganizma', 'Komplike Olmayan İYE Oranı', 'Komplike / Nozokomiyal İYE Oranı', 'Öne Çıkan Klinik Özellik'],
                'rows': [
                    ['Escherichia coli (UPEC)', '%75 - 90 (En sık)', '%30 - 50', 'Fimbriyalarıyla ürotelyuma tutunur'],
                    ['Staphylococcus saprophyticus', '%5 - 15', '< %2', 'Genç cinsel aktif kadınlarda 2. sırada'],
                    ['Klebsiella pneumoniae', '%2 - 5', '%10 - 15', 'Mukoid kapsüllü, nozokomiyal dirençli'],
                    ['Proteus mirabilis', '%2 - 4', '%10 - 15', 'Üreaz pozitif, strüvit/magnezyum amonyum taşı'],
                    ['Pseudomonas aeruginosa', '< %1', '%10 - 20', 'Kalıcı kateter, enstrümantasyon, yüksek direnç'],
                    ['Enterococcus faecalis', '%1 - 2', '%5 - 10', 'Gram (+) kok, ampisiline duyarlı / VRE riski'],
                    ['Candida albicans', '< %0.1', '%5 - 10', 'Geniş spektrumlu antibiyotik, diyabet, kateter']
                ]
            }
        },
        'spotPearls': [
            'Toplum kökenli basit sistitte etken %80-90 E. coli olduğu için rutin kültür yapılmadan ampirik tedavi verilebilir.',
            'Staphylococcus saprophyticus novobiyosine dirençlidir ve koagülaz negatiftir.',
            'Proteus enfeksiyonlarında idrar daima alkalidir (pH > 7.2) ve strüvit taşı riski çok yüksektir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Komplike ve komplike olmayan İYE etkenleri nasıl farklılaşır?',
            'Staphylococcus saprophyticus enfeksiyonlarının klinik özellikleri nelerdir?'
        ]
    },

    # Slide 8
    {
        'slideNumber': 8,
        'title': 'Klinik Sınıflama: Komplike Olmayan Sistit ve Piyelonefrit',
        'subtitle': 'Sağlıklı genç kadın tanımı, alt vs üst sistem semptomatolojisi',
        'badge': 'Klinik Sınıflama',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 19-22) ÜSE klinik yaklaşımda iki ana sınıfa ayrılır: **1) Akut Komplike Olmayan Sistit**: Gebe olmayan, bilinen yapısal veya fonksiyonel ürolojik anomalisi bulunmayan, immünolojik ve metabolik açıdan sağlıklı premenopozal kadınlarda gelişen alt üriner sistem enfeksiyonudur. Tipik semptomlar: **Dizüri (idrar yaparken yanma), polaküri (sık idrara çıkma), sıkışma hissi (urgency), bulanık veya kokulu idrar ve hematüri**dir. Suprapubik bölgede hassasiyet olabilir ancak **ATEŞ, TİTREME VE YAN AĞRISI YOKTUR**. **2) Akut Komplike Olmayan Piyelonefrit**: Yine yapısal anomalisi olmayan sağlıklı kadında enfeksiyonun üst üriner sisteme (renal pelvis ve parankim) tırmanmasıdır. Klinik tabloya **Yüksek ateş (>38°C), titreme, yan ağrısı (flank pain), bulantı, kusma ve Kostovertebral Açı Hassasiyeti (KVAH)** eklenir. Sistit semptomları eşlik edebilir veya etmeyebilir.',
        'flashcards': [
            {
                'id': 'uti-fc-08-01',
                'category': 'Akut Sistit',
                'front': 'Akut komplike olmayan sistit tablosunda hangi sistemik bulguların OLMAMASI beklenir?',
                'hint': 'Üst üriner sistem ve parankim tutulumu göstergeleri.',
                'back': '**Yüksek ateş, titreme, yan ağrısı ve kostovertebral açı hassasiyeti (KVAH) YOKTUR**. Bu bulguların varlığı sistit değil, akut piyelonefrit göstergesidir.'
            },
            {
                'id': 'uti-fc-08-02',
                'category': 'Akut Piyelonefrit',
                'front': 'Akut piyelonefrit tanısında fizik muayenede saptanan en patognomonik muayene bulgusu nedir?',
                'hint': 'Sırtta 12. kosta ile omurga arasındaki açıya perküsyonda hassasiyet.',
                'back': '**Kostovertebral Açı Hassasiyeti (KVAH / Giordano belirtisi)**. Renal kapsülün akut inflamatuvar gerilimine bağlı olarak tek veya iki taraflı şiddetli hassasiyet alınır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Komplike Olmayan Tanımı',
                    'desc': 'Yalnızca gebe olmayan, anatomik/fonksiyonel kusuru bulunmayan sağlıklı kadınlar için geçerlidir.',
                    'isKey': True
                },
                {
                    'title': 'Sistit Triadı',
                    'desc': 'Dizüri + Polaküri + Urgency (Sıkışma). Suprapubik hassasiyet eşlik edebilir.',
                    'isKey': True
                },
                {
                    'title': 'Piyelonefrit Semptomları',
                    'desc': 'Ateş (>38°C) + Titreme + Yan Ağrısı + KVAH hassasiyeti + Bulantı/Kusma.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 20-22: Akut Komplike Olmayan Sistit vs Piyelonefrit',
                'headers': ['Parametre', 'Akut Komplike Olmayan Sistit', 'Akut Komplike Olmayan Piyelonefrit'],
                'rows': [
                    ['Anatomik Seviye', 'Alt Üriner Sistem (Mesane)', 'Üst Üriner Sistem (Renal Parankim & Pelvis)'],
                    ['Ateş / Titreme', 'Kesinlikle YOKTUR', 'Vardır (Tipik olarak >38°C, titremeyle yükselir)'],
                    ['Yan Ağrısı / KVAH', 'YOKTUR', 'Belirgin pozitiftir (Tek veya çift taraflı)'],
                    ['İşeme Semptomları', 'Dizüri, polaküri, sıkışma belirgin', 'Eşlik edebilir veya tamamen silik olabilir'],
                    ['Gastrointestinal Bulgu', 'Genellikle yoktur', 'Bulantı, kusma, iştahsızlık sıktır'],
                    ['Lökositoz / CRP', 'Normal veya minimal yüksek', 'Belirgin lökositoz (sola kayma) ve yüksek CRP']
                ]
            }
        },
        'spotPearls': [
            'Dizüri ve polaküri ile başvuran genç bir kadında vajinal akıntı veya kaşıntı yoksa akut sistit olasılığı >%90\'dır.',
            'Hematüri (kanlı idrar yapma) akut sistitli hastaların %30\'unda görülebilir; malignite göstergesi değildir ve tek başına hastalığı komplike yapmaz.',
            'Yaşlılarda piyelonefrit klasik ateş ve yan ağrısı yerine konfüzyon, deliryum veya düşmelerle prezente olabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_complicated_uti'], matched_questions_dict['q_culture_indications']],
        'aiPromptSuggestions': [
            'Sistit ile piyelonefrit klinik ve laboratuvar olarak nasıl ayırt edilir?',
            'Giordano testi (KVAH) nasıl değerlendirilir?'
        ]
    },

    # Slide 9
    {
        'slideNumber': 9,
        'title': 'Komplike Üriner Sistem Enfeksiyonları',
        'subtitle': 'Erkek cinsiyet kuralı, anatomik/fonksiyonel bozukluklar ve kateterler',
        'badge': 'Komplike İYE',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 23-24) **Komplike ÜSE**; tedavinin başarısız olma olasılığını artıran, rekürrens riskini yükselten veya ciddi renal parankimal hasara yol açabilecek yapısal, fonksiyonel ya da metabolik bir anormallik zemininde gelişen enfeksiyonlardır. **DERS NOTUNUN EN ÇOK VURGULADIĞI ALTIN KURAL: \'Erkeklerde aksi ispatlanmadıkça gelişen her ÜSE KOMPLİKE kabul edilir!\'** Çünkü sağlıklı genç erkekte uzun üretra ve prostatik salgılar enfeksiyonu neredeyse imkansız kılar; erkekte enfeksiyon varsa altta yatan obstrüksiyon, darlık, prostatit veya taş araştırılmalıdır. Diğer komplike hasta grupları: **Gebeler**, kontrolsüz Diabetes Mellitus, immünsüpresyon, renal transplant hastaları, nörojenik mesane, vezikoüreteral reflü (VUR), böbrek taşları, kalıcı kateter/nefrostomi ve hastanede kazanılmış enfeksiyonlardır.',
        'flashcards': [
            {
                'id': 'uro-fc-09-01',
                'category': 'Erkek Kuralı',
                'front': 'Ders notuna göre erkek hastalarda gelişen üriner sistem enfeksiyonları için geçerli temel kabul nedir?',
                'hint': 'Sayfa 23: Erkeklerde aksi ispatlanmadıkça...',
                'back': '**"Erkeklerde aksi ispatlanmadıkça gelişen ÜSE KOMPLİKE kabul edilir."** Erkek anatomisi korunaklı olduğundan, her erkek İYE altta yatan taş, darlık veya BPH obstrüksiyonu açısından araştırılmalıdır.'
            },
            {
                'id': 'uro-fc-09-02',
                'category': 'Komplike Faktörler',
                'front': 'Bir hastada gelişen İYE\'yi \'komplike\' kılan 5 temel klinik/anatomik durum nedir?',
                'hint': 'Sayfa 23-24: Cinsiyet, gebelik, taş, kateter, metabolizma.',
                'back': '1) **Erkek cinsiyet**\n2) **Gebelik**\n3) **Üriner sistemde taş veya obstrüksiyon**\n4) **Kalıcı üriner kateter varlığı**\n5) **Diyabet veya immünsüpresif durumlar**'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Erkek Cinsiyet Prensibi (Sayfa 23)',
                    'desc': 'Erkeklerde basit sistit kavramı yoktur; tüm enfeksiyonlar komplike kabul edilerek tetkik edilir.',
                    'isKey': True
                },
                {
                    'title': 'Gebelik Komplike Bir Durumdur',
                    'desc': 'Progesteron etkisiyle üreteral dilatasyon ve hidronefroz geliştiğinden piyelonefrit riski çok yüksektir.',
                    'isKey': True
                },
                {
                    'title': 'Taş ve Yabancı Cisim',
                    'desc': 'Bakteriler biyofilm tabakası içine saklanarak antibiyotik penetrasyonunu engeller.',
                    'isKey': True
                },
                {
                    'title': 'Dirençli Patojenler',
                    'desc': 'Komplike İYE\'lerde E. coli sıklığı düşerken Proteus, Pseudomonas ve Enterokoklar artar.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 23-24: Komplike Üriner Sistem Enfeksiyonu Kriterleri',
                'headers': ['Kategori', 'Komplike Edici Durum / Faktör', 'Yarattığı Risk'],
                'rows': [
                    ['Cinsiyet / Konak', 'Erkek hastalar', 'Altta yatan prostatit, darlık, BPH obstrüksiyonu riski'],
                    ['Fizyolojik', 'Gebe kadınlar', 'Preterm eylem, düşük doğum ağırlığı, %40 pyelonefrite dönüşüm'],
                    ['Mekanik / Yabancı Cisim', 'Kalıcı üretral kateter, DJ stent, nefrostomi', 'Biyofilm oluşumu, çoklu ilaç dirençli nozokomiyal suşlar'],
                    ['Anatomik Obstrüksiyon', 'Nefrolitiyazis, üretra darlığı, UPJ darlığı', 'İdrar stazı, intrarenal reflü, ürosepsis riski'],
                    ['Fonksiyonel Bozukluk', 'Nörojenik mesane, VUR', 'Mesanede yüksek basınç ve rezidüel idrar, böbrek hasarı'],
                    ['Metabolik / İmmün', 'Diabetes Mellitus, kemoterapi, transplant', 'Bozulmuş lökosit fonksiyonu, amfizemli pyelonefrit riski']
                ]
            }
        },
        'spotPearls': [
            'Ders notu: Erkeklerde aksi kanıtlanana kadar tüm İYE\'ler komplike kabul edilir ve en az 7-14 gün tedavi edilir.',
            'Ateş yüksekliği tek başına bir enfeksiyonu komplike yapmaz; ateş sistemik tutulumu gösterir (örn. akut komplike olmayan piyelonefrit).',
            'Komplike İYE şüphesi olan her hastadan tedavi öncesinde mutlaka kantitatif idrar kültürü ve antibiyogram alınmalıdır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_complicated_uti'], matched_questions_dict['q_culture_indications']],
        'aiPromptSuggestions': [
            'Erkeklerde İYE neden daima komplike kabul edilir?',
            'Komplike İYE ile komplike olmayan İYE tedavi süreleri nasıl değişir?'
        ]
    },

    # Slide 10
    {
        'slideNumber': 10,
        'title': 'Tekrarlayan İYE: Relaps ve Reenfeksiyon Ayrımı',
        'subtitle': '2 hafta kuralı, persistan odak vs dışkı kaynaklı yeni suş bulaşı',
        'badge': 'Tekrarlayan İYE',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 25) **Tekrarlayan İYE (Rekürren İYE)**; son 1 yılda ≥3 atak veya son 6 ayda ≥2 atak geçirilmesi olarak tanımlanır. Tekrarlayan enfeksiyonlar mekanizma ve zamanlama açısından ikiye ayrılır: **1) Relaps (Bakteriyel Persistans - Nüks)**: Başarılı görünen bir tedavi bitimini takiben **İLK 2 HAFTA İÇİNDE** ortaya çıkar ve enfeksiyon **AYNI BAKTERİ SUŞU İLE** nükseder. Nedenleri: Yetersiz antibiyotik dozu veya süresi, parankimde veya toplayıcı sistemde gizli kalan persistan bir odak (**böbrek taşı, enfekte kist, kronik bakteriyel prostatit, medüller sünger böbrek**). Tedavisinde ürolojik odak araştırılır ve tedavi süresi 2-6 haftaya uzatılır. **2) Reenfeksiyon**: Tedavi bitiminden **2 HAFTADAN DAHA UZUN SÜRE SONRA** gelişir ve genellikle **FARKLI BİR MİKROORGANİZMA İLE** (veya aynı bakterinin farklı bir suşuyla) meydana gelir. Tekrarlayan İYE\'lerin **%80 - 90\'ı reenfeksiyondur**; nedeni perineal kolonizasyon ve dışarıdan yeni bulaştır.',
        'flashcards': [
            {
                'id': 'uro-fc-10-01',
                'category': 'Relaps vs Reenfeksiyon',
                'front': 'Tedavi bitiminden sonraki ilk 2 hafta içinde AYNI bakteriyle gelişen nükse ne ad verilir ve en sık nedenleri nelerdir?',
                'hint': 'Sayfa 25: Relaps / Bakteriyel persistans.',
                'back': '**Relaps (Bakteriyel Persistans)**. Yetersiz tedavi süresi veya üriner traktusta gizli kalmış persistan bir odak (**böbrek taşı, prostatit, abse**) nedeniyle oluşur.'
            },
            {
                'id': 'uro-fc-10-02',
                'category': 'Reenfeksiyon',
                'front': 'Tedaviden 2 hafta sonra genellikle FARKLI bir bakteriyle gelişen ve tekrarlayan olguların %80-90\'ını oluşturan tablo nedir?',
                'hint': 'Dışkı florasından yeni inokülasyon.',
                'back': '**Reenfeksiyon**. Perineal floranın üretraya yeniden tırmanmasıyla gelişen bağımsız yeni enfeksiyon ataklarıdır; altta yatan yapısal taş/prostatit odağı aranmaz.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Tekrarlayan İYE Tanımı',
                    'desc': 'Yılda ≥3 atak veya son 6 ayda ≥2 atak geçirilmesidir.',
                    'isKey': True
                },
                {
                    'title': '2 Hafta ve Bakteri Kriteri (Sayfa 25)',
                    'desc': '<2 hafta + Aynı bakteri = Relaps; >2 hafta + Farklı bakteri = Reenfeksiyon.',
                    'isKey': True
                },
                {
                    'title': 'Reenfeksiyonun Ezici Sıklığı',
                    'desc': 'Tekrarlayan olguların %80-90\'ı reenfeksiyondur; davranışsal faktörlerle ilişkilidir.',
                    'isKey': True
                },
                {
                    'title': 'Relapsta Gizli Odak Uyarısı',
                    'desc': 'Relaps saptandığında mutlaka DÜSG/USG ile enfekte taş veya erkekte prostatit taranmalıdır.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 25: Relaps vs Reenfeksiyon Ayırıcı Tanı Tablosu',
                'headers': ['Özellik', 'Relaps (Bakteriyel Persistans)', 'Reenfeksiyon'],
                'rows': [
                    ['Zamanlama', 'Tedavi bitiminden sonraki ilk 2 hafta içinde', 'Tedavi bitiminden >2 hafta (aylar) sonra'],
                    ['Mikrobiyolojik Etken', 'Önceki enfeksiyondaki AYNI bakteri suşu', 'Genellikle FARKLI bakteri (veya farklı E. coli suşu)'],
                    ['Görülme Sıklığı', 'Tekrarlayan olguların %10 - 20\'si', 'Tekrarlayan olguların %80 - 90\'ı (En sık)'],
                    ['Temel Patoloji', 'Persistan anatomik odak (Taş, kist, abse, prostatit)', 'Perineal flora kolonizasyonu, cinsel aktivite'],
                    ['Klinik Yönetim', 'Altta yatan odağın cerrahi/medikal tedavisi + 2-6 hafta tedavi', 'Davranışsal önlemler, postkoital profilaksi, topikal östrojen']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 25: Relaps tedavisi yetersiz tedaviye veya persistan enfeksiyon odağına (taş vb.) bağlıdır.',
            'Erkekte relaps eden İYE aksi kanıtlanana kadar kronik bakteriyel prostatit kabul edilir ve en az 4-6 hafta tedavi edilir.',
            'Reenfeksiyon sıklığını azaltmak için koit sonrası miksiyon ve bol su tüketimi en etkili kanıta dayalı davranışsal önlemdir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_relapse_reinfection']],
        'aiPromptSuggestions': [
            'Relaps ile reenfeksiyon nasıl ayırt edilir?',
            'Tekrarlayan İYE olan bir hastaya yaklaşım algoritması nasıldır?'
        ]
    },

    # Slide 11
    {
        'slideNumber': 11,
        'title': 'Asemptomatik Bakteriüri (ASB) Tanımı ve Tarama Kriterleri',
        'subtitle': 'Kass kriteri (≥10^5 CFU/mL), ardışık 2 kültür kuralı ve klinik anlamı',
        'badge': 'Asemptomatik Bakteriüri',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 26 ve 73) **Asemptomatik Bakteriüri (ASB)**; hastada dizüri, polaküri, sıkışma, ateş veya yan ağrısı gibi üriner sisteme ait hiçbir semptom ya da fizik muayene bulgusu yokken, idrar kültüründe anlamlı sayıda bakteri üremesidir. Tanı kriteri (Kass Kriteri): **Orta akım idrarında ≥10^5 CFU/mL (kob/mL)** saf bakteri üremesidir. Kadınlarda distal üretra ve perine kontaminasyonu sık olduğundan, kesin tanı için **en az 24 saat arayla (birer gün arayla) alınmış 2 ardışık orta akım idrar kültüründe AYNI üropatojenin ≥10^5 CFU/mL üremesi** şarttır. Erkeklerde ise tek bir temiz orta akım idrarında ≥10^5 CFU/mL üreme tanı için yeterlidir. Kateterize hastada tek örnekte ≥10^2 CFU/mL olması da ASB kabul edilir. ASB bir hastalık değil, mesane lümeninin kommensal kolonizasyonudur.',
        'flashcards': [
            {
                'id': 'uro-fc-11-01',
                'category': 'ASB Kriteri',
                'front': 'Asemptomatik bir kadında Asemptomatik Bakteriüri (ASB) tanısı koyabilmek için gereken kültür kriteri nedir?',
                'hint': 'Sayfa 26: Kaç kültür, hangi aralıkla ve kaç koloni?',
                'back': 'Birer gün arayla (en az 24 saat arayla) alınmış **iki ardışık temiz orta akım idrar kültüründe AYNI bakterinin ≥ 10^5 CFU/mL** üremesidir.'
            },
            {
                'id': 'uro-fc-11-02',
                'category': 'Erkek ASB',
                'front': 'Asemptomatik bir erkekte ASB tanısı için kaç idrar kültürü yeterlidir?',
                'hint': 'Kadınlardan farklı olarak kontaminasyon riski düşüktür.',
                'back': 'Erkeklerde temiz orta akım idrarında **tek bir kültürde ≥ 10^5 CFU/mL** üreme olması tanı koydurucudur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Semptomsuz Bakteri Varlığı',
                    'desc': 'Hastada hiçbir disüri, pollaküri veya sistemik enfeksiyon bulgusu bulunmaz.',
                    'isKey': True
                },
                {
                    'title': 'Kass Kriteri (≥10^5 CFU/mL)',
                    'desc': 'Anlamlı bakteriüri eşiğidir; kontaminasyonu gerçek lümen üremesinden ayırır.',
                    'isKey': True
                },
                {
                    'title': 'Kadında İki Kültür Şartı',
                    'desc': 'Tek kültürde pozitiflik %80 güvenilirdir; ardışık 2 kültür güvenilirliği %95\'e çıkarır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 26: Örnekleme Türüne Göre Asemptomatik Bakteriüri Tanı Eşikleri',
                'headers': ['Hasta Grubu / Örnekleme Yöntemi', 'Gereken Örnek Sayısı', 'Tanısal Anlamlı Bakteriüri Eşiği'],
                'rows': [
                    ['Asemptomatik Kadın (Orta Akım)', '2 ardışık örnek (≥24 saat arayla)', 'Aynı bakteriden ≥ 10^5 CFU/mL'],
                    ['Asemptomatik Erkek (Orta Akım)', '1 tek örnek', '≥ 10^5 CFU/mL'],
                    ['Kateterize Hasta (Tek sonda çekimi)', '1 tek örnek', '≥ 10^2 CFU/mL'],
                    ['Suprapubik Aspirasyon Örneği', '1 tek örnek', 'Herhangi bir sayıda gram (-) basil']
                ]
            }
        },
        'spotPearls': [
            'ASB popülasyonda yaşla birlikte artar; huzurevinde kalan yaşlı kadınların %50\'sinde ASB pozitiftir.',
            'ASB varlığında idrarda lökosit (piyüri) bulunması tek başına antibiyotik tedavisi başlama endikasyonu DEĞİLDİR.',
            'Gereksiz ASB tedavisi bakteriyi yok etmez, aksine dirençli suşların yerleşmesine yol açar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_asb_definition'], matched_questions_dict['q_asb_indications']],
        'aiPromptSuggestions': [
            'Asemptomatik bakteriüri kriterleri kadın ve erkekte nasıl değişir?',
            'Piyüri olması asemptomatik bakteriüriyi tedavi etmeyi gerektirir mi?'
        ]
    },

    # Slide 12
    {
        'slideNumber': 12,
        'title': 'Asemptomatik Bakteriüride Tedavi Endikasyonları: Kimler Tedavi Edilir?',
        'subtitle': 'Yalnızca 2 kesin endikasyon: Gebeler ve İnvaziv Ürolojik Girişimler',
        'badge': 'Tedavi Endikasyonları',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 73-74) **Asemptomatik Bakteriüri genel popülasyonda kesinlikle tedavi EDİLMEZ**. Diyabetik hastalar, yaşlılar, menopozdaki kadınlar, kalıcı idrar sondası takılı hastalar veya omurilik felçlilerinde ASB tedavi edilirse mikroorganizma yok edilemez; aksine daha dirençli mikroorganizmalarla süperenfeksiyon gelişir. **DERS NOTUNA GÖRE ASB YALNIZCA 2 DURUMDA MUTLAK TEDAVİ EDİLİR:** **1) GEBELER**: Gebelikte ASB sıklığı %2-10\'dur. Tedavi edilmezse gebelerin **%20 - 40\'ında akut piyelonefrit** gelişir; bu durum erken doğum (preterm eylem), düşük doğum ağırlığı ve perinatal mortaliteye yol açar. Bu nedenle gebeler ilk trimesterde taranır ve ASB saptanırsa **3 GÜN** uygun antibiyotikle tedavi edilir. **2) Genitoüriner mukozal kanamaya yol açabilecek İNVAZİV ÜROLOJİK GİRİŞİM yapılacak hastalar** (TUR-P, TUR-M, perkütan nefrolitotomi, üreteroskopi); bakteriyemi ve ölümcül ürosepsis riskini önlemek için işlem öncesi tedavi şarttır.',
        'flashcards': [
            {
                'id': 'uro-fc-12-01',
                'category': 'ASB Endikasyonları',
                'front': 'Ders notuna göre Asemptomatik Bakteriürinin MUTLAK tedavi edilmesi gereken 2 klinik endikasyonu nedir?',
                'hint': 'Sayfa 73: Bir kadın doğum, bir üroloji endikasyonu.',
                'back': '1) **GEBELER** (tedavi edilmezse %40 piyelonefrit ve preterm eylem yapar).\n2) **Genitoüriner sisteme mukoza kanaması yapabilecek İNVAZİV GİRİŞİM yapılacak hastalar** (ürosepsisi önlemek için).'
            },
            {
                'id': 'uro-fc-12-02',
                'category': 'Gereksiz Tedavi Tuzakları',
                'front': 'Diyabetik bir kadında veya kalıcı sondalı bir hastada ASB saptandığında antibiyotik verilmeli midir?',
                'hint': 'Ders notu Sayfa 73: Kimler tedavi edilmez?',
                'back': '**HAYIR, KESİNLİKLE VERİLMEZ!** Diyabetlilerde, yaşlılarda ve kateterli hastalarda ASB tedavisi asemptomatik durumu düzeltmez; aksine dirençli suşların seçilmesine ve toksisiteye yol açar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Yalnızca 2 Kesin Endikasyon (Sayfa 73)',
                    'desc': '1) Gebe kadınlar, 2) Mukozal kanamalı invaziv ürolojik girişim öncesi.',
                    'isKey': True
                },
                {
                    'title': 'Gebelikte 3 Günlük Tedavi',
                    'desc': 'Gebelikte ASB saptandığında 3 gün güvenli oral antibiyotik verilir ve kontrol kültürü yapılır.',
                    'isKey': True
                },
                {
                    'title': 'Diyabet ve Sonda Yanılgısı',
                    'desc': 'Diyabetik kadınlar ve kateterli hastalar taranmaz ve tedavi edilmez (En klasik sınav tuzağı!).',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 73: Asemptomatik Bakteriüri Tedavi Karar Matrisi',
                'headers': ['Hasta / Klinik Durum', 'Tarama & Tedavi Endikasyonu?', 'Tedavi Edilme Gerekçesi / Edilmeme Sebebi'],
                'rows': [
                    ['Gebe Kadınlar', 'EVET (Mutlak Tedavi)', '%20-40 piyelonefrit riski, preterm eylem ve fetal kayıp önlenir'],
                    ['İnvaziv Ürolojik Girişim Öncesi', 'EVET (Mutlak Tedavi)', 'İşlem esnasında kana bakteri karışması ve ürosepsis engellenir'],
                    ['Diabetes Mellituslu Kadınlar', 'HAYIR (Tedavi Edilmez)', 'Enfeksiyon sıklığını azaltmaz, dirençli bakterilere yol açar'],
                    ['Kalıcı İdrar Sondalı Hastalar', 'HAYIR (Tedavi Edilmez)', 'Sonda kaldığı sürece bakteri yok edilemez, kolonizasyondur'],
                    ['Huzurevinde Kalan Yaşlılar', 'HAYIR (Tedavi Edilmez)', 'Mortalite ve morbiditeyi etkilemez, toksisite yaratır'],
                    ['Omurilik Yaralanmalı (TAK yapan)', 'HAYIR (Tedavi Edilmez)', 'Semptomsuz bakteriüri fizyolojik flora gibi kabul edilir']
                ]
            }
        },
        'spotPearls': [
            'TUS ve Kurul sınavlarının en klasik sorusu: \'Diyabetik kadında ASB tedavi edilmez, gebede ise mutlaka tedavi edilir!\'',
            'Gebelikte ASB tedavi edilmezse olguların üçte birinde fulminan akut piyelonefrit gelişir.',
            'İnvaziv ürolojik girişim yapılacak hastalarda antibiyotik tedavisi işlemden önce başlatılmalı ve idrar steril edilmelidir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_asb_indications']],
        'aiPromptSuggestions': [
            'Gebelikte asemptomatik bakteriüri neden bu kadar tehlikelidir?',
            'Diyabetik hastalarda ASB neden tedavi edilmez?'
        ]
    },

    # Slide 13
    {
        'slideNumber': 13,
        'title': 'Çocuklarda İYE ve Yaşa Göre Klinik Bulgular',
        'subtitle': 'Yenidoğan sepsisi, açıklanamayan ateş, VUR riski ve renal skar',
        'badge': 'Pediatrik İYE',
        'badgeColor': 'blue',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 29-31) çocuklarda İYE sıklığı, kliniği ve komplikasyonları erişkinden çok farklıdır. Çocukluk çağında İYE\'nin en korkulan sonucu böbrek parankiminde kalıcı hasar ve **Renal Skar (nedbe)** oluşmasıdır; bu durum ileride hipertansiyon ve son dönem böbrek yetmezliğine yol açabilir. Çocuklarda yaş küçüldükçe klinik bulgular silikleşir ve atipikleşir: **1) Yenidoğan Dönemi**: Tipik işeme semptomları görülmez. **Ateş veya hipotermi, emmeme, kusma, letarji, huzursuzluk, kilo alamama (gelişme geriliği) ve uzamış sarılık** gibi sepsis benzeri genel bulgularla seyreder. **2) Süt Çocukluğu (1 ay - 2 yaş)**: **Açıklanamayan yüksek ateş**, iştahsızlık, kusma, pis kokulu idrar, huzursuzluk. **3) 2 Yaşından Büyük Çocuklar**: Dizüri, karın ağrısı, polaküri, enürezis (idrar kaçırma) ve yan ağrısı gibi klasik lokal bulgular belirir. Ateşli İYE geçiren çocukların **%30 - 40\'ında Vezikoüreteral Reflü (VUR)** saptanır.',
        'flashcards': [
            {
                'id': 'uti-fc-13-01',
                'category': 'Pediatri',
                'front': 'Yenidoğan döneminde İYE hangi non-spesifik semptomlarla prezente olur?',
                'hint': 'Sayfa 31: Sepsis benzeri sistemik bulgular.',
                'back': '**Ateş veya hipotermi, emmeme (beslenememe), kusma, letarji, huzursuzluk, uzamış sarılık ve kilo alamama** (tipik lokal üriner bulgu yoktur!).'
            },
            {
                'id': 'uti-fc-13-02',
                'category': 'VUR İlişkisi',
                'front': 'Ateşli üriner enfeksiyon geçiren küçük çocuklarda altta yatan en sık doğumsal anormallik nedir?',
                'hint': 'İdrarın mesaneden üretere geri kaçışı.',
                'back': '**Vezikoüreteral Reflü (VUR)**. Ateşli İYE geçiren çocukların yaklaşık %30-40\'ında saptanır ve tedavi edilmezse renal skara yol açar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Atipik Bebeklik Semptomları',
                    'desc': 'Süt çocuklarında açıklanamayan ateşin en sık nedenlerinden biri İYE\'dir.',
                    'isKey': True
                },
                {
                    'title': 'Renal Skar Riski',
                    'desc': 'Özellikle ilk 2 yaşta geçirilen ateşli piyelonefrit atakları kalıcı parankim hasarı bırakır.',
                    'isKey': True
                },
                {
                    'title': 'VUR Taraması Şartı',
                    'desc': 'Ateşli İYE geçiren çocuklarda USG ve gerekirse voiding sistoüretrografi (VCUG) çekilmelidir.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 31: Çocuklarda Yaş Gruplarına Göre İYE Klinik Bulguları',
                'headers': ['Yaş Grubu', 'Baskın Semptom ve Bulgular', 'Klinik Karakter'],
                'rows': [
                    ['Yenidoğan (0-1 ay)', 'Emmeme, kusma, letarji, ateş/hipotermi, uzamış sarılık, kilo alamama', 'Sepsis benzeri genel tablo'],
                    ['Süt Çocuğu (1 ay - 2 yaş)', 'Açıklanamayan ateş, huzursuzluk, kusma, kötü kokulu idrar, iştahsızlık', 'Sistemik bulgular ön planda'],
                    ['Okul Öncesi (2 - 5 yaş)', 'Karın ağrısı, kusma, ateş, dizüri, yeni başlayan enürezis (idrar kaçırma)', 'Lokal ve sistemik miks'],
                    ['Okul Çağı (>5 yaş)', 'Klasik dizüri, polaküri, urgency, yan ağrısı ve KVAH hassasiyeti', 'Erişkin benzeri lokalize semptomlar']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 31: Yenidoğanda uzamış sarılık ve beslenememe durumunda idrar yolu enfeksiyonu mutlaka ekarte edilmelidir.',
            'Küçük çocuklarda idrar örneği alınırken torba örneği yerine kateter veya suprapubik aspirasyon tercih edilmelidir.',
            'Tek bir ateşli İYE atağı bile çocukta kalıcı renal parankim hasarı ve hipertansiyon riski yaratabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_complicated_uti']],
        'aiPromptSuggestions': [
            'Bebeklerde İYE neden erişkinden farklı seyreder?',
            'Çocuklarda renal skar oluşumu nasıl engellenir?'
        ]
    },

    # Slide 14
    {
        'slideNumber': 14,
        'title': 'İdrar Örnekleme Yöntemleri ve Laboratuvara Giriş',
        'subtitle': 'Orta akım, kateterizasyon, torba örneği ve Altın Standart Suprapubik Aspirasyon',
        'badge': 'Örnekleme',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 33-39) İYE tanısında en kritik ilk basamak doğru idrar örneğinin toplanmasıdır. Hatalı örnekleme gereksiz antibiyotik kullanımına veya yanlış negatifliğe yol açar. Örnekleme yöntemleri: **1) Temiz Orta Akım İdrarı (MSU)**: En sık uygulanan yöntemdir. Perine temizliği sonrası ilk 10-20 mL idrar dışarı akıtılarak üretra florası yıkanır; ardından orta akım steril kaba alınır. Sabah ilk idrarı (en az 4 saat mesanede beklemiş) en değerlisidir. **2) Üretral Kateterizasyon**: İdrarını tutamayan, bilinci kapalı veya aşırı obez hastalarda uygulanır; giriş esnasında steriliteye dikkat edilmelidir. **3) Torba Örneği**: Tuvalet eğitimi almamış bebeklerde kullanılır. **EN AZ GÜVENİLEN YÖNTEMDİR**; perine kontaminasyonu nedeniyle yanlış pozitiflik oranı çok yüksektir; negatif çıkarsa enfeksiyonu dışlar fakat pozitif çıkarsa kateterle doğrulanmalıdır. **4) SUPRAPUBİK ASPİRASYON**: Dolu mesaneye simfizis pubisin üzerinden iğneyle girilerek idrar çekilmesidir. **KONTAMİNASYONSUZ TEK ÖRNEKTİR VE TANI İÇİN ALTIN STANDARTTIR!**',
        'flashcards': [
            {
                'id': 'uro-fc-14-01',
                'category': 'Altın Standart',
                'front': 'Kontaminasyonsuz idrar elde etmede ve kesin mikrobiyolojik tanıda ALTIN STANDART örnekleme yöntemi nedir?',
                'hint': 'Sayfa 39: İğne ile mesaneden doğrudan aspirasyon.',
                'back': '**Suprapubik Aspirasyon**. Distal üretra florasını tamamen baypas ettiği için kontaminasyon riski sıfırdır; altın standarttır.'
            },
            {
                'id': 'uro-fc-14-02',
                'category': 'Torba Örneği Tuzağı',
                'front': 'Bebeklerde torba ile idrar toplama yönteminin en zayıf yönü ve güvenilirlik kuralı nedir?',
                'hint': 'Sayfa 37: En az güvenilen yöntem.',
                'back': '**En az güvenilen yöntemdir**; perineal kontaminasyon oranı çok yüksektir. Negatif gelirse İYE\'yi ekarte ettirir; ancak pozitif gelirse ASLA doğrudan tedavi başlanmaz, kateterle doğrulanır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Sabah İlk İdrarı',
                    'desc': 'Bakterilerin lümende nitrit ve lökosit esteraz oluşturabilmesi için en az 4 saat beklemiş idrar idealdir.',
                    'isKey': True
                },
                {
                    'title': 'Orta Akım Mantığı',
                    'desc': 'İlk porsiyon distal üretradaki kommensalleri temizler; orta porsiyon mesane içeriğini yansıtır.',
                    'isKey': True
                },
                {
                    'title': 'Suprapubik Aspirasyon (Altın Standart)',
                    'desc': 'Mesaneden doğrudan enjektörle alınır; üreyen tek bir bakteri bile patolojik kabul edilir.',
                    'isKey': True
                },
                {
                    'title': 'Torba Örneği Uyarısı',
                    'desc': 'Yalnızca enfeksiyonu dışlamak için kullanılır; üreme olursa kateterize örnek gerekir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 35-39: İdrar Örnekleme Yöntemlerinin Karşılaştırması',
                'headers': ['Örnekleme Yöntemi', 'Uygulama Alanı', 'Kontaminasyon Riski', 'Güvenilirlik Derecesi'],
                'rows': [
                    ['Temiz Orta Akım İdrarı', 'Koopere yetişkinler ve büyük çocuklar', 'Düşük-Orta (Uygun temizlikle)', 'Yüksek (Rutin pratikte ilk tercih)'],
                    ['Suprapubik Aspirasyon', 'Bebekler, şüpheli olgular, anaerop şüphesi', 'SIFIR (Florayı baypas eder)', 'ALTIN STANDART (%100 Özgüllük)'],
                    ['Üretral Kateterizasyon', 'İdrar yapamayanlar, yoğun bakım, bebekler', 'Düşük (Steril teknikle)', 'Yüksek'],
                    ['Perineal İdrar Torbası', 'Tuvalet eğitimi olmayan bebekler', 'ÇOK YÜKSEK (%50-70 yanlış pozitif)', 'EN AZ GÜVENİLEN YÖNTEM']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 39: Suprapubik aspirasyon idrar toplama yöntemleri arasında altın standarttır.',
            'İdrar alındıktan sonra en geç 2 saat içinde incelenmeli veya +4°C buzdolabında saklanmalıdır; aksi takdirde oda ısısında bakteriler hızla çoğalarak yalancı pozitiflik yaratır.',
            'Orta akım idrarı alınırken ilk 10-20 mL idrarın tuvalete yapılması distal üretra florasını temizlemek için şarttır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_culture_indications']],
        'aiPromptSuggestions': [
            'Suprapubik aspirasyon hangi durumlarda yapılır?',
            'İdrar torbası ile örnek toplarken nelere dikkat edilmelidir?'
        ]
    },

    # Slide 15
    {
        'slideNumber': 15,
        'title': 'Tam İdrar Tahlili (TİT): Dipstik, Lökosit Esteraz ve Nitrit Testi',
        'subtitle': '4 saat mesane bekleme şartı, gram (-) enterik nitrat redüktazı ve duyarlılık',
        'badge': 'Dipstik / TİT',
        'badgeColor': 'indigo',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 40-46) **İdrar Dipstik Testi (TİT/Strip Testi)**; hızlı, ucuz ve poliklinik şartlarında dakikalar içinde sonuç veren temel tanı aracıdır. Enfeksiyon tanısında iki kimyasal reaksiyon kritiktir: **1) Nitrit Testi**: Normal idrarda nitrat bulunur fakat nitrit bulunmaz. E. coli, Klebsiella ve Proteus gibi **Gram negatif enterik bakteriler**, sahip oldukları nitrat redüktaz enzimiyle diyetsel nitratı **nitrite** dönüştürür. Testin pozitif olması enfeksiyon için **yüksek özgüllüğe (>%90)** sahiptir. Ancak iki kritik istisnası vardır: İdrarın mesanede **en az 4 saat beklemiş olması gerekir** (yoksa bakteri nitratı dönüştürecek zaman bulamaz; yalancı negatiflik). Ayrıca **Enterococcus, Streptococcus ve Staphylococcus türleri nitrat redüktaz üretmez (nitrit negatiftir!)**. **2) Lökosit Esteraz Testi**: Nötrofillerin granüllerinde bulunan esteraz enzimini saptar; **piyüri** varlığını gösterir. Klinik bulgularla birleştiğinde duyarlılığı **%94\'e** ulaşır.',
        'flashcards': [
            {
                'id': 'uro-fc-15-01',
                'category': 'Nitrit Testi',
                'front': 'Dipstik testinde nitrit reaksiyonunun pozitifleşebilmesi için idrarın mesanede en az kaç saat beklemesi gerekir ve hangi bakteriler nitrit yapamaz?',
                'hint': 'Sayfa 43-44: Süre şartı ve gram (+) koklar.',
                'back': 'İdrarın mesanede **en az 4 saat** beklemesi gerekir.\n**Enterococcus, Streptococcus ve Staphylococcus** türleri nitrat redüktaz enzimine sahip olmadıkları için nitrit testi daima NEGATİF kalır.'
            },
            {
                'id': 'uro-fc-15-02',
                'category': 'Lökosit Esteraz',
                'front': 'Dipstik testinde lökosit esteraz testinin pozitif çıkması neyi gösterir?',
                'hint': 'Sayfa 45: İnflamatuvar hücre varlığı.',
                'back': 'İdrarda parçalanmış veya intakt nötrofil lökositlerin varlığını, yani **Piyüriyi** gösterir (duyarlılığı %94\'e kadar çıkar).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Gram Negatif Nitrat Redüktazı',
                    'desc': 'Enterobakteriler nitratı nitrite çevirir; yüksek özgüllüğe sahiptir.',
                    'isKey': True
                },
                {
                    'title': '4 Saat Bekleme Kuralı',
                    'desc': 'Sık idrara çıkan polakürik hastada bakteri enzimi nitratı dönüştüremez ve yalancı negatif çıkar.',
                    'isKey': True
                },
                {
                    'title': 'Nitrit Üretmeyen Patojenler',
                    'desc': 'Enterokoklar, Streptokoklar, Stafilokoklar ve Candida nitrit negatiftir.',
                    'isKey': True
                },
                {
                    'title': 'Lökosit Esteraz + Nitrit Kombinasyonu',
                    'desc': 'İkisi birden pozitif olduğunda İYE için pozitif prediktif değer >%95\'e ulaşır.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 43-46: Dipstik Testlerinin Tanısal Değeri ve Tuzakları',
                'headers': ['Test Bileşeni', 'Ölçtüğü Parametre', 'Duyarlılık / Özgüllük', 'Yalancı Negatiflik Nedenleri'],
                'rows': [
                    ['Nitrit Testi', 'Bakteriyel nitrat redüktaz aktivitesi', 'Duyarlılık: %50-70 / Özgüllük: >%90', 'İdrarın mesanede <4 saat kalması, Enterokok/Stafilokok etkeni, C vitamini'],
                    ['Lökosit Esteraz', 'Nötrofil granül esteraz enzimi', 'Duyarlılık: %80-94 / Özgüllük: %70-85', 'Glikozüri, yüksek dansite, proteinüri, bazı sefalosporinler'],
                    ['Nitrit (+) & LE (+)', 'Bakteriüri + Piyüri birlikteliği', 'Özgüllük: >%95', 'Enfeksiyon lehine en güçlü hızlı strip kanıtıdır'],
                    ['Nitrit (-) & LE (+)', 'Steril Piyüri veya Gram (+) kok', 'Özgüllük: Orta', 'Enterokok sistiti, Chlamydia, Tüberküloz veya taş/tümör']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 43-45: Nitrit yüksek oranda özgüldür fakat duyarlılığı düşüktür; nitritin negatif olması İYE\'yi ekarte ettirmez.',
            'Yüksek doz C vitamini (askorbik asit) tüketimi hem lökosit esteraz hem nitrit testinde yalancı negatifliğe yol açabilir.',
            'Enterokok sistitlerinde nitrit testi daima negatif gelecektir; bu durum sınavların klasik soru tipidir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Nitrit testi neden bazen idrar yolu enfeksiyonunda negatif çıkar?',
            'Lökosit esteraz testi ile piyüri nasıl korele edilir?'
        ]
    },

    # Slide 16
    {
        'slideNumber': 16,
        'title': 'İdrar Mikroskopisi ve Steril Piyüri',
        'subtitle': 'Piyüri tanımı (>5 lökosit/HPF), Lökosit Silendirleri ve Tüberküloz şüphesi',
        'badge': 'Mikroskopi',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 47-49) **İdrar Mikroskopisi**, santrifüj edilmiş idrar sedimentinin 400x büyütmede (büyük büyütme sahası - HPF) incelenmesidir. **Piyüri (İdrarda lökosit varlığı)**; santrifüj edilmiş idrarda **büyük büyütmede >5 lökosit/HPF** veya santrifüj edilmemiş idrarda >10 lökosit/mm³ olarak tanımlanır. Mikroskopide en kritik patognomonik bulgu **LÖKOSİT SİLENDİRLERİ (Leukocyte Casts)**dir. Lökosit silendirleri Tamm-Horsfall proteini içine hapsolmuş nötrofillerdir ve enfeksiyonun doğrudan renal tübül ve parankimden kaynaklandığını kanıtlar; **Akut Piyelonefrit için patognomoniktir** (sistitte kesinlikle silendir görülmez!). **STERİL PİYÜRİ**: İdrarda piyüri (lökosit) varlığına rağmen rutin kültürde bakteri ürememesidir. Nedenleri: **Daha önce başlanmış yetersiz antibiyotik tedavisi**, **Mycobacterium tuberculosis (Renal Tüberküloz)**, **Chlamydia trachomatis / Ureaplasma**, böbrek taşları, neoplaziler ve interstisyel nefrittir.',
        'flashcards': [
            {
                'id': 'uro-fc-16-01',
                'category': 'Lökosit Silendiri',
                'front': 'İdrar mikroskopisinde Lökosit Silendiri (Leukocyte cast) görülmesi hangi klinik antite için patognomoniktir ve sistitte görülür mü?',
                'hint': 'Renal parankim kaynaklı inflamasyon.',
                'back': '**Akut Piyelonefrit için patognomoniktir**. Lökosit silendirleri renal tübüllerde oluştuğu için üst üriner sistem parankim tutulumunu kanıtlar; alt üriner sistem sistitinde KESİNLİKLE GÖRÜLMEZ.'
            },
            {
                'id': 'uro-fc-16-02',
                'category': 'Steril Piyüri',
                'front': 'İdrar mikroskopisinde belirgin lökosit (piyüri) saptanmasına rağmen standart kültürde üreme olmaması durumuna ne denir ve en tipik 3 nedeni nedir?',
                'hint': 'Sayfa 48: Steril piyüri nedenleri.',
                'back': '**Steril Piyüri** denir. En sık nedenleri:\n1) Daha önce alınmış antibiyotik tedavisi\n2) **Renal Tüberküloz** (asidorezistan basil)\n3) **Chlamydia trachomatis / Üretrit**\n(Ayrıca üriner sistem taşı ve neoplaziler).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Piyüri Eşiği (Sayfa 47)',
                    'desc': 'Santrifüjlü idrarda büyük büyütmede (HPF) >5 lökosit bulunmasıdır.',
                    'isKey': True
                },
                {
                    'title': 'Lökosit Silendiri Eşittir Piyelonefrit',
                    'desc': 'Tübüllerde şekillenen bu yapılar enfeksiyonun renal parankimde olduğunu kesinleştirir.',
                    'isKey': True
                },
                {
                    'title': 'Steril Piyüri ve Tüberküloz (Sayfa 48)',
                    'desc': 'Kültür negatif piyüride akla ilk olarak antibiyotik kullanımı, klamidya ve tüberküloz gelmelidir.',
                    'isKey': True
                },
                {
                    'title': 'Hematüri Birlikteliği',
                    'desc': 'Sistitlerin üçte birinde erozif mukozal kanamaya bağlı eritrosit izlenir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 47-49: İdrar Sedimentinde Hücresel Elemanların Klinik Anlamı',
                'headers': ['Mikroskobik Eleman', 'Tanı Eşiği', 'Klinik Karşılığı ve Ayırıcı Tanı'],
                'rows': [
                    ['Lökosit (Piyüri)', '>5 / HPF', 'İnflamasyon veya enfeksiyon varlığı (alt veya üst İYE)'],
                    ['Lökosit Silendirleri', 'Herhangi bir sayıda', 'Akut Piyelonefrit (Tübüler inflamasyonun kesin kanıtı)'],
                    ['Eritrosit (Hematüri)', '>3 / HPF', 'Hemorajik sistit, taş, glomerulonefrit veya ürotelyal tümör'],
                    ['Bakteriüri', '>1 basil / HPF', 'Kantitatif olarak ≥10^5 CFU/mL bakteriüri ile koreledir'],
                    ['Yassı Epitel Hücreleri', 'Yoğun varlığı', 'Perineal kontaminasyon göstergesi (örnek geçersizdir!)']
                ]
            }
        },
        'spotPearls': [
            'Lökosit silendirleri piyelonefrit ile sistiti ayırmada idrar mikroskopisinin en değerli bulgusudur.',
            'Steril piyüri saptanan genç bir hastada dizüri varsa cinsel yolla bulaşan Chlamydia trachomatis mutlaka düşünülmelidir.',
            'İdrarda çok sayıda yassı epitel (skuamöz epitel) hücresi görülmesi perineal/vajinal kontaminasyonu gösterir; kültür sonucu dikkate alınmamalıdır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_etiology_ecoli']],
        'aiPromptSuggestions': [
            'Lökosit silendirleri nasıl oluşur ve ne anlama gelir?',
            'Steril piyüri ile gelen hastaya nasıl yaklaşılır?'
        ]
    },

    # Slide 17
    {
        'slideNumber': 17,
        'title': 'İdrar Kültürü: Altın Standart ve Anlamlı Bakteriüri Sınırları',
        'subtitle': 'Kass kriterleri (10^5, 10^4, 10^3, 10^2) ve İdrar Kültürü Endikasyonları',
        'badge': 'Kültür & Kass',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 52-56) **Kantitatif İdrar Kültürü tanı için ALTIN STANDARTTIR**. Ancak kültürde üreyen her bakteri klinik enfeksiyon anlamına gelmez. Edward Kass tarafından tanımlanan ve modifiye edilen **Anlamlı Bakteriüri Eşikleri**: **1) Asemptomatik bireyde orta akım idrarında ≥10^5 CFU/mL** (kadında 2 örnek, erkekte 1 örnek). **2) Akut semptomatik sistitli kadında ≥10^3 CFU/mL** (özellikle E. coli ise bu eşik tanı koydurur!). **3) Semptomatik piyelonefrit veya komplike İYE\'de ≥10^4 CFU/mL**. **4) Kateterize hastada tek sonda örneğinde ≥10^2 CFU/mL**. **5) Suprapubik aspirasyonda herhangi bir sayıda Gram (-) basil** üremesi anlamlıdır. **KÜLTÜR ENDİKASYONLARI (Sayfa 55)**: Şüpheli piyelonefrit, gebeler, erkek hastalar, diyabetikler, tedaviye yanıtsız olgular, tekrarlayan İYE. **DERS NOTU KRİTİK BİLGİ (Sayfa 56): Genç, gebe olmayan, anatomik kusuru bulunmayan basit sistitli kadınlarda idrar kültürü ve ek tetkik GEREKSİZDİR; ampirik tedavi verilir!**',
        'flashcards': [
            {
                'id': 'uro-fc-17-01',
                'category': 'Kass Kriterleri',
                'front': 'Akut komplike olmayan sistit semptomları (dizüri, sık idrar) olan bir kadında anlamlı idrar kültürü eşiği nedir?',
                'hint': 'Klasik 10^5 değil, semptomatik alt sınır.',
                'back': '**≥ 10^3 CFU/mL (kob/mL)**. Semptomatik bir kadında temiz orta akım idrarında ≥10^3 koloni UPEC üremesi tanı koydurucudur.'
            },
            {
                'id': 'uro-fc-17-02',
                'category': 'Kültür Endikasyonları',
                'front': 'Ders notuna göre hangi hasta grubunda semptomatik tedavi öncesinde kantitatif idrar kültürü yapılması GEREKSİZDİR?',
                'hint': 'Sayfa 56: Ek tetkik gereksizdir.',
                'back': '**Genç, gebe olmayan, sağlıklı premenopozal kadınlarda gelişen basit akut sistitte** idrar kültürü yapılması gereksizdir; ampirik tedavi başlanır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'İdrar Kültürü Altın Standarttır',
                    'desc': 'Etken mikroorganizmayı ve antibiyogram duyarlılığını kesin olarak belirler.',
                    'isKey': True
                },
                {
                    'title': 'Kass Eşikleri Klinik Tabloya Göre Değişir',
                    'desc': 'Asemptomatikte 10^5, sistitte 10^3, piyelonefritte 10^4, kateterde 10^2 CFU/mL.',
                    'isKey': True
                },
                {
                    'title': 'Basit Sistitte Kültür Yapılmaz (Sayfa 56)',
                    'desc': 'Tipik sistitte ampirik fosfomisin veya nitrofurantoin başlanır; rutin kültür maliyet ve zaman kaybıdır.',
                    'isKey': True
                },
                {
                    'title': 'Polimikrobiyal Üreme Kontaminasyondur',
                    'desc': 'Birden fazla farklı morfolojide bakteri üremesi neredeyse daima perineal bulaştır; tekrar gerekir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 52-55: Klinik Tablolara Göre Anlamlı Bakteriüri Sınırları (Kass)',
                'headers': ['Klinik Antite', 'Örnekleme Türü', 'Tanısal Koloni Sayısı (CFU/mL)'],
                'rows': [
                    ['Asemptomatik Bakteriüri (Kadın)', 'Orta Akım (2 ardışık örnek)', '≥ 10^5 CFU/mL'],
                    ['Asemptomatik Bakteriüri (Erkek)', 'Orta Akım (Tek örnek)', '≥ 10^5 CFU/mL'],
                    ['Akut Komplike Olmayan Sistit (Kadın)', 'Temiz Orta Akım', '≥ 10^3 CFU/mL (E. coli için)'],
                    ['Akut Piyelonefrit / Komplike İYE', 'Temiz Orta Akım', '≥ 10^4 CFU/mL'],
                    ['Sondalı / Kateterize Hasta', 'Steril Kateter Örneği', '≥ 10^2 CFU/mL'],
                    ['Suprapubik Aspirasyon', 'İğne ile aspirasyon', 'Herhangi bir sayıda Gram (-) basil']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 56: Tipik sistit semptomları olan genç kadında ampirik tedavi yeterlidir; ek tetkik ve kültür gereksizdir.',
            'Erkeklerde, gebelerde ve çocuklarda semptom olsun ya da olmasın kültür mutlak şarttır.',
            'Kültürde 3 veya daha fazla farklı bakteri üremesi enfeksiyon değil, örneğin kontamine olduğunu gösterir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_culture_indications'], matched_questions_dict['q_asb_definition']],
        'aiPromptSuggestions': [
            'İdrar kültürü endikasyonları nelerdir?',
            'Kass anlamlı bakteriüri kriterleri nelerdir?'
        ]
    },

    # Slide 18
    {
        'slideNumber': 18,
        'title': 'Radyolojik Görüntüleme Yöntemleri ve Endikasyonları',
        'subtitle': 'USG, DÜSG ve Kontrastsız/Kontrastlı BT: Ne zaman görüntüleme istenir?',
        'badge': 'Radyoloji',
        'badgeColor': 'purple',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 57-63) basit akut sistit olgularında radyolojik görüntülemenin yeri yoktur. Görüntüleme yöntemleri **komplike İYE, tedaviye 72 saatte yanıt vermeyen piyelonefrit veya sepsis tablosunda** endikedir. Amaç: Altta yatan obstrüksiyonu (taş), renal abseleri veya anatomik defektleri saptamaktır. **1) Ultrasonografi (USG)**: İlk basamak görüntüleme yöntemidir; radyasyon içermez, gebelerde ve çocuklarda güvenlidir. Hidronefrozu (obstrüksiyon), renal apseleri ve parankim kalınlığını mükemmel gösterir. **2) Direkt Üriner Sistem Grafisi (DÜSG)**: Radyoopak taşları ve amfizemli enfeksiyonlarda toplayıcı sistemdeki gaz gölgelerini gösterir. **3) Kontrastlı Bilgisayarlı Tomografi (BT)**: Renal parankim enfeksiyonlarında ve abselerde **EN DUYARLI VE EN DEĞERLİ GÖRÜNTÜLEME YÖNTEMİDİR**. Akut piyelonefritte kontrast tutulumunda azalma gösteren karakteristik **Kama Şeklinde (Wedge-shaped) hipodens perfüzyon defektleri** izlenir.',
        'flashcards': [
            {
                'id': 'uro-fc-18-01',
                'category': 'Radyoloji',
                'front': 'Akut piyelonefritte kontrastlı batın BT\'de izlenen en karakteristik parankimal radyolojik bulgu nedir?',
                'hint': 'Tübüler inflamasyon ve vazokonstrüksiyona bağlı kama paterni.',
                'back': '**Kama şeklinde (Wedge-shaped) hipodens perfüzyon defektleri**. İnflame renal lobüllerde mikrovasküler perfüzyon azalmasına bağlı olarak kama tarzında kontrast tutulum kaybı izlenir.'
            },
            {
                'id': 'uro-fc-18-02',
                'category': 'Görüntüleme Endikasyonu',
                'front': 'Akut piyelonefrit tedavisi başlanan bir hastada acil USG veya BT görüntüleme endikasyonu ne zaman doğar?',
                'hint': 'Sayfa 58: Uygun tedaviye rağmen ateşin düşmemesi süresi.',
                'back': 'Uygun parenteral antibiyotik tedavisine rağmen **48 - 72 saat içinde klinik yanıt alınamaması, ateşin düşmemesi** veya septik şok bulgularının gelişmesidir (abse veya taş obstrüksiyonu aranır).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Basit Sistitte Görüntüleme Yasaktır',
                    'desc': 'Rutin komplike olmayan sistitte hiçbir radyolojik tetkik gerekmez.',
                    'isKey': True
                },
                {
                    'title': 'USG İlk Tercihtir',
                    'desc': 'Hidronefroz, taş ve perinefritik koleksiyon taramasında hızlı ve radyasyonsuzdur.',
                    'isKey': True
                },
                {
                    'title': 'BT Altın Standarttır',
                    'desc': 'Renal abseleri, gaz oluşturan amfizemli piyelonefriti ve parankimal flegmonu en iyi BT gösterir.',
                    'isKey': True
                },
                {
                    'title': '72 Saat Kuralı',
                    'desc': 'Antibiyotik altında 72 saatte ateşi düşmeyen hastada mutlaka abse veya taş ekarte edilmelidir.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 57-63: ÜSE Radyolojik Görüntüleme Modaliteleri',
                'headers': ['Modalite', 'Endikasyon', 'Karakteristik Radyolojik Bulgu', 'Kısıtlılık / Not'],
                'rows': [
                    ['Ultrasonografi (USG)', 'İlk basamak, gebe, çocuk, obstrüksiyon şüphesi', 'Kalikektazi, pelvikaliektazi, hipoekoik abse', 'Operatör bağımlı, küçük taşları atlayabilir'],
                    ['DÜSG', 'Nefrolitiyazis şüphesi', 'Radyoopak kalsiyum kalkülüsleri, gaz gölgesi', 'Radyolüsent taşları ve doku detayını göstermez'],
                    ['Kontrastlı Batın BT', 'Tedaviye dirençli piyelonefrit (72 saat kuralı)', 'Kama şeklinde (wedge-shaped) hipoperfüzyon, abse', 'Renal yetmezlikte kontrast nefropatisi riski'],
                    ['Manyetik Rezonans (MR)', 'Gebelikte dirençli pyelonefrit veya kontrast alerjisi', 'Radyasyonsuz parankimal ödem ve abse tespiti', 'Pahalı ve acil şartlarda ulaşımı zordur']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 58: Akut piyelonefritte uygun tedaviye rağmen 72 saatte klinik düzelme yoksa altta yatan obstrüksiyon veya abse düşünülerek acil görüntüleme yapılır.',
            'Diyabetik hastalarda gaz üreten bakterilere bağlı Amfizemli Piyelonefrit BT\'de parankimde gaz kabarcıklarıyla tanınır ve acil nefrektomi gerektirebilir.',
            'Basit sistitte görüntüleme yapmak maliyet ve gereksiz radyasyon kaynağıdır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_culture_indications']],
        'aiPromptSuggestions': [
            'Piyelonefritte BT ne zaman çekilmelidir?',
            'Wedge-shaped perfüzyon defekti ne anlama gelir?'
        ]
    },

    # Slide 19
    {
        'slideNumber': 19,
        'title': 'Tedavi Prensipleri: Akut Sistit ve Piyelonefrit Yönetimi',
        'subtitle': 'Fosfomisin, Nitrofurantoin, Florokinolon kısıtlaması ve tedavi süreleri',
        'badge': 'Tedavi Protokolü',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 65-72) antibakteriyel tedavi hastalığın tablosuna (sistit vs piyelonefrit) ve hastanın özelliklerine göre planlanır: **1) Akut Komplike Olmayan Sistit Tedavisi**: Birinci basamakta **Fosfomisin trometamol (3 gram tek doz po)** veya **Nitrofurantoin (2x100 mg po, 5 gün)** tercih edilir. Alternatif olarak Pivmesillinam verilebilir. **ÇOK KRİTİK KURAL: Florokinolonlar (Siprofloksasin) ve Beta-laktamlar basit sistitte birinci basamakta KULLANILMAZ!** Florokinolonlar yan etki profilleri (tendon rüptürü, QT uzaması) ve direnç gelişimi nedeniyle sadece piyelonefrit ve komplike olgulara saklanır. **2) Komplike Sistit**: Tedavi süresi **7 güne** uzatılır. **3) Akut Komplike Olmayan Piyelonefrit**: Kültür ve antibiyogram mutlak alınır. Ayaktan oral tedavi alabilecek hafif-orta olgularda: **Oral Florokinolonlar (Siprofloksasin 2x500 mg 7 gün veya Levofloksasin 1x750 mg 5 gün)** birinci seçenektir. Oral alamayan veya ağır tablolarda: **Parenteral 3. Kuşak Sefalosporinler (Seftriakson 1-2g/gün)** veya Aminoglikozid başlanır.',
        'flashcards': [
            {
                'id': 'uro-fc-19-01',
                'category': 'Sistit Tedavisi',
                'front': 'Akut komplike olmayan sistit tedavisinde uluslararası rehberlerde ve ders notunda yer alan BİRİNCİ BASAMAK 2 temel oral ajan nedir?',
                'hint': 'Sayfa 67: Biri tek doz şase, diğeri 5 günlük kapsül.',
                'back': '1) **Fosfomisin trometamol** (3 gram tek doz şase)\n2) **Nitrofurantoin** (2x100 mg, 5 gün)\n(Florokinolonlar basit sistitte ilk basamakta KULLANILMAZ!).'
            },
            {
                'id': 'uro-fc-19-02',
                'category': 'Piyelonefrit Tedavisi',
                'front': 'Akut komplike olmayan piyelonefritte ayaktan oral tedavide ilk tercih edilen antibiyotik grubu hangisidir?',
                'hint': 'Böbrek parankiminde yüksek doku konsantrasyonu sağlayan geniş spektrumlu grup.',
                'back': '**Florokinolonlar (Siprofloksasin veya Levofloksasin)**. Renal parankimde çok yüksek doku penetrasyonu sağladıkları için ayaktan piyelonefrit tedavisinde ilk seçenektir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Sistitte İlk Basamak (Sayfa 67)',
                    'desc': 'Fosfomisin 3g tek doz veya Nitrofurantoin 5 gün. Pratik ve etkin.',
                    'isKey': True
                },
                {
                    'title': 'Florokinolon Kısıtlaması Kuralı',
                    'desc': 'Basit sistitte siprofloksasin verilmez; direnci korumak için piyelonefrite saklanır.',
                    'isKey': True
                },
                {
                    'title': 'Piyelonefritte Parankim Konsantrasyonu',
                    'desc': 'Piyelonefritte doku penetrasyonu şarttır; bu yüzden nitrofurantoin piyelonefritte KULLANILMAZ!',
                    'isKey': True
                },
                {
                    'title': 'Tedavi Süreleri',
                    'desc': 'Komplike olmayan sistit: 1-5 gün; Komplike sistit: 7 gün; Piyelonefrit: 7-14 gün.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 66-72: ÜSE Klinik Tablolarında Ampirik Tedavi Protokolü',
                'headers': ['Klinik Tablo', 'Birinci Basamak Tercih', 'Doz ve Süre', 'Uygulama Notu'],
                'rows': [
                    ['Akut Komplike Olmayan Sistit', 'Fosfomisin trometamol', '3 g po, Tek Doz (Gece yatarken)', 'Hafif-orta semptomda ilk tercih'],
                    ['Akut Komplike Olmayan Sistit', 'Nitrofurantoin', '2x100 mg po, 5 gün', 'Asit idrarda etkili, GFR <30-60 kontrendike'],
                    ['Komplike Sistit (Erkek, DM)', 'Kinolon veya Sefalosporin', 'Oral 7 gün', 'Tedavi öncesi mutlaka kültür alınmalıdır'],
                    ['Ayaktan Akut Piyelonefrit', 'Siprofloksasin / Levofloksasin', '7 - 10 gün oral', 'Florokinolon direnci <%10 olan bölgelerde'],
                    ['Yatan / Ağır Akut Piyelonefrit', 'Seftriakson veya Seftazidim', '1-2 g/gün IV (10-14 gün)', 'Klinik düzelince oral tedaviye geçilir']
                ]
            }
        },
        'spotPearls': [
            'Nitrofurantoin idrarda konsantre olur fakat renal parankimde doku düzeyine ulaşamaz; bu yüzden piyelonefritte KESİNLİKLE KULLANILMAZ.',
            'Fosfomisin trometamol mesanede 48-72 saat boyunca MİK üzerinde kalarak tek dozda kür sağlar.',
            'Komplike sistit olgularında tedavi süresi asla tek doz veya 3 gün olamaz; en az 7 gün sürdürülmelidir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_nitrofurantoin_pharma'], matched_questions_dict['q_culture_indications']],
        'aiPromptSuggestions': [
            'Basit sistitte florokinolonlar neden ilk tercih değildir?',
            'Nitrofurantoin neden piyelonefritte kullanılamaz?'
        ]
    },

    # Slide 20
    {
        'slideNumber': 20,
        'title': 'Ürolojik Antibiyotiklerin Farmakolojik Özellikleri',
        'subtitle': 'TMP-SMX sinerjisi, Nitrofurantoin kısıtlılıkları, Sefalosporinler ve Gebelik Güvenliği',
        'badge': 'Farmakoloji',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 78-84) İYE tedavisinde kullanılan antibiyotiklerin farmakolojik kısıtlılıkları sınavların vazgeçilmez sorularıdır: **1) Trimetoprim-Sülfametaksazol (TMP-SMX)**: Trimetoprim ve sülfametaksazol bakteriyel folik asit sentez yolağında ardışık iki enzimi (dihidropteroat sentaz ve dihidrofolat redüktaz) bloke ederek **güçlü sinerjistik bakterisid etki** gösterir. Toplumda direnç >%20 olduğu için ampirik kullanım azalmıştır. **2) Nitrofurantoin**: İdrardan hızla atılır, idrar konsantrasyonu çok yüksek iken serum/doku düzeyi sıfırdır. **Pseudomonas ve Proteus türleri doğal dirençlidir**. Asit idrarda etkindir. **Böbrek yetmezliğinde (GFR <30-60 mL/dk) idrara geçemez, kanda birikip periferik nöropati yapar; bu nedenle kontrendikedir!** Kronik kullanımda interstisyel akciğer fibrozu yapabilir. **3) Sefalosporinler**: Enterobakterilere karşı çok etkilidir; **Gebelikte en güvenli antibiyotik grubudur (Kategori B)**. **4) Aminopenisilinler (Ampisilin/Amoksisilin)**: %40-60 direnç nedeniyle tek başlarına ampirik İYE\'de kullanılmazlar. **5) Fosfomisin**: Peptidoglikan sentezinin ilk basamağını (MurA) bloke eder; çapraz direnç düşüktür.',
        'flashcards': [
            {
                'id': 'uro-fc-20-01',
                'category': 'Farmakoloji',
                'front': 'Nitrofurantoinin doğal olarak etkisiz olduğu (doğal dirençli) iki önemli üropatojen bakteri hangisidir?',
                'hint': 'Sayfa 79: Pseudomonas ve bir üreaz pozitif etken.',
                'back': '**Pseudomonas aeruginosa** ve **Proteus mirabilis** (ayrıca Serratia türleri). Bu bakterilerin enfeksiyonunda nitrofurantoin asla kullanılmaz.'
            },
            {
                'id': 'uro-fc-20-02',
                'category': 'Gebelik Güvenliği',
                'front': 'Gebelikte gelişen asemptomatik bakteriüri veya sistit tedavisinde EN GÜVENLİ oral antibiyotik seçenekleri nelerdir?',
                'hint': 'Kategori B olan sefalosporinler ve fosfomisin.',
                'back': '**Fosfomisin trometamol**, **Oral Sefalosporinler (Sefaleksin, Sefuroksim)** veya **Amoksisilin-Klavulanat** (Florokinolonlar kıkırdak hasarı, Doksisiklin diş lekelenmesi, TMP-SMX folat antagonizmi nedeniyle kontrendikedir!).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'TMP-SMX Sinerjisi (Sayfa 78)',
                    'desc': 'Folat sentezinde ardışık iki basamağı inhibe ederek bakterisid etki sağlar.',
                    'isKey': True
                },
                {
                    'title': 'Nitrofurantoin Böbrek Uyarısı',
                    'desc': 'GFR <30-60 mL/dk kontrendikedir; parankime geçmez, kanda birikip nöropati yapar.',
                    'isKey': True
                },
                {
                    'title': 'Sefalosporinler Gebelikte İlk Tercih',
                    'desc': 'Gebelikte güvenle kullanılır; fetal toksisitesi yoktur.',
                    'isKey': True
                },
                {
                    'title': 'Aminopenisilin Direnci (%40-60)',
                    'desc': 'E. coli ampirik tedavisinde tek başına ampisilin/amoksisilin artık kullanılamaz.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 78-84: Ürolojik Antibiyotiklerin Karşılaştırmalı Farmakoloji Matrisi',
                'headers': ['Antibiyotik', 'Etki Mekanizması', 'Klinik Avantajı', 'Temel Kısıtlılık / Kontrendikasyon'],
                'rows': [
                    ['Fosfomisin Trometamol', 'MurA enzim inh. (hücre duvarı)', 'Tek doz 3g, çapraz direnç çok düşük', 'Piyelonefritte ve prostatitte yetersiz doku düzeyi'],
                    ['Nitrofurantoin', 'Bakteriyel ribozom ve DNA inaktivasyonu', 'Mesanede yüksek konsantrasyon, düşük direnç', 'GFR <30-60 kontrendike, Proteus/Pseudomonas etkisiz, parankime geçmez'],
                    ['Sefalosporinler (2/3. Kuşak)', 'PBP inhibisyonu (hücre duvarı)', 'Gebelikte en güvenli grup (Kategori B)', 'Enterokoklara doğal olarak etkisizdir'],
                    ['TMP-SMX', 'Folat yolağı ardışık enzim blokajı', 'Prostat dokusuna mükemmel penetrasyon', 'Yüksek direnç (>%20), gebelikte 1. ve 3. trimester sakıncalı'],
                    ['Florokinolonlar', 'DNA Giraz (Topoizomeraz II ve IV) inh.', 'Mükemmel renal parankim ve prostat penetrasyonu', 'Basit sistitte ilk basamak değil; gebelerde kontrendike'],
                    ['Aminoglikozidler (Gentamisin)', '30S ribozom inhibisyonu', 'Ağır ürosepsiste çok hızlı bakterisid etki', 'Nefrotoksisite ve ototoksisite riski (TDM gerekir)']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 79: Nitrofurantoin Pseudomonas ve Proteus türleri dışındaki üropatojenlere etkilidir.',
            'Nitrofurantoin asidik idrarda maksimum etkinliğe ulaşır; alkalinizasyon ilacın gücünü düşürür.',
            'Florokinolonlar kıkırdak toksisitesi (kondrotoksisite) nedeniyle gebelerde ve büyüme çağındaki çocuklarda zorunlu olmadıkça kullanılmaz.'
        ],
        'relatedQuestions': [matched_questions_dict['q_nitrofurantoin_pharma']],
        'aiPromptSuggestions': [
            'Gebelikte hangi antibiyotikler güvenlidir, hangileri kontrendikedir?',
            'TMP-SMX sinerjisi nasıl çalışır?'
        ]
    },

    # Slide 21
    {
        'slideNumber': 21,
        'title': 'Korunma, Profilaksi ve Bağışıklama (OM-89/Uro-Vaxom)',
        'subtitle': 'Postkoital miksiyon, vajinal östrojen, antibiyotik profilaksisi ve oral aşı',
        'badge': 'Korunma & Aşı',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Resmi ders notuna göre (Sayfa 85-87) tekrarlayan İYE yönetiminde antibiyotik direncinin önlenmesi için medikal profilaksi öncesinde **koruyucu davranışsal ve biyolojik önlemler** ilk basamakta yer almalıdır: **1) Davranışsal Önlemler**: Cinsel aktif kadınlarda **ilişki sonrası hemen miksiyon (işeme)** önerilir (üretraya inoküle olan bakterileri süpürür). Bol sıvı alımı (>2 L/gün), genital bölgenin önden arkaya silinmesi, spermisid ve diyafram kullanımının sonlandırılması. **2) Postmenopozal Kadınlarda Topikal Vajinal Östrojen**: Vajinal atrofiyi geri çevirir, laktobasil kolonizasyonunu yeniden sağlar ve vajen pH\'sını asitleştirerek reenfeksiyonları belirgin şekilde azaltır. **3) İlaç Profilaksisi**: Davranışsal önlemler yetersizse; koit ilişkili olanlarda **tek doz postkoital antibiyotik** (nitrofurantoin veya TMP-SMX) veya koitten bağımsız olanlarda 3-6 ay düşük doz gece antibiyotik profilaksisi. **4) Bağışıklama (Oral Bakteriyel Aşı - OM-89 / Uro-Vaxom)**: Yılda >3 atak geçiren komplike olmayan tekrarlayan İYE\'lerde kullanılır; 18 farklı E. coli suşunun liyofilize lizatını içerir, mukozal IgA salgısını artırarak nüksleri önler.',
        'flashcards': [
            {
                'id': 'uro-fc-21-01',
                'category': 'Bağışıklama',
                'front': 'Ders notuna göre yılda >3 atak geçiren komplike olmayan tekrarlayan ÜSE\'lerde profilaksi amacıyla kullanılan bağışıklama ajanı nedir?',
                'hint': 'Sayfa 86-87: 18 E. coli suşu liyofilize lizatı (oral aşı).',
                'back': '**Oral Bakteriyel Aşı (OM-89 / Uro-Vaxom)**. 18 farklı E. coli suşunun liyofilize lizatını içerir; mesane mukozal IgA yanıtını ve makrofaj aktivitesini artırarak tekrarlayan sistit ataklarını azaltır.'
            },
            {
                'id': 'uro-fc-21-02',
                'category': 'Davranışsal Önlem',
                'front': 'Cinsel ilişki ile tetiklenen reenfeksiyonlarda hastaya önerilecek en basit ve etkili davranışsal önlem nedir?',
                'hint': 'Sayfa 85: İlişki sonrası eylem.',
                'back': '**İlişkiden (koitten) hemen sonra miksiyon (idrar yapma)**. Koit esnasında mekanik olarak üretraya itilen bakterileri mesaneye tutunmadan idrar akımıyla dışarı atar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Postkoital Miksiyon Kuralı (Sayfa 85)',
                    'desc': 'İlişki sonrası ilk 15 dakikada işemek mekanik yıkamayla bakteriyel yükü temizler.',
                    'isKey': True
                },
                {
                    'title': 'Postmenopozal Vajinal Östrojen',
                    'desc': 'Sistemik değil lokal östrojen kremleri laktobasilleri canlandırarak pH\'yı düşürür.',
                    'isKey': True
                },
                {
                    'title': 'Postkoital Tek Doz Profilaksi',
                    'desc': 'Sürekli antibiyotik yerine yalnızca ilişkiden sonra tek doz nitrofurantoin veya TMP-SMX verilir.',
                    'isKey': True
                },
                {
                    'title': 'OM-89 (Uro-Vaxom) Aşısı (Sayfa 86-87)',
                    'desc': 'Yılda >3 atak geçirenlerde immünoprofilaksi olarak 3 ay boyunca sabah aç karnına uygulanır.'
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 85-87: Tekrarlayan İYE Korunma ve Profilaksi Basamakları',
                'headers': ['Basamak / Yöntem', 'Hedef Kitle', 'Etki Mekanizması', 'Uygulama Şekli'],
                'rows': [
                    ['Postkoital Miksiyon', 'Cinsel aktif kadınlar', 'İnoküle olan bakterileri mesaneye varmadan mekanik atma', 'İlişkiden hemen sonra idrar yapılması'],
                    ['Topikal Vajinal Östrojen', 'Postmenopozal kadınlar', 'Glikojen artışı, laktobasil restorasyonu, vajen asitleşmesi', 'Haftada 2-3 gece lokal vajinal krem/ovül'],
                    ['Bağışıklama (OM-89)', 'Yılda >3 atak geçiren kadınlar', 'Lokal mukozal IgA ve poliklonal T hücre stimülasyonu', 'Günde 1 kapsül oral, 3 ay boyunca'],
                    ['Postkoital Antibiyotik', 'Koitle tetiklenen reenfeksiyonlar', 'İnokülasyon anında mesane lümeninde bakterisid etki', 'İlişkiden sonra 2 saat içinde tek doz'],
                    ['Sürekli Düşük Doz Profilaksi', 'Refrakter tekrarlayan İYE', 'Bakteriyel kolonizasyonu 3-6 ay sürekli baskılama', 'Her gece yatarken düşük doz Nitrofurantoin/TMP-SMX']
                ]
            }
        },
        'spotPearls': [
            'Ders notu Sayfa 86-87: Yılda >3 atak geçiren komplike olmayan tekrarlayan İYE\'lerde OM-89 oral aşı ile bağışıklama önerilir.',
            'Postmenopozal kadında oral östrojen değil, lokal/topikal vajinal östrojen laktobasil kolonizasyonunda etkilidir.',
            'Postkoital tek doz antibiyotik profilaksisi, günlük sürekli profilaksi kadar etkilidir ve ilaç maruziyetini %70-80 azaltır.'
        ],
        'relatedQuestions': [
            matched_questions_dict['q_relapse_reinfection'],
            matched_questions_dict['q_complicated_uti']
        ],
        'aiPromptSuggestions': [
            'OM-89 (Uro-Vaxom) aşısı nasıl etki eder ve kimlere verilir?',
            'Postmenopozal kadınlarda vajinal östrojenin İYE koruyuculuğu nasıldır?'
        ]
    }
]

# Build complete deck object for Batch 3
batch3_deck = {
    'id': 'deck-urinary-tract-infections',
    'title': 'Üriner Sistem Enfeksiyonları',
    'shortTitle': 'Üriner Sistem Enfeksiyonları',
    'discipline': 'Üroloji / Enfeksiyon Hastalıkları',
    'committee': 'Kurul 1',
    'instructor': 'Dr. Özer Baran',
    'audioFile': '3)Üriner Sistem Enfeksiyonları.mp3',
    'audioDuration': '60 dk',
    'confidence': '%99 (Resmi Ders Notu & Redakte Veri Sentezi)',
    'themeColor': 'rose',
    'matchedNoteId': 'knote-donem3-kurul1-uriner-enfeksiyonlar',
    'matchedNoteTitle': '3)Üriner Sistem Enfeksiyonları.txt',
    'overview': 'Üriner sistem enfeksiyonlarının (sistit, piyelonefrit, komplike İYE, asemptomatik bakteriüri) epidemiyolojisi, cinsiyet-yaş dinamikleri (neonatal erkek üstünlüğü); asendan (%99) ve hematojen patogenez; konak savunması (uromodulin, GAG, miksiyon); virülans faktörleri (Tip 1 vs P fimbriya); mikrobiyolojik etkenler (UPEC, S. saprophyticus, Proteus, Pseudomonas); idrar toplama (suprapubik altın standart); dipstik TİT (lökosit esteraz, nitrit ve 4 saat kuralı); mikroskopi (piyüri, lökosit silendirleri, steril piyüri); Kass anlamlı bakteriüri eşikleri; ASB\'nin 2 mutlak tedavi endikasyonu (gebelik ve invaziv ürolojik girişim); ampirik tedaviler (fosfomisin, nitrofurantoin, florokinolon kısıtlaması) ve OM-89 bağışıklama profilaksisi.',
    'highYieldPearls': [
        'ÜSE insanların hekime başvurmasına en sık yol açan bakteriyel enfeksiyon grubudur; kadınların %50\'si yaşam boyu en az bir kez geçirir.',
        'Neonatal dönemde İYE erkek bebeklerde kızlardan daha sıktır (Erkek/Kız: 1.5/1); 50 yaşından sonra erkekte BPH nedeniyle tekrar artar.',
        'ÜSE\'lerin %99\'u asendan yolla gelişir; hematojen yol (<%2) S. aureus ve tüberküloz için geçerlidir.',
        'Tip 1 fimbriya mannoza duyarlıdır ve mesane sistitinden sorumludur; P fimbriya (Pap) mannoza dirençlidir, Gal-Gal reseptörüne bağlanır ve piyelonefrit yapar.',
        'Toplum kökenli komplike olmayan sistitte en sık etken UPEC (%75-90), ikinci sırada Staph. saprophyticus (%5-15) gelir.',
        'DERS NOTU ALTIN KURALI: Erkeklerde aksi ispatlanmadıkça gelişen her ÜSE KOMPLİKE kabul edilir!',
        'Relaps tedavi bitimini takiben ilk 2 haftada AYNI bakteriyle nükseder (gizli taş/prostatit odağı); reenfeksiyon >2 hafta sonra FARKLI bakteriyle gelişir (%80-90 en sık).',
        'Suprapubik aspirasyon kontaminasyonsuz tek örnektir ve altın standarttır; torba örneği en az güvenilendir.',
        'Nitrit testi enterobakterilerin varlığını gösterir ve çok özgüldür; ancak idrarın mesanede en az 4 saat beklemesi gerekir ve Enterokoklar nitrit üretmez!',
        'Lökosit silendirleri Akut Piyelonefrit için patognomoniktir; sistitte asla görülmez.',
        'Genç, gebe olmayan, sağlıklı kadında basit sistitte idrar kültürü ve ek tetkik GEREKSİZDİR; ampirik tedavi verilir.',
        'Asemptomatik Bakteriüri (ASB) diyabetiklerde ve kateterlilerde tedavi EDİLMEZ; yalnızca 2 durumda tedavi edilir: GEBELER ve İNVAZİV ÜROLOJİK GİRİŞİMLER!',
        'Basit sistitte birinci basamak Fosfomisin 3g tek doz veya Nitrofurantoin 5 gündür; Florokinolonlar basit sistitte ilk basamakta KULLANILMAZ!',
        'Nitrofurantoin renal parankime geçmez, bu yüzden piyelonefritte KULLANILMAZ; ayrıca GFR <30-60 mL/dk olduğunda kontrendikedir.',
        'Yılda >3 atak geçiren tekrarlayan İYE\'lerde 18 E. coli suşu içeren oral aşı (OM-89 / Uro-Vaxom) ile bağışıklama önerilir.'
    ],
    'slides': slides_batch3,
    'totalSlides': len(slides_batch3),
    'matchedPastQuestionsCount': 7
}

# Insert Batch 3 right after Batch 2 (at index 2)
# Remove any existing deck with this ID
filtered_decks = [d for d in existing_decks if d.get('id') not in ['deck-urinary-tract-infections', 'learn-uriner-sistem-enfeksiyonlari']]
filtered_decks.insert(2, batch3_deck)

with open(decks_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_decks, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(filtered_decks)} decks into {decks_file} (Batch 3 inserted at index 2).")

# Update meta_file
if os.path.exists(meta_file):
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta_list = json.load(f)
else:
    meta_list = []

batch3_meta = {
    'id': batch3_deck['id'],
    'title': batch3_deck['title'],
    'shortTitle': batch3_deck['shortTitle'],
    'discipline': batch3_deck['discipline'],
    'committee': batch3_deck['committee'],
    'instructor': batch3_deck['instructor'],
    'totalSlides': len(slides_batch3),
    'matchedQuestionsCount': len(matched_questions_dict),
    'totalFlashcardsCount': sum(len(s.get('flashcards', [])) for s in slides_batch3),
    'themeColor': '#e11d48',
    'overview': batch3_deck['overview']
}

filtered_meta = [m for m in meta_list if m.get('id') not in ['deck-urinary-tract-infections', 'learn-uriner-sistem-enfeksiyonlari']]
filtered_meta.insert(2, batch3_meta)

with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_meta, f, ensure_ascii=False, indent=2)

print(f"Updated {meta_file} with {len(filtered_meta)} entries.")
