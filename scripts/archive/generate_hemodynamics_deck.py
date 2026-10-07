#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_hemodynamics_deck.py
Generates the deep (%500 detail) 22-slide learning deck for:
"Hemodinamik Bozukluklar: Ödem, Hiperemi, Konjesyon, Tromboz ve Kanama" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş)
Incorporating 22 slides, 44 3D flashcards, 5 comparison tables, and 30+ past exam questions.
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

def find_matched_questions(keywords, max_count=2):
    matched = []
    seen_ids = set()
    for q in ALL_QUESTIONS:
        if q.get('discipline') != 'Tıbbi Patoloji':
            continue
        text = (str(q.get('stem', '')) + ' ' + str(q.get('explanation', ''))).lower()
        if any(kw in text for kw in keywords):
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
                    'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında yer alan hemodinamik bozukluklar ile doğrudan ilişkilidir.'
                })
                if len(matched) >= max_count:
                    break
    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Hemodinamik Denge ve Sıvı Değişimi Temelleri",
        "subtitle": "İntravasküler kompartman, interstisyum ve mikrosirkülasyonun fizyopatolojisi",
        "badge": "Hemodinami Temelleri",
        "badgeColor": "indigo",
        "keywords": ["hemodinami", "starling", "interstisyum", "sıvı"],
        "lead": "Doku ve hücrelerin canlılığı; intravasküler yatak ile interstisyel alan arasında sürekli ve dengeli bir sıvı, besin ve metabolit alışverişine bağlıdır.",
        "spotPearls": [
            "Normal koşullarda kapiller yatağın arteriyel ucundan interstisyuma süzülen sıvı miktarı, venöz uçtan geri emilen ve lenfatiklerle drene edilen sıvıya eşittir.",
            "Bu dengenin vasküler lehte bozulması veya lenfatik drenajın durması interstisyel boşlukta sıvı birikimiyle (Ödem) sonuçlanır."
        ],
        "keyBullets": [
            {"title": "Dolaşım Kompartmanları", "desc": "Vücut suyunun 2/3'ü intraselüler, 1/3'ü ekstraselülerdir. Ekstraselüler sıvının %80'i interstisyumda, %20'si plazmadadır."},
            {"title": "Endotel Bariyeri", "desc": "Kapiller endoteli suya ve küçük solütlere karşı serbest geçirgenken, plazma proteinlerini (özellikle albümini) lümende hapseder."},
            {"title": "Kompansatuvar Lenfatik Sistem", "desc": "Günde yaklaşık 2-4 litre fazla süzüntü sıvısı lenfatiklerce toplanarak duktus torasikus yoluyla venöz dolaşıma iade edilir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-1",
                "question": "Mikrosirkülasyonda fizyolojik koşullarda hafif net sıvı kaçışı olmasına rağmen dokularda neden ödem oluşmaz?",
                "answer": "Çünkü arteriyel uçta dışarı çıkan az miktardaki fazla sıvı ve sızan az sayıda protein, lenfatik damarlar tarafından kesintisiz olarak drene edilip kana geri taşınır.",
                "hint": "Lenfatik pompa fazlalığı sürekli süpürür."
            },
            {
                "id": "fc-hemo-2",
                "question": "Plazma proteinlerinin kapiller dışına kaçmasını engelleyen en kritik hücresel bariyer nedir?",
                "answer": "Sağlam endotel hücreleri ve endotel hücreler arası sıkı bağlantılar (tight junction) ile bazal membranın negatif elektrostatik yüküdür.",
                "hint": "Endotel ve anyonik bazal membran albümini içeride tutar."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Starling Hipotezi ve Transkapiller Kuvvetler",
        "subtitle": "Hidrostatik basınç ile kolloid onkotik basıncın zıt kutuplu dengesi",
        "badge": "Starling Kuvvetleri",
        "badgeColor": "sky",
        "keywords": ["starling", "hidrostatik", "onkotik", "albümin"],
        "lead": "Kapiller membran boyunca sıvı hareketi, Starling denklemiyle tanımlanan dört temel fiziksel basınç vektörünün cebirsel toplamıyla belirlenir.",
        "spotPearls": [
            "KAPİLLER HİDROSTATİK BASINÇ (32 mmHg arteriyel, 12 mmHg venöz): Sıvıyı damar dışına, dokuya iten temel kuvvettir.",
            "PLAZMA KOLLOİD ONKOTİK BASINCI (yaklaşık 25-28 mmHg): Başlıca ALBÜMİN tarafından oluşturulur ve sıvıyı damar içinde tutan/çeken temel kuvvettir."
        ],
        "keyBullets": [
            {"title": "Arteriyel Uç Dinamiği", "desc": "Hidrostatik basınç (32 mmHg) onkotik basınçtan (25 mmHg) yüksek olduğundan net kuvvet sıvıyı filtre ederek interstisyuma çıkarır."},
            {"title": "Venöz Uç Dinamiği", "desc": "Hidrostatik basınç (12 mmHg) onkotik basıncın altına iner; net kuvvet sıvıyı dokudan tekrar kapiller lümenine çeker."},
            {"title": "İnterstisyel Onkotik Basınç", "desc": "Fizyolojik dokuda interstisyel protein konsantrasyonu çok düşüktür; ancak inflamasyonda vasküler permeabilite artınca yükselerek ödemi şiddetlendirir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-3",
                "question": "Starling kuvvetlerine göre plazma onkotik basıncını oluşturan en önemli plazma proteini hangisidir ve neden?",
                "answer": "ALBÜMİN! Hem plazmadaki en bol protein olması (plazma proteinlerinin %60'ı) hem de küçük molekül ağırlığı sayesinde ozmotik partikül sayısının en yüksek olması nedeniyle onkotik basıncın %70-80'ini tek başına üretir.",
                "hint": "En küçük ama en kalabalık plazma proteini."
            },
            {
                "id": "fc-hemo-4",
                "question": "Starling dengesine göre ödem oluşturan iki temel zıt basınç bozukluğu nedir?",
                "answer": "1) Kapiller Hidrostatik Basıncın artması (sıvıyı dışarı iter), 2) Plazma Kolloid Onkotik Basıncının düşmesi (sıvıyı içeride tutamaz).",
                "hint": "Ya dışarı iten basınç artar, ya içeride tutan emiş gücü düşer."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Hiperemi ve Konjesyon: Tanım, Mekanizma ve Farklar",
        "subtitle": "Aktif arteriyoler vazodilatasyon vs pasif venöz dönüş engeli",
        "badge": "Damarsal Süreçler",
        "badgeColor": "red",
        "keywords": ["hiperemi", "konjesyon", "aktif", "pasif", "siyanoz", "eritem"],
        "lead": "Hiperemi ve konjesyon; bir dokudaki lokal damar yatağında kan hacminin artmasını ifade eder; ancak mekanizmaları ve klinik görünümleri birbirinin tam zıddıdır.",
        "spotPearls": [
            "HİPEREMİ: AKTİF bir süreçtir; arteriyoler vazodilatasyonla dokuya giren arteryel kan artar; doku KIRMIZI VE SICAKTIR (Eritem).",
            "KONJESYON: PASİF bir süreçtir; venöz dönüşün engellenmesiyle dokuda venöz kan göllenir; doku MAVİ-KIRMIZI VE SOĞUKTUR (Siyanoz)."
        ],
        "keyBullets": [
            {"title": "Hiperemi Örnekleri", "desc": "Egzersiz yapan iskelet kasında metabolik vazodilatasyon, yemek sonrası gastrointestinal sistem veya akut inflamasyonun erken vasküler evresi."},
            {"title": "Konjesyon Örnekleri", "desc": "Sistemik olarak Sağ veya Sol Kalp Yetmezliği; lokal olarak derin ven trombozu (DVT) veya tümörün venöz basısı."},
            {"title": "Klinik Görünüm Ayrımı", "desc": "Hiperemide oksijenli kan fazlalığı parlak kırmızı eritem yapar; konjesyonda ise deoksijene hemoglobin birikimi morumsu siyanoza yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-5",
                "question": "Hiperemi ile konjesyon arasındaki 3 temel patolojik farkı belirtiniz.",
                "answer": "1) Hiperemi aktif (arteriyoler genişleme), konjesyon pasiftir (venöz çıkış engeli). 2) Hiperemide kan arteryel ve oksijenli, konjesyonda venöz ve deoksijenedir. 3) Hiperemide doku kırmızı ve sıcak (eritem), konjesyonda mavi-mor ve soğuktur (siyanoz).",
                "hint": "Biri aktif giriş artışı (sıcak-kırmızı), diğeri pasif çıkış tıkanıklığı (soğuk-mor)."
            },
            {
                "id": "fc-hemo-6",
                "question": "Bacakta gelişen derin ven trombozunda (DVT) bacak dokusunda hiperemi mi yoksa konjesyon mu gelişir?",
                "answer": "Lokal KONJESYON gelişir! Ana ven tıkandığı için kan kalbe dönemez, bacak venöz yatağında göllenir, doku siyanotikleşir ve şiddetli ödem oluşur.",
                "hint": "Ven tıkalıysa kan çıkamaz = Konjesyon."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Akut ve Kronik Pulmoner Konjesyon Patolojisi",
        "subtitle": "Sol kalp yetmezliği, alveoler mikrohemorajiler ve 'Kalp Yetmezliği Hücreleri'",
        "badge": "Akciğer Patolojisi",
        "badgeColor": "rose",
        "keywords": ["pulmoner konjesyon", "sol kalp yetmezliği", "hemosiderofaj", "kalp yetmezliği hücreleri"],
        "lead": "Sol kalp yetmezliğinde sol ventrikül kanı pompalayamaz; geriye doğru pulmoner venöz basınç artarak akciğer kılcallarında ağır konjesyona neden olur.",
        "spotPearls": [
            "Akut pulmoner konjesyonda alveoler kapillerler kanla dolup taşar; alveol boşluklarına transüda sıvısı (Pulmoner Ödem) dolar.",
            "Kronik pulmoner konjesyonda rüptüre olan kapillerlerden sızan eritrositleri yutan makrofajlar sitoplazmalarında hemosiderin biriktirir: 'KALP YETMEZLİĞİ HÜCRELERİ' (Hemosiderofajlar)."
        ],
        "keyBullets": [
            {"title": "Mekanizma: Sol Ventrikül İflası", "desc": "İskemik kalp hastalığı veya mitral kapak stenozunda sol atriyum ve pulmoner venöz basınç 25-30 mmHg üzerine çıkarak kılcalları genişletir."},
            {"title": "Akut Akciğer Konjesyonu", "desc": "Alveol septal kapillerleri aşırı geniştir; septumlarda ödem ve alveol lümenlerinde pembe proteinöz sıvı ile fokal intraalveoler kanamalar izlenir."},
            {"title": "Kronik Akciğer Konjesyonu ve Kahverengi İndürasyon", "desc": "Uzamış konjesyonda alveol duvarları kalınlaşır ve fibrotikleşir. Yoğun hemosiderin yüklü makrofajlar akciğere sert, pas rengi bir görünüm verir ('Brown Induration')."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-7",
                "question": "Kronik pulmoner konjesyonda balgamda veya akciğer biyopsisinde görülen 'Kalp Yetmezliği Hücreleri' gerçekte hangi hücrelerdir ve sitoplazmalarında ne biriktirirler?",
                "answer": "Alveoler Makrofajlardır! Alveol lümenine sızıp parçalanan eritrositleri fagositoz ederek içlerindeki demiri 'Hemosiderin' pigmenti halinde sitoplazmalarında biriktirirler.",
                "hint": "Hemosiderin yüklü alveoler makrofaj = Kalp yetmezliği hücresi."
            },
            {
                "id": "fc-hemo-8",
                "question": "Kronik sol kalp yetmezliğinde akciğerin makroskopik olarak kahverengi ve sert olmasını (Brown Induration) açıklayan iki bulgu nedir?",
                "answer": "1) Yoğun hemosiderin pigmenti birikimi (kahverengi pas rengi verir), 2) Kronik ödeme sekonder alveol septal interstitiumunda gelişen belirgin fibrozis (akciğere sertlik / indürasyon verir).",
                "hint": "Demir (pas rengi) + Fibröz bağ dokusu (sertlik)."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Akut ve Kronik Hepatik Konjesyon: 'Muskat Cevizi Karaciğer'",
        "subtitle": "Sağ kalp yetmezliği, santrilobüler konjesyonel nekroz ve periportal yağlanma",
        "badge": "Karaciğer Patolojisi",
        "badgeColor": "amber",
        "keywords": ["nutmeg", "muskat cevizi", "sağ kalp yetmezliği", "santrilobüler", "karaciğer"],
        "lead": "Sağ kalp yetmezliğinde vena kava inferior ve hepatik venlerdeki basınç artışı karaciğer parankiminde karakteristik bir pasif venöz göllenme tablosu yaratır.",
        "spotPearls": [
            "Karaciğerin kronik pasif konjesyonundaki klasik makroskopik görünümü 'MUSKAT CEVİZİ KARACİĞER'dir (Nutmeg Liver).",
            "Bu alacalı görüntünün nedeni: Santral ven çevresindeki HİPOKSİK KOAGÜLATİF NEKROZ (koyu kırmızı) ile periferik periportal hepatositlerdeki YAĞLANMANIN (açıksarı) kontrast oluşturmasıdır."
        ],
        "keyBullets": [
            {"title": "Akut Hepatik Konjesyon", "desc": "Santral ven ve sinüzoidler kanla aşırı genişler; santral hepatositler bası atrofisine uğrar. Karaciğer makroskopik olarak mor-kırmızı ve büyüktür."},
            {"title": "Kronik Hepatik Konjesyon ve Nekroz", "desc": "Santrilobüler bölge (Zon 3) terminal dolaşımda olduğundan oksijenden en fakir alandır; uzamış venöz stazda hipoksiye dayanamayarak nekroze olur."},
            {"title": "Kardiyak Siroz (Kardiyak Skleroz)", "desc": "Ağır ve tedavi edilmemiş sağ kalp yetmezliği santral venler çevresinde fibrozise (sentrilobüler fibrozis) ve nihayetinde kardiyak siroza yol açabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-9",
                "question": "'Muskat Cevizi Karaciğer' (Nutmeg Liver) patolojik tablosuna en sık yol açan primer kardiyovasküler hastalık nedir?",
                "answer": "SAĞ KALP YETMEZLİĞİ (veya Konstriktif Perikardit, Budd-Chiari sendromu). Vena cava inferior ve hepatik venlerdeki basınç artışı karaciğere geri yansır.",
                "hint": "Akciğer sol kalpten, karaciğer sağ kalpten etkilenir."
            },
            {
                "id": "fc-hemo-10",
                "question": "Muskat cevizi karaciğerde nekrozun özellikle santrilobüler bölgede (Zon 3) yoğunlaşmasının anatomik nedeni nedir?",
                "answer": "Çünkü Zon 3 (santral ven çevresi) hepatik arter kan akımına en uzak, oksijen saturasyonunun en düşük olduğu alandır. İskemi ve venöz göllenmede hipoksiye en ilk ve en ağır teslim olan bölgedir.",
                "hint": "Oksijenin en son ulaştığı sınır bölgedir."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Ödem Kavramı ve Terminolojisi: Transüda vs Eksüda",
        "subtitle": "İnterstisyel sıvı artışı, protein içeriği, özgül ağırlık ve enflamatuvar ayrım",
        "badge": "Ödem Patolojisi",
        "badgeColor": "sky",
        "keywords": ["ödem", "transüda", "eksüda", "anasarka", "protein"],
        "lead": "Ödem; interstisyel doku boşluklarında veya vücut seröz boşluklarında (plevra, periton, perikard) anormal sıvı birikimidir.",
        "spotPearls": [
            "TRANSÜDA: Endotel bariyeri sağlamdır; hidrostatik basınç artışı veya onkotik basınç düşüşüyle oluşur; PROTEİNDEN FAKİRDİR (<3 g/dL, dansite <1.012).",
            "EKSÜDA: Endotel geçirgenliği bozulmuştur (İNFLAMASYON); lökosit ve plazma proteinleri dışarı kaçar; PROTEİNDEN ZENGİNDİR (>3 g/dL, dansite >1.020)."
        ],
        "keyBullets": [
            {"title": "Anasarka Tanımı", "desc": "Tüm vücutta yaygın, derin, masif subkutan ödem ile birlikte seröz boşluklarda (asit, plevral efüzyon) yaygın sıvı toplanması tablosudur."},
            {"title": "Seröz Boşluk Efüzyonları", "desc": "Hidrotoraks (plevral efüzyon), Hidroperikardiyum ve Hidroperiton (Asit) olarak adlandırılır."},
            {"title": "Klinik Ayrım Önemi", "desc": "Plevral ponksiyonda sıvının transüda çıkması kalp/karaciğer/böbrek yetmezliğini; eksüda çıkması ise pnömoni veya maligniteyi düşündürür."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-11",
                "question": "Laboratuvarda bir ödem sıvısının transüda mı yoksa eksüda mı olduğunu ayırt ettiren en temel iki parametre nedir?",
                "answer": "1) Protein konsantrasyonu (Transüdada <3 g/dL, Eksüdada >3 g/dL), 2) Sıvının Dansitesi / Özgül ağırlığı (Transüdada <1.012, Eksüdada >1.020).",
                "hint": "Eksüda protein ve hücre dolu ağır sıvıdır."
            },
            {
                "id": "fc-hemo-12",
                "question": "Klinikte 'Anasarka' terimi neyi ifade eder ve en sık hangi organ yetmezliklerinde görülür?",
                "answer": "Tüm vücutta aşırı derecede yaygın cilt altı ödemi ile plevra, perikard ve batında (asit) eşzamanlı sıvı toplanması tablosudur. Ağır Nefrotik Sendrom, Dekompanse Karaciğer Sirozu ve Ağır Konjestif Kalp Yetmezliğinde görülür.",
                "hint": "Tepeden tırnağa göllenen masif jeneralize ödem."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Ödeme Yol Açan 5 Temel Patofizyolojik Mekanizma",
        "subtitle": "Starling dengesini yıkan hemodinamik ve vasküler bozukluklar matrisi",
        "badge": "Etyopatogenez",
        "badgeColor": "indigo",
        "keywords": ["ödem mekanizmaları", "hidrostatik", "onkotik", "lenfödem", "sodyum tutulumu"],
        "lead": "İnsan hastalıklarında ödem gelişimi beş ana patofizyolojik mekanizmanın biri veya birkaçının kombinasyonu sonucu ortaya çıkar.",
        "spotPearls": [
            "Ödemin 5 temel mekanizması: 1) Artmış hidrostatik basınç, 2) Azalmış plazma onkotik basıncı, 3) Lenfatik obstrüksiyon, 4) Sodyum ve su tutulumu, 5) Vasküler permeabilite artışı.",
            "Kalp yetmezliği hem hidrostatik basıncı artırarak hem de böbrek perfüzyonunu azaltıp RAAS aktivasyonuyla sodyum tutarak çifte mekanizmayla ödem yapar."
        ],
        "keyBullets": [
            {"title": "1. Artmış Hidrostatik Basınç", "desc": "Bozulmuş venöz dönüş (Kalp yetmezliği, derin ven trombozu) veya arteriyoler dilatasyon (sıcak, nörohumoral)."},
            {"title": "2. Azalmış Onkotik Basınç (Hipoalbüminemi)", "desc": "Albüminin idrarla kaybı (Nefrotik sendrom), sentezlenememesi (Siroz) veya malnütrisyon (Kwashiorkor)."},
            {"title": "3. Lenfatik Obstrüksiyon (Lenfödem)", "desc": "İnflamatuvar skar, cerrahi diseksiyon veya neoplastik invazyon nedeniyle doku sıvısının drene edilememesi."},
            {"title": "4. Sodyum ve Su Retansiyonu", "desc": "Akut glomerülonefrit veya böbrek hipoperfüzyonunda Renin-Anjiyotensin-Aldosteron artışı."},
            {"title": "5. İnflamatuvar Permeabilite Artışı", "desc": "Histamin, bradikinin ve lökotrienlerin postkapiller venüllerde endotel aralıklarını açması."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-13",
                "question": "Kalp yetmezliğinde ödem oluşumuna katkıda bulunan iki temel mekanizma nedir?",
                "answer": "1) Venöz kanın göllenmesiyle kapiller hidrostatik basıncın doğrudan artması. 2) Düşen kalp debisine yanıt olarak böbreklerin RAAS sistemini aktive edip sekonder sodyum ve su tutulumu yapması.",
                "hint": "Biri fiziksel basınç artışı, diğeri hormonal böbrek yanıtı."
            },
            {
                "id": "fc-hemo-14",
                "question": "İnflamatuvar ödem ile hemodinamik ödem arasındaki temel patolojik fark nedir?",
                "answer": "İnflamatuvar ödem endotel geçirgenliğinin bozulması sonucu gelişen EKSÜDADIR (protein zengin). Hemodinamik ödem ise endotel sağlamken basınç dengesizliğiyle gelişen TRANSÜDADIR (protein fakir).",
                "hint": "Biri damar delinmesi (eksüda), diğeri fiziksel basınç kayması (transüda)."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Azalmış Plazma Onkotik Basıncı ve Hipoalbüminemi",
        "subtitle": "Nefrotik sendrom, karaciğer sirozu ve protein malnütrisyonu (Kwashiorkor)",
        "badge": "Onkotik Çöküş",
        "badgeColor": "sky",
        "keywords": ["hipoalbüminemi", "nefrotik", "siroz", "kwashiorkor", "onkotik"],
        "lead": "Plazma albümin seviyesi kritik eşik olan 2.5-3.0 g/dL'nin altına indiğinde sıvıyı damarda tutacak emme kuvveti kaybolur ve jeneralize ödem gelişir.",
        "spotPearls": [
            "Plazma albümin kaybının en dramatik prototipi NEFROTİK SENDROMDUR; glomerül bazal membranının delinmesiyle günde >3.5 gram masif proteinüri görülür.",
            "Hipoalbüminemi sonucu damar içi hacim azalır; böbrekler bunu 'hipovolemi' algılayarak Aldosteron salgılar; tutulan su da dokuya kaçarak ödemi bir kısır döngüye sokar."
        ],
        "keyBullets": [
            {"title": "Böbrek Kaynaklı Kayıp (Nefrotik Sendrom)", "desc": "Glomerüler podosit veya bazal membran hasarı masif albüminüriye yol açar. Ödem önce gevşek dokuda (göz kapakları) belirir."},
            {"title": "Karaciğer Kaynaklı Yetersiz Sentez (Siroz)", "desc": "Fonksiyonel hepatosit kütlesinin kaybı protein fabrikasını kapatır; karaciğer albümin sentezleyemez."},
            {"title": "Gastrointestinal Kayıplar ve Malnütrisyon", "desc": "Kwashiorkor'da diyette protein yoktur; Protein Kaybettiren Enteropati'de ise bağırsak mukozasından lümene albümin sızar."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-15",
                "question": "Aşağıdakilerden hangisi plazma onkotik basıncını azaltarak ödeme yol açan durumlardan biri DEĞİLDİR?",
                "answer": "Derin Ven Trombozu (DVT) veya Konjestif Kalp Yetmezliği! Bu durumlar onkotik basıncı düşürmez; kapiller HİDROSTATİK basıncı artırarak ödem yapar.",
                "hint": "DVT basıncı artırır, albümini düşürmez!"
            },
            {
                "id": "fc-hemo-16",
                "question": "Nefrotik sendromda gelişen ödemin başlangıçta en belirgin olarak Göz Kapaklarında (Periorbital) ortaya çıkmasının nedeni nedir?",
                "answer": "Göz çevresindeki cilt altı bağ dokusunun son derece gevşek ve hidrostatik direncini karşılayacak bağ dokusu liflerinden fakir olmasıdır. Düşük basınçlı ödem sıvısı en kolay bu gevşek dokuya sızar.",
                "hint": "Göz kapağı dokusu gevşektir, suyu hemen içine çeker."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Lenfatik Tıkanıklık ve Lenfödem Patolojisi",
        "subtitle": "Kanser invazyonu, cerrahi aksiller diseksiyon, radyasyon ve Filaryazis",
        "badge": "Lenfatik Drenaj",
        "badgeColor": "violet",
        "keywords": ["lenfödem", "filaryazis", "peau dorange", "aksiller diseksiyon", "meme kanseri"],
        "lead": "Lenfatik obstrüksiyon; lenfatik akımın mekanik olarak engellenmesi sonucu dokudan protein ve sıvının uzaklaştırılamamasıyla gelişen lokalize ödemdir.",
        "spotPearls": [
            "Meme kanseri cerrahisinde AKSİLLER LENF NODU DİSEKSİYONU ve radyoterapi, o taraf kolda ömür boyu kalıcı LENFÖDEM riskine yol açar.",
            "Meme kanserinde tümörün dermal lenfatikleri tıkaması sonucu deride portakal kabuğu görünümü ('PEAU D'ORANGE') gelişir."
        ],
        "keyBullets": [
            {"title": "Paraziter Filaryazis (Wuchereria bancrofti)", "desc": "Tropikal bölgelerde sivrisineklerle bulaşan nematod lenf kanallarına yerleşir; skrotum ve bacaklarda devasa ödem ('Fil Hastalığı / Elefantiyazis') yapar."},
            {"title": "İyatrojenik Lenfödem", "desc": "Onkolojik cerrahi (mastektomi, pelvik lenfadenektomi) ve radyasyonun indüklediği yoğun fibrozis lenfatik kanalları oblitere eder."},
            {"title": "Karakteristik Özellik", "desc": "Lenfödem başlangıçta gode bırakırken, zamanla biriken proteinler fibroblast proliferasyonunu uyarır; doku kalınlaşır, sertleşir ve gode bırakmaz (non-pitting)."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-17",
                "question": "Meme kanseri olan bir hastada memenin üzerinde 'Portakal Kabuğu' (Peau d'orange) görünümü gelişmesinin patolojik mekanizması nedir?",
                "answer": "Tümör hücrelerinin yüzeyel dermal lenfatik kanalları infiltre edip tıkamasıdır. Dermal ödem gelişir ancak meme cildini derine bağlayan Cooper ligamanları deriyi çektiği için portakal kabuğu çukurlukları oluşur.",
                "hint": "Tümör lenfatikleri tıkar, Cooper ligamanları deriyi çeker."
            },
            {
                "id": "fc-hemo-18",
                "question": "Tropikal bölgelerde skrotum ve bacaklarda masif şişliğe (Elefantiyazis) yol açan lenfatik parazit hangisidir?",
                "answer": "Wuchereria bancrofti (veya Brugia malayi). Lenf nodlarında ve kanallarında kalıcı granülomatöz inflamasyon ve fibrotik obstrüksiyon yapar.",
                "hint": "Fil hastalığı yapan sivrisinek paraziti."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Subkutan (Periferik) Ödem: Gode Bırakan Ödem Dinamiği",
        "subtitle": "Yerçekimi bağımlı dağılım, pitting ödem mekanizması ve gode derecelendirmesi",
        "badge": "Fizik Muayene",
        "badgeColor": "sky",
        "keywords": ["pitting", "gode", "periferik ödem", "yerçekimi", "pretibial"],
        "lead": "Subkutan dokudaki ödem dağılımı yerçekiminden doğrudan etkilenir; fizik muayenede parmak basısıyla çukurluk oluşmasıyla (gode/pitting) karakterizedir.",
        "spotPearls": [
            "Ayakta duran veya oturan hastada ödem BACAKLARDA (pretibial ve ayak bileğinde); yatağa bağımlı hastada ise SAKRUM bölgesinde göllenir (Bağımlı / Dependent Ödem).",
            "Gode Bırakan Ödem (Pitting Edema): Başparmakla kemik yüzeyine basıldığında serbest interstisyel sıvının çevre dokuya itilmesi ve bası çekilince çukur kalmasıdır."
        ],
        "keyBullets": [
            {"title": "Yerçekimi Bağımlılığı (Dependent Edema)", "desc": "Kalp yetmezliği kaynaklı hidrostatik ödem yerçekimiyle vücudun en alt noktalarına çöker. Pozisyonla yeri değişir."},
            {"title": "Gode Bırakmayan Ödem Ayrımı", "desc": "Kronik lenfödem veya miksödemde (tiroid hipotiroidizmi - glikozaminoglikan birikimi) doku sertleşmiştir, parmak basısıyla gode kalmaz."},
            {"title": "Klinik Derecelendirme (1+ ila 4+)", "desc": "Bası sonrası oluşan çukurun derinliği ve eski haline dönme süresiyle (1+ hafif çukur, 4+ derin ve >20 sn kalan çukur) derecelendirilir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-19",
                "question": "Hareketsiz yatağa bağımlı konjestif kalp yetmezliği hastasında periferik ödem öncelikle hangi anatomik bölgede aranmalıdır?",
                "answer": "Presakral / Sakral bölgede! Yerçekimi nedeniyle yatan hastada en alt seviye sakrum ve uyluk arkasıdır.",
                "hint": "Yatan hastada bacakta değil, bel/sakrumda göllenir."
            },
            {
                "id": "fc-hemo-20",
                "question": "Pitting (Gode bırakan) ödem ile Non-pitting (Gode bırakmayan) ödem arasındaki temel patolojik içerik farkı nedir?",
                "answer": "Pitting ödem serbest akıcı interstisyel sıvıdan (transüda) kaynaklanır ve parmakla yana itilebilir. Non-pitting ödem ise proteinden zengin fibrozisle organize olmuş lenfödem veya miksödemdeki mukopolisakkarid birikimidir.",
                "hint": "Biri serbest su, diğeri jelimsi matriks/fibrozis."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Akut Akciğer Ödemi (Pulmoner Ödem) Patolojisi",
        "subtitle": "Alveoler kapiller basınç çöküşü, pembe köpüklü sıvı ve hipoksi acili",
        "badge": "Kritik Klinik",
        "badgeColor": "red",
        "keywords": ["pulmoner ödem", "akciğer ödemi", "sol kalp yetmezliği", "köpüklü balgam", "ards"],
        "lead": "Pulmoner ödem; sol ventrikül yetmezliği veya akut endotel hasarı sonucu alveol boşluklarına sıvı dolmasıyla gaz değişimini engelleyen ölümcül bir klinik tablodur.",
        "spotPearls": [
            "Akut pulmoner ödemde akciğer ağırlığı normalin 2-3 katına çıkar (ıslak, ağır, batık akciğer).",
            "Bronş ve trakea kesitinde HAVA KABARCIKLARIYLA KARIŞMIŞ PEMBE KÖPÜKLÜ SIVI taşar; hasta boğulma hissi ve ortopne ile prezente olur."
        ],
        "keyBullets": [
            {"title": "Hemodinamik Pulmoner Ödem", "desc": "Sol kalp yetmezliğinde pulmoner kapiller hidrostatik basıncın 28-30 mmHg üzerine çıkmasıyla serum alveollere sızar."},
            {"title": "Mikrovasküler Hasara Bağlı Ödem (ARDS)", "desc": "Sepsis veya toksik gaz inhalasyonunda endotel ve alveol epitelinin doğrudan parçalanmasıyla gelişen eksüdatif ödemdir (Hiyalen membranlar)."},
            {"title": "Mikroskopik Görünüm", "desc": "Standart H&E boyasında alveol lümenlerini homojen pembe, granüler amorf proteinöz bir materyal doldurur; kapillerler tıkabasa eritrositle doludur."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-21",
                "question": "Akut sol kalp yetmezliği atağında hastanın ağzından pembe köpüklü sekresyon gelmesinin patolojik açıklaması nedir?",
                "answer": "Yüksek kapiller basınçla alveollere fışkıran ödem sıvısının (transüda) kapiller çatlamasıyla gelen az miktarda eritrositle karışması ve solunum havasıyla çalkalanarak köpük halini almasıdır.",
                "hint": "Hava + Ödem sıvısı + Eritrosit = Pembe köpük."
            },
            {
                "id": "fc-hemo-22",
                "question": "Kardiyojenik akciğer ödemi ile ARDS'ye bağlı akciğer ödemi arasındaki temel mikroskopik ve etyolojik fark nedir?",
                "answer": "Kardiyojenik ödem endotel sağlarken yüksek basınçla oluşan proteinden fakir TRANSÜDADIR. ARDS ise yaygın endotel ve pnömosit nekrozu sonucu gelişen, hiyalen membranlar içeren zengin EKSÜDADIR.",
                "hint": "Biri hidrostatik pompa arızası, diğeri endotel harabiyeti."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Beyin Ödemi Patolojisi: Vazojenik vs Sitotoksik Ödem",
        "subtitle": "Kafatası rijiditesi, girus silinmesi, foramen magnum ve herniasyon tehdidi",
        "badge": "Nöropatoloji",
        "badgeColor": "violet",
        "keywords": ["beyin ödemi", "vazojenik", "sitotoksik", "herniasyon", "girus"],
        "lead": "Beyin rijid kranium içinde kapalı olduğundan, ödem sonucu intrakraniyal basıncın (KİBAS) artması hayati beyin sapı fıtıklaşmalarına (herniasyon) yol açar.",
        "spotPearls": [
            "VAZOJENİK ÖDEM: Kan-Beyin Bariyerinin bozulmasıyla ekstraselüler alana sıvı sızmasıdır (Tümörler, travma, enfeksiyon).",
            "SİTOTOKSİK ÖDEM: İskemide Na+/K+ pompasının iflasıyla sıvının HÜCRE İÇİNE dolup nöron ve gliaları şişirmesidir (Hücresel ödem).",
            "Ödemli beyinde GİRUSLAR DÜZLEŞİR, SULKUSLAR DARALIR ve ventriküller basıya uğrayarak küçülür."
        ],
        "keyBullets": [
            {"title": "Vazojenik Ödem Özellikleri", "desc": "En sık görülen tiptir. Kan-beyin bariyeri endotel geçirgenliği artar; özellikle beyaz cevherde hücreler arası boşlukta sıvı toplanır."},
            {"title": "Sitotoksik Ödem Özellikleri", "desc": "Hücre zarı hasarı ve ATP çöküşü ile su hücre içine girer; gri cevher dahil tüm hücresel elemanlar şişer."},
            {"title": "Ölümcül Komplikasyon: Herniasyon", "desc": "Genişleyen beyin dokusu; falks altından (Subfalsin), tentoryum kenarından (Unkal/Transtentoryal) veya foramen magnumdan (Tonsiller Herniasyon) fıtıklaşarak solunum merkezini ezer."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-23",
                "question": "Beyin ödeminde 'Vazojenik Ödem' ile 'Sitotoksik Ödem' arasındaki en kritik lokalizasyon ve mekanizma farkı nedir?",
                "answer": "Vazojenik ödemde Kan-Beyin Bariyeri bozulur ve sıvı hücrelerin DIŞINDA (ekstraselüler / beyaz cevherde) birikir. Sitotoksik ödemde ise hücre membran pompaları iflas eder ve su hücrelerin İÇİNE (intraselüler / nöron ve glialara) dolar.",
                "hint": "Vazojenik = Hücre dışı; Sitotoksik = Hücre içi şişme."
            },
            {
                "id": "fc-hemo-24",
                "question": "Ağır beyin ödeminde serebellar tonsillerin foramen magnumdan aşağıya fıtıklaşması (Tonsiller Herniasyon) neden hızla ölüme yol açar?",
                "answer": "Çünkü foramen magnumdan fıtıklaşan tonsiller, bulbusu (medulla oblongata) sıkıştırarak buradaki hayati solunum ve kardiyovasküler düzenleme merkezlerini ezer ve arrest geliştirir.",
                "hint": "Solunum merkezi ezilir."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Kanama (Hemoraji) ve Hemorajik Diyatez Kavramı",
        "subtitle": "Vasküler bütünlük kaybı, ekstrasellüler kaçış ve pıhtılaşma defektleri",
        "badge": "Hemoraji",
        "badgeColor": "rose",
        "keywords": ["kanama", "hemoraji", "hemorajik diyatez", "trombosit"],
        "lead": "Kanama (hemoraji); damar bütünlüğünün bozulması sonucu kanın tüm hücresel ve sıvı elemanlarıyla birlikte damar dışına çıkmasıdır.",
        "spotPearls": [
            "Kanama eksternal (vücut dışına) veya internal (doku içine / vücut boşluklarına) olabilir.",
            "HEMORAJİK DİYATEZ: Önemsiz travmalarla bile spontan ve aşırı kanamaya yol açan herediter veya edinsel pıhtılaşma bozuklukları eğilimidir (Hemofili, Trombositopeni, K vitamini eksikliği)."
        ],
        "keyBullets": [
            {"title": "Damar Yırtılması Nedenleri", "desc": "Mekanik travma, ateroskleroz, anevrizma rüptürü, vaskülit veya malign tümörlerin damar duvarını eritip erode etmesi."},
            {"title": "Hematom Tanımı", "desc": "Kanın doku içinde kitle oluşturan birikimidir. Küçük bir 'çürükten' ölümcül masif retroperitoneal hematoma kadar değişebilir."},
            {"title": "Pıhtılaşma Faktör Eksiklikleri", "desc": "Hemofili A (Faktör VIII eksikliği) veya Hemofili B (Faktör IX) tipik olarak derin doku ve eklem içi kanamalarla (hemartroz) seyreder."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-25",
                "question": "Hematom ile basit kanama arasındaki morfolojik fark nedir?",
                "answer": "Hematom, doku içine sızan kanın orada yer kaplayan solid veya pıhtılaşmış bir KİTLE oluşturması durumudur.",
                "hint": "Doku içinde kitle oluşturan kan birikintisi."
            },
            {
                "id": "fc-hemo-26",
                "question": "Hemorajik diyatez tablosuna yol açan en sık 3 edinsel klinik neden nedir?",
                "answer": "1) Karaciğer yetmezliği (tüm pıhtılaşma faktörlerinin sentezi bozulur), 2) K vitamini eksikliği (Faktör II, VII, IX, X yapılamaz), 3) Trombositopeni (kemik iliği yetmezliği veya ITP).",
                "hint": "Karaciğer, K vitamini veya trombosit yetersizliği."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Küçük Yüzeyel Kanamalar: Peteşi ve Purpura Morfolojisi",
        "subtitle": "1-2 mm mikroskobik odaklar ile 3-5 mm lezyonların patolojik mekanizması",
        "badge": "Dermatopatoloji",
        "badgeColor": "red",
        "keywords": ["peteşi", "purpura", "trombositopeni", "vaskülit"],
        "lead": "Deri, mukoza ve serozal yüzeylerde izlenen küçük fokal kanamalar, boyutlarına ve etyolojik mekanizmalarına göre sınıflandırılır.",
        "spotPearls": [
            "PETEŞİ: Deri, mukoza veya serozal yüzeylerde görülen 1 - 2 mm çapındaki toplu iğne başı büyüklüğünde minik kanama odaklarıdır.",
            "Peteşinin en sık nedenleri: TROMBOSİTOPENİ (trombosit sayısının azalması), trombosit fonksiyon bozuklukları ve C vitamini eksikliğidir (Skorbüt)."
        ],
        "keyBullets": [
            {"title": "Peteşi Özellikleri (1-2 mm)", "desc": "Kapiller endotelinin mikroskobik rüptürleridir. Trombosit tıkacı yapılamadığı için kapiller geçirgenlik basınçla delinir."},
            {"title": "Purpura Özellikleri (3-5 mm)", "desc": "Peteşilerden daha büyük (3-5 mm) kanama odaklarıdır. Nedenleri: Vaskülitler, artmış vasküler frajilite (senil purpura) veya ağır travma."},
            {"title": "Basmakla Solmama Kuralı", "desc": "Peteşi ve purpura damar dışına çıkmış eritrositlerden oluştuğu için parmakla basıldığında SOLMAZ (Hiperemi ve eritemden en temel klinik farkı budur!)."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-27",
                "question": "Deri, mukoza ve serozal yüzeylerde görülen, çapı 1-2 mm olan küçük kanama odaklarına ne ad verilir ve en sık sebebi nedir?",
                "answer": "PETEŞİ! En sık sebebi Trombositopeni (trombosit sayısının düşmesi) veya trombosit fonksiyon defektleridir.",
                "hint": "1-2 mm minik nokta = Peteşi."
            },
            {
                "id": "fc-hemo-28",
                "question": "Bir deri lezyonunun eritem (hiperemi) mi yoksa peteşi/purpura (kanama) mı olduğunu anlamak için uygulanan basit klinik test nedir?",
                "answer": "Diyaskopi (cam veya parmakla lezyonun üzerine basma) testidir. Eritemde kan damar içindedir, basmakla kan uzaklaşır ve lezyon solar. Peteşi/purpurada ise kan damar dışına sızmıştır, basmakla KESİNLİKLE SOLMAZ.",
                "hint": "Basınca soluyorsa damar içi (eritem), solmuyorsa kanama (peteşi)!"
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Büyük Kanamalar: Ekimoz ve Renk Değişimi Dinamiği",
        "subtitle": "1-2 cm subkutan hematomlar ve hemoglobinin enzimatik yıkım döngüsü",
        "badge": "Hematom Dinamiği",
        "badgeColor": "amber",
        "keywords": ["ekimoz", "bilirubin", "biliverdin", "hemosiderin", "çürük"],
        "lead": "Ekimoz (çürük); 1 ila 2 cm'den büyük subkutan hematomları tanımlar ve zaman içinde büyüleyici bir biyokimyasal renk spektrumu sergiler.",
        "spotPearls": [
            "EKİMOZ: >1-2 cm çapındaki geniş deri altı kanamalarıdır.",
            "Ekimozun renk döngüsü: Kırmızı-mavi (Hemoglobin) -> Mavi-yeşil (Biliverdin) -> Sarı-kahverengi (Bilirubin) -> Altın sarısı/pas rengi (Hemosiderin)."
        ],
        "keyBullets": [
            {"title": "Başlangıç Rengi (Kırmızı-Mor)", "desc": "Damar dışına çıkan eritrositlerdeki deoksijene hemoglobin dokuya koyu kırmızı-mavi rengini verir."},
            {"title": "Makrofaj Fagositozu ve Parçalanma", "desc": "Bölgeye gelen doku makrofajları eritrositleri yutar; hem oksijenaz enzimi hemin porfirin halkasını parçalar."},
            {"title": "Bilirubin ve Hemosiderin Aşaması", "desc": "Hem proteini önce yeşil biliverdine, sonra sarı bilirubine döner. Açığa çıkan demir ise kahverengi hemosiderin olarak depolanır."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-29",
                "question": "Bir travma sonrası oluşan ekimozun (morluğun) birkaç gün sonra yeşilimsi, ardından sarımsı bir renk almasının biyokimyasal nedeni nedir?",
                "answer": "Makrofajlarca fagosite edilen eritrositlerdeki Hemoglobinin parçalanmasıdır. Hem molekülü önce yeşil renkli BİLİVERDİNE, ardından sarı renkli BİLİRUBİNE dönüştürülür.",
                "hint": "Hemoglobin -> Biliverdin (yeşil) -> Bilirubin (sarı)."
            },
            {
                "id": "fc-hemo-30",
                "question": "Ekimoz lezyonunun son iyileşme evresinde dokuda altın sarısı-kahverengi kalıcı renk bırakan demir pigmenti hangisidir?",
                "answer": "HEMOSİDERİN pigmentidir. Makrofajlar içinde ferritin agregatları halinde depolanır.",
                "hint": "Demir pigmenti hemosiderindir."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Vücut Kavitelerine Kanamalar: Seröz Boşluk İnvazyonu",
        "subtitle": "Hemotoraks, hemoperikardiyum, hemoperiton ve eklem içi kanamalar (Hemartroz)",
        "badge": "Kaviter Kanama",
        "badgeColor": "red",
        "keywords": ["hemotoraks", "hemoperikardiyum", "hemoperiton", "hemartroz", "tamponad"],
        "lead": "Kanın vücudun doğal seröz kavitelerine akması, hacim kaybının ötesinde organları mekanik basıya uğratarak ani ölümlere neden olabilir.",
        "spotPearls": [
            "HEMOPERİKARDİYUM: Perikard boşluğuna hızla 200-300 ml kan dolması kalbin diastolde genişlemesini engelleyerek KARDİYAK TAMPONAD ve ani arrest yapar.",
            "HEMARTROZ: Eklem içine kanamadır; Hemofili hastalarında tekrarlayan hemartrozlar eklem kıkırdağını yıkarak kalıcı deformiteye ve ankilöze yol açar."
        ],
        "keyBullets": [
            {"title": "Hemotoraks", "desc": "Plevra boşluğuna kan dolmasıdır. Aort anevrizması rüptürü veya kaburga kırıklarına bağlı interkostal damar yırtılmasında görülür."},
            {"title": "Hemoperikardiyum", "desc": "Miyokard enfarktüsü sonrası ventrikül serbest duvar rüptürü veya Aort Diseksiyonunun perikarda açılmasıyla gelişir."},
            {"title": "Hemoperiton", "desc": "Karın içine masif kanamadır. Dalak rüptürü (travma veya enfeksiyöz mononükleoz) veya ektopik gebelik tubal rüptürü en sık nedenleridir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-31",
                "question": "Akut miyokard enfarktüsü geçiren bir hastada 4-5. günlerde ani kardiyojenik şok ve ölüm gelişirse en olası kaviter kanama komplikasyonu nedir?",
                "answer": "Ventrikül serbest duvar rüptürüne bağlı HEMOPERİKARDİYUM ve KARDİYAK TAMPONAD. Nekroze kas yırtılır, perikard kanla dolar ve kalp diastolde dolamaz.",
                "hint": "Kalp duvarı yırtılır, perikard dolar = Tamponad."
            },
            {
                "id": "fc-hemo-32",
                "question": "Hemofili A hastalarında diz ekleminde tekrarlayan ağrılı şişlik ve hareket kısıtlılığına yol açan kaviter kanama terimi nedir?",
                "answer": "HEMARTROZ (eklem içi kanama). Zamanla eklem kıkırdağında destrüksiyon ve ankilozan artropati oluşturur.",
                "hint": "Eklem = Artroz; Kan = Hem."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Kanamanın Klinik Önemi: Hacim, Hız ve Lokalizasyon",
        "subtitle": "Kayıp oranları, hipovolemik şok, demir eksikliği ve intrakraniyal kritik alanlar",
        "badge": "Klinik Seyir",
        "badgeColor": "red",
        "keywords": ["hipovolemik şok", "lokalizasyon", "beyin sapı", "demir eksikliği"],
        "lead": "Bir kanamanın klinik sonucu üç ana parametreye bağlıdır: Kaybedilen kanın hacmi, kanamanın hızı ve kanamanın gerçekleştiği anatomik lokalizasyon.",
        "spotPearls": [
            "Toplam kan hacminin %20'sine kadar olan ani kanamalar sağlıklı erişkinde kompanse edilebilir; ANCAK >%20 HIZLI KAYIP HİPOVOLEMİK ŞOKA yol açar.",
            "Lokalizasyon hayatidir: Cilt altında 500 ml kanama önemsiz bir hematomken; BEYİN SAPINDA 1-2 ML KANAMA solunum merkezini ezerek ani ölüme neden olur."
        ],
        "keyBullets": [
            {"title": "Kanama Hızı Faktörü", "desc": "Yavaş ve sinsi kanamalarda (aylar içinde) vücut plazma hacmini kompanse eder; ancak kronik demir eksikliği anemisi gelişir."},
            {"title": "Ani Masif Kanama", "desc": "Aort anevrizması rüptürü veya gastrointestinal varis kanamasında dakikalar içinde kan basıncı düşer, organ perfüzyonu durur ve şok gelişir."},
            {"title": "Demir Dengesi ve Dışarı Kanama", "desc": "Doku içi hematomlarda demir makrofajlarca geri kazanılır; ancak GIS veya ürogenital gibi DIŞARI kanamalarda demir kaybedilir ve anemi kaçınılmazdır."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-33",
                "question": "Deri altına olan 200 ml'lik bir kanama ile beyin sapına olan 5 ml'lik bir kanamanın klinik ağırlığı neden taban tabana zıttır?",
                "answer": "Çünkü kanamanın lokalizasyonu hacminden çok daha kritiktir! Deri altı doku genişlemeye müsaittir; beyin sapı ise foramen magnum içinde rijid bir alandır ve 5 ml kanama bile hayati solunum-dolaşım merkezlerini doğrudan ezerek öldürür.",
                "hint": "Lokalizasyon hayattır: Beyinde mililitreler bile ölümcüldür."
            },
            {
                "id": "fc-hemo-34",
                "question": "Kronik gizli mide ülseri kanamasında hastada hangi tip anemi gelişir ve neden?",
                "answer": "Demir Eksikliği Anemisi (Mikrositer hipokrom anemi)! Çünkü kan vücut dışına (gastrointestinal lümene) atıldığı için eritrositlerdeki demir vücut tarafından geri emilemez ve tükenir.",
                "hint": "Dışarı kanamalarda demir kaybedilir."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Tromboz Patolojisine Giriş: Virchow Triadı",
        "subtitle": "Endotel hasarı, hemodinamik değişiklikler (staz/türbülans) ve hiperkoagülabilite",
        "badge": "Virchow Triadı",
        "badgeColor": "indigo",
        "keywords": ["virchow", "tromboz", "endotel hasarı", "staz", "hiperkoagülabilite"],
        "lead": "Tromboz; canlı bir organizmada damar veya kalp lümeni içinde uygunsuz olarak intravasküler pıhtı (trombüs) oluşması patolojisidir.",
        "spotPearls": [
            "TROMBOZ OLUŞUMUNUN 3 TEMEL DİREĞİ (VİRCHOW TRİADI): 1) Endotel hasarı, 2) Akım anormallikleri (Staz veya Türbülans), 3) Kanda Hiperkoagülabilite.",
            "Arteriyel ve kardiyak trombozda en kritik tetikleyici faktör ENDOTEL HASARIDIR (Ateroskleroz, vaskülit). Venöz trombozda ise STAZ başroldedir."
        ],
        "keyBullets": [
            {"title": "1. Endotel Hasarı", "desc": "Ateroskleroz, hipertansiyon, sigara toksinleri veya bakteriyel endotoksinler endoteli soyar; subendotelyal von Willebrand Faktör (vWF) ve kollajen açığa çıkar."},
            {"title": "2. Akım Değişiklikleri: Staz ve Türbülans", "desc": "Normalde kan aksiyel akar (hücreler ortada, plazma kenarda). Staz ve türbülans laminar akımı bozar, trombositleri endotelle temas ettirir."},
            {"title": "3. Hiperkoagülabilite (Trombofili)", "desc": "Primer (genetik: Faktör V Leiden, Protrombin 20210A) veya sekonder (kanser, oral kontraseptif, immobilizasyon) pıhtılaşma eğilimidir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-35",
                "question": "Virchow Triadı'nın 3 temel bileşeni nedir ve arteriyel trombozda hangisi en belirleyicidir?",
                "answer": "1) Endotel hasarı, 2) Kan akımında staz veya türbülans, 3) Hiperkoagülabilite. Arteriyel trombozda en belirleyici faktör ENDOTEL HASARIDIR (özellikle rüptüre olan aterom plağı).",
                "hint": "Virchow = Endotel + Akım + Pıhtılaşma."
            },
            {
                "id": "fc-hemo-36",
                "question": "Venöz yatakta (örneğin bacak derin venlerinde) trombozu tetikleyen en primer Virchow faktörü hangisidir?",
                "answer": "STAZ (Kan akımının yavaşlaması ve göllenmesi). Uzun uçak yolculukları, yatak istirahati veya kalp yetmezliği venöz staz yaratarak pıhtıyı başlatır.",
                "hint": "Arterde hasar, vende staz ön plandadır."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Trombüsün Morfolojisi: Zahn Çizgileri ve Postmortem Pıhtı Ayrımı",
        "subtitle": "Trombosit-fibrin lamelleri ile eritrosit tabakalarının laminer deseni",
        "badge": "Trombüs Morfolojisi",
        "badgeColor": "red",
        "keywords": ["zahn çizgileri", "postmortem pıhtı", "trombüs", "tavuk yağı"],
        "lead": "Canlıda akan kanda oluşan gerçek bir trombüs, ölümden sonra damarda pıhtılaşan kandan 'Zahn Çizgileri' ve damar duvarına yapışıklığı ile ayrılır.",
        "spotPearls": [
            "ZAHN ÇİZGİLERİ (Lines of Zahn): Trombosit ve fibrinden zengin açık renkli şeritler ile eritrositten zengin koyu kırmızı şeritlerin ardışık lamelleridir.",
            "Zahn çizgileri trombüsün AKAN KANDA (CANLI ORGANİZMADA) oluştuğunun mutlak kanıtıdır; ölüm sonrası oluşan pıhtılarda (postmortem clot) Zahn çizgisi bulunmaz."
        ],
        "keyBullets": [
            {"title": "Zahn Çizgilerinin Oluşumu", "desc": "Kalp boşluklarında ve aortta yüksek akım altında trombositlerin katman katman çökmesiyle mikroskobik ve makroskopik çizgilenmeler oluşur."},
            {"title": "Mural Trombüs", "desc": "Kalp odacıklarının (enfarktlı sol ventrikül) veya anevrizmatik aort lümeninin duvarına yapışık, lümeni tamamen tıkamayan trombüslerdir."},
            {"title": "Postmortem Pıhtı Ayrımı", "desc": "Ölüm sonrası pıhtı jelatinsi, yumuşak, damar duvarına YAPIŞMAYAN, üstte sarı 'tavuk yağı' (chicken fat), altta 'frenk üzümü jölesi' (currant jelly) görünümündedir."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-37",
                "question": "Otopside damar lümeninde bulunan bir kitlenin ölümden önce mi (gerçek trombüs) yoksa ölümden sonra mı (postmortem pıhtı) oluştuğu nasıl anlaşılır?",
                "answer": "Gerçek trombüs kuru, granüler, damar duvarına sıkıca yapışıktır ve 'Zahn Çizgileri' içerir. Postmortem pıhtı ise yumuşak, jelatinsi, duvara yapışmaz ve iki tabakalıdır (tavuk yağı / frenk üzümü jölesi).",
                "hint": "Zahn çizgisi ve duvara yapışma = Canlıda oluşmuş gerçek trombüs."
            },
            {
                "id": "fc-hemo-38",
                "question": "Zahn çizgilerini mikroskobik olarak oluşturan açık ve koyu renkli bantların içeriği nedir?",
                "answer": "Açık renkli bantlar: Trombositler ve fibrin ağı. Koyu renkli bantlar: Bu ağın arasına hapsolmuş yoğun eritrosit tabakaları.",
                "hint": "Açık = Trombosit/Fibrin; Koyu = Eritrosit."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Arteriyel Trombüsler vs Venöz Trombüsler (Flebotromboz)",
        "subtitle": "Beyaz pıhtı vs kırmızı pıhtı, retrograd vs antegrad büyüme",
        "badge": "Trombüs Tipleri",
        "badgeColor": "indigo",
        "keywords": ["arteriyel trombüs", "venöz trombüs", "flebotromboz", "kırmızı pıhtı", "beyaz pıhtı"],
        "lead": "Arteriyel ve venöz trombüsler; oluştukları damar yatağının hemodinamik hızına ve tetikleyici mekanizmalarına göre tamamen zıt biyolojik özellikler taşır.",
        "spotPearls": [
            "ARTERİYEL TROMBÜS: Yüksek akımlı ortamda endotel hasarıyla başlar; trombositten zengindir (BEYAZ PIHTI); pıhtı kalbe doğru geriye (RETROGRAD) uzanır.",
            "VENÖZ TROMBÜS: Yavaş akımlı stazla başlar; eritrositten zengindir (KIRMIZI PIHTI / Flebotromboz); pıhtı akım yönünde kalbe doğru (ANTEGRAD) uzanır."
        ],
        "keyBullets": [
            {"title": "Arteriyel Trombüs Lokalizasyonu", "desc": "En sık Koroner arterler, Serebral arterler ve Femoral arterlerdir. Genellikle aterom plağı üzerinde oklüziftir ve organ enfarktına yol açar."},
            {"title": "Venöz Trombüs Lokalizasyonu", "desc": "%90 bacak derin venlerinde (Popliteal, Femoral, İliak venler) görülür. Lümeni tıkar; en büyük riski kopup Akciğere emboli atmasıdır."},
            {"title": "Kuyruk ve Emboli Riski", "desc": "Her iki trombüs de kalbe doğru büyür. Venöz trombüsün akım yönünde lümende serbest sallanan 'kuyruğu' kolayca koparak tromboemboliye dönüşür."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-39",
                "question": "Arteriyel trombüsler neden 'Beyaz Pıhtı', venöz trombüsler ise 'Kırmızı Pıhtı' olarak adlandırılır?",
                "answer": "Arteriyel trombüsler hızlı akımda endotel yırtığına yapışan yoğun trombosit ve fibrinden oluşur (soluk/beyaz). Venöz trombüsler ise durgun kan gölünde oluştuğu için pıhtı ağına çok sayıda eritrosit takılır (koyu kırmızı).",
                "hint": "Arterde trombosit (beyaz), vende eritrosit gölü (kırmızı)."
            },
            {
                "id": "fc-hemo-40",
                "question": "Derin ven trombozunun (DVT) en ölümcül ve en korkulan komplikasyonu nedir?",
                "answer": "PULMONER TROMBOEMBOLİZM (PTE). Bacak veninden kopan trombüs fragmanı vena cava ve sağ kalpten geçerek pulmoner arter yatağını tıkar ve ani ölüme yol açabilir.",
                "hint": "Bacaktan kopup akciğere uçan pıhtı."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Trombüsün Akıbeti: 4 Temel Patolojik Sonlanım",
        "subtitle": "Yayılma (propagasyon), embolizasyon, erime (lizis) ve organizasyon/rekanalizasyon",
        "badge": "Trombüs Evrimi",
        "badgeColor": "amber",
        "keywords": ["organizasyon", "rekanalizasyon", "lizis", "propagasyon", "tpa"],
        "lead": "Bir trombüs oluştuktan sonra saatler ve günler içinde dört temel patolojik yoldan birine veya birkaçına ilerler.",
        "spotPearls": [
            "Trombüsün 4 akıbeti: 1) Yayılma (Propagasyon), 2) Embolizasyon, 3) Çözünme / Erime (Disolüsyon / Lizis), 4) ORGANİZASYON VE REKANALİZASYON.",
            "Organizasyon ve Rekanalizasyonda: Trombüs içine kapillerler ve fibroblastlar girer (granülasyon dokusu); pıhtı içinde yeni mikro-kanallar açılarak kan akımı kısmen restore edilir."
        ],
        "keyBullets": [
            {"title": "1. Propagasyon (Yayılma)", "desc": "Trombüs daha fazla trombosit ve fibrin toplayarak damar boyunca uzanır ve lümeni tamamen tıkar."},
            {"title": "2. Embolizasyon (Kopma)", "desc": "Trombüsün bir kısmı veya tamamı damar duvarından koparak kan akımıyla uzak bir organa taşınır."},
            {"title": "3. Disolüsyon (Erime)", "desc": "Fibrinolitik sistem (Plazmin) erken dönemde pıhtıyı eritir. Trombüs eskidiğinde fibrin çapraz bağları artar ve pıhtı lizise dirençli hale gelir (tPA erken verilmelidir!)."},
            {"title": "4. Organizasyon ve Rekanalizasyon", "desc": "Endotel ve makrofajlar pıhtıyı bağ dokusuna dönüştürür. Yeni lümenler açılarak pıhtı damar duvarında fibröz bir tepeciğe dönüşür."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-41",
                "question": "Akut iskemik inme veya miyokard enfarktüsünde fibrinolitik tedavinin (tPA) ilk birkaç saat içinde verilmesinin patolojik nedeni nedir?",
                "answer": "Çünkü yeni oluşmuş taze trombüs plazmin tarafından kolayca eritilebilir. Saatler geçtikçe trombüs içinde yoğun fibrin çapraz bağlanması ve polimerizasyon gelişir; pıhtı lizise dirençli hale gelir.",
                "hint": "Taze pıhtı erir, yaşlanan pıhtı taşlaşır."
            },
            {
                "id": "fc-hemo-42",
                "question": "Patolojide trombüsün 'Rekanalizasyonu' ne anlama gelir?",
                "answer": "Organize olan fibröz trombüs kitlesi içinde yeni kılcal damarların ve endotel döşeli lümenlerin açılması, böylece tıkanmış damardan kan akımının kısmen de olsa yeniden sağlanmasıdır.",
                "hint": "Tıkanıklığın içinden tünel açılması."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Hemodinamik Bozukluklar Büyük Entegrasyon ve Sınav Özeti",
        "subtitle": "Ödem, konjesyon, kanama ve tromboz klinik karar algoritmaları",
        "badge": "Kurul 1 Özeti",
        "badgeColor": "indigo",
        "keywords": ["hemodinami özet", "kurul 1 patoloji", "starling özet"],
        "lead": "Dönem 3 Kurul 1 Patoloji sınavlarında hemodinamik bozukluklar; Starling dengesi, konjesyon organ lezyonları, kanama boyutları ve Virchow triadı ekseninde sorgulanır.",
        "spotPearls": [
            "Starling bozukluğunda: Kalp yetmezliği = Hidrostatik artış; Nefrotik/Siroz = Onkotik düşüş; Masif ödem = Anasarka.",
            "Organ lezyonlarında: Akciğer = Hemosiderofajlar (Kalp yetmezliği hücresi); Karaciğer = Muskat cevizi (Zon 3 nekrozu).",
            "Kanama boyutlarında: 1-2 mm = Peteşi; 3-5 mm = Purpura; >1-2 cm = Ekimoz.",
            "Trombüs ayrımında: Canlı akış kanıtı = Zahn çizgileri; Ölüm sonrası pıhtı = Tavuk yağı jölesi."
        ],
        "keyBullets": [
            {"title": "Ödem Sentezi", "desc": "Transüda (protein fakir, hidrostatik/onkotik) ile Eksüda (protein zengin, inflamasyon) ayrımı tüm klinik branşlarda temel kılavuzdur."},
            {"title": "Konjesyon Sentezi", "desc": "Sol kalp yetmezliği akciğeri (kahverengi indürasyon), sağ kalp yetmezliği karaciğeri (muskat cevizi) ve periferik dokuları (pretibial gode) vurur."},
            {"title": "Tromboemboli Sentezi", "desc": "Virchow triadındaki staz DVT'ye, DVT koparak pulmoner emboliye; arteriyel aterom rüptürü ise miyokard enfarktüsüne ilerler."}
        ],
        "flashcards": [
            {
                "id": "fc-hemo-43",
                "question": "Kurul 1 Patoloji sınavı için en kritik 4 hemodinamik terimi birer cümleyle eşleştiriniz: Peteşi, Muskat Cevizi, Zahn Çizgisi, Transüda.",
                "answer": "Peteşi: 1-2 mm trombositopenik kanama. Muskat Cevizi: Sağ kalp yetmezliğinde karaciğer konjesyonu. Zahn Çizgisi: Canlıda akan kanda trombüs oluşum kanıtı. Transüda: Basınç dengesizliğiyle oluşan protein fakir ödem.",
                "hint": "4 kritik amfi spotu."
            },
            {
                "id": "fc-hemo-44",
                "question": "Sol kalp yetmezliğinde ödem önce akciğerde başlarken, Nefrotik sendromda neden önce göz kapaklarında (periorbital) başlar?",
                "answer": "Sol kalp yetmezliğinde primer bozukluk sol ventrikül basıncının doğrudan pulmoner venlere yansımasıdır (lokal hidrostatik artış). Nefrotik sendromda ise sistemik albümin kaybı vardır ve sıvı en kolay en gevşek bağ dokusu olan periorbital sahaya sızar.",
                "hint": "Biri lokal venöz basınç, diğeri sistemik albümin kaybı."
            }
        ]
    }
]

COMPARISON_TABLES = {
    2: {
        "title": "Starling Kuvvetleri ve Kapiller Sıvı Değişim Dengesi",
        "headers": ["Basınç Türü", "Arteriyel Uç Değeri", "Venöz Uç Değeri", "Etki Yönü ve Fonksiyonu"],
        "rows": [
            ["Kapiller Hidrostatik Basınç (Pc)", "32 - 35 mmHg", "12 - 15 mmHg", "Sıvıyı lümenden interstisyel dokuya İTER (Filtrasyon)"],
            ["Plazma Kolloid Onkotik Basıncı (πc)", "25 - 28 mmHg", "25 - 28 mmHg", "Sıvıyı interstisyumdan lümene ÇEKER (Albümin bağımlı)"],
            ["İnterstisyel Hidrostatik Basınç (Pi)", "-2 ila 0 mmHg", "-2 ila 0 mmHg", "Genellikle hafif negatif/sıfırdır; doku turgorunu korur"],
            ["İnterstisyel Onkotik Basınç (πi)", "1 - 3 mmHg", "1 - 3 mmHg", "Normalde düşüktür; inflamasyonda protein sızınca artar"],
            ["Net Filtrasyon Basıncı", "+8 ila +10 mmHg (Çıkış)", "-8 ila -10 mmHg (Giriş)", "Arterde süzülen sıvının %90'ı venöz uçta geri emilir; %10 lenfatikle döner"]
        ]
    },
    3: {
        "title": "Hiperemi ile Konjesyonun Temel Karşılaştırma Matrisi",
        "headers": ["Kriter", "Hiperemi (Aktif Süreç)", "Konjesyon (Pasif Süreç)"],
        "rows": [
            ["Mekanizma", "Arteriyoler dilatasyonla dokuya kan girişinde aktif artış", "Venöz drenajın engellenmesi sonucu dokuda pasif göllenme"],
            ["Kanın Niteliği", "Oksijenlenmiş zengin arteryel kan", "Deoksijene, karbondioksit yüklü venöz kan"],
            ["Doku Rengi ve Isısı", "Parlak kırmızı (Eritem) ve SICAK", "Koyu mavi-kırmızı (Siyanoz) ve SOĞUK"],
            ["Tipik Fizyolojik/Klinik Örnek", "Egzersiz kası, utanınca yüz kızarması, akut iltihap", "Sağ/Sol Kalp yetmezliği, derin ven trombozu (DVT)"],
            ["Kronikleşme Etkisi", "Genellikle geçicidir; doku hasarı bırakmaz", "Kronik hipoksi, parankim atrofisi, fibrozis ve mikroskobik kanama"]
        ]
    },
    6: {
        "title": "Transüda ile Eksüda Ödem Sıvılarının Ayırıcı Tanı Kriterleri",
        "headers": ["Özellik", "Transüda (Non-İnflamatuvar)", "Eksüda (İnflamatuvar)"],
        "rows": [
            ["Temel Neden", "Hidrostatik basınç artışı veya Onkotik basınç düşüşü", "Endotel hasarı ve vasküler permeabilite artışı (İltihap)"],
            ["Protein İçeriği", "DÜŞÜK (< 3.0 g/dL - başlıca az miktarda albümin)", "YÜKSEK (> 3.0 g/dL - fibrinojen ve globulinler dahil)"],
            ["Özgül Ağırlık (Dansite)", "< 1.012 (Su gibi berrak)", "> 1.020 (Bulanık, yoğun, hücresel)"],
            ["Lökosit Sayısı", "Çok az (< 1000/µL - birkaç mezotelyal hücre)", "Çok yüksek (> 1000-50000/µL - nötrofiller/makrofajlar)"],
            ["Fibrin Varlığı / Pıhtılaşma", "Fibrinojen yoktur; pıhtılaşmaz", "Fibrinojen zengindir; kendiliğinden pıhtılaşır"],
            ["Klasik Klinik Örnekler", "Konjestif kalp yetmezliği, Karaciğer sirozu, Nefrotik sendrom", "Bakteriyel pnömoni efüzyonu, Pürülan menenjit, Peritonit"]
        ]
    },
    15: {
        "title": "Deri ve Mukoza Kanamalarının Boyut ve Klinik Sınıflaması",
        "headers": ["Kanama Tipi", "Çap / Boyut", "Karakteristik Görünüm", "En Sık Etyolojik Nedenler"],
        "rows": [
            ["Peteşi", "1 - 2 mm", "Toplu iğne başı gibi küçük, kırmızı-mor, düz odaklar", "Trombositopeni, trombosit disfonksiyonu, Skorbüt"],
            ["Purpura", "3 - 5 mm", "Peteşiden büyük, bazen palpabl kırmızı-mor odaklar", "Vaskülitler (Henoch-Schönlein), amiloidoz, travma"],
            ["Ekimoz (Çürük)", "> 1 - 2 cm", "Geniş subkutan hematom; morluktan sarı-yeşile döner", "Travma, koagülopati, antikoagülan kullanımı"],
            ["Hematom", "Değişken kitle", "Doku içinde palpe edilen kitle oluşturan kan birikimi", "Büyük damar yırtılması, cerrahi komplikasyon, anevrizma"],
            ["Hemartroz", "Eklem boşluğu", "Eklemde şişlik, ağrı ve hareket kaybı", "Hemofili A ve B, ağır eklem travması"]
        ]
    },
    20: {
        "title": "Arteriyel Trombüsler ile Venöz Trombüslerin Karşılaştırması",
        "headers": ["Özellik", "Arteriyel Trombüs", "Venöz Trombüs (Flebotromboz)"],
        "rows": [
            ["Primer Başlatıcı Faktör", "Endotel Hasarı (Ateroskleroz, vaskülit)", "Staz ve Hiperkoagülabilite"],
            ["Oluştuğu Akım Hızı", "Yüksek akımlı ve türbülanslı ortam", "Düşük akımlı ve durgun venöz ortam"],
            ["Hücresel Bileşim", "Trombositten ve fibrinden zengin ('BEYAZ PIHTI')", "Eritrositlerden ve fibrinden zengin ('KIRMIZI PIHTI')"],
            ["Pıhtının Büyüme Yönü", "Kan akımının tersine, kalbe doğru (RETROGRAD)", "Kan akımı yönünde, kalbe doğru (ANTEGRAD)"],
            ["En Sık Yerleşim", "Koroner, Serebral ve Femoral arterler", "Bacak derin venleri (Popliteal, Femoral, İliak)"],
            ["Primer Klinik Risk", "Organ Enfarktı (Miyokard enfarktüsü, İskemik inme)", "Pulmoner Embolizm (Akciğer damar tıkanması)"]
        ]
    }
}

def build_deck():
    slides = []
    total_matched_questions = 0

    for s_raw in SLIDES_DATA:
        s_num = s_raw["slideNumber"]
        title = s_raw["title"]
        subtitle = s_raw["subtitle"]
        badge = s_raw["badge"]
        badge_color = s_raw["badgeColor"]
        keywords = s_raw["keywords"]
        lead = s_raw["lead"]
        spot_pearls = s_raw["spotPearls"]
        key_bullets = s_raw["keyBullets"]
        flashcards = []
        for fc in s_raw.get("flashcards", []):
            q_val = fc.get("question") or fc.get("front", "")
            a_val = fc.get("answer") or fc.get("back", "")
            flashcards.append({
                "id": fc.get("id", ""),
                "category": fc.get("category", "Akıl Kartı"),
                "front": q_val,
                "back": a_val,
                "question": q_val,
                "answer": a_val,
                "hint": fc.get("hint", "")
            })

        matched_qs = find_matched_questions(keywords, max_count=2)
        total_matched_questions += len(matched_qs)

        narrative_lines = []
        narrative_lines.append(f"### {title}")
        narrative_lines.append(f"#### {subtitle}")
        narrative_lines.append("")
        narrative_lines.append(lead)
        narrative_lines.append("")
        narrative_lines.append("💡 **Klinik ve Sınav Odaklı Spot İpuçları:**")
        for p in spot_pearls:
            narrative_lines.append(f"• {p}")
        narrative_lines.append("")
        narrative_lines.append("#### Detaylı Müfredat Maddeleri ve Tıbbi Patoloji Sentezi")
        for b in key_bullets:
            narrative_lines.append(f"• **{b['title']}:** {b['desc']}")

        synthesis_narrative = "\n".join(narrative_lines).strip()

        core_content = {
            "keyBullets": key_bullets
        }

        if s_num in COMPARISON_TABLES:
            core_content["table"] = COMPARISON_TABLES[s_num]

        slide_obj = {
            "slideNumber": s_num,
            "title": title,
            "subtitle": subtitle,
            "badge": badge,
            "badgeColor": badge_color,
            "synthesisNarrative": synthesis_narrative,
            "flashcards": flashcards,
            "coreContent": core_content,
            "spotPearls": spot_pearls,
            "relatedQuestions": matched_qs,
            "aiPromptSuggestions": [
                f"{title} konusundaki en kritik sınav soruları nelerdir?",
                f"Robbins patolojiye göre {title} patogenezini adım adım açıkla.",
                f"Bu slayttaki bulgular fizyopatolojik olarak hangi hastalıklarla ilişkilidir?"
            ]
        }
        slides.append(slide_obj)

    deck_obj = {
        "id": "learn-odem-hiperemi-konjesyon",
        "title": "Hemodinamik Bozukluklar: Ödem, Hiperemi, Konjesyon, Tromboz ve Kanama",
        "shortTitle": "Hemodinamik Bozukluklar",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Dolaşım, Hücre Hasarı ve İltihap (TIP 301)",
        "instructor": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji AD)",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_matched_questions,
        "totalFlashcardsCount": len(slides) * 2,
        "themeColor": "sky",
        "overview": (
            "Dönem 3 Kurul 1 Patoloji müfredatının hemodinami bloğu; Prof. Dr. Hikmet Keleş'in amfi ders notları "
            "ve Robbins Temel Patoloji referansıyla %500 derinlikte yapılandırılmıştır. Starling kuvvetleri, "
            "ödemin 5 temel patofizyolojik mekanizması, transüda-eksüda ayrımı, anasarka, kalp yetmezliği "
            "hücreleri (kronik pulmoner konjesyon), muskat cevizi karaciğer (hepatik konjesyon), beyin ödemi "
            "ve herniasyon tipleri, kanama morfolojisi (peteşi, purpura, ekimoz), seröz kavite kanamaları, "
            "Virchow triadı, Zahn çizgileri ve arteriyel-venöz trombüs ayrımı 22 interaktif slayt, 44 3D akıl "
            "kartı ve 5 karşılaştırma tablosu ile eksiksiz sunulmaktadır."
        ),
        "highYieldPearls": [
            "Ödem mekanizmasında: Kalp yetmezliği = Hidrostatik basınç artışı; Nefrotik Sendrom ve Siroz = Onkotik basınç düşüşü (hipoalbüminemi).",
            "TRANSÜDA protein fakirdir (<3 g/dL, dansite <1.012, endotel sağlam); EKSÜDA protein zengindir (>3 g/dL, dansite >1.020, endotel hasarlı iltihap).",
            "Kronik pulmoner konjesyonda alveoler makrofajlar eritrosit fagosite ederek 'KALP YETMEZLİĞİ HÜCRELERİ'ne (Hemosiderofaj) dönüşür.",
            "Kronik pasif karaciğer konjesyonunda Zon 3 santrilobüler nekroz ve periportal yağlanma 'MUSKAT CEVİZİ KARACİĞER' tablosu verir.",
            "1-2 mm minik kanama PETEŞİ (trombositopeni); 3-5 mm PURPURA (vaskülit); >1-2 cm ise EKİMOZ olarak adlandırılır.",
            "ZAHN ÇİZGİLERİ trombüsün CANLI VE AKAN KANDA oluştuğunu kanıtlar; postmortem pıhtıda Zahn çizgisi bulunmaz."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Hemodinamik Bozukluklar...")
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
            elif item.get('id') == 'learn-kronik-enflamasyon':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Hemodinamik Bozukluklar marked as completed!")

    print("Success! Hemodynamics deck generation completed.")

if __name__ == '__main__':
    main()
