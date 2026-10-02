#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_cell_injury_deck.py
Generates the deep (%500 detail) 24-slide learning deck for:
"Hücre Hasarı, Hücre Ölümü ve Nekroz" (Tıbbi Patoloji - Prof. Dr. Hikmet Keleş)
Incorporating 24 slides, 48 3D flashcards, 6 comparison tables, and 30+ past exam questions.
"""

import json
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

DECKS_PATH = os.path.join('src', 'data', 'interactive_learning_decks.json')
META_PATH = os.path.join('src', 'data', 'learning_decks_meta.json')
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
                    'explanation': q.get('explanation') or 'Bu soru Kurul 1 Patoloji müfredatında yer alan hücre hasarı ve nekroz mekanizmalarıyla doğrudan ilişkilidir.'
                })
                if len(matched) >= max_count:
                    break
    return matched

# Definitions of all 24 slides
SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Hücre Hasarı Kavramı ve Homeostazın Bozulması",
        "subtitle": "Hücrenin fizyolojik dengeyi koruyamadığı patolojik süreçler ve sonuçları",
        "badge": "Patoloji Temelleri",
        "badgeColor": "indigo",
        "keywords": ["hücre hasarı", "homeostaz", "reversibl"],
        "lead": "Hücre hasarı; hücrenin fizyolojik adaptasyon kapasitesini aşan stres veya zararlı uyaranlara maruz kaldığında normal homeostazını sürdürememesi halidir.",
        "spotPearls": [
            "Normal hücre fizyolojik sınırlar içinde homeostaz durumundadır; stres adaptasyona, zararlı uyaran ise hücre hasarına yol açar.",
            "Hasarın geri dönüşümlü (reversibl) veya geri dönüşümsüz (irreversibl) olması; uyaranın şiddetine, süresine ve hücrenin tipine bağlıdır."
        ],
        "keyBullets": [
            {"title": "Homeostazın Çöküşü", "desc": "Hücreler metabolik ve yapısal gereksinimlerini dar bir fizyolojik aralıkta dengeler. Bu dengenin bozulması biyokimyasal disfonksiyon başlatır."},
            {"title": "Zararlı Etken ve Yanıt Dinamiği", "desc": "Hafif ve geçici hasarlar geri dönüşümlüyken; şiddetli, ısrarlı veya ani gelişen stres doğrudan hücre ölümüne (nekroz veya apoptoz) götürür."},
            {"title": "Patofizyolojik Sonuç", "desc": "Fonksiyon kaybı morfolojik değişikliklerden çok önce başlar; ışık mikroskobik bulgular biyokimyasal çöküşten saatler sonra ortaya çıkar."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-1",
                "question": "Hücre hasarı geliştiğinde fonksiyon kaybı mı yoksa morfolojik yapısal bozulma mı önce ortaya çıkar?",
                "answer": "Fonksiyon kaybı çok daha önce ortaya çıkar! Işık mikroskobunda morfolojik nekroz bulgularının belirmesi için saatler (örneğin miyokard enfarktüsünde 4-12 saat) gerekirken, biyokimyasal disfonksiyon saniyeler içinde başlar.",
                "hint": "Enfarkt sonrası ilk 1 saatte mikroskopta hücreler normal görünebilir!"
            },
            {
                "id": "fc-chi-2",
                "question": "Hücrenin zararlı bir uyarana karşı geliştirebileceği 3 ana yanıt yolu nedir?",
                "answer": "1) Adaptasyon (uyaran hafif/kronik ise), 2) Geri Dönüşümlü Hücre Hasarı (akut hafif-orta hasar), 3) Hücre Ölümü (şiddetli veya kalıcı hasarda nekroz veya apoptoz).",
                "hint": "Stresin şiddeti yanıtın yönünü belirler."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Stres ve Zararlı Uyaranlara Hücresel Yanıt Aşamaları",
        "subtitle": "Adaptasyon, reversibl hasar ve hücre ölümü spektrumu",
        "badge": "Hücresel Yanıt",
        "badgeColor": "indigo",
        "keywords": ["adaptasyon", "hipertrofi", "hasar", "ölüm"],
        "lead": "Hücreye uygulanan stresin doğası ve hücresel rezerv, sürecin adaptasyonla mı atlatılacağını yoksa fatal hücre hasarıyla mı sonlanacağını belirler.",
        "spotPearls": [
            "Fizyolojik stres durumunda hücre öncelikle hipertrofi, hiperplazi, atrofi veya metaplazi ile adapte olmaya çalışır.",
            "Adaptasyon kapasitesi aşıldığında veya uyaran bizzat zararlı/toksik olduğunda hücre hasarı kaçınılmazdır."
        ],
        "keyBullets": [
            {"title": "Adaptif Yanıtlar", "desc": "Bölünmeyen hücreler (kalp kası) hipertrofi ile, bölünebilen dokular (karaciğer, kemik iliği) hiperplazi ile iş yükü artışına yanıt verir."},
            {"title": "Kritik Eşik Noktası", "desc": "Stres kaldırıldığında geri dönebilen aşama 'Reversibl Hasar'dır. Belirli bir biyokimyasal eşik aşıldığında hasar geri dönüşümsüzleşir."},
            {"title": "Ölüm Yolu Ayrımı", "desc": "İrreversibl hasara uğrayan hücre enerji kaybı ve membran parçalanmasıyla 'Nekroz'a veya programlı olarak 'Apoptoz'a ilerler."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-3",
                "question": "Miyokard hücreleri artan tansiyon (iş yükü) karşısında neden hiperplazi değil hipertrofi geliştirir?",
                "answer": "Çünkü erişkin kardiyomiyositler kalıcı (bölünmeyen) hücrelerdir; hücre sayısını artıramazlar (hiperplazi yapamazlar), ancak protein sentezleyerek hücre hacmini büyütürler (hipertrofi).",
                "hint": "Bölünme yeteneği olmayan dokularda tek çare büyümektir."
            },
            {
                "id": "fc-chi-4",
                "question": "Reversibl hasar ile İrreversibl hasar arasındaki temel biyolojik sınır nedir?",
                "answer": "Uyaran ortadan kaldırıldığında hücrenin normal yapı ve fonksiyonuna dönebilme yeteneğidir. Membran bütünlüğü ve ATP üretim kapasitesi korunuyorsa hasar reversibldir.",
                "hint": "Geri dönebilirlik membran ve mitokondriye bağlıdır."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Hücre Hasarının Başlıca Nedenleri: Hipoksi ve İskemi",
        "subtitle": "Oksijen yetersizliği ve arteryel perfüzyon kaybının hücresel yansımaları",
        "badge": "Etyopatogenez",
        "badgeColor": "rose",
        "keywords": ["hipoksi", "iskemi", "oksijen", "perfüzyon"],
        "lead": "Hipoksi (oksijen azlığı) ve iskemi (kan akımı kesintisi), insan patolojisinde hücre hasarı ve nekrozun en sık görülen nedenleridir.",
        "spotPearls": [
            "İSKEMİ, HİPOKSİDEN DAHA HIZLI VE AĞIR HASAR VERİR; çünkü sadece oksijeni değil, glukozu da keser ve metabolitlerin (laktik asit) uzaklaştırılmasını engeller.",
            "Hipoksinin en sık nedeni arteriyel tromboz veya emboliye ikincil gelişen iskemidir; ancak anemi veya CO zehirlenmesinde kan akımı normalken hipoksi gelişir."
        ],
        "keyBullets": [
            {"title": "Hipoksi Tanımı ve Tipleri", "desc": "Dokuda oksijen basıncının düşmesidir. Nedenleri: İskemi, solunum yetmezliği, anemi (taşıma kapasitesi kaybı), CO zehirlenmesi ve ağır kan kaybı."},
            {"title": "İskemi: Çifte Darbe", "desc": "Arteryel obstrüksiyon veya venöz göllenme nedeniyle dokuya arteryel kan perfüzyonunun durmasıdır. Glikoliz için gereken glukoz desteği de kesilir."},
            {"title": "Metabolit Akümülasyonu", "desc": "İskemide glikolitik son ürünler ve asit atılamaz, doku hızla asidoza girer; bu da iskemiyi saf hipoksiden çok daha yıkıcı kılar."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-5",
                "question": "İskemi ile hipoksi arasındaki en temel fark nedir ve hangisi dokuya daha hızlı zarar verir?",
                "answer": "İskemi dokuya çok daha hızlı ve şiddetli zarar verir! Hipokside kan akımı devam ettiği için glukoz taşınabilir ve metabolitler yıkanabilir. İskemide ise kan akımı durduğu için glukoz verilemez ve toksik asidik atıklar dokuda birikir.",
                "hint": "İskemi = Kan akımının kesilmesi; Hipoksi = Sadece oksijenin azalması."
            },
            {
                "id": "fc-chi-6",
                "question": "Karbonmonoksit (CO) zehirlenmesinde dokuda iskemi mi yoksa hipoksi mi gelişir?",
                "answer": "Hipoksi gelişir! Kan akımı ve damar perfüzyonu açıktır (iskemi yoktur); ancak hemoglobinin oksijen bağlama ve dokuya bırakma kapasitesi felç olduğu için dokular oksijensiz kalır (anoksik/hipoksik hipoksi).",
                "hint": "Damar tıkalı değil, taşıyıcı hemoglobin bloke!"
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Toksinler, Kimyasallar ve Çevresel Hasar Faktörleri",
        "subtitle": "Doğrudan sitotoksisite ve metabolik ara ürünlerle gelişen hasar",
        "badge": "Toksik Hasar",
        "badgeColor": "amber",
        "keywords": ["toksin", "parasetamol", "cıva", "sitotoksisite"],
        "lead": "Kimyasal maddeler ve toksinler; ya doğrudan membran bileşenleriyle reaksiyona girerek ya da sitokrom P450 ile toksik metabolitlere dönüşerek hücreyi zedeler.",
        "spotPearls": [
            "Cıva klorür hücre membranındaki sülfhidril gruplarına doğrudan bağlanarak akut tübüler nekroza yol açar.",
            "Parasetamol ve Karbontetraklorür (CCl4) ise karaciğerde sitokrom P450 ile toksik serbest radikallere (NAPQI, CCl3•) dönüşerek indirekt hasar üretir."
        ],
        "keyBullets": [
            {"title": "Doğrudan Etkili Toksinler", "desc": "Hücrenin kritik moleküllerine doğrudan bağlanırlar. Ağır metaller (cıva, kurşun) membran ATPaz enzimlerini ve sülfhidril gruplarını bloke eder."},
            {"title": "Metabolik Aktivasyonla Etki", "desc": "Bizzat kendileri toksik olmayan maddeler, karaciğerde P-450 monooksijenazlarca reaktif serbest radikallere dönüştürülerek lipid peroksidasyonu yapar."},
            {"title": "Klinik Örnek: Parasetamol Nekrozu", "desc": "Aşırı dozda glutatyon depoları tükenir; toksik metabolit NAPQI hepatosit makromoleküllerine kovalent bağlanarak santrilobüler masif nekroz oluşturur."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-7",
                "question": "Parasetamol toksisitesinde hepatosit nekrozuna yol açan reaktif toksik ara ürünün adı nedir?",
                "answer": "NAPQI (N-asetil-p-benzokinon imin). Normalde glutatyon ile nötralize edilir; glutatyon tükendiğinde hepatosit proteinlerine bağlanarak masif karaciğer nekrozuna neden olur.",
                "hint": "Antidotu glutatyon öncülü olan N-Asetilsistein (NAC)'dir."
            },
            {
                "id": "fc-chi-8",
                "question": "Doğrudan sitotoksik hasar ile metabolik dönüşüm gerektiren hasar arasındaki farka birer örnek veriniz.",
                "answer": "Doğrudan hasar: Cıva klorür (sülfhidril gruplarını bağlar). Metabolik dönüşüm: Karbontetraklorür (CCl4 -> CCl3• radikaline dönüşerek lipid peroksidasyonu yapar).",
                "hint": "Biri hemen bağlar, diğeri P-450 enzimleriyle radikale dönüşür."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Enfeksiyöz, İmmünolojik, Genetik ve Beslenme Dengesizlikleri",
        "subtitle": "Biyolojik ajanlardan otoimmüniteye ve metabolik eksikliklere hasar nedenleri",
        "badge": "Etyolojik Spektrum",
        "badgeColor": "blue",
        "keywords": ["enfeksiyon", "otoimmün", "genetik", "beslenme"],
        "lead": "Submikroskopik virüslerden metazoan parazitlere kadar tüm patojenler ile konağın kendi immün sistemi hücre hasarının önde gelen nedenlerindendir.",
        "spotPearls": [
            "İmmünolojik reaksiyonlar koruyucu olmakla birlikte; otoimmün hastalıklarda (SLE, RA) ve alerjilerde bizzat hücre yıkımının ana kaynağıdır.",
            "Genetik anomaliler tek bir baz mutasyonuyla (Orak Hücreli Anemi) ölümcül hasar yaratabileceği gibi, enzim defektleriyle (Lizozomal depo hastalıkları) hücreyi toksik yüke boğabilir."
        ],
        "keyBullets": [
            {"title": "Enfeksiyöz Patojenler", "desc": "Virüsler hücre içi replikasyon ve sitolizle; bakteriler endotoksin/ekzotoksinlerle; mantar ve parazitler mekanik ve doku destrüksiyonuyla hasar verir."},
            {"title": "İmmünolojik Hasar", "desc": "Antikor ve kompleman aracılı hücre lizisi veya sitotoksik T lenfositlerin perforin/granzim deşarjı hedef hücrede membran delinmesi ve apoptoz yapar."},
            {"title": "Beslenme Dengesizlikleri", "desc": "Protein-kalori malnütrisyonu (Kwashiorkor, Marasmus), avitaminozlar veya tam tersine aşırı beslenme (Obezite, Ateroskleroz ve Tip 2 Diyabet)."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-9",
                "question": "Orak hücreli anemide tek bir nükleotid mutasyonu nasıl hücre hasarına ve doku nekrozuna yol açar?",
                "answer": "Beta-globin zincirinde glutamik asit yerine valin geçmesi (HbS), deoksijene durumda polimerizasyona ve eritrositlerin oraklaşmasına yol açar. Oraklaşan hücreler mikrodolaşımı tıkayarak iskemik enfarktlar ve doku nekrozu üretir.",
                "hint": "Genetik anormallik -> mikrovasküler oklüzyon -> iskemi."
            },
            {
                "id": "fc-chi-10",
                "question": "Aşırı beslenme hücresel düzeyde hangi patolojiler üzerinden doku zedelenmesine yol açar?",
                "answer": "Lipid fazlalığı arter duvarında aterosklerotik plaklara (iskemi kaynağı) ve hepatositlerde yağlanmaya (steatohepatit) yol açar. Ayrıca insülin direnci üzerinden endotel hasarı geliştirir.",
                "hint": "Sadece açlık değil, aşırılık da hücre hasarı nedenidir."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Hücre Hasarında Genel Prensipler ve Duyarlılık Faktörleri",
        "subtitle": "Uyaran tipi, süresi, şiddeti ile hücrenin metabolik ve genetik yapısının etkileşimi",
        "badge": "Patolojik İlkeler",
        "badgeColor": "indigo",
        "keywords": ["duyarlılık", "iskemi süresi", "nöron", "fibroblast"],
        "lead": "Hücresel yanıt; zedeleyici etkenin tipine, süresine ve şiddetine bağlı olduğu kadar, hedef hücrenin metabolik durumuna ve genetik donanımına da sıkı sıkıya bağlıdır.",
        "spotPearls": [
            "İSKEMİYE EN DUYARLI HÜCRELER: Beyin kortikal nöronlarıdır (3-5 dakika içinde irreversibl hasara uğrar).",
            "Miyokard hücreleri 20-30 dakika; iskelet kası ve fibroblastlar ise saatlerce iskemiye dayanabilir."
        ],
        "keyBullets": [
            {"title": "Uyaranın Özellikleri", "desc": "Düşük doz kimyasal veya kısa süreli iskemi reversibl hasar yaparken; yüksek doz veya uzamış süre nekroza yol açar."},
            {"title": "Hücre Tipi ve Metabolik İhtiyaç", "desc": "Yüksek oksijen tüketen ve glikolitik kapasitesi düşük hücreler (nöronlar, kardiyomiyositler) iskemiye en dayanıksız hücrelerdir."},
            {"title": "Genetik Polimorfizmler", "desc": "Sitokrom P450 genetik varyantları, aynı dozdaki bir toksinin farklı bireylerde çok farklı derecelerde hasar oluşturmasına neden olur."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-11",
                "question": "Tam arteryel iskemi durumunda beyin korteks nöronları ile kalp kası hücrelerinin geri dönüşümsüz hasar eşikleri ne kadardır?",
                "answer": "Kortikal nöronlar: 3 - 5 dakika! Kalp kası hücreleri: 20 - 30 dakika! Bu süreler aşıldığında perfüzyon tekrar sağlansa dahi hücre ölümü engellenemez.",
                "hint": "Beyin dakikalar içinde, kalp ise yarım saatte irreversibl sınıra varır."
            },
            {
                "id": "fc-chi-12",
                "question": "Aynı toksine maruz kalan iki insanda hasar derecesinin farklı olmasını açıklayan en önemli hücresel faktör nedir?",
                "answer": "Sitokrom P-450 enzim sistemindeki genetik polimorfizmlerdir. Hızlı metabolize edicilerde toksik ara ürün hızla birikerek ağır hasar yaratırken, yavaş olanlarda tablo daha hafif seyredebilir.",
                "hint": "Genetik zemin hedef hücrenin direncini ve toksin metabolizmasını tayin eder."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Hücresel Hasarın Temel Biyokimyasal ve Organel Hedefleri",
        "subtitle": "Mitokondri, plazma membranı, protein sentezi ve genetik materyal zinciri",
        "badge": "Hücresel Hedefler",
        "badgeColor": "violet",
        "keywords": ["mitokondri", "membran", "dna", "atp"],
        "lead": "Çeşitli zararlı etkenler hücrede dağınık hasar vermez; başlıca dört kritik hücre içi sistemi ve organeli hedef alır.",
        "spotPearls": [
            "Hücre hasarının 4 kritik hedefi: 1) Mitokondri (ATP üretimi), 2) Hücre zarları (iyon dengesi), 3) Protein sentezi (ribozom/ER), 4) Genetik aygıt (DNA).",
            "Hangi nedenle başlarsa başlasın; intraselüler Kalsiyum artışı proteaz, endonükleaz ve fosfolipazları aktive ederek hücreyi intihara sürükler."
        ],
        "keyBullets": [
            {"title": "Mitokondri ve ATP Üretimi", "desc": "Hücrenin enerji santralidir. Oksidatif fosforilasyonun çökmesi tüm hücresel fonksiyonları kaskat şeklinde durdurur."},
            {"title": "Hücre Zarlarının Bütünlüğü", "desc": "Plazma zarı hücre içi iyon dengesini; lizozom zarı ise sindirici asit hidrolazların sitoplazmaya dökülmesini önler."},
            {"title": "Protein Sentez Mekanizması", "desc": "Granüllü endoplazmik retikulumdan ribozomların dökülmesi yapısal ve enzimatik protein üretimini kilitler."},
            {"title": "Genomik Bütünlük (DNA)", "desc": "Onarılamaz DNA hasarı p53 aracılı apoptoz yolağını aktive ederek hücreyi kontrollü ölüme yönlendirir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-13",
                "question": "Hücre zedelenmesinde sitozolik serbest Kalsiyum (Ca2+) artışının ölümcül olmasının nedeni nedir?",
                "answer": "Yüksek kalsiyum 4 yıkıcı enzimi aktive eder: 1) Fosfolipazlar (membranı parçalar), 2) Proteazlar (hücre iskeletini yıkar), 3) Endonükleazlar (DNA'yı kırar), 4) ATPazlar (kalan ATP'yi tüketir).",
                "hint": "Kalsiyum hücre içinde tehlikeli bir intihar tetiğidir!"
            },
            {
                "id": "fc-chi-14",
                "question": "Hücre hasarında lizozom membranının yırtılması ne ile sonuçlanır?",
                "answer": "Asit hidrolazların (asit fosfataz, ribonükleaz, DNAaz, proteazlar) sitoplazmaya kaçması ve hücresel bileşenlerin otolitik olarak sindirilmesiyle (nekroz) sonuçlanır.",
                "hint": "Lizozom patlaması hücrenin kendi kendini sindirmesidir (otoliz)."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "İskemik Hasar Patogenezi: ATP Çöküşü ve İyon Dengesi",
        "subtitle": "Glikoliz, asidoz, Na+/K+ pompa yetmezliği ve hidropik göllenme",
        "badge": "İskemik Kaskat",
        "badgeColor": "red",
        "keywords": ["atp", "glikoliz", "asidoz", "pompa"],
        "lead": "İskemi başladığında mitokondriyal elektron taşıma zinciri durur; saniyeler içinde ATP tükenerek hücre içi iyonik ve metabolik kaos başlar.",
        "spotPearls": [
            "ATP düşüşü plazma membranındaki Na+/K+ ATPaz pompasını durdurur: Hücre içine Na+ ve SU girer, K+ dışarı kaçar -> HÜCRESEL ŞİŞME gelişir.",
            "Kompansatris anaerobik glikoliz glikojen depolarını tüketir ve laktik asit biriktirir: pH düşer (intraselüler asidoz) ve nükleer kromatin kümeleşir."
        ],
        "keyBullets": [
            {"title": "Oksidatif Fosforilasyon Kaybı", "desc": "Oksijen yokluğunda ATP sentaz durur. Enerjiye bağımlı tüm hücresel pompalar ve sentez reaksiyonları bloke olur."},
            {"title": "Anaerobik Glikoliz ve Asidoz", "desc": "Hücre hayatta kalmak için anaerobik yolağa geçer. Glikojen hızla biter, laktat üretimi hücre içi pH'yı asidik seviyeye çeker."},
            {"title": "Ribozomların Ayrılması", "desc": "ATP tükenmesi ve sitoplazmik şişme granüllü ER'nin genişlemesine ve ribozomların ER membranından kopmasına yol açar; protein sentezi durur."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-15",
                "question": "İskemik hücrede hücre içinin şişmesine ve suyla dolmasına yol açan primer biyokimyasal bozukluk nedir?",
                "answer": "ATP yetersizliğine bağlı olarak plazma membranındaki Na+/K+ ATPaz pompasının çalışmamasıdır. Sodyum hücre dışına pompalanamaz, hücre içinde birikir; osmoz kuralları gereği su sodyumu takip ederek hücreyi şişirir.",
                "hint": "Tuz nereye, su oraya: Na+ içerde kalırsa hücre balonlaşır."
            },
            {
                "id": "fc-chi-16",
                "question": "İskeminin erken evresinde nükleer kromatinin erken kümeleşmesine (clumping) ne sebep olur?",
                "answer": "Anaerobik glikoliz sonucu laktik asit ve inorganik fosfat birikimiyle hücre içi pH'nın düşmesi (intraselüler asidoz).",
                "hint": "Asidik ortam nükleer proteinleri çökeltir."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Geri Dönüşümlü (Reversibl) Hücre Hasarı Tanımı ve Sınırları",
        "subtitle": "Zararlı etken ortadan kalktığında hücrenin homeostazı yeniden kazanabilme evresi",
        "badge": "Reversibl Evre",
        "badgeColor": "sky",
        "keywords": ["reversibl", "hidropik", "yağlanma"],
        "lead": "Geri dönüşümlü hasar; hücrede morfolojik ve fonksiyonel anormallikler bulunmasına rağmen, uyaran sonlandırıldığında tamamen iyileşebilen aşamadır.",
        "spotPearls": [
            "Geri dönüşümlü hücre hasarının ışık mikroskobunda tanınan 2 temel morfolojik kalıbı vardır: 1) HÜCRESEL ŞİŞME (Hidropik Değişim), 2) YAĞLANMA (Steatoz).",
            "Reversibl evrede plazma zarı ve organel zarları kabarmış olsa da BÜTÜNLÜĞÜ KORUNMUŞTUR; hücre dışına enzim sızıntısı olmaz."
        ],
        "keyBullets": [
            {"title": "Biyolojik Çerçeve", "desc": "Mitokondriyal oksidatif fosforilasyon kapasitesi kalıcı olarak ölmemiştir. Oksijen verildiğinde ATP üretimi yeniden başlar."},
            {"title": "Hücresel Şişme (Bulanık Şişme)", "desc": "Neredeyse tüm hasar tiplerinde İLK ortaya çıkan bulgudur. İyon ve sıvı dengesinin bozulması sonucu gelişir."},
            {"title": "Yağlanma (Lipid Vakuolleri)", "desc": "Özellikle yağ metabolizmasında aktif olan karaciğer ve miyokard hücrelerinde toksik veya hipoksik hasarda görülür."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-17",
                "question": "Işık mikroskobunda reversibl hasarın en erken ve neredeyse evrensel ilk göstergesi nedir?",
                "answer": "Hücresel Şişme (Hidropik Değişim / Bulanık Şişme / Vakuoler Dejenerasyon). Hücre membran pompalarının yetersizliğine bağlı olarak suyla dolmasıdır.",
                "hint": "Hücre zedelendiğinde ilk olarak su toplar."
            },
            {
                "id": "fc-chi-18",
                "question": "Reversibl hasar evresinde kanda troponin veya karaciğer transaminazları (AST/ALT) yükselir mi?",
                "answer": "HAYIR! Çünkü reversibl evrede plazma membran bütünlüğü bozulmamıştır; makromoleküller ve enzimler hücre dışına sızamaz. Bu enzimlerin kanda yükselmesi İRREVERSİBL membran parçalanmasını (nekrozu) gösterir.",
                "hint": "Enzim kaçağı = Membran yırtılması = Nekroz!"
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Hücresel Şişme (Hidropik Değişim): Makroskopi ve Mikroskopi",
        "subtitle": "Solukluk, turgor artışı, vakuolizasyon ve bulanık şişme",
        "badge": "Morfoloji",
        "badgeColor": "sky",
        "keywords": ["hidropik", "turgor", "vakuol", "solukluk"],
        "lead": "Hücresel şişme; organ düzeyinde solukluk ve ağırlık artışına, mikroskopik düzeyde ise sitoplazmik berrak vakuollere yol açar.",
        "spotPearls": [
            "Makroskopik olarak organ: Büyümüştür, ağırlığı artmıştır, turgoru artmıştır ve kapillerlerin sıkışması nedeniyle SOLUKTUR.",
            "Mikroskopik olarak sitoplazmada berrak vakuoller görülür; bu vakuoller şişmiş ve kopmuş Endoplazmik Retikulum parçalarıdır (Hidropik Dejenerasyon)."
        ],
        "keyBullets": [
            {"title": "Makroskopik Bulgular", "desc": "Bir organdaki (böbrek, karaciğer) tüm hücreler şiştiğinde organ gerginleşir, kesit yüzeyi dışarı taşar ve soluk bir görünüm alır."},
            {"title": "Mikroskopik Görünüm", "desc": "Hücre sınırları belirsizleşir, sitoplazma soluklaşır ve ince pembe granüler bir hal alır (Bulanık Şişme)."},
            {"title": "Ultrastrüktürel Değişiklikler", "desc": "Elektron mikroskobunda mikrovillusların silinmesi, plazma membranında kabarcıklar (blebs) ve mitokondriyal hafif şişme izlenir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-19",
                "question": "Akut tübüler hasarlı bir böbreğin makroskopik kesitinde izlenen solukluk ve ağırlık artışının patolojik temeli nedir?",
                "answer": "Toplu hücresel şişmedir (hidropik dejenerasyon). Şişen tübül epitel hücreleri parankim içi kapillerleri dıştan basıya uğratarak kan akımını azaltır ve organı soluklaştırır.",
                "hint": "Hücreler şişip çevre kapillerleri ezer."
            },
            {
                "id": "fc-chi-20",
                "question": "Işık mikroskobunda hidropik değişim gösteren hücrenin sitoplazmasındaki mikro-vakuollerin kaynağı hangi organeldir?",
                "answer": "Genişlemiş ve lümenine su dolmuş Endoplazmik Retikulum (ER) kesecikleridir.",
                "hint": "Suyu toplayıp vakuol oluşturan zarlı ağ yapısı."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Yağlanma (Steatoz / Yağlı Dejenerasyon) Patolojisi",
        "subtitle": "Trigliseridlerin sitoplazmik vakuollerde birikimi ve etyolojik nedenleri",
        "badge": "Metabolik Hasar",
        "badgeColor": "amber",
        "keywords": ["steatoz", "yağlanma", "karaciğer", "trigliserid"],
        "lead": "Yağlanma (steatoz); yağ metabolizmasıyla uğraşan parankim hücrelerinde trigliseridlerin anormal birikimiyle karakterize reversibl hasar formudur.",
        "spotPearls": [
            "En sık KARACİĞERDE görülür; ayrıca miyokard, böbrek ve iskelet kasında da izlenebilir.",
            "Gelişmiş ülkelerde karaciğer steatozunun en sık nedenleri: ALKOL KÖTÜYE KULLANIMI, OBEZİTE ve DİYABET (Metabolik Disfonksiyon İlişkili Karaciğer Hastalığı - MASLD)."
        ],
        "keyBullets": [
            {"title": "Patogenetik Mekanizma", "desc": "Serbest yağ asidi girişinde artış, yağ asidi oksidasyonunda azalma veya apoprotein sentez yetersizliği (VLDL olarak atılamama)."},
            {"title": "Morfolojik Görünüm", "desc": "Erken dönemde mikroveziküler lipid damlacıkları; ilerledikçe birleşerek çekirdeği kenara iten makroveziküler büyük yağ kistleri oluşturur."},
            {"title": "Geri Dönüş Potansiyeli", "desc": "Etken kaldırıldığında (alkolün kesilmesi, kilo kaybı) lipidler hücreden temizlenir ve karaciğer parankimi tamamen normale döner."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-21",
                "question": "Protein malnütrisyonunda (Kwashiorkor) karaciğerde neden şiddetli yağlanma (steatoz) gelişir?",
                "answer": "Çünkü trigliseridlerin karaciğerden VLDL formunda kana salınabilmesi için APOPROTEİN sentezi şarttır. Protein eksikliğinde apoprotein üretilemez; yağ asitleri karaciğerde hapsolur ve steatoz oluşur.",
                "hint": "Paketleyecek protein yoksa yağ dışarı çıkamaz!"
            },
            {
                "id": "fc-chi-22",
                "question": "Kronik hipokside kalp kasında oluşan yağlanmanın tipik makroskopik görüntüsü nasıldır?",
                "answer": "'Kaplan Postu Kalp' (Tigered heart / Cor tigrinum). Endokard altında sarı yağlı şeritler ile kırmızı normal miyokardın ardışık alacalı çizgilenmesidir.",
                "hint": "Sarı-kırmızı alacalı post deseni."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Reversibl Hasarın Ultrastrüktürel ve Membran Bulguları",
        "subtitle": "Blebbing, miyelin figürler, mikrovillus kaybı ve nükleer durum",
        "badge": "Elektron Mikroskopi",
        "badgeColor": "violet",
        "keywords": ["bleb", "miyelin figür", "mikrovillus", "ultrastrüktür"],
        "lead": "Elektron mikroskobu, ışık mikroskobunda fark edilemeyen ince membran deformasyonlarını ve organel şişmelerini reversibl evrede net olarak yakalar.",
        "spotPearls": [
            "Reversibl hasarın elektron mikroskobu bulguları: Plazma membranında tomurcuklanma (blebs), mikrovillusların düzleşmesi ve MİYELİN FİGÜRLER.",
            "Miyelin figürler; hasarlı hücresel zarlardan kaynaklanan fosfolipid kitlelerinin soğan zarı tarzında konsantrik kıvrımlarıdır."
        ],
        "keyBullets": [
            {"title": "Plazma Membran Deformasyonu", "desc": "Hücre iskeletinin gevşemesiyle zar dışarıya doğru kabarcıklar (blebbing) oluşturur; lümen yüzeyindeki mikrovilluslar silinir."},
            {"title": "Mitokondriyal Değişiklikler", "desc": "Mitokondrilerde hafif şişme ve kristalarda düzleşme görülür; ancak irreversibl hasarda görülen amorf dansiteler henüz YOKTUR."},
            {"title": "Nükleer Korunma", "desc": "Çekirdekte hafif kromatin kümeleşmesi dışında nükleer zar intaktır; nükleus parçalanması veya erimesi reversibl evrede kesinlikle görülmez."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-23",
                "question": "Patolojide 'Miyelin Figür' (Myelin Figure) neyi ifade eder ve neden oluşur?",
                "answer": "Hasarlı plazma veya organel membranlarından dökülen fosfolipidlerin sitoplazmada soğan zarı gibi iç içe konsantrik helezonlar oluşturmasıdır. Hem reversibl hasarda hem de nekrozda görülebilir.",
                "hint": "Fosfolipid artıklarının oluşturduğu konsantrik kıvrımlar."
            },
            {
                "id": "fc-chi-24",
                "question": "Reversibl hasarda elektron mikroskobunda mitokondride görülen şişme ile İrreversibl hasardaki mitokondriyal bulgu arasındaki fark nedir?",
                "answer": "Reversibl evrede hafif şişme ve krista aralanması vardır. İrreversibl evrede ise mitokondri matriksinde 'AMORF DANSİTELER' (flokülan dansiteler/kalsiyum birikimleri) ve yüksek iletkenlik porları açılır.",
                "hint": "Amorf matriks dansitesi geri dönüşümsüzlüğün damgasıdır."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Geri Dönüşümsüz (İrreversibl) Hasara Geçişin 2 Kritik Eşiği",
        "subtitle": "Kalıcı mitokondriyal hasar ve membran bütünlüğünün iflası (Point of No Return)",
        "badge": "Kritik Eşik",
        "badgeColor": "red",
        "keywords": ["irreversibl", "mitokondriyal hasar", "membran parçalanması", "point of no return"],
        "lead": "Hücrenin ölüm fermanını imzalayan ve geri dönüşü imkansız kılan 'Geri Dönüşü Olmayan Nokta' (Point of No Return) iki temel biyokimyasal olayla tanımlanır.",
        "spotPearls": [
            "İrreversibl hasarın İKİ VAZGEÇİLMEZ DÖNÜM NOKTASI: 1) Kalıcı mitokondriyal disfonksiyon (ATP sentezinin geri dönemez çöküşü), 2) MEMBRAN BÜTÜNLÜĞÜNÜN KAYBI.",
            "Plazma membranının delinmesi hücre içi enzimlerin (Troponin, CK-MB, AST) kana karışmasının ve hücre ölümünün kesin kanıtıdır."
        ],
        "keyBullets": [
            {"title": "1. Mitokondriyal Geçirgenlik Geçiş Poru", "desc": "Mitokondri zarında 'MPTP' porlarının kalıcı olarak açılması membran potansiyelini sıfırlar ve ATP üretimini geri dönüşsüz biçimde bitirir."},
            {"title": "2. Plazma ve Organel Zarlarının Parçalanması", "desc": "Kalsiyumla aktive olan fosfolipazlar lipidleri parçalar, reaktif oksijen radikalleri (ROS) lipid peroksidasyonu yapar; membran kevgire döner."},
            {"title": "Lizozomal Sindirim Başlaması", "desc": "Lizozom zarının delinmesiyle hidrolitik enzimler sitoplazmayı ve nükleusu sindirmeye başlar; otoliz ve heteroliz tetiklenir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-25",
                "question": "Hücre hasarının geri dönüşümsüz (irreversibl) hale geldiğini kanıtlayan en temel iki biyolojik kriter nedir?",
                "answer": "1) Mitokondriyal fonksiyonun kalıcı olarak çökmesi (oksidatif fosforilasyonun ve ATP üretiminin geri dönememesi), 2) Membran bütünlüğünün derin kaybı (plazma ve lizozom zarlarının parçalanması).",
                "hint": "Enerji santrali kalıcı söndü ve dış duvar yıkıldı."
            },
            {
                "id": "fc-chi-26",
                "question": "Akut miyokard enfarktüsünde iskeminin 30. dakikasında kanda neden kardiyak troponin saptanmaya başlar?",
                "answer": "Çünkü 20-30. dakikadan sonra kardiyomiyositlerde membran bütünlüğü parçalanır (irreversibl nekroz başlar) ve intraselüler makromolekül olan troponin dolaşıma sızar.",
                "hint": "Hücre zarı delinmeden büyük proteinler kana geçemez."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Hücre Ölümü Tiplerine Genel Bakış: Nekroz vs Apoptoz",
        "subtitle": "Kaza sonucu kontrolsüz parçalanma ile programlı intiharın temel ayrımı",
        "badge": "Ölüm Tipleri",
        "badgeColor": "red",
        "keywords": ["nekroz", "apoptoz", "enflamasyon", "karşılaştırma"],
        "lead": "Hücre ölümü başlıca iki mekanizmayla gerçekleşir: Şiddetli dış hasarla kontrolsüz parçalanan 'Nekroz' ve hücresel sinyallerle düzenlenen programlı 'Apoptoz'.",
        "spotPearls": [
            "NEKROZ DAİMA PATOLOJİKTİR, membran parçalanır, hücre şişer ve DAİMA ÇEVRESEL ENFLAMASYON EŞLİK EDER.",
            "APOPTOZ FİZYOLOJİK VEYA PATOLOJİK OLABİLİR, membran sağlam kalır (apoptoz cisimcikleri), hücre büzüşür ve ENFLAMASYON GELİŞMEZ."
        ],
        "keyBullets": [
            {"title": "Hücre Boyutu Değişimi", "desc": "Nekrozda iyon pompası iflasıyla hücre şişer ve lizisle patlar. Apoptozda hücre büzüşür (piknotik) ve yoğunlaşır."},
            {"title": "Zar Bütünlüğü ve Dökülme", "desc": "Nekrozda zar parçalanır, sitoplazma içeriği çevreye saçılır. Apoptozda zar intaktır; hücre fagositlerce yutulan membranöz cisimciklere ayrılır."},
            {"title": "Enflamatuvar Yanıt Farkı", "desc": "Nekrozda ortama saçılan hücresel içerik (DAMPs) yoğun lökosit göçü ve akut iltihap başlatır; apoptozda iltihap görülmez."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-27",
                "question": "Nekroz ile apoptoz arasındaki en kritik 3 morfolojik ve klinik fark nedir?",
                "answer": "1) Nekroz daima patolojiktir, apoptoz ise fizyolojik de olabilir. 2) Nekrozda hücre şişer ve zarı parçalanır; apoptozda büzüşür ve zarı intaktır. 3) Nekroz daima yoğun enflamasyon başlatır; apoptozda kesinlikle enflamasyon gelişmez!",
                "hint": "Enflamasyon var mı yok mu? Membran patladı mı intakt mı?"
            },
            {
                "id": "fc-chi-28",
                "question": "Apoptozda hücresel içerik neden çevreye dökülmez ve enflamasyon tetiklemez?",
                "answer": "Çünkü apoptoza giden hücre sitoplazmasını membranla çevrili 'Apoptoz Cisimcikleri' halinde paketler ve yüzeyine fosfatidilserin çıkararak makrofajlar tarafından sessizce fagositoz ettirir.",
                "hint": "Paketli çöp gibi sessizce temizlenir."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Nekrozun Genel Özellikleri ve Enflamasyon Tetiklenmesi",
        "subtitle": "Hücresel otoliz, heteroliz ve DAMP molekülleri aracılı lökosit infiltrasyonu",
        "badge": "Nekroz Biyolojisi",
        "badgeColor": "red",
        "keywords": ["nekroz", "enflamasyon", "damp", "lökosit"],
        "lead": "Nekroz; hücre zarının parçalanması, intraselüler enzimlerin ortama dökülmesi ve bu yıkım ürünlerinin yoğun bir enflamatuvar yanıt uyarmasıyla karakterizedir.",
        "spotPearls": [
            "Nekrotik hücrelerden salınan nükleer proteinler (HMGB1), ATP ve ürik asit 'DAMP' (Hasar İlişkili Moleküler Kalıplar) olarak davranır.",
            "DAMP'lar makrofajlardaki inflamazomu aktive ederek IL-1 salgılatır ve bölgeye nötrofil akını başlatır."
        ],
        "keyBullets": [
            {"title": "Otoliz ve Heteroliz", "desc": "Ölü hücrenin sindirimi ya kendi lizozom enzimleriyle (otoliz) ya da bölgeye gelen lökositlerin enzimatik silahlarıyla (heteroliz) yürütülür."},
            {"title": "Enflamatuvar Çağrı", "desc": "Hücre zarı delindiğinde dökülen proteinler sahadaki damarları genişletir (vazodilatasyon) ve nötrofilleri kemoseriyle nekroz alanına toplar."},
            {"title": "Sonuç: Skar veya Rejenerasyon", "desc": "Nekrotik kalıntılar lökositlerce temizlendikten sonra doku ya parankim hücreleriyle yenilenir ya da fibröz bağ dokusu (skar) ile onarılır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-29",
                "question": "Nekrotik bir odakta lökosit infiltrasyonunu ve akut enflamasyonu başlatan moleküler yapılar genel olarak nasıl adlandırılır?",
                "answer": "DAMPs (Damage-Associated Molecular Patterns / Hasarla İlişkili Moleküler Paternler). Örnekler: HMGB1 proteini, serbest ATP, ürik asit ve mitokondriyal DNA.",
                "hint": "Mikropta PAMP, ölü konak hücresinde DAMP!"
            },
            {
                "id": "fc-chi-30",
                "question": "Otoliz ile heteroliz arasındaki fark nedir?",
                "answer": "Otoliz: Hücrenin kendi lizozomlarından çıkan enzimlerle kendini sindirmesidir. Heteroliz: Nekroz alanına göç eden lökositlerin (nötrofil/makrofaj) enzimleri tarafından sindirilmesidir.",
                "hint": "Oto = Kendi; Hetero = Dışarıdan gelen lökosit."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Nekrozun Sitoplazmik Değişiklikleri: Yoğun Eozinofili",
        "subtitle": "RNA kaybı, denatüre proteinlerin eozin tutulumu ve camsı camsı homojenleşme",
        "badge": "Mikroskopik Bulgular",
        "badgeColor": "rose",
        "keywords": ["eozinofili", "camsı", "glikojen kaybı", "sitoplazma"],
        "lead": "Nekrotik hücreler standart Hematoksilen-Eozin (H&E) boyamada belirgin derecede parlak pembe/kırmızı (hiper-eozinofilik) boyanır.",
        "spotPearls": [
            "Nekrozda ARTMIIŞ EOZİNOFİLİNİN 2 TEMEL NEDENİ: 1) Bazofilik boyanan sitoplazmik RNA'ların (ribozomların) kaybolması, 2) Denatüre olan sitoplazmik proteinlerin eozini çok daha güçlü bağlamasıdır.",
            "Hücre glikojen partiküllerini kaybettiğinde sitoplazması daha camsı (glassy) ve homojen bir görünüm alır."
        ],
        "keyBullets": [
            {"title": "Artmış Eozinofili (Pembeleşme)", "desc": "Normalde sitoplazmaya hafif mavimsi-mor ton veren ribozomal RNA nükleazlarca parçalanır. Açığa çıkan denatüre proteinler anyonik boya olan eozini bağlar."},
            {"title": "Camsı (Glassy) Görünüm", "desc": "Glikojen depolarının tükenmesi ve sitoplazmik organellerin vakuolize olup erimesi sitoplazmayı homojen ve saydamlaştırır."},
            {"title": "Güve Yeniği (Moth-eaten) Sitoplazma", "desc": "Enzimler organelleri sindirdikçe sitoplazma içinde vakuoller ve boşluklar oluşur, hücre adeta süngerimsi delikli bir hal alır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-31",
                "question": "Işık mikroskobunda nekrotik hücrelerin canlı hücrelere kıyasla belirgin şekilde hiper-eozinofilik (parlak pembe) görünmesinin iki nedeni nedir?",
                "answer": "1) Bazofilik (mavi) boyanan sitoplazmik RNA'ların parçalanarak kaybolması, 2) Denatüre olan intraselüler proteinlerin eozin boyasını çok daha yoğun bağlamasıdır.",
                "hint": "Mavi veren RNA biter, denatüre protein pembe boyayı çeker."
            },
            {
                "id": "fc-chi-32",
                "question": "Nekrotik miyositlerde sitoplazmanın 'camsı' (homojen parlak) görünmesinin nedeni nedir?",
                "answer": "Glikojen granüllerinin tamamen tükenmesi ve organellerin parçalanarak proteinlerin homojen çökeltiler oluşturmasıdır.",
                "hint": "Granüller kaybolunca zemin camsılaşır."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Nekrozun Nükleer Değişiklikleri: Piknoz, Karyoreksis, Karyolizis",
        "subtitle": "Kromatin kondansasyonu, nükleer fragmentasyon ve çekirdeğin tamamen erimesi",
        "badge": "Nükleer Paternler",
        "badgeColor": "red",
        "keywords": ["piknoz", "karyoreksis", "karyolizis", "nükleus"],
        "lead": "Nekrotik hücre ölümünün ışık mikroskobundaki en kesin ve tartışmasız kanıtı çekirdekteki (nükleus) 3 ardışık morfolojik değişikliktir.",
        "spotPearls": [
            "PİKNOZ: Çekirdeğin büzüşmesi, küçülmesi ve koyu siyah-mavi homojen kitleye dönüşmesidir.",
            "KARYOREKSİS: Piknotik çekirdeğin parçalanması ve nükleer toz halinde dağılmasıdır.",
            "KARYOLİZİS: DNAaz aktivitesiyle kromatinin tamamen sindirilmesi ve çekirdeğin solup yok olmasıdır (hayalet nükleus)."
        ],
        "keyBullets": [
            {"title": "1. Piknoz (Pyknosis)", "desc": "DNA yoğunlaşması sonucu nükleer hacim küçülür, kromatin aşırı kondanse olur ve çekirdek koyu bazofilik tek bir nokta halini alır."},
            {"title": "2. Karyoreksis (Karyorrhexis)", "desc": "Piknotik nükleus membran bütünlüğünü kaybederek çok sayıda küçük bazofilik parçaya bölünür (nükleer fragmentasyon)."},
            {"title": "3. Karyolizis (Karyolysis)", "desc": "Endonükleazların DNA'yı tamamen eritmesi sonucu çekirdeğin bazofilik boyanması kaybolur; 1-2 gün içinde hücrede çekirdek tamamen silinir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-33",
                "question": "Nekrozda görülen Piknoz, Karyoreksis ve Karyolizis terimlerini tek birer cümleyle tanımlayınız.",
                "answer": "Piknoz: Çekirdeğin büzüşüp koyulaşması. Karyoreksis: Çekirdeğin parçalanıp dağılması. Karyolizis: Çekirdeğin enzimlerle sindirilip tamamen silinmesi/kaybolması.",
                "hint": "Büzüşme -> Parçalanma -> Erime sıralaması."
            },
            {
                "id": "fc-chi-34",
                "question": "Karyolizis sürecinde kromatinin solup kaybolmasını sağlayan temel enzim grubu nedir?",
                "answer": "Lizozomal ve intraselüler Endonükleazlar ile DNAaz enzimleridir. Asidik ortamda aktive olarak DNA omurgasını hidrolize ederler.",
                "hint": "Lizis = Erimeyi yapan nükleazlar."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Doku Nekrozu Kalıpları 1: Koagülatif Nekroz",
        "subtitle": "Solid organ enfarktları, hücre çatısının korunması ve 'Hayalet Hücreler'",
        "badge": "Koagülatif Nekroz",
        "badgeColor": "red",
        "keywords": ["koagülatif", "enfarkt", "miyokard", "hayalet hücre", "iskemi"],
        "lead": "Koagülatif nekroz; doku çatısının ve hücre sınırlarının günlerce korunduğu, iskemik enfarktların en karakteristik nekroz kalıbıdır.",
        "spotPearls": [
            "BEYİN HARİÇ tüm solid organların (Kalp, Böbrek, Dalak) iskemik enfarktlarında KOAGÜLATİF NEKROZ gelişir.",
            "Asidoz hem yapısal proteinleri hem de enzimleri denatüre ettiği için proteoliz bloke olur; hücreler çekirdeksiz 'HAYALET HÜCRELER' (Tombstone) olarak yerinde kalır."
        ],
        "keyBullets": [
            {"title": "Mekanizma: Enzimatik Blokaj", "desc": "Şiddetli asidoz lizozomal proteolitik enzimleri de denatüre eder. Kendi kendini sindiremeyen hücreler haftalarca yapısal iskeletini korur."},
            {"title": "Mikroskopik Özellik", "desc": "Hücrelerin dış sınırları ve dokunun mimarisi tanınabilir; ancak çekirdekler (piknoz/karyolizis nedeniyle) kaybolmuştur ve sitoplazma hiper-eozinofiliktir."},
            {"title": "Makroskopik Görünüm", "desc": "Tipik olarak kama şeklinde (apeksi tıkanan damara, tabanı organ kapsülüne bakan), soluk, kuru ve sert enfarkt alanlarıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-35",
                "question": "Koagülatif nekrozda ölü hücrelerin günlerce şeklini ve doku çatısını koruyabilmesinin biyokimyasal sebebi nedir?",
                "answer": "Ağır asidozun hücresel proteolitik enzimleri de denatüre etmesidir. Enzimler felç olduğu için ölü hücreler hemen sindirilemez ve yapısal iskeletleri korunur.",
                "hint": "Enzimler de piştiği için hücreyi eritemez."
            },
            {
                "id": "fc-chi-36",
                "question": "Hangi solid organ enfarktında koagülatif nekroz GÖRÜLMEZ ve neden?",
                "answer": "BEYİN (Serebral İnfarkt)! Beyin dokusu yoğun lipid içerdiği ve zengin lizozomal hidrolazlara sahip olduğu için iskemisinde koagülatif değil LİKEFAKSİYON (Sıvılaşma) nekrozu gelişir.",
                "hint": "En büyük kurul tuzağı: Beyin koagüle olmaz, sıvılaşır!"
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Doku Nekrozu Kalıpları 2: Likefaksiyon (Sıvılaşma) Nekrozu",
        "subtitle": "Fokal bakteriyel enfeksiyonlar, apseler ve santral sinir sistemi enfarktları",
        "badge": "Likefaksiyon",
        "badgeColor": "amber",
        "keywords": ["likefaksiyon", "apse", "beyin enfarktı", "irin", "sıvılaşma"],
        "lead": "Likefaksiyon nekrozu; ölü hücrelerin tamamen sindirilerek dokunun vizköz, sıvı bir kitleye (irin/kist) dönüştüğü nekroz tipidir.",
        "spotPearls": [
            "İki klasik durumda görülür: 1) Fokal bakteriyel ve mantar enfeksiyonları (APSE oluşumu), 2) BEYİN İNFARKTLARI (hipoksik SSS ölümü).",
            "Nötrofillerin lizozomal enzim salınımı dokuyu tamamen eritir; ölü lökositler ve hücre enkazı sarı-yeşil renkli 'İRİN' (Pus) oluşturur."
        ],
        "keyBullets": [
            {"title": "Enzimatik Çözünme", "desc": "Koagülatif nekrozun tam aksine burada proteoliz ve sindirim baskındır. Doku çatısı tamamen silinir, geride sıvı dolu kavite kalır."},
            {"title": "Bakteriyel Apseler", "desc": "Stafilokok gibi piyojenik bakteriler nötrofilleri çeker. Nötrofillerin döktüğü elastaz, kollajenaz ve proteazlar parankimi eriterek apse havuzuna çevirir."},
            {"title": "Beyin İnfarktının Özelliği", "desc": "Mikroglialar ve çevre astrositler nekrotik dokuyu eritir. Sonuçta koagülatif enfarkt gibi skarlaşmaz, içi BOS benzeri sıvı dolu 'kistik kavite' bırakır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-37",
                "question": "Beyin dokusu enfarktında koagülatif nekroz yerine likefaksiyon nekrozu görülmesinin temel nedeni nedir?",
                "answer": "Beyin dokusunun yüksek lipid ve su içeriğine sahip olması, hücre çatısının bağ dokusundan fakir olması ve otolitik lizozomal enzimlerin çok hızlı aktive olmasıdır.",
                "hint": "Beyin bağ dokudan yoksundur ve zengin hidrolazlara sahiptir."
            },
            {
                "id": "fc-chi-38",
                "question": "Likefaksiyon nekrozunun karakteristik klinik ürünü olan 'İrin' (Pus) mikroskobik olarak nelerden oluşur?",
                "answer": "Nekrotik nötrofiller (lökositler), sıvılaşmış doku hücre kalıntıları, bakteriler ve protein yönünden zengin eksüda sıvısından oluşur.",
                "hint": "Ölü nötrofil + erimiş doku enkazı = İrin."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Doku Nekrozu Kalıpları 3: Gangrenöz Nekroz",
        "subtitle": "Ekstremite iskemisi, Kuru Gangren vs Yaş Gangren ve Clostridium enfeksiyonu",
        "badge": "Klinik Patern",
        "badgeColor": "rose",
        "keywords": ["gangren", "kuru gangren", "yaş gangren", "clostridium", "diyabet"],
        "lead": "Gangrenöz nekroz; bağımsız bir morfolojik tip olmayıp, genellikle alt ekstremitede kan akımının kesilmesiyle başlayan klinik bir terimdir.",
        "spotPearls": [
            "KURU GANGREN: Çok katmanlı dokuda gelişen saf iskemik koagülatif nekrozdur; doku siyahlaşır, kurur ve büzüşür (mumyalaşma).",
            "YAŞ GANGREN: İskemik koagülatif nekroz üzerine bakteriyel süperenfeksiyon eklendiğinde lökosit enzimleriyle Likefaksiyon nekrozuna dönüşmesidir."
        ],
        "keyBullets": [
            {"title": "Etyolojik Odak: Periferik Arter Hastalığı", "desc": "Diyabetik vaskülit ve ateroskleroz sonucu ayak ve bacaklarda arteryel tıkanıklık gangrenin en sık zeminidir."},
            {"title": "Kuru Gangren Tablosu", "desc": "Bakteriyel enfeksiyon yoktur veya minimaldir. Sağlam doku ile nekrotik doku arasında keskin bir demarkasyon hattı bulunur."},
            {"title": "Yaş Gangren ve Gazlı Gangren", "desc": "Bakteriler (Clostridium perfringens) dokuyu fermente ederek gaz kabarcıkları (krepitasyon), kokuşma ve hızla yayılan septik şok tablosu üretir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-39",
                "question": "Kuru gangren ile yaş gangren arasındaki patolojik mekanizma farkı nedir?",
                "answer": "Kuru gangren saf iskemik KOAGÜLATİF nekrozdur (bakteri yoktur). Yaş gangren ise koagülatif nekroz üzerine bakterilerin binmesiyle LİKEFAKSİYON nekrozunun eklenmiş halidir.",
                "hint": "Kuru = Koagülatif; Yaş = Koagülatif + Likefaksiyon (bakteri)."
            },
            {
                "id": "fc-chi-40",
                "question": "Diyabetik bir hastanın ayak parmağında keskin sınırlı, siyah, kurumuş ve sertleşmiş lezyon hangi gangren tipidir?",
                "answer": "Kuru Gangren. Mumyalaşmış görünüm tipiktir ve süperenfeksiyon gelişene kadar sıvılaşma göstermez.",
                "hint": "Siyah ve kupkuru = Mumyalaşma = Kuru Gangren."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Doku Nekrozu Kalıpları 4: Kazeöz Nekroz",
        "subtitle": "Tüberküloz, peynirimsi makroskopi, granülomatöz iltihap ve Langhans dev hücreleri",
        "badge": "Kazeöz Nekroz",
        "badgeColor": "amber",
        "keywords": ["kazeöz", "tüberküloz", "granülom", "peynirleşme", "langhans"],
        "lead": "Kazeöz nekroz; peynirimsi, ufalanabilir beyaz makroskopik görünümüyle tanınan ve neredeyse tüberküloza özgü olan özelleşmiş bir nekroz kalıbıdır.",
        "spotPearls": [
            "KAZEÖZ NEKROZUN EN KARAKTERİSTİK NEDENİ TÜBERKÜLOZDUR (Mycobacterium tuberculosis).",
            "Mikroskopide: Doku mimarisi tamamen silinmiştir; ortada şekilsiz, aselüler, pembe amorf granüler enkaz, çevresinde epiteloid histiyositler ve Langhans dev hücreleri (Granülom) yer alır."
        ],
        "keyBullets": [
            {"title": "Peynirimsi (Caseous) Karakter", "desc": "Makroskopik olarak enfarkt gibi sert veya apse gibi sıvı değildir; ufalanan, sarı-beyaz renkli kuru çökelek peyniri kıvamındadır."},
            {"title": "Mikroskopik Ayrım", "desc": "Koagülatif nekroz gibi doku çatısını korumaz; Likefaksiyon gibi tamamen sıvılaşmaz; ikisinin arasında amorf nükleer toz birikintisidir."},
            {"title": "Granülomatöz Çevre", "desc": "Nekroz çekirdeği; aktive epiteloid makrofajlar, çok çekirdekli Langhans dev hücreleri ve en dışta lenfosit halkasıyla sınırlandırılır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-41",
                "question": "Akciğer üst lob kavitesinde sarı-beyaz renkli, peynirimsi ve ufalanabilir nekroz saptanan bir hastada en olası etken nedir?",
                "answer": "Mycobacterium tuberculosis (Tüberküloz). Bu görüntü kazeöz (peynirleşme) nekrozunun patognomonik makroskopisidir.",
                "hint": "Peynirimsi nekroz = Tüberküloz!"
            },
            {
                "id": "fc-chi-42",
                "question": "Kazeöz nekroz mikroskobik olarak koagülatif nekrozdan nasıl ayırt edilir?",
                "answer": "Koagülatif nekrozda doku mimarisi ve hücre sınırları (hayalet hücreler) korunmuştur. Kazeöz nekrozda ise doku mimarisi TAMAMEN SİLİNMİŞTİR; yapı tamamen amorf, granüler ve aselüler pembe enkaza dönmüştür.",
                "hint": "Koagülatifte hücre iskeleti var, kazeözde hücre sınırı sıfır!"
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Doku Nekrozu Kalıpları 5: Yağ Nekrozu ve Sabunlaşma",
        "subtitle": "Pankreatik lipaz aktivasyonu, kalsiyum sabunları ve tebeşir beyazı lekeler",
        "badge": "Yağ Nekrozu",
        "badgeColor": "sky",
        "keywords": ["yağ nekrozu", "pankreatit", "sabunlaşma", "saponifikasyon", "kalsiyum"],
        "lead": "Yağ nekrozu; aktif pankreatik enzimlerin salınmasıyla veya travmayla yağ dokusunun destrüksiyona uğradığı odakları tanımlar.",
        "spotPearls": [
            "AKUT PANKREATİTTE aktive olan LİPAZ enzimi çevre omentum ve mezenterdeki trigliseridleri serbest yağ asitlerine hidrolize eder.",
            "Serbest yağ asitleri KALSİYUM ile birleşerek 'KALSİYUM SABUNLARI' (Saponifikasyon) oluşturur; makroskopide TEBEŞİR BEYAZI (chalky white) plaklar görülür."
        ],
        "keyBullets": [
            {"title": "Pankreatik Enzimatik Hasar", "desc": "Duktal obstrüksiyon veya alkolle aktive olan lipaz ve proteazlar peripankreatik yağ dokusunu sindirir."},
            {"title": "Saponifikasyon (Sabunlaşma)", "desc": "Açığa çıkan yağ asitleri serum kalsiyumu ile presipite olur. Bu durum hastada serum kalsiyumunun düşmesine (hipokalsemi) yol açar."},
            {"title": "Mikroskopik Görünüm", "desc": "Nekrotik adipositlerin sınırları belirsiz gölgeler halindedir; kalsiyum çökeltileri H&E boyasında bazofilik (mavi-mor) granüler kitleler oluşturur."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-43",
                "question": "Akut pankreatitli bir hastada ameliyat veya otopside peritonda görülen 'tebeşir beyazı' sert odakların biyokimyasal içeriği nedir?",
                "answer": "Kalsiyum Sabunları (Saponifikasyon odakları). Lipazın trigliseridleri yıkmasıyla açığa çıkan serbest yağ asitlerinin kalsiyum iyonlarıyla birleşerek çökmesidir.",
                "hint": "Yağ asidi + Kalsiyum = Sabunlaşma."
            },
            {
                "id": "fc-chi-44",
                "question": "Şiddetli akut nekrotizan pankreatitte kanda neden HİPOKALSEMİ (kalsiyum düşüklüğü) gelişir?",
                "answer": "Çünkü dolaşımdaki iyonize kalsiyum, periton ve mezenterde nekroze olan yağ dokusundaki yağ asitleri tarafından sabunlaşma reaksiyonuyla yoğun şekilde tüketilip çöktürülür.",
                "hint": "Kalsiyum sabunlaşma odaklarına çekilir, kandaki seviyesi düşer."
            }
        ]
    },
    {
        "slideNumber": 23,
        "title": "Doku Nekrozu Kalıpları 6: Fibrinoid Nekroz",
        "subtitle": "İmmün kompleks birikimi, vaskülitler, Malign Hipertansiyon ve damar duvarı homojenleşmesi",
        "badge": "Fibrinoid Nekroz",
        "badgeColor": "violet",
        "keywords": ["fibrinoid", "vaskülit", "malign hipertansiyon", "immün kompleks", "damar"],
        "lead": "Fibrinoid nekroz; antijen-antikor komplekslerinin damar duvarlarında birikmesi veya aşırı yüksek tansiyon sonucu gelişen özgül bir damar lezyonudur.",
        "spotPearls": [
            "FİBRİNOİD NEKROZ GENELLİKLE DAMAR DUVARLARINDA (ARTER VE ARTERİYOLLERDE) GÖRÜLÜR.",
            "İmmün kompleksler ile damar dışına sızan FİBRİN birleşerek H&E boyasında parlak pembe, amorf, 'fibrin benzeri' (fibrinoid) bir halka oluşturur."
        ],
        "keyBullets": [
            {"title": "Görüldüğü Tipik Hastalıklar", "desc": "Poliarteritis Nodoza (PAN), Sistemik Lupus Eritematozus (SLE vasküliti) ve Malign Hipertansiyon."},
            {"title": "Patofizyolojik Mekanizma", "desc": "İmmün vaskülitlerde Tip III aşırı duyarlılıkla kompleman aktive olur; endotel parçalanarak plazma proteinleri ve fibrinojen damar duvarına sızar."},
            {"title": "Malign Hipertansiyon Etkisi", "desc": "Ani ve aşırı yüksek kan basıncı arteriyol endotelini mekanik olarak yırtar; kan proteinleri duvara zorla itilerek nekrotik fibrinoid halka üretir."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-45",
                "question": "Işık mikroskobunda arteriyol duvarında parlak eozinofilik (pembe), homojen, amorf halkasal birikim ve nekroz saptandığında ilk akla gelecek nekroz tipi nedir?",
                "answer": "Fibrinoid Nekroz. Damar duvarında biriken immün kompleksler ve damar dışına kaçan fibrinin oluşturduğu tipik tablodur.",
                "hint": "Damar duvarında parlak pembe halka = Fibrinoid!"
            },
            {
                "id": "fc-chi-46",
                "question": "Fibrinoid nekrozun görüldüğü en tipik iki immünolojik/vasküler hastalık nedir?",
                "answer": "1) Poliarteritis Nodoza (PAN) veya SLE gibi sistemik immün vaskülitler, 2) Malign Hipertansiyon (hiperplastik arteriyoloskleroz ile birlikte).",
                "hint": "Biri vaskülit, diğeri ölümcül yüksek tansiyon."
            }
        ]
    },
    {
        "slideNumber": 24,
        "title": "Nekrotik Hücrelerden Enzim Kaçışı ve Klinik Biyobelirteçler",
        "subtitle": "Organ spesifik enzimler, plazma seviyeleri ve doku hasarının laboratuvar tanısı",
        "badge": "Klinik Biyokimya",
        "badgeColor": "blue",
        "keywords": ["troponin", "ck-mb", "ast", "alt", "amilaz", "biyobelirteç"],
        "lead": "Nekroz sırasında plazma membran bütünlüğünün bozulması, dokuya özgü intraselüler proteinlerin kana karışmasına ve hasarın laboratuvarda tespitine olanak tanır.",
        "spotPearls": [
            "Kardiyak İskemi / Enfarkt: Kardiyak Troponin I ve T (en spesifik) ile CK-MB kullanılır.",
            "Karaciğer Hasarı: ALT (karaciğere özgül) ve AST yükselir; Akut Pankreatit: Serum Amilaz ve Lipaz yükselir."
        ],
        "keyBullets": [
            {"title": "Kardiyak Belirteçler", "desc": "Miyokard nekrozunda Troponin I ve T 2-4 saatte yükselmeye başlar, 24-48 saatte pik yapar ve 7-10 gün yüksek kalır. CK-MB ise 48-72 saatte normale döner."},
            {"title": "Hepatobiliyer Enzimler", "desc": "Hepatosit nekrozunda ALT (alanin aminotransferaz) ve AST sitoplazmadan kana boşalır. Safra kanalı hasarında ise ALP ve GGT yükselir."},
            {"title": "Pankreas ve İskelet Kası", "desc": "Pankreas nekrozunda lipaz ve amilaz; iskelet kası rabdomiyolizinde ise total kreatin kinaz (CK-MM) ve miyoglobin kana karışır."}
        ],
        "flashcards": [
            {
                "id": "fc-chi-47",
                "question": "Akut miyokard enfarktüsü tanısında Troponin'in CK-MB'ye göre en büyük iki klinik üstünlüğü nedir?",
                "answer": "1) Miyokarda çok daha yüksek doku spesifisitesine sahiptir (iskelet kası zedelenmelerinden etkilenmez). 2) Kanda 7-10 gün boyunca yüksek kalarak geç başvuran enfarktların da yakalanmasını sağlar.",
                "hint": "Daha spesifik ve kanda çok daha uzun süre kalır."
            },
            {
                "id": "fc-chi-48",
                "question": "Akut pankreatit tanısında serum amilazına kıyasla Serum Lipazının tercih edilmesinin nedeni nedir?",
                "answer": "Lipaz pankreas dokusuna çok daha özgüldür (amilaz tükürük bezi hastalıklarında da yükselebilir) ve kanda daha uzun süre yüksek kalır.",
                "hint": "Lipaz = Pankreasa özel; Amilaz = Tükürükte de var."
            }
        ]
    }
]

# Six comprehensive comparison tables attached to critical slides
COMPARISON_TABLES = {
    8: {
        "title": "İskemik Hücre Hasarında Biyokimyasal Kaskat ve Olaylar Sırası",
        "headers": ["Aşama", "Hücresel / Biyokimyasal Olay", "Sonuç ve Morfolojik Yansıma", "Reversibl / İrreversibl"],
        "rows": [
            ["1. Dakika", "Oksijen kesilmesi -> Oksidatif fosforilasyon durur", "Mitokondriyal ATP sentezi çöker", "Reversibl"],
            ["2-5. Dakika", "Anaerobik glikoliz artar, laktik asit birikir", "pH düşer (asidoz), nükleer kromatin kümeleşir", "Reversibl"],
            ["5-10. Dakika", "Na+/K+ ATPaz pompası durur, Na+ ve su girer", "Hücresel şişme (hidropik değişim), mikrovillus kaybı", "Reversibl"],
            ["10-15. Dakika", "Granüllü ER şişer, ribozomlar ayrılır", "Protein sentezi durur, lipid birikimi başlar", "Reversibl"],
            ["20-30. Dakika", "Mitokondri geçirgenlik poru açılır, kalsiyum dolar", "ATP sentez kapasitesi kalıcı olarak ölür", "İrreversibl Eşik!"],
            [">30. Dakika", "Fosfolipazlar membranı deler, enzimler kana sızar", "Troponin/enzim kaçağı, lizozom patlaması, otoliz", "Kesin Nekroz"]
        ]
    },
    10: {
        "title": "Geri Dönüşümlü Hasar vs Geri Dönüşümsüz Hasar Karşılaştırması",
        "headers": ["Özellik", "Geri Dönüşümlü (Reversibl) Hasar", "Geri Dönüşümsüz (İrreversibl / Nekroz) Hasar"],
        "rows": [
            ["Membran Durumu", "Zar intaktır; kabarcıklar (blebs) ve mikrovillus silinmesi vardır", "Plazma ve organel zarları delinmiş, parçalanmıştır"],
            ["Mitokondri", "Hafif şişme, krista aralanması", "Ağır vakuolizasyon, matriks içinde amorf/flokülan dansiteler"],
            ["Hücre İçi Enzimler", "Hücre içinde kalır; serum seviyeleri normaldir", "Parçalanan zardan kana dökülür (Troponin, ALT, AST yüksek)"],
            ["Nükleus", "Hafif kromatin kümeleşmesi; nükleer zar intaktır", "Piknoz -> Karyoreksis -> Karyolizis (çekirdek erir)"],
            ["Klinik Sonuç", "Uyaran kalkınca tam iyileşme ve fonksiyon kazanımı", "Hücre ölümü, akut enflamasyon ve skar oluşumu"]
        ]
    },
    14: {
        "title": "Nekroz ile Apoptozun Temel Ayırıcı Tanı Kriterleri",
        "headers": ["Kriter", "Nekroz (Nekrotik Hücre Ölümü)", "Apoptoz (Programlı Hücre Ölümü)"],
        "rows": [
            ["Hücre Boyutu", "Büyümüş (hücresel şişme ve lizis)", "Küçülmüş (büzüşme ve kondansasyon)"],
            ["Zar Bütünlüğü", "Parçalanmış, geçirgen, delikli", "İntaktır; apoptoz cisimcikleri şeklinde tomurcuklanır"],
            ["Hücre İçeriği", "Ortama kontrolsüzce saçılır (enzimatik sindirim)", "Membranöz cisimciklerle paketlenir, ortama kaçmaz"],
            ["Enflamatuvar Yanıt", "DAİMA VARDIR (yoğun nötrofilik/makrofajik reaksiyon)", "KESİNLİKLE YOKTUR (sessiz fagositoz)"],
            ["Fizyolojik / Patolojik", "DAİMA PATOLOJİKTİR (kaza sonucu hücre ölümü)", "Fizyolojik (embriyogenez, hormon) veya patolojik (DNA hasarı)"],
            ["Mekanizma", "ATP tükenmesi, membran yırtılması, kalsiyum toksisitesi", "Genetik program, kaspaz aktivasyonu, mitokondriyal/ölüm reseptör"]
        ]
    },
    17: {
        "title": "Nekrozda Nükleer Değişikliklerin Morfolojik Özellikleri",
        "headers": ["Evre", "Tanım", "Mikroskopik / H&E Görünümü", "Biyokimyasal Mekanizma"],
        "rows": [
            ["Piknoz", "Nükleusun büzüşmesi ve küçülmesi", "Küçük, aşırı yoğun, koyu siyahımsı-mavi nükleus", "DNA'nın aşırı yoğun kondansasyonu"],
            ["Karyoreksis", "Nükleusun parçalanması", "Nükleer zar dağılır; sitoplazmaya saçılmış bazofilik parçalar", "Endonükleazların kromatin bloklarını kırması"],
            ["Karyolizis", "Nükleusun erimesi ve silinmesi", "Çekirdek bazofilisini kaybeder; soluk pembe gölge kalır", "DNAaz enzimlerinin DNA'yı tamamen sindirmesi"]
        ]
    },
    20: {
        "title": "Altı Temel Doku Nekrozu Kalıbının Büyük Karşılaştırma Matrisi",
        "headers": ["Nekroz Tipi", "Temel Mekanizma", "Tipik Morfolojik Özellik", "Klasik Klinik Örnekler"],
        "rows": [
            ["Koagülatif", "Protein ve enzim denatürasyonu; mimari korunur", "Hücre iskeleti intakt, çekirdeksiz hayalet hücreler", "Miyokard, böbrek, dalak enfarktları (Beyin hariç!)"],
            ["Likefaksiyon", "Enzimatik sindirim ve otoliz baskın; erime", "Doku sıvılaşır; sarı-yeşil irin havuzu veya kist", "Bakteriyel apseler ve BEYİN enfarktları"],
            ["Gangrenöz", "Ekstremite iskemisi; koagülatif (+/- likefaksiyon)", "Kuru (siyah, kuru) veya Yaş (bakteriyel, kokulu)", "Diyabetik ayak, periferik arter tıkanıklığı"],
            ["Kazeöz", "Tüberküloz basilinin granülomatöz yıkımı", "Peynirimsi, ufalanan amorf pembe enkaz, dev hücreler", "Tüberküloz enfeksiyonu (akciğer ve lenf nodu)"],
            ["Yağ Nekrozu", "Lipazların trigliseridi yıkıp kalsiyumla birleşmesi", "Tebeşir beyazı sabunlaşma (saponifikasyon) plakları", "Akut pankreatit, travmatik meme nekrozu"],
            ["Fibrinoid", "Damar duvarında immün kompleks + fibrin birikimi", "Damar lümeni çevresinde parlak pembe amorf halka", "Poliarteritis Nodoza (PAN), Malign Hipertansiyon"]
        ]
    },
    24: {
        "title": "Doku Hasarı ve Nekrozda Salınan Klinik Biyokimyasal Biyobelirteçler",
        "headers": ["Hedef Doku / Organ", "Salınan Temel Biyobelirteçler", "Klinik Kullanım ve Tanısal Değeri"],
        "rows": [
            ["Kalp Kası (Miyokard)", "Kardiyak Troponin I & T, CK-MB", "Akut Miyokard Enfarktüsü (Troponin 7-10 gün yüksek kalır)"],
            ["Karaciğer (Hepatosit)", "ALT (Alanin Aminotransferaz), AST", "Akut hepatit, toksik karaciğer nekrozu (Parasetamol)"],
            ["Safra Kanalları", "ALP (Alkalen Fosfataz), GGT", "Biliyer obstrüksiyon, kolestatik karaciğer hasarı"],
            ["Ekzokrin Pankreas", "Serum Lipaz ve Amilaz", "Akut Pankreatit (Lipaz daha spesifik ve uzun ömürlüdür)"],
            ["İskelet Kası", "Total Kreatin Kinaz (CK-MM), Miyoglobin", "Rabdomiyoliz, ezilme (crush) sendromu, miyozitler"],
            ["Beyin Parankimi", "NSE (Nöron Spesifik Enolaz), S100B", "Ağır iskemik inme, kafa travması, hipoksik ansefalopati"]
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
        flashcards = s_raw["flashcards"]

        # Match questions
        matched_qs = find_matched_questions(keywords, max_count=2)
        total_matched_questions += len(matched_qs)

        # Build structured synthesis narrative
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

        # Core content
        core_content = {
            "keyBullets": key_bullets
        }

        # Check if table exists for this slide
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
                f"Bu slayttaki patolojik bulgular klinikte hangi hastalıklarla prezente olur?"
            ]
        }
        slides.append(slide_obj)

    deck_obj = {
        "id": "learn-hucre-hasari-hucre-olumu",
        "title": "Hücre Hasarı, Hücre Ölümü ve Nekroz Patolojisi",
        "shortTitle": "Hücre Hasarı & Nekroz",
        "discipline": "Tıbbi Patoloji",
        "committee": "Kurul 1 - Hücre Hasarı, İltihap ve Neoplazi (TIP 301)",
        "instructor": "Prof. Dr. Hikmet Keleş (Tıbbi Patoloji AD)",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_matched_questions,
        "totalFlashcardsCount": len(slides) * 2,
        "themeColor": "indigo",
        "overview": (
            "Dönem 3 Kurul 1 Patoloji müfredatının temel taşı olan bu derste; Prof. Dr. Hikmet Keleş'in "
            "resmi ders notları, Robbins Temel Patoloji ilkeleri ve çıkmış kurul soruları sentezlenmiştir. "
            "Homeostazın çöküşü, hipoksi ve iskemi patofizyolojisi, ATP azalması, hücre içi kalsiyum akışı, "
            "hidropik şişme ve yağlanma (reversibl hasar), irreversibl hasara geçişin 2 kritik eşiği, nekroz "
            "sitoplazmik ve nükleer değişiklikleri (piknoz, karyoreksis, karyolizis), 6 temel doku nekrozu kalıbı "
            "(koagülatif, likefaksiyon, gangrenöz, kazeöz, yağ ve fibrinoid nekroz) ve klinik enzim belirteçleri "
            "24 kapsamlı interaktif slayt, 48 3D akıl kartı ve 6 karşılaştırma tablosu ile eksiksiz sunulmaktadır."
        ),
        "highYieldPearls": [
            "İSKEMİ HİPOKSİDEN DAHA HIZLI VE YIKICIDIR; hem oksijeni hem glukozu keser, laktik asidi biriktirir.",
            "Reversibl hasarın ilk ve evrensel bulgusu Na+/K+ ATPaz pompa yetmezliğine bağlı HÜCRESEL ŞİŞMEDİR.",
            "İrreversibl hasara geçişin (Point of No Return) 2 şartı: Kalıcı mitokondri disfonksiyonu ve MEMBRAN BÜTÜNLÜĞÜNÜN KAYBIDIR.",
            "Beyin hariç tüm solid organ enfarktlarında KOAGÜLATİF NEKROZ; Beyin enfarktlarında ve bakteriyel apselerde LİKEFAKSİYON NEKROZU görülür.",
            "Akut pankreatitte lipaz aktivasyonu ile KALSİYUM SABUNLARI (Saponifikasyon / Yağ Nekrozu) gelişir ve kanda hipokalsemiye yol açar.",
            "Damar duvarlarında (vaskülit, malign HT) immün kompleks ve fibrin birikimi FİBRİNOİD NEKROZ yapar."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Hücre Hasarı ve Nekroz...")
    deck = build_deck()
    print(f"Generated deck with {len(deck['slides'])} slides and {deck['totalFlashcardsCount']} flashcards.")

    # Update interactive_learning_decks.json
    with open(DECKS_PATH, 'r', encoding='utf-8') as f:
        decks = json.load(f)

    # Find if deck exists
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

    # Update learning_decks_meta.json
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

    print("Success! Cell injury deck generation completed.")

if __name__ == '__main__':
    main()
