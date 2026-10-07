#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_cellular_adaptation_deck.py
Generates the deep (%500 detail) 24-slide learning deck for:
"Hücresel Adaptasyonlar: Atrofi, Hipertrofi, Hiperplazi, Metaplazi ve Otofaji"
(Tıbbi Patoloji - Prof. Dr. Hikmet Keleş)
Incorporating 24 slides, 48 3D flashcards, 5 comparison tables, and matched past exam questions.
"""

import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
META_PATH = os.path.join('src', 'data', 'learning_decks_meta.json')
QUEUE_PATH = os.path.join('src', 'data', 'learning_batch_queue.json')
QUESTIONS_PATH = os.path.join('src', 'data', 'pastQuestions.json')

def load_questions():
    if not os.path.exists(QUESTIONS_PATH):
        return []
    with open(QUESTIONS_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        return json.load(f)

ALL_QUESTIONS = load_questions()

def find_matched_questions(target_ids=None, keywords=None, max_count=2):
    matched = []
    seen_ids = set()

    # 1. Match specific target IDs first
    if target_ids:
        for tid in target_ids:
            for q in ALL_QUESTIONS:
                if q.get('id') == tid and tid not in seen_ids:
                    seen_ids.add(tid)
                    opts = []
                    for o in q.get('options', []):
                        opts.append({
                            'key': o.get('key', ''),
                            'text': o.get('text', ''),
                            'isCorrect': o.get('key') == q.get('correctAnswer')
                        })
                    matched.append({
                        'id': tid,
                        'examYear': q.get('examYear', 'Kurul 1 Çıkmış'),
                        'question': q.get('stem'),
                        'options': opts,
                        'correctAnswer': q.get('correctAnswer', 'A'),
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında hücresel adaptasyon konusuyla doğrudan ilişkilidir.'
                    })
                    break

    # 2. Match by keywords if needed
    if len(matched) < max_count and keywords:
        for q in ALL_QUESTIONS:
            text = (str(q.get('stem', '')) + ' ' + str(q.get('explanation', ''))).lower()
            if any(kw.lower() in text for kw in keywords):
                qid = q.get('id')
                if qid not in seen_ids and q.get('stem') and q.get('options'):
                    seen_ids.add(qid)
                    opts = []
                    for o in q.get('options', []):
                        opts.append({
                            'key': o.get('key', ''),
                            'text': o.get('text', ''),
                            'isCorrect': o.get('key') == q.get('correctAnswer')
                        })
                    matched.append({
                        'id': qid,
                        'examYear': q.get('examYear', 'Kurul 1 Çıkmış'),
                        'question': q.get('stem'),
                        'options': opts,
                        'correctAnswer': q.get('correctAnswer', 'A'),
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında hücresel adaptasyon konusuyla doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Hücre ve Biyolojik Homeostazın Dinamik Dengesi",
        "subtitle": "Hücre-çevre sürekli etkileşimi, dinamik denge ve dar fizyolojik sınırlar",
        "badge": "Biyolojik Çerçeve",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-pat-031"],
        "keywords": ["homeostaz", "hücre", "fizyolojik denge"],
        "lead": "Hücreler çevreleriyle sürekli dinamik bir etkileşim halindedir; değişen iç ve dış koşullara rağmen hücre büyüklüğü, sayısı ve fonksiyonunu belirli dar sınırlar içinde koruma yeteneğine homeostaz denir.",
        "spotPearls": [
            "Fizyolojik homeostaz durumunda hücre boyutu, sayısı ve metabolik fonksiyonu dar fizyolojik aralıklarda tutulur.",
            "Hücrenin karşılaştığı stres düzeyi fizyolojik sınırları aştığında hücre önce ADAPTASYON mekanizmalarını devreye sokarak yeni bir kararlı duruma ulaşır."
        ],
        "keyBullets": [
            {"title": "Sürekli Çevresel Etkileşim", "desc": "Hücreler metabolitler, hormonlar, mekanik kuvvetler ve kimyasal sinyallerle kesintisiz bir dinamik iletişim yürütür."},
            {"title": "Homeostazın Koruyucu Kalkanı", "desc": "Normal hücre içi iyonik yoğunluklar, pH, ATP seviyeleri ve protein sentez dengesi katı geri bildirim döngüleriyle korunur."},
            {"title": "Fizyolojik Kapasite Sınırları", "desc": "Her hücre tipi belirli bir çalışma aralığına sahiptir; bu aralık aşıldığında yeni bir kararlı duruma (adaptasyona) geçiş zorunlu hale gelir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-1",
                "question": "Homeostazın hücresel patolojideki tanımı nedir?",
                "answer": "Değişen iç ve dış çevresel koşullara rağmen hücrenin boyut, sayı ve fonksiyonunu belirli dar sınırlar içinde dengede tutmasıdır.",
                "hint": "Dinamik denge durumu."
            },
            {
                "id": "fc-ha-2",
                "question": "Hücre homeostatik sınırları aşan fizyolojik stresle karşılaştığında ilk olarak hangi biyolojik yanıtı verir?",
                "answer": "Hücresel adaptasyon (hücre hemen ölmez, yeni bir kararlı denge durumu kurmaya çalışır).",
                "hint": "Hemen hasar ve ölüm değil, uyum arayışı."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Hücresel Stres Spektrumu ve Temel Yanıt Paternleri",
        "subtitle": "Adaptasyon, geri dönüşümlü hasar ve hücre ölümü yol ayrımı",
        "badge": "Yanıt Spektrumu",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["adaptasyon", "geri dönüşümlü hasar", "nekroz", "hücre ölümü"],
        "lead": "Hücreler fizyolojik streslere veya patolojik zararlı etkenlere maruz kaldığında üç ana yanıt basamağından birine girer: Adaptasyon, geri dönüşümlü hasar veya hücre ölümü.",
        "spotPearls": [
            "Hafif ve orta şiddetteki uzamış stresler ADAPTASYON ile karşılanırken; ani, şiddetli veya adaptasyon kapasitesini aşan hasarlar HÜCRE HASARI VE ÖLÜMÜNE yol açar.",
            "Stres etkeni ortadan kaldırıldığında adaptif değişiklikler ve geri dönüşümlü hasar normale döner; ölüm (nekroz/apoptoz) ise GERİ DÖNÜŞÜMSÜZDÜR."
        ],
        "keyBullets": [
            {"title": "Adaptif Yanıt", "desc": "Hücre yapısını, boyutunu veya sayısını değiştirerek canlılığını ve işlevini yeni bir dengede sürdürür."},
            {"title": "Geri Dönüşümlü Hasar", "desc": "Hücre şişmesi ve yağlanma gibi morfolojik değişiklikler oluşur; etken kalkarsa hücre eski durumuna dönebilir."},
            {"title": "Geri Dönüşümsüz Hasar ve Ölüm", "desc": "Hasar eşiği aşıldığında mitokondri membranı çöker, kalsiyum içeri dolar ve hücre nekroz veya apoptoza gider."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-3",
                "question": "Hücresel stres karşısında hücrenin verebileceği 3 temel yanıt basamağı nedir?",
                "answer": "1) Hücresel adaptasyon, 2) Geri dönüşümlü hasar, 3) Geri dönüşümsüz hasar ve hücre ölümü (nekroz veya apoptoz).",
                "hint": "Hafiften ölümcüle giden basamaklar."
            },
            {
                "id": "fc-ha-4",
                "question": "Adaptasyon ile hücre hasarı arasındaki en kritik belirleyici faktör nedir?",
                "answer": "Stresin şiddeti, maruziyet süresi ve hücrenin metabolik/adaptif kapasitesidir.",
                "hint": "Doza ve süreye bağımlılık."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Hücresel Adaptasyonun Biyolojik Tanımı ve Amacı",
        "subtitle": "Yeni bir kararlı durum (steady state), reversibilite ve hayatta kalma stratejisi",
        "badge": "Adaptasyonun Amacı",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["kararlı durum", "steady state", "reversibilite", "hayatta kalma"],
        "lead": "Hücresel adaptasyon; hücrelerin sayı, boyut, fenotip, metabolik aktivite veya fonksiyon gibi özelliklerini geri dönüşümlü (reversibl) olarak değiştirerek yeni bir kararlı durum kurmasıdır.",
        "spotPearls": [
            "Adaptasyonun nihai amacı: Stres altında YENİ BİR KARARLI DURUM (new steady state) kurarak hücrenin CANLILIĞINI VE FONKSİYONUNU devam ettirmektir.",
            "Tüm adaptif yanıtlar doğası gereği GERİ DÖNÜŞÜMLÜDÜR (reversibl); uyarının ortadan kalkmasıyla hücre orijinal bazal haline döner."
        ],
        "keyBullets": [
            {"title": "Yeni Kararlı Durum (Steady State)", "desc": "Stres altındaki hücre yıkılmak yerine yeni bir fizyolojik dengeye ayarlanır."},
            {"title": "Reversibilite Prensibi", "desc": "Patolojik veya fizyolojik tetikleyici çekildiğinde doku mimarisi eski dengesine geriler."},
            {"title": "Fenotipik ve Fonksiyonel Esneklik", "desc": "Sadece boyut veya sayı değil, sentezlenen protein türleri ve gen ekspresyon profili de değişir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-5",
                "question": "Hücresel adaptasyonun patofizyolojik temel hedefi nedir?",
                "answer": "Hücrenin strese rağmen canlılığını ve temel fonksiyonunu sürdürebilmesi için yeni bir kararlı denge durumu kurmaktır.",
                "hint": "Yeni bir steady state."
            },
            {
                "id": "fc-ha-6",
                "question": "Adaptasyon yanıtlarının geri dönüşümlü (reversibl) olması ne anlama gelir?",
                "answer": "Tetikleyici stres, hormon veya iş yükü ortadan kalktığında hücre ve organın orijinal bazal boyut ve durumuna geri dönmesidir.",
                "hint": "Uyarının kalkmasıyla normale dönüş."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Fizyolojik ve Patolojik Adaptasyonun Temel Ayrımı",
        "subtitle": "Normal hormonal/iş yükü uyarıları vs aşırı/anormal streslere yanıt",
        "badge": "Sınıflama",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["fizyolojik adaptasyon", "patolojik adaptasyon", "hormonal", "stres"],
        "lead": "Adaptasyon süreçleri tetikleyici uyarının doğasına göre fizyolojik veya patolojik olarak iki ana sınıfa ayrılır.",
        "spotPearls": [
            "FİZYOLOJİK ADAPTASYON: Normal hormonlar veya endojen kimyasal mediyatörlerin uyarısına yanıt olarak gelişir (örn. gebelikte uterus ve memenin büyümesi).",
            "PATOLOJİK ADAPTASYON: Anormal veya aşırı streslere karşı hücreyi hayatta tutmak için gelişir; ancak dokunun 'normal' fizyolojik fonksiyonu bozulabilir."
        ],
        "keyBullets": [
            {"title": "Fizyolojik Tetikleyiciler", "desc": "Gebelikteki hormon dalgalanmaları veya sporcuda kas iş yükü gibi normal vücut gereksinimlerine yanıttır."},
            {"title": "Patolojik Stresler", "desc": "Sistemik hipertansiyon, aterosklerotik iskemi veya kronik asit reflüsü gibi hastalığa bağlı yüklenmelerdir."},
            {"title": "Fonksiyonel Maliyet", "desc": "Patolojik adaptasyon hücreyi ölümden korur ancak organ sertleşebilir, lümen daralabilir veya karsinogenez zemini doğabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-7",
                "question": "Fizyolojik adaptasyon ile patolojik adaptasyon arasındaki temel tetikleyici farkı nedir?",
                "answer": "Fizyolojik adaptasyon normal hormonal veya fonksiyonel uyarılara yanıtken; patolojik adaptasyon hücre hasarından kaçınmayı amaçlayan anormal streslere yanıttır.",
                "hint": "Normal hormon vs anormal stres."
            },
            {
                "id": "fc-ha-8",
                "question": "Gebelikte uterusun büyümesi hangi adaptasyon kategorisine girer?",
                "answer": "Fizyolojik adaptasyona girer (östrojen hormon uyarısına bağlı fizyolojik hipertrofi ve hiperplazi).",
                "hint": "Doğal gebelik süreci."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Başlıca Dört Hücresel Adaptasyon Tipi: Karşılaştırmalı Matris",
        "subtitle": "Hipertrofi, hiperplazi, atrofi ve metaplazinin temel biyolojik eksenleri",
        "badge": "Karşılaştırma Matrisi",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-pat-031"],
        "keywords": ["hipertrofi", "hiperplazi", "atrofi", "metaplazi"],
        "lead": "Hücrelerin stres karşısında geliştirdiği dört temel adaptasyon mekanizması; hücre boyutu, hücre sayısı ve hücre fenotipindeki değişimlere göre net sınırlarla ayrılır.",
        "spotPearls": [
            "HİPERTROFİ: Hücre boyutunda artış (bölünemeyen hücrelerde tek seçenek).",
            "HİPERPLAZİ: Hücre sayısında artış (bölünebilen hücrelerde).",
            "ATROFİ: Hücre boyutu ve sayısında azalma (metabolik küçülme).",
            "METAPLAZİ: Bir olgun hücre tipinin strese dayanıklı başka bir olgun hücre tipine dönüşmesi."
        ],
        "keyBullets": [
            {"title": "Hipertrofi ve Hiperplazi Ayrımı", "desc": "Hipertrofide hücre sayısı sabit kalıp hücre büyürken; hiperplazide DNA sentezi ile yeni hücreler çoğalır."},
            {"title": "Atrofinin Koruyucu Küçülmesi", "desc": "Kaynak yetersizliğinde hücre ölmeyip küçülerek minimal enerjiyle hayatta kalır."},
            {"title": "Metaplazinin Kalkan Rolü", "desc": "Hassas epitel yerini dayanıklı epitele bırakarak dokunun delinmesini veya erimesini önler."}
        ],
        "table": {
            "title": "Başlıca Dört Hücresel Adaptasyon Tipinin Karşılaştırma Matrisi",
            "headers": ["Adaptasyon Tipi", "Hücre Boyutu", "Hücre Sayısı", "Görüldüğü Dokular", "Temel Mekanizma", "Kanser Riski"],
            "rows": [
                ["Hipertrofi", "Artar (Büyür)", "Değişmez", "Kalıcı (kalp, iskelet kası) ve stabil", "Yapısal protein ve organel artışı", "Yok (doğrudan kanserojen değil)"],
                ["Hiperplazi", "Değişmez/Artabilir", "Artar (Çoğalır)", "Labil ve stabil (epitel, kemik iliği)", "Kök hücre ve mitoz aktivasyonu", "Patolojik tipinde zemin hazırlayabilir"],
                ["Atrofi", "Azalır (Küçülür)", "Azalabilir", "Tüm dokular (özellikle kas, beyin, endokrin)", "Ubikuitin-proteazom ve otofaji", "Yok (aksine metabolik baskılanma)"],
                ["Metaplazi", "Değişken", "Değişken (fenotip değişir)", "Epitel ve mezenkimal dokular", "Kök hücre gen reprogramlaması", "Kronikleşirse displazi/kanser riski yüksek!"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ha-9",
                "question": "Bölünme kapasitesi olmayan bir hücre kitlesinde organ büyümesi hangi adaptasyon tipi ile gerçekleşir?",
                "answer": "Yalnızca Hipertrofi ile (hücre sayısı artamaz, hücre boyutu büyür).",
                "hint": "Kalp kası ve çizgili kas örneği."
            },
            {
                "id": "fc-ha-10",
                "question": "Hangi adaptasyon tipinde hücrenin olgun fenotipi başka bir olgun fenotip ile yer değiştirir?",
                "answer": "Metaplazi.",
                "hint": "Epitel dönüşümü."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Hipertrofi: Tanım ve Hücresel/Organel Mekanizmaları",
        "subtitle": "Yapısal proteinler, aktin-miyozin miyofilamentleri ve organel çoğalması",
        "badge": "Hipertrofi",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["hipertrofi", "protein sentezi", "organel", "miyofilament"],
        "lead": "Hipertrofi; hücre sayısında bir artış olmaksızın, hücre içi yapısal bileşenlerin sentezlenmesi sonucu hücre boyutunun artması ve buna bağlı olarak organın büyümesidir.",
        "spotPearls": [
            "Saf hipertrofi: Hücre bölünmesi YOKTUR; artan iş yükünü karşılamak üzere hücre başına protein, organel ve miyofilament kütlesi artar.",
            "Hipertrofide hücre şişmesi (ödem) yoktur; büyüme SIVI DEĞİL, BİYOSENTEZLENMİŞ YAPI SAL PROTEİNLERİN artışına bağlıdır."
        ],
        "keyBullets": [
            {"title": "Yapısal Protein Sentezi", "desc": "Ribozom aktivitesi ve mRNA transkripsiyonu artırılarak aktin, miyozin ve sitoiskelet proteinleri hızla üretilir."},
            {"title": "Organel Büyümesi", "desc": "Mitokondri sayısı ve endoplazmik retikulum genişliği hücrenin artan metabolik yükünü karşılamak üzere çoğalır."},
            {"title": "Saf Hipertrofi Kuralı", "desc": "Mitoz yeteneği bulunmayan miyositler ve nöronlar gibi kalıcı hücrelerde organ büyümesinin tek fizyolojik yoludur."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-11",
                "question": "Hipertrofide organ büyümesini sağlayan hücresel içerik artışı nedir?",
                "answer": "Hücre içi yapısal proteinlerin (miyofilamentler, aktin-miyozin) ve organellerin (mitokondri, ER) sentezindeki artıştır.",
                "hint": "Sıvı değil, gerçek yapısal protein."
            },
            {
                "id": "fc-ha-12",
                "question": "Saf hipertrofinin görüldüğü hücrelerin temel biyolojik kısıtlılığı nedir?",
                "answer": "DNA sentezleyip mitotik bölünme gerçekleştirememeleridir (kalıcı/permanent hücreler olmaları).",
                "hint": "Bölünme yeteneği kaybı."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Fizyolojik Hipertrofi: Gebelik Uterusu ve İskelet Kası",
        "subtitle": "Östrojen uyarılı myometrium ve ağırlık çalışan sporcunun çizgili kası",
        "badge": "Fizyolojik Hipertrofi",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["gebelik uterusu", "östrojen", "iskelet kası", "fizyolojik hipertrofi"],
        "lead": "Fizyolojik hipertrofinin en çarpıcı iki örneği; gebelikte hormonal etkiyle büyüyen uterus ve ağır antrenmanla genişleyen iskelet kas lifleridir.",
        "spotPearls": [
            "Gebelikte uterus büyümesi: Sadece hipertrofi değil, ÖSTROJEN UYARISIYLA HEM HİPERTROFİ HEM HİPERPLAZİ BİRLİKTE yürütülür.",
            "İskelet kası lifleri: Bölünme yeteneği olmadığı için ağırlık egzersizine SAF HİPERTROFİ (lif çapında büyüme) ile yanıt verir."
        ],
        "keyBullets": [
            {"title": "Gebelik Uterusu (Şekil 1.20 Analizi)", "desc": "Küçük mekik biçimli miyositler, östrojenik uyarım ile devasa, plump ve yüksek kasılma kapasiteli düz kas hücrelerine dönüşür."},
            {"title": "Doğum Sonrası İnvolüsyon", "desc": "Hormon uyarısı doğumla birlikte kesildiğinde uterus haftalar içinde proteazom ve otofaji ile küçülerek eski boyutuna geriler."},
            {"title": "İskelet Kası Lif Genişlemesi", "desc": "Mekanik yüklenme uyarısıyla kas liflerinin çapı artar, yeni sarkomerler paralel olarak dizilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-13",
                "question": "Gebelikte uterusun büyümesinde düz kas hücrelerinde hangi iki adaptasyon mekanizması birlikte rol oynar?",
                "answer": "Hem Hipertrofi (hücre boyutunda büyüme) hem de Hiperplazi (hücre sayısında artış).",
                "hint": "İkili kombinasyon."
            },
            {
                "id": "fc-ha-14",
                "question": "Ağırlık çalışan bir vücut geliştiricinin pazu kaslarındaki büyüme hangi adaptasyon türüne girer?",
                "answer": "Fizyolojik Hipertrofi (iskelet kas liflerinin saf boyut artışı).",
                "hint": "Bölünme olmaksızın lif çapı artışı."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Patolojik Hipertrofi: Miyokard Hipertrofisi ve Morfoloji",
        "subtitle": "Sistemik hipertansiyon, aort darlığı ve TTC doku boyama mekanizması",
        "badge": "Patolojik Hipertrofi",
        "badgeColor": "red",
        "target_ids": ["d3-k4-pat-005", "d3-k4-kvd-005"],
        "keywords": ["miyokard hipertrofisi", "hipertansiyon", "aort stenozu", "TTC"],
        "lead": "Patolojik hipertrofinin en sık ve en önemli klinik örneği; sistemik hipertansiyon veya aort kapak stenozuna bağlı olarak gelişen sol ventrikül hipertrofisidir.",
        "spotPearls": [
            "Normal sol ventrikül duvar kalınlığı 1 - 1.5 cm iken, miyokard hipertrofisinde 2 cm'nin üzerine çıkar ve kalp ağırlığı 500-800 gramı aşabilir.",
            "TRİFENİLTETRAZOLYUM KLORÜR (TTC): Canlı miyokard dokusunu laktat dehidrogenaz enzimi aracılığıyla MAGENTA (kırmızı-mor) renge boyar; nekrotik infarkt alanı renksiz kalır."
        ],
        "keyBullets": [
            {"title": "Hemodinamik Yüklenme", "desc": "Sürekli artmış art yük (afterload) karşısında sol ventrikül miyositleri duvar gerilimini azaltmak için kalınlaşır."},
            {"title": "Makroskopi ve Morfoloji (Şekil 1.21)", "desc": "Ventrikül lümeni daralırken miyokard duvarı konsantrik olarak belirginleşir; çekirdekler irileşir (kutu şeklinde çekirdek)."},
            {"title": "TTC Boyasının Moleküler Prensibi", "desc": "Miyokard infarktında hücre ölümüyle dehidrogenaz enzimleri hücre dışına kaçtığından TTC infarkt alanını boyayamaz."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-15",
                "question": "Miyokard hipertrofisinde sol ventrikül duvar kalınlığı tanısal olarak hangi değeri aşar?",
                "answer": "2 cm'yi aşar (normal kalınlık: 1 - 1.5 cm'dir).",
                "hint": "2 santimetre eşiği."
            },
            {
                "id": "fc-ha-16",
                "question": "Trifeniltetrazolyum klorür (TTC) boyasının canlı miyokardı magenta rengine boyamasının biyokimyasal temeli nedir?",
                "answer": "Canlı miyokarddaki aktif intraselüler dehidrogenaz enzimlerinin TTC substratını indirgeyerek renkli formazana dönüştürmesidir.",
                "hint": "Dehidrogenaz enzim aktivitesi."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Kardiyak Hipertrofinin Moleküler Sinyal Yolakları",
        "subtitle": "Mekanik gerilme sensörleri, vazoaktif peptidler ve fetal gen reaktivasyonu",
        "badge": "Moleküler Mekanizma",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["integrin", "anjiyotensin II", "endotelin-1", "GATA4", "NFAT", "ANF"],
        "lead": "Kardiyomiyosit hipertrofisi; mekanik gerilme, vazoaktif ajanlar ve büyüme faktörlerinin tetiklediği karmaşık bir hücre içi sinyal iletim kaskadı ile yönetilir.",
        "spotPearls": [
            "Tetikleyici üçlü: 1) Mekanik gerilme (integrinler), 2) GPCR agonistleri (Endotelin-1, Anjiyotensin II, α-adrenerjik), 3) Büyüme faktörleri (IGF-1, TGF-β).",
            "FETAL GEN ANAHTARLAMASI: Erişkin α-MHC yerine enerji tasarrufu sağlayan fetal β-miyozin ağır zinciri (β-MHC) üretilir ve atriyal natriüretik faktör (ANF) ventrikülden salgılanır."
        ],
        "keyBullets": [
            {"title": "Membran Mekanosensörleri", "desc": "İntegrinler ve sitoiskelet gerilimi algılayarak hücre içi kinaz kaskadlarını (MAPK, PI3K/Akt) aktive eder."},
            {"title": "Transkripsiyon Faktörleri", "desc": "GATA4, NFAT (Kalsinörin yolağı) ve MEF2 aktive olarak sarkomerik gen ekspresyonunu hızlandırır."},
            {"title": "Ekonomik İzoformlara Geçiş", "desc": "Fetal genlerin yeniden uyanması, kalbin artmış iş yüküne daha düşük ATP tüketimi ile direnmesini sağlayan koruyucu bir adaptasyondur."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-17",
                "question": "Kardiyak hipertrofide yetişkin miyozin izoformundan fetal izoforma geçişin biyolojik mantığı nedir?",
                "answer": "Erişkin alfa-MHC yerine daha yavaş kasılan fakat enerjiyi (ATP'yi) çok daha ekonomik kullanan fetal beta-MHC sentezlenmesidir.",
                "hint": "Enerji ekonomisi ve fetal reprogramlama."
            },
            {
                "id": "fc-ha-18",
                "question": "Hipertrofiye uğramış ventrikül miyositlerinin kan basıncını ve volümünü düşürmek için salgıladığı fetal peptit nedir?",
                "answer": "Atriyal Natriüretik Faktör (ANF / BNP).",
                "hint": "Tuz ve su attırıcı peptit."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Hipertrofiden Dekompansasyona ve Kalp Yetmezliğine Geçiş Sınırları",
        "subtitle": "Vasküler beslenme yetersizliği, miyofibril lizisi ve ventrikül dilatasyonu",
        "badge": "Dekompansasyon",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["dekompansasyon", "kalp yetmezliği", "iskemi", "miyofibril lizisi"],
        "lead": "Hipertrofi sonsuz bir adaptasyon değildir; kritik bir kütleye ulaşıldığında biyosentetik ve vasküler sınırlar aşılarak organ yetmezliği başlar.",
        "spotPearls": [
            "Adaptasyonun sınırları: Kas lifleri kalınlaşırken KORONER KAPİLLERLER AYNI ORANDA ÇOĞALAMAZ; miyositler rölatif iskemiye sürüklenir.",
            "DEKOMPANSASYON PATOLOJİSİ: Mitokondri ATP üretemez, miyofibriller parçalanır (lizis), kardiyomiyosit apoptozu ve interstisyel fibrozis başlar; ventrikül genişler (dilatasyon) ve kalp yetmezliği gelişir."
        ],
        "keyBullets": [
            {"title": "Kapiller / Miyosit Oransızlığı", "desc": "Kas kalınlaşır ancak oksijenin difüzyon mesafesi uzar ve mikrovasküler perfüzyon yetersiz kalır."},
            {"title": "Metabolik ve Biyosentetik Çöküş", "desc": "Mitokondriyal oksidatif kapasite devasa kas kitlesini besleyecek ATP'yi üretemez hale gelir."},
            {"title": "Konsantrikten Dilate Kardiak Çöküşe", "desc": "Miyosit kaybı ve interstisyel kollajen birikimi (fibrozis) ventrikülün esnekliğini bozar; dilatasyon ve konjestif yetmezlik kaçınılmaz olur."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-19",
                "question": "Miyokard hipertrofisinin dekompansasyona uğrayıp kalp yetmezliğine dönüşmesindeki en kritik vasküler kısıtlılık nedir?",
                "answer": "Koroner mikrovasküler kapiller ağın kas liflerindeki büyüme hızına yetişememesi ve miyositlerde rölatif iskemi gelişmesidir.",
                "hint": "Kapiller difüzyon yetersizliği."
            },
            {
                "id": "fc-ha-20",
                "question": "Dekompansasyona giren hipertrofik kalbin histopatolojik özellikleri nelerdir?",
                "answer": "Miyofibril kaybı (lizisi), kardiyomiyosit apoptozu, interstisyel fibrozis ve ventriküler dilatasyon.",
                "hint": "Kas erimesi ve bağ dokusu artışı."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Hiperplazi: Tanım, Gereksinimler ve Hücresel Temeller",
        "subtitle": "Bölünme yeteneği olan dokularda hücre sayısının artışı ve organ büyümesi",
        "badge": "Hiperplazi",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["hiperplazi", "hücre sayısı", "mitoz", "kök hücre"],
        "lead": "Hiperplazi; hücre sayısındaki artış sonucu bir organ veya dokunun boyut ve kütlesinin büyümesidir.",
        "spotPearls": [
            "TEMEL ŞART: Hiperplazinin gerçekleşebilmesi için hücrelerin DNA SENTEZİ YAPABİLME VE BÖLÜNME (mitotik) KAPASİTESİNE sahip olması şarttır.",
            "Labil (sürekli bölünen) ve stabil (uyarıyla bölünen) dokularda görülür; kalıcı hücrelerde (kalp kası, nöron) hiperplazi OLMAZ."
        ],
        "keyBullets": [
            {"title": "Hücresel Çoğalma Mekanizması", "desc": "Olgun diferansiye hücrelerin mitoza girmesi ve doku kök hücrelerinin uyarılmasıyla hücre sayısı artar."},
            {"title": "Hipertrofi ile Sık Birliktelik", "desc": "Bölünebilen dokularda hiperplazi ve hipertrofi genellikle aynı hormon veya stres uyarısına eşzamanlı yanıt verir."},
            {"title": "Gen Büyüme Faktörü Yanıtı", "desc": "Hormonlar ve büyüme faktörleri hücre siklusunda G0 evresinden G1 ve S evresine geçişi tetikler."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-21",
                "question": "Bir dokuda hiperplazi gelişebilmesinin en temel hücresel önkoşulu nedir?",
                "answer": "Dokudaki hücrelerin replikatif kapasiteye (DNA sentezi ve mitotik bölünme yeteneğine) sahip olmasıdır.",
                "hint": "Bölünebilir hücre popülasyonu."
            },
            {
                "id": "fc-ha-22",
                "question": "Neden kalp kasında hiperplazi görülmez de sadece hipertrofi görülür?",
                "answer": "Kardiyomiyositler doğumdan kısa süre sonra kalıcı (permanent) hücre evresine geçerek mitoz bölünme yeteneklerini kaybettikleri içindir.",
                "hint": "Kalıcı hücre kısıtlılığı."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Fizyolojik Hiperplazi: Hormonal ve Kompansatuar Tipler",
        "subtitle": "Puberte/gebelik memesi ve karaciğer parsiyel rezeksiyonu rejenerasyonu",
        "badge": "Fizyolojik Hiperplazi",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["hormonal hiperplazi", "kompansatuar hiperplazi", "karaciğer rejenerasyonu", "HGF"],
        "lead": "Fizyolojik hiperplazi, vücudun doğal hormonal gereksinimlerine veya doku kaybını telafi etme ihtiyacına göre iki temel sınıfta incelenir.",
        "spotPearls": [
            "1. HORMONAL HİPERPLAZİ: Puberte ve gebelikte dişi meme glandüler epitelinin çoğalması; menstrüel döngüde östrojenle endometrium proliferasyonu.",
            "2. KOMPANSATUAR HİPERPLAZİ: Parsiyel hepatektomi sonrası karaciğerin orijinal kütlesine geri dönmesi; mitotik aktivite 12 saat içinde başlar (HGF, IL-6, TNF etkisi)."
        ],
        "keyBullets": [
            {"title": "Hormonal Epitel Çoğalması", "desc": "Östrojen ve progesteron meme bezi asinüslerini ve duktuslarını laktasyona hazırlamak üzere sayıca çoğaltır."},
            {"title": "Karaciğer Rejenerasyonu (Kompansatuar)", "desc": "Karaciğerin üçte ikisi cerrahi olarak çıkarılsa dahi kalan hepatositler bölünerek dokuyu 1-2 haftada orijinal ağırlığına ulaştırır."},
            {"title": "Sitokin ve Büyüme Faktörü Dalgası", "desc": "Kupffer hücrelerinden TNF ve IL-6 salınır; ardından HGF (Hepatosit Büyüme Faktörü) ve EGF hepatositleri S fazına iter."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-23",
                "question": "Fizyolojik hiperplazinin iki temel tipi hangileridir ve birer örnek veriniz?",
                "answer": "1) Hormonal hiperplazi (gebelikte meme bezlerinin büyümesi), 2) Kompansatuar hiperplazi (parsiyel rezeksiyon sonrası karaciğer rejenerasyonu).",
                "hint": "Hormon uyarısı vs organ telafisi."
            },
            {
                "id": "fc-ha-24",
                "question": "Karaciğer rezeksiyonu sonrası kalan hepatositlerde mitotik aktivite yaklaşık ne kadar süre sonra başlar?",
                "answer": "Yaklaşık 12 saat kadar erken bir sürede başlar ve doku kütlesi tamamlanana kadar sürer.",
                "hint": "12 saatlik hızlı başlatma."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Patolojik Hiperplazi: Hormon ve Büyüme Faktörü Dengesizliği",
        "subtitle": "Endometrial hiperplazi, benign prostat hiperplazisi (BPH) ve viral siğiller",
        "badge": "Patolojik Hiperplazi",
        "badgeColor": "red",
        "target_ids": ["d3-k1-pat-071"],
        "keywords": ["patolojik hiperplazi", "endometrial hiperplazi", "BPH", "HPV", "dihidrotestosteron"],
        "lead": "Patolojik hiperplazilerin büyük çoğunluğuna; hormonların veya büyüme faktörlerinin aşırı, dengesiz ve uygunsuz salınımı neden olur.",
        "spotPearls": [
            "ENDOMETRİAL HİPERPLAZİ: Progesteron ile dengelenmemiş mutlak veya rölatif ÖSTROJEN FAZLALIĞI sonucu glandüler hücrelerin kontrolsüz çoğalmasıdır (anormal uterin kanama nedeni).",
            "BENİGN PROSTAT HİPERPLAZİSİ (BPH): Androjenlerin (özellikle DİHİDROTESTOSTERON - DHT) stromal ve glandüler hücre proliferasyonunu uyarmasıyla gelişir (Kurul 1 Soru #71)."
        ],
        "keyBullets": [
            {"title": "Endometrial Dengesizlik", "desc": "Anovulatuar sikluslarda veya östrojen üreten over tümörlerinde endometrium aşırı kalınlaşır."},
            {"title": "Prostat Stromal-Epitelyal Proliferasyonu", "desc": "5-alfa redüktaz enzimiyle üretilen DHT, prostat stromal hücrelerinde FGF ve TGF salgılatarak hiperplaziyi tetikler."},
            {"title": "Viral Hiperplazi (HPV)", "desc": "Human Papillomavirus enfeksiyonunda viral proteinler (E6 ve E7) hücre siklusu frenlerini gevşeterek deri siğillerine (verruca vulgaris) yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-25",
                "question": "Endometrial hiperplazinin patogenezindeki temel endokrin dengesizlik nedir?",
                "answer": "Progesteron tarafından karşılanmamış (dengelenmemiş) aşırı östrojen uyarısıdır.",
                "hint": "Östrojen / progesteron dengesizliği."
            },
            {
                "id": "fc-ha-26",
                "question": "Benign prostat hiperplazisinde (BPH) hücre proliferasyonunu tetikleyen en potent primer androjen metaboliti hangisidir?",
                "answer": "Dihidrotestosteron (DHT).",
                "hint": "5-alfa redüktaz ürünü."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Hiperplazi ve Kanser (Neoplazi) İlişkisi: Biyolojik Ayrım",
        "subtitle": "Kontrollü proliferasyon sınırı, reversibilite ve karsinogenez için verimli toprak",
        "badge": "Kanser İlişkisi",
        "badgeColor": "rose",
        "target_ids": ["d3-k1-pat-057"],
        "keywords": ["neoplazi", "karsinogenez", "endometrial karsinom", "fertile soil"],
        "lead": "Patolojik hiperplazi kanser değildir; ancak büyüme kontrol mekanizmalarını kalıcı olarak kaybeden karsinogenez süreci için 'verimli bir toprak' oluşturur.",
        "spotPearls": [
            "KRİTİK AYRIM: Patolojik hiperplazide büyüme sinyali (hormon/uyaran) ortadan kalktığında hiperplazi DURUR VE GERİLER; kanserde ise büyüme OTONOMDUR ve durmaz.",
            "VERİMLİ TOPRAK (FERTILE SOIL): Sürekli bölünen hücrelerde DNA replikasyon hataları ve mutasyon birikme riski katlanarak artar; atipili endometrial hiperplazi endometrial karsinom riskini belirgin artırır."
        ],
        "keyBullets": [
            {"title": "Regülasyon Mekanizmalarının Korunması", "desc": "Hiperplastik hücreler normal fizyolojik durdurma sinyallerine hala yanıt verebilir."},
            {"title": "Mutasyonel Yatkınlık", "desc": "Yüksek mitotik hız karsinojenlere ve mutasyonlara karşı dokuyu savunmasız kılar."},
            {"title": "Klinik Uyarı", "desc": "Endometrial hiperplazide hücresel atipi varlığı maligniteye gidişin en önemli histopatolojik belirtecidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-27",
                "question": "Patolojik hiperplaziyi gerçek bir kanserden (neoplaziden) ayıran en temel biyolojik özellik nedir?",
                "answer": "Hiperplazide hücrelerin normal düzenleyici kontrol mekanizmalarına yanıt vermesi ve uyaran ortadan kalktığında proliferasyonun durmasıdır.",
                "hint": "Uyarana bağımlılık vs otonomi."
            },
            {
                "id": "fc-ha-28",
                "question": "Patolojik hiperplazinin kanser gelişimi açısından klinik önemi nedir?",
                "answer": "Neoplazi için 'verimli bir zemin' (fertile soil) oluşturmasıdır; hızlı hücre bölünmesi mutasyon riskini artırır (örn. endometrial karsinom riski).",
                "hint": "Malign transformasyona zemin hazırlama."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Atrofi: Tanım ve Makroskopik/Mikroskopik Morfoloji",
        "subtitle": "Hücre kütlesi kaybı, metabolik küçülme ve senil beyin atrofisi analizi",
        "badge": "Atrofi",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["atrofi", "beyin atrofisi", "girus daralması", "sulkus genişlemesi"],
        "lead": "Atrofi; hücre boyutu ve/veya hücre sayısındaki azalmaya bağlı olarak bir organ veya dokunun boyut ve hacminin küçülmesidir.",
        "spotPearls": [
            "Atrofik hücreler ÖLÜ DEĞİLDİR; metabolik aktiviteleri ve fonksiyonları asgari düzeye indirilmiş, kısıtlı kaynaklarla canlı kalmaya adapte olmuş hücrelerdir.",
            "BEYİN ATROFİSİ (Şekil 1.22): Aterosklerotik serebrovasküler hastalık ve yaşlanmada parankim kaybı sonucu GİRUSLAR DARALIR, SULKUSLAR GENİŞLER."
        ],
        "keyBullets": [
            {"title": "Metabolik Enerji Tasarrufu", "desc": "Hücre azalan kan akımı veya besin karşısında boyutunu küçülterek bazal hayatta kalma eşiğini aşağı çeker."},
            {"title": "Makroskopi: Organ Büzüşmesi", "desc": "Atrofik böbrek, beyin veya dalakta kapsül buruşur, ağırlık düşer ve çevre yağ dokusu boşluğu doldurabilir."},
            {"title": "Geri Dönüş Eşiği", "desc": "Stres erken dönemde kalkarsa hücre eski boyutuna döner; ancak uzun ve şiddetli atrofi hücreyi apoptoz ile ölüme sürükler."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-29",
                "question": "Atrofik hücrenin biyolojik canlılık durumu nasıldır?",
                "answer": "Hücre ölü değildir; yapısal proteinlerini azaltmış, metabolizmasını minimuma indirerek kısıtlı kaynakla hayatta kalmaya adapte olmuştur.",
                "hint": "Minimal canlılık dengesi."
            },
            {
                "id": "fc-ha-30",
                "question": "Ateroskleroz ve yaşlanmaya bağlı beyin atrofisinde makroskopik olarak girus ve sulkuslarda ne görülür?",
                "answer": "Beyin maddesi kaybına bağlı olarak giruslar daralır, sulkuslar ise derinleşip genişler.",
                "hint": "Dar giruslar, geniş sulkuslar."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Atrofinin Etiyolojik Nedenleri ve Klinik Paternleri",
        "subtitle": "Kullanılmama, denervasyon, iskemi, kaşeksi ve endokrin çekilme karşılaştırması",
        "badge": "Etiyoloji Tablosu",
        "badgeColor": "violet",
        "target_ids": ["d3-k1-pat-039"],
        "keywords": ["kullanılmama atrofisi", "denervasyon atrofisi", "kaşeksi", "endokrin atrofi"],
        "lead": "Atrofi gelişimine yol açan etiyolojik faktörler; dokunun mekanik yükünden sinirsel desteğine, hormon düzeyinden mikrovasküler kan akımına kadar geniş bir yelpazeyi kapsar.",
        "spotPearls": [
            "KULLANILMAMA (Disuse) ATROFİSİ: Kırık alçısına alınan bacakta kas liflerinin hızla incelmesi (reversibldir).",
            "DENERVASYON ATROFİSİ: Alt motor nöron hasarında (polio, sinir kesisi) kas liflerinde dramatik ve hızlı kütle kaybı.",
            "ENDOKRİN ATROFİ: Menopozda östrojen kaybı ile uterus, meme ve overlerin fizyolojik involüsyonu."
        ],
        "keyBullets": [
            {"title": "Mekanik Uyarı Eksikliği", "desc": "Hareketsiz kalan iskelet kasında protein sentezi düşer, kemikte osteoklastik rezorpsiyon artar."},
            {"title": "Nörotrofik Faktör Kaybı", "desc": "Sinir lifi kesildiğinde kas lifi kasılma uyarısından ve trofik nörotransmiterlerden mahrum kalarak erir."},
            {"title": "Kronik Hipoperfüzyon", "desc": "Ateroskleroz ile daralan arterler dokuya yeterli oksijen ve besin taşıyamaz; parankim küçülür."}
        ],
        "table": {
            "title": "Atrofi Nedenleri ve Klinik Patern Karşılaştırması",
            "headers": ["Atrofi Nedeni", "Temel Mekanizma", "Tipik Klinik Örnek", "Geri Dönüşüm Potansiyeli"],
            "rows": [
                ["Kullanılmama (Disuse)", "Azalmış iş yükü ve mekanik stres", "Alçıya alınan ekstremite kasları", "Egzersizle tamamen geri dönebilir"],
                ["Denervasyon", "Trofik motor sinir uyarısının kaybı", "Poliomyelit veya sinir kesisi sonrası kas", "Sinir rejenere olmazsa zordur"],
                ["İskemi (Azalmış Kan Akımı)", "Kronik arteriyel hipoperfüzyon", "Senil aterosklerotik beyin ve böbrek atrofisi", "Hasar eşiği aşılmışsa kalıcıdır"],
                ["Yetersiz Beslenme (Kaşeksi)", "Protein-kalori eksikliği, TNF/sitokin", "Marasmus, kanser kaşeksisi kas erimesi", "Beslenme düzelirse kısmen döner"],
                ["Endokrin Uyarı Kaybı", "Hormon desteğinin çekilmesi", "Menopoz sonrası endometrium ve meme atrofisi", "Fizyolojik yaşlanma süreci"],
                ["Basınç Atrofisi", "Büyüyen kitlenin dokuyu sıkıştırması", "Tümör çevresindeki basıya uğrayan parankim", "Basınç erken kalkarsa toparlayabilir"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ha-31",
                "question": "Kırık nedeniyle 6 hafta alçıda kalan kolda gelişen kas kaybı hangi atrofi tipidir?",
                "answer": "Kullanılmama (disuse) atrofisi.",
                "hint": "İş yükü azalması."
            },
            {
                "id": "fc-ha-32",
                "question": "Menopoz sonrasında kadınlarda uterus ve meme dokusunun küçülmesi hangi mekanizmayla gerçekleşir?",
                "answer": "Endokrin atrofi (trofik östrojenik hormon uyarısının kesilmesine bağlı fizyolojik atrofi).",
                "hint": "Hormon çekilmesi."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Atrofinin Biyokimyasal Mekanizmaları: Ubikuitin-Proteazom Yolağı",
        "subtitle": "Protein sentezinin baskılanması ve 26S proteazomda artmış proteoliz",
        "badge": "Biyokimyasal Mekanizma",
        "badgeColor": "indigo",
        "target_ids": ["d3-k3-pat-017"],
        "keywords": ["ubikuitin", "proteazom", "UPS", "protein yıkımı", "mTOR"],
        "lead": "Atrofi; hücresel düzeyde protein sentezinin azalması ile protein yıkımının hızlanmasının ortak bileşkesi olarak ortaya çıkar.",
        "spotPearls": [
            "AZALMIŞ SENTEZ: Düşük metabolik hız ve besin eksikliğinde mTOR yolağı baskılanır ve ribozomlarda protein üretimi yavaşlar.",
            "UBİKUTİN-PROTEAZOM YOLAĞI: Atrofik sinyaller (açlık, sitokinler) E3 ubikuitin ligazları uyarır; hedef yapısal proteinler UBİKUTİN ile işaretlenip 26S PROTEAZOMDA parçalanır."
        ],
        "keyBullets": [
            {"title": "Sentez ve Yıkım Dengesi", "desc": "Normal hücredeki hassas protein dengesi atrofide net bir negatif protein bilançosuna kayar."},
            {"title": "Ubikuitinasyon Süreci", "desc": "E1 (aktive edici), E2 (taşıyıcı) ve E3 (ligaz) enzimleri hasarlı veya gereksiz proteinlere kovalent poliubikuitin zinciri ekler."},
            {"title": "Proteazomal Yıkım", "desc": "26S proteazom fıçı şeklindeki proteolitik kor kompleksiyle işaretlenmiş proteini yakalar ve oligopeptidlere parçalar."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-33",
                "question": "Atrofi sırasında yapısal proteinlerin hızlanmış yıkımından sorumlu temel hücresel proteolitik sistem hangisidir?",
                "answer": "Ubikuitin-Proteazom Yolağı (UPS).",
                "hint": "Hücresel çöp öğütücü kompleks."
            },
            {
                "id": "fc-ha-34",
                "question": "Ubikuitin-proteazom sisteminde hedef proteinin işaretlenmesini sağlayan küçük regülatör molekül hangisidir?",
                "answer": "Ubikuitin (hedef proteini etiketler).",
                "hint": "Yıkım damgası."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Otofaji: Hücresel Geri Dönüşüm Mekanizması ve Lizozomal Sindirim",
        "subtitle": "Otofagozom oluşumu, Atg genleri ve 'Esmer Atrofi' pigmenti Lipofuksin",
        "badge": "Otofaji",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["otofaji", "otofagozom", "lipofuksin", "esmer atrofi"],
        "lead": "Otofaji ('kendi kendini yeme'); hücrenin açlık ve stres dönemlerinde kendi organel ve sitoplazmik bileşenlerini lizozomlar içinde sindirerek enerji ve yapı taşı elde etmesidir.",
        "spotPearls": [
            "OTOFAGOZOM: Çift zarlı bir vakuol sitozol ve hasarlı organelleri çevreler; LİZOZOM ile birleşerek OTOFAGOLİZOZOM (otolizozom) haline gelir ve hidrolitik enzimlerle sindirilir.",
            "ESMER ATROFİ VE LİPOFUKSİN: Sindirilemeyen lipid peroksidasyon artıkları lizozomlarda rezidüel cisim olarak kalır; sarı-kahverengi LİPOFUKSİN (yaşlılık/yıpranma pigmenti) oluşturarak atrofik organa esmer renk verir."
        ],
        "keyBullets": [
            {"title": "Biyolojik Temizleme ve Yakıt", "desc": "Hücre dışarıdan besin alamadığında mitokondri ve ribozomlarını geri dönüştürerek hayati ATP üretimini sürdürür."},
            {"title": "Moleküler Düzenleme", "desc": "Atg (autophagy-related) genleri, Beclin-1 ve LC3 lipidasyonu otofagozom zarının kapanmasını yönetir."},
            {"title": "Rezidüel Cisimcikler", "desc": "Lizozomal sindirimden arta kalan sindirilmemiş membran lipidleri lipofuksin granüllerine dönüşür."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-35",
                "question": "Otofajide çift katlı otofagozom zarının lizozomla kaynaşması sonucu oluşan sindirim yapısına ne ad verilir?",
                "answer": "Otofagolizozom (otolizozom).",
                "hint": "Lizozom füzyon ürünü."
            },
            {
                "id": "fc-ha-36",
                "question": "Kronik atrofiye uğramış yaşlı bir kalpte görülen sarı-kahverengi esmer atrofi pigmenti hangisidir?",
                "answer": "Lipofuksin (aşınma-yıpranma / yaşlılık pigmenti).",
                "hint": "Lipid peroksidasyon kalıntısı."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Otofaji ve Hücre Ölümü Arasındaki Biyolojik Köprü",
        "subtitle": "Adaptif hayatta kalma kalkanından aşırı tüketim ve apoptoza geçiş",
        "badge": "Hayatta Kalma ve Ölüm",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["otofajik hücre ölümü", "mitofaji", "apoptoz", "nörodejenerasyon"],
        "lead": "Otofaji başlangıçta mükemmel bir hayatta kalma kalkanıdır; ancak stres etkeni çözülemez ve açlık aşırı uzarsa, kendi kendini tüketme hücreyi ölüme sürükler.",
        "spotPearls": [
            "ERKEN FAZ: Koruyucu adaptasyon; hasarlı mitokondrileri temizler (mitofaji), sitokrom c kaçağını ve apoptozu engeller.",
            "GEÇ / AŞIRI FAZ: Organeller tükenir, hücre iskeleti çöker ve hücre 'Tip II Programlı Hücre Ölümü' veya apoptoz ile ortadan kaldırılır."
        ],
        "keyBullets": [
            {"title": "İkili Biyolojik Karakter", "desc": "Otofaji kontrollü düzeyde hücreyi kurtarır; kontrolsüz ve aşırı düzeyde hücrenin intiharına yol açar."},
            {"title": "Nörodejeneratif ve Miyopatik İlişki", "desc": "Alzheimer, Parkinson ve bazı kas hastalıklarında hatalı protein birikimi ve defektif otofaji patolojinin merkezindedir."},
            {"title": "İskemik Doku Yanıtı", "desc": "Tıkanmış arter bölgesindeki sınır miyositleri veya nöronlar otofaji ile saatlerce nekroza karşı direnir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-37",
                "question": "Otofajinin erken evrede apoptozu önleyici koruyucu etkisi nasıl gerçekleşir?",
                "answer": "Hasarlı, serbest radikal üreten mitokondrileri temizleyerek (mitofaji) sitokrom c salınımını ve kaspaz aktivasyonunu bloke eder.",
                "hint": "Mitofaji koruması."
            },
            {
                "id": "fc-ha-38",
                "question": "Otofajinin aşırı ve kontrolsüz devam etmesi hücresel düzeyde hangi sonuca yol açar?",
                "answer": "Hücrenin temel yaşamsal organellerini tüketerek apoptoza veya otofajik hücre ölümüne gitmesine neden olur.",
                "hint": "Organel tükenmesi ve ölüm."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Metaplazi: Tanım, Biyolojik Anlamı ve Kök Hücre Reprogramlaması",
        "subtitle": "Strese duyarlı hücrenin dayanıklı hücreyle değişimi ve transkripsiyonel reprogramlama",
        "badge": "Metaplazi",
        "badgeColor": "blue",
        "target_ids": ["d3-k1-pat-031"],
        "keywords": ["metaplazi", "kök hücre", "reprogramlama", "diferansiyasyon"],
        "lead": "Metaplazi; bir olgun (diferansiye) hücre tipinin yerini, mevcut stres faktörlerine daha dayanıklı olan başka bir olgun hücre tipinin aldığı geri dönüşümlü bir adaptasyondur.",
        "spotPearls": [
            "KURUL ÇIKMIŞ SORU TANIMI: 'Belli bir strese duyarlı olan bir hücre tipinin yerini, olumsuz çevre koşullarına daha dayanıklı olan başka bir hücre tipinin alması' = METAPLAZİ (Dönem 3 Kurul 1 Patoloji Soru #31).",
            "KÖK HÜCRE REPROGRAMLAMASI: Var olan olgun epitel hücresi şekil değiştirmez! Doku kök hücreleri sitokinler ve büyüme faktörleri etkisiyle yeni bir diferansiyasyon yoluna programlanır."
        ],
        "keyBullets": [
            {"title": "Fenotipik Değişim İlkesi", "desc": "Hücre orijinal görevini yapamaz hale gelse de ortamdaki toksik kimyasallara veya asite karşı canlı kalır."},
            {"title": "Genetik Reprogramlama", "desc": "Transkripsiyon faktörleri doku kök hücrelerinin epigenetik kilitlerini değiştirerek farklı bir olgun hücre üretir."},
            {"title": "Reversibilite Şartı", "desc": "Kronik tahriş (sigara dumanı, asit reflüsü) kesildiğinde kök hücreler yeniden orijinal epitel tipini üretmeye başlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-39",
                "question": "Metaplazide hücresel dönüşüm doğrudan diferansiye olmuş olgun hücrenin şekil değiştirmesiyle mi gerçekleşir?",
                "answer": "HAYIR! Doku kök hücrelerinin (rezerv hücrelerinin) transkripsiyonel olarak yeniden programlanması ve farklı bir hücre hattına diferansiye olmasıyla gerçekleşir.",
                "hint": "Kök hücre reprogramlaması."
            },
            {
                "id": "fc-ha-40",
                "question": "Belli bir strese duyarlı bir hücre tipinin yerini olumsuz çevre koşullarına daha dayanıklı başka bir hücre tipinin alması hangi adaptasyon tipidir?",
                "answer": "Metaplazi (Dönem 3 Kurul 1 çıkmış patoloji sorusu).",
                "hint": "Hücre tipi değişimi."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Epitelyal Skuamöz Metaplazi: Bronş ve Serviks Örnekleri",
        "subtitle": "Sigara dumanı etkisi, solunum epitelinin kaybı ve Vitamin A eksikliği",
        "badge": "Skuamöz Metaplazi",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["skuamöz metaplazi", "sigara dumanı", "bronş epiteli", "mukosiliyer temizlik", "vitamin A"],
        "lead": "Klinikte en sık karşılaşılan epitel metaplazisi; silindirik veya kolumnar epitelin dayanıklı çok katlı yassı (skuamöz) epitele dönüştüğü skuamöz metaplazidir.",
        "spotPearls": [
            "SİGARA VE BRONŞ EPİTELİ: Trakea ve bronşlardaki normal SİLİYALI PSÖDOSTRATİFİYE KOLUMNAR epitel, sigara dumanı toksisitesine karşı ÇOK KATLI YASSI EPİTELE dönüşür.",
            "BEDEL: Çok katlı yassı epitel dumana dayanıklıdır; ANCAK MUKUS SALGISI VE MUKOSİLİYER TEMİZLEME MEKANİZMASI TAMAMEN KAYBEDİLİR (enfeksiyon riski artar)."
        ],
        "keyBullets": [
            {"title": "Bronş Epitelinin Skuamöz Dönüşümü (Şekil 1.23)", "desc": "Bazal membran üzerinde narin silyalı hücrelerin yerini kalın, tabakalı yassı epitel hücreleri alır."},
            {"title": "Endoservikal Metaplazi", "desc": "Uterin servikste kolumnar endoservikal epitel asidik vajinal florayla karşılaştığında skuamöz metaplaziye uğrar (fizyolojik transformasyon zonu)."},
            {"title": "Vitamin A Eksikliği Etkisi", "desc": "Retinoik asit epitel farklılaşmasını kontrol eder; eksikliğinde solunum yolu, mesane ve göz konjonktivasında skuamöz metaplazi gelişir."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-41",
                "question": "Sigara içen bir bireyin bronş epitelinde gelişen metaplazide orijinal epitel ve yeni oluşan metaplastik epitel tipleri nelerdir?",
                "answer": "Orijinal: Siliyalı psödostratifiye kolumnar epitel -> Metaplastik: Çok katlı yassı (skuamöz) epitel.",
                "hint": "Kolumnardan yassı epitele dönüşüm."
            },
            {
                "id": "fc-ha-42",
                "question": "Solunum yolu epitelinde skuamöz metaplazi gelişmesinin en önemli fonksiyonel dezavantajı nedir?",
                "answer": "Mukus üreten goblet hücrelerinin ve siliyaların kaybolması sonucu koruyucu mukosiliyer klirens mekanizmasının yok olmasıdır.",
                "hint": "Mukosiliyer temizlik kaybı."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Kolumnar Metaplazi: Barrett Özofagusu Patolojisi",
        "subtitle": "Kronik reflü zemininde intestinal metaplazi ve adenokarsinom riski",
        "badge": "Barrett Özofagusu",
        "badgeColor": "red",
        "target_ids": ["d3-b-114", "d3-k3-pat-024"],
        "keywords": ["barrett özofagusu", "intestinal metaplazi", "goblet hücresi", "GÖRH", "adenokarsinom"],
        "lead": "Gastroözofageal reflü hastalığında mide asidine maruz kalan alt özofagus skuamöz epitelinin asite dirençli intestinal kolumnar epitele dönüşmesine Barrett Özofagusu denir.",
        "spotPearls": [
            "BARRETT ÖZOFAGUSU HİSTOPATOLOJİSİ: Özofagusun normal ÇOK KATLI YASSI EPİTELİNİN yerini, asit ve safraya dirençli GOBLET HÜCRELERİ İÇEREN İNTESTİNAL TİP KOLUMNAR EPİTEL alır.",
            "MALİGNİTE RİSKİ: Barrett özofagusu metaplazisi zemininde ÖZOFAGUS ADENOKARSİNOMU gelişme riski 30-40 kat artmıştır (Dönem 3 Kurul çıkmış patoloji sorusu)."
        ],
        "keyBullets": [
            {"title": "Asit ve Safra İrritasyonu", "desc": "Alt özofagus sfinkter yetmezliğinde reflü olan gastrik asit yassı epitelde peptik ülsere yol açar."},
            {"title": "Goblet Hücreli İntestinal Epitel", "desc": "Kök hücreler gastrik asitten korunmak için bikarbonat ve musin salgılayan intestinal kolumnar hücreler üretir."},
            {"title": "Displazi Takibi", "desc": "Barrett saptanan hastalara düzenli endoskopik biyopsiler yapılarak düşük/yüksek dereceli displazi taraması yapılır."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-43",
                "question": "Barrett özofagusunda mikroskop altında tanı koydurucu en karakteristik metaplastik hücre hangisidir?",
                "answer": "Goblet hücreleri (intestinal tip kolumnar metaplaziyi kanıtlar).",
                "hint": "Mukus vakuollü intestinal hücre."
            },
            {
                "id": "fc-ha-44",
                "question": "Barrett özofagusu hangi primer kanser tipi için majör bir prekürsör risk faktörüdür?",
                "answer": "Özofagus Adenokarsinomu (30-40 kat artmış risk taşır).",
                "hint": "Skuamöz değil, adenokarsinom."
            }
        ]
    },
    {
        "slideNumber": 23,
        "title": "Mezenkimal Metaplazi ve Metaplazinin 'İki Uçlu Kılıç' Karakteri",
        "subtitle": "Myositis ossificans, bağ dokusu metaplazisi ve displazi-karsinogenez basamakları",
        "badge": "Mezenkimal & Risk",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["myositis ossificans", "mezenkimal metaplazi", "displazi", "iki uçlu kılıç"],
        "lead": "Metaplazi yalnızca epitelde değil mezenkimal dokularda da görülebilir; hücreyi akut hasardan korurken kronikleştiğinde displazi ve karsinoma zemin hazırlar.",
        "spotPearls": [
            "MYOSİTİS OSSİFİKANS: Travma veya kas içi hematom sonrasında yumuşak doku veya çizgili kas içinde KEMİK VE KIKIRDAK DOKUSU oluşması mezenkimal metaplazinin en klasik örneğidir.",
            "İKİ UÇLU KILIÇ (DOUBLE-EDGED SWORD): Bir yandan hücreyi strese dayanıklı kılar, diğer yandan koruyucu fonksiyonları yıkar ve kanserojen mutasyonlara açık premalign bir zemin oluşturur."
        ],
        "keyBullets": [
            {"title": "Kemikleşme Reaksiyonu", "desc": "İntramusküler kanama odağındaki mezenkimal kök hücreler osteoblastlara farklılaşarak kalsifiye kemik lamelleri üretir."},
            {"title": "Karsinogenez Basamakları", "desc": "Normal Doku -> Metaplazi -> Düşük Dereceli Displazi -> Yüksek Dereceli Displazi -> İnvaziv Karsinom zinciri işler."},
            {"title": "Geri Dönüş Eşiği", "desc": "Metaplazi henüz neoplazi değildir; uyarının (sigara, reflü) kesilmesiyle metaplazi tamamen gerileyebilir."}
        ],
        "table": {
            "title": "Metaplazi Örnekleri, Dokusal Dönüşüm ve Malignite İlişkisi",
            "headers": ["Metaplazi Türü", "Orijinal Doku", "Metaplastik Doku", "Tetikleyici Neden", "Olası Malignite"],
            "rows": [
                ["Skuamöz Metaplazi", "Bronş silyalı kolumnar epitel", "Çok katlı yassı epitel", "Sigara dumanı katranı", "Skuamöz hücreli akciğer karsinomu"],
                ["Barrett Özofagusu", "Özofagus çok katlı yassı", "Gobletli intestinal kolumnar", "Kronik gastroözofageal reflü", "Özofagus adenokarsinomu"],
                ["Skuamöz Metaplazi", "Mesane transizyonel (ürotel)", "Çok katlı yassı epitel", "Schistosoma veya mesane taşı", "Mesane skuamöz hücreli karsinomu"],
                ["Gastrik İntestinal", "Mide glandüler epitel", "İntestinal tip kolumnar epitel", "Kronik Helicobacter pylori", "Mide intestinal tip adenokarsinomu"],
                ["Mezenkimal Metaplazi", "İskelet kası / bağ dokusu", "Matür kemik dokusu (ossöz)", "Travma / intramusküler hematom", "Malign transformasyon göstermez (benign)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ha-45",
                "question": "İskelet kası veya yumuşak doku travması sonrası kas içinde kemik dokusu oluşması hangi mezenkimal adaptasyondur?",
                "answer": "Myositis Ossificans (osseöz mezenkimal metaplazi).",
                "hint": "Kas içinde kemikleşme."
            },
            {
                "id": "fc-ha-46",
                "question": "Neden metaplazi patolojide 'iki uçlu bir kılıç' olarak tanımlanır?",
                "answer": "Çünkü mevcut zararlı uyarana karşı hücreyi dayanıklı kılar ancak dokunun özgün koruyucu fonksiyonlarını yok eder ve uzadığında displazi/kanser riski doğurur.",
                "hint": "Koruma vs malign transformasyon."
            }
        ]
    },
    {
        "slideNumber": 24,
        "title": "Adaptasyon, Reversibl Hasar ve Hücre Ölümü Spektrumu: Entegrasyon",
        "subtitle": "Kurul 1 Patoloji sınavı altın spotları, klinik sentez ve patolojik karar ağacı",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-pat-031"],
        "keywords": ["hücre hasarı", "kurul 1", "patoloji özeti", "altın spotlar"],
        "lead": "Hücrenin strese verdiği yanıt; stresin şiddeti, süresi ve hücrenin genetik/metabolik kapasitesine bağlı olarak adaptasyondan geri dönüşümsüz ölüme uzanan kesintisiz bir spektrumdur.",
        "spotPearls": [
            "DÖRT BÜYÜK ADAPTASYON: Hipertrofi (boyut ↑), Hiperplazi (sayı ↑), Atrofi (boyut/sayı ↓), Metaplazi (fenotip değişimi).",
            "KARDİYAK SPESİFİTE: Kalp kası bölünemez -> Saf Hipertrofi; Uterus gebelikte bölünür ve büyür -> Hipertrofi + Hiperplazi.",
            "PROTEOLİTİK SİSTEM: Atrofide artan protein yıkımı Ubikuitin-Proteazom Yolağı ve Otofaji ile yürütülür; rezidüel pigment Lipofuksindir."
        ],
        "keyBullets": [
            {"title": "Stres Karar Ağacı", "desc": "Fizyolojik/hafif stres -> Adaptasyon; Şiddetli/akut yük -> Hücresel şişme/yağlanma; İrreversibl eşik aşımı -> Nekroz veya Apoptoz."},
            {"title": "Geri Dönüşüm Anahtarı", "desc": "Adaptasyon ve hafif hasarda etken ortadan kalktığında doku normale döner; metaplazide sigara bırakıldığında bronş epiteli silyalı haline geri döner."},
            {"title": "Kurul 1 Klinik Vizyonu", "desc": "Hekimlikte amaç, patolojik adaptasyon evresindeki hastayı tanıyıp etkeni kaldırarak dokuyu irreversibl hücre ölümünden ve kanserden korumaktır."}
        ],
        "flashcards": [
            {
                "id": "fc-ha-47",
                "question": "Dönem 3 Kurul 1 Patoloji sınavında adaptasyon tipleri için 4 temel anahtar kelime eşleşmesi nedir?",
                "answer": "Hipertrofi = Boyut artışı; Hiperplazi = Sayı artışı; Atrofi = Küçülme/Yıkım artışı; Metaplazi = Olgun hücre tipi değişimi.",
                "hint": "Dört temel direk."
            },
            {
                "id": "fc-ha-48",
                "question": "Hücrenin adaptasyon yeteneğini aşıp irreversibl hasara ve ölüme geçişine neden olan kritik hücre içi olaylar nelerdir?",
                "answer": "Mitokondriyal geçirgenlik geçişi (ATP tükenmesi), aşırı kalsiyum akışı, membran bütünlüğünün bozulması ve lizozomal enzim salınımı.",
                "hint": "Mitokondri ve kalsiyum çöküşü."
            }
        ]
    }
]

def build_synthesis_narrative(slide_data):
    lines = []
    lines.append(f"### {slide_data['title']}")
    lines.append(f"#### {slide_data['subtitle']}")
    lines.append("")
    lines.append(f"• **Temel Patofizyolojik Çerçeve:** {slide_data['lead']}")
    lines.append("")
    
    for kb in slide_data.get('keyBullets', []):
        lines.append(f"• **{kb['title']}:** {kb['desc']}")
        lines.append("")

    lines.append("💡 **Klinik Patoloji Sentezi ve Fakülte Sınav İncileri (Prof. Dr. Hikmet Keleş):**")
    for sp in slide_data.get('spotPearls', []):
        lines.append(f"• {sp}")
    
    return "\n".join(lines)

def build_deck():
    slides = []
    total_cards = 0
    total_questions = 0

    for s_raw in SLIDES_DATA:
        narrative = build_synthesis_narrative(s_raw)
        
        # Build coreContent
        core_content = {
            "keyBullets": s_raw.get('keyBullets', [])
        }
        if "table" in s_raw:
            core_content["table"] = s_raw["table"]

        # Fetch matched questions
        target_ids = s_raw.get('target_ids', [])
        keywords = s_raw.get('keywords', [])
        matched_qs = find_matched_questions(target_ids=target_ids, keywords=keywords, max_count=2)
        total_questions += len(matched_qs)

        # AI prompt suggestions
        title_clean = s_raw['title']
        ai_prompts = [
            f"Prof. Dr. Hikmet Keleş'in ders anlatımında '{title_clean}' konusundaki en can alıcı sınav vurguları nelerdir?",
            f"Robbins Temel Patoloji 11. Baskı ilkelerine göre '{title_clean}' patofizyolojisini moleküler basamaklarıyla açıklar mısın?",
            f"Bu slayttaki patolojik adaptasyon mekanizmasının reversibilitesini ve hücre ölümüyle olan sınır çizgisini klinik örneklerle açıklar mısın?"
        ]

        flashcards = []
        for fc in s_raw.get('flashcards', []):
            q_val = fc.get('question') or fc.get('front', '')
            a_val = fc.get('answer') or fc.get('back', '')
            flashcards.append({
                "id": fc.get('id', ''),
                "category": fc.get('category', 'Akıl Kartı'),
                "front": q_val,
                "back": a_val,
                "question": q_val,
                "answer": a_val,
                "hint": fc.get('hint', '')
            })
        total_cards += len(flashcards)

        slide_obj = {
            "slideNumber": s_raw['slideNumber'],
            "title": s_raw['title'],
            "subtitle": s_raw['subtitle'],
            "badge": s_raw['badge'],
            "badgeColor": s_raw['badgeColor'],
            "synthesisNarrative": narrative,
            "flashcards": flashcards,
            "coreContent": core_content,
            "spotPearls": s_raw.get('spotPearls', []),
            "relatedQuestions": matched_qs,
            "aiPromptSuggestions": ai_prompts
        }
        slides.append(slide_obj)

    deck_obj = {
        "id": "learn-hucresel-adaptasyon-ve-hu",
        "title": "Hücresel Adaptasyonlar: Atrofi, Hipertrofi, Hiperplazi, Metaplazi ve Otofaji",
        "shortTitle": "Hücresel Adaptasyonlar Patolojisi",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "sourceFile": "4) Hücresel Adaptasyonlar.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "indigo",
        "overview": "Dönem 3 Kurul 1 Tıbbi Patoloji müfredatında yer alan Hücresel Adaptasyonlar dersinin Robbins & Kumar Basic Pathology 11. Baskı temelinde hazırlanmış, %500 derinlikte kapsamlı interaktif öğrenim sunumu. Hipertrofi, hiperplazi, atrofi, metaplazi ve otofajinin tüm hücresel, moleküler ve morfolojik basamaklarını, karşılaştırma tablolarını, 3D akıl kartlarını ve fakülte çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "Hipertrofi hücre boyutu artışı (kalıcı hücrelerde tek seçenek); Hiperplazi hücre sayısı artışı (mitotik hücrelerde).",
            "Gebelikte uterus büyümesinde HEM hipertrofi HEM hiperplazi birlikte rol oynar; iskelet kası egzersizinde SAF hipertrofi görülür.",
            "Miyokard hipertrofisinde sol ventrikül duvarı >2 cm olur; TTC boyası canlı dokudaki dehidrogenaz aktivitesiyle magentaya boyar.",
            "Kardiyak hipertrofide fetal gen reaktivasyonu (α-MHC -> β-MHC ve ANF salınımı) enerji tasarrufu sağlayan koruyucu bir adaptasyondur.",
            "Endometrial hiperplazide karşılanmamış östrojen; BPH'da dihidrotestosteron (DHT) patogenezden sorumludur.",
            "Atrofide yapısal protein yıkımı Ubikuitin-Proteazom Yolağı (UPS) ile yürütülür; lizozomal otofaji artıklarından Lipofuksin (esmer atrofi) birikir.",
            "Metaplazi kök hücrelerin transkripsiyonel olarak yeniden programlanmasıdır (var olan hücre şekil değiştirmez).",
            "Sigara içenlerde bronş silyalı kolumnar epiteli çok katlı yassı epitele dönüşür; mukosiliyer temizleme kaybolur.",
            "Kronik reflüde (Barrett özofagusu) yassı epitel goblet hücreli intestinal kolumnar epitele dönüşür; özofagus adenokarsinomu riski 30-40 kat artar.",
            "Myositis ossificans: Travma sonrası kas veya bağ dokusu içinde kemik oluşumu mezenkimal metaplazinin en klasik örneğidir."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Hücresel Adaptasyonlar...")
    deck = build_deck()
    print(f"Generated deck with {len(deck['slides'])} slides and {deck['totalFlashcardsCount']} flashcards.")

    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    found_idx = -1
    for i, d in enumerate(decks):
        if d.get('id') == deck['id']:
            found_idx = i
            break

    if found_idx >= 0:
        decks[found_idx] = deck
        print(f"Updated existing deck at index {found_idx} (ID: {deck['id']})")
    else:
        decks.append(deck)
        print(f"Appended new deck (ID: {deck['id']})")

    with open(DECKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)

    if os.path.exists(META_PATH):
        with open(META_PATH, 'r', encoding='utf-8') as f:
            meta_list = json.load(f)
        
        meta_entry = {
            "id": deck["id"],
            "title": deck["title"],
            "shortTitle": deck["shortTitle"],
            "discipline": deck["discipline"],
            "committee": deck["committee"],
            "instructor": deck["instructor"],
            "totalSlides": deck["totalSlides"],
            "matchedQuestionsCount": deck["matchedQuestionsCount"],
            "totalFlashcardsCount": deck["totalFlashcardsCount"],
            "themeColor": deck["themeColor"],
            "overview": deck["overview"]
        }

        m_idx = -1
        for i, m in enumerate(meta_list):
            if m.get('id') == deck['id']:
                m_idx = i
                break
        if m_idx >= 0:
            meta_list[m_idx] = meta_entry
        else:
            meta_list.append(meta_entry)

        with open(META_PATH, 'w', encoding='utf-8') as f:
            json.dump(meta_list, f, ensure_ascii=False, indent=2)
        print("Updated learning_decks_meta.json successfully.")

    # Update queue file
    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        for item in queue:
            if item.get('id') == deck['id']:
                item['status'] = 'completed'
                item['slidesCount'] = len(deck['slides'])
                item['detailLevel'] = '500%'
            elif item.get('id') == 'learn-intraseluler-birikimler':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Hücresel Adaptasyon marked as completed, İntraselüler Birikimler next!")

    print("Success! Cellular adaptation deck generation completed.")

if __name__ == '__main__':
    main()
