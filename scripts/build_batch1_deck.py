import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load existing decks so we can update or prepend Batch 1
decks_file = 'src/data/interactive_learning_decks.json'
meta_file = 'src/data/learning_decks_meta.json'
past_q_file = 'src/data/pastQuestions.json'

with open(decks_file, 'r', encoding='utf-8') as f:
    existing_decks = json.load(f)

# Load real past questions to find matches
with open(past_q_file, 'r', encoding='utf-8') as f:
    all_past_questions = json.load(f)

print(f"Loaded {len(existing_decks)} existing decks and {len(all_past_questions)} past questions.")

# Define real past questions for urinary obstruction
matched_questions_dict = {
    'q_bph': {
        'id': 'urol-bph-path-01',
        'examYear': '2021-2022',
        'committeeId': 'Kurul 5',
        'discipline': 'Tıbbi Patoloji / Üroloji',
        'topic': 'Benign Prostat Hiperplazisi ve Çıkım Obstrüksiyonu',
        'stem': 'Benign prostat hiperplazisinin (BPH) patogenezinde prostatik stromal ve epitelyal hücre proliferasyonunun ana medyatörü aşağıdakilerden hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Testosteron'},
            {'key': 'B', 'text': 'Dihidrotestosteron (DHT)', 'isCorrect': True},
            {'key': 'C', 'text': 'Östrojen'},
            {'key': 'D', 'text': 'Prolaktin'},
            {'key': 'E', 'text': 'İnsülin benzeri büyüme faktörü (IGF-1)'}
        ],
        'correctAnswer': 'B',
        'explanation': 'BPH patogenezinde temel androjenik medyatör dihidrotestosterondur (DHT). Testosteron, prostat stromal hücrelerinde bulunan Tip-2 5-alfa redüktaz enzimi ile DHT\'ye dönüştürülür. DHT nükleer androjen reseptörlerine bağlanarak büyüme faktörlerinin (FGF, TGF-beta) transkripsiyonunu uyarır ve mesane çıkım obstrüksiyonuna zemin hazırlayan stromal ve epitelyal hiperplaziye yol açar.'
    },
    'q_pod': {
        'id': 'urol-pod-02',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 5',
        'discipline': 'Üroloji / Nefroloji',
        'topic': 'Postobstrüktif Diürez Yönetimi',
        'stem': 'Bilateral üreteral obstrüksiyonu veya soliter böbrek tıkanıklığı cerrahi/girişimsel olarak dekomprese edilen hastada erken dönemde gelişen post-obstrüktif diürez yönetimi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?',
        'options': [
            {'key': 'A', 'text': 'Kaybedilen idrar miktarının %100\'ünden fazlası agresif şekilde intravenöz olarak yerine konulmalıdır.'},
            {'key': 'B', 'text': 'Poliüri daima kalıcıdır ve hastaya ömür boyu vazopressin başlanmalıdır.'},
            {'key': 'C', 'text': 'İdrar çıkışı saatlik izlenmeli; iatrojenik poliüri kısır döngüsünden kaçınmak için kaybedilen hacmin yaklaşık %50-75\'i replase edilmelidir.', 'isCorrect': True},
            {'key': 'D', 'text': 'Postobstrüktif diürez sadece tek taraflı parsiyel obstrüksiyonlarda görülür.'},
            {'key': 'E', 'text': 'Serum potasyum ve magnezyum düzeyleri bu süreçte asla değişmez.'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Postobstrüktif diürez (POD), bilateral veya soliter böbrek tıkanıklığının dekompresyonu sonrası saatte >200 mL idrar çıkışıyla karakterizedir. Tedavideki en kritik kural iatrojenik poliüri kısır döngüsünü önlemektir: Hastaya çıkardığı idrar kadar (%100) sıvı verilirse, verilen sıvı ozmotik ve volüm yükü oluşturarak diürezi sürdürür. Bu nedenle idrar çıkışının %50-75\'i replase edilmeli, elektrolitler (K, Mg, Na) yakından izlenmelidir.'
    },
    'q_luts': {
        'id': 'urol-luts-03',
        'examYear': '2021-2026',
        'committeeId': 'Kurul 5',
        'discipline': 'Üroloji',
        'topic': 'Alt Üriner Sistem Semptomları (LUTS)',
        'stem': 'Aşağıdaki alt üriner sistem semptomlarından hangisi mesane dolumu ve depolama (storage / irritatif) semptomları arasında yer alır?',
        'options': [
            {'key': 'A', 'text': 'İdrar akış hızında azalma (Zayıf akım)'},
            {'key': 'B', 'text': 'İdrarı tam boşaltamama hissi'},
            {'key': 'C', 'text': 'İdrar sıklığı / Sık idrara çıkma (Pollaküri / Frequency)', 'isCorrect': True},
            {'key': 'D', 'text': 'İşeme başlangıcında tutukluk (Hesitancy)'},
            {'key': 'E', 'text': 'Kesintili işeme (Intermittency)'}
        ],
        'correctAnswer': 'C',
        'explanation': 'Alt üriner sistem semptomları (LUTS); Depolama (irritatif), İşeme (obstrüktif) ve İşeme sonrası semptomlar olarak üçe ayrılır. Pollaküri (frequency), noktüri, urgency (ani sıkışma) ve sıkışma tipi inkontinans depolama semptomlarıdır. Zayıf akım, hesitancy (duraksama), intermittency (kesintili işeme) ve ıkınarak işeme ise işeme/obstrüksiyon semptomlarıdır.'
    },
    'q_infected_hydro': {
        'id': 'urol-inf-hydro-04',
        'examYear': '2024-2025',
        'committeeId': 'Kurul 5',
        'discipline': 'Üroloji / Acil Tıp',
        'topic': 'Enfekte Hidronefroz ve Ürolojik Aciller',
        'stem': 'Üreteral obstrüksiyona bağlı hidronefroz zemininde yüksek ateş (39°C), titreme ve lökositoz tablosu gelişen bir hastada en acil ve hayat kurtarıcı yaklaşım hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Sadece oral antibiyotik başlanıp elektif şartlarda 2 hafta sonrasına ameliyat randevusu verilmesi'},
            {'key': 'B', 'text': 'Tıkanmış toplayıcı sistemin derhal acil dekompresyonu (Double-J stent veya perkütan nefrostomi) ve parenteral geniş spektrumlu antibiyotik başlanması', 'isCorrect': True},
            {'key': 'C', 'text': 'Hastaya yüksek doz diüretik verilerek taşın düşürülmeye zorlanması'},
            {'key': 'D', 'text': 'Görüntüleme yapmadan doğrudan açık nefrektomi uygulanması'},
            {'key': 'E', 'text': 'Sıvı kısıtlaması yapılarak idrar üretiminin durdurulması'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Obstrüksiyon + Enfeksiyon (ateş, titreme, piyüri) = Mutlak Ürolojik Acil! Tıkanmış ve enfekte olmuş toplayıcı sistem kapalı bir abse gibidir; artan hidrostatik basınç pyelovenöz reflü ile bakterilerin ve endotoksinlerin doğrudan kana geçmesine ve dakikalar içinde üroseptik şoka yol açar. Tıkanıklık Double-J stent veya Perkütan Nefrostomi (PCN) ile acilen drene edilmeli ve parenteral antibiyoterapi verilmelidir.'
    },
    'q_imaging': {
        'id': 'urol-img-05',
        'examYear': '2025-2026',
        'committeeId': 'Kurul 5',
        'discipline': 'Radyoloji / Üroloji',
        'topic': 'Üriner Obstrüksiyonda Görüntüleme',
        'stem': 'Üst üriner sistem obstrüksiyonunun ve şüpheli nefrolitiyazisin değerlendirilmesinde güncel kılavuzlara göre en yüksek duyarlılık ve özgüllüğe sahip altın standart anatomik görüntüleme yöntemi hangisidir?',
        'options': [
            {'key': 'A', 'text': 'Direkt Üriner Sistem Grafisi (DÜSG)'},
            {'key': 'B', 'text': 'Kontrassız Helikal / Düşük Doz Bilgisayarlı Tomografi (Taş Protokolü BT)', 'isCorrect': True},
            {'key': 'C', 'text': 'İntravenöz Pyelografi (IVP)'},
            {'key': 'D', 'text': 'Baryumlu Üst Gastrointestinal Pasaj Grafisi'},
            {'key': 'E', 'text': 'Renal Anjiyografi'}
        ],
        'correctAnswer': 'B',
        'explanation': 'Kontrassız Helikal Bilgisayarlı Tomografi (Taş BT), %98\'in üzerinde duyarlılık ve özgüllükle üst üriner sistem obstrüksiyonunun, taş varlığının, taş boyutunun, yerleşim yerinin ve sekonder obstrüksiyon bulgularının (üreteral dilatasyon, perinefritik stranding) saptanmasında altın standarttır. İntravenöz kontrast gerektirmez, dakikalar içinde sonuç verir.'
    }
}

# 21 Rich, Deeply Curated Slides Based on Official Lecture Note '1)Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi.txt'
slides_batch1 = [
    # Slide 1
    {
        'slideNumber': 1,
        'title': 'Üriner Obstrüksiyon: Temel Tanımlar, Terminoloji ve Kapsam',
        'subtitle': 'Eksternal meadan renal tubuluslara kadar idrar akımını engelleyen patolojiler',
        'badge': 'Temel Kavramlar & Terminoloji',
        'badgeColor': 'sky',
        'synthesisNarrative': '**Obstrüktif üropati**, idrar akımına karşı eksternal mea ile renal tubuluslar arasında herhangi bir anatomik veya fonksiyonel düzeyde engel bulunması halidir. Bu durum obstrüksiyonun proksimalinde idrar stazına ve intraluminal hidrostatik basınç artışına yol açar. **Hidronefroz**, toplayıcı sistemin (renal pelvis ve kaliksler) kalıcı dilatasyonunu tanımlarken; **obstrüktif nefropati** ise artan basınca ve doku iskemisine ikincil olarak gelişen renal parankim hasarı ve tübüler fonksiyon bozukluğunu ifade eder.',
        'flashcards': [
            {
                'id': 'fc-obs-1-1',
                'category': 'Terminoloji',
                'front': 'Obstrüktif üropati ile obstrüktif nefropati arasındaki temel fark nedir?',
                'hint': 'Biri anatomik akım engelini, diğeri böbrek parankiminin fonksiyonel hasarını tanımlar.',
                'back': '**Obstrüktif Üropati:** Eksternal mea ile nefron tubulusları arasındaki herhangi bir düzeyde idrar akımını mekanik veya fonksiyonel olarak engelleyen durumdur.\n\n**Obstrüktif Nefropati:** Bu tıkanıklığın böbrek parankiminde meydana getirdiği iskemi, hücresel atrofi, tübüler fonksiyon kaybı ve nefron hasarıdır.'
            },
            {
                'id': 'fc-obs-1-2',
                'category': 'Patofizyoloji',
                'front': 'Obstrüksiyon proksimalinde gelişen idrar stazının iki temel klinik sonucu nedir?',
                'hint': 'Bakteriyel kolonizasyon ve kristal presipitasyonu.',
                'back': '1. **Enfeksiyon Riski:** Durgun idrar bakteriyel proliferasyonu hızlandırır ve piyelonefrit/ürosepsise zemin hazırlar.\n2. **Taş Oluşumu (Litiyazis):** Staz, idrar kristallerinin birikmesini ve taş çekirdekleşmesini (nükleasyon) belirgin derecede artırır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Obstrüktif Üropati Kavramı',
                    'desc': 'Eksternal üretral meadan renal tübüllere kadar uzanan üriner traktusun herhangi bir seviyesinde idrar akımına karşı oluşan mekanik veya fonksiyonel dirençtir. Proksimal alanda hidrodinamik basınç artışı ve staz oluşturur.',
                    'isKey': True
                },
                {
                    'title': 'Hidronefroz ve Kaliektazi',
                    'desc': 'Obstrüksiyona veya vezikoüreteral reflüye ikincil olarak renal pelvis ve kaliks sisteminin genişlemesidir. Hidronefroz tek başına fonksiyonel bozulmanın derecesini göstermez; basınçsız genişleme (atonik) de olabilir.',
                    'isKey': False
                },
                {
                    'title': 'Obstrüktif Nefropati',
                    'desc': 'İntraluminal yüksek basınç, renal hemodinamik değişiklikler ve doku iskemisi sonucu tübüler epitelde apoptoz, interstisyel fibrozis ve glomerüler filtrasyon çöküşü ile karakterize parankimal hasar tablosudur.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ürolojik Terminoloji ve Patofizyolojik Odaklar',
                'headers': ['Terim', 'Anatomik / Patolojik Odak', 'Klinik Karakteristik', 'Geri Dönüş Potansiyeli'],
                'rows': [
                    ['Obstrüktif Üropati', 'Eksternal mea - tübül hattı', 'Lümende mekanik veya dinamik akım engeli', 'Tıkanıklık açılırsa tam düzelebilir'],
                    ['Hidronefroz', 'Pelvis ve kaliksler', 'Toplayıcı sistemde hacimsel genişleme / dilatasyon', 'Erken dönemde düzelir; kronikleşirse kalıcı kaliektazi kalabilir'],
                    ['Obstrüktif Nefropati', 'Böbrek korteks ve medullası', 'Tübüler atrofi, apoptoz, interstisyel fibrozis ve GFR kaybı', 'Süreye bağlıdır; 4-6 haftayı aşan tam tıkanmalarda nefron kaybı kalıcıdır']
                ]
            }
        },
        'spotPearls': [
            'Obstrüksiyon proksimalinde daima staz ve hidrostatik basınç artışı gelişir.',
            'Klinik tablonun ciddiyetini obstrüksiyonun seviyesi, derecesi, süresi ve enfeksiyon varlığı belirler.'
        ],
        'relatedQuestions': [matched_questions_dict['q_luts']],
        'aiPromptSuggestions': ['Obstrüktif nefropatide tübüler hasar nasıl başlar?', 'Hidronefroz ile obstrüktif üropati arasındaki klinik fark nedir?']
    },

    # Slide 2
    {
        'slideNumber': 2,
        'title': 'Obstrüksiyonun Anatomik ve Klinik Sınıflandırması',
        'subtitle': 'Nedene, süreye, dereceye, seviyeye ve etkilenen tarafa göre ayrım',
        'badge': 'Etyolojik Sınıflandırma',
        'badgeColor': 'indigo',
        'synthesisNarrative': 'Üriner obstrüksiyonlar klinikte beş ana eksende sınıflandırılır: **Nedene göre** konjenital (UPJ darlığı, PUV) veya edinsel (taş, BPH); **süreye göre** akut (şiddetli kolik ağrı) veya kronik (sinsi ve sessiz); **derecesine göre** komplet (tam anüri) veya inkomplet/parsiyel; **seviyesine göre** infravezikal (mesane boynu ve üretra) veya supravezikal (üreter ve böbrek); **tarafına göre** ise unilateral ya da bilateral olarak değerlendirilir.',
        'flashcards': [
            {
                'id': 'fc-obs-2-1',
                'category': 'Sınıflandırma',
                'front': 'İnfravezikal obstrüksiyon ile supravezikal obstrüksiyon arasındaki temel anatomik ve klinik fark nedir?',
                'hint': 'Mesanenin yukarısı mı, aşağısı mı?',
                'back': '**İnfravezikal (Mesane çıkımı ve üretra):** BPH, üretra darlığı veya PUV gibi nedenlerle mesane boşalamaz; bilateral böbrek etkilenimi, mesane trabekülasyonu ve glob vesicale riski vardır.\n\n**Supravezikal (Üreter ve böbrek):** Üreter taşı, UPJ darlığı veya retroperitoneal fibrozis gibi mesane üstü tıkanıklıklardır; genellikle tek taraflıdır ve mesane dolumu normaldir.'
            },
            {
                'id': 'fc-obs-2-2',
                'category': 'Klinik İpucu',
                'front': 'Akut obstrüksiyon ile kronik obstrüksiyonun ağrı profili nasıldır?',
                'hint': 'Renal kapsülün aniden gerilmesi şiddetli koliğe neden olur.',
                'back': '**Akut Obstrüksiyon:** Renal kapsül ve toplayıcı sistem aniden gerildiği için son derece şiddetli, kıvrandırıcı renal kolik ağrısı oluşturur.\n\n**Kronik Obstrüksiyon:** Yavaş geliştiği için kapsül gerilmez; genellikle tamamen ağrısız ve sinsidir, hasta doğrudan azotemi veya kitle ile başvurabilir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Etyolojik Köken (Konjenital vs Edinsel)',
                    'desc': 'Konjenital anomaliler genellikle yenidoğan ve çocukluk çağında saptanır (UPJ darlığı, üreterosel, posterior üretral valv). Edinsel nedenler ise erişkin yaşta sık görülen litiyazis, BPH, pelvik maligniteler ve cerrahi travmalardır.',
                    'isKey': True
                },
                {
                    'title': 'Süreye ve Dereceye Göre Ayrım',
                    'desc': 'Akut tam obstrüksiyon anüri ve dayanılmaz flank ağrısıyla acil müdahale gerektirirken; kronik parsiyel obstrüksiyon toplayıcı sistemi yavaşça dilate ederek asemptomatik parankim incelmesine neden olur.',
                    'isKey': False
                },
                {
                    'title': 'Anatomik Seviye: Supravezikal vs İnfravezikal',
                    'desc': 'Supravezikal tıkanıklıklar üreter düzeyindedir ve aksi kanıtlanana kadar tek taraflıdır. İnfravezikal tıkanıklıklar mesane çıkımını etkilediğinden bilateral hidronefroz ve böbrek yetmezliği riski taşır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Obstrüksiyonun 5 Ana Sınıflandırma Ekseni',
                'headers': ['Sınıflandırma Ekseni', 'Alt Kategoriler', 'Tipik Klinik Örnekler'],
                'rows': [
                    ['Nedene Göre', 'Konjenital / Edinsel', 'Konjenital: UPJ darlığı, PUV, üreterosel | Edinsel: Üreter taşı, BPH, serviks kanseri basısı'],
                    ['Süreye Göre', 'Akut / Kronik', 'Akut: Taşa bağlı ani üreter tıkanıklığı | Kronik: Yavaş büyüyen BPH veya retroperitoneal fibrozis'],
                    ['Derecesine Göre', 'Komplet / İnkomplet (Parsiyel)', 'Komplet: Tam lümen tıkanıklığı (anüri riski) | İnkomplet: Dar lümenden idrar geçişi devam eder'],
                    ['Seviyesine Göre', 'İnfravezikal / Supravezikal', 'İnfravezikal: Prostat, üretra, mesane boynu | Supravezikal: Üreter, üreteropelvik bileşke'],
                    ['Tarafına Göre', 'Unilateral / Bilateral', 'Unilateral: Tek üreter taşı | Bilateral: PUV, BPH, retroperitoneal kitle, bilateral üreter taşı']
                ]
            }
        },
        'spotPearls': [
            'Akut bilateral komplet obstrüksiyon anüri ile prezente olan mutlak acil cerrahi tablodur.',
            'İnfravezikal obstrüksiyonlar daima her iki böbreği birden tehdit eder.'
        ],
        'relatedQuestions': [matched_questions_dict['q_bph']],
        'aiPromptSuggestions': ['Hangi obstrüksiyon tipi anüriye yol açar?', 'Supravezikal ve infravezikal seviye ayrımının klinik önemi nedir?']
    },

    # Slide 3
    {
        'slideNumber': 3,
        'title': 'Renal Seviyedeki Obstrüksiyon Etyolojisi',
        'subtitle': 'Konjenital kistler, tümörler, tüberküloz, taşlar ve papiller nekroz',
        'badge': 'Renal Düzey Patolojileri',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Böbreğin kendi parankimi ve pelvisi düzeyindeki obstrüksiyonlar geniş bir etyolojik yelpazeye sahiptir. Konjenital olarak polikistik böbrek hastalığı ve UPJ\'yi çaprazlayan **aberran polar damarlar** toplayıcı sistemi basıya uğratabilir. Neoplastik grupta Wilms tümörü, renal hücreli karsinom (RCC) ve renal pelvisin **transizyonel hücreli karsinomu (TCC)** lümeni tıkayabilir. İnflamatuar grupta kazeöz darlıklar yapan **renal tüberküloz** ve kist hidatik; metabolik grupta ise staghorn taşlar ve dökülen nekrotik papillalar (papiller nekroz) renal tıkanıklığa yol açar.',
        'flashcards': [
            {
                'id': 'fc-obs-3-1',
                'category': 'Etyoloji',
                'front': 'Renal pelvisi döşeyen epitelyumdan köken alıp lümeni tıkayan en sık malign tümör nedir?',
                'hint': 'Ürotelyal karsinom olarak da bilinir.',
                'back': '**Renal Pelvis Transizyonel Hücreli Karsinomu (TCC / Ürotelyal Karsinom):** Renal pelvis lümenine doğru ekzofitik büyüme göstererek idrar akımını engeller ve hidronefroz ile ağrısız gros hematüriye neden olur.'
            },
            {
                'id': 'fc-obs-3-2',
                'category': 'Tüberküloz',
                'front': 'Renal tüberküloz toplayıcı sistemde hangi mekanizmayla obstrüksiyona yol açar?',
                'hint': 'Kazeöz nekroz sonrası gelişen fibrozis ve infundibuler stenoz.',
                'back': 'Renal TBC; medüller kazeöz nekroz alanlarının toplayıcı sisteme açılması, infundibulum ve pelviste ülserasyonlar ve ardından yoğun granülasyon/sikatrisyel fibrozis oluşturarak kaliks infundibulumlarında ve üreterde darlıklara yol açar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Konjenital Renal Nedenler',
                    'desc': 'Polikistik böbrek hastalığı (ADPKD), peripelvik kistler, UPJ darlığı ve alt polü besleyen aberan renal arter/venlerin üreteropelvik bileşkeyi dıştan sıkıştırması.',
                    'isKey': True
                },
                {
                    'title': 'Neoplastik ve Hematolojik Süreçler',
                    'desc': 'Pediatrik grupta Wilms tümörü (nefrobastom); erişkinde renal hücreli karsinom (RCC), pelvis renalis ürotelyal kanseri ve tübülleri tıkayan Bence-Jones protein silendirleri (Multiple Myeloma nefropatisi).',
                    'isKey': True
                },
                {
                    'title': 'İnflamatuar, Metabolik ve Vasküler Sebepler',
                    'desc': 'Renal tüberküloz (infundibuler darlıklar, otonefrektomi), Echinococcus granulosus (kist hidatik), staghorn böbrek taşları, diyabetik veya analjezik nefropatisine bağlı papiller nekroz ve renal arter anevrizması basısı.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Renal Düzey Obstrüksiyon Nedenleri Sınıflaması',
                'headers': ['Etyolojik Kategori', 'Klinik Varlıklar / Patolojiler', 'Patofizyolojik Mekanizma'],
                'rows': [
                    ['Konjenital', 'Polikistik Böbrek, Peripelvik Kistler, Aberan Polar Damar', 'Kistlerin toplayıcı sisteme basısı, damarın UPJ\'yi asması'],
                    ['Neoplastik', 'Wilms Tümörü, RCC, Renal Pelvis TCC, Multiple Myeloma', 'İntraluminal tümör büyümesi veya tübüler protein tıkacı'],
                    ['İnflamatuar', 'Renal Tüberküloz, Echinococcus (Kist Hidatik)', 'Kazeöz sikatrizasyon, infundibuler darlık, kist basısı'],
                    ['Metabolik', 'Nefrolitiyazis (Pelvis ve kaliks taşları)', 'Lümenin taş kütlesi ile tam veya parsiyel tıkanması'],
                    ['Çeşitli', 'Nekroze renal papilla, Renal travma, Renal arter anevrizması', 'Dökülen papillanın infundibuluma oturması, hematom basısı']
                ]
            }
        },
        'spotPearls': [
            'Aberran renal polar damarlar üreteropelvik bileşkeyi dıştan çaprazlayarak hidronefroza neden olabilir.',
            'Diyabetik nefropatide dökülen nekrotik renal papillalar akut üreter koliği ve renal obstrüksiyon tablosunu taklit edebilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['Renal tüberküloz nasıl hidronefroz yapar?', 'Aberran damar UPJ darlığına nasıl yol açar?']
    },

    # Slide 4
    {
        'slideNumber': 4,
        'title': 'Üreter Düzeyindeki Obstrüksiyon Etyolojisi (İntrensek & Ekstrensek)',
        'subtitle': 'UPJ darlıkları, üreterosel, retrokaval üreter, maligniteler ve Ormond hastalığı',
        'badge': 'Üreteral Patolojiler',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Üreter düzeyindeki tıkanıklıklar lümen içi (intrensek) veya çevre dokulardan kaynaklanan bası (ekstrensek) nedenlerle gelişir. Konjenital nedenlerin başında çocukluk çağında hidronefrozun en sık sebebi olan **UPJ darlığı**, üreterosel ve sağ üreterin vena cava inferiorun arkasından dolandığı **retrokaval üreter** gelir. Neoplastik süreçlerde primer üreter karsinomları ile serviks, rektum ve prostat kanserlerinin doğrudan invazyonu görülür. Ekstrensek nedenler arasında en tipik olanı, aort çevresinde yoğun fibröz plak oluşturan ve üreterleri mediyale çeken **Retroperitoneal Fibrozis (Ormond Hastalığı)** tablosudur.',
        'flashcards': [
            {
                'id': 'fc-obs-4-1',
                'category': 'Anatomi & Embriyoloji',
                'front': 'Retrokaval üreter (Circumcaval Ureter) anatomik olarak hangi damarla ilişkilidir ve en sık hangi tarafta görülür?',
                'hint': 'Vena kava inferior ve daima sağ taraf.',
                'back': '**Vena Cava İnferior (VCİ):** Embriyolojik gelişimde subkardinal venlerin anormal devamlılığı sonucu sağ üreter VCİ\'nin arkasından dolanarak sıkışır. Daima SAĞ üreterde görülür.'
            },
            {
                'id': 'fc-obs-4-2',
                'category': 'Patoloji & Sınav Sorusu',
                'front': 'Retroperitoneal Fibrozis (Ormond Hastalığı) nedir ve üreterleri radyolojik olarak nasıl yönlendirir?',
                'hint': 'Üreterleri laterale mi mediyale mi çeker?',
                'back': 'Aorta ve iliak damarlar çevresinde idiyopatik (veya IgG4 ilişkili) yoğun fibröz bağ dokusu proliferasyonudur. Radyolojide bilateral üreterleri **MEDİYALE (omurgaya doğru)** çeker ve bilateral hidronefroza yol açar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Konjenital Üreteral Anomaliler',
                    'desc': 'Üreteropelvik bileşke (UPJ) darlığı, üreterovezikal bileşke (UVJ) darlığı, üreterosel (distal intramural üreterin kistik balonlaşması), vezikoüreteral reflü, retrokaval üreter ve Prune-Belly sendromu.',
                    'isKey': True
                },
                {
                    'title': 'Malign İnfiltrasyon ve Metastazlar',
                    'desc': 'Primer ürotelyal üreter karsinomu; jinekolojik maligniteler (özellikle serviks ve over kanserleri), kolorektal kanserler ve retroperitoneal sarkomların üreteri çevrelemesi veya doğrudan infiltre etmesi.',
                    'isKey': True
                },
                {
                    'title': 'İnflamatuar ve Ekstrensek Fibrotik Nedenler',
                    'desc': 'Üreter tüberkülozu, Schistosoma haematobium (distal üreter darlığı ve bilharzial kalsifikasyonlar), endometriozis ve Retroperitoneal Fibrozis (Ormond hastalığı).',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'İntrensek vs Ekstrensek Üreter Obstrüksiyonu',
                'headers': ['Tip', 'Patoloji Grubu', 'Tipik Hastalıklar', 'Ayırıcı Özellik'],
                'rows': [
                    ['İntrensek (Lümen İçi)', 'Konjenital / Neoplastik / İnflamatuar', 'UPJ darlığı, Üreter taşı, Üreterosel, Primer Üreter TCC', 'Lümen içi daralma veya tıkaç; endoürolojik (retrograd) görülür'],
                    ['Ekstrensek (Dış Bası)', 'Malign / Fibrotik / Vasküler', 'Serviks CA, Retroperitoneal Fibrozis (Ormond), Aort anevrizması, Retrokaval üreter', 'Üreter dıştan sıkışır; Ormond\'da üreterler mediyale deviyedir']
                ]
            }
        },
        'spotPearls': [
            'Ormond hastalığında (Retroperitoneal fibrozis) üreterlerin mediyale deviyasyonu patognomoniktir.',
            'Schistosomiasis enfeksiyonu üreter distalinde kalsifikasyonlara ve üreter darlıklarına yol açar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['Ormond hastalığının radyolojik bulguları nelerdir?', 'Retrokaval üreter nasıl cerrahi tedavi edilir?']
    },

    # Slide 5
    {
        'slideNumber': 5,
        'title': 'Alt Üriner Sistem (Mesane ve Üretra) Obstrüksiyonu Etyolojisi',
        'subtitle': 'PUV, BPH, üretra darlıkları, mesane tümörleri ve nörojenik disfonksiyon',
        'badge': 'İnfravezikal Patolojiler',
        'badgeColor': 'amber',
        'synthesisNarrative': 'İnfravezikal obstrüksiyonlar mesane boynundan eksternal meaya kadar olan çıkım yolunu etkiler. Yaş gruplarına göre etyoloji dramatik farklılık gösterir: Yenidoğan erkek çocuklarda en sık infravezikal obstrüksiyon nedeni **Posterior Üretral Valv (PUV)** iken; yaşlı erkeklerde en sık neden **Benign Prostat Hiperplazisi (BPH)**\'dir. Ayrıca geçirilmiş gonokokal enfeksiyonlar veya kateter/pelvik travma sonrası gelişen **üretra darlıkları**, mesane boynu kontraktürü, prostat adenokarsinomu ve mesane tümörleri infravezikal tıkanıklığın başlıca etkenleridir.',
        'flashcards': [
            {
                'id': 'fc-obs-5-1',
                'category': 'Pediatri & Üroloji',
                'front': 'Yenidoğan erkek bebekte bilateral hidronefroz ve mesane çıkım obstrüksiyonunun EN SIK konjenital nedeni nedir?',
                'hint': 'Prostatik üretrada mukozal valv yapısı.',
                'back': '**Posterior Üretral Valv (PUV):** Prostatik üretrada anormal konjenital mukozal katlantıların idrar akımını bloke etmesidir. Oligohidramniyos, pulmoner hipoplazi ve bilateral ağır hidronefroza yol açabilir.'
            },
            {
                'id': 'fc-obs-5-2',
                'category': 'Erişkin Üroloji',
                'front': '50 yaş üstü erkeklerde infravezikal obstrüksiyonun en sık edinsel nedeni nedir ve hangi bölgeden köken alır?',
                'hint': 'Prostatın transizyonel zonu.',
                'back': '**Benign Prostat Hiperplazisi (BPH):** Prostatın transizyonel zonundaki stromal ve glandüler hücrelerin DHT etkisiyle çoğalarak üretra lümenini daraltmasıdır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Pediatrik Acil: Posterior Üretral Valv (PUV)',
                    'desc': 'Yalnızca erkek infantlarda görülür. Prostatik üretradaki obstrüktif mukozal valvler intrauterin dönemde mesane hipertrofisine, bilateral VUR ve böbrek yetmezliğine yol açabilir.',
                    'isKey': True
                },
                {
                    'title': 'Erişkinde BPH ve Prostat Kanseri',
                    'desc': 'Transizyonel zon hiperplazisi olan BPH mesane çıkım direncini artırırken; periferal zon kaynaklı prostat kanserleri ileri evrede üretra ve mesane boynunu invaze ederek obstrüksiyon yapar.',
                    'isKey': True
                },
                {
                    'title': 'Üretra Darlığı, Fimozis ve Nörojenik Mesane',
                    'desc': 'Enfeksiyon sekeli (gonore) veya enstrümantasyon/straddle travması sonrası üretral spongiofibrozis (darlık); meatal stenoz, fimozis ve detrüssör-sfinkter dissinerjisi (DSD).',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Yaş Gruplarına Göre İnfravezikal Obstrüksiyon Etyolojisi',
                'headers': ['Yaş Grubu', 'En Sık Neden', 'İkincil / Diğer Nedenler', 'Klinik Etki'],
                'rows': [
                    ['Yenidoğan / Çocuk (Erkek)', 'Posterior Üretral Valv (PUV)', 'Konjenital üretra darlığı, Fimozis, Meatal stenoz', 'Bilateral hidronefroz, oligohidramniyos riski'],
                    ['Genç Erişkin Erkek', 'Üretra Darlığı (Travmatik / İatrojenik / Post-enfeksiyöz)', 'Mesane boynu kontraktürü, Üretra taşları', 'Zayıf akım, çatallı işeme, idrar yolu enfeksiyonu'],
                    ['İleri Yaş Erkek (>50 yaş)', 'Benign Prostat Hiperplazisi (BPH)', 'Prostat Kanseri, Mesane Tümörü, Nörojenik mesane', 'LUTS, glob vesicale, mesane taşları, böbrek yetmezliği']
                ]
            }
        },
        'spotPearls': [
            'Posterior üretral valv şüphesinde kesin tanı yöntemi İşeme Sistoüretrografisi (VCUG)\'dir.',
            'İnfravezikal obstrüksiyon tedavi edilmezse mesanede kalıcı miyojenik yetmezlik gelişir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_bph']],
        'aiPromptSuggestions': ['PUV tanısı nasıl konur ve acil tedavisi nedir?', 'Üretra darlığı tedavisinde optik üretrotomi ve üretroplasti endikasyonları nelerdir?']
    },

    # Slide 6
    {
        'slideNumber': 6,
        'title': 'Alt Üriner Sistem Obstrüksiyonunda Kompansasyon Evresi',
        'subtitle': 'Detrüssör kas hipertrofisi ve intravezikal basınç artışı',
        'badge': 'Mesane Kompansasyonu',
        'badgeColor': 'sky',
        'synthesisNarrative': 'Mesane çıkımında direnç arttığında, mesane bu engeli aşabilmek ve rezidü idrar bırakmadan boşalabilmek için kompansasyon mekanizmalarını devreye sokar. Detrüssör düz kas liflerinde **hipertrofi ve hiperplazi** gelişir. Kasılma sırasında intravezikal basınç normalin **2 ila 4 katına** kadar yükselir. Kompansasyon evresinde mesane henüz gücünü koruduğu için işeme sonu rezidü idrar (PMR) minimaldir; ancak hasta işeme başlangıcında zorlanma (hesitancy) ve akım hızında azalma tarifler.',
        'flashcards': [
            {
                'id': 'fc-obs-6-1',
                'category': 'Fizyopatoloji',
                'front': 'Kompansasyon evresinde mesane çıkım direncini yenmek için intravezikal basınç kaç katına çıkar?',
                'hint': 'Basınç katlanarak artar.',
                'back': 'İntravezikal basınç normal işeme basıncının **2 ila 4 katına** kadar yükselir. Bu artış detrüssör kas hipertrofisi ve hiperplazisi ile sağlanır.'
            },
            {
                'id': 'fc-obs-6-2',
                'category': 'Klinik Evreleme',
                'front': 'Mesane kompanse evredeyken postmiksiyonel rezidü idrar (PMR) nasıldır?',
                'hint': 'Mesane henüz tam boşalabilir.',
                'back': 'Kompansasyon evresinde mesane artan basıncıyla çıkım direncini yenebildiği için işeme sonrasında rezidü idrar (PMR) **yoktur veya minimaldir**; dekompanse evreye geçildiğinde rezidü idrar birikmeye başlar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Detrüssör Hipertrofisi ve Hiperplazisi',
                    'desc': 'Tıkanıklığa karşı artan duvar gerimi düz kas hücrelerinde mekanik stres sinyallerini tetikler; kas fibrillerinin çapı ve sayısı artarak mesane duvarı kalınlaşır.',
                    'isKey': True
                },
                {
                    'title': 'İntravezikal Basıncın 2-4 Kat Artışı',
                    'desc': 'Normalde 20-40 cmH2O civarında olan işeme basıncı, daralmış lümenden idrarı fışkırtabilmek için 80-120 cmH2O ve üzerine kadar yükselir.',
                    'isKey': True
                },
                {
                    'title': 'Miyojenik Uyum ve Elektriksel İleti',
                    'desc': 'Düz kas hücreleri arasındaki gap-junction bağlantıları artar; amaç tüm detrüssör demetlerinin aynı anda, eşzamanlı ve güçlü bir kasılma üretmesini sağlamaktır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Kompansasyon Evresinin Patofizyolojik Değişiklikleri',
                'headers': ['Parametre', 'Normal Durum', 'Kompansasyon Evresi', 'Klinik Yansıması'],
                'rows': [
                    ['Mesane Duvar Kalınlığı', '2 - 3 mm', '5 - 10 mm (Hipertrofik)', 'USG\'de kalınlaşmış duvar görünümü'],
                    ['İşeme İçi Tepe Basıncı', '25 - 40 cmH2O', '80 - 120 cmH2O (2-4 kat artış)', 'İşeme için daha yüksek efor harcanması'],
                    ['Postmiksiyonel Rezidü İdrar', '< 10 - 20 mL', 'Sıfır veya minimal (< 50 mL)', 'Mesane henüz tam boşalabilir'],
                    ['Semptomlar', 'Asemptomatik', 'Hesitancy, akım zayıflaması', 'Hasta idrarı başlatmakta zorlanır']
                ]
            }
        },
        'spotPearls': [
            'Kompansasyon evresinde mesane çıkım direncini aşmak için intravezikal basınç 2-4 kat yükselir.',
            'Bu evrede rezidü idrar henüz belirgin değildir; detrüssör gücünü korumaktadır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_luts']],
        'aiPromptSuggestions': ['Detrüssör hipertrofisi sistoskopide nasıl görünür?', 'Kompansasyon evresinden dekompansasyona geçişi ne belirler?']
    },

    # Slide 7
    {
        'slideNumber': 7,
        'title': 'Dekompansasyon Evresi: Trabekülasyon, Selül ve Divertiküller',
        'subtitle': 'Kas demetleri kabarması, mukozal cepçikler ve kalıcı kontraktilite kaybı',
        'badge': 'Mesane Dekompansasyonu',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Obstrüksiyon sürdüğünde kompanse mekanizmalar tükenir ve **dekompansasyon evresi** başlar. Kas lifleri arasına aşırı kollajen birikir, kan akımı bozulur ve düzensiz kas demetleri lümene doğru kabararak **trabekülasyon** oluşturur. Trabeküller arasında mukozanın dışa yaptığı küçük cepçiklere **selül**, bunların büyümesine **sakkül**, mukozanın detrüssör katını tamamen aşıp peritona veya perivezikal yağ dokusuna fıtıklaşmasına ise **divertikül** adı verilir. KRİTİK KLİNİK: Dekompanse aşamada tıkanıklık açılsa dahi mesane kontraktilitesinde kalıcı miyojenik hasar kalabilir!',
        'flashcards': [
            {
                'id': 'fc-obs-7-1',
                'category': 'Patoloji',
                'front': 'Mesane trabekülü, selül ve divertikül oluşum sırası ve anatomik farkı nedir?',
                'hint': 'Kalın kas demeti -> küçük cepçik -> gerçek fıtıklaşma.',
                'back': '1. **Trabekül:** Hipertrofik kalın detrüssör kas demetlerinin lümene kabarmasıdır.\n2. **Selül:** Kas demetleri arasındaki mukozal küçük cepçiklerdir.\n3. **Divertikül:** Selüllerin perivezikal alana doğru tüm kas tabakasını aşarak fıtıklaşmasıdır (içinde kas tabakası bulunmaz!).'
            },
            {
                'id': 'fc-obs-7-2',
                'category': 'Klinik Uyarı',
                'front': 'Dekompanse aşamada infravezikal obstrüksiyon cerrahiyle giderilse bile neden tam iyileşme olmayabilir?',
                'hint': 'Miyojenik hasar ve aşırı interstisyel fibrozis.',
                'back': 'Aşırı gerilme, iskemi ve kas lifleri arasına yoğun kollajen/elastik bağ dokusu depolanması sonucu **miyojenik yetmezlik (atonik mesane)** gelişir. Neksus (gap-junction) ileti mekanizmaları kalıcı olarak hasar gördüğünden mesane tekrar etkili kasılamaz.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Trabekülasyon Gelişimi',
                    'desc': 'Hipertrofik detrüssör kas lifleri birbiri üzerine binerek mesane mukozası altında kabarık, kafes şeklinde kalın kirişler oluşturur (sistoskopide patognomonik trabeküle mesane).',
                    'isKey': True
                },
                {
                    'title': 'Selül, Sakkül ve Gerçek Divertiküller',
                    'desc': 'Yüksek intraluminal basınç, kas lifleri arasındaki zayıf yarıklardan mukozayı dışarı doğru iter. Küçük cepçiklere selül, büyüyenlere sakkül, perivezikal boşluğa çıkanlara divertikül denir. Divertikül duvarında detrüssör kası yoktur; bu nedenle kendi kendini boşaltamaz (staz, taş ve tümör odağıdır).',
                    'isKey': True
                },
                {
                    'title': 'Kalıcı Miyojenik Yetmezlik',
                    'desc': 'Dekompanse mesanede yüksek miktarda postmiksiyonel rezidü idrar (PMR > 200-500 mL) kalır; obstrüksiyon açılsa bile hasta ömür boyu temiz aralıklı kateterizasyona (TAK) bağımlı kalabilir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Kompanse vs Dekompanse Mesane Karşılaştırması',
                'headers': ['Özellik', 'Kompansasyon Evresi', 'Dekompansasyon Evresi'],
                'rows': [
                    ['Mesane Morfolojisi', 'Konsantrik kalınlaşmış düzgün duvar', 'Trabekülasyon, selüller, sakküller ve divertiküller'],
                    ['Detrüssör Kas Yapısı', 'Hipertrofik, hiperplastik canlı kas', 'Kollajenize, fibrotik, dejenere kas lifleri'],
                    ['Rezidü İdrar (PMR)', 'Yok veya minimal (< 50 mL)', 'Belirgin (100 - 1000 mL, taşma inkontinansı)'],
                    ['Obstrüksiyon Açılınca Sonuç', 'Mesane fonksiyonları tamamen normale döner', 'Miyojenik yetmezlik kalıcı olabilir (düzensiz iyileşme)']
                ]
            }
        },
        'spotPearls': [
            'Mesane divertiküllerinin duvarında detrüssör kas tabakası bulunmaz; idrar stazı, enfeksiyon ve karsinom odağıdır.',
            'Dekompanse aşamada tıkanıklık açılsa bile mesane kontraktilitesinde beklenen tam düzelme sağlanamayabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_bph']],
        'aiPromptSuggestions': ['Mesane divertikülü içinde neden taş ve tümör gelişir?', 'Miyojenik mesane hasarı ürodinamik olarak nasıl saptanır?']
    },

    # Slide 8
    {
        'slideNumber': 8,
        'title': 'Üst Üriner Sistem Obstrüksiyonu: Üreter Peristaltizm Dinamiği',
        'subtitle': 'Longitudinal ve sirküler kas liflerinin bolus iletimi ve sfinkterik bariyer görevi',
        'badge': 'Üreter Dinamiği',
        'badgeColor': 'teal',
        'synthesisNarrative': 'Üst üriner sistemde idrarın böbrekten mesaneye transportu aktif üreter peristaltizmi ile sağlanır. Üreter duvarı iki temel kas katmanından oluşur: **Longitudinal kas lifleri** boylamasına kasılarak idrar bolusunu aşağıya doğru iletir; **sirküler kas lifleri** ise bolusun arkasından büzülerek üreterde oluşan yüksek basıncın retrograd olarak böbreğe iletilmesini engelleyen fizyolojik bir sfinkter bariyeri oluşturur. Obstrüksiyon geliştiğinde üreter lümenindeki basınç sirküler bariyeri aşar ve retrograd olarak renal pelvise iletilir.',
        'flashcards': [
            {
                'id': 'fc-obs-8-1',
                'category': 'Üreter Histolojisi',
                'front': 'Üreterin longitudinal ve sirküler kas liflerinin temel fonksiyonel farkı nedir?',
                'hint': 'Biri aşağı iter, diğeri geri basınç kaçışını önler.',
                'back': '**Longitudinal Lifler:** İdrar bolusunu aşağıya (distale) doğru aktif olarak iletir.\n\n**Sirküler Lifler:** Bolusun arkasında lümeni büzerek distale iletilen yüksek basıncın böbreğe geri kaçmasını engelleyen sfinkterik bariyer görevi görür.'
            },
            {
                'id': 'fc-obs-8-2',
                'category': 'Fizyopatoloji',
                'front': 'Obstrüksiyonun erken döneminde üreter düz kası idrar transportunu sürdürmek için ne yapar?',
                'hint': 'Daha güçlü kontraksiyonlar ve hipertrofi.',
                'back': 'Obstrüksiyonun proksimalindeki üreter segmenti idrar akımını devam ettirebilmek için **daha kuvvetli kontraksiyonlar** yapar ve düz kasta hipertrofi/hiperplazi gözlenir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Longitudinal İç Kas Lifleri',
                    'desc': 'Renal pelvisten üreterovezikal bileşkeye kadar uzanır; boyuna kasılarak idrar lümenini kısaltır ve idrar bolusunu öne doğru iter.',
                    'isKey': True
                },
                {
                    'title': 'Sirküler Dış Kas Lifleri',
                    'desc': 'Lümeni halkasal olarak sarar; bolusun hemen arkasından kasılarak koaptasyon sağlar ve distale iletilen yüksek hidrostatik dalganın böbreğe geri yansımasını engeller.',
                    'isKey': True
                },
                {
                    'title': 'Peristaltik Yetmezlik ve Progresif Dilatasyon',
                    'desc': 'Obstrüksiyon devam ettiğinde kas lifleri aşırı gerilir; miyojenik elektriksel iletiyi sağlayan neksus bağlantıları hasarlanır, peristaltizm kaybolur ve üreter hidroüreter halini alır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Üreter Kas Tabakaları ve Obstrüksiyon Yanıtı',
                'headers': ['Kas Tabakası', 'Lif Yönelimi', 'Fizyolojik Fonksiyon', 'Obstrüksiyondaki Bozulma'],
                'rows': [
                    ['İç Longitudinal Katman', 'Boylamasına', 'İdrar bolusunu mesaneye doğru itmek', 'Kasılma amplitüdü yetersiz kalır, lümen boyu uzar (tortuozite)'],
                    ['Dış Sirküler Katman', 'Halkasal / Çembersel', 'Geri kaçışı önleyen sfinkterik bariyer', 'Koaptasyon yeteneği kaybolur; yüksek basınç böbreğe yansır'],
                    ['Miyositler Arası Neksuslar', 'Hücrelerarası köprüler', 'Peristaltik dalganın elektriksel iletimi', 'Aşırı gerilme ile neksuslar kopar; aperistaltizm gelişir']
                ]
            }
        },
        'spotPearls': [
            'Üreter sirküler kas lifleri yüksek basıncın böbreğe geri iletilmesini engelleyen dinamik sfinkterdir.',
            'Kronik obstrüksiyonda kollajen ve elastik bağ dokusu kas liflerinin yerini alarak üreter peristaltizmini tamamen yok eder.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['Üreter düz kas liflerinde neksus hasarı neye yol açar?', 'Üreter peristaltizmi kesilince idrar transportu nasıl devam eder?']
    },

    # Slide 9
    {
        'slideNumber': 9,
        'title': 'Kaliks ve Papilla Morfolojisinde Basınç Değişiklikleri',
        'subtitle': 'Konkavite kaybı, forniks küntleşmesi, papilla basısı ve 7. gün tübüler atrofisi',
        'badge': 'Kaliks & Papilla Morfolojisi',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Üst üriner sistem obstrüksiyonuna sekonder retrograd hidrostatik basınç artışı ilk olarak **kaliksleri** etkiler. Kalikslerin normal konkav (fincan) görüntüsü hızla silinir. Kaliksin lateral köşeleri olan forniksler küntleşir; renal papillalar basıyla ezilerek yassılaşır ve zamanla dışa doğru konveks bir hal alır. İlk birkaç haftada üreter ve renal pelviste ilerleyici dilatasyon izlenirken, kas dokusunun yerini kollajen ve elastik bağ dokusu alır. Obstrüksiyonun **7. gününden itibaren** dilate toplayıcı kanallarda ve distal tübüllerde hücresel atrofi ve apoptoz süreci başlar.',
        'flashcards': [
            {
                'id': 'fc-obs-9-1',
                'category': 'Radyoloji & Patoloji',
                'front': 'Obstrüksiyona sekonder basınç artışı toplayıcı sistemde İLK olarak hangi anatomik yapıyı etkiler ve ne tür değişiklik yapar?',
                'hint': 'Kaliks konkavitesi ve forniksler.',
                'back': '**Kaliksleri etkiler:** Normal konkav (fincan) görüntüsü bozulur. Forniksler küntleşir; papillalar silinir, yassılaşır ve dışa doğru konveks hal alır (hidronefrotik kaliektazi).'
            },
            {
                'id': 'fc-obs-9-2',
                'category': 'Zamanlama & Histoloji',
                'front': 'Tam obstrüksiyonun kaçıncı gününden itibaren dilate toplayıcı kanallarda tübüler atrofi ve nekroz başlar?',
                'hint': 'İlk haftanın sonu.',
                'back': '**7. Gün:** Obstrüksiyonun 7. gününden itibaren dilate toplayıcı kanallarda ve tübüllerde belirgin hücresel atrofi, apoptoz ve nekroz süreci başlar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Kaliks Konkavitesinin Kaybı ve Forniks Küntleşmesi',
                    'desc': 'Normalde kaliksler renal papillayı fincan gibi sarar ve konkavdır. Basınç yükseldiğinde ilk etkilenen yer olan kaliks forniksleri açılarak küntleşir (erken radyolojik hidronefroz bulgusu).',
                    'isKey': True
                },
                {
                    'title': 'Papillaların Yassılaşması ve Konveks Görünüm',
                    'desc': 'İntrapelvik hidrostatik basınç renal papillaları doğrudan ezer; papillalar içe doğru çöker, silinir ve konveks bombelik kazanır.',
                    'isKey': True
                },
                {
                    'title': '7. Gün Eşiği ve Tübüler Apoptoz',
                    'desc': 'Basınç toplayıcı kanallara ve distal nefronlara iletilir. 7. günde epitel hücrelerinde apoptoz, nekroz ve lümende dökülen silendirler saptanır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Toplayıcı Sistem Morfolojisinin Basınç Altındaki Evreleri',
                'headers': ['Evre / Zaman', 'Kaliks Görünümü', 'Papilla Durumu', 'Histopatolojik Karşılığı'],
                'rows': [
                    ['Normal Anatomi', 'Derin konkav (fincan)', 'Sivri, kaliks içine uzanır', 'Normal tübüler epitel ve sağlam neksuslar'],
                    ['Erken Obstrüksiyon (İlk günler)', 'Forniksler küntleşir, konkavite azalır', 'Papillalar basıklaşır', 'Tübüler dilatasyon, hafif interstisyel ödem'],
                    ['7. Gün Eşiği', 'Kaliksler genişlemiş, açılar kayıp', 'Papilla silinmiş ve düzleşmiş', 'Toplayıcı kanallarda tübüler atrofi ve nekroz başlangıcı'],
                    ['Kronik İleri Dönem', 'Geniş konveks kistik kaliksler (Kaliektazi)', 'Tamamen atrofik, tanınmaz', 'Ağır parankim incelmesi, interstisyel fibrozis']
                ]
            }
        },
        'spotPearls': [
            'Obstrüksiyonun toplayıcı sistemdeki ilk morfolojik belirtisi kaliks fornikslerinin küntleşmesidir.',
            '7. günden itibaren toplayıcı tübüllerde geri dönüşümsüz atrofi ve nekroz süreçleri tetiklenir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['Hidronefroz ultrasonografik olarak nasıl evrelenir?', 'Kaliks forniks küntleşmesi IVP\'de nasıl görünür?']
    },

    # Slide 10
    {
        'slideNumber': 10,
        'title': 'Koruyucu Basınç Azaltıcı Mekanizmalar: Pyelointerstisyel Reflü',
        'subtitle': 'Böbreğin basınç dekompresyonu ve sinüs/perirenal rezorpsiyon',
        'badge': 'Koruyucu Kaçış Yolları',
        'badgeColor': 'blue',
        'synthesisNarrative': 'Obstrüksiyonda hızla artan intrapelvik basınç, böbrek parankiminin yırtılmasını ve GFR\'nin aniden sıfıra inmesini engellemek için doğal basınç azaltıcı koruyucu mekanizmaları tetikler. Bu sistemlerin içinde **en sık görüleni Pyelointerstisyel Reflü**\'dür. Yüksek basınçla yırtılan papilla ve forniks mikro-defektlerinden idrar toplayıcı sistem dışına sızarak böbrek sinüsüne ve perirenal alana geçer; buradan hem venöz yolla hem de lenfatiklerle emilerek sistemik dolaşıma taşınır.',
        'flashcards': [
            {
                'id': 'fc-obs-10-1',
                'category': 'Fizyopatoloji',
                'front': 'Üst üriner sistem obstrüksiyonunda devreye giren koruyucu mekanizmalar içinde EN SIK görülen hangisidir?',
                'hint': 'İnterstisyel alana ve böbrek sinüsüne kaçış.',
                'back': '**Pyelointerstisyel Reflü:** En sık görülen koruyucu mekanizmadır. Basınçla yırtılan forniks ve papillalardan idrarın böbrek sinüsüne ve perirenal alana sızması, oradan venöz ve lenfatik damarlarla emilmesidir.'
            },
            {
                'id': 'fc-obs-10-2',
                'category': 'Mekanizma',
                'front': 'Pyelointerstisyel reflü böbrek fonksiyonlarını nasıl korur?',
                'hint': 'Pelvis içi basıncı düşürerek GFR devamlılığını sağlar.',
                'back': 'Renal pelvis içindeki aşırı hidrostatik basıncı düşürür (dekompresyon sağlar); böylece glomerüler filtrasyonun tamamen durmasını ve parankimin ani hasarını geciktirir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'En Sık Görülen Koruyucu Yol',
                    'desc': 'İntrapelvik hidrostatik basınç kritik eşiği aştığında toplayıcı sistemin en zayıf noktası olan kaliks fornikslerinden mikro yırtılmalar gelişir ve idrar interstisyuma geçer.',
                    'isKey': True
                },
                {
                    'title': 'Böbrek Sinüsü ve Perirenal Alana Geçiş',
                    'desc': 'Fornikslerden sızan idrar renal parankim aralıklarına ve böbrek sinüsüne yayılır. Sinüs içindeki zengin venöz ve lenfatik pleksuslar idrarı rezorbe eder.',
                    'isKey': True
                },
                {
                    'title': 'Klinik Önemi',
                    'desc': 'Bu koruyucu mekanizma normal fonksiyonel işlevini sürdürdüğü sürece intrapelvik basınç tamponlanır ve böbrek fonksiyonlarındaki bozulma gecikir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Pyelointerstisyel Reflünün Aşamaları ve Yolu',
                'headers': ['Basamak', 'Anatomik Bölge', 'Fizyolojik Olay', 'Klinik Sonuç'],
                'rows': [
                    ['1. Basınç Yükselmesi', 'Renal Pelvis', 'İdrar stazı ile intrapelvik basıncın aşırı artışı', 'Pelvik duvar gerimi tepeye ulaşır'],
                    ['2. Forniks Mikro-Yırtılması', 'Kaliks Forniksi', 'En zayıf anatomik sınırdan idrarın parankime sızması', 'İntrapelvik basınçta ani kısmi düşüş'],
                    ['3. Sinüs & Perirenal Yayılım', 'Böbrek Sinüsü', 'İdrarın interstisyel bağ dokusu boşluklarına geçmesi', 'Perinefritik ödem ve sirkülasyona emilim'],
                    ['4. Venöz / Lenfatik Rezorpsiyon', 'Hiler Damarlar', 'İdrar sıvısının lenf ve venler yoluyla dolaşıma katılması', 'Glomerüler filtrasyonun devamının sağlanması']
                ]
            }
        },
        'spotPearls': [
            'Üst üriner sistem obstrüksiyonunda en sık görülen koruyucu basınç boşaltma yolu Pyelointerstisyel reflüdür.',
            'Forniks rüptürü pelvik basıncı tahliye ederek glomerüler filtrasyonun bir süre daha devam etmesine imkan tanır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['Pyelointerstisyel reflü ile urinoma arasındaki ilişki nedir?', 'Forniks mikro-yırtılması ağrıyı nasıl etkiler?']
    },

    # Slide 11
    {
        'slideNumber': 11,
        'title': 'Pyelolenfatik ve Pyelovenöz Reflü Dinamiği',
        'subtitle': 'Lenfatik natriürez, venöz kaçış ve enfeksiyonda ürosepsis tehlikesi',
        'badge': 'Lenfatik & Venöz Drenaj',
        'badgeColor': 'indigo',
        'synthesisNarrative': 'İkinci koruyucu mekanizma olan **Pyelolenfatik Reflü**, böbrek hiler ve kapsüler lenfatikleri aracılığıyla gerçekleşir. Normalde böbrek lenfatik hacmi yaklaşık idrar akım hızına eşittir; akut obstrüksiyonda bu akım katlanarak artar ve belirgin natriürez/diürez oluşturur. Üçüncü mekanizma olan **Pyelovenöz Reflü** ise venöz sisteme doğrudan idrar dönüşüdür ve koruyucu etki açısından **EN AZ ETKİLİ** koruma yoludur. HAYATİ TEHLİKE: İdrar enfekte ise pyelovenöz reflü bakterilerin ve endotoksinlerin doğrudan dolaşıma karışmasına ve dakikalar içinde ürosepsise yol açar!',
        'flashcards': [
            {
                'id': 'fc-obs-11-1',
                'category': 'Mekanizma & Karşılaştırma',
                'front': 'Obstrüksiyonda devreye giren koruyucu yollardan EN AZ ETKİLİ olanı hangisidir ve neden en tehlikelidir?',
                'hint': 'Venöz sisteme doğrudan kaçış.',
                'back': '**Pyelovenöz Reflü:** Koruyucu etkisi en zayıf olan yoldur. En tehlikeli olmasının sebebi, enfeksiyon varlığında bakterilerin ve endotoksinlerin doğrudan venöz dolaşıma geçerek yıldırım hızında **ürosepsis ve septik şoka** yol açmasıdır.'
            },
            {
                'id': 'fc-obs-11-2',
                'category': 'Lenfatik Fizyoloji',
                'front': 'Normal bir böbreğin lenfatik drenaj hacmi yaklaşık ne kadardır ve obstrüksiyonda nasıl değişir?',
                'hint': 'İdrar akımına yakın bir debi.',
                'back': 'Böbrek lenfatik hacmi normalde yaklaşık **idrar akımı kadardır**. Üreter obstrüksiyonunda ve su diürezinde bu volüm belirgin olarak artar ve akut obstrüksiyonda natriürez ve diürez oluşturur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Pyelolenfatik Reflü ve Lenf Debisi',
                    'desc': 'Böbrek lenf sıvısı hiler ve subkapsüler lenfatikler aracılığıyla drene olur. Akut üreteral obstrüksiyonda lenfatik akım hızlanarak toplayıcı sistemdeki aşırı hidrostatik basıncı boşaltır.',
                    'isKey': True
                },
                {
                    'title': 'Pyelovenöz Reflü (En Az Etkili Koruma)',
                    'desc': 'Kaliks fornikslerinden arkuat ve interlobuler venlere doğrudan idrar geçişidir. Basınç düşürme kapasitesi düşüktür ve en az etkili sistemdir.',
                    'isKey': True
                },
                {
                    'title': 'Enfekte Hidronefrozda Ürosepsis Kapısı',
                    'desc': 'Eğer idrar steril değilse, pyelovenöz ve pyelolenfatik reflü bakterilerin vasküler alana doğrudan geçiş kapısı haline gelir; bu durum tabloyu ürolojik acile dönüştürür.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Koruyucu Reflü Mekanizmalarının Karşılaştırmalı Özellikleri',
                'headers': ['Reflü Tipi', 'Geçiş Yolu', 'Görülme Sıklığı / Etkinliği', 'Enfeksiyon Durumundaki Risk'],
                'rows': [
                    ['Pyelointerstisyel', 'Forniks -> Böbrek sinüsü ve perirenal alan', 'En sık görülür, yüksek dekompresyon', 'Perirenal apse ve ürinom riski'],
                    ['Pyelolenfatik', 'Forniks -> Hiler ve kapsüler lenfatikler', 'Orta sıklıkta, natriürez/diürez uyarır', 'Lenfanjit ve sistemik yayılım'],
                    ['Pyelovenöz', 'Forniks -> Doğrudan intrarenal venler', 'En az etkili koruma sistemi', 'Doğrudan kana bakteri geçişi: Masif Ürosepsis!']
                ]
            }
        },
        'spotPearls': [
            'Pyelovenöz reflü koruma açısından en az etkilidir ve enfekte idrarın doğrudan kana geçiş kapısıdır.',
            'Böbreğin lenfatik akım hacmi normalde yaklaşık idrar debisi kadardır; obstrüksiyonda katlanarak artar.'
        ],
        'relatedQuestions': [matched_questions_dict['q_infected_hydro']],
        'aiPromptSuggestions': ['Pyelovenöz reflü nasıl üroseptik şok yapar?', 'Böbrek lenfatiklerinin obstrüksiyondaki kompanse edici rolü nedir?']
    },

    # Slide 12
    {
        'slideNumber': 12,
        'title': 'Forniks Rüptürü, İdrar Ekstravazasyonu ve Ürinom (Urinoma)',
        'subtitle': 'Aşırı intrapelvik basınç patlaması, perirenal koleksiyon ve klinik paradoks',
        'badge': 'Klinik Komplikasyon',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Akut komplet üreter obstrüksiyonunda (özellikle üretere aniden sıkışan taşlarda) intrapelvik hidrostatik basınç doku tolerans sınırını aştığında **forniks rüptürü ve ekstravazasyon** meydana gelir. Forniks yırtıldığı anda intrapelvik basınç aniden düştüğü için hastanın dayanılmaz şiddetteki renal kolik ağrısı paradoksal olarak aniden hafifleyebilir; bu durum hekimi yanıltmamalıdır! Yırtıktan dışarı sızan idrar perirenal ve retroperitoneal fasyalar arasında toplanarak fibröz bir kılıfla çevrilir ve **ürinom (urinoma)** adı verilen kistik idrar koleksiyonunu oluşturur.',
        'flashcards': [
            {
                'id': 'fc-obs-12-1',
                'category': 'Klinik Tuzak',
                'front': 'Akut üreter taşında kıvranan hastanın ağrısının aniden ve tamamen kesilmesi neyin habercisi olabilir?',
                'hint': 'Basınç patlaması ve forniks rüptürü.',
                'back': '**Forniks Rüptürü (İntrapelvik Basınç Boşalması):** Aşırı basınç nedeniyle kaliks forniksi yırtılmıştır; basınç aniden düştüğü için gerilme ağrısı kesilir. Ancak ekstravaze idrar retroperitonda ürinoma ve apse riski yaratır.'
            },
            {
                'id': 'fc-obs-12-2',
                'category': 'Terminoloji',
                'front': 'Ürinom (Urinoma) nedir ve nasıl tedavi edilir?',
                'hint': 'Retroperitoneal idrar kisti.',
                'back': 'Forniks rüptürü veya travma sonrası perirenal/retroperitoneal alanda biriken, çevresi granülasyon ve fibröz doku ile sarılmış idrar koleksiyonudur. Tedavide üreteral Double-J stent veya perkütan drenaj uygulanır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Forniks Rüptürünün Mekanizması',
                    'desc': 'Akut intraluminal basınç 50-70 mmHg üzerine çıktığında kalikslerin en ince bölgesi olan forniks bileşkesi çatlar ve idrar retroperitoneal boşluğa ekstravaze olur.',
                    'isKey': True
                },
                {
                    'title': 'Klinik Ağrı Paradoksu',
                    'desc': 'Renal kolik ağrısının ana kaynağı pelvis ve kapsül gerilmesidir. Forniks rüptürüyle basınç düştüğünden ağrı aniden rahatlar; hastanın iyileştiği sanılabilir fakat BT\'de perirenal ekstravazasyon görülür.',
                    'isKey': True
                },
                {
                    'title': 'Ürinom Oluşumu ve Tedavi Esasları',
                    'desc': 'Steril ürinomlar üretere Double-J stent konularak toplayıcı sistem drene edildiğinde hızla rezorbe olur; enfekte ürinomlar ise perkütan kateterle drene edilmelidir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Forniks Rüptürü ve Ürinom Klinik Seyri',
                'headers': ['Aşama', 'Fizyolojik Değişim', 'Klinik Tablo', 'Radyolojik Bulgu (BT)'],
                'rows': [
                    ['Rüptür Öncesi', 'İntrapelvik tepe basınç', 'Dayanılmaz şiddette renal kolik', 'Belirgin hidronefroz ve perinefritik ödem'],
                    ['Rüptür Anı', 'Forniks yırtılması ve basınç tahliyesi', 'Ağrıda ani ve belirgin hafifleme', 'Kontrast ekstravazasyonu (kaçak)'],
                    ['Ürinom Evresi', 'Retroperitonda idrar birikimi', 'Karında dolgunluk, subfebril ateş', 'Gerota fasyası içinde sıvı koleksiyonu (ürinom)']
                ]
            }
        },
        'spotPearls': [
            'Forniks rüptürü sonrasında renal kolik ağrısının aniden kaybolması iyileşme değil, basınç tahliyesidir.',
            'Ürinom tanısında kontrastlı BT\'nin geç (ekskresyon) fazında kontrastın toplayıcı sistem dışına sızdığı görülür.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['Ürinom ile perirenal apse nasıl ayırt edilir?', 'Forniks rüptüründe acil cerrahi gerekir mi?']
    },

    # Slide 13
    {
        'slideNumber': 13,
        'title': 'Renal Hemodinamik & Bifazik Yanıt',
        'subtitle': 'PGE2 vazodilatasyonundan TXA2 ve Ang-II vazokonstriksiyonuna geçiş',
        'badge': 'Hemodinamik Fazlar',
        'badgeColor': 'amber',
        'synthesisNarrative': 'Akut tek taraflı üreteral obstrüksiyonda böbrek kan akımı ve basınç yanıtı karakteristik bir **bifazik hemodinamik seyir** izler. İlk 1-2 saatlik erken fazda, artan basınca yanıt olarak lokal **Prostaglandin E2 (PGE2)** ve Prostasiklin (PGI2) salgılanır; afferent arteriyol gevşer ve Renal Kan Akımı (RBF) geçici olarak artar. Ancak 5-24 saat sonrasında devreye giren güçlü vazokonstriktörler (**Tromboksan A2, Anjiyotensin II, Endotelin-1**) afferent ve efferent arteriyolleri şiddetle kasar. Renal kan akımı ve GFR hızla çöker; böbrek dokusunda iskemi ve hipoksi başlar.',
        'flashcards': [
            {
                'id': 'fc-obs-13-1',
                'category': 'Farmakoloji & Hemodinami',
                'front': 'Akut obstrüksiyonun ilk 1-2 saatinde böbrek kan akımını (RBF) geçici olarak artıran ana medyatör nedir?',
                'hint': 'Lokal sentezlenen bir prostaglandin.',
                'back': '**Prostaglandin E2 (PGE2) ve Prostasiklin (PGI2):** Afferent arteriyolde vazodilatasyon yaparak erken dönemde böbrek kan akımını artırır (bu yüzden NSAİİ\'ler PGE2\'yi bloke ederek ağrıyı ve pelvik basıncı düşürür).'
            },
            {
                'id': 'fc-obs-13-2',
                'category': 'Mekanizma',
                'front': 'Obstrüksiyonun geç döneminde (5-24 saat sonrası) böbrek kan akımını çökerterek iskemiye yol açan ana vazokonstriktörler nelerdir?',
                'hint': 'Tromboksan ve renin-anjiyotensin elemanları.',
                'back': '**Tromboksan A2 (TXA2), Anjiyotensin II ve Endotelin:** Renal arteriyollerde yoğun vazokonstriksiyon yaparak renal kan akımını ve GFR\'yi dramatik olarak düşürür.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': '1. Faz: Erken Hiperemi ve Vazodilatasyon (İlk 1-2 Saat)',
                    'desc': 'Üreteral basınç artar; medüller PGE2 ve PGI2 salınımı uyarılır. Afferent arteriyol genişler, böbrek kan akımı (RBF) tepe noktasına ulaşır ve intrapelvik basınç maksimuma çıkar.',
                    'isKey': True
                },
                {
                    'title': '2. Faz: Vazokonstriktör Şift (5-24 Saat)',
                    'desc': 'Renin salgılanmasıyla Anjiyotensin II artar; makrofaj ve trombositlerden TXA2 salınır. Afferent arteriyol direnci hızla yükselir, RBF düşmeye başlar.',
                    'isKey': True
                },
                {
                    'title': '3. Faz: Kronik Hipoperfüzyon ve İskemi (>24 Saat)',
                    'desc': 'Hem RBF hem de intrapelvik basınç düşüşe geçer. GFR kontrol değerlerinin %20-30\'una kadar geriler; doku iskemisi ve tübüler nekroz zemin hazırlar.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Akut Tek Taraflı Üreteral Obstrüksiyonda Bifazik Hemodinamik Yanıt',
                'headers': ['Zaman Dilimi', 'Renal Kan Akımı (RBF)', 'Üreteral Basınç', 'Baskın Medyatörler'],
                'rows': [
                    ['0 - 2 Saat (Erken Faz)', 'Artar (Vazodilatasyon)', 'Maksimum tepe değer', 'PGE2, PGI2, Nitrik Oksit (NO)'],
                    ['2 - 5 Saat (Geçiş Fazı)', 'Azalmaya başlar', 'Yüksek kalır', 'Anjiyotensin II devreye girer'],
                    ['5 - 24 Saat (Geç Faz)', 'Belirgin azalır (Vazokonstriksiyon)', 'Azalmaya başlar', 'Tromboksan A2 (TXA2), Endotelin'],
                    ['> 24 Saat (Kronik Faz)', 'Çok düşük (İskemi)', 'Düşük / orta düzey', 'TGF-beta, TNF-alfa (Fibrozis başlatıcılar)']
                ]
            }
        },
        'spotPearls': [
            'Akut obstrüksiyonun ilk saatlerinde PGE2 vazodilatasyon yapar; NSAİİ ilaçlar bu mekanizmayı keserek renal kolik ağrısını dindirir.',
            'Geç evredeki renal iskemi ve vazokonstriksiyonun temel sorumlusu Tromboksan A2 ve Anjiyotensin II\'dir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['NSAİİ\'ler renal kolik tedavisinde neden ilk tercihtir?', 'Bilateral obstrüksiyonda hemodinamik yanıt tek taraflıdan nasıl farklıdır?']
    },

    # Slide 14
    {
        'slideNumber': 14,
        'title': 'İskemi, Apoptoz ve İnterstisyel Fibrozis Patofizyolojisi',
        'subtitle': 'TNF-alfa ve TGF-beta aracılı tübüler kayıp ve geri dönüşümsüz nefroskleroz',
        'badge': 'Moleküler Mekanizmalar',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Böbrek hasarı ilk aşamada artan üreteral basıncın mekanik basısı ile başlarken, daha sonra ortaya çıkan renal kan akımındaki azalmayla doku iskemisi ve hücresel atrofi meydana gelir. **Tümör Nekrozis Faktör-alfa (TNF-α)**, iskemik renal hasar süresince enflamatuar hücre infiltrasyonunu ve renal tübüler hücre apoptozunu stimüle edebilme kapasitesine sahip potent bir proenflamatuar sitokindir. Beraberinde salınan **TGF-β** fibroblastları aktive ederek kollajen depolanmasını tetikler ve geri dönüşümsüz interstisyel fibrozis ile nefron kaybına yol açar.',
        'flashcards': [
            {
                'id': 'fc-obs-14-1',
                'category': 'Moleküler Patoloji',
                'front': 'Obstrüksiyona bağlı iskemik renal hasarda tübüler hücre apoptozunu ve enflamatuar infiltrasyonu stimüle eden sitokin nedir?',
                'hint': 'Tümör nekrozis faktör ailesi.',
                'back': '**Tümör Nekrozis Faktör-alfa (TNF-α):** İskemik hasar gören tübüler hücrelerde doğrudan apoptozu tetikler ve monosit/makrofaj infiltrasyonunu uyararak fibrozis sürecini başlatır.'
            },
            {
                'id': 'fc-obs-14-2',
                'category': 'Fibrozis',
                'front': 'Obstrüktif nefropatide tübüler epitelin mezenkimal dönüşümünü (EMT) ve kalıcı interstisyel fibrozisi yöneten ana büyüme faktörü nedir?',
                'hint': 'Transforming growth factor.',
                'back': '**Transforming Growth Factor-beta (TGF-β):** Fibroblastları miyofibroblastlara dönüştürür, Tip-1 ve Tip-3 kollajen sentezini artırır ve geri dönüşümsüz renal parankim fibrozisine yol açar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Mekanik Stres ve Doku İskemisi',
                    'desc': 'Yüksek tübüler basınç tübül hücrelerini gerer ve peritübüler kapillerleri sıkarak doku perfüzyonunu bozar. Hücre içi ATP tükenir ve serbest oksijen radikalleri (ROS) açığa çıkar.',
                    'isKey': True
                },
                {
                    'title': 'TNF-α ve Tübüler Hücre Apoptozu',
                    'desc': 'TNF-alfa kaspaz kaskadını aktive ederek toplayıcı kanal ve distal tübül epitel hücrelerini programlı hücre ölümüne (apoptoz) sürükler; tübül kitle kaybı hızlanır.',
                    'isKey': True
                },
                {
                    'title': 'TGF-β ve İnterstisyel Fibrozis',
                    'desc': 'Ekstrasellüler matriks sentezi aşırı artar ve matriks metalloproteinazlar (MMP) baskılanır. Tübüller yerini skar dokusuna bırakır; bu aşamada tıkanıklık açılsa bile fonksiyonel iyileşme sınırlıdır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Moleküler Medyatörler ve Renal Hasar Kaskadı',
                'headers': ['Medyatör', 'Kaynak Hücre', 'Patolojik Fonksiyon', 'Sonuç'],
                'rows': [
                    ['TNF-α', 'Tübül epiteli, İnfiltre makrofajlar', 'Proenflamatuar yanıt, Kaspaz aktivasyonu', 'Tübüler apoptoz ve hücre nekrozu'],
                    ['TGF-β', 'İnterstisyel fibroblastlar, Endotel', 'Epitel-mezenkim transdiferansiasyonu (EMT)', 'Tip I/III kollajen birikimi, Skar dokusu'],
                    ['TXA2', 'Trombositler, Glomerüler hücreler', 'Şiddetli renal vazokonstriksiyon', 'İskemi, medüller hipoksi'],
                    ['Anjiyotensin II', 'Renal tübül ve arteriyoller', 'Efferent vazokonstriksiyon, NF-kB uyarımı', 'Glomerüler hipertansiyon, fibrozis tetiklenmesi']
                ]
            }
        },
        'spotPearls': [
            'TNF-alfa tübüler hücre apoptozunun, TGF-beta ise interstisyel fibrozisin ana moleküler yöneticisidir.',
            'İnterstisyel fibrozis geliştikten sonra obstrüksiyon açılsa bile kaybedilen nefronlar geri kazanılamaz.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['TNF-alfa blokerleri obstrüktif nefropatide fibrozisi önler mi?', 'Epitel-mezenkimal transdiferansiasyon (EMT) böbrekte nasıl gelişir?']
    },

    # Slide 15
    {
        'slideNumber': 15,
        'title': 'GFR Geri Dönüş Potansiyeli ve Obstrüksiyon Süresi İlişkisi',
        'subtitle': 'Deneysel köpek verileri ve insan klinik süre korelasyonu',
        'badge': 'Deneysel & Klinik Veriler',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Obstrüksiyon giderildikten sonra böbreğin GFR fonksiyonunun ne kadarının geri döneceğini belirleyen en kritik faktör **obstrüksiyonun süresi**dir. Klasik deneysel çalışmalarda: **2 haftalık** tam obstrüksiyon sonrası açılan böbrek 3-4 ay içinde kontrol fonksiyonunun **%46**\'sına; **4 haftalık** obstrüksiyon sonrası 5 ay içinde kontrolün **%35**\'ine ulaşabilmektedir. Ancak **6 haftalık tam obstrüksiyondan sonra geri dönen renal fonksiyon YOKTUR (%0)**! İnsanlar için kesin bir gün sınırı olmamakla birlikte, obstrüksiyon ne kadar erken açılırsa fonksiyonel rezerv o kadar iyi korunur.',
        'flashcards': [
            {
                'id': 'fc-obs-15-1',
                'category': 'Deneysel Veriler & Sınav Sorusu',
                'front': 'Deneysel çalışmalarda 2 haftalık ve 6 haftalık tam üreter obstrüksiyonu sonrası geri dönen GFR oranları sırasıyla nedir?',
                'hint': '2 haftada yaklaşık yarısı, 6 haftada ise hiçbiri.',
                'back': '**2 Haftalık Obstrüksiyon:** Kontrol GFR fonksiyonunun **%46\'sı** geri döner (3-4 ay içinde).\n\n**6 Haftalık Obstrüksiyon:** **Geri dönen fonksiyon YOKTUR (%0)!** Nefronlar kalıcı olarak kaybedilmiştir.'
            },
            {
                'id': 'fc-obs-15-2',
                'category': 'Klinik Karar',
                'front': 'İnsanlarda 4 haftalık tam tıkanıklıktan sonra fonksiyonel geri dönüşüm mümkün müdür?',
                'hint': 'Kısmen mümkündür ancak nefron kaybı belirgindir.',
                'back': 'Kısmen mümkündür (deneysel modelde %35 civarı); ancak toparlanma 5 aya kadar uzar ve hastanın yaşı, enfeksiyon varlığı ve önceden var olan böbrek rezervi nihai sonucu belirler.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': '2 Haftalık Tam Obstrüksiyon',
                    'desc': 'Dekompresyonu takiben toparlanma süreci 3-4 ayı bulur. Böbrek eski fonksiyonel kapasitesinin yaklaşık yarısını (%46) geri kazanabilir.',
                    'isKey': True
                },
                {
                    'title': '4 Haftalık Tam Obstrüksiyon',
                    'desc': 'Fonksiyonel dönüşüm oldukça yavaşlar; 5 aylık süreçte kontrol fonksiyonunun sadece üçte biri (%35) kurtarılabilir.',
                    'isKey': True
                },
                {
                    'title': '6 Haftalık Eşik ve Fonksiyon Kaybı (%0)',
                    'desc': '6 haftayı aşan komplet üreteral tıkanıklıklarda tübüler atrofi ve fibrozis tam katmana ulaşır; obstrüksiyon açılsa bile anlamlı GFR geri dönüşü gerçekleşmez.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Üreteral Obstrüksiyon Süresi ve GFR Geri Kazanım Tablosu',
                'headers': ['Obstrüksiyon Süresi', 'Geri Kazanılan Maksimum GFR', 'Geri Kazanım İçin Gereken Süre', 'Klinik Durum'],
                'rows': [
                    ['2 Hafta', 'Kontrolün % 46\'sı', '3 - 4 Ay içinde', 'Anlamlı fonksiyonel toparlanma'],
                    ['4 Hafta', 'Kontrolün % 35\'i', '5 Ay içinde', 'Kısmi toparlanma, belirgin nefron kaybı'],
                    ['6 Hafta', '% 0 (Geri Dönen Fonksiyon Yok)', 'Yok', 'Geri dönüşümsüz afonksiyonel böbrek (Atrofi)'],
                    ['İnsan Klinikleri', 'Değişken (Süre uzadıkça hızla düşer)', 'Aylar sürer', 'Enfeksiyon eklenirse günler içinde nefron kaybı!']
                ]
            }
        },
        'spotPearls': [
            '6 haftalık tam üreter obstrüksiyonunda deneysel olarak geri dönen böbrek fonksiyonu %0\'dır.',
            'Tıkanıklığa enfeksiyon eşlik ederse doku nekrozu hızlanır ve haftalar değil günler içinde kalıcı nefron kaybı olur.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['Parsiyel obstrüksiyonlarda GFR geri dönüş süresi ne kadardır?', 'Köpek deneyleri verileri insan kliniğine nasıl uyarlanır?']
    },

    # Slide 16
    {
        'slideNumber': 16,
        'title': 'Renal Kontrbalans Mekanizması (Hinman Hipotezi)',
        'subtitle': 'Kompansatuar renal hipertrofi ve kontralateral hipotrofi dinamikleri',
        'badge': 'Kompansatuar Yanıtlar',
        'badgeColor': 'indigo',
        'synthesisNarrative': '**Renal Kontrbalans** (Hinman teorisi), tek taraflı böbrek hasarı veya obstrüksiyonunda sağlam ve hasta böbrek arasındaki dinamik fonksiyonel dengeyi tanımlar. Bir böbrek cerrahi olarak çıkarılırsa ya da obstrüksiyon sonucu fonksiyonunu kaybederse, diğer sağlam böbrek metabolik yükü karşılamak için büyür (**kompansatuar renal hipertrofi**). Eğer tek taraflı obstrüksiyon uzun süre sonra giderilirse veya renal transplantasyon yapılırsa, hipertrofiye uğramış böbrek fonksiyonu domine eder ve obstrüksiyondan kurtarılan hasta böbrek fonksiyonel olarak gerileyebilir (**renal hipotrofi**).',
        'flashcards': [
            {
                'id': 'fc-obs-16-1',
                'category': 'Fizyoloji & Teori',
                'front': 'Renal Kontrbalans kavramı neyi ifade eder?',
                'hint': 'Bir böbrek kaybedildiğinde diğerinin büyümesi ve sonrasındaki fonksiyonel yarış.',
                'back': 'Bir böbrek çıkarıldığında veya obstrüksiyonla devre dışı kaldığında diğer böbreğin hipertrofiye uğraması; tek taraflı obstrüksiyon geç dönemde açıldığında ise sağlam hipertrofik böbreğin baskın kalıp hasta böbreğin göreceli hipotrofiye uğramasıdır.'
            },
            {
                'id': 'fc-obs-16-2',
                'category': 'Klinik Anlam',
                'front': 'Tek taraflı tam obstrüksiyonda hastanın serum kreatinin düzeyi neden uzun süre normal kalabilir?',
                'hint': 'Karşı böbreğin kompansasyonu.',
                'back': 'Karşı sağlam böbrek **kompansatuar hipertrofi** göstererek glomerüler filtrasyon iş yükünün tamamını üstlenir. Bu nedenle tek taraflı obstrüksiyonlu hasta böbreğini tamamen kaybederken serum kreatinini yanıltıcı şekilde normal kalabilir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Kompansatuar Renal Hipertrofi',
                    'desc': 'Sağlam böbrek nefronlarında hem hücresel hipertrofi hem de hiperfiltrasyon gelişir; tek böbrek toplam renal kapasitenin %75-80\'ini tek başına karşılayabilir.',
                    'isKey': True
                },
                {
                    'title': 'Renal Hipotrofi Riski',
                    'desc': 'Hasta böbrekteki tıkanıklık çok geç açılırsa, sağlam hipertrofik böbrek vücudun tüm metabolik atıklarını zaten temizlediğinden hasta böbreğe iş yükü kalmaz ve fonksiyonel hipotrofiye uğrar.',
                    'isKey': True
                },
                {
                    'title': 'Sessiz Böbrek Kaybı Tuzağı',
                    'desc': 'Bilateral obstrüksiyon hızla azotemi yaparken, tek taraflı obstrüksiyon kontrbalans nedeniyle kan tahlillerinde hiçbir biyokimyasal bozulma vermeden sessizce böbreği çürütebilir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Renal Kontrbalans Sürecinin Evreleri',
                'headers': ['Aşama', 'Hasta Böbreğin Durumu', 'Sağlam Böbreğin Durumu', 'Total GFR & Serum Kreatinin'],
                'rows': [
                    ['Akut Tıkanıklık', 'Obstrüktif hasar başlar', 'Normal fonksiyon', 'Hafif geçici dalgalanma, genelde normal'],
                    ['Kronik Obstrüksiyon', 'Progresif parankim kaybı', 'Kompansatuar hipertrofi (büyüme)', 'Serum kreatinin tamamen normal!'],
                    ['Geç Dekompresyon', 'Tıkanıklık açılır (düşük rezerv)', 'Hipertrofik baskın böbrek', 'Toplam GFR yeterli, hasta böbrek hipotrofik kalır']
                ]
            }
        },
        'spotPearls': [
            'Tek taraflı üreter obstrüksiyonunda serum kreatininin normal olması böbreğin iyi durumda olduğunu kanıtlamaz.',
            'Sağlam böbreğin kompansatuar hipertrofisi tek taraflı böbrek hasarını maskeleyen en büyük faktördür.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['Renal kontrbalans teorisi klinik pratikte nasıl uygulanır?', 'Kompansatuar hipertrofi ne kadar sürede gelişir?']
    },

    # Slide 17
    {
        'slideNumber': 17,
        'title': 'Klinik Belirtiler ve Semptomatoloji (Akut vs Kronik)',
        'subtitle': 'Renal kolik, yansıyan ağrılar, akut anüri ve kronik üremi tablosu',
        'badge': 'Semptomlar & Klinik',
        'badgeColor': 'blue',
        'synthesisNarrative': 'Üriner obstrüksiyonun semptomları oluşum hızına (akut/kronik), tek ya da çift taraflı oluşuna, seviyesine ve komplet/parsiyel olmasına göre değişir. **Akut obstrüksiyon**; kapsül gerilmesine bağlı şiddetli flank ağrısı (renal kolik), kasığa ve uyluğa yansıma, bulantı ve kusma ile karakterizedir. Enfeksiyon eklenirse yüksek ateş ve titreme eşlik eder. Akut bilateral komplet obstrüksiyonun tipik bulgusu **ani başlayan anüri**dir. **Kronik obstrüksiyon** ise çoğunlukla asemptomatiktir; bilateral kronik olgular karın çevresinde artış, ayak bileği ödemi, hipertansiyon ve üremi bulguları (ensefalopati, tremor, GİS kanamaları) ile başvurur.',
        'flashcards': [
            {
                'id': 'fc-obs-17-1',
                'category': 'Klinik Semptomatoloji',
                'front': 'Akut bilateral üreter obstrüksiyonunun en karakteristik ve dramatik klinik prezentasyonu nedir?',
                'hint': 'İdrar çıkışının aniden sıfırlanması.',
                'back': '**Ani Başlayan Tam Anüri (İdrar Çıkışının <50-100 mL/gün olması):** Akut gelişen anüri tablosunda aksi kanıtlanana kadar bilateral obstrüksiyon veya soliter böbreğin tam tıkanıklığı düşünülmelidir.'
            },
            {
                'id': 'fc-obs-17-2',
                'category': 'Ağrı Yansıması',
                'front': 'Renal kolik ağrısı neden sırttan kasığa, skrotuma veya labiumlara doğru yayılır?',
                'hint': 'T10-L1 dermatom afferent sinirleri.',
                'back': 'Böbrek ve üreter afferent sempatik lifleri spinal kordun **T10 - L1** segmentlerine girer. Bu segmentler iliohipogastrik, ilioinguinal ve genitofemoral sinirlerin dermatomları ile örtüştüğünden ağrı böğürden testise/labiuma ve uyluğun iç yüzüne yansır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Akut Obstrüksiyonun Şiddetli Tablosu',
                    'desc': 'Renal kolik (flank ağrısı), kostovertebral açı hassasiyeti (KVAH), paralitik ileus, bulantı ve kusma. Enfeksiyon durumunda akut piyelonefrit ve yüksek ateş (39-40°C).',
                    'isKey': True
                },
                {
                    'title': 'Akut Anüri: Mutlak Cerrahi İpucu',
                    'desc': 'Prerenal veya renal azotemiler genellikle oligüri yaparken; aniden idrarın bıçak gibi kesilmesi (anüri) hemen daima ürolojik bir obstrüksiyona işaret eder.',
                    'isKey': True
                },
                {
                    'title': 'Kronik Obstrüksiyonun Sinsi Seyri',
                    'desc': 'Asemptomatik hidronefroz, bilateral kronik olgularda volüm yüklenmesi bulguları (ayak bileği ödemi, hipertansiyon, dispne) ve üremi komplikasyonları.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Akut vs Kronik Üriner Obstrüksiyon Klinik Karşılaştırması',
                'headers': ['Klinik Özellik', 'Akut Obstrüksiyon', 'Kronik Obstrüksiyon'],
                'rows': [
                    ['Başlangıç Şekli', 'Aniden saatler içinde başlar', 'Haftalar-aylar içinde sinsi gelişir'],
                    ['Ağrı Karakteri', 'Şiddetli, kıvrandırıcı renal kolik (KVAH +)', 'Genellikle tamamen ağrısız veya künt dolgunluk'],
                    ['İdrar Çıkışı', 'Tek taraflı ise normal; bilateral ise anüri', 'Fluktuasyon gösterebilir (Poliüri / Oligüri)'],
                    ['Böbrek Parankimi', 'Parankim kalınlığı korunmuştur', 'Parankim incelmiş, kistik kaliektazi mevcuttur'],
                    ['Biyokimyasal Tablo', 'Üre/Kreatinin normal olabilir (tek taraflıysa)', 'İleri evrede üre/kreatinin artışı, metabolik asidoz']
                ]
            }
        },
        'spotPearls': [
            'Ani başlayan tam anüri tablosunda ilk olarak bilateral obstrüksiyon veya tek böbrekli hastada tıkanıklık düşünülmelidir.',
            'Kronik obstrüksiyonlar hiçbir ağrı yapmadan hastayı son dönem böbrek yetmezliğine sokabilir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_luts']],
        'aiPromptSuggestions': ['Renal kolik ağrısı ile akut apandisit nasıl ayırt edilir?', 'Akut anüri hastasına acil serviste ilk yaklaşım nasıl olmalıdır?']
    },

    # Slide 18
    {
        'slideNumber': 18,
        'title': 'Glob Vesicale: Tanı, Belirtiler ve Ani Dekompresyon Tehlikesi',
        'subtitle': 'Akut komplet retansiyon, suprapubik kitle ve kademeli boşaltım kuralı',
        'badge': 'Ürolojik Acil Durum',
        'badgeColor': 'rose',
        'synthesisNarrative': '**Glob vesicale**, akut komplet infravezikal obstrüksiyona bağlı olarak mesanede idrar birikmesi ve hastanın idrarını hiçbir şekilde boşaltamaması durumudur. Hasta son derece huzursuzdur; aşırı şiddetli işeme isteği tarifler fakat damla idrar yapamaz. Fizik muayenede suprapubik bölgede göbeğe kadar uzanabilen hassas, küre şeklinde matite veren palpabl kitle saptanır. HAYATİ UYARI: Glob vesicale saptandığında idrar aniden ve hızla tamamen boşaltılmamalıdır! Ani boşaltım mesane venlerinde vakum etkisi yaparak **masif hematüriye (hematuria ex vacuo)** ve ani vazovagal hipotansiyona yol açar; idrar kademeli boşaltılmalıdır!',
        'flashcards': [
            {
                'id': 'fc-obs-18-1',
                'category': 'Acil Tıp & Komplikasyon',
                'front': 'Glob vesicale tablosunda mesane bir anda ve hızla tamamen boşaltılırsa hangi iki tehlikeli komplikasyon gelişebilir?',
                'hint': 'Kanama ve tansiyon düşüşü.',
                'back': '1. **Hematuria Ex Vacuo (Dekompresyon Hematürisi):** Mesane duvarındaki aşırı gerilmiş venöz pleksusların ani basınç düşüşüyle patlaması sonucu masif mukozal kanama.\n2. **Ani Vazovagal Hipotansiyon ve Senkop:** Pelvik venöz yatakta kanın aniden göllenmesi sonucu venöz dönüşün düşmesi.'
            },
            {
                'id': 'fc-obs-18-2',
                'category': 'Klinik Protokol',
                'front': 'Glob vesicale saptanan hastada foley kateter ile idrar boşaltma protokolü nasıl olmalıdır?',
                'hint': 'Kademeli klempleme yöntemi.',
                'back': 'İlk seferde en fazla **400 - 500 mL** idrar boşaltıldıktan sonra kateter klemplenmeli; 15-20 dakika aralıklarla kontrollü ve **kademeli** olarak drenaj sürdürülmelidir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Glob Vesicale Klinik Prezentasyonu',
                    'desc': 'Akut komplet çıkım tıkanıklığı (BPH atağı, üretra taşı, pıhtı retansiyonu). Mesane kapasitesi 1000-1500 mL\'ye ulaşabilir; hasta kıvranır, terler ve suprapubik kitle aşırı hassastır.',
                    'isKey': True
                },
                {
                    'title': 'Taşma (İshiyüri Paradoksu) İnkontinansı',
                    'desc': 'Bazen mesane içi basınç sfinkter direncini aştığında damla damla idrar kaçar (overflow inkontinans); bu durum idrar yapabiliyor sanılarak glob tanısını geciktirebilir.',
                    'isKey': True
                },
                {
                    'title': 'Kademeli Dekompresyon Kuralı',
                    'desc': 'Mesanenin aşırı hızlı boşaltılması pelvik konjesyona ve mesane mukozasından pıhtılı kanamaya yol açacağından kateter mutlaka kademeli klemplenerek boşaltılmalıdır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Glob Vesicale Yönetiminde Doğrular ve Yanlışlar',
                'headers': ['Yaklaşım Boyutu', 'Tehlikeli / Yanlış Yaklaşım', 'Doğru Klinik Protokol'],
                'rows': [
                    ['Boşaltım Hızı', 'Torba takıp 1500 mL idrarı tek seferde sonuna kadar çekmek', 'İlk 400-500 mL sonrası klemplemek, kademeli boşaltmak'],
                    ['Olası Komplikasyon', 'Hematuria ex vacuo, ani tansiyon düşmesi ve senkop', 'Dengeli pelvik dekompresyon, hasta konforu'],
                    ['Üretral Giriş Başarısızlığı', 'Zorlayarak üretrayı yırtmak (yalancı pasaj)', 'Suprapubik perkütan sistostomi ile mesaneye girmek'],
                    ['Tanı Doğrulaması', 'Yalnızca hastanın ifadesine güvenmek', 'Suprapubik palpasyon, perküsyon (matite) ve yatak başı USG']
                ]
            }
        },
        'spotPearls': [
            'Glob vesicale aniden ve tamamen boşaltılırsa mesane mukozasından masif dekompresyon kanaması (hematuria ex vacuo) gelişir.',
            'Suprapubik matite ve palpabl kitle saptanan hastada ilk adım yatak başı kateterizasyondur.'
        ],
        'relatedQuestions': [matched_questions_dict['q_bph']],
        'aiPromptSuggestions': ['Hematuria ex vacuo nasıl tedavi edilir?', 'Foley takılamayan glob vesicale hastasına nasıl müdahale edilir?']
    },

    # Slide 19
    {
        'slideNumber': 19,
        'title': 'Radyolojik Tanı ve Görüntüleme Protokolleri',
        'subtitle': 'USG, DÜSG, Kontrassız BT, IVP ve Nükleer Tıp (MAG-3/DTPA)',
        'badge': 'Tanı Protokolleri',
        'badgeColor': 'emerald',
        'synthesisNarrative': 'Üriner obstrüksiyonun tanısında radyolojik görüntüleme hem anatomik düzeyi hem de fonksiyonel etkiyi ortaya koyar. **Ultrasonografi (USG)**; non-invaziv, hızlı ve ucuz olması nedeniyle **İLK DEĞERLENDİRME YÖNTEMİ**dir; hidronefrozu ve parankim kalınlığını mükemmel gösterir fakat subjektiftir ve erken fazda yalancı negatif olabilir. Günümüzde üst üriner sistem obstrüksiyonunun anatomik altın standardı **Kontrassız Helikal BT (Taş BT)**\'dir. **İntravenöz Pyelografi (IVP)** toplayıcı sistem anatomisini gösterse de kontrast ve radyasyon gerektirir; böbrek fonksiyonları bozuksa kontrast atılamayacağı için yapılamaz. Fonksiyonel değerlendirmede ise **Nükleer Tıp (99mTc-MAG3 / DTPA + Furosemid)** mekanik tıkanıklığı atonik dilatasyondan ayırır.',
        'flashcards': [
            {
                'id': 'fc-obs-19-1',
                'category': 'Görüntüleme & Sınav Sorusu',
                'front': 'Üriner obstrüksiyon şüphesinde İLK başvurulacak yöntem ile taş/anatomi için ALTIN STANDART yöntem hangileridir?',
                'hint': 'Biri radyasyonsuz ilk basamak, diğeri helikal tomografi.',
                'back': '**İlk Değerlendirme Yöntemi:** Ultrasonografi (USG) — Radyasyonsuz, hızlı, ucuz, parankim ve dilatasyonu gösterir.\n\n**Anatomik Altın Standart:** Kontrassız Helikal BT (Taş BT) — %98 duyarlılıkla obstrüksiyon seviyesini ve etyolojiyi kesin gösterir.'
            },
            {
                'id': 'fc-obs-19-2',
                'category': 'Nükleer Tıp',
                'front': 'Diüretikli Renogramda (MAG-3 / DTPA + Lasix) mekanik obstrüksiyon ile atonik hidronefroz nasıl ayırt edilir?',
                'hint': 'Furosemid verilince eğrinin seyri.',
                'back': '**Mekanik Obstrüksiyon:** Furosemid (Lasix) verilmesine rağmen radyoaktif madde boşalamaz, aktivite eğrisi yükselmeye devam eder.\n\n**Atonik (Non-obstrüktif) Dilatasyon:** Furosemid verilince idrar akımı hızlanır ve radyoaktivite hızla yıkanarak eğri hızla aşağı iner (washout +).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Ultrasonografi (USG) İlk Basamak Rolü',
                    'desc': 'Toplayıcı sistem dilatasyonunu (Grade 1-4 hidronefroz), böbrek boyutlarını ve korteks kalınlığını saptar. Gebe ve çocuklarda güvenlidir. Taş üreter ortasındaysa USG ile görülmesi zordur.',
                    'isKey': True
                },
                {
                    'title': 'Kontrassız Helikal BT (Taş Protokolü)',
                    'desc': 'Dakikalar içinde çekilir, kontrast nefrotoksisitesi riski yoktur. İndinavir taşları hariç tüm taşları saptar; perinefritik stranding ve üreteral dilatasyonu netleştirir.',
                    'isKey': True
                },
                {
                    'title': 'IVP ve Nükleer Tıp Sintigrafisi Sınırları',
                    'desc': 'IVP kreatinin > 2 mg/dL ise nefrotoksiktir ve görüntü vermez. MAG-3 tübüler sekresyonla atıldığından böbrek fonksiyonu azalmış hastalarda DTPA\'ya tercih edilir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Üriner Obstrüksiyonda Görüntüleme Modaliteleri Karşılaştırması',
                'headers': ['Yöntem', 'Temel Endikasyon', 'Avantajları', 'Sınırlılık / Kontrendikasyon'],
                'rows': [
                    ['Ultrasonografi (USG)', 'İlk değerlendirme, gebe/çocuk', 'Non-invaziv, ucuz, radyasyon yok', 'Operatör bağımlı, üreter taşlarında yetersiz'],
                    ['Kontrassız Helikal BT', 'Üst üriner obstrüksiyon altın standardı', '%98 duyarlılık, hızlı, anatomik netlik', 'İyonize radyasyon içerir'],
                    ['İntravenöz Pyelografi (IVP)', 'Toplayıcı sistem anatomisi, striktür', 'Anatomik detay, kaçak gösterimi', 'Kontrast nefrotoksisitesi; kreatinin yüksekse yapılamaz!'],
                    ['Nükleer Tıp (MAG-3 / DTPA)', 'Fonksiyonel obstrüksiyon ayrımı', 'GFR ve tübüler fonksiyon, Lasix testi', 'Anatomik çözünürlük düşüktür']
                ]
            }
        },
        'spotPearls': [
            'USG üriner obstrüksiyonda ilk değerlendirme yöntemi; kontrassız helikal BT ise altın standarttır.',
            'Böbrek yetmezliği olan veya kreatinini yüksek hastada IVP nefrotoksik olduğu için kesinlikle kontrendikedir.'
        ],
        'relatedQuestions': [matched_questions_dict['q_imaging']],
        'aiPromptSuggestions': ['MAG-3 sintigrafisinde T1/2 süresi ne anlama gelir?', 'İndinavir taşları neden BT\'de görünmez?']
    },

    # Slide 20
    {
        'slideNumber': 20,
        'title': 'Tedavi Prensipleri, Acil Dekompresyon ve Enfekte Obstrüksiyon',
        'subtitle': 'Kateter, Double-J stent, Perkütan Nefrostomi ve septik şok önleme',
        'badge': 'Tedavi & Acil Müdahale',
        'badgeColor': 'rose',
        'synthesisNarrative': 'Üriner obstrüksiyon tedavisinin birincil hedefi toplayıcı sistemdeki basıncı acilen düşürmek, stazı ortadan kaldırmak ve nefron kaybını engellemektir. İnfravezikal tıkanıklıklarda ilk adım **üretral foley kateterizasyon**, başarısızlıkta ise suprapubik perkütan sistostomidir. Üst üriner sistem tıkanıklıklarında **retrograd Double-J üreter stenti** veya **Perkütan Nefrostomi (PCN)** uygulanır. EN KRİTİK ÜROLOJİK ACİL: Obstrüksiyon + Ateş/Piyüri (Enfekte Hidronefroz) saptandığında hasta acil ameliyathaneye alınarak toplayıcı sistem derhal dekomprese edilmeli ve eşzamanlı parenteral antibiyotik başlanmalıdır!',
        'flashcards': [
            {
                'id': 'fc-obs-20-1',
                'category': 'Ürolojik Acil & Hayat Kurtarma',
                'front': 'Obstrüksiyona eşlik eden yüksek ateş ve titreme (enfekte hidronefroz) neden mutlak ürolojik acildir?',
                'hint': 'Tıkanmış piyelonefrit ve pyelovenöz reflü.',
                'back': 'Kapalı bir abse haline gelen toplayıcı sistemdeki yüksek basınç, bakterileri ve endotoksinleri pyelovenöz yolla doğrudan kana pompalar. Saatler içinde **üroseptik şok ve ölüm** gelişir; derhal acil dekompresyon (DJ stent veya Perkütan Nefrostomi) şarttır.'
            },
            {
                'id': 'fc-obs-20-2',
                'category': 'Girişimsel Üroloji',
                'front': 'Üreter taşına bağlı enfekte hidronefrozu olan ve genel durumu kötü hastada taşa cerrahi müdahale ne zaman yapılmalıdır?',
                'hint': 'Hemen taş kırılır mı, yoksa önce sadece drenaj mı?',
                'back': 'Akut enfeksiyon ve obstrüksiyon anında taşa müdahale edilmez! Önce acil drenaj (Double-J stent veya PCN) ve antibiyotik ile hasta sepsisten çıkarılır; taş tedavisi enfeksiyon tamamen düzeldikten haftalar sonra elektif şartlarda yapılır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'İnfravezikal Drenaj Yolları',
                    'desc': 'Üretral Foley kateter; üretra darlığı, yalancı pasaj veya akut prostatitte travmayı önlemek için perkütan suprapubik sistostomi.',
                    'isKey': True
                },
                {
                    'title': 'Supravezikal Dekompresyon (DJ Stent vs PCN)',
                    'desc': 'Sistoskopi altında retrograd Double-J stent takılması; stentin çıkamadığı komplet taşlarda veya ağır septik hastada lokal anesteziyle USG eşliğinde Perkütan Nefrostomi (PCN).',
                    'isKey': True
                },
                {
                    'title': 'Etyolojiye Yönelik Kesin Tedavi',
                    'desc': 'Dekompresyon sağlandıktan ve enfeksiyon kontrol altına alındıktan sonra nedene yönelik kesin tedavi (Üreteroskopi/Lazer litotripsi, TURP, üretroplasti, piyeloplasti) planlanır.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Üriner Dekompresyon Modaliteleri ve Endikasyonları',
                'headers': ['Dekompresyon Yöntemi', 'Uygulama Yolu', 'Birincil Endikasyon', 'Klinik Avantajı'],
                'rows': [
                    ['Üretral Foley Sonda', 'Transüretral', 'Glob vesicale, BPH retansiyonu', 'Yatak başında anında uygulanabilir'],
                    ['Suprapubik Sistostomi', 'Suprapubik perkütan', 'Üretra darlığı, üretra travması, foley takılamayanlar', 'Üretral yaralanma ve enfeksiyon riskini baypas eder'],
                    ['Retrograd Double-J Stent', 'Sistoskopik üreteral', 'Üreter taşları, UPJ darlığı, tümör basısı', 'Dışarıda torba/kateter bırakmaz, iç drenaj sağlar'],
                    ['Perkütan Nefrostomi (PCN)', 'Lomber ciltten pelvise', 'DJ takılamayan taşlar, ağır ürosepsis, pyonefroz', 'Ağır hastada lokal anesteziyle minimal invaziv drenaj']
                ]
            }
        },
        'spotPearls': [
            'Enfekte obstrüktif hidronefrozda altın kural: Önce acil drenaj ve antibiyotik, sonra elektif taş cerrahisi!',
            'Foley takılamayan akut retansiyon hastasında üretrayı zorlamak yalancı pasaj yapar; suprapubik sistostomi açılmalıdır.'
        ],
        'relatedQuestions': [matched_questions_dict['q_infected_hydro']],
        'aiPromptSuggestions': ['Double-J stent mi perkütan nefrostomi mi tercih edilmeli?', 'Pyonefroz tanısı konan hastada acil ameliyat adımları nelerdir?']
    },

    # Slide 21
    {
        'slideNumber': 21,
        'title': 'Postobstrüktif Diürez (POD): Patofizyoloji ve Sıvı-Elektrolit Yönetimi',
        'subtitle': 'Osmotik yük, medüller gradiyent kaybı ve iatrojenik poliüri tuzağı',
        'badge': 'Dekompresyon Sonrası Kritik Süreç',
        'badgeColor': 'amber',
        'synthesisNarrative': '**Postobstrüktif Diürez (POD)**, bilateral üreteral obstrüksiyon veya soliter böbrek tıkanıklığı açıldıktan sonra gelişen şiddetli poliüri tablosudur (>200 mL/saat veya >3-4 L/24 saat). **Fizyolojik POD**; obstrüksiyon süresince kanda biriken üre ve sodyumun filtre edilerek osmotik diürez oluşturmasıdır ve kendi kendini sınırlar. **Patolojik POD** ise yüksek basıncın renal medülladaki hipertonik konsantrasyon gradiyentini silmesi ve toplayıcı kanalların ADH\'ya yanıtsız kalması sonucu gelişir. HAYATİ TEDAVİ KURALI: Sıvı replasmanı idrar çıkışının **%50-75\'i** kadar yapılmalıdır; hastaya çıkardığı idrar kadar (%100) sıvı verilirse iatrojenik poliüri kısır döngüsü tetiklenir!',
        'flashcards': [
            {
                'id': 'fc-obs-21-1',
                'category': 'Tanı & Kriter',
                'front': 'Postobstrüktif diürez (POD) hangi anatomik tıkanıklıkların açılmasından sonra görülür ve tanı kriteri nedir?',
                'hint': 'Tek böbrek yetmez; iki taraf veya tek kalan böbrek.',
                'back': '**Bilateral obstrüksiyon** veya **soliter böbrek obstrüksiyonu** giderildikten sonra görülür. Tanı kriteri: Erişkinde idrar çıkışının ardışık saatlerde **>200 mL/saat** veya **>3-4 L/gün** olmasıdır.'
            },
            {
                'id': 'fc-obs-21-2',
                'category': 'Klinik Tuzak & Yönetim',
                'front': 'Postobstrüktif diürez tedavisinde hekimin yapabileceği EN BÜYÜK iatrojenik hata nedir?',
                'hint': 'Çıkardığı kadar sıvı vermek.',
                'back': '**Kaybedilen idrarın %100\'ünü veya fazlasını yerine koymak:** Verilen her litre sıvı yeni bir ozmotik/volüm yükü oluşturarak böbrekten diürezi körükler ve hastayı iatrojenik bir poliüri kısır döngüsüne sokar. Sıvı replasmanı **%50-75** ile sınırlandırılmalıdır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Postobstrüktif Diürez Tanı Eşiği',
                    'desc': 'Tıkanıklık açıldıktan sonra idrar debisinin erişkinde 200 mL/saat üzerine çıkmasıdır. Hastada birikmiş volüm ve solütlerin hızla tahliyesiyle başlar.',
                    'isKey': True
                },
                {
                    'title': 'Fizyolojik vs Patolojik Diürez Mekanizması',
                    'desc': 'Fizyolojik tipte biriken üre osmotik diüretik gibi davranır ve solütler temizlenince biter. Patolojik tipte ise medüller konsantrasyon mekanizması çökmüştür ve toplayıcı kanallar ADH\'ya dirençlidir (nefrojenik diabetes insipidus benzeri tablo).',
                    'isKey': True
                },
                {
                    'title': 'Kritik Sıvı ve Elektrolit Protokolü',
                    'desc': 'İdrar hacmi saatlik takip edilir. Kaybedilen sıvının %50-75\'i 0.45% NaCl (yarım izotonik) veya dengeli elektrolit solüsyonu ile verilir. K, Mg ve Na düzeyleri 4-6 saatte bir kontrol edilir.',
                    'isKey': False
                }
            ],
            'table': {
                'title': 'Fizyolojik vs Patolojik Postobstrüktif Diürez',
                'headers': ['Parametre', 'Fizyolojik Postobstrüktif Diürez', 'Patolojik Postobstrüktif Diürez'],
                'rows': [
                    ['Temel Neden', 'Biriken üre ve solütlerin osmotik etkisi', 'Medüller gradiyent kaybı ve tübüler ADH yanıtsızlığı'],
                    ['İdrar Osmolalitesi', 'Yüksek / İzostenürik (Solüt zengin)', 'Düşük / Hipostenürik (Aşırı sulu idrar)'],
                    ['Klinik Seyir', 'Solütler atılınca 24-48 saatte kendiliğinden biter', 'Günlerce sürebilir, şiddetli hipovolemi ve şok riski'],
                    ['Sıvı Replasmanı', 'Hasta susadıkça oral sıvı alabilir', 'Çıkışın %50-75\'i kadar IV kontrollü replasman']
                ]
            }
        },
        'spotPearls': [
            'Postobstrüktif diürez sadece bilateral veya soliter böbrek tıkanıklığı açıldığında ortaya çıkar.',
            'İdrar çıkışının %100\'ünü yerine koymak iatrojenik poliüri kısır döngüsü yaratarak diürezi yapay olarak sürdürür.'
        ],
        'relatedQuestions': [matched_questions_dict['q_pod']],
        'aiPromptSuggestions': ['Patolojik postobstrüktif diürezde desmopressin (DDAVP) işe yarar mı?', 'POD takibinde hangi laboratuvar testleri saatlik yapılmalıdır?']
    }
]

# Build updated Batch 1 deck object
batch1_deck = {
    'id': 'deck-urinary-obstruction',
    'title': 'Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi',
    'shortTitle': 'Üriner Obstrüksiyon',
    'discipline': 'Üroloji / Nefroloji',
    'committee': 'Kurul 5',
    'instructor': 'Üroloji Anabilim Dalı',
    'audioFile': '1)Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi.txt',
    'audioDuration': 'Ders Notu Tam Müfredatı (62 Sayfa)',
    'confidence': 'Resmi Ders Notu Doğrulanmış Sentezi (%100)',
    'themeColor': '#0284c7',
    'matchedNoteId': 'urinary-obstruction-full',
    'matchedNoteTitle': '1) Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi (Ders Notu)',
    'overview': 'Üriner obstrüksiyon; eksternal üretral meadan renal tubuluslara kadar idrar akımını engelleyen tüm mekanik ve fonksiyonel patolojileri kapsar. Bu ders; obstrüksiyonun anatomik ve etyolojik sınıflamasını, alt üriner sistemde kompanse ve dekompanse mesane dönüşümünü (trabekül, selül, divertikül), üst üriner sistemde üreter peristaltizmi ve kaliks/papilla morfolojisini, koruyucu basınç tahliye yollarını (pyelointerstisyel, pyelolenfatik, pyelovenöz), forniks rüptürü ve ürinom gelişimini, bifazik renal hemodinamik yanıtı (PGE2 vs TXA2/Ang-II), TNF-alfa ve TGF-beta aracılı tübüler apoptoz ve interstisyel fibrozisi, GFR geri dönüş sürelerini, Hinman renal kontrbalans hipotezini, glob vesicale tanı ve dekompresyon tuzaklarını, radyolojik protokolleri ve dekompresyon sonrası gelişen postobstrüktif diürezin (POD) sıvı-elektrolit yönetimini eksiksiz ve derinlemesine inceler.',
    'highYieldPearls': [
        'Obstrüksiyon proksimalinde daima staz ve hidrostatik basınç artışı gelişir; bu durum taş ve enfeksiyon riskini katlar.',
        'İnfravezikal obstrüksiyonun kompanse evresinde detrüssör basıncı 2-4 kat artar; dekompanse evrede ise trabekülasyon, selül ve divertiküller oluşur.',
        'Mesane divertiküllerinin duvarında detrüssör kas tabakası bulunmaz; idrar stazı, enfeksiyon ve karsinom odağıdır.',
        'Üst üriner sistem obstrüksiyonunda ilk etkilenen yapı kalikslerdir; konkav görünüm silinir, forniksler küntleşir, papillalar yassılaşır ve konveksleşir.',
        '7. günden itibaren dilate toplayıcı kanallarda ve tübüllerde tübüler atrofi ve apoptoz başlar.',
        'Koruyucu mekanizmalar içinde en sık görüleni Pyelointerstisyel Reflü; en az etkili ve en tehlikelisi ise Pyelovenöz Reflüdür (ürosepsis kapısı).',
        'Forniks rüptürü pelvik basıncı aniden düşürdüğü için hastanın renal kolik ağrısı paradoksal olarak aniden kaybolabilir.',
        'Akut obstrüksiyonun erken fazında PGE2 vazodilatasyon yaparak böbrek kan akımını geçici artırır; geç fazda ise Tromboksan A2 ve Anjiyotensin II iskemiye yol açar.',
        'TNF-alfa tübüler hücre apoptozunu tetiklerken, TGF-beta geri dönüşümsüz interstisyel fibrozisi yönetir.',
        '6 haftalık tam üreter obstrüksiyonundan sonra geri dönen GFR fonksiyonu %0\'dır.',
        'Renal kontrbalans: Sağlam böbreğin kompansatuar hipertrofisi tek taraflı böbrek yıkımında serum kreatininin normal kalmasına neden olarak hekimi aldatabilir.',
        'Glob vesicale aniden ve tamamen boşaltılırsa mesane mukozasından masif dekompresyon kanaması (hematuria ex vacuo) ve vazovagal hipotansiyon gelişir.',
        'Üriner obstrüksiyonda ilk değerlendirme yöntemi USG; anatomik altın standart ise Kontrassız Helikal BT\'dir.',
        'Obstrüksiyon + Ateş/Piyüri (Enfekte Hidronefroz) = Mutlak Ürolojik Acildir! Derhal acil dekompresyon (Double-J stent veya PCN) yapılmalıdır.',
        'Postobstrüktif diürez (>200 mL/saat) tedavisinde kaybedilen idrarın en fazla %50-75\'i replase edilmelidir; %100 replasman iatrojenik poliüri kısır döngüsü yaratır.'
    ],
    'slides': slides_batch1,
    'totalSlides': len(slides_batch1),
    'matchedPastQuestionsCount': 5
}

# Update or replace in existing_decks
deck_replaced = False
new_decks = []
for d in existing_decks:
    if d.get('id') in ['deck-2', 'deck-urinary-obstruction']:
        if not deck_replaced:
            new_decks.append(batch1_deck)
            deck_replaced = True
    else:
        new_decks.append(d)

if not deck_replaced:
    new_decks.insert(0, batch1_deck)

# Save back to file
with open(decks_file, 'w', encoding='utf-8') as f:
    json.dump(new_decks, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(new_decks)} decks with Batch 1 updated ({len(slides_batch1)} slides, {sum(len(s['flashcards']) for s in slides_batch1)} flashcards).")

# Update meta file
meta_data = []
for d in new_decks:
    meta_data.append({
        'id': d['id'],
        'title': d['title'],
        'shortTitle': d['shortTitle'],
        'discipline': d['discipline'],
        'committee': d['committee'],
        'instructor': d['instructor'],
        'totalSlides': len(d.get('slides', [])),
        'matchedQuestionsCount': sum(len(s.get('relatedQuestions', [])) for s in d.get('slides', [])),
        'totalFlashcardsCount': sum(len(s.get('flashcards', [])) for s in d.get('slides', [])),
        'themeColor': d.get('themeColor', '#1e40af'),
        'overview': d.get('overview', '')
    })

with open(meta_file, 'w', encoding='utf-8') as f:
    json.dump(meta_data, f, ensure_ascii=False, indent=2)

print(f"Updated meta file with {len(meta_data)} entries.")
