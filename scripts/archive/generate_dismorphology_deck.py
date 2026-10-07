#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_dismorphology_deck.py
Generates the deep (%500 detail) 20-slide learning deck for:
"Dismorfolojide Genetik Terminoloji ve Malformasyonlar" (Tıbbi Genetik - Dr. Öğr. Üyesi Serap Arslan)
Incorporating 20 slides, 40 3D flashcards, 5 comparison tables, and matched past exam questions (d3-k1-tbg-001 etc.).
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Tıbbi Genetik müfredatında dismorfoloji terminolojisi ile doğrudan ilişkilidir.'
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Tıbbi Genetik müfredatında dismorfoloji terminolojisi ile doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Tıbbi Genetik ve Dismorfolojiye Giriş",
        "subtitle": "Dr. David Smith (1960), normal morfogenezden sapmalar ve doğumsal defekt insidansı",
        "badge": "Giriş & Tanım",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["dismorfoloji", "david smith", "morfogenez", "konjenital malformasyon"],
        "lead": "Dismorfoloji; klinik genetiğin fiziksel gelişimdeki farklılıkları inceleyen, normal morfogenezden sapmaları değerlendiren ve doğumsal defektler üzerine uzmanlaşan ana bilim dalıdır.",
        "spotPearls": [
            "İLK TANIM: 'Dismorfoloji' kavramı ilk kez 1960 yılında Dr. David Smith tarafından tanımlanmıştır (Dys = anormal/hastalık, morph = biçim/şekil).",
            "TOPLUMSAL İNSİDANS: Tüm yenidoğan bebeklerin yaklaşık %3'ünde (yüzde üç) doğumda saptanan en az bir konjenital malformasyon mevcuttur."
        ],
        "keyBullets": [
            {"title": "2000'den Fazla Sendrom", "desc": "Dismorfolojinin karmaşıklığı tıp literatüründe tanımlanmış 2000'in üzerinde dismorfik sendrom bulunmasından kaynaklanır."},
            {"title": "Geniş Varyasyon Yelpazesi", "desc": "Doğumsal defektler vücudun içinde veya dışında, tekli veya çoklu, minör veya majör, sporadik veya kalıtsal olabilir."},
            {"title": "Klinik Prensip", "desc": "'Ne kadar çok görülürse o kadar çok bilinir; ne kadar çok bilinirse o kadar çok görülür' ilkesi dismorfolojinin temel mottosudur."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-1",
                "question": "Dismorfoloji terimini tıp literatüründe ilk kez kim ve ne zaman tanımlamıştır?",
                "answer": "1960 yılında Dr. David Smith tarafından tanımlanmıştır.",
                "hint": "1960, David Smith."
            },
            {
                "id": "fc-dm-2",
                "question": "Tüm canlı yenidoğanlarda en az bir konjenital malformasyon görülme sıklığı yaklaşık yüzde kaçtır?",
                "answer": "Yaklaşık %3 (yüzde üç) oranında görülür (genel konjenital anomali sıklığı %2-4'tür).",
                "hint": "%3 kuralı."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "Tıbbi Genetiğin Alt Disiplinleri ve Genetik Danışma",
        "subtitle": "Sitogenetik, moleküler genetik, gelişimsel genetik ve non-direktif danışmanlık",
        "badge": "Genetik Alanları",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["sitogenetik", "moleküler genetik", "genetik danışma", "non-direktif"],
        "lead": "Tıbbi genetik; kromozomları çalışan sitogenetikten, DNA dizilerini çalışan moleküler genetiğe ve aileye destek sağlayan klinik genetik danışmaya kadar geniş bir yelpazeyi kapsar.",
        "spotPearls": [
            "GENETİK DANIŞMA İLKESİ: Genetik danışmanlık aileyi yönlendirmeyen (NON-DİREKTİF), objektif riskleri ve seçenekleri aktaran psikoeğitimsel bir sağlık hizmetidir.",
            "PROBAND (İNDEKS VAKA): Ailede incelenen veya genetik danışmaya ilk başvuran etkilenmiş bireye verilen teknik isimdir."
        ],
        "keyBullets": [
            {"title": "Sitogenetik", "desc": "Kromozomların sayısal ve yapısal anormalliklerini ışık mikroskobu ve karyotipleme ile inceler."},
            {"title": "Moleküler Genetik", "desc": "Genlerin nükleotid yapısını, nokta mutasyonlarını ve sekanslama (Sanger, NGS, WES) yöntemlerini inceler."},
            {"title": "Gelişimsel (Developmental) Genetik", "desc": "Embriyogenez ve fetal büyüme sırasında organ morfogenezinin genetik kontrol basamaklarını inceler."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-3",
                "question": "Genetik danışmanlık sürecinin en temel etik ve mesleki yaklaşım prensibi nedir?",
                "answer": "Non-direktif (yönlendirici olmayan) olması; ailenin kendi özgür kararını verebilmesi için bilgilerin tam ve tarafsız sunulmasıdır.",
                "hint": "Yönlendirici olmama ilkesi."
            },
            {
                "id": "fc-dm-4",
                "question": "Klinik genetikte aile ağacında (pedigri) incelemeye ilk alınan etkilenmiş bireye ne ad verilir?",
                "answer": "Proband (veya İndeks Vaka / Propositus).",
                "hint": "İlk etkilenmiş aile üyesi."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Kromozomal Düzensizlikler: Sayısal ve Yapısal Spektrum",
        "subtitle": "Anöploidiler (2n±1), translokasyonlar, delesyonlar, inversiyonlar ve ring kromozomlar",
        "badge": "Sitogenetik",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["anöploidi", "translokasyon", "delesyon", "inversiyon", "izokromozom"],
        "lead": "Dismorfik sendromların önemli bir bölümü sayısal (anöploidi) veya yapısal kromozom anomalilerinden köken alır.",
        "spotPearls": [
            "SAYISAL DÜZENSİZLİKLER: Anöploidi (2n+1 trizomi veya 2n-1 monozomi; örn. Down sendromu 47,XX,+21; Turner sendromu 45,X0).",
            "YAPISAL DÜZENSİZLİKLER: Translokasyon (resiprokal/robertsonyan), delesyon (eksik parça), duplikasyon, inversiyon (parasentrik/perisentrik), ring (halka) ve izokromozom."
        ],
        "keyBullets": [
            {"title": "Öploidi vs Anöploidi", "desc": "Haploid sayının (n=23) tam katları öploidi (triploidi 69), tek bir kromozomun eksik veya fazla olması anöploididir."},
            {"title": "Dengeli vs Dengesiz Düzensizlikler", "desc": "Dengeli translokasyon taşıyıcısı fenotipik olarak normalken, çocuklarında delesyonlu dengesiz karyotip ve dismorfizm riski doğar."},
            {"title": "Mikrodelesyonlar", "desc": "Standart karyotipte görülemeyen ancak FISH veya mikroarray ile saptanan submikroskobik kayıplardır (örn. 22q11.2, Williams 7q11.23)."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-5",
                "question": "Tek bir kromozomun fazlalığı (2n+1) veya eksikliği (2n-1) ile seyreden kromozom düzensizliğine ne ad verilir?",
                "answer": "Anöploidi (trizomi veya monozomi).",
                "hint": "2n artı veya eksi 1."
            },
            {
                "id": "fc-dm-6",
                "question": "Sentromerin transvers (enine) bölünmesi sonucu iki uzun kol veya iki kısa kol taşıyan yapısal kromozoma ne ad verilir?",
                "answer": "İzokromozom.",
                "hint": "Ayna görüntüsü kollar."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Dismorfoloji ve Metabolik Hastalıklar Arasındaki Yapı-Fonksiyon Ayrımı",
        "subtitle": "Anormal yapı ± anormal fonksiyon vs normal yapı + anormal metabolik fonksiyon",
        "badge": "Kavramsal Ayrım",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["metabolik hastalık", "dismorfizm", "yapı fonksiyon"],
        "lead": "Pediatrik genetikte hastanın değerlendirilmesinde ilk temel ayrım; anomalinin primer yapısal mı (dismorfolojik) yoksa metabolik/biyokimyasal mı olduğunu saptamaktır.",
        "spotPearls": [
            "DİSMORFOLOJİ: Temelde ANORMAL YAPI (anatomik morfogenez defekti) vardır; fonksiyonel anomali eşlik edebilir veya etmeyebilir.",
            "METABOLİK HASTALIK: Doğumda bebekte ANATOMİK YAPI GENELLİKLE NORMALDİR; ancak enzim defekti nedeniyle ANORMAL FONKSİYON (asidoz, koma, konvülziyon) ortaya çıkar."
        ],
        "keyBullets": [
            {"title": "Fizik Muayene İpucu", "desc": "Yüz hatları, kulak yapısı, el çizgileri dismorfolojide tanı koydururken; metabolik hastalıkta bebek başlangıçta dismorfik görünmez."},
            {"title": "Zamanlama Farkı", "desc": "Malformasyonlar intrauterin organogenezde (ilk 8 hafta) oluşmuşken; metabolik semptomlar sıklıkla beslenmeye başlandıktan sonra patlar."},
            {"title": "Örtüşen Tablolar", "desc": "Zellweger sendromu ve lizozomal depo hastalıkları gibi bazı durumlarda metabolik defekt kemik ve yüz dismorfizmine yol açabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-7",
                "question": "Dismorfolojik hastalıklar ile doğumsal metabolik hastalıklar arasındaki en temel yapı-fonksiyon farkı nedir?",
                "answer": "Dismorfolojide anormal yapı (anatomik kusur) ön plandayken; metabolik hastalıklarda doğumda yapı genellikle normal olup anormal biyokimyasal fonksiyon ön plandadır.",
                "hint": "Anormal yapı vs anormal fonksiyon."
            },
            {
                "id": "fc-dm-8",
                "question": "Konjenital anomaliler intrauterin hangi kritik dönemde meydana gelir?",
                "answer": "Embriyonik organogenez döneminde (gebeliğin ilk 8-10 haftasında).",
                "hint": "İlk trimester organogenezi."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Konjenital Anomalilerin Boyutuna Göre Sınıflaması: Minör ve Majör Anomaliler",
        "subtitle": "Ciddi cerrahi/tıbbi önem taşıyan defektler vs zararsız anatomik varyasyonlar",
        "badge": "Sınıflama",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["minör anomali", "majör anomali", "kozmetik", "morfolojik"],
        "lead": "Doğumsal anomaliler klinik önemlerine ve cerrahi gereksinimlerine göre Minör ve Majör anomaliler olarak iki ana grupta sınıflandırılır.",
        "spotPearls": [
            "MİNOR ANOMALİ: Bilinen medikal, cerrahi ya da kozmetik önemi olmayan/çok az olan ve normal popülasyonun %4'ünden daha azında görülen varyasyonlardır.",
            "MAJÖR ANOMALİ: Bebeğin yaşamını, sağlığını tehdit eden, cerrahi onarım veya yoğun medikal tedavi gerektiren ciddi yapısal defektlerdir (MSS, KVS, GİS anomalileri)."
        ],
        "keyBullets": [
            {"title": "Popülasyon Sınırı (%4)", "desc": "Toplumda %4'ten sık görülen özellikler (örn. tek ayak parmağı kısalığı) anomali değil 'normal varyasyon' sayılır."},
            {"title": "Klinik Yaklaşım", "desc": "Tek başına bir minör anomali tedavi gerektirmez ancak genetik hekimine altta yatan sendrom için 'yol gösterici fener' olur."},
            {"title": "Majör Anomali İnsidansı", "desc": "Canlı doğan bebeklerin yaklaşık %2-3'ünde majör anomali saptanır (örn. anensefali, VSD, omfalosel, duodenal atrezi)."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-9",
                "question": "Tıbbi genetikte bir fiziksel özelliğin 'minör anomali' sayılabilmesi için genel popülasyonda görülme sıklığı en fazla ne kadar olmalıdır?",
                "answer": "Popülasyonun %4'ünden daha azında görülmelidir (%4'ün üzerinde görülüyorsa normal varyasyondur).",
                "hint": "%4 sıklık eşiği."
            },
            {
                "id": "fc-dm-10",
                "question": "Majör anomali ile minör anomaliyi ayıran temel klinik kriter nedir?",
                "answer": "Majör anomalinin cerrahi müdahale, medikal tedavi gerektirmesi veya hayati/kozmetik ciddi fonksiyonel bozukluğa yol açmasıdır.",
                "hint": "Medikal/cerrahi ciddiyet."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Minör Anomaliler: Tanısal Değeri, Sendromik İpuçları ve '3 Kuralı'",
        "subtitle": "Non-spesifik vs spesifik belirteçler ve ≥3 minör anomalide %90 majör defekt riski",
        "badge": "Minör Anomaliler",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["minör anomali", "3 kuralı", "hipertelorizm", "beyaz perçem", "telekantus"],
        "lead": "Minör anomaliler cerrahi tedavi gerektirmez; ancak hekime altta yatan gizli sendromu haber veren en hassas morfolojik pusuladır.",
        "spotPearls": [
            "ALTIN KURAL (3 KURALI): Birinci derece akrabalarında bulunmayan ÜÇ (3) VEYA DAHA FAZLA MİNOR ANOMALİSİ olan bir bebekte, %90 OLASILIKLA EŞLİK EDEN BİR MAJÖR ANOMALİ VEYA SENDROM VARDIR!",
            "NON-SPESİFİK MİNOR ANOMALİLER: Hipertelorizm (>400 sendromda), Blefarofimozis (100 sendromda), Telekantus (90 sendromda).",
            "SPESİFİK MİNOR ANOMALİLER: Alında beyaz perçem (Waardenburg sendromu), İris heterokromisi, Göz kapağı kolobomu (Treacher Collins), Tek üst santral kesici diş (Holoprozensefali)."
        ],
        "keyBullets": [
            {"title": "Dismorfik Değerlendirme Eşiği", "desc": "Bebekte tek bir minör anomali varsa majör defekt riski %3; 2 minör anomali varsa %10; 3 veya daha fazla varsa %90'a fırlar!"},
            {"title": "Göz Çevresi Ölçümleri", "desc": "Hipertelorizm göz kürelerinin (pupillalar arası mesafenin) birbirinden uzak olmasıdır; telekantus ise sadece iç kantal mesafenin genişliğidir."},
            {"title": "Tanısal İpuçları", "desc": "Alında beyaz perçem görüldüğünde hekim mutlaka işitme testine yönelmelidir (Waardenburg sendromunda sensörinöral sağırlık)."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-11",
                "question": "Ailesinde benzer bulgu olmayan bir yenidoğanda 3 veya daha fazla minör anomali saptandığında eşlik eden bir majör anomali/sendrom bulunma riski yüzde kaçtır?",
                "answer": "Yaklaşık %90 oranındadır (bu bebekler mutlaka detaylı dismorfolojik incelemeye alınmalıdır).",
                "hint": "%90 majör anomali riski."
            },
            {
                "id": "fc-dm-12",
                "question": "Hipertelorizm ile Telekantus arasındaki morfolojik fark nedir?",
                "answer": "Hipertelorizmde göz küreleri (pupillalar arası mesafe) birbirinden geniştir; telekantusta ise göz küreleri normal yerinde olup sadece iç göz kapak köşeleri (iç kantuslar) birbirinden uzaktadır.",
                "hint": "Pupilla mesafesi vs iç kantal mesafe."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Etiyopatogeneze Göre Anomaliler: Dört Temel Primer Defekt Matrisi",
        "subtitle": "Malformasyon, Deformasyon, Disrupsiyon ve Displazinin karşılaştırmalı biyolojisi",
        "badge": "Etiyopatogenez",
        "badgeColor": "indigo",
        "target_ids": ["d3-k1-tbg-001"],
        "keywords": ["malformasyon", "deformasyon", "disrupsiyon", "displazi", "primer defekt"],
        "lead": "Dismorfolojide tekil primer gelişimsel defektler; oluştukları intrauterin periyot ve etiyolojik mekanizmalarına göre dört net sınıfa ayrılır.",
        "spotPearls": [
            "MALFORMASYON: Embriyonik dönemde (organogenez) İNTRİNSİK hatalı oluşum (yarık dudak, VSD, spina bifida).",
            "DEFORMASYON: Fetal dönemde NORMAL DOKUNUN DIŞ MEKANİK KUVVETLE şekil değiştirmesi (pes ekinovarus, kalça çıkığı; reversibldir!).",
            "DİSRUPSİYON: Normal gelişen yapının EKSTRİNSİK VEYA VASKÜLER YIKIMLA (nekroz/amputasyon) parçalanması (amniyotik bant, gastroşizis).",
            "DİSPLAZİ: Doku düzeyinde ANORMAL HÜCRESEL ORGANİZASYON (iskelet displazileri; yaşla ilerleyicidir)."
        ],
        "keyBullets": [
            {"title": "Dönem Farkı", "desc": "Malformasyon ve displazi erken embriyonik doku evresinde; deformasyon ise fetal büyüme ve organlaşma evresinde şekillenir."},
            {"title": "Geri Dönüşüm (Reversibilite)", "desc": "Deformasyonlar doğum sonrası pozisyonun düzelmesi veya fizyoterapi ile geri dönebilirken; malformasyon ve disrupsiyon kalıcıdır."},
            {"title": "Tekrarlama Riski", "desc": "Disrupsiyonda genetik olmadığı için ailede tekrarlama riski sıfıra yakındır; malformasyonda tek gen/multifaktöriyel risk mevcuttur."}
        ],
        "table": {
            "title": "Dört Temel Konjenital Anomali Tipinin Etiyopatolojik Karşılaştırma Matrisi",
            "headers": ["Anomali Tipi", "Oluşum Mekanizması", "Gelişme Periyodu", "Tipik Klinik Örnekler", "Geri Dönüşüm", "Tekrarlama Riski"],
            "rows": [
                ["Malformasyon", "Primer intrinsik morfogenez hatası", "Embriyonik dönem (ilk 8 hafta)", "Yarık dudak/damak, VSD, Spina bifida", "Kalıcı (Cerrahi gerekir)", "Yüksek (Genetik/multifaktöriyel)"],
                ["Deformasyon", "Dış mekanik baskı, kompresyon ve sıkışma", "Fetal dönem (geç gebelik)", "Pes ekinovarus (clubfoot), Kalça çıkığı", "Doğum sonrası REVERSİBL olabilir", "Düşük / Değişken"],
                ["Disrupsiyon", "Normal yapının ekstrinsik/vasküler yıkımı", "Embriyonik veya fetal dönem", "Amniyotik bant amputasyonu, Gastroşizis", "Kalıcı (Doku kopmuştur)", "Çok Düşük (Kalıtsal değildir)"],
                ["Displazi", "Doku düzeyinde anormal hücresel organizasyon", "Tüm gelişim ve postnatal dönem", "Akondroplazi, Tanatoforik displazi", "Kalıcı ve İLERLEYİCİDİR", "Mendelyen kalıtıma bağlı (Yüksek)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-dm-13",
                "question": "Hangi konjenital defekt tipi doğum sonrasında kendiliğinden veya konservatif fizik tedavi ile geri dönüşümlü (reversibl) olabilir?",
                "answer": "Deformasyon (mekanik bası kalktığında doku normal genetik koduna göre düzelebilir).",
                "hint": "Mekanik baskı sonucu oluşan defekt."
            },
            {
                "id": "fc-dm-14",
                "question": "Amniyotik bant sendromu sonucu bir bebeğin parmaklarının veya kolunun kopması hangi defekt tipine örnektir?",
                "answer": "Disrupsiyon (dış mekanik bantla doku yıkımı/amputasyonu).",
                "hint": "Ekstrinsik yıkım ve amputasyon."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Malformasyon: Organogenez Dönemindeki Primer İntrinsik Hata",
        "subtitle": "Doku gelişiminde duraklama, yanlış yönlenme ve kalıcı anatomik defektler",
        "badge": "Malformasyon",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["malformasyon", "organogenez", "yarık damak", "spina bifida", "intrinsik"],
        "lead": "Malformasyon; organogenez döneminde bir yapının veya organın biçimlenmesindeki primer lokalize bir hatadan kaynaklanan kalıcı yapısal anomalidir.",
        "spotPearls": [
            "İNTRİNSİK GELİŞİM HATASI: Doku veya organın genetik programındaki duraklama, gecikme veya yanlış yönlenme sonucu doku baştan itibaren hatalı oluşur.",
            "KLASİK ÖRNEKLER: Yarık dudak/damak, konjenital kalp hastalıkları (Fallot tetralojisi, VSD), nöral tüp defektleri (spina bifida, anensefali), polidaktili.",
            "KOMBİNASYON: Malformasyon tek başına izole olabileceği gibi bir sendromun, sekansın veya asosiasyonun temel bileşeni olabilir."
        ],
        "keyBullets": [
            {"title": "İlk Trimester Hassasiyeti", "desc": "Gebeliğin 3-8. haftaları arasında organ primordiyumlarının füzyon veya kavitasyon kusurlarından doğar."},
            {"title": "Multifaktöriyel Zemin", "desc": "Yarık damak ve spina bifida gibi malformasyonlar hem genetik yatkınlık hem folik asit eksikliği gibi çevresel faktörlerle tetiklenir."},
            {"title": "Sistemik Taramalar", "desc": "Bir majör malformasyon (örn. omfalosel) saptandığında mutlaka fetal ekokardiyografi ve MSS ultrasonu yapılmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-15",
                "question": "Malformasyon gelişiminin en kritik embriyolojik zaman penceresi hangisidir?",
                "answer": "Organogenez dönemi (gebeliğin ilk 3 ila 8. haftaları arası).",
                "hint": "Embriyonik ilk haftalar."
            },
            {
                "id": "fc-dm-16",
                "question": "Spina bifida ve yarık dudak-damak hangi temel konjenital anomali sınıfına girer?",
                "answer": "Malformasyon (primer intrinsik doku oluşum hatası).",
                "hint": "İntrinsik anatomik defekt."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Deformasyon: Fetal Mekanik Kompresyon ve Kas-İskelet Distorsiyonu",
        "subtitle": "Oligohidramniyos, transvers duruş, pes ekinovarus ve kraniyofasiyal basıklık",
        "badge": "Deformasyon",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-tbg-001"],
        "keywords": ["deformasyon", "oligohidramniyos", "pes ekinovarus", "kraniyofasiyal basıklık", "çıkmış soru"],
        "lead": "Deformasyon; embriyolojik olarak tamamen normal gelişmiş bir fetal yapının dış mekanik kompresyon veya kısıtlayıcı güçlere maruz kalmasıyla şeklinin bozulmasıdır.",
        "spotPearls": [
            "KURUL 1 ÇIKMIŞ SORU (Soru #1): 'Aşağıdakilerden hangisi bir deformasyona örnektir?' -> Doğru Cevap: OLİGOHİDRAMNİYOZA BAĞLI KRANİYOFASYAL BASIKLIK VE TALİPES DEFORMİTESİ.",
            "ETİYOLOJİK MEKANİK GÜÇLER: Uterin kısıtlılık (büyük bebek, ilk gebelik, ikiz/çoğul gebelik, bikornus uterus), oligohidramniyos (amniyotik sıvı azlığı) ve transvers fetal duruş.",
            "ETKİLENEN DOKULAR: Neredeyse daima KEMİK, KIKIRDAK VE EKLEMLERİ tutar (pes ekinovarus / clubfoot, gelişimsel kalça çıkığı, plagiosefali)."
        ],
        "keyBullets": [
            {"title": "Normal Genetik Kod", "desc": "Doku hücrelerinde hiçbir genetik veya enzimatik defekt yoktur; sadece mekanik ezilme söz konusudur."},
            {"title": "Postnatal Deformasyon", "desc": "Prematüre hipotonik bebeklerin sürekli aynı pozisyonda yatırılması skafosefali ve plagiosefaliye (düz kafa) yol açabilir."},
            {"title": "Düşük Tekrarlama Riski", "desc": "Uterin septum gibi anatomik engel düzeltildiğinde sonraki gebeliklerde deformasyon tekrarlama riski son derece düşüktür."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-17",
                "question": "Oligohidramnioza bağlı olarak fetusta gelişen basık yüz görünümü ve pes ekinovarus (çarpık ayak) hangi anomali tipine örnektir?",
                "answer": "Deformasyon (Dönem 3 Kurul 1 çıkmış genetik sorusu).",
                "hint": "Mekanik kompresyon defekti."
            },
            {
                "id": "fc-dm-18",
                "question": "Deformasyonlar vücutta en sık hangi doku ve organ sistemlerini etkiler?",
                "answer": "Kas-iskelet sistemini; özellikle kemik, kıkırdak ve eklemleri tutar (kalça çıkığı, ayak ve kafa kemikleri).",
                "hint": "Kemik, kıkırdak ve eklemler."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Disrupsiyon: Normal Yapının Ekstrinsik veya Vasküler Yıkımı",
        "subtitle": "Amniyotik bant amputasyonları, vasküler kesinti (gastroşizis, atreziler) ve teratojenler",
        "badge": "Disrupsiyon",
        "badgeColor": "red",
        "target_ids": ["d3-k1-tbg-001"],
        "keywords": ["disrupsiyon", "amniyotik bant", "gastroşizis", "vasküler iskemi", "talidomid"],
        "lead": "Disrupsiyon; normal olarak gelişmekte olan bir organ veya vücut parçasının dışsal bir mekanik ajan veya vasküler iskemi/infarktüs sonucu parçalanması ve kalıcı olarak şekil bozukluğuna uğramasıdır.",
        "spotPearls": [
            "İKİ TEMEL PATOGENEZ: 1) Dış mekanik bantlar (Amniyotik bant sendromu), 2) Vasküler kan akımının kesintiye uğraması sonucu doku nekrozu ve rezorpsiyonu.",
            "AMNİYOTİK BANT: Amniyon zarının yırtılıp ipliksi bantlar oluşturarak fetal parmakları, ekstremiteleri boğması ve ampüte etmesi en klasik disrupsiyondur.",
            "VASKÜLER İNTESTİNAL ATREZİLER VE GASTROŞİZİS: Mezenterik arter tıkanması bağırsağın o segmentinde nekroza yol açarak atrezi ve disrupsiyona neden olur.",
            "SIFIR TEKRARLAMA RİSKİ: Disrupsiyonlar genetik değildir; aile için sonraki gebeliklerde tekrarlama riski yok denecek kadar azdır!"
        ],
        "keyBullets": [
            {"title": "Gelişimin Duraklaması ve Yıkımı", "desc": "Yapı başlangıçta kusursuz oluşurken maruz kalınan travma veya iskemi ile tahrip edilir."},
            {"title": "Embriyolojik Sınırlara Uymama", "desc": "Amniyotik bant lezyonları tek bir dermatom veya embriyolojik segmente uymaz; rastgele asimetrik amputasyonlar yapar."},
            {"title": "Teratojenik Disrupsiyon", "desc": "Talidomid gibi damar oluşumunu (anjiyogenezi) engelleyen teratojenler ekstremitelerin güdük kalmasına (fokomeli) yol açar."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-19",
                "question": "Amniyotik bant sendromunda gelişen ekstremite amputasyonunun disrupsiyon olarak adlandırılmasının temel sebebi nedir?",
                "answer": "Normal olarak oluşmuş bir ekstremitenin dış bir mekanik faktör (amniyon bandı) tarafından boğularak sekonder olarak yıkıma ve kopmaya uğramasıdır.",
                "hint": "Normal yapının sonradan yıkımı."
            },
            {
                "id": "fc-dm-20",
                "question": "Disrupsiyon tipi konjenital anomalilerin sonraki gebeliklerde tekrarlama riski nasıldır?",
                "answer": "Çok düşüktür (genetik bir mutasyondan değil rastlantısal mekanik/vasküler olaylardan kaynaklandığı için sporidiktir).",
                "hint": "Genetik olmayan sporadik risk."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Displazi: Doku Düzeyinde Anormal Hücresel Organizasyon",
        "subtitle": "Enzim ve yapısal protein bozuklukları, iskelet displazileri ve klinik ilerleyicilik",
        "badge": "Displazi",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["displazi", "hücresel organizasyon", "iskelet displazisi", "akondroplazi", "FGFR3"],
        "lead": "Dismorfolojide displazi; vücuttaki belirli bir doku tipinde hücrelerin anormal organizasyonu sonucu ortaya çıkan yapısal ve fonksiyonel morfogenez hatasıdır.",
        "spotPearls": [
            "HÜCRESEL VE ENZİMATİK BOZUKLUK: Hücre düzeyinde enzim yapımı veya yapısal protein sentezi bozulmuştur (örn. kollajen veya büyüme faktörü reseptör defektleri).",
            "SÜREKLİLİK VE İLERLEYİCİLİK: Dokuda intrinsik hücresel bozukluk bulunduğundan, çocuk büyüdükçe ve doku fonksiyon gördükçe KLİNİK BULGULAR GİDEREK AĞIRLAŞIR.",
            "MAJÖR ÖRNEKLER: İskelet displazileri (Akondroplazi - FGFR3 geni, Tanatoforik displazi), Ektodermal displaziler ve Lizozomal depo hastalıkları."
        ],
        "keyBullets": [
            {"title": "Patolojideki Displaziden Farkı", "desc": "Tıbbi genetikte displazi kanser öncüsü hücresel atipiyi değil, doku mimarisinin genetik gelişim bozukluğunu tanımlar."},
            {"title": "Mendelyen Kalıtım", "desc": "Displaziler çoğunlukla tek gen mutasyonlarına bağlı olup otozomal dominant veya resesif kalıtım gösterir (akondroplazi OD)."},
            {"title": "Sistemik Doku Tutulumu", "desc": "Hata tek bir organda değil, o dokunun vücutta bulunduğu her yerde izlenir (vücuttaki tüm endokondral kemikler etkilenir)."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-21",
                "question": "Tıbbi genetikte displazinin deformasyon ve malformasyondan en önemli seyirsel farkı nedir?",
                "answer": "Displastik dokularda intrinsik hücresel bozukluk sürekli olduğundan, yaş ilerledikçe ve çocuk büyüdükçe klinik bulguların progresif olarak ağırlaşmasıdır.",
                "hint": "Yaşla ağırlaşma ve süreklilik."
            },
            {
                "id": "fc-dm-22",
                "question": "En sık görülen kalıtsal orantısız cücelik nedeni olan Akondroplazi hangi anomali sınıfına ve hangi gen mutasyonuna aittir?",
                "answer": "İskelet displazisine aittir ve FGFR3 (Fibroblast Büyüme Faktörü Reseptörü 3) gen mutasyonundan kaynaklanır.",
                "hint": "İskelet displazisi ve FGFR3."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Birlikte Görülmelerine Göre Anomaliler: Dağılım ve Kombinasyon Paternleri",
        "subtitle": "İzole defektler (%60), sendromlar (%20), sekanslar (%10) ve asosiasyonlar (%3)",
        "badge": "Kombinasyonlar",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["izole", "sekans", "sendrom", "asosiasyon", "epidemiyoloji"],
        "lead": "Yenidoğanda konjenital anomali saptandığında, defektin tek başına mı yoksa diğer organ kusurlarıyla belirli bir kalıp içinde mi bulunduğu acilen ayırt edilmelidir.",
        "spotPearls": [
            "YENİDOĞAN DAĞILIMI: Konjenital anomalilerin yaklaşık %60-65'i İZOLE MAJÖR ANOMALİ, %20'si SENDROMLAR, %8-13'ü SEKANSLAR ve %3'ü ASOSİASYONLARDIR.",
            "İZOLE ANOMALİ: Tek bir organ sistemini tutar (yarık dudak, pilor stenozu, doğumsal kalça çıkığı). Kalıtımı genellikle multifaktöriyeldir.",
            "ÇOKLU ANOMALİ ŞÜPHESİ: Bir organda malformasyon saptandığında diğer sistemler (özellikle MSS, KVS, GİS) mutlaka ultrason ve ekokardiyografi ile taranmalıdır."
        ],
        "keyBullets": [
            {"title": "%60 İzole Baskınlığı", "desc": "Doğumsal kalp defekti veya yarık damaklı bebeklerin büyük kısmında başka hiçbir organ kusuru eşlik etmez."},
            {"title": "Sendrom Tanıma Gücü", "desc": "Birden fazla sistem tutulduğunda sendromik ayrım başlar; genetik tanı ve prognoz belirlenir."},
            {"title": "Sistemik Görüntüleme Kuralı", "desc": "Tek görünen anomalilerin altında gizli kardiyak veya renal malformasyonlar yatabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-23",
                "question": "Yenidoğan döneminde saptanan konjenital anomalilerin en büyük yüzdesini hangi grup oluşturur?",
                "answer": "%60-65 ile İzole majör anomaliler oluşturur.",
                "hint": "Tek organ tutulumu oranı."
            },
            {
                "id": "fc-dm-24",
                "question": "Birlikte görülmelerine göre konjenital anomali sınıflamasının 4 ana kategorisi hangileridir?",
                "answer": "1) İzole anomaliler, 2) Sekanslar, 3) Asosiasyonlar, 4) Sendromlar.",
                "hint": "Dört kombinasyon paterni."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Sekanslar (Kaskadlar): Tek Primer Defektten Doğan Çığ Etkisi",
        "subtitle": "Primer bozukluğun tetiklediği ardışık sekonder zincirleme anomaliler",
        "badge": "Sekans",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["sekans", "kaskad", "potter sekansı", "nöral tüp sekansı", "pierre robin"],
        "lead": "Sekans; erken morfogenez döneminde altta yatan tek bir primer yapısal defektin (malformasyon, deformasyon veya disrupsiyon) ardışık bir dizi sekonder anomaliyi çığ gibi tetiklemesidir.",
        "spotPearls": [
            "ZİNCİRLEME REAKSİYON: Başlatıcı tek bir primer olay vardır; diğer tüm morfolojik bozukluklar bu primer olayın kaçınılmaz mekanik veya fizyolojik sonuçlarıdır.",
            "BAŞLATICI DEFEKT TİPİ: Sekansı başlatan defekt bir malformasyon (renal agenezi), deformasyon veya disrupsiyon olabilir.",
            "EN BİLİNEN ÖRNEKLER: POTTER Sekansı, Nöral Tüp Defekti Sekansı (Meningomyelosel -> Hidrosefali + Pes ekinovarus) ve Pierre Robin Sekansı."
        ],
        "keyBullets": [
            {"title": "Tek Primer Neden", "desc": "Sendromlarda birden fazla bağımsız etki varken, sekansta tüm bulgular tek bir başlangıç noktasına indirgenebilir."},
            {"title": "Pierre Robin Kaskadı", "desc": "Mikrognati (çene küçüklüğü) -> Dilin geriye düşmesi (glosopitozis) -> Damak plaklarının birleşememesi -> U-şekilli yarık damak."},
            {"title": "Tekrarlama Riski", "desc": "Sekansın tekrarlama riski sekansı başlatan primer defektin genetik modeline (tek gen veya multifaktöriyel) göre belirlenir."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-25",
                "question": "Klinik genetikte 'Sekans' kavramı neyi ifade eder?",
                "answer": "Erken morfogenezde altta yatan tek bir primer defektin domino taşı gibi ardışık sekonder anomaliler dizisine yol açmasıdır.",
                "hint": "Çığ veya domino etkisi."
            },
            {
                "id": "fc-dm-26",
                "question": "Pierre Robin sekansında U-şekilli yarık damağa yol açan başlatıcı primer anatomik kusur nedir?",
                "answer": "Mandibula hipoplazisidir (mikrognati / alt çene küçüklüğü); dil geriye itilerek damakların birleşmesini engeller.",
                "hint": "Mikrognati ve glosopitozis."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "Potter Sekansı: Renal Agenezi, Oligohidramniyos ve Letal Pulmoner Hipoplazi",
        "subtitle": "Fetal idrar eksikliği, uterin bası, fasial distorsiyon ve solunum yetmezliği",
        "badge": "Potter Sekansı",
        "badgeColor": "red",
        "target_ids": ["d3-k1-tbg-001"],
        "keywords": ["potter sekansı", "renal agenezi", "oligohidramniyos", "pulmoner hipoplazi", "potter yüzü"],
        "lead": "Potter sekansı; bilateral böbrek yokluğu veya idrar çıkış yolu tıkanıklığının amniyotik sıvıyı tüketerek fetusu ezdiği ve akciğer gelişimini durdurduğu en dramatik sekans örneğidir.",
        "spotPearls": [
            "ZİNCİRİN İLK HALKASI: BİLATERAL RENAL AGENEZİ (veya obstrüktif üropati) -> Fetus idrar üretemez.",
            "ZİNCİRİN İKİNCİ HALKASI: OLİGOHİDRAMNİYOS (Amniyotik sıvının temel kaynağı 16. haftadan sonra fetal idrardır).",
            "MEKANİK EZİLME (DEFORMASYON): Amniyotik yastık kaybolunca uterus fetusu ezer -> 'Potter Yüzü' (basık gaga burun, basık düşük kulaklar, basık çene) ve Pes ekinovarus (talipes).",
            "ÖLÜM NEDENİ - PULMONER HİPOPLAZİ: Amniyotik sıvı akciğer bronş dallanmasını stimüle edemez; akciğer hipoplazisi nedeniyle bebek doğumdan dakikalar sonra solunum yetmezliğinden kaybedilir!"
        ],
        "keyBullets": [
            {"title": "Amniyotik Sıvının Yaşamsal Rolü", "desc": "Sıvı sadece bebeği çarpmalardan korumaz, fetal solunum hareketleriyle alveollerin açılmasını ve gelişmesini sağlar."},
            {"title": "Bilateral vs Unilateral", "desc": "Tek taraflı renal agenezide diğer böbrek idrar ürettiği için Potter sekansı gelişmez; bilateral agenezi letaldir."},
            {"title": "Görsel İpuçları (Şekil)", "desc": "Basık yüz, papağan gagası burun, infraorbital kıvrımlar ve ayak deformiteleri tipik kompresyon bulgularıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-27",
                "question": "Potter sekansında yenidoğan bebeğin doğumdan kısa süre sonra kaybedilmesine (exitus) yol açan temel patoloji nedir?",
                "answer": "Pulmoner Hipoplazi (amniyotik sıvı yetersizliğine bağlı akciğer gelişiminin durması sonucu ağır solunum yetmezliği).",
                "hint": "Akciğer gelişememesi."
            },
            {
                "id": "fc-dm-28",
                "question": "Potter sekansında oligohidramniyoz gelişmesinin temel primer patolojik sebebi nedir?",
                "answer": "Bilateral renal agenezi (her iki böbreğin yokluğu) veya alt üriner sistem obstrüksiyonudur (fetal idrar yapılamaması).",
                "hint": "Böbreklerin olmaması."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Asosiasyonlar (Birliktelikler): VACTERL ve MURCS",
        "subtitle": "Rastlantısal olasılıktan sık birleşen, ortak genetik modeli olmayan anomali kümeleri",
        "badge": "Asosiasyon",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["asosiasyon", "VACTERL", "MURCS", "anal atrezi", "TEF"],
        "lead": "Asosiasyon; iki veya daha fazla konjenital anomalinin rastgele görülme olasılığından istatistiksel olarak belirgin şekilde daha sık bir arada bulunduğu, ancak ortak bir genetik nedeni gösterilemeyen anomali topluluğudur.",
        "spotPearls": [
            "SENDROMLARDAN FARKI: Ortak bilinen tek bir genetik nedeni ve öngörülebilir kalıtım modeli YOKTUR; bu nedenle 'Sendrom' olarak adlandırılamaz.",
            "VACTERL ASOSİASYONU: V: Vertebral anomaliler, A: Anal atrezi, C: Kardiyak defektler (VSD vb.), TE: Trakeoözofageal fistül ve özofagus atrezisi, R: Renal anomaliler, L: Limb (Ekstremite - radial agenezi) anomalileri.",
            "KLİNİK ALGORİTMA: ANAL ATREZİ saptanan her yenidoğanda mutlaka omurga grafileri çekilmeli, EKO ile kalp ve USG ile böbrekler taranmalıdır!",
            "TEKRARLAMA RİSKİ: Oldukça düşüktür (<%1), aileye danışmada rahatlatıcı bilgi verilir."
        ],
        "keyBullets": [
            {"title": "MURCS Asosiasyonu", "desc": "Müllerian kanal aplazisi (uterus yokluğu), Renal aplazi ve Servikotorasik somit displazisi birlikteliğidir."},
            {"title": "Kombinasyon Esnekliği", "desc": "VACTERL tanısı için tüm harflerin bulunması şart değildir; 3 veya daha fazla komponentin bir arada bulunması yeterlidir."},
            {"title": "Embriyolojik Bağımsızlık", "desc": "Etkilenen yapılar embriyolojik olarak aynı dokudan köken almaz ve komşu değildir; mezodermal erken bir aksaklık düşünülmektedir."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-29",
                "question": "VACTERL asosiasyonunun baş harflerini oluşturan 6 temel konjenital anomali grubu hangileridir?",
                "answer": "Vertebral anomaliler, Anal atrezi, Kardiyak defektler, Trakeoözofageal fistül (TEF), Renal anomaliler ve Limb (ekstremite) defektleri.",
                "hint": "V-A-C-TE-R-L açılımı."
            },
            {
                "id": "fc-dm-30",
                "question": "Asosiasyonların sendromlardan en kritik genetik danışmanlık farkı nedir?",
                "answer": "Belli bir kalıtım modeli ve bilinen ortak bir genetik etiyolojisi olmaması ve sonraki gebeliklerde tekrarlama riskinin çok düşük olmasıdır.",
                "hint": "Kalıtım modelinin olmaması."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Sendromlar: Ortak Etiyolojiye Dayanan İyi Tanımlanmış Anomali Kalıpları",
        "subtitle": "Kromozomal, mikrodelesyon ve tek gen sendromları (Down, Angelman, Williams)",
        "badge": "Sendromlar",
        "badgeColor": "violet",
        "target_ids": [],
        "keywords": ["sendrom", "down sendromu", "williams", "angelman", "prader willi"],
        "lead": "Sendrom; bilinen tek bir ortak etiyolojik nedene (kromozom anomalisi, delesyon, tek gen mutasyonu, teratojen) dayanan ve birden fazla organ sistemini tutan iyi tanımlanmış anomaliler bütünüdür.",
        "spotPearls": [
            "SENDROM TANIMI: Birden fazla sistemin etkilendiği, ortak bir etiyolojisi ve tanımlanabilen kalıtım şekli bulunan konjenital anomaliler birlikteliğidir.",
            "DOWN SENDROMU (Trizomi 21): Tipik dismorfik yüz (epikantus, basık burun kökü), avuç içinde tek transvers fleksiyon çizgisi (SİMİAN ÇİZGİSİ), 1-2. ayak parmak arası açık (sandal yarığı), AVSD/kardiyak defektler, duodenal atrezi, lösemi ve erken Alzheimer riski.",
            "WILLIAMS SENDROMU: 7q11.23 mikrodelesyonu (ELN - elastin geni); Elfin benzeri yüz, supravalvüler aort darlığı, infantil hiperkalsemi ve aşırı dışadönük/sosyal kişilik."
        ],
        "keyBullets": [
            {"title": "Etiyolojik Dağılım", "desc": "Sendromların etiyolojisinde kromozomal anormallikler (%10), tek gen mutasyonları (%22) ve teratojenler (%5) yer alır."},
            {"title": "Angelman Sendromu", "desc": "15q11-q13 maternal delesyon (UBE3A geni); mutlu kukla görünümü, nedensiz kahkahalar, ataksik yürüyüş ve ağır konuşma geriliği."},
            {"title": "Prader-Willi Sendromu", "desc": "15q11-q13 paternal delesyon; yenidoğanda ağır hipotoni, çocuklukta doyma hissi kaybı (hiperfaji), morbid obezite ve hipogonadizm."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-31",
                "question": "Williams sendromundan sorumlu olan kromozomal mikrodelesyon bölgesi ve etkilenen temel yapısal gen hangisidir?",
                "answer": "7q11.23 mikrodelesyonu ve ELN (elastin) genidir.",
                "hint": "7q11.23 ve elastin geni."
            },
            {
                "id": "fc-dm-32",
                "question": "Down sendromunda avuç içinde görülen ve iki transvers çizginin birleşmesiyle oluşan tek yatay çizgiye ne ad verilir?",
                "answer": "Simian çizgisi (tek palmar fleksiyon çizgisi).",
                "hint": "Tek avuç içi çizgisi."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Frajil X Sendromu: Dinamik Trinükleotid Tekrarı ve X'e Bağlı Mental Retardasyon",
        "subtitle": "FMR1 geni, CGG tekrar artışı (>200 tam mutasyon), makroorşidizm ve otizm",
        "badge": "Frajil X",
        "badgeColor": "red",
        "target_ids": [],
        "keywords": ["frajil x", "FMR1", "CGG tekrarı", "dinamik mutasyon", "makroorşidizm"],
        "lead": "Frajil X sendromu; erkeklerde Down sendromundan sonra zeka geriliğinin en sık nedeni olup, kalıtsal mental retardasyonun ise dünyadaki bir numaralı nedenidir.",
        "spotPearls": [
            "BİR NUMARALI KALITSAL MR: Kalıtsal mental retardasyonun en sık nedenidir (Erkeklerde 1/4000, kadınlarda 1/6000).",
            "DİNAMİK MUTASYON MEKANİZMASI: FMR1 geninin 5' UTR bölgesindeki (CGG)n üçlü nükleotid tekrar sayısının artışıdır (Normal: 6-54; Premutasyon: 55-200; TAM MUTASYON: >200 tekrar).",
            "GEN SUSTURULMASI: Tekrar sayısı 200'ü aştığında promoter bölgesi hipermetillenir; FMR1 geni susar ve FMRP proteini sentezlenemez.",
            "KLİNİK TRİAD: 1) Uzun ince yüz ve belirgin çene, 2) Büyük/belirgin kulaklar, 3) Puberte sonrası dev testisler (MAKROORŞİDİZM). Olguların %60'ında otizm spektrumu eşlik eder!"
        ],
        "keyBullets": [
            {"title": "Dinamik Değişkenlik", "desc": "Tekrar sayısı kuşaktan kuşağa anneden geçerken amplifiye olarak (büyüyerek) aktarılır (antisipasyon)."},
            {"title": "Davranışsal Fenotip", "desc": "Göz kontağından kaçınma, el çırpma/sallama, el ısırma, dokunmaya aşırı duyarlılık ve hiperaktivite tipiktir."},
            {"title": "Bağ Dokusu Bulguları", "desc": "Eklem laksisitesi (çift eklemli parmaklar), pektus ekskavatum ve mitral kapak prolapsusu (MVP) eşlik edebilir."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-33",
                "question": "Frajil X sendromunda tam mutasyon sınırını oluşturan CGG trinükleotid tekrar sayısı kaçtır ve genetik susturma nasıl gerçekleşir?",
                "answer": "Tekrar sayısı 200'ün üzerindedir (>200); promoter bölgesinin hipermetilasyonu sonucu FMR1 geni susturulur ve FMRP proteini yapılamaz.",
                "hint": "200 üzeri tekrar ve metilasyon."
            },
            {
                "id": "fc-dm-34",
                "question": "Frajil X sendromlu erkeklerde puberte sonrasında gelişen en karakteristik fiziksel muayene bulgusu nedir?",
                "answer": "Makroorşidizm (testislerin normalden belirgin olarak büyük olması).",
                "hint": "Büyük testisler."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Dismorfik Hastada Tanı Algoritması ve Genetik Test Basamakları",
        "subtitle": "Karyotip, Kromozomal Mikroarray (CMA), hedefe yönelik paneller ve WES'in yeri",
        "badge": "Tanı Algoritması",
        "badgeColor": "sky",
        "target_ids": [],
        "keywords": ["karyotip", "mikroarray", "WES", "tanı algoritması", "gen paneli"],
        "lead": "Dismorfik bir bebek veya çocuk değerlendirilirken pahalı ve yorucu testlere körlemesine başvurulmamalı; akılcı basamaklı bir genetik tanı algoritması izlenmelidir.",
        "spotPearls": [
            "SENDROM ŞÜPHESİ VARSA: Doğrudan hedefe yönelik spesifik test yapılır (Down için karyotip, Williams/22q11 için FISH/MLPA, Frajil X için PCR/üçlü tekrar analizi).",
            "SENDROM ŞÜPHESİ YOKSA (İLK BASAMAK): 1. Aşama Karyotipleme -> 2. Aşama Kromozomal Mikroarray (CMA / aCGH) -> 3. Aşama Gen Panelleri -> SON ÇARE: Tüm Ekzom Dizi Analizi (WES).",
            "WES İLK AŞAMA TESTİ DEĞİLDİR: WES pahalıdır, analizi zordur, hasta başına 10-15 bin varyant üretir ve büyük dengeli delesyon/translokasyonları GÖSTEREMEZ!"
        ],
        "keyBullets": [
            {"title": "Karyotipin Gücü", "desc": "Işık mikroskobunda 5 Mb üzeri büyük kromozomal translokasyon ve sayı anomalilerini en ucuz yoldan gösterir."},
            {"title": "Mikroarray (CMA) Devrimi", "desc": "Karyotipin göremediği submikroskobik kopya sayısı değişikliklerini (CNV: delesyon ve duplikasyonlar) 50-100 kb çözünürlükle yakalar."},
            {"title": "Klinik Önemi Belirsiz Varyant (VUS)", "desc": "WES yapıldığında çıkan binlerce varyantın anlamlandırılması güçtür; bu yüzden ilk basamakta önerilmez."}
        ],
        "table": {
            "title": "Dismorfik Hastada Basamaklı Genetik Tanı Yöntemleri ve Özellikleri",
            "headers": ["Tanı Yöntemi", "Çözünürlük Seviyesi", "Saptadığı Anomaliler", "Kullanım Basamağı"],
            "rows": [
                ["Konvansiyonel Karyotip", "> 5 MegaBaz (Mb)", "Sayısal anomaliler, Dengeli/dengesiz büyük translokasyonlar", "1. Basamak temel tarama testi"],
                ["Kromozomal Mikroarray (CMA)", "50 - 100 KiloBaz (kb)", "Submikroskobik mikrodelesyonlar ve duplikasyonlar (CNV)", "Karyotip normalse 2. Basamak altın standart"],
                ["FISH / MLPA", "Gene özgü tek prob", "Hedeflenen spesifik mikrodelesyonlar (22q11, 7q11, vb.)", "Spesifik sendrom şüphesinde hızlı tanı"],
                ["Hedefe Yönelik NGS Panelleri", "Tek nükleotid düzeyinde", "Klinik fenotipe uyan gen grubundaki (örn. 50 gen) mutasyonlar", "Fenotipe özgü genetik arama"],
                ["Tüm Ekzom Dizi Analizi (WES)", "Tüm ekzom (20.000 gen)", "Nadir tek gen mutasyonları, yeni varyantlar", "SON ÇARE (Diğer tüm testler negatifse)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-dm-35",
                "question": "Belirgin bir klinik sendrom şüphesi olmayan, açıklanamayan multipl konjenital anomalili bir bebekte karyotip normalse ikinci basamakta hangi test istenmelidir?",
                "answer": "Kromozomal Mikroarray analizi (CMA / aCGH - kopya sayısı değişikliklerini taramak için).",
                "hint": "Mikroarray / aCGH."
            },
            {
                "id": "fc-dm-36",
                "question": "Neden Tüm Ekzom Dizi Analizi (WES) dismorfik hastada ilk basamakta istenmemelidir?",
                "answer": "Pahalı olması, analizinin çok uzun sürmesi, 10-15 bin varyant üretmesi ve dengeli translokasyonlar ile büyük delesyon/duplikasyonları saptayamaması nedeniyle.",
                "hint": "Pahalı, karmaşık ve dengeli yapıları görememe."
            }
        ]
    },
    {
        "slideNumber": 19,
        "title": "NGS Varyant Analizi ve ACMG Sınıflama Kılavuzu",
        "subtitle": "Patojenik, Muhtemelen Patojenik, VUS, Muhtemelen Benign ve Benign sınıfları",
        "badge": "Varyant Analizi",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["ACMG", "VUS", "patojenik", "benign", "varyant"],
        "lead": "Yeni Nesil Dizileme (NGS) teknolojileriyle saptanan genetik mutasyonlar, Amerikan Tıbbi Genetik Koleji (ACMG) kriterlerine göre 5 standart kategoride raporlanır.",
        "spotPearls": [
            "ACMG BEŞLİ SINIFLAMASI: 1) Patojenik, 2) Muhtemelen Patojenik, 3) VUS (Variant of Uncertain Significance - Klinik Önemi Belirsiz), 4) Muhtemelen Benign, 5) Benign.",
            "VUS İKİLEMİ: VUS saptandığında hastaya kesin tanı konulamaz ve gebelik terminasyonu veya radikal cerrahi gibi klinik kararlar ASLA VUS'a dayandırılamaz!",
            "VERİ TABANI GÜNCELLEMESİ: VUS çıkan hastaların genetik verileri 6 ay-1 yılda bir literatür ve popülasyon veri tabanları (GnomAD, ClinVar) taranarak yeniden değerlendirilir."
        ],
        "keyBullets": [
            {"title": "Popülasyon Veri Tabanları", "desc": "GnomAD ve 1000 Genomes'ta sıklığı %1'in üzerinde olan varyantlar genellikle zararsız benign polimorfizmlerdir."},
            {"title": "In Silico Yazılımlar", "desc": "PolyPhen-2, SIFT ve MutationTaster gibi biyoinformatik araçlar mutasyonun protein yapısına zarar verip vermeyeceğini simüle eder."},
            {"title": "Segregasyon Analizi", "desc": "Aynı varyantın ailedeki diğer hasta bireylerde bulunup sağlıklı bireylerde bulunmaması patojeniteyi kanıtlar."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-37",
                "question": "ACMG kılavuzuna göre klinik önemi belirsiz olan ve tedavi/terminasyon kararı aldırmayan varyant grubuna ne ad verilir?",
                "answer": "VUS (Variant of Uncertain Significance).",
                "hint": "Klinik önemi belirsiz varyant."
            },
            {
                "id": "fc-dm-38",
                "question": "Bir DNA sekans değişikliğinin toplumda %1'den daha sık görülmesi onun patojenik bir mutasyon mu yoksa benign polimorfizm mi olduğunu düşündürür?",
                "answer": "Benign bir polimorfizm (zararsız varyant) olduğunu düşündürür.",
                "hint": "%1 frekans eşiği."
            }
        ]
    },
    {
        "slideNumber": 20,
        "title": "Sentez ve Özet: Dismorfolojik Karar Ağacı ve Kurul 1 Altın İpuçları",
        "subtitle": "Dr. Öğr. Üyesi Serap Arslan amfi dersi çekirdek sentezi ve sınav spotları",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-tbg-001"],
        "keywords": ["altın spotlar", "kurul 1", "tbg çıkmış soru", "serap arslan"],
        "lead": "Dismorfoloji; hekimin görsel muayene titizliği ile modern genomik teknolojileri birleştiren eşsiz bir klinik dedektiflik sanatıdır.",
        "spotPearls": [
            "DÖRT BÜYÜK DEFEKT: Malformasyon (intrinsik hata; yarık damak/kalp), Deformasyon (mekanik bası; pes ekinovarus / kalça çıkığı), Disrupsiyon (dışsal yıkım; amniyotik bant amputasyonu), Displazi (dokuda hücresel organizasyon bozukluğu; akondroplazi).",
            "DÖRT KOMBİNASYON: İzole (%60), Sekans (%10; Potter sekansı), Asosiasyon (%3; VACTERL - kalıtım modeli yok), Sendrom (%20; Down, Williams, Frajil X - ortak etiyoloji).",
            "MİNOR ANOMALİ ALARMI: 3 veya daha fazla minör anomali saptandığında %90 majör anomali eşliği aranmalıdır.",
            "GENETİK TEST KURALI: Belirli sendrom şüphesi yoksa Karyotip -> CMA -> Gen Paneli -> En son WES!"
        ],
        "keyBullets": [
            {"title": "Anamnez ve 3 Kuşak Pedigri", "desc": "Akraba evliliği, teratojen maruziyeti, tekrarlayan düşükler ve ebeveyn yaşı dikkatle kaydedilmelidir."},
            {"title": "Antropometrik Muayene", "desc": "-3SD mikrosefali ve boy kısalığı; +3SD makrosefali; gözler arası mesafe (telekantus vs hipertelorizm) ölçülmelidir."},
            {"title": "Non-Direktif Yaklaşım", "desc": "Aileye asla 'gebeligi sonlandırın' veya 'kesin doğurun' denmez; riskler tam aktarılarak karar aileye bırakılır."}
        ],
        "flashcards": [
            {
                "id": "fc-dm-39",
                "question": "Dönem 3 Kurul 1 Tıbbi Genetik sınavında deformasyon, disrupsiyon ve malformasyon için en klasik birer örnek nedir?",
                "answer": "Deformasyon = Oligohidramnioza bağlı pes ekinovarus/kraniyofasiyal basıklık; Disrupsiyon = Amniyotik bant amputasyonu; Malformasyon = Yarık dudak-damak veya Fallot tetralojisi.",
                "hint": "Üç majör prototip örnek."
            },
            {
                "id": "fc-dm-40",
                "question": "VACTERL ile Down sendromu arasındaki en temel sınıflama ve kalıtım farkı nedir?",
                "answer": "Down sendromu bilinen ortak bir genetik etiyolojiye (Trizomi 21) dayanan bir 'Sendrom' iken; VACTERL ortak bir genetik nedeni gösterilemeyen ve rastgele birliktelikten sık görülen bir 'Asosiasyon'dur.",
                "hint": "Sendrom vs Asosiasyon."
            }
        ]
    }
]

def build_synthesis_narrative(slide_data):
    lines = []
    lines.append(f"### {slide_data['title']}")
    lines.append(f"#### {slide_data['subtitle']}")
    lines.append("")
    lines.append(f"• **Temel Tıbbi Genetik Çerçevesi:** {slide_data['lead']}")
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
            f"Dr. Öğr. Üyesi Serap Arslan'ın ders anlatımında '{title_clean}' konusundaki en can alıcı sınav vurguları nelerdir?",
            f"Dismorfolojide malformasyon, deformasyon ve disrupsiyon ayrımını '{title_clean}' bağlamında açıklar mısın?",
            f"Klinik genetik yaklaşımında '{title_clean}' tablosuyla gelen bir yenidoğanda basamaklı test algoritması nasıl işletilmelidir?"
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
        "id": "learn-dismorfoloji-terminolojisi",
        "title": "Dismorfolojide Genetik Terminoloji ve Malformasyonlar",
        "shortTitle": "Dismorfoloji Terminolojisi",
        "discipline": "Tıbbi Genetik",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Dr. Öğr. Üyesi Serap Arslan",
        "sourceFile": "1)DİSMORFOLOJİDE GENETİK TERMİNOLOJİ.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "indigo",
        "overview": "Dönem 3 Kurul 1 Tıbbi Genetik müfredatında yer alan Dismorfolojide Genetik Terminoloji dersinin %500 derinlikte kapsamlı interaktif öğrenim sunumu. Malformasyon, deformasyon, disrupsiyon, displazi, izole defektler, sekanslar (Potter sekansı), asosiasyonlar (VACTERL), sendromlar (Down, Williams, Frajil X), basamaklı genetik tanı algoritması ve ACMG varyant sınıflamasını, 40 adet 3D akıl kartını, 5 adet karşılaştırma tablosunu ve Kurul 1 çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "Deformasyon: Dış mekanik bası sonucu normal dokunun şekil değiştirmesidir (oligohidramnioza bağlı kraniyofasyal basıklık ve pes ekinovarus - Kurul 1 Çıkmış Soru #1).",
            "Malformasyon: Embriyonik organogenezde primer doku oluşum hatasıdır (yarık dudak-damak, VSD, spina bifida).",
            "Disrupsiyon: Normal gelişen yapının dış mekanik bant veya vasküler iskemiyle parçalanmasıdır (amniyotik bant amputasyonu, gastroşizis; kalıtsal değildir).",
            "Displazi: Doku düzeyinde hücresel organizasyon bozukluğudur (akondroplazi - FGFR3; klinik bulgular yaşla ağırlaşır).",
            "3 veya daha fazla minör anomalisi olan bebekte %90 olasılıkla eşlik eden bir majör anomali veya sendrom mevcuttur.",
            "Potter sekansında ölüm nedeni bilateral renal agenezi değil, oligohidramniyozun yol açtığı PULMONER HİPOPLAZİDİR.",
            "VACTERL ortak genetik modeli olmayan bir ASOSİASYONDUR; Vertebral, Anal atrezi, Kardiyak, TEF, Renal, Limb komponentlerinden oluşur.",
            "Williams sendromu 7q11.23 mikrodelesyonu (ELN - elastin geni); Elfin yüz, supravalvüler aort darlığı ve hiperkalsemi ile seyreder.",
            "Frajil X sendromu kalıtsal mental retardasyonun 1 numaralı nedenidir; FMR1 geni 5' UTR CGG tekrarı >200 tam mutasyon, makroorşidizm ve otizm görülür.",
            "Basamaklı genetik tanı algoritması: Karyotipleme -> Mikroarray (CMA) -> Gen Panelleri -> Son Çare: WES!"
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Dismorfolojide Genetik Terminoloji...")
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
            elif item.get('id') == 'learn-kromozomal-hastaliklar-ve':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Dismorfoloji completed, Kromozomal Hastalıklar next!")

    print("Success! Dismorphology deck generation completed.")

if __name__ == '__main__':
    main()
