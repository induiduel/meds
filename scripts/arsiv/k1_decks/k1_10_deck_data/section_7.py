"""
Kromozomal Hastalıklar ve Genetik Danışma (Ders 10) - Bölüm 7 (Slayt 61 - 70)
Konu: Gonozomal Kromozom Anomalileri, X İnaktivasyonu, Klinefelter Sendromu (47,XXY), 47,XYY ve Trizomi X
Checkpoint: Slayt 69 ([TEKRAR SAYFASI - CHECKPOINT 7])
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_7_slides():
    return [
        # Slayt 61
        {
            "title": "Gonozomal Kromozom Anomalileri ve X İnaktivasyonu (Lyon Hipotezi)",
            "subtitle": "Cinsiyet Kromozomu Dozaj Kompansasyonu ve Barr Cismi Biyolojisi",
            "badge": "X İnaktivasyonu",
            "coreContent": {
                "text": "Cinsiyet kromozomu (gonozom; X ve Y) anomalileri, otozomal anomalilere kıyasla hem popülasyonda çok daha yüksek sıklıkta görülür (yaklaşık 1/400 ila 1/500 canlı doğum) hem de fenotipik olarak çok daha hafif ve tolere edilebilir tablolara yol açar. Gonozomal anöploidilerin bu denli iyi tolere edilmesinin arkasında iki temel biyolojik mekanizma yatar: (1) Dişi somatik hücrelerinde erken embriyogenezde (blastokist evresinde) gerçekleşen X kromozomu inaktivasyonu (Lyonizasyon): Mary Lyon tarafından tanımlanan bu hipoteze göre, hücredeki X kromozomu sayısı ne olursa olsun (XX, XXY, XXX), yalnız tek bir aktif X kromozomu kalır; fazlalık olan tüm diğer X kromozomları heterokromatinleşerek nükleus zarının kenarında yoğun, inaktif 'Barr cisimciği' (seks kromatini) haline getirilir. (2) Y kromozomunun genetik içerik açısından son derece fakir olması ve temelde yalnızca erkek cinsiyet determinasyonunu yöneten SRY genini taşımasıdır.",
                "keyBullets": [
                    {"title": "Yüksek İnsidans / Hafif Fenotip", "desc": "Gonozomal anomaliler 1/400 sıklıkta görülür ve otozomlara göre çok hafiftir.", "isKey": True},
                    {"title": "Lyon Hipotezi", "desc": "Hücredeki X sayısı kaç olursa olsun tek bir X aktif kalır, fazlalıklar Barr cismi olur.", "isKey": True},
                    {"title": "Barr Cismi Kuralı", "desc": "Barr cisimciği sayısı = Toplam X kromozomu sayısı eksi bir (N - 1).", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Karyotip", "Toplam X Sayısı", "Barr Cisimciği Sayısı (N - 1)", "Fenotipik Cinsiyet"],
                    [
                        [("46,XY (Normal Erkek)", False, ""), ("1", False, ""), ("0 (Barr cismi yok)", False, ""), ("Normal erkek", False, "")],
                        [("46,XX (Normal Dişi)", False, ""), ("2", False, ""), ("1 Barr cismi", True, "Dişi hücrede tek inaktif X"), ("Normal dişi", False, "")],
                        [("45,X (Turner Sendromu)", False, ""), ("1", False, ""), ("0 (Barr cismi yok)", True, "Tek X'li dişi"), ("Dişi (Turner)", False, "")],
                        [("47,XXY (Klinefelter)", False, ""), ("2", False, ""), ("1 Barr cismi", True, "Erkekte dişi kromatini"), ("Erkek (Klinefelter)", False, "")],
                        [("47,XXX (Triple X)", False, ""), ("3", False, ""), ("2 Barr cismi", True, "İki inaktif X"), ("Dişi (Trizomi X)", False, "")]
                    ]
                ),
                make_cloze(
                    "İnaktif hale getirilen X kromozomunun interfaz nükleus zarının iç kenarında oluşturduğu yoğunlaşmış heterokromatin kütlesine Barr cisimciği denir.",
                    "Barr cisimciği",
                    "Seks kromatini cisimcik adını anımsayınız"
                ),
                make_micro_quiz(
                    "Karyotipi 48,XXXY olan polizomik bir erkeğin somatik hücrelerinde yapılan interfaz nükleus incelemesinde kaç adet Barr cisimciği (seks kromatini) saptanır?",
                    {
                        "A": "Hiç saptanmaz (0)",
                        "B": "1 adet",
                        "C": "2 adet",
                        "D": "3 adet",
                        "E": "4 adet"
                    },
                    "C",
                    {
                        "A": "Tek X taşıyanlarda 0'dır.",
                        "B": "47,XXY'de 1 tanedir.",
                        "C": "Doğru cevap C'dir: Barr cisimciği sayısı formülü (X sayısı - 1) olup, 3 X kromozomu olan bu bireyde (3 - 1) = 2 adet Barr cismi bulunur.",
                        "D": "49,XXXXY'de 3 tanedir.",
                        "E": "5 X kromozomu gerekir."
                    }
                )
            ],
            "spotPearls": [
                "Barr cisimciği sayısı = X kromozomu sayısı - 1.",
                "Lyon hipotezi: Tek bir X aktif kalır, fazlalık tüm X'ler inaktif hale getirilir.",
                "Gonozomal anomaliler X inaktivasyonu ve Y'nin gen fakirliği sayesinde otozomlardan çok daha hafiftir."
            ]
        },

        # Slayt 62
        {
            "title": "Psödootozomal Bölgeler (PAR1 ve PAR2) ve X İnaktivasyonundan Kaçış",
            "subtitle": "X ve Y Homolojisi, SHOX Geni ve Anöploidi Fenotipinin Kökeni",
            "badge": "Psödootozomal Bölgeler",
            "coreContent": {
                "text": "Eğer fazlalık X kromozomları tamamen inaktive ediliyorsa, neden Klinefelter (47,XXY) veya Turner (45,X) sendromlu bireylerde belirgin klinik anomaliler ortaya çıkar? Bu temel biyolojik sorunun yanıtı, X ve Y kromozomlarının uç kısımlarında yer alan 'Psödootozomal Bölgeler'de (PAR1 ve PAR2) ve X inaktivasyonundan kaçan (escape) genlerde gizlidir. X ve Y kromozomlarının telomerik uçlarındaki PAR bölgeleri birbirleriyle tam dizi homolojisine sahiptir; erkek mayozunda X ve Y kromozomları bu bölgeler üzerinden eşleşir ve zorunlu bir krossing-over gerçekleştirir. Çok kritik bir moleküler kural olarak: PAR bölgelerindeki genler (ve X'in non-PAR bölgesindeki genlerin yaklaşık %15'i) dondurulan X kromozomunda İNAKTİVE EDİLMEZ; iki kopyadan da ifade edilmeye devam eder. Bu genlerin en prototipi PAR1'de yer alan ve boy uzamasını yöneten SHOX genidir. Turner'da SHOX'un tek kopyaya düşmesi kısa boya, Klinefelter'da ise 3 kopyaya çıkması aşırı uzun boya yol açar.",
                "keyBullets": [
                    {"title": "PAR Bölgeleri (PAR1 ve PAR2)", "desc": "X ve Y kromozomlarının homolog uçlarıdır; mayozda eşleşmeyi sağlarlar.", "isKey": True},
                    {"title": "İnaktivasyondan Kaçış", "desc": "PAR bölgeleri inaktive edilen X'te de sessizleştirilmez; iki kopyadan okunur.", "isKey": True},
                    {"title": "SHOX Geni Etkisi", "desc": "PAR1'deki SHOX gen dozajı Turner'da kısa boyu, Klinefelter ve XYY'de uzun boyu belirler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "SHOX Gen Dozajının Fenotipe Yansıması",
                    "Turner Sendromu (45,X - Tek SHOX)",
                    "Tek bir PAR1 bölgesi ve tek bir SHOX geni bulunur; haploinsüfisyens nedeniyle belirgin kısa boy ve kemik displazisi gelişir.",
                    "Klinefelter / XYY Sendromu (3 SHOX Kopyası)",
                    "Üç adet PAR1 bölgesi ve üç kopya SHOX geni bulunur; aşırı kemik uzaması ve orantısız uzun boy gelişir."
                ),
                make_cloze(
                    "X ve Y kromozomlarının uç kısımlarında yer alan ve X inaktivasyonundan kaçan homolog bölgelere psödootozomal bölgeler adı verilir.",
                    "psödootozomal",
                    "Yalancı otozomal bölge terimini anımsayınız"
                ),
                make_active_recall(
                    "X ve Y kromozomlarının PAR1 bölgesinde yer alan, dozaj eksikliğinde Turner sendromunda kısa boya, fazlalığında ise Klinefelter'da uzun boya yol açan kritik homeobox geni hangisidir?",
                    "SHOX (Short Stature Homeobox) genidir.",
                    "Boy uzaması düzenleyici homeobox geni"
                )
            ],
            "spotPearls": [
                "X ve Y kromozomları PAR bölgeleri üzerinden mayozda krossing-over yapar.",
                "PAR genleri X inaktivasyonundan KAÇAR; inaktif X'te de aktif kalırlar.",
                "PAR1'deki SHOX geninin tek kopyası Turner'da kısa boy, 3 kopyası Klinefelter'da uzun boy yapar."
            ]
        },

        # Slayt 63
        {
            "title": "Klinefelter Sendromu (47,XXY): Epidemiyoloji ve Ebeveynsel Köken",
            "subtitle": "Erkek İnfertilitesinin En Sık Genetik Nedeni ve Karyotip Dağılımı",
            "badge": "Klinefelter Sendromu",
            "coreContent": {
                "text": "Klinefelter sendromu (47,XXY), erkeklerde en sık rastlanan cinsiyet kromozomu anomalisi ve erkek infertilitesinin tek başına en yaygın genetik nedenidir. Canlı doğan erkek bebeklerdeki sıklığı yaklaşık 1/500 ila 1/1000 (ortalama 1/660) arasındadır. Olguların yaklaşık %85'i klasik serbest 47,XXY karyotipine sahipken, yaklaşık %15'i mozaik (46,XY / 47,XXY) veya yüksek dereceli polizomik varyantlardır (48,XXXY, 49,XXXXY). Moleküler analizler, Klinefelter sendromundaki ekstra X kromozomunun yaklaşık %50 oranında maternal, %50 oranında paternal kökenli olduğunu ortaya koymuştur. Paternal kökenli olgular paternal Mayoz I aşamasında X ve Y kromozomlarının psödootozomal bölgedeki (PAR1) anormal rekombinasyonu ve ayrılma kusurundan kaynaklanır. Maternal kökenli olgularda ise ileri anne yaşı risk artıran bir faktördür.",
                "keyBullets": [
                    {"title": "Görülme Sıklığı", "desc": "Canlı erkek doğumlarında yaklaşık 1/660 sıklıkla en yaygın gonozomal anöploididir.", "isKey": True},
                    {"title": "Eşit Ebeveyn Kökeni", "desc": "Ekstra X kromozomunun kökeni yaklaşık %50 maternal, %50 paternaldir.", "isKey": True},
                    {"title": "Paternal Mayoz I Hatası", "desc": "Paternal kaynaklı olgular X ve Y'nin Mayoz I'de ayrılamamasından doğar.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Ebeveyn Kaynağı", "Görülme Payı", "Gerçekleştiği Mayoz Evresi", "İlişkili Faktör"],
                    [
                        [("Paternal Köken (Baba)", False, ""), ("Yaklaşık %50", True, "Yarı yarıya dağılım"), ("Paternal Mayoz I (X ve Y ayrılamaması)", True, "X-Y ayrılma kusuru"), ("PAR1 anormal rekombinasyonu"), ],
                        [("Maternal Köken (Anne)", False, ""), ("Yaklaşık %50", True, "Yarı yarıya dağılım"), ("Maternal Mayoz I veya Mayoz II", False, ""), ("İleri anne yaşı pozitif korelasyonu"), ]
                    ]
                ),
                make_micro_quiz(
                    "Klinefelter sendromunda (47,XXY) fazladan bulunan X kromozomunun ebeveynsel kökeni incelendiğinde aşağıdaki ifadelerden hangisi bilimsel olarak doğrudur?",
                    {
                        "A": "Ekstra X daima %100 anne kaynaklıdır",
                        "B": "Ekstra X daima %100 baba kaynaklıdır",
                        "C": "Ekstra X kromozomunun yaklaşık %50'si anne, %50'si baba kaynaklıdır",
                        "D": "Yalnızca mitotik ayrılma hatasıyla oluşur",
                        "E": "Yalnızca 45 yaş üstü babaların çocuklarında görülür"
                    },
                    "C",
                    {
                        "A": "Down sendromu gibi maternal baskın değildir.",
                        "B": "Yalnız babadan gelmez.",
                        "C": "Doğru cevap C'dir: Klinefelter sendromunda ekstra X yaklaşık %50 maternal, %50 paternal kaynaklıdır (paternal mayoz I'de XY ayrılmama hatası sıktır).",
                        "D": "Mayotik ayrılamama primer yoldur.",
                        "E": "Baba yaşından ziyade anne yaşı maternal grupta etkilidir."
                    }
                ),
                make_cloze(
                    "Klinefelter sendromunda (47,XXY) fazladan bulunan X kromozomu yaklaşık %50 oranında baba kaynaklıdır.",
                    "%50",
                    "Paternal köken oranını düşününüz"
                )
            ],
            "spotPearls": [
                "Klinefelter sendromu en sık gonozomal anöploididir (1/660 erkek).",
                "Ekstra X kromozomu yaklaşık %50 maternal, %50 paternal kaynaklıdır.",
                "Paternal olgular babanın Mayoz I'inde X ve Y'nin ayrılamamasıyla oluşur."
            ]
        },

        # Slayt 64
        {
            "title": "Klinefelter Sendromunda Testiküler Patoloji: Hiyalinizasyon ve İnfertilite",
            "subtitle": "Seminifer Tübül Sklerozu, Leydig Hücre Hiperplazisi ve Azospermi",
            "badge": "Testiküler Patoloji",
            "coreContent": {
                "text": "Klinefelter sendromlu bireylerde fiziksel ve seksüel gelişim puberte dönemine kadar tamamen normal seyreder. Çocukluk çağında fenotipik bir belirti vermediği için hastaların çok büyük bir kısmı adölesan dönemine veya evlenip çocuk sahibi olamadıkları erişkin döneme kadar tanı almazlar. Puberte ile birlikte hipofizden pulsatil GnRH uyarısıyla FSH ve LH salgısı artar. Ancak testis dokusunda fazladan bulunan X kromozomunun germ hücreleri üzerindeki sitotoksik etkisi nedeniyle seminifer tübüllerde ilerleyici atrofi, fibrozis ve hiyalinizasyon (kollajenleşme) başlar. Germ hücreleri tamamen kaybolur (Sertoli-cell-only benzeri tablo) ve seminifer tübüller tıkanarak skleroze olur. Leydig hücreleri kompensatuar olarak psödohiperplaziye uğrar ancak yeterli testosteron üretemez. Sonuç olarak ejakülatta hiç olgun sperm bulunmaması tablosu olan azospermi gelişir ve hastalar daima primer infertil kalırlar.",
                "keyBullets": [
                    {"title": "Puberte Öncesi Sessizlik", "desc": "Puberteye kadar testisler ve fiziksel gelişim normaldir; tanı çoğunlukla erişkinde konur.", "isKey": True},
                    {"title": "Tübüler Hiyalinizasyon", "desc": "Seminifer tübüllerde ilerleyici fibrozis, skleroz ve germ hücre kaybı gelişir.", "isKey": True},
                    {"title": "Primer İnfertilite", "desc": "Testiküler yetmezlik sonucu mutlak azospermi gelişir; hastalar daima infertildir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_causal_chain(
                    "Klinefelter Testiküler Yıkım ve Azospermi Zinciri",
                    [
                        "1. Ekstra X kromozomu testiste germ hücre mezenkiminde sitotoksik stres yaratır",
                        "2. Puberte sonrasında seminifer tübüllerde ilerleyici fibrozis ve hiyalinizasyon başlar",
                        "3. Spermatogonyumlar ölür; tübüller elastikiyetini kaybederek küçük sert fibröz yumrulara döner",
                        "4. Ejakülatta hiç spermatozoa bulunamaz (azospermi) ve kalıcı primer infertilite gelişir"
                    ]
                ),
                make_cloze(
                    "Klinefelter sendromlu erkeklerde seminifer tübüllerin hiyalinizasyonu ve germ hücrelerinin kaybı sonucu ejakülatta hiç sperm bulunmaması durumuna azospermi denir.",
                    "azospermi",
                    "Sperm yokluğu tıbbi terimini anımsayınız"
                ),
                make_active_recall(
                    "Klinefelter sendromlu hastalar klinik polikliniklere hayatlarının hangi döneminde ve en sık hangi yakınma ile başvurarak kesin tanı alırlar?",
                    "Genellikle genç erişkinlik döneminde, evlilik sonrası çocuk sahibi olamama (primer infertilite) nedeniyle başvurarak tanı alırlar.",
                    "Erişkin tanı başvuru nedeni"
                )
            ],
            "spotPearls": [
                "Klinefelter sendromu puberteye kadar klinik belirti vermez; en sık infertilite ile tanı alır.",
                "Testis histolojisinde seminifer tübül hiyalinizasyonu ve atrofi görülür.",
                "Germ hücresi kaybına bağlı mutlak azospermi vardır; hastalar daima infertildir."
            ]
        },

        # Slayt 65
        {
            "title": "Klinefelter Sendromunda Fiziksel Özellikler ve Hormon Profili",
            "subtitle": "Önökoid Vücut Yapısı, Jinekomasti ve Hipergonadotropik Hipogonadizm",
            "badge": "Klinik ve Endokrin Profil",
            "coreContent": {
                "text": "Klinefelter sendromunun fizik muayenesinde karakteristik bir habitus mevcuttur. Ekstra SHOX gen dozajı nedeniyle boy uzundur; özellikle bacak boyunun gövdeye oranla aşırı uzun olduğu 'önökoid' vücut yapısı dikkati çeker. Testisler belirgin derecede küçük (<2-4 ml), sert ve hipoplaziktir; penis boyutu genellikle normal veya hafif küçüktür. Sekonder seks karakterlerinin gelişimi eksiktir; sakal, bıyık ve vücut kıllanması seyrektir, pubik kıllanma kadınsı (ters üçgen) dağılım gösterir. Olguların yaklaşık %40-50'sinde belirgin jinekomasti (erkekte meme büyümesi) izlenir; bu durum Klinefelter hastalarında meme kanseri gelişme riskini genel erkek popülasyonuna kıyasla 20-50 kat artırır. Endokrin hormon panelinde klasik 'Hipergonadotropik Hipogonadizm' tablosu saptanır: Testiküler geri bildirimin (inhibin B ve testosteron) çökmesiyle serum FSH ve LH düzeyleri belirgin derecede yüksek, serbest testosteron düzeyi ise düşüktür.",
                "keyBullets": [
                    {"title": "Önökoid Habitus", "desc": "Uzun boy, bacakların gövdeye oranla aşırı uzun olması ve dar omuzlar.", "isKey": True},
                    {"title": "Jinekomasti ve Kanser", "desc": "Jinekomasti sıktır; meme kanseri riski erkeklere göre 20-50 kat artmıştır.", "isKey": True},
                    {"title": "Hormon Profili", "desc": "Hipergonadotropik hipogonadizm: FSH ve LH yüksek, testosteron düşüktür.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Hormonal Parametre", "Serum Düzeyi Değişimi", "Patofizyolojik Mekanizma"],
                    [
                        [("Serum FSH Düzeyi", False, ""), ("Belirgin derecede YÜKSEK", True, "FSH artışı"), ("Sertoli hücresi yokluğu ve İnhibin B negatif geri bildiriminin çökmesi", False, "")],
                        [("Serum LH Düzeyi", False, ""), ("Belirgin derecede YÜKSEK", True, "LH artışı"), ("Düşük testosteron nedeniyle hipofizer LH deşarjı", False, "")],
                        [("Serum Testosteron", False, ""), ("Düşük veya düşük-normal", True, "Androjen azlığı"), ("Leydig hücresi disfonksiyonu ve testosteron sentez yetersizliği", False, "")],
                        [("Östradiol / Testosteron Oranı", False, ""), ("Belirgin derecede ARTMIŞ", False, ""), ("Jinekomasti ve kadınsı yağ dağılımının temel tetikleyicisi", False, "")]
                    ]
                ),
                make_micro_quiz(
                    "24 yaşında uzun boylu, jinekomastisi olan, testis hacimleri bilateral 3 ml ölçülen ve infertilite nedeniyle başvuran bir erkeğin hormon profilinde aşağıdakilerden hangisi beklenir?",
                    {
                        "A": "Düşük FSH, Düşük LH, Yüksek Testosteron",
                        "B": "Yüksek FSH, Yüksek LH, Düşük Testosteron",
                        "C": "Normal FSH, Normal LH, Normal Testosteron",
                        "D": "Düşük FSH, Yüksek LH, Yüksek Testosteron",
                        "E": "Yüksek FSH, Düşük LH, Düşük Testosteron"
                    },
                    "B",
                    {
                        "A": "Sekonder hipogonadizm profilidir.",
                        "B": "Doğru cevap B'dir: Klinefelter sendromu primer testiküler yetmezlik (hipergonadotropik hipogonadizm) yapar; FSH ve LH yüksek, testosteron düşüktür.",
                        "C": "Normal profil Klinefelter'a uymaz.",
                        "D": "FSH düşük olamaz.",
                        "E": "LH da mutlaka yükselir."
                    }
                ),
                make_cloze(
                    "Klinefelter sendromlu erkeklerde meme dokusunun hipertrofisine bağlı olarak meme kanseri riski genel erkek popülasyonuna kıyasla belirgin derecede artmıştır.",
                    "meme kanseri",
                    "Erkekte risk artışı gösteren maligniteyi anımsayınız"
                )
            ],
            "spotPearls": [
                "Klinefelter sendromunda hormon profili: YÜKSEK FSH, YÜKSEK LH, DÜŞÜK TESTOSTERONDUR (hipergonadotropik hipogonadizm).",
                "Önökoid uzun boy, küçük sert testisler (<4 ml) ve jinekomasti karakteristiktir.",
                "Erkek meme kanseri riski 20-50 kat artmıştır; tedavi 11-12 yaşta başlanan testosteron replasmanıdır."
            ]
        },

        # Slayt 66
        {
            "title": "Yüksek Dereceli Polizomi X Erkekleri: 48,XXXY ve 49,XXXXY",
            "subtitle": "Kromozom Dozajı Kuralı: Ekstra X Sayısı Arttıkça Fenotipik Yıkım",
            "badge": "Polizomik Varyantlar",
            "coreContent": {
                "text": "Klinefelter sendromunun klasik 47,XXY karyotipinin yanı sıra, çoklu mayotik ayrılamamalar sonucunda ortaya çıkan yüksek dereceli cinsiyet kromozomu polisomileri de mevcuttur: 48,XXYY, 48,XXXY ve 49,XXXXY karyotipleri bu grubun başlıca örnekleridir. Tıbbi genetiğin en temel aksiyomlarından biri olarak: Bir erkek karyotipinde X kromozomlarının sayısı arttıkça, fenotipik dismorfoloji belirginleşir, seksüel gelişim kusurları derinleşir ve zihinsel yetersizliğin derecesi dramatik biçimde ağırlaşır. Klasik 47,XXY olgularında hafif öğrenme güçlüğü görülürken, 48,XXXY olgularında orta derece, 49,XXXXY olgularında ise derin zekâ geriliği (IQ < 30) izlenir. 49,XXXXY erkeklerinde mikrognati, hipertelorizm, epikantus, radioulnar sinostoz (önkol kemiklerinin kaynaşması), inmemiş testis (kriptorşidizm), mikropenis ve ağır konjenital kalp defektleri tabloya eklenir.",
                "keyBullets": [
                    {"title": "Dozaj-Ağırlık Kuralı", "desc": "Karyotipteki her bir fazladan X kromozomu IQ puanında yaklaşık 10-15 puanlık düşüşe yol açar.", "isKey": True},
                    {"title": "49,XXXXY Fenotipi", "desc": "Ağır mental retardasyon, mikropenis, kriptorşidizm ve radioulnar sinostozla seyreder.", "isKey": True},
                    {"title": "Barr Cismi Sayısı", "desc": "48,XXXY karyotipinde 2 adet, 49,XXXXY karyotipinde ise 3 adet Barr cisimciği bulunur.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Karyotip", "Barr Cismi Sayısı", "Zihinsel Durum (Ortalama IQ)", "Karakteristik Klinik Tablo"],
                    [
                        [("47,XXY (Klasik)", False, ""), ("1", False, ""), ("IQ: 85 - 95 (Hafif öğrenme güçlüğü)", True, "Hafif bilişsel etkilenme"), ("Önökoid uzun boy, infertilite, jinekomasti", False, "")],
                        [("48,XXXY", False, ""), ("2", False, ""), ("IQ: 40 - 60 (Orta derece retardasyon)", True, "Belirgin zekâ geriliği"), ("Klinodaktili, belirgin hipogonadizm", False, "")],
                        [("49,XXXXY", False, ""), ("3", False, ""), ("IQ: 20 - 40 (Ağır-derin retardasyon)", True, "Derin zihinsel yetersizlik"), ("Radioulnar sinostoz, mikropenis, ağır dismorfoloji", False, "")]
                    ]
                ),
                make_cloze(
                    "49,XXXXY karyotipine sahip bir erkeğin somatik hücre nükleusunda tam olarak 3 adet Barr cisimciği izlenir.",
                    "3",
                    "Barr cisimciği sayısını hesaplayınız (N - 1)"
                ),
                make_active_recall(
                    "Polizomi X varyantı olan 49,XXXXY sendromunda iskelet sisteminde patognomonik olarak saptanan önkol kemik kaynaşması anomalisi nedir?",
                    "Radioulnar sinostoz (radius ve ulna kemiklerinin konjenital füzyonu) anomalisidir.",
                    "Önkol kemik füzyonu"
                )
            ],
            "spotPearls": [
                "Erkek karyotipinde X kromozomu sayısı arttıkça ZİHİNSEL GERİLİK VE DİSMORFOZ AĞIRLAŞIR.",
                "Her fazladan X kromozomu ortalama IQ'yu yaklaşık 15 puan düşürür.",
                "49,XXXXY sendromunda radioulnar sinostoz, mikropenis ve derin retardasyon görülür."
            ]
        },

        # Slayt 67
        {
            "title": "47,XYY Sendromu (Jakob Sendromu): Biyoloji, Büyüme ve Fertilite",
            "subtitle": "Paternal Mayoz II Hatası, Uzun Boy ve Normal Üreme Potansiyeli",
            "badge": "47,XYY Sendromu",
            "coreContent": {
                "text": "47,XYY sendromu (Jakob sendromu), erkeklerde fazladan bir Y kromozomunun bulunmasıyla karakterize gonozomal bir anöploididir (yaklaşık 1/1000 canlı erkek doğum). Fazladan Y kromozomunun oluşum mekanizması istisnasız tektir: Paternal Mayoz II aşamasında kardeş Y kromatitlerinin ayrılamaması (nondisjunction) sonucu oluşan YY sperminin (24,YY) normal bir oositle döllenmesidir. 47,XYY erkeklerinin en belirgin fiziksel özelliği aşırı uzun boydur; ortalama boy popülasyon ortalamasının belirgin üzerindedir (SHOX ve Y kromozomu büyüme genleri etkisi). Zekâ düzeyi genellikle normal sınırlardadır ancak motor koordinasyon zayıflığı, sakarlık, konuşma gecikmesi ve hafif öğrenme sorunları görülebilir. Çok kritik bir klinik ve sınav spotu olarak: 47,XYY erkekleri KLINEFELTER'IN AKSİNE GENELDE FERTİLDİR; sperm parametreleri normaldir ve doğal yolla normal kromozomlu (46,XX veya 46,XY) sağlıklı çocuk sahibi olabilirler.",
                "keyBullets": [
                    {"title": "Oluşum Mekanizması", "desc": "İstisnasız Paternal Mayoz II kardeş Y kromatit ayrılmama hatasıdır.", "isKey": True},
                    {"title": "Uzun Boy ve Normal IQ", "desc": "Aşırı uzun boyludurlar; bilişsel kapasite genellikle normal sınırlar içindedir.", "isKey": True},
                    {"title": "Normal Fertilite Kuralı", "desc": "Klinefelter'ın aksine FERTİLDİRLER; normal sağlıklı çocuk sahibi olabilirler.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Klinefelter (47,XXY) vs Jakob Sendromu (47,XYY) Karşılaştırması",
                    "Klinefelter Sendromu (47,XXY)",
                    "Küçük sert testisler, testiküler hiyalinizasyon, azospermi, jinekomasti; kesinlikle İNFERTİLDİR; 1 Barr cismi vardır.",
                    "47,XYY Sendromu (Jakob Sendromu)",
                    "Normal testis boyutları, normal sperm üretimi, jinekomasti yok; genellikle FERTİLDİR; Barr cismi yoktur (0)."
                ),
                make_micro_quiz(
                    "47,XYY karyotipine sahip bir bireyin sitogenetik oluşum mekanizması aşağıdakilerden hangisinde kesin ve doğru olarak tanımlanmıştır?",
                    {
                        "A": "Maternal Mayoz I ayrılamaması",
                        "B": "Maternal Mayoz II ayrılamaması",
                        "C": "Paternal Mayoz I ayrılamaması",
                        "D": "Paternal Mayoz II ayrılamaması",
                        "E": "Post-zigotik mitoz anafaz gecikmesi"
                    },
                    "D",
                    {
                        "A": "Annede Y kromozomu yoktur.",
                        "B": "Annede Y kromozomu yoktur.",
                        "C": "Paternal Mayoz I'de XY ayrılamaz ve XXY (Klinefelter) oluşur.",
                        "D": "Doğru cevap D'dir: 47,XYY ancak babanın Mayoz II evresinde kardeş Y kromatitlerinin ayrılamamasıyla üretilen YY spermi ile oluşabilir.",
                        "E": "Mayotik kökenlidir."
                    }
                ),
                make_cloze(
                    "Klinefelter sendromlu erkeklerin daima infertil olmasına karşılık, 47,XYY karyotipine sahip erkekler genel olarak fertil olup normal çocuk sahibi olabilirler.",
                    "fertil",
                    "Üreme yeteneği durumunu anımsayınız"
                )
            ],
            "spotPearls": [
                "47,XYY sendromunun tek oluşum yolu PATERNAL MAYOZ II ayrılamamasıdır.",
                "47,XYY erkekleri aşırı uzun boyludur ancak FERTİLDİRLER.",
                "Barr cisimciği içermezler (0 Barr cismi)."
            ]
        },

        # Slayt 68
        {
            "title": "Trizomi X (47,XXX) ve Yüksek Dereceli X Polizomi Dişileri",
            "subtitle": "Triple-X Sendromu, İki Barr Cisimciği ve Normal Üreme",
            "badge": "Trizomi X",
            "coreContent": {
                "text": "Trizomi X (47,XXX / Triple-X sendromu), canlı doğan kız bebeklerde yaklaşık 1/1000 sıklıkla görülen en yaygın dişi gonozomal anöploidisidir. Fazladan X kromozomu olguların %90'ından fazlasında maternal kaynaklıdır ve ileri anne yaşıyla pozitif korelasyon gösterir. Blastokist evresinde gerçekleşen Lyonizasyon sürecinde, hücre başına iki adet X kromozomu inaktive edilir; bu nedenle interfaz nükleusunda iki adet Barr cisimciği izlenir. Trizomi X'li kız çocukları ve kadınlar genellikle belirgin bir dismorfik anomali sergilemezler; uzun boy ve epikantus görülebilir. Dil gelişimi gecikmesi, okuma güçlüğü (disleksi) ve hafif psikososyal uyumsuzluklar bildirilse de zekâ düzeyleri genellikle normal veya normale yakındır. En önemli klinik özellik olarak: Trizomi X kadınlarında pubertal gelişim, menstrüel siklus ve FERTİLİTE GENELDE TAMAMEN NORMALDİR; normal çocuk sahibi olabilirler. Ancak 48,XXXX ve 49,XXXXX olgularında derin retardasyon ve dismorfizm kaçınılmazdır.",
                "keyBullets": [
                    {"title": "Görülme Sıklığı", "desc": "Kız doğumlarında yaklaşık 1/1000 sıklıkta görülür; %90 maternal kaynaklıdır.", "isKey": True},
                    {"title": "İki Barr Cisimciği", "desc": "Hücrede iki X inaktive edildiğinden 2 adet Barr cisimciği saptanır.", "isKey": True},
                    {"title": "Normal Fertilite", "desc": "Pubertal gelişim ve üreme kapasitesi olguların ezici çoğunluğunda normaldir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Karyotip", "Barr Cismi Sayısı", "Fertilite Durumu", "Fenotipik Cinsiyet"],
                    [
                        [("47,XXX (Triple X)", False, ""), ("2", True, "Çift Barr cismi"), ("Genelde normal ve fertil", True, "Doğal gebe kalabilir"), ("Dişi"), ],
                        [("48,XXXX (Tetra X)", False, ""), ("3", True, "Üç Barr cismi"), ("Prematür ovaryan yetmezlik riski", False, ""), ("Dişi (orta zekâ geriliği)"), ],
                        [("49,XXXXX (Penta X)", False, ""), ("4", True, "Dört Barr cismi"), ("Tamamen steril / infantil gonad", False, ""), ("Dişi (ağır dismorfik tablo)"), ]
                    ]
                ),
                make_cloze(
                    "47,XXX (Triple-X) karyotipine sahip bir kadının ağız mukoza epitel hücrelerinde 2 adet Barr cisimciği saptanır.",
                    "2",
                    "Triple X'teki Barr cisimciği sayısını hesaplayınız"
                ),
                make_active_recall(
                    "Trizomi X (47,XXX) karyotipinde iki X kromozomu inaktive edildiği halde bu kadınlarda boyun uzun olmasının moleküler nedeni nedir?",
                    "İnaktive edilen iki X kromozomunda da psödootozomal PAR1 bölgesindeki SHOX geninin inaktivasyondan kaçarak 3 doz olarak okunmasıdır.",
                    "SHOX geninin inaktivasyondan kaçışı"
                )
            ],
            "spotPearls": [
                "47,XXX (Triple X) sendromunda 2 adet Barr cisimciği bulunur.",
                "Fertilite ve pubertal gelişim genellikle tamamen normaldir.",
                "Hafif konuşma geriliği ve uzun boy dışında belirgin fiziksel anomali vermez."
            ]
        },

        # Slayt 69 (CHECKPOINT 7)
        {
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Gonozomal Polizomiler: Klinefelter (47,XXY) ve 47,XYY",
            "subtitle": "Bölüm Sonu Entegrasyonu ve Aktif Hatırlama İstasyonu",
            "badge": "Checkpoint 7",
            "coreContent": {
                "text": "Bu bölümde cinsiyet kromozomu polizomilerinin biyolojik ve klinik özelliklerini entegre ettik. X inaktivasyonu (Lyon hipotezi) sayesinde hücredeki X sayısı kaç olursa olsun tek bir X aktif kalır, fazlalıklar Barr cismine döner (Barr sayısı = X sayısı - 1). Ancak psödootozomal bölgeler (PAR1 ve PAR2) inaktivasyondan kaçar; PAR1'deki SHOX geni boyu uzatır. Klinefelter sendromu (47,XXY; 1/660 erkek) en sık gonozomal anöploididir; ekstra X %50 anne, %50 baba kaynaklıdır (paternal mayoz I hatası). Puberteye kadar sessizdir; pubertede seminifer tübül hiyalinizasyonu ile mutlak azospermi ve primer infertilite gelişir; önökoid uzun boy, küçük sert testisler, jinekomasti (meme kanseri riski artmış) ve hipergonadotropik hipogonadizm (yüksek FSH/LH, düşük testosteron) ile seyreder. 47,XYY sendromu paternal mayoz II hatasıyla oluşur; uzun boyludurlar ancak Klinefelter'ın aksine fertildirler. 47,XXX dişilerinde 2 Barr cismi vardır ve fertildirler.",
                "keyBullets": [
                    {"title": "Barr Cismi Formülü", "desc": "Barr sayısı = X sayısı - 1; PAR bölgeleri inaktivasyondan kaçar (SHOX geni).", "isKey": True},
                    {"title": "Klinefelter (47,XXY)", "desc": "1 Barr cismi; azospermi, infertilite, yüksek FSH/LH, jinekomasti, meme ca riski.", "isKey": True},
                    {"title": "Fertilite Ayrımı", "desc": "Klinefelter mutlak infertildir; 47,XYY ve 47,XXX genel olarak fertildir.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_table(
                    ["Klinik Durum", "Karyotip", "Fertilite Potansiyeli", "Barr Cisimciği Sayısı"],
                    [
                        [("Klinefelter Sendromu", False, ""), ("47,XXY", False, ""), ("Daima İNFERTİL (Azospermi)", True, "Kalıcı kısırlık"), ("1 Barr cismi", False, "")],
                        [("Jakob Sendromu", False, ""), ("47,XYY", False, ""), ("Genelde FERTİL (Normal çocuk sahibi)", True, "Doğal üreme var"), ("0 (Barr cismi yok)", False, "")],
                        [("Trizomi X (Triple X)", False, ""), ("47,XXX", False, ""), ("Genelde FERTİL (Normal menstrüasyon)", True, "Doğal üreme var"), ("2 Barr cismi", False, "")],
                        [("Turner Sendromu", False, ""), ("45,X", False, ""), ("Çoğunlukla İNFERTİL (Çizgi gonad)", False, ""), ("0 (Barr cismi yok)", False, "")]
                    ]
                ),
                make_cloze(
                    "Klinefelter sendromlu erkeklerde hipofizer negatif geri bildirimin çökmesi sonucu serum FSH ve LH düzeyleri belirgin derecede yükselir.",
                    "FSH",
                    "Seminifer tübül yetmezliğinde yükselen gonadotropini anımsayınız"
                ),
                make_active_recall(
                    "Klinefelter sendromunda görülen önökoid uzun boy ile 47,XYY sendromunda görülen uzun boyun ortak moleküler genetik nedeni nedir?",
                    "PAR1 bölgesindeki büyüme geni olan SHOX geninin her iki sendromda da 3 kopya olarak ifade edilmesidir.",
                    "SHOX gen dozaj fazlalığı"
                )
            ],
            "spotPearls": [
                "Klinefelter (47,XXY): 1 Barr cismi, küçük sert testis, azospermi, infertilite, yüksek FSH/LH.",
                "47,XYY: 0 Barr cismi, paternal mayoz II hatası, uzun boy, FERTİLDİR.",
                "47,XXX: 2 Barr cismi, genelde normal fenotip, FERTİLDİR."
            ]
        },

        # Slayt 70
        {
            "title": "Gonozomal Aneuploidilerde Davranışsal, Bilişsel ve Psikososyal Gelişim",
            "subtitle": "Öğrenme Güçlükleri, Dilsel Beceriler ve Sosyal Uyum Yönetimi",
            "badge": "Psikososyal Gelişim",
            "coreContent": {
                "text": "Gonozomal kromozom anomalileri (47,XXY, 47,XYY, 47,XXX), otozomal trizomilerin aksine derin veya ağır zihinsel engellilik yaratmaz; hastaların büyük çoğunluğunun genel zekâ katsayısı (tam ölçekli IQ) normal veya normale yakın sınırlardadır (IQ 85-100). Ancak spesifik nörobilişsel alanlarda belirgin disfonksiyonlar görülebilir. Klinefelter sendromlu erkeklerde sözel zekâ performansı pratik/uzamsal zekâya göre daha düşüktür; çocuklukta konuşma ve telaffuz gecikmesi, okuma-yazma güçlüğü (disleksi), dikkat dağınıklığı, utangaçlık, düşük özgüven ve psikososyal çekingenlik sıktır. 47,XYY erkeklerinde ise motor koordinasyon becerilerinde gecikme, hiperaktivite, dürtüsellik ve düşük hayal kırıklığı toleransı dikkati çeker (geçmişteki hatalı 'suçlu kromozomu' miti bilimsel olarak çürütülmüştür). Erken dönemde sağlanan özel eğitim desteği, konuşma terapisi ve zamanında başlanan testosteron replasmanı bireylerin toplumsal ve akademik başarısını maksimize eder.",
                "keyBullets": [
                    {"title": "Hafif Bilişsel Etki", "desc": "Genel IQ normal sınırlardadır; derin zekâ geriliği görülmez.", "isKey": True},
                    {"title": "Sözel vs Motor Profil", "desc": "XXY'de sözel anlama ve okuma güçlüğü; XYY'de motor sakarlık ve dürtüsellik sıktır.", "isKey": True},
                    {"title": "Erken Destek", "desc": "Konuşma terapisi ve testosteron replasmanı sosyal uyum ve başarıyı artırır.", "isKey": False}
                ]
            },
            "interactiveElements": [
                make_before_after(
                    "Klinefelter vs XYY Bilişsel ve Davranışsal Profili",
                    "Klinefelter Sendromu (47,XXY) Profili",
                    "Sözel IQ düşük; disleksi, okuma güçlüğü, utangaç ve içe dönük mizaç, düşük benlik saygısı.",
                    "47,XYY Sendromu Profili",
                    "Motor koordinasyon zayıf (sakarlık), hiperaktivite, dürtü kontrol güçlüğü, normal agresyon seviyesi."
                ),
                make_cloze(
                    "Klinefelter sendromlu çocukların bilişsel profilinde pratik zekâya kıyasla sözel zekâ ve dil becerileri daha belirgin derecede etkilenir.",
                    "sözel",
                    "Dil ve kelime odaklı zekâ alanını anımsayınız"
                ),
                make_active_recall(
                    "1960'lı yıllarda ortaya atılan ve 47,XYY karyotipinin bireyleri doğuştan saldırgan ve suç işlemeye yatkın kıldığı yönündeki hatalı iddiaya tıp tarihinde ne ad verilmiştir?",
                    "'Süper erkek' veya 'suçlu kromozomu' (criminal chromosome) miti adı verilmiştir; bilimsel olarak tamamen çürütülmüştür.",
                    "Çürütülen kriminal genetik miti"
                )
            ],
            "spotPearls": [
                "Gonozomal polizomilerde genel IQ genellikle normal veya hafif düşüktür.",
                "Klinefelter'da sözel anlama güçlüğü ve disleksi sıktır; adölesanda testosteron replasmanı çok faydalıdır.",
                "47,XYY'nin suçlulukla doğrudan genetik ilişkisi yoktur; temel sorun hafif motor sakarlık ve dikkat eksikliğidir."
            ]
        }
    ]
