#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_intracellular_accumulations_deck.py
Generates the deep (%500 detail) 24-slide learning deck for:
"İntraselüler Birikimler ve Patolojik Kalsifikasyonlar" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş)
Incorporating 24 slides, 48 3D flashcards, 5 comparison tables, and matched past exam questions.
"""

import json
import os
import sys

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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında hücre içi birikimler ve kalsifikasyon ile doğrudan ilişkilidir.'
                    })
                    break

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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında hücre içi birikimler ve kalsifikasyon ile doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Hücre İçi Birikimlerin Biyolojik Çerçevesi ve Sınıflaması",
        "subtitle": "Anormal metabolizma, depolanma yerleri ve hücresel toksisite spektrumu",
        "badge": "Genel Bakış",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["hücre içi birikim", "sitoplazma", "organel", "toksisite"],
        "lead": "Hücreler metabolik dengesizlik veya genetik kusurlar nedeniyle çeşitli maddeleri anormal miktarlarda biriktirebilir; bu maddeler tamamen zararsız olabileceği gibi ağır hücre hasarına ve ölüme de yol açabilir.",
        "spotPearls": [
            "Hücre içi birikintiler 3 temel lokalizasyonda yerleşir: SİTOPLAZMA, ÖZELLEŞMİŞ ORGANELLER (özellikle Lizozomlar) veya ÇEKİRDEK.",
            "Biriken maddeler ya normal hücresel metabolitlerdir (lipid, protein, glikojen) ya da anormal/yabancı maddelerdir (pigmentler, mutant proteinler)."
        ],
        "keyBullets": [
            {"title": "Dinamik Hücre Yanıtı", "desc": "Hücre biriken maddeyi metabolize edemez veya dışarı atamazsa organel içi kompartmanlarda hapseder."},
            {"title": "Toksisite ve Hasar Aralığı", "desc": "Hafif yağlanma tamamen geri dönüşümlüyken, mutant protein agregatları ER stresini tetikleyerek apoptoza neden olur."},
            {"title": "Patolojik Tanı Değeri", "desc": "Işık mikroskobunda görülen birikintiler klinisyene primer metabolik hastalık, intoksikasyon veya genetik mutasyon hakkında kesin tanı sağlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-1",
                "question": "Hücre içi anormal birikintilerin en sık yerleştiği üç hücresel kompartman hangileridir?",
                "answer": "Sitoplazma, özelleşmiş organeller (özellikle lizozomlar) ve hücre çekirdeği.",
                "hint": "Hücre içi lokalizasyonlar."
            },
            {
                "id": "fc-ia-2",
                "question": "Hücre içi birikintiler her zaman hücre ölümüne mi yol açar?",
                "answer": "HAYIR; hafif steatoz veya karbon birikimi gibi durumlar zararsız ve geri dönüşümlü olabilirken, aşırı amiloid veya mutant protein birikimi hücreyi ölüme götürür.",
                "hint": "Zararsızdan letale uzanan spektrum."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Dört Temel Hücre İçi Birikim Mekanizması (Şekil 1.24)",
        "subtitle": "Uzaklaştırma yetersizliği, anormal protein, eksojen madde ve lizozomal defekt",
        "badge": "Patogenez",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["birikim mekanizmaları", "lizozomal", "katlanma defekti", "eksojen"],
        "lead": "Robbins patoloji ilkelerine göre hücre içi birikimler dört temel moleküler mekanizma üzerinden meydana gelir.",
        "spotPearls": [
            "1. Yetersiz Uzaklaştırma: Normal endojen madde üretilir fakat paketlenip atılamaz (örn. karaciğer steatozu).",
            "2. Anormal Endojen Madde: Genetik mutasyonla yanlış katlanan protein hücrede hapsolur (örn. α1-antitripsin).",
            "3. Eksojen Madde: Hücrenin parçalayamadığı yabancı partikül birikir (örn. antrakosis / karbon).",
            "4. Lizozomal Depo: Spesifik enzim eksikliğiyle substrat lizozomda çöker (örn. Tay-Sachs, Niemann-Pick)."
        ],
        "keyBullets": [
            {"title": "Metabolik Sekresyon Blokajı", "desc": "Apoprotein sentezi aksadığında trigliseridler hepatosit içinde birikerek karaciğer yağlanmasına yol açar."},
            {"title": "Kinetik Katlanma Bozukluğu", "desc": "Şaperon desteğine rağmen hatalı katlanan proteinler proteazom kapasitesini aşarak ER'de birikir."},
            {"title": "Enzim Yoksunluğu", "desc": "Lizozomal asit hidrolaz eksikliği metabolik ara ürünlerin lizozom içinde şişkin vakuoller oluşturmasına neden olur."}
        ],
        "table": {
            "title": "Hücre İçi Anormal Birikimlerin Dört Temel Mekanizması ve Klinik Örnekleri",
            "headers": ["Mekanizma Tipi", "Hücresel Bozukluk", "Biriken Madde Türü", "Karakteristik Klinik Hastalık"],
            "rows": [
                ["1. Yetersiz Uzaklaştırma", "Normal üretim var; transport veya sekresyon yetersiz", "Normal endojen madde (Trigliserid)", "Hepatosteatoz (Yağlı karaciğer), Nefrotik protein damlaları"],
                ["2. Anormal Endojen Madde", "Genetik mutasyon veya hatalı protein katlanması", "Yanlış katlanmış mutant protein", "α1-Antitripsin eksikliği, Prion hastalıkları (CJD)"],
                ["3. Eksojen Madde Birikimi", "Hücrede bu maddeyi parçalayacak enzim sistemi yok", "Sindirilamayan eksojen partikül", "Antrakosis (Karbon / Kömür tozu), Silikozis, Asbestozis"],
                ["4. Lizozomal Yıkım Bozukluğu", "Genetik asit hidrolaz enzim eksikliği", "Kompleks substrat (Lipid / GAG)", "Gaucher, Tay-Sachs, Niemann-Pick, Mukopolisakkaridozlar"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ia-3",
                "question": "Hücrede normal üretilen bir maddenin transport veya sekresyon kusuru nedeniyle birikmesine en klasik örnek nedir?",
                "answer": "Karaciğerde trigliserid birikimi sonucu gelişen Hepatosteatoz (yağlı karaciğer).",
                "hint": "Lipid sekresyon blokajı."
            },
            {
                "id": "fc-ia-4",
                "question": "Hücrenin metabolize edemediği sindirilemeyen eksojen maddelerin birikimine en yaygın örnek hangisidir?",
                "answer": "Hava kirliliği ve kömür tozunun solunmasıyla gelişen akciğer Antrakosisi (karbon birikimi).",
                "hint": "Siyah akciğer pigmenti."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Hücre İçi Lipid Birikimleri: Spektrum ve Klinik Formlar",
        "subtitle": "Trigliseridler, kolesterol esterleri ve membran fosfolipidlerinin dinamikleri",
        "badge": "Lipid Patolojisi",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["lipid birikimi", "steatoz", "kolesterol", "ateroskleroz"],
        "lead": "Lipidler hücre membranlarının yapısı ve enerji depolanması için yaşamsaldır; ancak anormal birikimleri steatoz, ateroskleroz ve ksantomlar gibi majör klinik tablolara yol açar.",
        "spotPearls": [
            "Hücre içinde en sık biriken 3 temel lipid grubu: TRİGLİSERİDLER, KOLESTEROL/KOLESTERİL ESTERLERİ ve FOSFOLİPİDLERDİR.",
            "Kolesterol birikimleri genellikle köpüksü sitoplazmaya sahip makrofajlar (KÖPÜK HÜCRELERİ) şeklinde izlenir."
        ],
        "keyBullets": [
            {"title": "Trigliserid Dinamiği", "desc": "Karaciğer parankiminde birikerek steatoza (yağlı değişim) neden olur."},
            {"title": "Kolesterol Aşırılığı", "desc": "Ateromatöz plaklarda intimal köpük hücreleri ve ekstraselüler kolesterol kristalleri oluşturur."},
            {"title": "Fosfolipid Agregatları", "desc": "Hasarlı membranlardan kopan fosfolipidler miyelin figürleri ve kalsifikasyon çekirdekleri üretir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-5",
                "question": "İnsan hücrelerinde patolojik olarak biriken başlıca üç lipid sınıfı hangileridir?",
                "answer": "Trigliseridler, kolesterol ve kolesteril esterleri ile fosfolipidler.",
                "hint": "Üç majör yağ grubu."
            },
            {
                "id": "fc-ia-6",
                "question": "Ateroskleroz ve ksantomlarda kolesterol yüklü makrofajlara verilen karakteristik isim nedir?",
                "answer": "Köpük hücreleri (foam cells).",
                "hint": "Köpüksü sitoplazmalı histiyositler."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Steatoz (Yağlı Değişim): Tanım, Organlar ve Patofizyoloji",
        "subtitle": "Parankimal hücrelerde trigliserid birikimi ve karaciğer metabolik kavşağı",
        "badge": "Steatoz",
        "badgeColor": "amber",
        "target_ids": ["d3-k3-pat-017"],
        "keywords": ["steatoz", "trigliserid", "yağlı karaciğer", "hepatosit"],
        "lead": "Steatoz; parankimal hücreler içinde anormal trigliserid birikimidir; en sık lipid metabolizmasının merkezi olan karaciğerde görülmekle birlikte kalp, böbrek ve kasta da izlenebilir.",
        "spotPearls": [
            "STEATOZ TANIMI: Parankimal hücrelerde anormal TRİGLİSERİD birikimidir; en sık KARACİĞERDE görülür.",
            "ETİYOLOJİ ÇEŞİTLİLİĞİ: Gelişmiş ülkelerde en sık nedenler ALKOLİZM, OBEZİTE ve TİP 2 DİYABETTİR (NAFLD/NASH)."
        ],
        "keyBullets": [
            {"title": "Metabolik Merkez Karaciğer", "desc": "Serbest yağ asitleri kandan alınır veya asetattan sentezlenir; trigliseride dönüştürülüp VLDL ile kana salınır."},
            {"title": "Sekresyon Aksaklığı", "desc": "Apoprotein sentezi bozulduğunda (protein malnütrisyonu / kwashiorkor) trigliseridler paketlenemez ve birikir."},
            {"title": "Toksik ve Hipoksik İnhibisyon", "desc": "Alkol ve hipoksi mitokondriyal yağ asidi oksidasyonunu bloke ederek yağ asitlerini trigliserid sentezine yönlendirir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-7",
                "question": "Steatoz (yağlı değişim) hangi spesifik kimyasal lipid türünün parankim hücrelerinde birikmesidir?",
                "answer": "Trigliseridlerin birikmesidir.",
                "hint": "Nötral yağlar."
            },
            {
                "id": "fc-ia-8",
                "question": "Kwashiorkor (ağır protein malnütrisyonu) hastalığında karaciğer yağlanmasının patofizyolojik mekanizması nedir?",
                "answer": "Apoprotein sentezinin yetersiz olması nedeniyle trigliseridlerin lipoprotein (VLDL) olarak paketlenip sekrete edilememesidir.",
                "hint": "Taşıyıcı protein eksikliği."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Hepatosteatoz Morfolojisi: Makroveziküler vs Mikroveziküler Yağlanma",
        "subtitle": "Makroskopik sarı parlak karaciğer ve mikroskopik yağ kistleri",
        "badge": "Morfoloji",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["makroveziküler", "mikroveziküler", "yağ kistleri", "steatohepatit"],
        "lead": "Karaciğer yağlanması makroskopik olarak organı büyütüp sarı ve yağlı bir kıvama getirirken; mikroskobik olarak yağ vakuollerinin boyutuna göre iki farklı paternde sınıflandırılır.",
        "spotPearls": [
            "MAKROVEZİKÜLER YAĞLANMA: Büyük tek bir yağ damlası çekirdeği hücre kenarına iter (en sık; alkol, obezite, diyabette).",
            "MİKROVEZİKÜLER YAĞLANMA: Çekirdek santraldedir, sitoplazma minik köpüksü damlacıklarla doludur (Reye sendromu, gebeliğin akut yağlı karaciğeri, valproat toksisitesi - letal olabilir!)."
        ],
        "keyBullets": [
            {"title": "Makroskopi: Sarı Devasa Karaciğer", "desc": "Karaciğer 3-6 kg ağırlığa ulaşabilir, kenarları küntleşir, kesit yüzeyi parlak sarı ve ele yağlı bulaşır."},
            {"title": "Yağ Kistleri Oluşumu", "desc": "Genişleyen makroveziküller komşu hepatositleri patlatarak ekstraselüler yağ globülleri ve kistler oluşturur."},
            {"title": "Geri Dönüş Eşiği ve Siroz", "desc": "Hafif steatoz etken kalkınca tamamen geri döner; ancak steatohepatit (iltihap + Mallory cisimcikleri) fibrozis ve siroza ilerler."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-9",
                "question": "Makroveziküler ve mikroveziküler yağlanmanın mikroskopik çekirdek yerleşimi farkı nedir?",
                "answer": "Makrovezikülerde dev lipid damlası çekirdeği perifere iter; mikrovezikülerde ise minik damlacıklar sitoplazmaya dağılmıştır ve çekirdek merkezde kalır.",
                "hint": "Çekirdeğin periferik itilmesi vs santral kalması."
            },
            {
                "id": "fc-ia-10",
                "question": "Mikroveziküler karaciğer yağlanmasının görüldüğü hayati acil durumlar nelerdir?",
                "answer": "Reye sendromu (aspirin kullanan çocuklar), gebeliğin akut yağlı karaciğeri ve valproik asit toksisitesi.",
                "hint": "Mitokondriyal toksisite tabloları."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Kolesterol ve Kolesteril Ester Birikimi: Ateroskleroz, Ksantomlar ve Kolesterolozis",
        "subtitle": "Köpük hücreleri, kolesterol kristalleri ve Aşil tendonu ksantomları",
        "badge": "Kolesterol",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["ateroskleroz", "ksantom", "kolesterolozis", "köpük hücresi"],
        "lead": "Hücreler aşırı kolesterolü parçalayamaz; bu nedenle biriken kolesterol esterleri makrofajlar ve damar düz kas hücreleri tarafından yutularak köpük hücrelerine dönüşür.",
        "spotPearls": [
            "ATEROSKLEROZ: Büyük ve orta boy arterlerin intimasında köpük hücreleri, nekrotik kor ve iğnemsi kolesterol kleftleri birikir.",
            "KSANTOMLAR: Ailesel hiperkolesterolemi olgularında subkutan dokuda ve özellikle AŞİL TENDONUNDA sarımsı kolesterol nodülleri oluşur.",
            "KOLESTEROLEZİS: Safra kesesi lamina propriasında kolesterol yüklü makrofaj birikimi ('çilek safra kesesi')."
        ],
        "keyBullets": [
            {"title": "Ateromatöz Plak Patolojisi", "desc": "İntimada biriken LDL okside olur; çöpçü (scavenger) reseptörlü makrofajlar kontrolsüzce yutarak köpük hücresi olur."},
            {"title": "Kolesterol Kleftleri", "desc": "Ölen köpük hücrelerinden dökülen kolesterol kristalleri doku takibinde eriyerek geride iğne biçimli boşluklar bırakır."},
            {"title": "Ksantelazma", "desc": "Göz kapaklarında kolesterol yüklü histiyositlerin oluşturduğu yumuşak sarı plaklardır (dislipidemi göstergesi)."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-11",
                "question": "Ailesel hiperkolesterolemi hastalarında tendonlarda (özellikle Aşil tendonunda) görülen sarı nodüllere ne ad verilir?",
                "answer": "Ksantom (tendon ksantomu).",
                "hint": "Lipid yüklü histiyosit nodülleri."
            },
            {
                "id": "fc-ia-12",
                "question": "Safra kesesi mukozasında kolesterol yüklü makrofajların birikmesiyle oluşan lezyona ne ad verilir?",
                "answer": "Kolesterolozis ('çilek safra kesesi').",
                "hint": "Çilek görünümü."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Protein Birikimleri: Genel İlkeler ve Morfolojik Hiyalinleşme",
        "subtitle": "Artmış geri emilim, aşırı biyosentez ve yanlış katlanmış agregatlar",
        "badge": "Proteinler",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["protein birikimi", "hiyalin", "eozinofilik damlacık", "pinositoz"],
        "lead": "Morfolojik olarak saptanabilen protein birikimleri lipidlere göre daha nadirdir; genellikle sitoplazmada pembe, homojen, camsı 'hiyalin damlacıklar' şeklinde izlenir.",
        "spotPearls": [
            "HİYALİN KAVRAMI: Işık mikroskobunda homojen, camsı, parlak pembe (eozinofilik) görünen her türlü yapısal değişikliği tanımlayan tanımlayıcı bir terimdir.",
            "Üç temel kaynak: 1) Aşırı reabsorpsiyon (tübüllerde), 2) Aşırı normal protein sentezi (plazma hücresinde), 3) Yanlış katlanmış anormal protein agregatları."
        ],
        "keyBullets": [
            {"title": "Eozinofilik Camsı Görünüm", "desc": "Hematoksilen-eozin boyasında protein birikintileri parlak pembe renk alır ve hiyalin adını alır."},
            {"title": "Hücresel Klirens Yetersizliği", "desc": "Proteazom ve lizozom sistemleri anormal protein yükünü eritemediğinde agregatlar hücreyi boğar."},
            {"title": "Apoptoz Tetiklenmesi", "desc": "Endoplazmik retikulumda biriken yanlış katlanmış proteinler 'Unfolded Protein Response' (UPR) ile kaspazları uyarır."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-13",
                "question": "Patolojide 'Hiyalin' terimi neyi ifade eder?",
                "answer": "Işık mikroskobunda homojen, camsı ve parlak pembe (eozinofilik) görünen herhangi bir hücre içi veya hücre dışı materyali ifade eden morfolojik bir terimdir.",
                "hint": "Camsı pembe tanımlama."
            },
            {
                "id": "fc-ia-14",
                "question": "Hücre içinde yanlış katlanmış proteinlerin aşırı birikmesi hangi organel stresini ve ölüm yolunu tetikler?",
                "answer": "Endoplazmik retikulum (ER) stresini ve kaspaz aktivasyonuyla Apoptozu tetikler.",
                "hint": "ER stresi ve programlı ölüm."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Böbrek Proksimal Tübüllerinde Protein Reabsorpsiyon Damlacıkları",
        "subtitle": "Nefrotik sendromda albümin kaçağı, pinositoz ve reversibl hiyalin damlalar",
        "badge": "Böbrek Patolojisi",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["nefrotik sendrom", "proteinüri", "proksimal tübül", "reabsorpsiyon"],
        "lead": "Glomerüler filtre geçirgenliğinin bozulduğu nefrotik sendrom olgularında, proksimal tübül epitel hücreleri aşırı miktardaki albümini pinositozla geri emerek sitoplazmasında biriktirir.",
        "spotPearls": [
            "NEFROTİK SENDROM BULGUSU: Proksimal tübül hücreleri aşırı filtre edilen albümini pinositoz vezikülleri içinde depolar; bunlar parlak pembe HİYALİN DAMLACIKLAR olarak görülür.",
            "TAMAMEN GERİ DÖNÜŞÜMLÜ: Glomerül hasarı düzelip proteinüri kesilirse, tübül lizozomları biriken albümini yıkar ve damlacıklar tamamen kaybolur."
        ],
        "keyBullets": [
            {"title": "Pinositoz ve Lizozomal Füzyon", "desc": "Filtre edilen protein vezikülleri hücre içinde lizozomlarla birleşir ancak yük fazlalığı nedeniyle geçici olarak birikir."},
            {"title": "Tübüler Epitel Morfolojisi", "desc": "Sitoplazmada çok sayıda parlak eozinofilik küresel cisimcikler izlenir; tübül lümeni daralabilir."},
            {"title": "Böbrek Hasarı İndikatörü", "desc": "Bu damlacıklar primer tübül hastalığı değil, ağır glomerüler protein kaçağının (proteinürinin) doğrudan morfolojik kanıtıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-15",
                "question": "Nefrotik sendromlu bir hastanın böbrek biyopsisinde proksimal tübül epitel hücrelerinde görülen parlak pembe damlacıkların içeriği nedir?",
                "answer": "Pinositoz ile idrar filtratından geri emilmiş olan aşırı miktardaki plazma proteinleri (başlıca albümin).",
                "hint": "Geri emilen protein vezikülleri."
            },
            {
                "id": "fc-ia-16",
                "question": "Böbrek tübüllerindeki bu protein reabsorpsiyon damlacıkları kalıcı bir doku hasarı mıdır?",
                "answer": "HAYIR; tamamen geri dönüşümlüdür (reversibl). Proteinüri durduğunda lizozomlar proteini yıkar ve damlacıklar yok olur.",
                "hint": "Reversibilite özelliği."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Plazma Hücrelerinde Russell Cisimcikleri ve İmmünoglobulin Birikimi",
        "subtitle": "Genişlemiş RER sisternaları, Dutcher cisimcikleri ve multipl miyelom",
        "badge": "İmmünopatoloji",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["russell cisimciği", "plazma hücresi", "immünoglobulin", "dutcher"],
        "lead": "Kronik inflamasyon veya plazma hücre neoplazilerinde aşırı immünoglobulin sentezleyen plazma hücrelerinin granüllü endoplazmik retikulumunda devasa homojen eozinofilik cisimcikler birikir.",
        "spotPearls": [
            "RUSSELL CİSİMCİKLERİ: Plazma hücrelerinin granüllü endoplazmik retikulumunda (RER) aşırı sentezlenen İMMÜNOGLOBULİNLERİN birikmesiyle oluşan yuvarlak, parlak eozinofilik cisimciklerdir.",
            "DUTCHER CİSİMCİKLERİ: İmmünoglobulin agregatları hücre ÇEKİRDEĞİ içine invagine olup birikirse bunlara Dutcher cisimciği denir (multipl miyelom ve Waldenström'de sık)."
        ],
        "keyBullets": [
            {"title": "Dev RER Sisternaları", "desc": "Plazma hücresinin protein fabrikası olan RER aşırı antikor yüküyle genişler ve dev küresel bir vakuole döner."},
            {"title": "Mott Hücresi Görünümü", "desc": "İçi çok sayıda Russell cisimciğiyle dolu olan plazma hücrelerine morfolojide 'Mott hücresi' veya dut hücresi adı verilir."},
            {"title": "Reaktif vs Neoplastik Spektrum", "desc": "Kronik periodontit gibi uzun süren enfeksiyonlarda reaktif olarak görülebileceği gibi, multipl miyelomda klonal olarak izlenir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-17",
                "question": "Plazma hücrelerinin endoplazmik retikulumunda biriken eozinofilik immünoglobulin globüllerine ne ad verilir?",
                "answer": "Russell cisimcikleri.",
                "hint": "Plazma hücresi pembe küreleri."
            },
            {
                "id": "fc-ia-18",
                "question": "Russell cisimciği sitoplazmada RER'de yerleşirken, plazma hücresi çekirdeğinde görülen benzer immünoglobulin inklüzyonuna ne ad verilir?",
                "answer": "Dutcher cisimciği.",
                "hint": "Nükleer inklüzyon."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Yanlış Katlanmış Protein Hastalıkları (Tablo 1.4)",
        "subtitle": "Kistik fibrozis, Ailesel hiperkolesterolemi ve Tay-Sachs patolojisi",
        "badge": "Katlanma Hastalıkları",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["yanlış katlanma", "CFTR", "kistik fibrozis", "LDL reseptörü", "Tay-Sachs"],
        "lead": "Genetik mutasyonlar proteinlerin üçüncül konformasyonunu bozar; hücre bu anormal proteinleri ya hızla yıkarak fonksiyon eksikliğine yol açar ya da ER'de biriktirerek hücreyi öldürür.",
        "spotPearls": [
            "KİSTİK FİBROZİS: CFTR proteininin yanlış katlanması sonucu proteazomda erken yıkılması -> Epitel membranında CFTR yokluğu ve koyu kıvamlı sekresyonlar.",
            "AİLESEL HİPERKOLESTEROLEMİ: LDL reseptörünün yanlış katlanarak yıkılması -> LDL klirensi bozulur, ağır hiperkolesterolemi ve erken MI.",
            "TAY-SACHS HASTALIĞI: Heksozaminidaz α alt birimi eksikliği -> Nöronlarda GM2 gangliozid birikimi ve erken nörolojik ölüm."
        ],
        "keyBullets": [
            {"title": "Fonksiyon Kaybı Mekanizması", "desc": "Hücre kalite kontrol mekanizması (ERAD) yanlış katlanan proteini tanır ve fonksiyonel alana ulaşmadan parçalar."},
            {"title": "CFTR DelF508 Mutasyonu", "desc": "Kistik fibrozisteki en sık mutasyon tek bir fenilalanin delesyonu ile proteinin katlanmasını bozar."},
            {"title": "Lipid Reseptör Çöküşü", "desc": "LDL reseptörünün ER'den Golgiye transportunun engellenmesi plazma kolesterolünü 3-5 katına çıkarır."}
        ],
        "table": {
            "title": "Yanlış Katlanmış Proteinlerin Neden Olduğu Hastalıklar (Tablo 1.4 - Robbins 11. Baskı)",
            "headers": ["Hastalık", "Etkilenen Protein", "Moleküler Bozukluk", "Klinik Patoloji Sonucu"],
            "rows": [
                ["Kistik Fibrozis", "CFTR Transmembran İletkenlik Düzenleyici", "Yanlış katlanan mutant CFTR proteazomda yıkılır", "Klor/su transport kaybı, kronik akciğer enfeksiyonları ve bronşiektazi"],
                ["Ailesel Hiperkolesterolemi", "LDL Reseptörü", "Reseptör katlanamaz ve hücre yüzeyine taşınamaz", "LDL klirensinde çöküş, erken yaşta ateroskleroz ve tendon ksantomları"],
                ["Tay-Sachs Hastalığı", "Heksozaminidaz α-alt birimi", "Lizozomal enzim eksikliği ve katlanma defekti", "Nöronlarda toksik GM2 gangliozid birikimi, makulada kiraz kırmızısı leke"],
                ["Retinitis Pigmentosa", "Rodopsin", "Mutant rodopsin ER stresini tetikler", "Retina fotoreseptör hücre kaybı, ilerleyici körlük"],
                ["Creutzfeldt-Jakob (CJD)", "Prion Proteini (PrPC -> PrPSc)", "Alfa heliks yapısının beta kırmalı tabakalara dönüşümü", "Hızlı seyirli süngerimsi nörodejenerasyon ve demans"],
                ["α1-Antitripsin Eksikliği", "α1-Antitripsin (PiZ varyantı)", "ER'de polimerleşerek takılır, sekrete edilemez", "Karaciğerde birikimle Siroz; Akciğerde elastaz aşırılığıyla Panasinüs Amfizemi"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ia-19",
                "question": "Kistik fibrozis hastalığında primer moleküler patoloji proteinin fonksiyon yapamaması mıdır yoksa hücre tarafından yok edilmesi midir?",
                "answer": "Yanlış katlanan mutant CFTR proteininin ER kalite kontrol mekanizması tarafından tanınıp proteazomlarda erkenden yıkılması (hücre yüzeyine hiç ulaşamamasıdır).",
                "hint": "Erken proteazomal yıkım."
            },
            {
                "id": "fc-ia-20",
                "question": "Creutzfeldt-Jakob hastalığında normal prion proteininin (PrPC) patolojik forma (PrPSc) dönüşmesindeki temel yapısal konformasyonel değişim nedir?",
                "answer": "Alfa-heliks yapısının çözülüp proteazlara dirençli beta-kırmalı tabaka (beta-sheet) formuna yanlış katlanmasıdır.",
                "hint": "Alfa heliksten beta tabakaya geçiş."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "α1-Antitripsin Eksikliği: Çift Organ Patolojisi (Karaciğer ve Akciğer)",
        "subtitle": "SERPINA1 gen mutasyonu, PAS-pozitif diyastaz-dirençli globüller ve amfizem",
        "badge": "Genetik & Patoloji",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["antitripsin", "SERPINA1", "amfizem", "PAS boyası", "diyastaz"],
        "lead": "α1-antitripsin eksikliği; yanlış katlanan proteinin üretildiği organda (karaciğer) birikerek toksisite yaptığı, hedef organda ise (akciğer) eksikliği nedeniyle doku yıkımına yol açtığı mükemmel bir çift organ modelidir.",
        "spotPearls": [
            "ÇİFT ORGAN HASARI: Karaciğerde yanlış katlanan mutant Z proteini hepatosit ER'sinde BİRİKİR -> Hepatosit apoptozu, hepatit ve SİROZ.",
            "AKCİĞERDE EKSİKLİK HİSSEDİLİR: Kanda nötrofil elastazını baskılayacak α1-antitripsin bulunmaz -> Nötrofil elastazı alveol elastik liflerini eritir -> PANASİNÜS AMFİZEMİ (özellikle genç sigara içmeyenlerde!).",
            "TANI KOYDURUCU BOYA: Karaciğer biyopsisinde hepatosit sitoplazmasında PAS-POZİTİF, DİYASTAZA DİRENÇLİ pembe globüller izlenir."
        ],
        "keyBullets": [
            {"title": "PiZ Allel Mutasyonu (Glu342Lys)", "desc": "Tek baz mutasyonu proteinin tersiyer yapısını bozarak hepatosit endoplazmik retikulumunda polimerize olmasına yol açar."},
            {"title": "PAS Pozitif ve Diyastaz Direnci", "desc": "Glikojen PAS ile boyanıp diyastazla sindirilirken; α1-antitripsin glikoproteini diyastaz sindirimine DİRENÇLİDİR ve pembe kalır."},
            {"title": "Klinik İkilem", "desc": "Karaciğer hasarı toksik birikimden (gain-of-function); akciğer hasarı ise koruyucu inhibitörün yokluğundan (loss-of-function) kaynaklanır."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-21",
                "question": "α1-antitripsin eksikliğinde karaciğer biyopsisinde hepatosit sitoplazmasında görülen globüllerin histokimyasal boyanma özelliği nedir?",
                "answer": "PAS (Periyodik Asit-Schiff) pozitif ve DİYASTAZ SİNDİRİMİNE DİRENÇLİ olmalarıdır.",
                "hint": "PAS pozitif diyastaz dirençli."
            },
            {
                "id": "fc-ia-22",
                "question": "α1-antitripsin eksikliğinde akciğerde gelişen amfizemin temel patofizyolojik mekanizması nedir?",
                "answer": "Proteaz inhibitörü olan α1-antitripsinin yokluğunda nötrofil elastazının kontrolsüz kalarak alveolar elastik dokuyu parçalamasıdır.",
                "hint": "Nötrofil elastaz aşırılığı."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Hücre İçi Anormal Protein Agregatları: Mallory-Denk, Nörofibriler Yumaklar ve Lewy",
        "subtitle": "Sitokeratin ara filamanları, Tau hiperfosforilasyonu ve α-sinüklein agregasyonu",
        "badge": "Agregatlar",
        "badgeColor": "rose",
        "target_ids": ["d3-k3-pat-017"],
        "keywords": ["mallory denk", "nörofibriler yumak", "tau", "lewy cisimciği", "alkolik hepatit"],
        "lead": "Bazı patolojik durumlarda hasarlanan veya yanlış katlanan sitoiskelet proteinleri lizozom veya proteazomlar tarafından eritilemez ve karakteristik inklüzyon cisimcikleri oluşturur.",
        "spotPearls": [
            "MALLORY-DENK CİSİMCİKLERİ: Alkolik hepatitte (ve NASH'te) hepatosit sitoplazmasında eozinofilik, kordon benzeri yumaklar; SİTOKERATİN 8/18 ara filamanları ve ubikuitin içerir.",
            "NÖROFİBRİLER YUMAKLAR: Alzheimer hastalığında nöronlarda HİPERFOSFORİLE TAU mikrotübül proteininin oluşturduğu alev biçimli fibröz agregatlar.",
            "LEWY CİSİMCİKLERİ: Parkinson hastalığında substantia nigra dopaminerjik nöronlarında ALFA-SİNÜKLEİN birikintileri."
        ],
        "keyBullets": [
            {"title": "Sitokeratin Çöküşü (Mallory-Denk)", "desc": "Toksik asetaldehit ve serbest radikaller sitokeratin ara filamanlarını çapraz bağlayarak hücre içinde eritilemez amorf yumaklar yapar."},
            {"title": "Mikrotübül Çözülmesi (Tau)", "desc": "Hiperfosforile olan Tau mikrotübülleri terk eder ve çift helikal filamanlar halinde nöron gövdesinde yumaklaşır."},
            {"title": "Ubikuitin İle Damgalanma", "desc": "Hücre bu agregatları yıkmak için ubikuitinle etiketler ancak proteazom kanalları tıkandığı için parçalayamaz."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-23",
                "question": "Alkolik karaciğer hastalığında hepatositlerde görülen eozinofilik Mallory-Denk cisimcikleri hangi hücresel proteinden oluşur?",
                "answer": "Sitokeratin ara filamanları (özellikle Sitokeratin 8 ve 18) ve ubikuitin komplekslerinden oluşur.",
                "hint": "Sitokeratin ara filaman yumakları."
            },
            {
                "id": "fc-ia-24",
                "question": "Alzheimer hastalığındaki nörofibriler yumaklar ile Parkinson hastalığındaki Lewy cisimciklerinde biriken temel proteinler sırasıyla hangileridir?",
                "answer": "Alzheimer: Hiperfosforile Tau proteini; Parkinson: Alfa-sinüklein proteini.",
                "hint": "Tau ve alfa-sinüklein."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Glikojen Birikimleri: Diabetes Mellitus ve Glikojenozlar",
        "subtitle": "Armanni-Ebstein lezyonu, PAS pozitifliği ve enzim eksikliği sendromları",
        "badge": "Karbonhidratlar",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-pat-006", "d3-k1-pat-032"],
        "keywords": ["glikojen", "diabetes mellitus", "glikojen depo", "PAS", "Armanni-Ebstein"],
        "lead": "Glikojen normalde hücrelerde acil enerji deposu olarak depolanır; glikoz regülasyonu bozulduğunda veya glikolitik enzimler genetik olarak eksik olduğunda dokularda masif birikim yapar.",
        "spotPearls": [
            "DİABETES MELLİTUS'TA GLİKOJEN: Kontrolsüz hiperglisemide böbrek Henle kulpu ve distal tübüllerinde (Armanni-Ebstein lezyonu), karaciğerde ve kalp kasında birikir.",
            "GLİKOJEN DEPO HASTALIKLARI: Von Gierke (Tip I - Glukoz-6-fosfataz), Pompe (Tip II - Lizozomal asit maltaz; kardiyomegaliyle erken ölüm), McArdle (Tip V - Kas fosforilazı).",
            "TANI YÖNTEMİ: Glikojen doku kesitlerinde PAS ile parlak macenta boyanır; DİYASTAZ İLE SİNDİRİLİR (PAS-diyastaz negatifleşir)."
        ],
        "keyBullets": [
            {"title": "Armanni-Ebstein Hücreleri", "desc": "Glukozüri sırasında böbrek tübüllerine aşırı süzülen glukoz tübül hücrelerinde berrak glikojen vakuolleri oluşturur."},
            {"title": "Lizozomal Glikojen Yıkımı (Pompe)", "desc": "Diğer glikojenozlar sitoplazmik enzim defektleriyken, Pompe hastalığı bir lizozomal depo hastalığıdır."},
            {"title": "Vakuoler Boşluk Görünümü", "desc": "Rutin HE boyamada glikojen suda çözündüğü için hücre sitoplazması boş veya berrak (clear-cell) görünür."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-25",
                "question": "Glikojenin histolojik kesitlerde PAS (Periyodik Asit-Schiff) boyası ile diğer maddelerden ayırt edilmesini sağlayan enzim testi nedir?",
                "answer": "Diyastaz testi; glikojen diyastaz enzimi ile sindirilerek PAS boyanması kaybolur (PAS-pozitif, diyastaz-duyarlı).",
                "hint": "Diyastazla sindirilme."
            },
            {
                "id": "fc-ia-26",
                "question": "Kötü kontrollü diabetes mellitus hastalarında böbrek tübül epitel hücrelerinde görülen aşırı glikojen birikimi lezyonuna ne ad verilir?",
                "answer": "Armanni-Ebstein lezyonu (veya Armanni-Ebstein hücreleri).",
                "hint": "Diyabetik tübül glikojenozu."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Pigment Birikimleri: Biyolojik Sınıflama ve Genel Özellikler",
        "subtitle": "Eksojen çevre kirleticileri vs endojen biyokimyasal renk maddeleri",
        "badge": "Pigmentler",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["pigmentler", "eksojen", "endojen", "karbon", "melanin", "hemosiderin"],
        "lead": "Pigmentler dokulara kendilerine özgü renk veren maddelerdir; vücuda dışarıdan giren eksojen pigmentler veya vücut içinde sentezlenen endojen pigmentler olarak ikiye ayrılır.",
        "spotPearls": [
            "EN SIK EKSOJEN PİGMENT: Hava kirliliği ve tütün dumanında bulunan KARBON (Kömür tozu / Antrakotik pigment).",
            "BAŞLICA ENDOJEN PİGMENTLER: LİPOFUKSİN (yaşlılık/aşınma), MELANİN (UV koruyucu siyah pigment) ve HEMOSİDERİN (demir deposu)."
        ],
        "keyBullets": [
            {"title": "Eksojen Giriş Yolları", "desc": "İnhalasyon (akciğer), sindirim (ağır metaller - kurşun çizgisi) veya deri inokülasyonu (dövme mürekkepleri)."},
            {"title": "Endojen Sentez Yolları", "desc": "Hemoglobin katabolizması (hemosiderin/bilirubin), tirozin oksidasyonu (melanin) veya membran lipid peroksidasyonu (lipofuksin)."},
            {"title": "Fagositik Taşıma", "desc": "Gerek eksojen gerek endojen pigmentler sıklıkla doku makrofajları tarafından fagosite edilerek lenf nodlarına taşınır."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-27",
                "question": "İnsan vücudunda en sık rastlanan eksojen pigment hangisidir?",
                "answer": "Karbon pigmenti (kömür tozu / antrakotik pigment).",
                "hint": "Hava kirliliği ve tütün kaynaklı."
            },
            {
                "id": "fc-ia-28",
                "question": "Hücre içi en önemli üç endojen pigment hangileridir?",
                "answer": "Lipofuksin, Melanin ve Hemosiderin.",
                "hint": "Üç majör endojen renk maddesi."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Eksojen Pigment: Karbon (Antrakosis) ve Akciğer Patolojisi",
        "subtitle": "Alveoler makrofajlar, trakeobronşiyal lenf nodları ve kömür işçisi pnömokonyozu",
        "badge": "Eksojen Pigment",
        "badgeColor": "slate",
        "target_ids": [],
        "keywords": ["antrakosis", "karbon", "kömür tozu", "alveoler makrofaj"],
        "lead": "Şehir havasında ve sigara dumanında bulunan karbon partikülleri solunduğunda alveoler makrofajlarca yutulur ve lenfatik drenajla hilus lenf düğümlerine taşınır.",
        "spotPearls": [
            "ANTRAKOSİS: Akciğer parankiminde ve trakeobronşiyal lenf nodlarında siyah karbon birikmesidir; kentte yaşayan hemen herkeste zararsız bir bulgu olarak vardır.",
            "KÖMÜR İŞÇİSİ PNÖMOKONYOZU (CWP): Kömür madencilerinde aşırı karbon ve silika maruziyeti makrofaj ölümüne, yoğun fibroza ve masif parankimal harabiyete yol açar."
        ],
        "keyBullets": [
            {"title": "Hücresel Fagositoz", "desc": "Alveol lümenine inen karbon partikülleri makrofajlarca yutulur ancak sindirilemez (enzimi yoktur)."},
            {"title": "Lenfatik Göç", "desc": "Karbon yüklü makrofajlar lenf damarlarıyla plevra altına ve hiler lenf düğümlerine giderek buraları siyaha boyar."},
            {"title": "Dövme (Tattooing)", "desc": "Deriye enjekte edilen çözünmeyen pigmentler ömür boyu dermal makrofajlar içinde hareketsiz kalır."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-29",
                "question": "Akciğerde antrakosise neden olan karbon partiküllerini fagosite eden temel savunma hücresi hangisidir?",
                "answer": "Alveoler makrofajlar.",
                "hint": "Akciğer süpürge hücresi."
            },
            {
                "id": "fc-ia-30",
                "question": "Dövme (tattoo) işleminde deriye verilen mürekkep partikülleri nerede ve hangi hücrelerde ömür boyu depolanır?",
                "answer": "Dermiste yerleşik dermal makrofajların (histiyositlerin) sitoplazmasında depolanır.",
                "hint": "Dermal makrofaj içi birikim."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Lipofuksin ('Aşınma-Yıpranma' Pigmenti) ve Esmer Atrofi",
        "subtitle": "Serbest radikal lipid peroksidasyonu, perinükleer yerleşim ve yaşlanma",
        "badge": "Yaşlanma Pigmenti",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["lipofuksin", "aşınma pigmenti", "esmer atrofi", "lipid peroksidasyonu"],
        "lead": "Lipofuksin ('ceroid' veya yaşlılık pigmenti); doymamış membran lipidlerinin serbest radikal peroksidasyonu sonucu lizozomlarda sindirilemeyen artıkların oluşturduğu altın sarısı-kahverengi pigmenttir.",
        "spotPearls": [
            "LİPOFUKSİN KAYNAĞI: Hücre zarlarının oksijen radikalleriyle LİPİD PEROKSİDASYONUNA uğraması sonucu oluşan polimerize protein-lipid kompleksidir.",
            "ESMER ATROFİ: Yaşlılıkta ve ağır kaşekside küçülen kalp (miyokard) ve karaciğerde masif lipofuksin birikimi organa kahverengi görünüm verir ('Esmer Atrofi').",
            "MİKROSKOPİK GÖRÜNÜM: Özellikle miyosit ve hepatosit çekirdeğinin hemen kutuplarında (PERİNÜKLEER) sarı-kahverengi ince granüller."
        ],
        "keyBullets": [
            {"title": "Zararsız Yaşlanma Belirteci", "desc": "Lipofuksin hücreye doğrudan toksik değildir; hücrenin geçmiş serbest radikal hasarlarının kalıcı 'biyolojik ayak izidir'."},
            {"title": "Bölünmeyen Hücrelerde Birikim", "desc": "Mitoz bölünme yapamayan kalıcı hücrelerde (kalp kası lifleri ve beyin nöronları) yaşla birlikte katlanarak artar."},
            {"title": "Otofajik Lizozom Kökeni", "desc": "Hücre içi organel sindirimi (otofaji) tamamlanamadığında rezidüel cisimciklerde birikir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-31",
                "question": "Lipofuksin pigmentinin biyokimyasal kökeni nedir?",
                "answer": "Serbest oksijen radikallerinin yol açtığı membran fosfolipid peroksidasyonu ve polimerize protein kompleksleridir.",
                "hint": "Serbest radikal lipid hasarı."
            },
            {
                "id": "fc-ia-32",
                "question": "Yaşlı bir hastanın kalbinde atrofi ile birlikte altın sarısı-kahverengi perinükleer pigment birikimine ne ad verilir?",
                "answer": "Esmer Atrofi (Brown Atrophy).",
                "hint": "Kahverengi yaşlılık atrofisi."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Melanin ve Hemosiderin: Demir Depolanması ve Prusya Mavisi Reaksiyonu",
        "subtitle": "Melanositler, lokal/sistemik hemosideroz ve Perls Prusya mavisi histokimyası",
        "badge": "Demir & Pigment",
        "badgeColor": "violet",
        "target_ids": ["d3-k3-pat-003", "d3-k5-pat-022"],
        "keywords": ["melanin", "hemosiderin", "prusya mavisi", "perls", "hemokromatoz"],
        "lead": "Hemosiderin hemoglobinden türeyen demir depolama pigmentidir; altın sarısı görünümüyle lipofuksine çok benzer ancak PRUSYA MAVİSİ boyası ile maviye boyanarak kesin olarak ayrılır.",
        "spotPearls": [
            "HEMOSİDERİN: Hemoglobin katabolizması sonucu serbest kalan demirin ferritine bağlanıp agregat oluşturmasıyla doğar; altın sarısı-kahverengi kaba granüllerdir.",
            "AYIRICI TANI - PRUSYA MAVİSİ (PERLS): Hemosiderindeki Fe3+ demiri potasyum ferrosiyanür ile reaksiyona girerek PARLAK MAVİ renk verir! Lipofuksin ve melanin boyanmaz (Kurul çıkmış soru!).",
            "LOKAL vs SİSTEMİK: Lokal hemosideroz eski çürük/kanama alanlarında; sistemik hemosideroz kan transfüzyonları, hemoliz ve Herediter Hemokromatoziste görülür."
        ],
        "keyBullets": [
            {"title": "Hematomun Renk Evrimi", "desc": "Kırmızı eritrosit (hemoglobin) -> Yeşilimsi biliverdin -> Sarımsı bilirubin -> Altın-kahverengi hemosiderin."},
            {"title": "Organ Toksisitesi (Hemokromatoz)", "desc": "Demir birikimi aşırıya kaçtığında Fenton reaksiyonuyla hidroksil radikalleri üretir; siroz, diyabet ve kalp yetmezliği yapar."},
            {"title": "Melanin Karşılaştırması", "desc": "Melanositlerde tirozinaz ile üretilir, UV bariyeridir; Prusya mavisi ile boyanmaz, Fontana-Masson ile gümüşlenir."}
        ],
        "table": {
            "title": "Başlıca Doku Pigmentlerinin Karşılaştırmalı Özellikleri ve Ayırıcı Boyaları",
            "headers": ["Pigment", "Köken / Kaynak", "Işık Mikroskobu Rengi", "Özel / Ayırıcı Boya", "Temel Klinik Durum"],
            "rows": [
                ["Karbon (Antrakosis)", "Eksojen (Hava kirliliği, tütün)", "Kömür siyahı granüller", "Özel boyaya gerek yok (siyah)", "Kent yaşamı, Kömür işçisi pnömokonyozu"],
                ["Lipofuksin", "Endojen (Lipid peroksidasyonu)", "Altın sarısı - açık kahverengi", "PAS (+), Sudan Black (+), Prusya (-)", "Hücresel yaşlanma, Kalpte Esmer Atrofi"],
                ["Hemosiderin", "Endojen (Hemoglobin / Demir)", "Altın sarısı - pas kahverengisi", "Prusya Mavisi (Perls) ile PARLAK MAVİ", "Eski kanama, Hemolitik anemi, Hemokromatoz"],
                ["Melanin", "Endojen (Tirozinaz enzimi)", "Koyu kahverengi - siyah", "Fontana-Masson (+), Prusya (-)", "Güneş yanığı, Çil, Melanositik Nevus, Melanom"],
                ["Bilirubin", "Endojen (Halka açılmış porfirin)", "Yeşilimsi sarı - zeytin yeşili", "Fouchet boyası (+)", "Sarılık, Safra tıkanıklığı, Kolestaz"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ia-33",
                "question": "Karaciğer biyopsisinde görülen kahverengi pigmentin hemosiderin mi yoksa lipofuksin mi olduğunu ayırt etmek için hangi histokimyasal boya kullanılır?",
                "answer": "Prusya Mavisi (Perls) boyası; hemosiderindeki demir mavi renge boyanır, lipofuksin boyanmaz.",
                "hint": "Demir spesifik mavi boya."
            },
            {
                "id": "fc-ia-34",
                "question": "Deri altına kanama olduğunda (hematom / morluk) gün içinde mor-mavi rengin yeşile, sonra sarıya ve kahverengiye dönmesini sağlayan sırasıyla hangi pigmentlerdir?",
                "answer": "Hemoglobin (kırmızı-mor) -> Biliverdin (yeşil) -> Bilirubin (sarı) -> Hemosiderin (altın-kahverengi).",
                "hint": "Eritrosit katabolizma zinciri."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Hücre Dışı Birikimler ve Patolojik Kalsifikasyona Giriş",
        "subtitle": "Kalsiyum fosfat tuzlarının anormal çöküşü, distrofik ve metastatik ayrımı",
        "badge": "Kalsifikasyon",
        "badgeColor": "red",
        "target_ids": ["d3-k1-pat-029"],
        "keywords": ["patolojik kalsifikasyon", "distrofik", "metastatik", "kalsiyum fosfat"],
        "lead": "Patolojik kalsifikasyon; yumuşak dokularda kalsiyum tuzlarının anormal biçimde çökmesidir; serum kalsiyum düzeyine ve hedef dokunun canlılığına göre Distrofik veya Metastatik olarak ikiye ayrılır.",
        "spotPearls": [
            "DİSTROFİK KALSİFİKASYON: Serum kalsiyum düzeyi NORMALDİR; kalsiyum ÖLÜ VEYA HASARLI DOKULARA çöker (lokal patoloji).",
            "METASTATİK KALSİFİKASYON: Serum kalsiyum düzeyi YÜKSEKTİR (HİPERKALSEMİ); kalsiyum NORMAL (SAĞLIKLI) DOKULARA çöker (sistemik metabolik patoloji)."
        ],
        "keyBullets": [
            {"title": "Kristal Bileşimi", "desc": "Her iki tipte de çöken kalsiyum tuzları başlıca amorf kalsiyum fosfat ve hidroksiapatit kristalleri şeklindedir."},
            {"title": "Makroskopi: Kum ve Taş Sertliği", "desc": "Kalsifiye dokular beyaz, tebeşirimsi, sert ve gevrek bir hal alır; kesildiğinde kum gibi çatırdar (kumansı his)."},
            {"title": "Mikroskopi: Bazofilik Kümeler", "desc": "HE boyamada kalsiyum tuzları koyu mavi-mor (yoğun bazofilik), amorf veya granüler çökeltiler olarak görülür."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-35",
                "question": "Distrofik kalsifikasyon ile metastatik kalsifikasyon arasındaki en temel iki fizyopatolojik fark nedir?",
                "answer": "1) Serum kalsiyumu: Distrofikte normal, metastatikte yüksektir (hiperkalsemi). 2) Doku durumu: Distrofikte ölü/hasarlı dokuda, metastatikte normal dokuda birikir.",
                "hint": "Kalsiyum seviyesi ve doku canlılığı."
            },
            {
                "id": "fc-ia-36",
                "question": "Patolojik kalsifikasyon alanları rutin Hematoksilen-Eozin (HE) kesitlerinde ne renk görünür?",
                "answer": "Koyu mavi-mor (yoğun bazofilik) amorf veya granüler çökeltiler olarak görülür.",
                "hint": "Bazofilik boyanma."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Distrofik Kalsifikasyon: Mekanizma, Başlatıcı Veziküller ve Aterom Plağı",
        "subtitle": "Mitokondriyal nükleasyon, membran vezikülleri, ateroskleroz ve kalp kapakları",
        "badge": "Distrofik",
        "badgeColor": "rose",
        "target_ids": ["d3-k1-pat-029", "d3-k4-pat-005"],
        "keywords": ["distrofik kalsifikasyon", "aterosklerotik plak", "kalsifik aort darlığı", "mitokondri"],
        "lead": "Distrofik kalsifikasyon nekrotik hücre artıklarının kalsiyumu bağlamasıyla başlar; serum kalsiyumu tamamen normal olduğu halde doku taşlaşabilir.",
        "spotPearls": [
            "BAŞLANGIÇ ÇEKİRDEĞİ (NÜKLEASYON): Ölen hücrelerin hasarlı membranlarından kopan membran vezikülleri kalsiyumu bağlar; mitokondriler kristalleşmeyi başlatır.",
            "ATEROSKLEROZ: İleri aterom plaklarında intima nekrozu zemininde distrofik kalsifikasyon gelişir; damar duvarı kireçlenir ve kırılganlaşır (Kurul 1 Soru #29 çeldiricisi!).",
            "KALP KAPAKLARI: Yaşlılıkta dejeneratif kalsifik aort darlığı sol ventrikül hipertrofisine ve kalp yetmezliğine yol açar."
        ],
        "keyBullets": [
            {"title": "Nekrotik Tip Bağımsızlığı", "desc": "Koagülatif nekroz (enfarkt), kazeöz nekroz (tüberküloz) veya enzimatik yağ nekrozu (pankreatit sabunlaşması) alanlarında gelişebilir."},
            {"title": "Membran Fosfatidilserin Rolü", "desc": "Hasarlı membrandaki asidik fosfolipidler kalsiyumu çeker; fosfataz enzimleri fosfat ekleyerek kristali büyütür."},
            {"title": "Ghon Kompleksi Taşlaşması", "desc": "Tüberküloz odakları distrofik kalsifikasyonla tamamen kireçlenip radyografide opak taş gibi izlenir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-37",
                "question": "Distrofik kalsifikasyonda kalsiyum fosfat kristallerinin hücresel düzeyde ilk çökmeye başladığı organel hangisidir?",
                "answer": "Nekrotik hücrelerin kalsiyum yüklenmiş mitokondrileri ve hasarlı membran vezikülleridir.",
                "hint": "Mitokondri ve membran vezikülü."
            },
            {
                "id": "fc-ia-38",
                "question": "Aterosklerotik plak içinde gelişen kalsifikasyon distrofik midir yoksa metastatik midir?",
                "answer": "DİSTROFİKTİR; çünkü serum kalsiyumu normaldir ve birikim plak içindeki nekrotik merkezde gerçekleşir.",
                "hint": "Serum Ca normal, plak nekrotik."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Psammoma Cisimcikleri: Lameller Kalsifikasyon ve İlişkili Tümörler",
        "subtitle": "Konsantrik lamelli kireç odakları, tiroid papiller karsinomu ve menenjiom",
        "badge": "Tanısal Cisimcikler",
        "badgeColor": "violet",
        "target_ids": ["d3-k1-pat-049", "d3-k1-pat-058"],
        "keywords": ["psammoma", "psammom cisimciği", "tiroid papiller", "over seröz", "menenjiom"],
        "lead": "Bazı tümörlerde tek tek hücrelerin nekroze olup distrofik kalsifikasyona uğraması ve üzerine ardışık kalsiyum tabakalarının birikmesiyle konsantrik lameller 'Psammoma Cisimcikleri' oluşur.",
        "spotPearls": [
            "PSAMMOMA CİSİMCİĞİ TANIMI: Mikroskopta soğan zarı gibi iç içe geçmiş konsantrik kalsifiye lameller yapılar.",
            "GÖRÜLDÜĞÜ MAJÖR TÜMÖRLER (PSaMMoma): 1) Papiller Tiroid Karsinomu, 2) Seröz Over Karsinomu, 3) Menenjiom, 4) Mezotelyoma.",
            "KLİNİK ÖNEM: İnce iğne aspirasyon biyopsisinde psammoma cisimciği görülmesi papiller tiroid karsinomu için kuvvetli tanısal ipucudur."
        ],
        "keyBullets": [
            {"title": "Lameller Kalsifikasyon Adımları", "desc": "Tek bir tümör hücresi ölür -> Yüzeyine kalsiyum çöker -> Komşu hücreler ölür -> Kat kat mineral tabakaları birikir."},
            {"title": "Kumansı Görünüm (Yunanca Psammos)", "desc": "Tümör dokusunda kum tanecikleri hissi verir; radyolojik mikrokalsifikasyonlara karşılık gelir."},
            {"title": "Menenjiomdaki Psammomatöz Tip", "desc": "Benign menenjiomun histolojik alt tiplerinden biri masif psammoma cisimcikleriyle karakterizedir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-39",
                "question": "Histopatolojide konsantrik lameller tarzda tabakalanmış yuvarlak kalsifikasyonlara ne ad verilir?",
                "answer": "Psammoma cisimcikleri (Psammom cisimciği).",
                "hint": "Soğan zarı şeklinde kalsiyum."
            },
            {
                "id": "fc-ia-40",
                "question": "Psammoma cisimciklerinin en karakteristik olarak görüldüğü üç önemli neoplazi hangileridir?",
                "answer": "1) Tiroid Papiller Karsinomu, 2) Overin Seröz Karsinomu, 3) Menenjiom.",
                "hint": "Tiroid, over seröz ve meninks."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Metastatik Kalsifikasyon: Hiperkalsemi Etiyolojisi ve Sistemik Nedenler",
        "subtitle": "Hiperparatiroidizm, kemik destrüksiyonu, sarkoidoz ve böbrek yetmezliği",
        "badge": "Metastatik",
        "badgeColor": "red",
        "target_ids": ["d3-k1-pat-029"],
        "keywords": ["metastatik kalsifikasyon", "hiperkalsemi", "hiperparatiroidizm", "sarkoidoz", "kronik böbrek yetmezliği"],
        "lead": "Metastatik kalsifikasyon normal dokularda sistemik hiperkalsemiye bağlı olarak gelişir; etiyolojisinde kalsiyum metabolizmasını bozan dört majör neden grubu yer alır.",
        "spotPearls": [
            "KURUL 1 ÇIKMIŞ SORU (Soru #29): Metastatik kalsifikasyona yol açan durumlar: HİPERPARATİROİDİZM, SARKOİDOZ ve KRONİK BÖBREK YETMEZLİĞİDİR (Aterom plağı ise distrofiktir!).",
            "1. HİPERPARATİROİDİZM: Primer (paratiroid adenomu) veya sekonder (kronik böbrek yetmezliğinde fosfat retansiyonu).",
            "2. KEMİK YIKIMI: Multipl miyelom, kemik metastazları veya immobilizasyon.",
            "3. VİTAMİN D AŞIRILIĞI: İntoksikasyon veya Sarkoidozda granülom makrofajlarının kontrolsüz 1-alfa hidroksilaz üretimi."
        ],
        "keyBullets": [
            {"title": "PTH Hormon Fazlalığı", "desc": "Kemikten osteoklastik kalsiyum rezorpsiyonunu ve böbrekten kalsiyum emilimini aşırı artırır."},
            {"title": "Malignite Hiperkalsemisi", "desc": "Kemik metastazlarındaki litik lezyonlar veya tümörlerin PTHrP (paratiroid hormon ilişkili peptid) salgılaması."},
            {"title": "Sarkoidoz Mekanizması", "desc": "Granülomlardaki epiteloid makrofajlar kontrolsüz D vitamini aktifleştirerek bağırsaktan aşırı kalsiyum emdirir."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-41",
                "question": "Sarkoidoz hastalarında hiperkalsemi ve metastatik kalsifikasyon gelişmesinin moleküler mekanizması nedir?",
                "answer": "Granülomlardaki aktive makrofajların 1-alfa hidroksilaz enzimi üreterek kontrolsüz aktif D vitamini (kalsitriol) sentezlemesidir.",
                "hint": "Makrofaj kaynaklı D vitamini aktivasyonu."
            },
            {
                "id": "fc-ia-42",
                "question": "Kronik böbrek yetmezliğinde metastatik kalsifikasyonu tetikleyen temel endokrin ve mineral mekanizma nedir?",
                "answer": "Fosfat atılamaması (fosfat retansiyonu) ve D vitamini sentezlenememesi sonucu gelişen Sekonder Hiperparatiroidizmdir.",
                "hint": "Fosfat birikimi ve sekonder PTH artışı."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Metastatik Kalsifikasyonun Hedef Organları: Asit Atılımı ve Doku Alkalinizasyonu",
        "subtitle": "Mide fundusu, akciğer alveol septaları, böbrek tübülleri (nefrokalsinoz)",
        "badge": "Hedef Dokular",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["nefrokalsinoz", "mide mukozası", "akciğer alveol", "asit atılımı", "alkalinizasyon"],
        "lead": "Metastatik kalsifikasyon vücuttaki herhangi bir normal dokuda gelişebilmekle birlikte; asit salgılayan ve bu nedenle kendi iç ortamı hafif alkali kalan dokuları özellikle tercih eder.",
        "spotPearls": [
            "HEDEF DOKULAR VE PREFERANS: 1) MİDE MUKOZASI (asit salgılar), 2) AKCİĞER ALVEOL SEPTALARI (CO2 kaybeder), 3) BÖBREK TÜBÜLLERİ (asit idrara atılır).",
            "BİYOFİZİKSEL NEDEN: Asit dışarı atıldığında hücre içi kompartman rölatif ALKALİ kalır; alkali ortam kalsiyum fosfat tuzlarının çökmesini dramatik olarak kolaylaştırır.",
            "NEFROKALSİNOZ: Böbrek parankim ve tübüllerinde yaygın kalsiyum çökmesi renal tübüler asidoz ve böbrek yetmezliğine yol açabilir."
        ],
        "keyBullets": [
            {"title": "Mide Asit Pompası", "desc": "Paryetal hücreler lümene HCl pompalarken sitozol alkali hale gelir ve bazal membran boyunca kalsiyum çöker."},
            {"title": "Akciğer Gaz Değişimi", "desc": "Alveol kılcallarından hızla CO2 atılması kan pH'sını hafif yükseltir; alveol elastik lifleri kalsifiye olur."},
            {"title": "Klinik Seyir", "desc": "Genellikle sessizdir ancak masif akciğer tutulumu gaz difüzyonunu bozar; masif böbrek tutulumu yetmezlik yapar."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-43",
                "question": "Metastatik kalsifikasyonun en sık mide mukozası, akciğerler ve böbreklerde görülmesinin biyofiziksel sebebi nedir?",
                "answer": "Bu organların vücuttan asit (HCl, CO2 veya asit idrar) atarak kendi doku içi ortamlarını nispeten alkali hale getirmeleri ve alkali ortamın kalsiyum çökmesini kolaylaştırmasıdır.",
                "hint": "Asit kaybı ve internal alkalinizasyon."
            },
            {
                "id": "fc-ia-44",
                "question": "Böbrek tübül epiteli ve interstisyumunda yaygın kalsiyum tuzlarının çökmesiyle seyreden metastatik tabloya ne ad verilir?",
                "answer": "Nefrokalsinoz (nephrocalcinosis).",
                "hint": "Böbrek kireçlenmesi."
            }
        ]
    },
    {
        "slideNumber": 23,
        "title": "Distrofik vs Metastatik Kalsifikasyon: Büyük Karşılaştırma Matrisi",
        "subtitle": "Klinik patoloji korelasyonu, laboratuvar ayrımları ve organ hasar potansiyeli",
        "badge": "Karşılaştırma Matrisi",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-pat-029"],
        "keywords": ["distrofik vs metastatik", "kalsiyum tablosu", "kurul 1 soru"],
        "lead": "Tıbbi Patoloji sınavlarının ve klinisyenin en temel karar ağacı: Serum kalsiyumu ve doku durumuna göre distrofik ile metastatik kalsifikasyonun kesin ayrımıdır.",
        "spotPearls": [
            "SERUM KALSİYUMU: Distrofikte kesinlikle NORMALDİR; metastatikte kesinlikle YÜKSEKTİR (Hiperkalsemi).",
            "DOKU HASARI: Distrofik hasarlı/ölü dokuyu (infarkt, nekroz, aterom) tutar; metastatik tamamen sağlam normal dokuları tutar.",
            "TEDAVİ YAKLAŞIMI: Distrofikte hasarlı doku/kapak cerrahi olarak onarılır; metastatikte altta yatan hiperkalsemi nedeni (adenom, tümör vb.) tedavi edilir."
        ],
        "keyBullets": [
            {"title": "Laboratuvar Parametreleri", "desc": "Distrofikte kalsiyum ve fosfat dengesi normalken; metastatikte hiperkalsemi veya kalsiyum-fosfat çarpımı (>70) yüksektir."},
            {"title": "Mekanizma Ayrımı", "desc": "Distrofikte membran fosfolipidleri kalsiyumu bağlarken; metastatikte iyonik çözünürlük sınırı aşıldığı için kendiliğinden çöker."},
            {"title": "Klinik Etki", "desc": "Distrofik lokal organ disfonksiyonu (kapak darlığı) yaparken; metastatik yaygın çoklu organ tutulumuna neden olur."}
        ],
        "table": {
            "title": "Distrofik ve Metastatik Kalsifikasyonun Karşılaştırmalı Özellikleri (Robbins 11. Baskı)",
            "headers": ["Parametre", "Distrofik Kalsifikasyon", "Metastatik Kalsifikasyon"],
            "rows": [
                ["Serum Kalsiyum Düzeyi", "NORMAL (Kalsiyum metabolizması bozukluğu yoktur)", "YÜKSEK (Sistemik Hiperkalsemi mevcuttur)"],
                ["Etkilenen Hedef Doku", "ÖLÜ, NEKROTİK veya AĞIR HASARLI dokular", "NORMAL, SAĞLIKLI dokular"],
                ["Yerleşim Alanı", "Lokalize (Enfarkt, aterom plağı, kazeöz nekroz, kapak)", "Yaygın / Sistemik (Mide, akciğer, böbrek, arterler)"],
                ["Başlatıcı Mekanizma", "Nekrotik membran vezikülleri ve mitokondriyal nükleasyon", "Yüksek serum Ca x P çarpımına bağlı presipitasyon"],
                ["Sık Karşılaşılan Nedenler", "Ateroskleroz, Tüberküloz lenfadeniti, Kalsifik aort darlığı", "Hiperparatiroidizm, Kemik metastazları, Sarkoidoz, KBY"],
                ["Klinik Önemi", "Lokal kapak stenozu veya aterom kırılganlığı", "Nefrokalsinoz, respiratuar yetmezlik veya sessiz"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ia-45",
                "question": "Serum kalsiyum ve fosfat düzeyleri tamamen normal olan bir hastada aort kapağında kalsiyum çökmesi hangi kalsifikasyondur?",
                "answer": "Distrofik Kalsifikasyon.",
                "hint": "Normal kalsiyum düzeyi."
            },
            {
                "id": "fc-ia-46",
                "question": "Primer hiperparatiroidizmi olan bir hastanın mide mukozası ve böbreklerinde kalsiyum birikmesi hangi kalsifikasyondur?",
                "answer": "Metastatik Kalsifikasyon.",
                "hint": "Hiperkalsemiye bağlı birikim."
            }
        ]
    },
    {
        "slideNumber": 24,
        "title": "Sentez ve Özet: Hücre İçi Birikimler ve Kalsifikasyon Yol Haritası",
        "subtitle": "Prof. Dr. Hikmet Keleş'in amfi vurguları, Kurul 1 altın spotları ve klinik karar ağacı",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-pat-029"],
        "keywords": ["altın spotlar", "kurul 1", "patoloji özeti", "hikmet keleş"],
        "lead": "Hücre içi ve dışı birikimler, organizmanın metabolik stresini ve genetik defektlerini yansıtan en değerli patolojik pencerelerdir.",
        "spotPearls": [
            "LİPİD: Steatoz trigliserid birikimidir (en sık karaciğer); Aterosklerozda köpük hücreleri kolesterol esterleri taşır.",
            "PROTEİN: Nefrotik tübüllerde protein damlacıkları reversibldir; Plazma hücresinde RER'de Russell cisimcikleri; Alfa-1 antitripsinde PAS(+) diyastaz-dirençli globüller.",
            "PİGMENT: Hemosiderin Prusya mavisi ile PARLAK MAVİ boyanır; Lipofuksin yaşlanma ve serbest radikal hasarını gösterir.",
            "KALSİFİKASYON: Distrofikte serum kalsiyumu normal ve doku ölüdür (aterom, tüberküloz); Metastatikte serum kalsiyumu yüksek ve doku normaldir (hiperparatiroidi, sarkoidoz)."
        ],
        "keyBullets": [
            {"title": "Dört Mekanizma Çerçevesi", "desc": "Uzaklaştırma kusuru, anormal protein, eksojen madde ve lizozomal defekt tüm birikimlerin temelidir."},
            {"title": "Hekimlik Yaklaşımı", "desc": "Patolog biyopsideki birikimi tanıdığında hastanın sistemik hastalığı (diyabet, alkol, sarkoidoz, miyelom) aydınlatılır."},
            {"title": "Kurul 1 Sınav Başarısı", "desc": "Boyanma özellikleri (PAS-diyastaz, Prusya mavisi) ve kalsifikasyon ayrımları fakülte sınavının temel omurgasını oluşturur."}
        ],
        "flashcards": [
            {
                "id": "fc-ia-47",
                "question": "Kurul 1 Patoloji sınavı için hücre içi birikimlerde 4 temel boya-madde eşleştirmesi nedir?",
                "answer": "1) Glikojen = PAS pozitif (diyastazla sindirilir), 2) Alfa-1 antitripsin = PAS pozitif diyastaz-dirençli, 3) Hemosiderin = Prusya mavisi pozitif, 4) Lipid = Oil Red O / Sudan boyaları.",
                "hint": "Dört kritik histokimya boyası."
            },
            {
                "id": "fc-ia-48",
                "question": "Aterom plağındaki kalsifikasyon neden metastatik kalsifikasyon nedenleri arasında sayılamaz?",
                "answer": "Çünkü aterom plağındaki kalsifikasyon sistemik hiperkalsemiye değil, plaktaki lokal doku nekrozuna bağlı gelişen DİSTROFİK bir kalsifikasyondur.",
                "hint": "Lokal nekroz vs sistemik hiperkalsemi."
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
        
        core_content = {
            "keyBullets": s_raw.get('keyBullets', [])
        }
        if "table" in s_raw:
            core_content["table"] = s_raw["table"]

        target_ids = s_raw.get('target_ids', [])
        keywords = s_raw.get('keywords', [])
        matched_qs = find_matched_questions(target_ids=target_ids, keywords=keywords, max_count=2)
        total_questions += len(matched_qs)

        title_clean = s_raw['title']
        ai_prompts = [
            f"Prof. Dr. Hikmet Keleş'in ders anlatımında '{title_clean}' konusundaki en kritik sınav vurguları nelerdir?",
            f"Robbins Temel Patoloji 11. Baskı ilkelerine göre '{title_clean}' patofizyolojisini ve moleküler mekanizmalarını açıklar mısın?",
            f"Bu slayttaki birikim veya kalsifikasyon paterninin ayırıcı tanısında kullanılan özel histokimyasal boyalar nelerdir?"
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
        "id": "learn-intraseluler-birikimler",
        "title": "İntraselüler Birikimler ve Patolojik Kalsifikasyonlar",
        "shortTitle": "Hücre İçi Birikimler & Kalsifikasyon",
        "discipline": "Tıbbi Patoloji",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Prof. Dr. Hikmet Keleş",
        "sourceFile": "5) Hücre İçi Birikimler ve Kalsifikasyonlar.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "amber",
        "overview": "Dönem 3 Kurul 1 Tıbbi Patoloji müfredatında yer alan Hücre İçi Birikimler ve Patolojik Kalsifikasyonlar dersinin Robbins & Kumar Basic Pathology 11. Baskı temelinde hazırlanmış %500 derinlikte kapsamlı interaktif öğrenim sunumu. Steatoz, kolesterol birikimleri, hiyalin damlalar, Russell cisimcikleri, yanlış katlanmış proteinler (α1-antitripsin), glikojenozlar, antrakosis, lipofuksin, melanin, hemosiderin, distrofik ve metastatik kalsifikasyon mekanizmalarını, 5 adet karşılaştırma tablosunu, 48 adet 3D akıl kartını ve fakülte çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "Hücre içi birikimlerin 4 temel mekanizması: Yetersiz uzaklaştırma, anormal protein birikimi, eksojen madde ve lizozomal yıkım bozukluğu.",
            "Steatoz parankim hücrelerinde trigliserid birikimidir; kwashiorkorda apoprotein sentez azlığı nedeniyle VLDL paketlenemez.",
            "Böbrek proksimal tübül epitelindeki protein reabsorpsiyon damlacıkları nefrotik sendromda görülür ve tamamen reversibldir.",
            "Plazma hücrelerinin granüllü ER'sinde biriken immünoglobulinlere Russell cisimciği; çekirdeğe invagine olursa Dutcher cisimciği denir.",
            "α1-antitripsin eksikliğinde mutant Z proteini karaciğerde birikerek siroz yapar; kanda eksikliği akciğerde panasinüs amfizemine yol açar (PAS pozitif diyastaz-dirençli).",
            "Mallory-Denk cisimcikleri alkolik hepatitte sitokeratin ara filamanları ve ubikuitinden oluşur.",
            "Hemosiderin Prusya mavisi (Perls) ile maviye boyanır; Lipofuksin ve melanin boyanmaz.",
            "Lipofuksin lipid peroksidasyon artığı aşınma pigmentidir; yaşlı kalpte ve karaciğerde esmer atrofi oluşturur.",
            "Distrofik kalsifikasyonda serum kalsiyumu NORMALDİR, hasarlı/ölü dokuya çöker (ateroskleroz, kazeöz nekroz, kalsifik aort darlığı).",
            "Metastatik kalsifikasyonda serum kalsiyumu YÜKSEKTİR (Hiperkalsemi), normal dokulara (özellikle mide, akciğer, böbrek) çöker; nedenleri hiperparatiroidi, sarkoidoz, kemik metastazları ve KBY'dir."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for İntraselüler Birikimler ve Kalsifikasyonlar...")
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

    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
            queue = json.load(f)
        for item in queue:
            if item.get('id') == deck['id']:
                item['status'] = 'completed'
                item['slidesCount'] = len(deck['slides'])
                item['detailLevel'] = '500%'
            elif item.get('id') == 'learn-dismorfoloji-terminolojisi':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: İntraselüler Birikimler completed, Dismorfoloji next!")

    print("Success! Intracellular accumulations deck generation completed.")

if __name__ == '__main__':
    main()
