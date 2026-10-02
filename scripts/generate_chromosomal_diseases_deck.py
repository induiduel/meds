#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_chromosomal_diseases_deck.py
Generates the comprehensive %500 detail 22-slide learning deck for:
"Kromozomal Hastalıklar ve Genetik Danışma" (Tıbbi Genetik - Dr. Öğr. Üyesi Serap Arslan)
Incorporating 22 slides, 44 3D flashcards, 6 comparison tables, and matched past exam questions (d3-k1-tbg-002, d3-k1-tbg-003, d3-k1-tbg-014, d3-k2-tbg-001, d3-k1-pat-052 etc.).
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Tıbbi Genetik müfredatında kromozomal hastalıklar ile doğrudan ilişkilidir.'
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Tıbbi Genetik müfredatında kromozomal hastalıklar ile doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Kromozomal Hastalıklara Giriş ve Sitogenetik Temeller",
        "subtitle": "2n=46 insan kromozom kuruluşu, epidemiyoloji, dengeli ve dengesiz anomaliler",
        "badge": "Giriş & Epidemiyoloji",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["kromozom anomali", "dengeli kromozom", "dengesiz anomali"],
        "lead": "Normal insan karyotipinde 46 kromozom (2n=46) bulunur; kromozomların hem sayısında hem de yapısında meydana gelen değişiklikler kalıtsal hastalıkların en ağır mortalite ve morbiditeye sahip grubunu oluşturur.",
        "spotPearls": [
            "CANLI DOĞUM İNSİDANSI: Kromozomal bozukluklar tüm canlı doğumların yaklaşık %1'inde (yüzde birinde) saptanır; yüzden fazla farklı kromozomal sendrom tanımlanmıştır.",
            "EN YAYGIN TİP ANÖPLOİDİ: Klinik öneme sahip kromozom anomalilerinin en yaygın tipini anöploidiler oluşturur ve daima fiziksel ve/veya zihinsel sorunlarla seyreder.",
            "DENGELİ YENİDEN DÜZENLENME TUZAĞI: Dengeli anomaliler 1/500 sıklıkta görülür, taşıyıcıda genelde fenotipik etki göstermez ('görünürde dengeli'); ancak kırık noktası aktif geni bozarsa (DMD olgularında Xp;otozom translokasyonu gibi) fenotipik hastalık ortaya çıkabilir!",
            "REKÜRRENS RİSKİ: Dengeli taşıyıcıların sonraki kuşakta dengesiz gamet oluşturma riski yeniden düzenlenmenin tipine göre %1 ile %100 arasında değişir."
        ],
        "keyBullets": [
            {"title": "Kromozomal Hastalıkların Temeli", "desc": "Sitogenetik anormallikler genomun yüzlerce ila binlerce genini aynı anda etkileyerek çoklu konjenital anomalilere yol açar."},
            {"title": "Dengeli vs Dengesiz Kavramı", "desc": "Dengesiz anomalilerde gen dozajı (haploinsufficiency veya trizomik artış) bozulurken, dengeli anomalilerde genetik materyal kaybı veya fazlalığı yoktur."},
            {"title": "DMD ve Xp;Otozom İstisnası", "desc": "Görünürde dengeli translokasyonlar esnasında kırık hattı distrofin (DMD) genini parçalarsa dişi taşıyıcıda tam klinik tablo gelişebilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-1",
                "question": "Tüm canlı doğumlarda kromozomal anomali görülme sıklığı yaklaşık yüzde kaçtır ve en yaygın klinik tipi hangisidir?",
                "answer": "Canlı doğumların yaklaşık %1'inde görülür ve en yaygın klinik tipi anöploididir.",
                "hint": "%1 insidans, anöploidi."
            },
            {
                "id": "fc-ch-2",
                "question": "Dengeli kromozom anomalisi taşıyan bir bireyde fenotipik hastalık ortaya çıkmasının temel mekanizması nedir ve amfi dersinde verilen prototip örnek nedir?",
                "answer": "Translokasyon kırık noktalarının aktif bir genin yapısını/fonksiyonunu parçalamasıdır; ders notundaki örnek kız çocuklarında görülen Xp;otozom translokasyonuna bağlı Duchenne Muskuler Distrofi (DMD) tablosudur.",
                "hint": "Kırık noktasının gen içi kesisi, DMD Xp;otozom."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Sayısal Düzensizlikler: Öploidi, Poliploidi ve Triploidi Mekanizmaları",
        "subtitle": "Triploidi (69), tetraploidi (92), dispermi, molar gebelik ve abortus insidansı",
        "badge": "Sayısal: Poliploidi",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-pat-052"],
        "keywords": ["triploidi", "dispermi", "tetraploidi", "öploidi", "molar gebelik"],
        "lead": "Sayısal kromozom düzensizlikleri hücredeki kromozom setinin tam katları şeklinde değiştiğinde öploidi/poliploidi, tam katı olmayan tekil kromozom sapmalarında ise anöploidi olarak adlandırılır.",
        "spotPearls": [
            "POLİPLOİDİ ÖRNEKLERİ: İnsanda poliploidinin iki ana örneği Triploidi (3n=69) ve Tetraploidi (4n=92) takımlarıdır; poliploidiler insanda kural olarak letaldir.",
            "SPONTAN ABORTUSLARDAKİ DEV PAY: Triploidi tüm tanımlanmış gebeliklerin %1-3'ünde, 1. trimester spontan abortusların ise tam %20'sinde (beşte birinde) saptanır.",
            "TRİPLOİDİ OLUŞUMUNUN 3 MEKANİZMASI: 1) Bir yumurtanın (n) 2 sperm ile döllenmesi (Dispermi - n+n, en yaygın neden), 2) Diploid sperm (2n) + haploid yumurta (n), 3) Haploid sperm (n) + diploid yumurta (2n).",
            "MOLAR GEBELİK İLİŞKİSİ: Paternal kökenli ekstra kromozom takımı (dispermi) büyük plasenta ve hidatidiform mol (parsiyel mol) gelişimine yol açar."
        ],
        "keyBullets": [
            {"title": "Poliploidi Letalitesi", "desc": "Canlı doğum nadiren gerçekleşse bile triploid fetüsler doğumdan sonraki saatler veya günler içinde kaybedilir, yaşamla bağdaşmaz."},
            {"title": "Sitoplazma Bölünme Kusuru", "desc": "Tetraploidi (92 kromozom) genellikle erken embriyonik bölünmede DNA replikasyonu sonrası sitokinezin gerçekleşmemesiyle doğar."},
            {"title": "Parental Köken Etkisi (İmprinting)", "desc": "Ekstra takım babadan geldiğinde dev kistik plasenta (molar), anneden geldiğinde ise şiddetli gelişme geriliği ve küçük plasenta görülür."}
        ],
        "table": {
            "title": "Sayısal Kromozom Düzensizlikleri: Öploidi vs Anöploidi Karşılaştırması",
            "headers": ["Özellik", "Öploidi / Poliploidi", "Anöploidi"],
            "rows": [
                ["Kromozom Sayısı", "Haploid takımın tam katları (3n=69, 4n=92)", "Haploid takımın katı olmayan sapmalar (2n±1; 45 veya 47)"],
                ["Temel Mekanizma", "Dispermi (çift döllenme) veya sitokinez yetmezliği", "Kromozom ayrılamaması (non-disjunction) veya anafaz gecikmesi"],
                ["Klinik Örnekler", "Triploidi (69,XXY / 69,XXX), Tetraploidi (92)", "Trizomi 21 (Down), Trizomi 18 (Edwards), Monozomi X (Turner)"],
                ["Spontan Düşük Payı", "1. trimester abortuslarının %20'si", "1. trimester abortuslarının %50'den fazlası"],
                ["Postnatal Yaşam", "İstisnasız letal (canlı doğsa bile yaşayamaz)", "Spesifik sendromlarda canlı doğum ve uzun yaşam mümkün (Down, Turner, Klinefelter)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-3",
                "question": "1. trimester spontan abortus materyallerinin yaklaşık %20'sini oluşturan poliploidi tipi nedir ve en sık hangi mekanizmayla oluşur?",
                "answer": "Triploidi (3n=69); en sık bir yumurtanın iki sperm tarafından aynı anda döllenmesi (dispermi) sonucu oluşur.",
                "hint": "3n=69, dispermi."
            },
            {
                "id": "fc-ch-4",
                "question": "Triploidide ekstra kromozom takımının babadan (paternal) gelmesi durumunda plasentada tipik olarak hangi patoloji gelişir?",
                "answer": "Büyük plasenta ve hidatidiform mol (parsiyel mol) değişiklikleri gelişir.",
                "hint": "Paternal kaynak, hidatidiform kistik plasenta."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Anöploidi Oluşum Mekanizmaları: Non-Disjunction ve Anafaz Gecikmesi",
        "subtitle": "Mayoz I vs Mayoz II ayrılamama farkları, anaphase lagging ve mozaiklik",
        "badge": "Mekanizma: Non-Disjunction",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["non-disjunction", "mayoz 1", "mayoz 2", "anaphase lagging", "ayrılamama"],
        "lead": "Anöploidi hücre bölünmesi sırasında kromozomların kutuplara eşit dağılamaması sonucu ortaya çıkar; en önemli iki hücresel neden Mayotik/Mitotik Non-Disjunction ve Anafazda Geri Kalmadır (Anaphase Lagging).",
        "spotPearls": [
            "MAYOZ I NON-DISJUNCTION FARKI: Mayoz I'de homolog kromozomlar ayrılamazsa oluşan 24 kromozomlu anormal gamet HER İKİ PARENTAL HOMOLOĞA (anne ve babanın farklı kromozomlarına - heterolog) sahiptir!",
            "MAYOZ II NON-DISJUNCTION FARKI: Mayoz II'de kardeş kromatitler ayrılamazsa oluşan 24 kromozomlu anormal gametteki ekstra kromozomların İKİSİ DE AYNI EBEVEYNE AİT (özdeş kopyalar) olur!",
            "ANAFAZDA GERİ KALMA (ANAPHASE LAGGING): Kutuplara gitmekte geciken kromozom çekirdek zarı dışında kalıp sitoplazmada erir; monozomik hücre dizisi veya mozaik karyotipler doğurur.",
            "YAŞAMLA BAĞDAŞAN TEK MONOZOMİ: İnsanda canlı doğumla ve postnatal yaşamla bağdaşan yegane tam monozomi TURNER SENDROMU'dur (45,X); tüm otozomal tam monozomiler uterusta letaldir."
        ],
        "keyBullets": [
            {"title": "Metafaz-Anafaz Kontrol Noktası", "desc": "İğ ipliklerinin kinetokora tutunmasındaki kusurlar kromozomların kutuplara asimetrik çekilmesine neden olur."},
            {"title": "Mitotik Non-Disjunction ve Mozaisizm", "desc": "Döllenme sonrası embriyonik mitozda meydana gelen ayrılamama aynı zigottan farklı karyotipe sahip iki veya daha fazla hücre hattı (mozaiklik) üretir."},
            {"title": "Yaş Bağımlılığı", "desc": "Oositlerin doğumdan itibaren Mayoz I profazında (diploten/diktiyoten) beklemesi maternal yaşla birlikte kohezin proteinlerinin bozulmasına ve Mayoz I non-disjunction sıklığına yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-5",
                "question": "Mayoz I non-disjunction ile Mayoz II non-disjunction arasındaki genetik içerik farkı nedir?",
                "answer": "Mayoz I ayrılamamasında 24 kromozomlu gamet her iki ebeveyn homologunu taşırken (heterolog); Mayoz II ayrılamamasında ekstra kromozomlar aynı ebeveyne ait özdeş kromatitlerdir.",
                "hint": "Mayoz I = iki farklı ebeveyn homoloğu; Mayoz II = özdeş kromatitler."
            },
            {
                "id": "fc-ch-6",
                "question": "İnsan canlı doğumlarında yaşamla bağdaşan yegane tam monozomi hangisidir?",
                "answer": "Turner sendromudur (45,X monozomisi); tüm otozomal monozomiler embriyonik dönemde letaldir.",
                "hint": "45,X."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Anöploidi Tipleri ve Tanımları: Trizomi, Monozomi, Tetrazomi, Nullizomi",
        "subtitle": "Kromozom kuruluşu formülleri, otozomal letalite ve yaşayabilen trizomiler",
        "badge": "Sayısal: Anöploidi",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["trizomi", "monozomi", "tetrazomi", "nullizomi", "anöploidi"],
        "lead": "Anöploidi hücredeki diploid kromozom sayısına (46) bir veya birkaç kromozomun eklenmesi veya eksilmesidir; gen dozajındaki dramatik sapma nedeniyle ağır fenotiplerle seyreder.",
        "spotPearls": [
            "TRİZOMİ (2n+1 = 47): İnsan kromozomlarından herhangi birinin 3 adet olmasıdır. Canlı doğumlarda en sık gözlenen otozomal trizomiler +21 (Down), +18 (Edwards) ve +13 (Patau)'tür.",
            "TETRAZOMİ (2n+2 = 48): Belli bir homolog çiftten 4 adet bulunması ya da iki ayrı homolog çiftin trizomik olmasıdır.",
            "MONOZOMİ (2n-1 = 45): Diploid kromozom çiftinden birinin bulunmamasıdır; otozomal monozomiler erken implantasyon evresinde elenir, tek yaşayan form gonozomal 45,X'tir.",
            "NULLİZOMİ (2n-2 = 44): Belli bir homolog kromozom çiftinin her iki üyesinin birden bulunmamasıdır; insanda hücre düzeyinde dahi kesinlikle letaldir."
        ],
        "keyBullets": [
            {"title": "Otozomal Trizomi Kuralı", "desc": "Diğer otozomların (örneğin 16. kromozom trizomisi en sık düşük sebebidir) trizomileri fetüsün doğuma ulaşmasına izin vermez."},
            {"title": "Gen Dozajı Dengesizliği", "desc": "Kromozom üzerindeki yüzlerce genin %150 oranında aşırı ifadesi hücre içi protein dengesini (proteostaz) bozar."},
            {"title": "Gonozomal Tolerans", "desc": "Cinsiyet kromozom anöploidileri (47,XXY, 47,XXX, 45,X) X-inaktivasyonu (Lyonizasyon) sayesinde otozomal trizomilere göre çok daha hafif seyreder."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-7",
                "question": "Canlı doğumlarda en sık karşılaşılan 3 otozomal trizomi sendromu ve kromozom formülleri nelerdir?",
                "answer": "1) Down Sendromu (47,XX/XY,+21), 2) Edwards Sendromu (47,XX/XY,+18), 3) Patau Sendromu (47,XX/XY,+13).",
                "hint": "Trizomi 21, 18 ve 13."
            },
            {
                "id": "fc-ch-8",
                "question": "2n-2 ve 2n+2 kromozom formülleri sitogenetikte hangi anöploidi terimlerine karşılık gelir?",
                "answer": "2n-2 = Nullizomi (homolog çiftin tamamen yokluğu); 2n+2 = Tetrazomi (bir çiftin 4 kopya olması).",
                "hint": "Nulli (yokluk) ve Tetra (dört)."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Yapısal Kromozom Anomalileri Sınıflaması ve Biyolojik Mekanizma",
        "subtitle": "1/375 sıklık, dengeli (inversiyon, translokasyon) ve dengesiz (delesyon, duplikasyon, izo, ring, marker)",
        "badge": "Yapısal: Sınıflama",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["yapısal anomali", "dengeli yapısal", "dengesiz yapısal", "kromozom kırığı"],
        "lead": "Yapısal kromozom düzensizlikleri kromozom kollarında kırıklar oluşması ve kırılan segmentlerin kaybolması ya da anormal konumlarda yeniden birleşmesi sonucu ortaya çıkar; canlı doğan her 375 bebekten 1'inde saptanır.",
        "spotPearls": [
            "İNSİDANS 1/375: Canlı yenidoğanlarda yapısal kromozom anomalisi sıklığı yaklaşık 1/375'tir.",
            "DENGELİ GRUP (Genom Kaybı Yok): İnversiyonlar ve Translokasyonlar; taşıyıcıda genelde fenotip normaldir ancak mayozda dengesiz gamet oluşturma riski taşırlar.",
            "DENGESİZ GRUP (Genom Dozajı Bozuk): Delesyon, Duplikasyon, Ring (halka) kromozom, Marker kromozom ve İzokromozom.",
            "KUŞAKTAN KUŞAĞA AKTARIM: Dengeli taşıyıcı ebeveyn fenotipik olarak tamamen sağlıklıyken gametogenezde parçalanmış kromozomlar nedeniyle çocukta ölümcül dengesiz anomali doğabilir."
        ],
        "keyBullets": [
            {"title": "Kırık Onarım Hataları", "desc": "DNA çift zincir kırıklarının non-homolog end-joining (NHEJ) mekanizmasıyla hatalı birleştirilmesi yapısal düzensizliklerin moleküler kökenidir."},
            {"title": "Asentrik Parçaların Akıbeti", "desc": "Sentromeri bulunmayan asentrik kromozom parçaları hücre bölünmesinde iğ ipliklerine tutunamaz ve mikronükleus oluşturarak kaybolur."},
            {"title": "Disentrik Parçaların Akıbeti", "desc": "İki sentromer içeren parçalar anafazda iki ayrı kutba çekilerek kopma-füzyon-köprü döngüsüne girer ve hücre ölümüne yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-9",
                "question": "Canlı yenidoğanlarda yapısal kromozom anomalisi görülme insidansı nedir ve dengeli yapısal anomalilerin iki temel tipi hangileridir?",
                "answer": "Görülme sıklığı 1/375'tir; iki temel dengeli yapısal anomali tipi İnversiyonlar ve Translokasyonlardır.",
                "hint": "1/375, İnversiyon ve Translokasyon."
            },
            {
                "id": "fc-ch-10",
                "question": "Dengesiz yapısal kromozom anomalilerine 5 ana örnek veriniz.",
                "answer": "1) Delesyon, 2) Duplikasyon, 3) Ring (halka) kromozom, 4) Marker kromozom, 5) İzokromozom.",
                "hint": "Delesyon, duplikasyon, ring, marker, izo."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Delesyonlar ve Mikrodelesyon Sendromları Kapsamlı Matrisi",
        "subtitle": "Terminal vs interkalar delesyon, parsiyel monozomi, haploinsufficiency ve mikrodelesyon tablosu",
        "badge": "Yapısal: Delesyon",
        "badgeColor": "purple",
        "target_ids": ["d3-k1-tbg-003"],
        "keywords": ["delesyon", "mikrodelesyon", "cri du chat", "digeorge", "williams", "smith magenis"],
        "lead": "Delesyon bir kromozom segmentinin kırılarak kaybolmasıdır; parsiyel monozomi oluşturur ve fenotipik etkisi 'haploinsufficiency' (tek gen kopyasının yetersiz kalması) mekanizmasıyla ortaya çıkar.",
        "spotPearls": [
            "TERMINAL VS İNTERKALAR DELİSYON: Terminal delesyon tek kırıkla kromozom ucundan kopmadır (örn: Cri du chat 5p15.2); İnterkalar delesyon kol içi çift kırıkla oluşur, kopan asentrik parça kaybolur (örn: DiGeorge 22q11.2).",
            "MİKRODELESYON ÇÖZÜNÜRLÜĞÜ: >5 Mb delesyonlar klasik konvansiyonel bantlama (sitogenetik) ile saptanabilirken; <5 Mb mikrodelesyonlar ancak moleküler sitogenetik (FISH, Array CGH / CMA) ile teşhis edilebilir.",
            "CRİ DU CHAT (5p-): 5. kromozom kısa kol delesyonu del(5)(p15.2); infantil dönemde kedi miyavlamasına benzer ağlama sesi tipiktir (5p15.3 ağlama, 5p15.2 klinik).",
            "WOLF-HİRSCHHORN (4p-): 4p16.3 delesyonu; 'Grek miğferi' yüz görünümü, belirgin glabella ve balık ağzı ile seyreder."
        ],
        "keyBullets": [
            {"title": "Haploinsufficiency Prensibi", "desc": "Kopan segmentteki kritik gelişimsel genlerin dozajının %50'ye düşmesi normal morfogenezi imkansız kılar."},
            {"title": "Otozomal Boyut Kısıtı", "desc": "Büyük otozomal delesyonlar embriyonik dönemde kesinlikle yaşamla bağdaşmaz; canlı doğanlar sadece küçük terminal/mikrodelesyonlardır."},
            {"title": "İnterkalar Kırıkta Sentromer", "desc": "Kopan iki kırık arası parça sentromersizse (asentrik) yok olur; sentromerli gövde iki ucundan birleşerek kendini hücrede gösterir."}
        ],
        "table": {
            "title": "Dr. Öğr. Üyesi Serap Arslan Amfi Dersi Mikrodelesyon / Mikroduplikasyon Sendromları Tablosu",
            "headers": ["Sendrom Adı", "Kromozomal Bölge", "Anomali Tipi", "Karakteristik Klinik Bulgular"],
            "rows": [
                ["Cri du Chat Sendromu", "5p15.2 - p15.3", "Delesyon (terminal)", "Kedi feryadı ağlama, mikrosefali, ay dede yüzü, hipotoni"],
                ["Wolf-Hirschhorn Sendromu", "4p16.3", "Delesyon (terminal)", "Grek miğferi yüzü, belirgin glabella, balık ağzı, ağır MR"],
                ["DiGeorge Sendromu (VCFS)", "22q11.2", "Delesyon (interkalar)", "Timus aplazisi (T hücre yetmezliği), hipokalsemi, konotrunkal kalp defekti"],
                ["Cat-Eye Sendromu", "22q11", "Duplikasyon (tetrazomi)", "Oküler kolobom, anal atrezi, preauriküler fistüller"],
                ["Williams Sendromu", "7q11.23", "Delesyon (ELN geni)", "Elfin yüzü, supravalvüler aort darlığı, kokteyl kişiliği, hiperkalsemi"],
                ["Smith-Magenis Sendromu", "17p11.2", "Delesyon (RAI1 geni)", "Uyku ritm bozukluğu (ters melatonin), kendini kucaklama, öfke nöbetleri"],
                ["Prader-Willi / Angelman", "15q11 - q13", "Delesyon / UPD", "PWS: İnfantil hipotoni, hiperfaji/obezite; AS: Gülme nöbetleri, ataksi"],
                ["Herediter Basınca Duyarlı Nöropati (HNPP)", "17p12", "Delesyon (PMP22)", "Tekrarlayan bası nöropatileri, geçici pleksopatiler"],
                ["Charcot-Marie-Tooth Tip 1A (CMT1A)", "17p12", "Duplikasyon (PMP22)", "Dismiyelinizan polinöropati, pes kavus, distal kas atrofisi"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-11",
                "question": "5p15.2 delesyonu hangi sendroma yol açar ve laringeal hipoplaziye bağlı tipik infant bulgusu nedir?",
                "answer": "Cri du chat (Kedi Ağlaması) sendromuna yol açar; tipik bulgusu bebeklikte tiz kedi miyavlamasını andıran ağlama sesidir.",
                "hint": "Cri du chat, kedi miyavlaması."
            },
            {
                "id": "fc-ch-12",
                "question": "17p12 bölgesindeki PMP22 geninin delesyonu ve duplikasyonu sırasıyla hangi iki farklı nörolojik hastalığı doğurur?",
                "answer": "17p12 delesyonu = Herediter Basınca Duyarlı Nöropati (HNPP); 17p12 duplikasyonu = Charcot-Marie-Tooth Tip 1A (CMT1A).",
                "hint": "HNPP (delesyon) vs CMT1A (duplikasyon)."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Duplikasyonlar ve Eşit Olmayan Krossing-Over (Unequal Crossing Over)",
        "subtitle": "Kromozom segment trizomisi, mayotik hiza kayması ve kopya sayısı varyasyonları",
        "badge": "Yapısal: Duplikasyon",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["duplikasyon", "unequal crossing over", "krossing over", "eşitsiz krossing over"],
        "lead": "Duplikasyon bir kromozom segmentinin fazladan bir kopyasının bulunmasıdır; ilgili segment açısından kısmi (parsiyel) trizomi yaratır.",
        "spotPearls": [
            "EŞİT OLMAYAN KROSSİNG OVER (UNEQUAL CROSSING OVER): Duplikasyonlar en sık Mayoz I profazında dizi benzerliği olan homolog bölgelerin (düşük kopya tekrarları - LCR) yanlış hizalanması ve eşit olmayan krossing-over yapmasıyla meydana gelir.",
            "AYNI ANDA DELİSYON VE DUPLİKASYON: Eşit olmayan krossing-over gerçekleştiğinde kardeş kromatitlerin birinde duplikasyon oluşurken eşleniğinde zorunlu olarak delesyon oluşur!",
            "KLİNİK ETKİ DELİSYONDAN DAHA HAFİF: Fazlalık (duplikasyon) eksilmeye (delesyona) kıyasla hücresel mekanizmalar tarafından daha iyi tolere edilir; ancak gamet aktarımında ağır fenotipler doğurabilir.",
            "MİKRODUPLİKASYONLARIN TESPİTİ: Submikroskobik duplikasyonlar klasik mikroskopta görülemez; moleküler sitogenetik (Array CGH, MLPA) şarttır."
        ],
        "keyBullets": [
            {"title": "Tandem vs Ters Duplikasyon", "desc": "Kopya parçanın aynı yönelimle ardışık eklenmesi (tandem) veya 180 derece ters dönerek eklenmesi (inverted) şeklinde olabilir."},
            {"title": "Gamet Anomalisi Riski", "desc": "Duplikasyon taşıyıcısı bireyler mayotik sinapsis esnasında ilmek (loop) oluşturmak zorunda kalır ve bu durum ayrılmama riskini artırır."},
            {"title": "Evrimsel ve Patolojik Rol", "desc": "Gen duplikasyonları evrimde yeni gen aileleri yaratırken günümüz tıbbında otizm ve gelişimsel geriliklerin önemli bir nedenidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-13",
                "question": "Mayoz bölünmede eşit olmayan krossing-over (unequal crossing-over) gerçekleştiğinde kromatitlerde hangi iki yapısal sonuç aynı anda doğar?",
                "answer": "Kromatitlerden birinde duplikasyon meydana gelirken diğer kromatitte delesyon meydana gelir.",
                "hint": "Birinde fazlalık (duplikasyon), diğerinde eksiklik (delesyon)."
            },
            {
                "id": "fc-ch-14",
                "question": "Klinik etki bakımından duplikasyonlar ile delesyonlar karşılaştırıldığında genel biyolojik kural nedir?",
                "answer": "Kural olarak delesyonlar (monozomi etkisi) duplikasyonlara (trizomi etkisi) oranla fenotipik olarak çok daha ağır ve letal seyreder.",
                "hint": "Delesyon daima daha ağırdır."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "İnversiyonlar: Parasentrik ve Perisentrik İnversiyon Ayrımı",
        "subtitle": "Sentromer varlığı, 180 derece dönme, mayotik ilmek ve asentrik/disentrik riskleri",
        "badge": "Yapısal: İnversiyon",
        "badgeColor": "cyan",
        "target_ids": [],
        "keywords": ["inversiyon", "parasentrik", "perisentrik", "sentromer", "inversiyon ilmeği"],
        "lead": "İnversiyon tek bir kromozomda iki kırık oluşması ve kırılan segmentin 180 derece ters dönerek aynı yere yeniden birleşmesiyle meydana gelen dengeli bir yapısal anomalidir.",
        "spotPearls": [
            "PARASENTRİK İNVERSİYON (Sentromersiz): İnversiyona uğrayan segment sentromeri İÇERMEZ, kromozomun tek bir kolunda gerçekleşir (paracentric = sentromerin yanında).",
            "PERİSENTRİK İNVERSİYON (Sentromerli): İnversiyona uğrayan segment SENTROMERİ İÇERİR, kırık noktaları p ve q kollarındadır (pericentric = sentromeri çevreleyen).",
            "TAŞIYICIDA NORMAL FENOTİP: Dengeli yeniden düzenlenme olduğu için inversiyon taşıyıcıları fenotipik olarak tamamen normaldir; ancak sonraki nesle dengesiz gamet aktarma riski yüksektir.",
            "ASENTRİK VE DİSENTRİK KROMOZOM RİSKİ: Parasentrik inversiyon ilmeği içinde krossing-over olursa asentrik (sentromersiz) ve disentrik (çift sentromerli) kromatitler oluşur; bunlar embriyoda kesinlikle yaşamla bağdaşmaz ve erken düşüklere yol açar."
        ],
        "keyBullets": [
            {"title": "İnversiyon İlmeği (Loop)", "desc": "Mayozda homolog kromozomların karşılıklı gelebilmesi için inversiyonlu bölgenin ters kıvrılarak ilmek oluşturması şarttır."},
            {"title": "Perisentrik Krossing-Over Sonucu", "desc": "Perisentrik ilmek içi krossing-overda her iki kromatit birer sentromere sahip olur ancak duplikasyon ve delesyonlu dengesiz gametler doğar."},
            {"title": "En Sık Perisentrik Varyant", "desc": "9. kromozom perisentrik inversiyonu [inv(9)(p11q13)] toplumda en sık görülen normal sitogenetik polimorfizm kabul edilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-15",
                "question": "Parasentrik inversiyon ile perisentrik inversiyon arasındaki temel sitogenetik fark nedir?",
                "answer": "Parasentrik inversiyonda ters dönen segment sentromer içermez (tek kolda kalır); perisentrik inversiyonda segment sentromeri içerir (p ve q kollarını kapsar).",
                "hint": "Sentromer varlığı: Para=yok, Peri=var."
            },
            {
                "id": "fc-ch-16",
                "question": "Parasentrik inversiyon taşıyıcısı bir bireyde mayotik krossing-over sonrası oluşan asentrik ve disentrik kromatitlerin embriyodaki klinik akıbeti nedir?",
                "answer": "Asentrik ve disentrik yapılar hücre bölünmesini sürdüremediğinden kesinlikle yaşamla bağdaşmaz ve erken spontan abortusla (düşükle) sonuçlanır.",
                "hint": "Yaşamla bağdaşmaz, erken fetal kayıp."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Resiprokal Translokasyonlar ve Segregasyon Modelleri",
        "subtitle": "Homolog olmayan kromozomlar arası transfer, 46 kromozom, kuadrivalan ve 2:2 segregasyonu",
        "badge": "Yapısal: Translokasyon",
        "badgeColor": "emerald",
        "target_ids": [],
        "keywords": ["resiprokal translokasyon", "translokasyon", "segregasyon", "kuadrivalan"],
        "lead": "Resiprokal translokasyon homolog olmayan iki kromozom arasında karşılıklı parça değişimiyle gerçekleşir; toplam kromozom sayısı 46 olarak korunur.",
        "spotPearls": [
            "TAŞIYICIDA DENGELİ KARYOTİP: Resiprokal translokasyon taşıyıcılarında gen kaybı veya fazlalığı olmadığından fenotipik etki oluşmaz; bireyler sağlıklıdır.",
            "TANI KOYULMA ZAMANI: Taşıyıcılar en sık tekrarlayan spontan düşük (fetal kayıp), açıklanamayan infertilite veya malforme/dengesiz çocuk sahibi olma öyküsü araştırılırken tespit edilir.",
            "ÜÇ SEGREGASYON MODELİ: Translokasyon taşıyıcısında mayotik kuadrivalan yapı 3 çeşit segregasyon gösterir: 1) 2:2 segregasyonu (en sık görülen), 2) 3:1 segregasyonu, 3) 4:0 segregasyonu.",
            "2:2 SEGREGASYON ALT TİPLERİ: Alternatif segregasyon normal veya dengeli taşıyıcı gamet oluştururken; Adjacent-1 ve Adjacent-2 segregasyonları parsiyel trizomi/monozomili letal dengesiz gametler üretir."
        ],
        "keyBullets": [
            {"title": "Kuadrivalan (Dörtlü) Haç Şekli", "desc": "Mayoz I profazında 4 kromozomun homolog bölgeleri bir araya gelerek haç biçiminde kuadrivalan yapı oluşturur."},
            {"title": "Tekrarlayan Gebelik Kaybı Paneli", "desc": "İki veya daha fazla habitüel düşüğü olan çiftlerde ilk istenecek genetik test ebeveyn periferik kan karyotip analizidir."},
            {"title": "Prenatal Danışma İhtiyacı", "desc": "Dengeli resiprokal translokasyon taşıyıcısı çiftlere gebelikte mutlaka CVS/Amniyosentez veya tüp bebekte PGT önerilmelidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-17",
                "question": "Resiprokal translokasyon taşıyıcısı bireyler klinik genetik polikliniklerine en sık hangi şikayet ve öykü ile başvururlar?",
                "answer": "Tekrarlayan spontan fetal kayıplar (habitüel düşükler), infertilite veya konjenital anomalili bebek sahibi olma öyküsü ile başvururlar.",
                "hint": "Tekrarlayan düşükler ve infertilite."
            },
            {
                "id": "fc-ch-18",
                "question": "Mayoz bölünmede resiprokal translokasyon kuadrivalanının gösterdiği 3 temel segregasyon modeli hangileridir ve en sık hangisi gözlenir?",
                "answer": "1) 2:2 segregasyonu (en sık), 2) 3:1 segregasyonu, 3) 4:0 segregasyonu.",
                "hint": "2:2 (en sık), 3:1 ve 4:0."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Robertsonyan Translokasyonlar (Akrosentrik Füzyon)",
        "subtitle": "13, 14, 15, 21, 22 kromozomları, 45 kromozom kuruluşu, rob(14;21) ve rekürrens riskleri",
        "badge": "Yapısal: Robertsonyan",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["robertsonian", "robertsonyan", "akrosentrik", "rob(14;21)", "rob(13;14)"],
        "lead": "Robertsonyan translokasyon yalnızca akrosentrik kromozomlar (13, 14, 15, 21, 22) arasında gerçekleşen, kısa kolların kaybı ve uzun kolların sentromerden birleşmesiyle oluşan özel bir sentrik füzyondur.",
        "spotPearls": [
            "EN YAYGIN YAPISAL ANOMALİ (1/500): Robertsonyan translokasyon tüm insan yapısal kromozom anomalilerinin en yaygın tipidir (toplumda 1/500 sıklık).",
            "45 KROMOZOM KURULUŞU: İki akrosentrik kromozom birleştiğinde toplam kromozom sayısı 45'e düşer; kaybolan kısa kollar sadece yedekli ribozomal RNA (rRNA) ve satellit DNA içerdiğinden FENOTİPİK ETKİ YARATMAZ ve dengeli kabul edilir.",
            "EN SIK FORMLAR: 1) rob(13;14)(q10;q10) [1/1300 sıklıkta, en sık], 2) rob(14;21)(q10;q10) [Down sendromu riski taşıyan en önemli form].",
            "ANNE VS BABA TAŞIYICILIK RİSKİ: rob(14;21) taşıyıcısı ANNE ise Down sendromlu çocuk doğurma riski %10-15 iken; BABA taşıyıcı ise bu risk %4-5 düzeyindedir!",
            "HOMOLOG ROB(21;21) FACİASI: rob(21;21) taşıyıcısı bir ebeveynin normal çocuk sahibi olma şansı %0'dır; canlı doğan tüm gebelikleri %100 DOWN SENDROMLU olur!"
        ],
        "keyBullets": [
            {"title": "Akrosentrik Kromozom Beşlisi", "desc": "İnsan genomunda yalnızca 13, 14, 15, 21 ve 22. kromozomlar akrosentriktir ve satellit kısa kollara sahiptir."},
            {"title": "Görünürde Dengeli 45 Karyotip", "desc": "Karyotip yazımı örneğin kadın için 45,XX,rob(14;21)(q10;q10) şeklindedir; genetik danışmada kritik öneme sahiptir."},
            {"title": "Sperm Seçilimi Avantajı", "desc": "Babanın dengesiz gametlerinin (disomik sperm) döllenme kapasitesi oosite göre daha düşük olduğundan babadaki risk (%4-5) anneden düşüktür."}
        ],
        "table": {
            "title": "Robertsonyan Translokasyon vs Resiprokal Translokasyon Karşılaştırması",
            "headers": ["Özellik", "Robertsonyan Translokasyon", "Resiprokal Translokasyon"],
            "rows": [
                ["İlgili Kromozomlar", "SADECE Akrosentrikler (13, 14, 15, 21, 22)", "Tüm otozomlar ve gonozomlar arasında olabilir"],
                ["Kırık Noktaları", "Sentromerik / perisentromerik bölge", "Herhangi bir kromozom kolunda iki kırık"],
                ["Taşıyıcı Kromozom Sayısı", "45 kromozom (sentrik füzyon ile)", "46 kromozom (sayı değişmez)"],
                ["Kısa Kol Akıbeti", "Kısa kollar (p) koparak kaybolur (satellit RNA)", "Parçalar karşılıklı yer değiştirir, kayıp yoktur"],
                ["Toplum Sıklığı", "1/500 (En sık yapısal anomali)", "Yaklaşık 1/700 yenidoğan"],
                ["Down Sendromu Riski", "rob(14;21): Anne %10-15, Baba %4-5; rob(21;21): %100", "Spesifik translokasyon lokusuna bağlı değişken"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-19",
                "question": "Robertsonyan translokasyon hangi kromozomlar arasında gerçekleşebilir ve dengeli bir taşıyıcının karyotipinde kaç kromozom bulunur?",
                "answer": "Yalnızca akrosentrik kromozomlar (13, 14, 15, 21 ve 22) arasında gerçekleşir; dengeli bir taşıyıcıda 45 kromozom bulunur.",
                "hint": "Akrosentrikler (13, 14, 15, 21, 22) ve 45 kromozom."
            },
            {
                "id": "fc-ch-20",
                "question": "rob(14;21) taşıyıcısı anne ve babanın Down sendromlu çocuk sahibi olma riskleri yüzde kaçtır ve rob(21;21) taşıyıcısında bu oran ne kadardır?",
                "answer": "Anne taşıyıcıysa risk %10-15, baba taşıyıcıysa %4-5'tir; homolog rob(21;21) taşıyıcısında ise risk tam %100'dür.",
                "hint": "Anne %10-15, baba %4-5, rob(21;21) %100."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "İzokromozom, Ring ve Marker Kromozomlar",
        "subtitle": "Ayna simetrisi, i(Xq) Turner, halka instabilitesi ve mozaik süpernumerer marker kromozomlar",
        "badge": "Yapısal: İzo/Ring/Marker",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["izokromozom", "i(Xq)", "ring kromozom", "marker kromozom", "halka"],
        "lead": "İzokromozom, halka (ring) ve marker kromozomlar kompleks kromozomal kırılma ve sentromer bölünme kusurlarından kaynaklanan dengesiz yapısal bozukluklardır.",
        "spotPearls": [
            "İZOKROMOZOM MEKANİZMASI: Sentromerin uzunlamasına (boyuna) değil ENLEMESİNE (yatay) bölünmesi sonucu bir kolun tamamen kaybolması ve diğer kolun ayna simetrisi şeklinde iki kopyaya çıkmasıdır (parsiyel monozomi + parsiyel trizomi).",
            "EN SIK İZOKROMOZOM: En sık gözlenen izokromozom X kromozomu uzun kol izokromozomudur: i(Xq); Turner sendromu olgularının %15'ini oluşturur.",
            "RING (HALKA) KROMOZOM: Bir kromozomun p ve q kollarında eşzamanlı oluşan kırık uçlarının dairesel şekilde birleşmesidir; mitozda anafaz kopmalarına yol açtığından dinamik instabilite ve mozaik karyotiplere neden olur.",
            "MARKER KROMOZOM: Klasik G-bantlama ile tanınamayan ekstra küçük kromozomlardır (prenatal sıklık 1/2500); büyük kısmı 15. kromozom veya cinsiyet kromozomlarından köken alır, köken tayini için FISH veya Microarray şarttır."
        ],
        "keyBullets": [
            {"title": "İzokromozomda Dozaj Fırtınası", "desc": "Örneğin i(Xq)'da kısa kol (Xp) tamamen eksiktir (monozomik), uzun kol (Xq) ise fazladan mevcuttur (trizomik)."},
            {"title": "Halka Kromozom Telomer Kaybı", "desc": "Ring oluşumu için iki telomer bölgesinin de kırılıp dökülmesi gerekir; telomersiz 'yapışkan' uçlar birleşir."},
            {"title": "Marker Kromozom Fenotip Belirsizliği", "desc": "Marker ökromatik (aktif gen) içeriyorsa ağır sendrom yaratırken heterokromatin (satellit DNA) içeriyorsa sessiz kalabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-21",
                "question": "İzokromozom oluşumunun sitogenetik mekanizması nedir ve klinikte en sık karşılaşılan izokromozom örneği hangisidir?",
                "answer": "Sentromerin enlemesine (yatay) hatalı bölünmesiyle bir kolun silinip diğer kolun çiftlenmesidir; en sık örnek Turner sendromunda görülen i(Xq)'dur.",
                "hint": "Sentromerin enlemesine bölünmesi, i(Xq) Turner."
            },
            {
                "id": "fc-ch-22",
                "question": "Halka (ring) kromozomların hücre bölünmelerinde dinamik instabiliteye ve mozaik karyotiplere yol açmasının temel nedeni nedir?",
                "answer": "Mitoz anafazında kromatitlerin ayrılırken birbirine dolanması, kırılması ve eşit olmayan dağılarak hücre soy hatlarında farklı karyotipler doğurmasıdır.",
                "hint": "Mitozda anafaz dolanması ve kopmalar."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Down Sendromu (Trizomi 21): Genetik Etiyoloji ve Karyotip Dağılımı",
        "subtitle": "1/660 canlı doğum, %95 klasik trizomi (maternal yaş), %4 translokasyon, %1 mozaiklik",
        "badge": "Down Sendromu",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["down sendromu", "trizomi 21", "maternal yaş", "translokasyon down", "mozaik down"],
        "lead": "Down sendromu (Trizomi 21) kromozomal hastalıkların en sık ve en iyi bilinen sebebi olup orta derece zeka geriliğinin en yaygın genetik nedenidir (1/660 canlı doğum).",
        "spotPearls": [
            "KLASİK TRİZOMİ 21 (%95): Olguların %95'i mayotik ayrılmamadan (non-disjunction) kaynaklanır; bu ayrılmamanın %90'ı MATERNAL, %10'u PATERNAL kaynaklıdır ve doğrudan ARTAN ANNE YAŞI ile ilişkilidir.",
            "TRANSLOKASYON TİPİ (%4): 21. kromozom ile başka bir akrosentrik (genellikle 14 veya 22) arasındaki Robertsonyan translokasyondur; ARTAN ANNE YAŞINA BAĞLI DEĞİLDİR, ebeveyn karyotipi şarttır!",
            "MOZAİK TİP (%1): Postzigotik mitotik ayrılmama sonucu oluşur; fenotip klasik tipe oranla çok daha hafiftir ve tutulan doku oranına göre geniş çeşitlilik gösterir.",
            "PRENATAL ELENME: Trizomi 21'li gebeliklerin yalnızca %20-25'i canlı doğuma ulaşabilir; %75-80'i intrauterin dönemde spontan abortusla kaybedilir."
        ],
        "keyBullets": [
            {"title": "Maternal Yaş Eşiği", "desc": "35 yaş üzeri gebeliklerde oosit yaşlanmasına bağlı kiyazma çözülmeleri ve iğ ipliği instabilitesi riski katlayarak artırır."},
            {"title": "Translokasyonda Parental Analiz", "desc": "Translokasyonlu Down bebek doğduğunda ebeveynlerin taşıyıcı olup olmadığı belirlenmeden asla tekrarlama riski verilemez."},
            {"title": "Fakülte Karyotipleme Prensibi", "desc": "Klinik tanı ne kadar net olursa olsun genetik danışma ve sonraki gebelik planı için kesinlikle KARYOTİP DOĞRULAMASI şarttır."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-23",
                "question": "Down sendromunda etiyolojik karyotip dağılım yüzdeleri nelerdir ve klasik formda ebeveyn kökeni nasıldır?",
                "answer": "%95 Klasik Trizomi 21 (%90 maternal, %10 paternal mayotik ayrılmama), %4 Robertsonyan Translokasyon, %1 Mozaik Down Sendromu.",
                "hint": "%95 klasik (%90 anne), %4 translokasyon, %1 mozaik."
            },
            {
                "id": "fc-ch-24",
                "question": "Klasik Trizomi 21 ile Robertsonyan translokasyona bağlı Trizomi 21 arasındaki en kritik epidemiyolojik fark nedir?",
                "answer": "Klasik Trizomi 21 doğrudan artan anne yaşı ile ilişkili iken; Translokasyon tipi Down sendromu anne yaşından tamamen bağımsızdır.",
                "hint": "Translokasyon anne yaşından bağımsızdır."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Down Sendromu: Dismorfik Bulgular ve Tipik Fenotipik Özellikler",
        "subtitle": "Yenidoğan hipotonisi, brakisefali, Brushfield lekeleri, Simian çizgisi, sandal gap",
        "badge": "Down: Fenotip",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["down fenotip", "brushfield", "simian çizgisi", "hipotoni", "sandal gap"],
        "lead": "Down sendromunda tanı çoğunlukla doğum odasında dismorfik yüz, el ve ayak bulguları ile ilk dikkati çeken şiddetli yenidoğan hipotonisi sayesinde klinik olarak konur.",
        "spotPearls": [
            "YENİDOĞANDA İLK BULGU: Hipotoni (kurbağa pozisyonu, gevşek bebek) doğumda ilk dikkati çeken ve hekimi uyaran en temel klinik bulgudur.",
            "KRANİYOFASYAL DİSMORFOLOJİ: Düz oksiput, brakisefali, basık burun kökü, küçük düşük yerleşimli ve kıvrılmış kulaklar, yukarı çekik (upslanting) palpebral fissürler, epikantal kıvrımlar, açık ağız ve dışarı taşan dil (makroglossi), diş hipoplazisi.",
            "BRUSHFIELD LEKELERİ: Göz muayenesinde iris kenarına yakın yerleşimli çevresel beyaz/gri beneklenmeler (Brushfield lekeleri) patognomoniktir.",
            "EL VE AYAK BULGULARI: Kısa geniş eller, tek transvers palmar çizgi (SİMİAN ÇİZGİSİ), 5. parmakta klinodaktili ve midfalanks hipoplazisi; Ayaklarda 1. ve 2. parmaklar arasında geniş boşluk (SANDAL GAP / WIDE GAP) ve proksimale uzanan derin cilt oluğu."
        ],
        "keyBullets": [
            {"title": "Gevşek Ense Cildi", "desc": "Yenidoğanda ense cildinin kalın ve kıvrımlı olması fetal ultrasonografideki artmış ense saydamlığı (NT) ile koreledir."},
            {"title": "IQ Spektrumu", "desc": "Çocukluk çağında test edilebilir yaşa ulaşıldığında IQ genellikle 30-60 arasındadır; mutlu ve sosyal iletişimleri kuvvetlidir."},
            {"title": "Büyüme Eğrileri", "desc": "Down sendromlu çocukların boy uzaması ve baş çevresi standart persentil eğrilerinin altında seyreder, özel Down büyüme eğrileri kullanılır."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-25",
                "question": "Down sendromlu bir yenidoğanda doğumda ilk dikkati çeken nörolojik bulgu ve göz irisinde görülen patognomonik lezyon nedir?",
                "answer": "İlk dikkati çeken nörolojik bulgu jeneralize hipotoni; iriste görülen lezyon ise Brushfield lekeleridir.",
                "hint": "Hipotoni ve Brushfield lekeleri."
            },
            {
                "id": "fc-ch-26",
                "question": "Down sendromunda el ve ayakta görülen en karakteristik 3 fizik muayene bulgusu nedir?",
                "answer": "1) Avuç içinde tek yatay çizgi (Simian çizgisi), 2) 5. parmak klinodaktilisi ve midfalanks hipoplazisi, 3) Ayak 1-2. parmak arası geniş boşluk (sandal gap / wide gap) ve derin taban oluğu.",
                "hint": "Simian çizgisi, klinodaktili, sandal gap."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Down Sendromu: Sistemik Komplikasyonlar ve Klinik Takip",
        "subtitle": "AVSD, duodenal atrezi, 15 kat artmış lösemi, atlantoaksiyel instabilite ve erken Alzheimer",
        "badge": "Down: Komplikasyonlar",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["avsd", "endokardiyal yastık", "duodenal atrezi", "down lösemi", "atlantoaksiyel"],
        "lead": "Down sendromunda mortalite ve morbiditeyi belirleyen en önemli etkenler konjenital kalp defektleri, gastrointestinal atreziler, immünolojik yetmezlik ve hematolojik neoplazilerdir.",
        "spotPearls": [
            "1 NUMARALI ERKEN ÖLÜM SEBEBİ: Konjenital kalp hastalıkları canlı doğanların 1/3'ünde görülür; en sık lezyon Endokardiyal Yastık Defekti (Atriyoventriküler Septal Defekt - AVSD)'dir ve erken bebeklik ölümlerinin baş sorumlusudur.",
            "GİS MALFORMASYONLARI: Duodenal atrezi ('çift kabarcık / double bubble' manzarası), trakeoözofageal fistül ve Hirschsprung hastalığı sıklığı dramatik şekilde artmıştır.",
            "LÖSEMİDE 15 KAT ARTIŞ: Akut lösemi (özellikle ALL ve Akut Megakaryoblastik Lösemi / AML-M7) gelişme riski genel topluma göre 15 KAT artmıştır; ayrıca yenidoğanda geçici miyeloproliferatif hastalık (TMD) görülebilir.",
            "DİĞER KRİTİK KOMPLİKASYONLAR: Atlantoaksiyel subluksasyon (servikal omurilik basısı riski!), konjenital hipotiroidizm, çölyak hastalığı, katarakt, işitme kaybı ve 40 yaş sonrası erken başlayan Alzheimer Hastalığı (APP geni 21. kromozomdadır!)."
        ],
        "keyBullets": [
            {"title": "Atlantoaksiyel Grafi Şartı", "desc": "Down sendromlu çocuklar spora veya anesteziye girmeden önce C1-C2 instabilitesi açısından servikal grafi ile taranmalıdır."},
            {"title": "Tiroid Taraması", "desc": "Hipotiroidizm büyüme ve bilişsel gelişimi daha da baskılayacağından yıllık TSH ve serbest T4 takibi zorunludur."},
            {"title": "Alzheimer Patofizyolojisi", "desc": "21. kromozomda yer alan Amiloid Prekürsör Protein (APP) geninin 3 kopya olması 40'lı yaşlarda beyinde yaygın amiloid plak birikimine yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-27",
                "question": "Down sendromlu bebeklerde erken dönem ölümlerin en sık sebebi olan kardiyak malformasyon hangisidir?",
                "answer": "Endokardiyal Yastık Defekti (Atriyoventriküler Septal Defekt - AVSD) olup hastaların yaklaşık üçte birinde görülür.",
                "hint": "Endokardiyal yastık defekti (AVSD)."
            },
            {
                "id": "fc-ch-28",
                "question": "Down sendromunda hematolojik olarak hangi malignite riski kaç kat artmıştır ve 40 yaş sonrası erken ortaya çıkan nörodejeneratif tablo nedir?",
                "answer": "Akut lösemi riski 15 kat artmıştır; nörodejeneratif tablo ise erken başlangıçlı Alzheimer hastalığıdır (APP gen dozajı artışı).",
                "hint": "15 kat lösemi ve Alzheimer."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Edwards Sendromu (Trizomi 18): Patofizyoloji ve Klinik Spektrum",
        "subtitle": "1/750 canlı doğum, %95 fetal kayıp, %80 kız, clenched hand, rocker-bottom ve belirgin oksiput",
        "badge": "Edwards: Trizomi 18",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["edwards", "trizomi 18", "clenched hand", "rocker bottom", "fırlak topuk"],
        "lead": "Edwards sendromu (Trizomi 18) Down sendromundan sonra canlı doğumlarda en sık görülen ikinci otozomal trizomidir; ağır çoklu organ malformasyonları nedeniyle olguların %95'i intrauterin dönemde düşükle sonuçlanır.",
        "spotPearls": [
            "İNSİDANS VE SAĞKALIM: Canlı doğumlarda 1/750 sıklıkta görülür; canlı doğanların %50'si ilk hafta içinde, %90'ı ise ilk yıl içinde kaybedilir. Yaşayan olguların %80'i kızdır.",
            "PATOGNOMONİK EL: 'CLENCHED HAND' (Kenetlenmiş el) manzarası; 2. ve 5. parmakların 3. ve 4. parmaklar üzerine bindiği karakteristik fleksiyon kontraktürü tipiktir.",
            "PATOGNOMONİK AYAK: 'ROCKER-BOTTOM' (Beşik taban / fırlak topuk) ayağı; belirgin kalkaneus ve halluks (başparmak) dorsifleksiyonu eşlik eder.",
            "DİĞER KLİNİK TRİADLAR: Belirgin oksiput, mikrognati, düşük ve malforme kulaklar; yenidoğanda HİPERTONİSİTE (Down'daki hipotoninin tam tersi!); tek umbilikal arter ve ağır konjenital kalp defektleri (VSD, PDA, ASD)."
        ],
        "keyBullets": [
            {"title": "Maternal Yaş Faktörü", "desc": "%70'i normal ebeveynden mayotik non-disjunction (%95 maternal kökenli) ile doğar ve 35 yaş üstünde sıklığı katlanır."},
            {"title": "İntrauterin Belirteçler", "desc": "Azalmış fetal hareketler, küçük plasenta, polihidramniyoz veya oligohidramniyoz ve şiddetli simetrik İUGG tipiktir."},
            {"title": "Mozaik Trizomi 18", "desc": "Olguların %10'undan azı mozaiktir; bu grupta kliniğin şiddeti daha hafif olup çocukluk çağına sağkalım mümkündür."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-29",
                "question": "Edwards sendromunda (Trizomi 18) el ve ayakta görülen en karakteristik iki patognomonik muayene bulgusu nedir?",
                "answer": "Elde: Clenched hand (2. ve 5. parmakların 3. ve 4. üzerine bindiği kenetlenmiş yumruk); Ayakta: Rocker-bottom (beşik taban / fırlak topuk) deformitesi.",
                "hint": "Clenched hand ve rocker-bottom ayak."
            },
            {
                "id": "fc-ch-30",
                "question": "Yenidoğan kas tonusu açısından Down sendromu ile Edwards sendromu arasındaki temel klinik zıtlık nedir?",
                "answer": "Down sendromlu yenidoğanlar tipik olarak hipotonik (gevşek bebek) iken; Edwards sendromlu yenidoğanlar belirgin hipertonik (spastik/kasılmış) seyreder.",
                "hint": "Down = Hipotoni; Edwards = Hipertoni."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Patau Sendromu (Trizomi 13): Klinik Triad ve Santral Sinir Sistemi Defektleri",
        "subtitle": "1/5000 canlı doğum, holoprozensefali, mikroftalmi + yarık damak + polidaktili triadı, cutis aplasia",
        "badge": "Patau: Trizomi 13",
        "badgeColor": "purple",
        "target_ids": [],
        "keywords": ["patau", "trizomi 13", "holoprozensefali", "mikroftalmi", "cutis aplasia"],
        "lead": "Patau sendromu (Trizomi 13) canlı doğumla bağdaşan otozomal trizomilerin en ağır ve fatal olanıdır (1/5000 canlı doğum); canlı doğan bebeklerin %90'ı ilk 1 yıl içinde kaybedilir.",
        "spotPearls": [
            "KLASİK PATOGNOMONİK TRİAD: 1) MİKROFTALMİ / ANOFTALMİ, 2) YARIK DUDAK VE DAMAK (sıklıkla orta hat yarıkları), 3) POSTAKSİYEL POLİDAKTİLİ. Bu üçlü Trizomi 13 için karakteristiktir.",
            "SANTRAL SİNİR SİSTEMİ FELAKETİ: Ön beyin, olfaktör loblar ve optik kadehlerin iki hemisfer şeklinde ayrılamamasıyla karakterize HOLOPROZENSEFALİ görülür.",
            "DERİ VE KRANİYUM BULGULARI: Oksipital saçlı deride lokalize deri yokluğu defekti (CUTİS APLASİA / CUTİS CONGENİTA) ve alında kapiller hemanjiomlar çok tipiktir.",
            "DİĞER ANOMALİLER: Omfalosel, polikistik/displastik böbrekler, konjenital kalp anomalileri (VSD, PDA) ve mikrosefali."
        ],
        "keyBullets": [
            {"title": "Etiyolojik Dağılım", "desc": "%80 olgu klasik mayotik non-disjunction ile, %20 olgu ise Robertsonyan translokasyonla [özellikle rob(13;14)] ortaya çıkar."},
            {"title": "Düşük Materyali Sıklığı", "desc": "Spontan abortus materyallerinin kromozom analizinde Trizomi 13 oranı %15'lere kadar çıkar."},
            {"title": "Pediatrik Yönetim", "desc": "Ağır MSS ve kardiyorespiratuar malformasyonlar nedeniyle palyatif destek ön plandadır; cerrahi kararlar multidisipliner verilir."}
        ],
        "table": {
            "title": "Üç Büyük Canlı Doğan Otozomal Trizominin Kapsamlı Karşılaştırması",
            "headers": ["Özellik", "Down Sendromu (Trizomi 21)", "Edwards Sendromu (Trizomi 18)", "Patau Sendromu (Trizomi 13)"],
            "rows": [
                ["Canlı Doğum Sıklığı", "1/660 (En sık)", "1/750", "1/5000 (En nadir ve en ağır)"],
                ["1 Yaş Sağkalımı", "%75-80 canlı kalır", "< %10 (Çoğu ilk haftalarda ölür)", "< %10 (İlk aylarda ölüm)"],
                ["Yenidoğan Tonusu", "Belirgin HİPOTONİ", "Belirgin HİPERTONİ", "Hipotoni / Değişken"],
                ["Patognomonik El/Ayak", "Simian çizgisi, klinodaktili, sandal gap", "Clenched hand (kenetlenmiş), rocker-bottom", "Postaksiyel polidaktili, sindaktili"],
                ["Karakteristik Baş/Yüz", "Brakisefali, basık burun, Brushfield", "Belirgin oksiput, mikrognati, düşük kulak", "Holoprozensefali, mikroftalmi, yarık damak"],
                ["Deri / Karın Bulgusu", "Gevşek ense cildi", "Küçük pelvis, tek umbilikal arter", "Cutis aplasia (saçlı deride defekt), omfalosel"],
                ["En Sık Kalp Defekti", "Endokardiyal Yastık Defekti (AVSD)", "VSD, PDA, ASD", "VSD, PDA, Kompleks defektler"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-31",
                "question": "Patau sendromu (Trizomi 13) için karakteristik kabul edilen klasik klinik triad hangi 3 bulgudan oluşur?",
                "answer": "1) Mikroftalmi (veya anoftalmi), 2) Yarık dudak ve damak, 3) Postaksiyel polidaktili.",
                "hint": "Mikroftalmi, yarık damak/dudak, polidaktili."
            },
            {
                "id": "fc-ch-32",
                "question": "Trizomi 13'te santral sinir sisteminde ön beyin ve olfaktör lob gelişimini vuran malformasyon ve saçlı deride görülen tipik doku defekti nedir?",
                "answer": "Santral sinir sistemi malformasyonu Holoprozensefali; saçlı derideki defekt ise Cutis Aplasia (cutis congenita)'dır.",
                "hint": "Holoprozensefali ve cutis aplasia."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Triploid Sendrom (69 Kromozom) ve Molar Gebelik Patolojisi",
        "subtitle": "Spontan düşüklerin %20'si, diandrik (parsiyel mol) vs dijinik triploidi, miksoploidi (2n/3n)",
        "badge": "Poliploidi: Triploidi",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-pat-052"],
        "keywords": ["triploid", "69 kromozom", "molar gebelik", "miksoploidi", "parsiyel mol"],
        "lead": "Triploid sendrom her hücrede fazladan bir tam haploid takım bulunması (3n=69) durumudur; insan spontan abortuslarının beşte birini oluşturan en dramatik sitogenetik anomalidir.",
        "spotPearls": [
            "DÜŞÜKLERDEKİ %20 PAYI: Triploidi tüm kromozomal spontan düşüklerin %20'sini oluşturur; full triploidi olguları nadiren canlı doğar ve saatler içinde kaybedilir.",
            "DİANDRİK TRİPLOİDİ (Baba Kaynaklı): Ekstra kromozom takımı babadan geldiğinde (genellikle dispermi ile 1 ovuma 2 sperm girişi) BÜYÜK PLASENTA VE HİDATİDİFORM MOL (Parsiyel Mol) değişiklikleri gelişir.",
            "DİJİNİK TRİPLOİDİ (Anne Kaynaklı): Ekstra takım anneden geldiğinde (diploid yumurta) plasenta çok küçük ve sklerotiktir; fetüste şiddetli asimetrik gelişme geriliği görülür.",
            "MİKSOPLOİDİ (2n/3n MOZAİKLİK): Miksoploid (diploid/triploid mozaik) olgular çocukluk veya erişkinliğe kadar yaşayabilir; asimetrik vücut büyüme farkı, sindaktili ve ambigus genitalya karakteristiktir."
        ],
        "keyBullets": [
            {"title": "Dispermi Engelleme Kusuru", "desc": "Oosit zarının polispermiyi engelleyen zona pellusida kortikal granül reaksiyonunun yetersiz kalması dispermiye yol açar."},
            {"title": "Serum Belirteçleri", "desc": "Diandrik triploidilerde trofoblast proliferasyonu nedeniyle maternal serum beta-hCG düzeyleri olağanüstü yüksek seyreder."},
            {"title": "Sindaktili Bulgusu", "desc": "Canlı doğan triploidi olgularında el parmaklarında (özellikle 3. ve 4. parmaklar arası) kutanöz sindaktili sık eşlik eder."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-33",
                "question": "Diandrik triploidi (paternal köken) ile dijinik triploidi (maternal köken) arasındaki plasental patoloji farkı nedir?",
                "answer": "Diandrik triploidide plasenta çok büyük, kistik ve hidatidiform molar yapıdadır; dijinik triploidide ise plasenta küçük, fibrotik ve atrofiktir.",
                "hint": "Diandrik = büyük molar plasenta; Dijinik = küçük atrofik plasenta."
            },
            {
                "id": "fc-ch-34",
                "question": "Miksoploidi (2n/3n mozaiklik) taşıyan ve postnatal dönemde yaşayan bireylerde en ayırt edici iki klinik bulgu nedir?",
                "answer": "Vücut yarıları arasında asimetrik büyüme farkı (hemihipertrofi) ve ambigus genitalyadır.",
                "hint": "Asimetrik büyüme ve ambigus genitalya."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Yapısal Parsiyel Delesyon Sendromları: Cri-du-chat ve Wolf-Hirschhorn",
        "subtitle": "5p15 delesyonu (5p15.3 ağlama, 5p15.2 klinik) vs 4p16.3 delesyonu (Grek miğferi yüzü)",
        "badge": "Yapısal: Delesyon Sendromları",
        "badgeColor": "purple",
        "target_ids": ["d3-k1-tbg-003"],
        "keywords": ["cri du chat", "wolf hirschhorn", "5p delesyon", "4p delesyon", "grek miğferi"],
        "lead": "Otozomal delesyon sendromları arasında en sık tanımlanan ve karakteristik kraniyofasyal fenotiplerle tanınan prototipler Cri-du-chat (5p-) ve Wolf-Hirschhorn (4p-) sendromlarıdır.",
        "spotPearls": [
            "CRİ DU CHAT (5p-): 5. kromozomun kısa kolundaki delesyondur: del(5)(p15.2). %85 de novo kırıkla, %15 parental dengeli translokasyon aktarımıyla meydana gelir.",
            "5p KRİTİK BÖLGE AYRIMI: Anormal larinks gelişimine bağlı kedi miyavlaması ağlama sesi 5p15.3 bölgesine; mikrosefali, yuvarlak yüz ve mental retardasyon gibi ana klinik bulgular ise 5p15.2 bölgesine aittir!",
            "AĞLAMANIN AKIBETİ: Kedi miyavlaması ağlama sesi infantil dönemde belirgindir, laringeal kıkırdak olgunlaştıkça erişkinlikte kaybolur.",
            "WOLF-HİRSCHHORN (4p-): 4p16.3 delesyonudur (1/50.000 doğum). 'GREK MİĞFERİ' yüz görünümü (geniş belirgin glabella, kaşların burun köküyle devam etmesi), balık ağzı görünümü, korpus kallozum agenezisi ve şiddetli mental gerilik ile karakterizedir; klasik karyotipte görülemeyebilir, FISH ile tanı konur."
        ],
        "keyBullets": [
            {"title": "Cri du Chat Kraniyofasiyal Bulgular", "desc": "Mikrosefali, yuvarlak dolunay yüzü, hipertelorizm, aşağıya çekik (downslanting) palpebral fissürler, mikrognati ve epikantus."},
            {"title": "Wolf-Hirschhorn Nörolojisi", "desc": "Tedaviye dirençli epileptik nöbetler, derin hipotoni, mikrosefali ve korpus kallozum displazisi hastaların %100'ünde görülür."},
            {"title": "FISH Endikasyonu", "desc": "Submikroskobik 4p delesyonlarında standart bantlama normal rapor edilse dahi klinik şüphede 4p16.3 spesifik FISH probu istenmelidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-35",
                "question": "Cri-du-chat sendromunda infantil kedi feryadı ağlamasından sorumlu olan ve diğer klinik bulgulardan sorumlu olan kritik 5p delesyon bantları sırasıyla hangileridir?",
                "answer": "Kedi ağlaması sesinden 5p15.3 bandı; dismorfik ve nörolojik klinik özelliklerden ise 5p15.2 bandı sorumludur.",
                "hint": "5p15.3 = ağlama; 5p15.2 = klinik özellikler."
            },
            {
                "id": "fc-ch-36",
                "question": "del(4)(p16.3) sonucu ortaya çıkan Wolf-Hirschhorn sendromunda yüz görünümünü tanımlayan klasik benzetme nedir?",
                "answer": "Geniş ve belirgin glabella ile burun kökünün birleştiği 'Grek savaş miğferi' (Greek warrior helmet) görünümüdür.",
                "hint": "Grek miğferi görünümü."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "Gonozomal Kromozom Hastalıkları: Klinefelter (47,XXY), 47,XYY ve 47,XXX",
        "subtitle": "Xp-Yp psödootozomal ayrılmama, ögonoid yapı, azospermi, jinekomasti, fertilite durumları",
        "badge": "Gonozomal: Trizomiler",
        "badgeColor": "cyan",
        "target_ids": ["d3-k1-tbg-014"],
        "keywords": ["klinefelter", "47 xxy", "47 xyy", "47 xxx", "azospermi", "jinekomasti"],
        "lead": "Gonozomal anöploidiler canlı doğumlarda en sık rastlanan kromozom bozuklukları olup otozomlara kıyasla çok daha hafif dismorfoloji ve mental fenotiple seyreder.",
        "spotPearls": [
            "KLİNEFELTER SENDROMU (47,XXY): 1/2000 canlı erkek doğum. Hastaların %50'sinde neden PATERNAL MAYOZ 1'de Xp-Yp psödootozomal bölgesindeki anormal rekombinasyon ve ayrılamamadır!",
            "KLİNEFELTER FENOTİPİ: Uzun boy, ince-uzun ekstremiteler (ögonoid yapı), puberteye kadar normal görünüm; pubertede küçük sert testisler, jinekomasti, eksik virilizasyon ve seminifer tübüllerde hiyalinizasyon/fibrozis.",
            "HORMON PROFİLİ VE İNFERTİLİTE: Testosteron düşük/normal iken LH ve FSH belirgin YÜKSEKTİR (hipergonadotropik hipogonadizm). Daima azospermi ve İNFERTİLDİRLER; ilk tanı genellikle infertilite araştırmasında konur.",
            "47,XYY SENDROMU: Paternal Mayoz II'de kardeş kromatitlerin ayrılamamasıyla (YY spermi) oluşur. Uzun boylu, iri yapılıdırlar, motor koordinasyonları zayıf olabilir; FERTİLİTELERİ NORMALDİR ve çocukları genelde sağlıklıdır!",
            "47,XXX SENDROMU: Maternal mayotik ayrılmama kaynaklıdır. Uzun boy, hafif konuşma/öğrenme güçlüğü görülebilir; pubertal gelişim ve FERTİLİTE GENELDE NORMALDİR."
        ],
        "keyBullets": [
            {"title": "Malignite Riski", "desc": "Klinefelter olgularında meme kanseri riski normal erkeklere göre 20-50 kat artmıştır; ayrıca ekstragonadal mediastinal germ hücre tümörleri riski yüksektir."},
            {"title": "Erken Hormon Replasmanı", "desc": "11-12 yaşlarında başlanan testosteron tedavisi sekonder cinsiyet karakterlerini geliştirir, osteoporozu ve kas zayıflığını önler."},
            {"title": "X Sayısı Kuralı", "desc": "48,XXXY veya 49,XXXXY varyantlarında eklenen her bir ekstra X kromozomu zeka geriliğini ve dismorfik bulguları daha da ağırlaştırır."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-37",
                "question": "Klinefelter sendromunda (47,XXY) olguların %50'sinden sorumlu tutulan paternal mayoz kusuru hangi kromozomal bölgede gerçekleşir?",
                "answer": "Paternal Mayoz 1'de Xp-Yp psödootozomal bölgesindeki anormal rekombinasyona bağlı ayrılamamadır.",
                "hint": "Paternal Mayoz 1, Xp-Yp psödootozomal bölge."
            },
            {
                "id": "fc-ch-38",
                "question": "Klinefelter (47,XXY) ile 47,XYY sendromu karşılaştırıldığında fertilite (üreme) kapasitesi açısından en temel fark nedir?",
                "answer": "Klinefelter hastaları germ hücre aplazisi ve seminifer tübül fibrozisi nedeniyle daima infertildir (azospermi); 47,XYY bireyler ise genelde fertildir ve normal çocuk sahibi olabilirler.",
                "hint": "Klinefelter = İnfertil; 47,XYY = Fertil."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Turner Sendromu (45,X): Karyotip Varyantları ve Kapsamlı Klinik",
        "subtitle": "1/4000 dişi doğum, yaşamla bağdaşan tek monozomi, yele boyun, aort koarktasyonu ve streak gonad",
        "badge": "Turner: 45,X",
        "badgeColor": "rose",
        "target_ids": ["d3-k1-tbg-002", "d3-k2-tbg-001"],
        "keywords": ["turner sendromu", "45 x", "yele boyun", "kistik higroma", "aort koarktasyonu", "streak gonad"],
        "lead": "Turner sendromu (45,X ve varyantları) insanda tam monozomi olup postnatal yaşamla bağdaşan tek durumdur (1/4000 canlı kız bebek); intrauterin dönemde gebeliklerin %95'i spontan abortusla sonlanır.",
        "spotPearls": [
            "KARYOTİP DAĞILIMI: %50 klasik 45,X; %15 45,X/46,XX mozaisizm; %15 46,X,i(Xq) uzun kol izokromozomu; %5 46,X,del(Xp); %5 46,X,r(X)/45,X mozaiklik. Mevcut tek X kromozomu %70 oranında MATERNAL kaynaklıdır.",
            "FETAL VE YENİDOĞAN İPUÇLARI: İntrauterin dönemde lenfatik drenaj bozukluğuna bağlı dev KİSTİK HİGROMA gelişir; doğumda bunun kalıntısı olarak YELE BOYUN (pterigium colli) ve EL-AYAK SIRTINDA ŞİDDETLİ ÖDEM tipiktir.",
            "TEMEL KLİNİK BULGULAR: Kısa boy (SHOX geni delesyonu), düşük arka saç çizgisi, kalkan göğüs, geniş aralıklı meme başları, cubitus valgus, at nalı böbrek.",
            "KARDİYOVASKÜLER ANOMALİLER: Aort Koarktasyonu ve Biküspit Aort Kapağı en sık görülen yaşamı tehdit edici kardiyak kusurlardır.",
            "GONADAL VE HORMONAL TABLO: Overler gelişimini tamamlayamaz; fibröz bantlar şeklinde çizgi gonadlar (STREAK GONAD) kalır. Primer amenore, infertilite, düşük östrojen ve yüksek FSH/LH (hipergonadotropik hipogonadizm). Zeka kural olarak NORMALDİR!"
        ],
        "keyBullets": [
            {"title": "del(Xp) vs del(Xq) Ayrımı", "desc": "Kısa kol delesyonlarında [del(Xp)] kısa boy ve organ malformasyonları belirginken; uzun kol delesyonlarında [del(Xq)] sadece gonadal disfonksiyon görülür."},
            {"title": "Büyüme Hormonu ve Östrojen", "desc": "Çocuklukta boy kısalığını önlemek için rekombinant GH; ergenlikte sekonder seks karakterleri ve kemik sağlığı için östrojen replasmanı verilir."},
            {"title": "Spontan Puberte İstisnası", "desc": "Özellikle mozaik olgularda %10-20 spontan puberte ve %2-5 geçici menstrüasyon görülebilir; nadiren gebelik bildirilmiştir."}
        ],
        "table": {
            "title": "Gonozomal Kromozom Sayısal Anomalileri Karşılaştırma Matrisi",
            "headers": ["Sendrom", "Karyotip", "Doğum Sıklığı", "Boy & Yapı", "Gonad & Fertilite", "Karakteristik Bulgular", "Zeka"],
            "rows": [
                ["Turner Sendromu", "45,X (%50), mozaik, i(Xq)", "1/4000 dişi", "Kısa boy, kalkan göğüs", "Streak gonad, primer amenore, infertil", "Yele boyun, kistik higroma, aort koarktasyonu", "Normal (Sözel yüksek, uzaysal zayıf)"],
                ["Klinefelter Sendromu", "47,XXY (%85), varyantlar", "1/2000 erkek", "Uzun boy, ögonoid yapı", "Küçük sert testis, azospermi, infertil", "Jinekomasti, meme ca riski, yüksek FSH/LH", "Hafif sözel öğrenme güçlüğü"],
                ["47,XYY Sendromu", "47,XYY", "1/1000 erkek", "Uzun boy, iri yapı", "Normal testis gelişimi, FERTİL", "Kistik akne, hafif motor koordinasyon kusuru", "Normal (Hafif davranış problemleri)"],
                ["Trizomi X (Triple X)", "47,XXX", "1/1000 dişi", "Uzun boy", "Normal over gelişimi, FERTİL", "Epikantus, midfasiyal hipoplazi", "Normal (Hafif konuşma gecikmesi)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-39",
                "question": "Fetal ultrasonda kistik higroma saptanan veya yenidoğanda el-ayak sırtı ödemi ve yele boyun görülen bir kız bebekte en olası tanı ve kardiyak risk nedir?",
                "answer": "Turner Sendromu (45,X); en önemli kardiyak anomali riski Aort Koarktasyonu ve biküspit aort kapağıdır.",
                "hint": "Turner sendromu ve Aort koarktasyonu."
            },
            {
                "id": "fc-ch-40",
                "question": "Turner sendromunda overlerin yerini alan fibröz çizgi dokuya ne ad verilir ve hastaların genel zeka düzeyi nasıldır?",
                "answer": "Streak gonad (çizgi gonad / gonadal disgenezis) adı verilir; hastaların genel zeka düzeyi normaldir (mental retardasyon sendromun parçası değildir).",
                "hint": "Streak gonad, zeka normaldir."
            }
        ]
    },
    {
        "slideNumber": 21,
        "title": "Genomik İmprinting ve Uniparental Dizomi (UPD): Prader-Willi vs Angelman",
        "subtitle": "15q11-q13 lokusu, maternal/paternal delesyon ve UPD mekanizması, izodizomi vs heterodizomi",
        "badge": "İmprinting & UPD",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["imprinting", "uniparental dizomi", "prader willi", "angelman", "15q11-q13", "izodizomi"],
        "lead": "Genomik imprinting ebeveynden kalıtılan alellerin maternal veya paternal kökenine bağlı olarak epigenetik mekanizmalarla susturulmasıdır; delesyon veya Uniparental Dizomi (UPD) varlığında klasik hastalık tabloları doğar.",
        "spotPearls": [
            "UNİPARENTAL DİZOMİ (UPD) TANIMI: Diploid bir bireyde homolog kromozom çiftinin her iki üyesinin de tek bir ebeveynden gelmesi durumudur. İZODİZOMİ tek bir ebeveyn kromozomunun duplikasyonu iken; HETERODİZOMİ ebeveynin iki farklı homologunun birden aktarılmasıdır.",
            "PRADER-WİLLİ SENDROMU (PWS): 15q11-q13 lokusundaki babaya ait (paternal) aktif genlerin kaybıdır. %70 PATERNAL DELESYON, %30 MATERNAL UNİPARENTAL DİZOMİ (Maternal UPD) ile oluşur.",
            "PWS KLİNİĞİ: İnfantil dönemde şiddetli hipotoni ve beslenme güçlüğü; çocuklukta doymak bilmeyen aşırı yeme (hiperfaji), morbid obezite, küçük el ve ayaklar, hipogonadizm ve mental gerilik.",
            "ANGELMAN SENDROMU (AS): 15q11-q13 lokusundaki anneye ait (maternal) aktif UBE3A geninin kaybıdır. %70 MATERNAL DELESYON, %3-5 PATERNAL UNİPARENTAL DİZOMİ (Paternal UPD) veya UBE3A mutasyonu ile oluşur.",
            "AS KLİNİĞİ: Uygunsuz paroksismal kahkaha ve gülme nöbetleri ('Happy Puppet' - Mutlu Kukla), konuşmanın hiç olmaması, ataksik kukla benzeri yürüyüş, mikrosefali ve ağır mental gerilik."
        ],
        "keyBullets": [
            {"title": "Mendel Dışı Epigenetik Kalıtım", "desc": "DNA dizi değişimi olmadan sitozin metilasyonu ile spesifik alellerin gametogenezde susturulması esasına dayanır."},
            {"title": "Trizomi Kurtarma (Trisomy Rescue)", "desc": "Trizomik bir zigottan mitozda fazlalık kromozomun atılması (anaphase lagging) tesadüfen aynı ebeveyne ait 2 kromozom bırakarak UPD doğurabilir."},
            {"title": "Metilasyon Analizi Şartı", "desc": "PWS ve Angelman şüphesinde delesyon yanında UPD'yi de tek seferde tarayan altın standart test DNA Metilasyon Analizidir (MS-MLPA)."}
        ],
        "table": {
            "title": "15q11-q13 Lokusunda Genomik İmprinting: Prader-Willi vs Angelman Sendromu",
            "headers": ["Özellik", "Prader-Willi Sendromu (PWS)", "Angelman Sendromu (AS)"],
            "rows": [
                ["Etkilenen Kromozom", "15q11-q13", "15q11-q13"],
                ["Eksik Olan İfade", "Paternal aktif genlerin kaybı", "Maternal aktif genin kaybı (UBE3A)"],
                ["Delesyon Oranı", "%70 Paternal 15q11-q13 Delesyonu", "%70 Maternal 15q11-q13 Delesyonu"],
                ["UPD Oranı", "%30 Maternal Uniparental Dizomi (Maternal UPD)", "%3-5 Paternal Uniparental Dizomi (Paternal UPD)"],
                ["Karakteristik Davranış", "Kontrolsüz hiperfaji, yemek arama, inatçılık", "Sürekli neşeli görünüm, kahkaha krizleri"],
                ["Nöromotor Özellikler", "İnfantta derin hipotoni, sonradan obezite", "Ataksik kesik adımlarla yürüyüş, motor apraksi"],
                ["Konuşma & Dil", "Konuşma gecikmeli ancak var", "Konuşma hemen hemen hiç yoktur (1-2 kelime)"],
                ["Fiziksel Özellikler", "Küçük el ve ayaklar, badem göz, hipogonadizm", "Geniş ağız, aralıklı dişler, mikrosefali, dil çıkması"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ch-41",
                "question": "Prader-Willi Sendromu ile Angelman Sendromu 15q11-q13 lokusunda hangi ebeveyn delesyonu ve UPD tipleriyle ortaya çıkar?",
                "answer": "Prader-Willi: Paternal delesyon (%70) veya Maternal UPD (%30); Angelman: Maternal delesyon (%70) veya Paternal UPD (%3-5).",
                "hint": "PWS = Paternal del / Maternal UPD; AS = Maternal del / Paternal UPD."
            },
            {
                "id": "fc-ch-42",
                "question": "İzodizomi ile Heterodizomi arasındaki temel genetik fark nedir?",
                "answer": "İzodizomide tek bir ebeveyn kromozomu duplike olmuştur (otozomal resesif hastalık riski taşır); Heterodizomide ise ebeveynin iki farklı homolog kromozomu birden aktarılmıştır.",
                "hint": "İzodizomi = tek kromozomun kopyası; Heterodizomi = iki farklı ebeveyn homoloğu."
            }
        ]
    },
    {
        "slideNumber": 22,
        "title": "Büyük Sentez: Genetik Danışma İlkeleri, Rekürrens Riskleri ve Kurul 1 Altın İpuçları",
        "subtitle": "Dr. Öğr. Üyesi Serap Arslan amfi dersi çekirdek sentezi, non-direktif yaklaşım ve tanı algoritması",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-tbg-009", "d3-k1-tbg-011"],
        "keywords": ["genetik danışma", "non direktif", "rekürrens", "prenatal tanı", "pgt", "altın spotlar"],
        "lead": "Genetik danışma; kalıtsal hastalık taşıyan veya taşıma riski bulunan bireylere hastalığın seyri, prognozu, tekrarlama riskleri ve tanı/tedavi seçenekleri hakkında yönlendirici olmadan (non-direktif) kapsamlı bilgi verilmesidir.",
        "spotPearls": [
            "ALTIN KURAL - NON-DİREKTİF DANIŞMANLIK: Genetik danışman asla aile adına karar vermez; hiçbir zaman yönlendirici olmamalıdır ('bebeği aldırın' ya da 'kesin doğurun' denmez). Riskler tam ve tarafsız aktarılarak karar aileye bırakılır.",
            "REKÜRRENS RİSKİ KURALLARI: 1) Klasik Trizomi 21'de 30 yaşından genç anneler için tekrarlama riski %1.4 iken ileri yaşta yaşa bağımlı genel risktir; 2) rob(14;21) translokasyonunda anne taşıyıcıysa risk %10-15, baba taşıyıcıysa %4-5'tir; 3) Homolog rob(21;21) taşıyıcısında tekrarlama riski %100'dür!",
            "PRENATAL İNVAZİV TANI PENCERELERİ: Koryon Villus Örneklemesi (CVS) 11-14. haftalarda trofoblastlardan; Amniyosentez 15-20. haftalarda amniyositlerden; Kordosentez >20. haftada fetal göbek kordon kanından yapılır.",
            "PGD / PGT ENDİKASYONLARI: Bilinen dengeli translokasyon taşıyıcılığı, monogenik hastalık öyküsü veya tekrarlayan düşük öyküsü PGD endikasyonudur; yalnızca tek başına ileri anne yaşı klasik PGD endikasyonu sayılmaz.",
            "TANI ALGORİTMASI SIRASI: Rutin sitogenetik karyotip analizi -> Görünür anomali yoksa ve mikrodelesyon şüphesi varsa FISH / Karyotipleme -> Açıklanamayan sendromlarda CMA (Mikroarray) -> Tek gen kuşkusu varsa NGS Paneli."
        ],
        "keyBullets": [
            {"title": "Ayrıntılı Pedigri Çizimi", "desc": "Danışmanlıkta en az 3 kuşak pedigri çizilmeli, akraba evlilikleri, ölü doğumlar ve tekrarlayan düşükler sorgulanmalıdır."},
            {"title": "Multidisipliner İzlem", "desc": "Down sendromlu olgularda kardiyoloji, endokrinoloji, KBB, ortopedi ve özel eğitim randevuları doğumdan itibaren planlanmalıdır."},
            {"title": "Görünürde Dengeli Translokasyon Tuzağı", "desc": "Dengeli yeniden düzenlenme taşıyan ailede fenotip normal olsa bile sonraki kuşakta dengesiz bebek riski %1-100 arasında değişir."}
        ],
        "flashcards": [
            {
                "id": "fc-ch-43",
                "question": "Genetik danışmanın en temel etik ve mesleki ilkesi nedir?",
                "answer": "Yönlendirici olmamak (non-direktif danışmanlık); ailenin kararına müdahale etmeden tüm bilimsel gerçekleri, riskleri ve çözüm yollarını tarafsızca aktarmaktır.",
                "hint": "Non-direktif (yönlendirici olmayan) ilke."
            },
            {
                "id": "fc-ch-44",
                "question": "rob(14;21) taşıyıcısı bir annenin çocuğunda Down sendromu riski yüzde kaç iken; rob(21;21) taşıyıcısı bir ebeveynde bu risk yüzde kaçtır?",
                "answer": "rob(14;21) taşıyıcısı annede risk %10-15; rob(21;21) taşıyıcısı ebeveynde ise risk tam %100'dür.",
                "hint": "Anne rob(14;21) = %10-15; rob(21;21) = %100."
            }
        ]
    }
]

def build_synthesis_narrative(slide_data):
    lines = []
    lines.append(f"### {slide_data['title']}")
    lines.append(f"#### {slide_data['subtitle']}")
    lines.append("")
    lines.append(f"• **Temel Sitogenetik ve Klinik Çerçeve:** {slide_data['lead']}")
    lines.append("")
    
    for kb in slide_data.get('keyBullets', []):
        lines.append(f"• **{kb['title']}:** {kb['desc']}")
        lines.append("")

    lines.append("💡 **Klinik Genetik Sentezi ve Fakülte Sınav İncileri (Dr. Öğr. Üyesi Serap Arslan):**")
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
            f"Dr. Öğr. Üyesi Serap Arslan'ın amfi dersinde '{title_clean}' konusunda yaptığı en kritik sınav vurguları nelerdir?",
            f"Klinik genetik yaklaşımında '{title_clean}' ile gelen bir hastada sitogenetik ve moleküler tanı algoritması nasıl işletilmelidir?",
            f"Dönem 3 Kurul 1 sınavında '{title_clean}' konusundan çıkabilecek vaka kurgusu ve şaşırtıcı seçenekler nelerdir?"
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
        "id": "learn-kromozomal-hastaliklar-ve",
        "title": "Kromozomal Hastalıklar ve Genetik Danışma",
        "shortTitle": "Kromozomal Hastalıklar",
        "discipline": "Tıbbi Genetik",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "sourceFile": "2)KROMOZOMAL HASTALIKLAR VE GENETİK DANIŞMA.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "emerald",
        "overview": "Dönem 3 Kurul 1 Tıbbi Genetik müfredatında yer alan Kromozomal Hastalıklar ve Genetik Danışma dersinin %500 derinlikte kapsamlı interaktif öğrenim sunumu. Sayısal bozukluklar (öploidi, triploidi, anöploidi), yapısal anomaliler (delesyonlar, mikrodelesyon sendromları, duplikasyonlar, inversiyonlar, resiprokal ve Robertsonyan translokasyonlar), otozomal trizomiler (Down, Edwards, Patau), gonozomal hastalıklar (Klinefelter, Turner, XYY, Triple X), genomik imprinting (Prader-Willi, Angelman), non-direktif genetik danışmanlık ve prenatal tanı prensiplerini, 44 adet 3D akıl kartını, 6 adet karşılaştırma tablosunu ve Kurul 1 çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "Kromozomal anomaliler tüm canlı doğumların %1'inde görülür ve en yaygın klinik tipi ANÖPLOİDİDİR.",
            "Triploidi 1. trimester spontan abortusların %20'sini oluşturur; ekstra kromozom babadan geldiğinde (dispermi) HİDATİDİFORM MOL gelişir.",
            "Mayoz I non-disjunction her iki ebeveyn homologunu taşırken; Mayoz II non-disjunction özdeş kromatitleri taşır.",
            "İnsanda canlı doğumla ve postnatal yaşamla bağdaşan tek tam monozomi TURNER SENDROMU'dur (45,X).",
            "Cri-du-chat 5p15.2 delesyonu (5p15.3 ağlama), Wolf-Hirschhorn 4p16.3 delesyonudur (Grek miğferi yüzü).",
            "Robertsonyan translokasyon yalnızca akrosentriklerde (13, 14, 15, 21, 22) görülür; dengeli taşıyıcı 45 kromozomludur. rob(14;21) anne riski %10-15, baba riski %4-5; rob(21;21) riski %100'dür!",
            "Down sendromu olgularının %95'i klasik trizomi (artan anne yaşıyla ilişkili), %4'ü Robertsonyan translokasyon (anne yaşından bağımsız), %1'i mozaiktir.",
            "Down sendromunda erken ölümlerin en sık nedeni Atriyoventriküler Septal Defekt (AVSD)'dir; akut lösemi riski 15 kat artmıştır.",
            "Edwards (Trizomi 18) için 'clenched hand' ve 'rocker-bottom' ayak; Patau (Trizomi 13) için 'mikroftalmi + yarık damak + polidaktili' triadı karakteristiktir.",
            "Klinefelter (47,XXY) paternal Mayoz 1'de Xp-Yp psödootozomal ayrılmama sonucu oluşur; jinekomasti, azospermi ve yüksek gonadotropinlerle seyreder.",
            "Turner (45,X) fetal kistik higroma, yele boyun, aort koarktasyonu ve streak gonadla seyreder; ZEKA NORMALDİR!",
            "15q11-q13 lokusunda Paternal delesyon / Maternal UPD = Prader-Willi; Maternal delesyon / Paternal UPD = Angelman Sendromu.",
            "Genetik danışmanlık daima NON-DİREKTİF (yönlendirici olmayan) ilkede verilmelidir."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Kromozomal Hastalıklar ve Genetik Danışma...")
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
            elif item.get('id') == 'learn-halk-sagligi-salgin-has':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Kromozomal Hastalıklar completed, Salgın Hastalıklar next!")

    print("Success! Chromosomal diseases deck generation completed.")

if __name__ == '__main__':
    main()
