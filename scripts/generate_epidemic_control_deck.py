#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generate_epidemic_control_deck.py
Generates the comprehensive %500 detail 18-slide learning deck for:
"Salgın Hastalıklarda Kontrol, Sürveyans ve Korunma" (Halk Sağlığı - Uzm. Dr. Erkay Nacar)
Incorporating 18 slides, 36 3D flashcards, 5 comparison tables, and matched Kurul 1 exam questions (d3-k1-hs-007, d3-k1-hs-008, d3-k1-hs-016, d3-k1-hs-017, d3-k1-enf-001, d3-k1-hs-004, d3-k1-hs-005).
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Halk Sağlığı müfredatında salgın hastalıklarda kontrol ve korunma ile doğrudan ilişkilidir.'
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
                        'explanation': q.get('explanation') or 'Bu soru Kurul 1 Halk Sağlığı müfredatında salgın hastalıklarda kontrol ve korunma ile doğrudan ilişkilidir.'
                    })
                    if len(matched) >= max_count:
                        break

    return matched

SLIDES_DATA = [
    {
        "slideNumber": 1,
        "title": "Bulaşıcı Hastalıkların Yeniden Ortaya Çıkışı ve 1970 Yanılgısı",
        "subtitle": "1970'ler sonu aşırı iyimserlik, 1500'den fazla yeni patojen ve HIV epidemisi",
        "badge": "Giriş & Tarihçe",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-hs-001"],
        "keywords": ["bulaşıcı hastalık", "yeniden ortaya çıkan", "halk sağlığı tarihi"],
        "lead": "1970'li yıllarda antibiyotiklerin çeşitlenmesi ve kitlesel aşılamaların başarısı, tıp dünyasında bulaşıcı hastalıkların artık insanlık için bir tehdit oluşturmayacağı yanılgısını doğurmuştu; ancak tarih bu beklentiyi boşa çıkardı.",
        "spotPearls": [
            "1970 YANILGISI: 1970'lerde enfeksiyon hastalıklarının kontrol altına alındığı düşünülürken o günden bugüne 1500'DEN FAZLA YENİ PATOJEN (HIV, Ebola, SARS, MERS, vb.) tanımlanmıştır.",
            "HIV'IN AĞIR TABLOSU: Yalnızca HIV virüsü dünya genelinde 70 milyondan fazla insanı enfekte etmiş ve 35 milyondan fazla insanın ölümüne yol açmıştır.",
            "TEHDİT KESİNTİSİZ SÜRÜYOR: Antibiyotik direnci, zoonotik sıçramalar ve ekolojik tahribat nedeniyle bulaşıcı hastalıklar küresel halk sağlığının bir numaralı güvenlik tehdididir."
        ],
        "keyBullets": [
            {"title": "Gelişmiş Tedavilere Rağmen Tehdit", "desc": "Antimikrobiyal ilaçlar patojenlerin evrimsel seleksiyon baskısını artırarak dirençli suşların ortaya çıkmasına zemin hazırlamıştır."},
            {"title": "Ekolojik Denge Bozulması", "desc": "Ormansızlaşma, vahşi yaşam pazarları ve hızlı kentleşme hayvan-insan temasını artırarak yeni salgınlara kapı aralamıştır."},
            {"title": "Sürekli Teyakkuz Gereksinimi", "desc": "Halk sağlığı sistemlerinin rehavete kapılmadan her an yeni bir pandemiye hazır sürveyans ağları kurması zorunludur."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-1",
                "question": "1970'li yıllardan sonra antibiyotik ve aşıların gelişimiyle bulaşıcı hastalıkların bittiği zannedilirken günümüze kadar kaç yeni patojen keşfedilmiştir?",
                "answer": "1500'den fazla yeni patojen (HIV, Ebola, SARS, MERS, Zika vb.) keşfedilmiştir.",
                "hint": "1500'den fazla patojen."
            },
            {
                "id": "fc-ep-2",
                "question": "Yalnızca HIV pandemisi dünya genelinde kaç milyon kişiyi enfekte etmiş ve kaç milyon kişinin ölümüne yol açmıştır?",
                "answer": "70 milyondan fazla kişiyi enfekte etmiş, 35 milyondan fazla kişinin ölümüne yol açmıştır.",
                "hint": "70 milyon enfeksiyon, 35 milyon ölüm."
            }
        ]
    },
    {
        "slideNumber": 2,
        "title": "21. Yüzyılda Salgınların Dinamikleri: Küreselleşme ve Jet Hızı",
        "subtitle": "Kıtalararası uçak seyahati, 2009 H1N1 yayılımı ve 2015 Güney Kore MERS epidemisi",
        "badge": "Küresel Dinamikler",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["küreselleşme", "h1n1", "mers epidemisi", "uçak seyahati"],
        "lead": "21. yüzyılda salgınlar insanlık tarihinde hiç olmadığı kadar hızlı ve geniş coğrafyalara yayılmaktadır; önceden aylar veya yıllar alan yayılım bugün kıtalararası bir uçağın uçuş süresine inmiştir.",
        "spotPearls": [
            "JET HIZIYLA KÜRESELLEŞME: Önceden lokal kalan salgınlar günümüzde kıtalararası bir yolcu uçağının uçabildiği hızla (24 saatten kısa sürede) tüm dünyaya yayılabilmektedir.",
            "2009 H1N1 PANDEMİSİ: 2009 domuz gribi salgını 9 AYDAN DAHA KISA bir sürede dünyanın tüm kıtalarına ulaşmayı başarmıştır.",
            "2015 GÜNEY KORE MERS EPİDEMİSİ: Orta Doğu'dan MERS virüsünü taşıyan TEK BİR YOLCU Güney Kore'ye iniş yapmış; ülkede 186 vaka ve 36 ölümle sonuçlanan büyük bir hastane salgını başlatmıştır!"
        ],
        "keyBullets": [
            {"title": "Havalimanları ve Salgın Kapıları", "desc": "Modern ulaşım ağları semptomsuz kuluçka dönemindeki yolcuların binlerce kilometre uzağa patojen taşımasına imkan tanır."},
            {"title": "Sağlık Kuruluşlarında Amplifikasyon", "desc": "Erken tanı konamayan indeks vaka acil servislerde ve hastane koridorlarında diğer hastalara ve sağlık personeline hızla bulaşır."},
            {"title": "Zaman Pencerelerinin Daralması", "desc": "Halk sağlığı ekiplerinin ilk vakayı fark edip izolasyonu başlatması için sahip olduğu süre günler değil saatler düzeyindedir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-3",
                "question": "2009 H1N1 (domuz gribi) salgını tüm kıtalara ne kadar sürede ulaşmıştır?",
                "answer": "9 aydan daha kısa bir süre içinde dünyanın tüm kıtalarına yayılmıştır.",
                "hint": "9 aydan kısa sürede."
            },
            {
                "id": "fc-ep-4",
                "question": "2015 yılında Güney Kore'de 186 vaka ve 36 ölüme yol açan MERS salgını ülkeye nasıl giriş yapmıştır?",
                "answer": "Orta Doğu'dan MERS virüsünü taşıyan tek bir havayolu yolcusunun ülkeye girişiyle başlamıştır.",
                "hint": "Tek bir yolcu ile."
            }
        ]
    },
    {
        "slideNumber": 3,
        "title": "Yeni Ortaya Çıkan Patojenler ve Zoonotik Tehdit: %70 Kuralı",
        "subtitle": "Zoonozlar, hayvan ticareti, canlı hayvan pazarları ve 'Tek Sağlık' (One Health) zorunluluğu",
        "badge": "Zoonozlar & Tek Sağlık",
        "badgeColor": "emerald",
        "target_ids": [],
        "keywords": ["zoonoz", "hayvan kaynaklı", "ortaya çıkan patojenler", "tek sağlık"],
        "lead": "Salgınlara neden olan mikroorganizmalar ya tamamen yeni ortaya çıkmış (emerging) ya da daha önce bilinen ancak yeniden canlanan (re-emerging) patojenlerdir; bu patojenlerin en büyük rezervuarı hayvanlar alemidir.",
        "spotPearls": [
            "%70 HAYVAN KAYNAKLI KURALI: İnsanlarda yeni ortaya çıkan enfeksiyon patojenlerinin yaklaşık %70'İ HAYVAN KAYNAKLIDIR (zoonotik kökenli).",
            "ZOONOTİK TEHDİDİN NEDENİ: Hayvanların tarımda yoğun kullanılması, ticari amaçla kıtalararası taşınması ve canlı hayvan pazarlarında farklı türlerle ve insanlarla yakın temasta bulunması türler arası bariyeri kaldırır.",
            "SAĞLIKLI ÇEVRE ŞARTI: İnsan sağlığını korumak hayvan sağlığı ve çevre ekolojisini korumaktan bağımsız düşünülemez ('Tek Sağlık / One Health' felsefesi).",
            "TARİHİ ÖRNEKLER: Madagaskar Kara Veba (2017, 209 ölü), Asya SARS (8000+ vaka), 2014 Batı Afrika Ebola, 2015 Zika ve her yıl dünyada 40'tan fazla kolera salgını meydana gelmektedir."
        ],
        "keyBullets": [
            {"title": "Türler Arası Sıçrama (Spillover)", "desc": "Yarasa, kemirgen ve vahşi memelilerdeki virüsler ara konakçılar aracılığıyla insan reseptörlerine uyum sağlayacak mutasyonları kazanır."},
            {"title": "Canlı Hayvan Pazarlarının Rolü", "desc": "Farklı türlerin dar kafeslerde stres altında bir arada tutulması viral rekombinasyon ve süper-enfeksiyon hızını katlar."},
            {"title": "Veteriner-Tıp Entegrasyonu", "desc": "Zoonotik salgınların önlenmesi beşeri hekimlik ile veteriner hekimliğin ortak sürveyans yürütmesini zorunlu kılar."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-5",
                "question": "İnsanlarda yeni ortaya çıkan enfeksiyon hastalıklarına yol açan patojenlerin yaklaşık yüzde kaçı hayvan kaynaklıdır (zoonozdur)?",
                "answer": "Yaklaşık %70'i (yüzde yetmişi) hayvan kaynaklıdır.",
                "hint": "%70 kuralı."
            },
            {
                "id": "fc-ep-6",
                "question": "Zoonotik patojenlerin insanlara kolayca bulaşarak büyük salgınlar başlatmasında en kritik iki çevresel/ticari risk faktörü nedir?",
                "answer": "1) Hayvanların tarımda aşırı yoğun kullanılması ve taşınması, 2) Canlı hayvan pazarlarında farklı türlerin ve insanların yakın temasta bulunması.",
                "hint": "Yoğun tarım/ticaret ve canlı hayvan pazarları."
            }
        ]
    },
    {
        "slideNumber": 4,
        "title": "Epidemiyolojik Dağılım Kalıpları: Endemi, Epidemi, Pandemi, Sporadi",
        "subtitle": "Toplumsal görülme paternleri, bazal sınır, beklenenden fazla artış ve coğrafi yayılım",
        "badge": "Epidemiyoloji Tanımları",
        "badgeColor": "amber",
        "target_ids": ["d3-k1-enf-001", "d3-k1-hs-007", "d3-k1-hs-008"],
        "keywords": ["epidemi", "endemi", "pandemi", "sporadik", "salgın tanımı"],
        "lead": "Bir enfeksiyon hastalığının bir toplumda gösterdiği zaman, yer ve kişi örüntüsü epidemiyolojinin temel sınıflandırmasını belirler; salgın kavramı mutlak bir sayı değil, beklenen düzeye göre anlamlı artışı ifade eder.",
        "spotPearls": [
            "EPİDEMİ (SALGIN) TANIMI: Bir hastalığın belirli bir bölgede veya toplulukta, BEKLENEN / ALIŞILMIŞ (bazal) SEYRİNDEN ANLAMLI ÖLÇÜDE DAHA FAZLA görülmesidir (Kurul 1 Çıkmış Soru!).",
            "ENDEMİ TANIMI: Bir hastalığın belirli bir coğrafi alanda veya toplumda SÜREKLİ VE ALIŞILMIŞ DÜZEYDE görülmesidir (örneğin sıtmanın Afrika'da endemik olması).",
            "PANDEMİ TANIMI: Bir epideminin ülke sınırlarını aşarak KITALAR ARASI çok geniş coğrafi alanlara ve küresel ölçeğe yayılmasıdır.",
            "SPORADİK TANIMI: Bir hastalığın belirli bir yerde düzenli bir örüntüden bağımsız olarak ARA SIRA VE TEK TÜK OLGULAR şeklinde gözlenmesidir (Kurul 1 Çıkmış Soru!)."
        ],
        "keyBullets": [
            {"title": "Göreli Artış Prensibi", "desc": "Toplumda hiç görülmeyen bir hastalık (örneğin Türkiye'de tek bir kuduz veya çocuk felci vakası) ortaya çıktığında tek vaka dahi epidemi kabul edilir."},
            {"title": "Endemik Düzey Eşiği", "desc": "Grip her kış mevsimsel endemik seyrederken yeni bir suşla vaka sayısının geçmiş yılların üst sınırını aşması epidemiyi tanımlar."},
            {"title": "Sürveyans Grafiği", "desc": "Endemik kanal eğrilerinin (geçmiş 5 yılın medyanı) üzerine çıkan vaka eğrisi salgın alarmı verir."}
        ],
        "table": {
            "title": "Görülme Sıklığı ve Coğrafi Dağılıma Göre Epidemiyolojik Tanımlar Matrisi",
            "headers": ["Kavram", "Tanım ve Karakteristik Patern", "Vaka Sıklığı & Eşik", "Klasik Tıp Örneği"],
            "rows": [
                ["Endemi", "Belli bir coğrafyada sürekli, düzenli ve alışılmış düzeyde bulunma", "Beklenen bazal seviyede sabit / mevsimsel", "Tropikal Afrika'da Sıtma, Karadeniz'de Guatr"],
                ["Epidemi (Salgın)", "Belli bir bölgede beklenenden anlamlı ölçüde daha fazla vaka görülmesi", "Alışılmış sınırın (endemik eşiğin) üzerine ani çıkış", "Madagaskar Veba Salgını, Şehir Su Şebekesi Kolera Salgını"],
                ["Pandemi", "Epideminin ülke sınırlarını aşarak kıtalararası küresel boyuta ulaşması", "Birden fazla kıtada geniş kitleleri etkileme", "1918 İspanyol Gribi, 2009 H1N1, 2019 SARS-CoV-2"],
                ["Sporadik", "Belli bir bölgede ara sıra, dağınık ve tek tük olgular halinde görülme", "Düzenli bir paterni ve bulaş odağı olmayan izole vakalar", "Kırsal alanda tek tük görülen Kırım-Kongo Kanamalı Ateşi veya Tetanoz"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ep-7",
                "question": "Bir hastalığın belirli bir bölgede ve dönemde 'beklenenden anlamlı ölçüde daha fazla görülmesi' hangi epidemiyolojik terimle tanımlanır?",
                "answer": "Epidemi (Salgın) olarak tanımlanır.",
                "hint": "Epidemi (Salgın)."
            },
            {
                "id": "fc-ep-8",
                "question": "Bir hastalığın bir bölgede 'ara sıra ve tek tük olgular şeklinde' görülmesine ne ad verilir?",
                "answer": "Sporadik (sporadi) adı verilir.",
                "hint": "Sporadik."
            }
        ]
    },
    {
        "slideNumber": 5,
        "title": "Epidemik Fazlar ve Salgın Eğrisinin 4 Aşaması",
        "subtitle": "Giriş/Ortaya çıkma, lokal yayılım, amplifikasyon ve bağışıklıkla sönme evresi",
        "badge": "Salgın Fazları",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["epidemik fazlar", "amplifikasyon", "lokal yayılım", "sönme aşaması"],
        "lead": "Her salgın belirli biyolojik ve toplumsal dinamiklere sahip dört ardışık epidemik faz üzerinden ilerler; müdahalenin başarısı hangi fazda eyleme geçildiğine doğrudan bağlıdır.",
        "spotPearls": [
            "1. AŞAMA - GİRİŞ VEYA ORTAYA ÇIKMA (EMERGENCE): Patojenin bir topluluğa ilk girişi ya da hayvan rezervuarından insana sıçramasıdır.",
            "2. AŞAMA - LOKAL YAYILIM (LOCALIZED TRANSMISSION): Patojenin indeks vakanın yakın çevresinde (aile, işyeri, mahalle) insandan insana bulaşmaya başlamasıdır.",
            "3. AŞAMA - AMPLİFİKASYON (BÜYÜME VE KATLANMA): Salgının topluma yayılarak geometrik hızla katlanması, sağlık tesislerine aşırı hasta akını ve kitlesel morbidite evresidir.",
            "4. AŞAMA - SÖNME VE GERİLEME (BURN-OUT / REDUCTION): Toplumda patojene karşı bağışıklığın yayılması (enfeksiyonu geçirme veya aşılanma) ve kontrol önlemleriyle salgının sönmesidir."
        ],
        "keyBullets": [
            {"title": "Kritik Müdahale Penceresi", "desc": "Salgını kontrol etmenin en ucuz ve en etkili olduğu evre 1. ve 2. aşamadır; 3. aşamada ancak hasar azaltma (mitigasyon) yapılabilir."},
            {"title": "Amplifikasyonun Motoru", "desc": "Süper yayıcı bireyler, kapalı kalabalık ortamlar ve gecikmiş izolasyon salgının 3. aşamaya fırlamasına yol açar."},
            {"title": "Sürü Bağışıklığı Eşiği (Herd Immunity)", "desc": "Toplumda bağışık birey oranı patojenin R0 (temel üreme katsayısı) değerine ulaştığında salgın doğal olarak 4. aşamaya girer."}
        ],
        "table": {
            "title": "Salgın Eğrisinin 4 Epidemik Fazı ve Karakteristik Özellikleri",
            "headers": ["Faz No & Adı", "Temel Biyolojik Olay", "Toplumsal Görünüm", "Öncelikli Halk Sağlığı Eylemi"],
            "rows": [
                ["1. Faz: Giriş / Ortaya Çıkma", "Patojenin topluluğa girişi, zoonotik sıçrama", "Tekil indeks vaka, henüz yayılım yok", "Erken tanı, sınır sürveyansı, temaslı izolasyonu"],
                ["2. Faz: Lokal Yayılım", "İnsandan insana ilk bulaş halkaları", "Küçük aile veya kurum içi vaka kümeleri", "Filyasyon, temaslı takibi, odak dezenfeksiyonu"],
                ["3. Faz: Amplifikasyon", "Geometrik vaka artışı, kontrolün zorlaşması", "Hastanelere akın, yoğun bakım yetersizliği", "Kitlesel kısıtlamalar, triyaj, mitigasyon"],
                ["4. Faz: Sönme / Azalma", "Duyarlı birey tükenmesi, bağışıklık gelişimi", "Yeni vaka sayısında kalıcı plato ve düşüş", "Aşılama tamamlama, rehabilitasyon, ders çıkarma"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ep-9",
                "question": "Salgınların seyrindeki 4 epidemik aşama sırasıyla hangileridir?",
                "answer": "1) Giriş ya da ortaya çıkma, 2) Lokal yayılım, 3) Amplifikasyon (katlanarak büyüme), 4) Bağışıklığın yayılmasıyla sönme.",
                "hint": "Giriş -> Lokal yayılım -> Amplifikasyon -> Sönme."
            },
            {
                "id": "fc-ep-10",
                "question": "Salgının 4. ve son aşamasında sönmesini sağlayan temel epidemiyolojik mekanizma nedir?",
                "answer": "Patojene karşı toplumda bağışıklığın (enfeksiyon geçirme veya aşılama yoluyla) yayılması ve duyarlı havuzun tükenmesidir.",
                "hint": "Bağışıklığın yayılması."
            }
        ]
    },
    {
        "slideNumber": 6,
        "title": "Salgını Bekleme, Erken Teşhis ve Klinisyenin Rolü",
        "subtitle": "Öngörü analizi, yayılma sürücüleri ve Ebola'nın Batı Afrika'da 2 ay fark edilememesi dersi",
        "badge": "Erken Teşhis & Sürveyans",
        "badgeColor": "cyan",
        "target_ids": [],
        "keywords": ["erken teşhis", "klinisyenin rolü", "ebola batı afrika", "öngörü"],
        "lead": "Salgınların ne zaman patlayacağı tam bir kesinlikle öngörülemez; ancak risklerin bilimsel olarak tahmin edilmesi ve klinik sürveyansın uyanık tutulması yıkımı engellemenin tek yoludur.",
        "spotPearls": [
            "ÖNGÖRÜ VE RİSK TAHMİNİ: Ortaya çıkacak en olası patojenlerin önceden tahmin edilmesi ve yayılmayı kolaylaştıracak 'sürücülerin' (iklim, göç, hijyen) belirlenmesini kapsar.",
            "TANI İLK OLARAK KLİNİSYENLE BAŞLAR: Salgın alarmını laboratuvar değil, poliklinikte anormal bir vaka kümelenmesini fark eden dikkatli hekim çalar!",
            "EBOLA DERSİ (BATI AFRİKA 2014): Ebola virüsü Batı Afrika'da tam İKİ AY BOYUNCA TANI ALMAMIŞTIR; bu klinik gecikme virüsün 3 ülkeye yayılmasına ve 11.000'den fazla insanın ölümüne neden olmuştur.",
            "SAĞLIK SİSTEMİNE ERİŞEBİLİRLİK: Halk sağlık merkezlerine kolayca ulaşamazsa veya korku yüzünden başvurmaktan çekinirse salgın yer altında kontrolsüzce büyür."
        ],
        "keyBullets": [
            {"title": "Korku ve Hatalı Kararlar", "desc": "Salgınlar bireylerde ve yöneticilerde yoğun korkuya yol açar; korku ise gerçeklerin gizlenmesine ve hatalı kararlara neden olur."},
            {"title": "Hızlı Araştırma Zorunluluğu", "desc": "Yeni ortaya çıkan etkenler hakkında literatürde çok az bilgi bulunur; sahada anlık epidemiyolojik araştırmalar şarttır."},
            {"title": "Klinisyenin İhbar Yükümlülüğü", "desc": "Bulaşıcı hastalık şüphesi taşıyan her hekim vakayı 24 saat içinde Halk Sağlığı Birimlerine (İl Sağlık Müdürlüğü) bildirmek zorundadır."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-11",
                "question": "Salgınların erken teşhisinde ilk alarmın başladığı yer neresidir ve 2014 Batı Afrika Ebola salgınında bu alandaki trajik gecikme ne kadardır?",
                "answer": "Tanı ilk olarak klinisyenle başlar; 2014 Ebola salgınında klinisyenler tarafından tanı konması tam 2 ay gecikmiştir.",
                "hint": "Klinisyenle başlar, Ebola'da 2 ay tanı almadı."
            },
            {
                "id": "fc-ep-12",
                "question": "Salgın durumlarında kriz yönetiminde yöneticilerin en çok kaçınması gereken psikososyal faktör nedir?",
                "answer": "Korku ve paniğin yönetilememesidir; çünkü korku hatalı ve yıkıcı kararların alınmasına yol açar.",
                "hint": "Korku hatalı kararlara neden olur."
            }
        ]
    },
    {
        "slideNumber": 7,
        "title": "Sınırlama (Containment), Mitigasyon ve Müdahale Zamanlaması",
        "subtitle": "İlk vaka ilkesi, patojen tam bilinmese bile müdahale, hasar azaltma (mitigasyon)",
        "badge": "Müdahale Stratejisi",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["sınırlama", "mitigasyon", "ilk vaka", "containment"],
        "lead": "Salgın yönetiminde zamanlama her şeydir; altın kural, sınırlama tedbirlerinin patojenin adı tam olarak konulmasa dahi ilk şüpheli vaka görüldüğü anda başlatılmasıdır.",
        "spotPearls": [
            "İLK VAKA KURALI: Sınırlama (containment) İLK VAKA TEŞHİS EDİLDİĞİ ANDA BAŞLAMALIDIR; patojen henüz laboratuvarda tam izole edilmemiş olsa dahi izolasyon derhal devreye sokulmalıdır!",
            "SINIRLAMA (CONTAINMENT): Patojenin yayılma odağını karantinaya alarak çevreye saçılmasını engelleme çabasıdır.",
            "MİTİGASYON (ETKİ AZALTMA): Patojen sınırlamayı aşıp geniş topluluklara veya pandemiye dönüştüyse artık amaç virüsü sıfırlamak değil; morbidite, mortalite, ekonomik ve sosyal yıkımı en aza indirmektir.",
            "SAĞLIK SİSTEMİ KAPASİTESİ: Mitigasyon eğriyi basıklaştırarak (flatten the curve) yoğun bakım ve hastane yataklarının kilitlenmesini önler."
        ],
        "keyBullets": [
            {"title": "Beklemenin Maliyeti", "desc": "Laboratuvar teyidini beklemek için kaybedilen 48 saat, vaka sayısının geometrik olarak onlarca katına çıkmasına yol açar."},
            {"title": "Çok Sektörlü Hasar", "desc": "Mitigasyon yalnızca tıbbi ölümleri değil; okulların kapanması, lojistik krizler ve işgücü kaybının getirdiği ekonomik felaketi de yönetmektir."},
            {"title": "Esnek Eylem Planları", "desc": "Salgının boyutu değiştikçe filyasyon stratejisinden toplumsal mesafe ve triyaj protokollerine hızlı geçiş yapılmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-13",
                "question": "Salgın yönetiminde sınırlama (containment) önlemleri ne zaman başlatılmalıdır?",
                "answer": "Patojen henüz tam belirlenmemiş olsa dahi İLK VAKA TEŞHİS EDİLDİĞİ ANDA derhal başlatılmalıdır.",
                "hint": "İlk vaka teşhis edildiği anda."
            },
            {
                "id": "fc-ep-14",
                "question": "Sınırlama aşılarak hastalık pandemi düzeyine ulaştığında uygulanan 'Mitigasyon' (etki azaltma) stratejisinin temel hedefi nedir?",
                "answer": "Hastalığın yol açacağı mortalite, morbidite, ekonomik ve sosyal zararları en aza indirmek ve sağlık sisteminin çökmesini engellemektir.",
                "hint": "Zararları en aza indirmek."
            }
        ]
    },
    {
        "slideNumber": 8,
        "title": "Hastalık Mücadele Düzeyleri: Kontrol, Eliminasyon ve Eradikasyon",
        "subtitle": "Kavramsal hiyerarşi, sürveyansın devamı zorunluluğu ve dünya çapında kalıcı sıfırlama",
        "badge": "Mücadele Düzeyleri",
        "badgeColor": "purple",
        "target_ids": ["d3-k1-hs-016", "d3-k1-hs-017"],
        "keywords": ["eradikasyon", "eliminasyon", "kontrol", "çiçek hastalığı"],
        "lead": "Bulaşıcı hastalıklarla mücadelede ulaşılabilecek hedefler hiyerarşik olarak kontrol, eliminasyon ve eradikasyon olarak üçe ayrılır; bu kavramlar sınavların en klasik sorularını oluşturur.",
        "spotPearls": [
            "KONTROL: Bir hastalığın sıklığının belirli bir coğrafi bölgede kabul edilebilir düzeye indirilmesidir.",
            "ELİMİNASYON (BÖLGESEL SIFIRLAMA): Hastalığın belirli bir coğrafi alanda (örneğin bir ülkede) artık bir halk sağlığı sorunu olmaktan çıkması ve YERLİ (OTOKTON) VAKANIN GÖRÜLMEMESİDİR. DİKKAT: Eliminasyonda müdahale, sürveyans ve aşı önlemleri kesintisiz DEVAM ETMELİDİR! (Kurul 1 Çıkmış Soru!).",
            "ERADİKASYON (KÜRESEL VE KALICI YOK ETME): Patojenin DÜNYA ÇAPINDAKİ görülme sıklığının KALICI OLARAK SIFIRLANMASIDIR; artık dünyada hiçbir rezervuarı kalmaz, aşı ve müdahaleler sonlandırılabilir (Kurul 1 Çıkmış Soru!).",
            "İNSANDA TEK ERADİKE HASTALIK: İnsanlık tarihinde bugüne kadar tamamen eradike edilen TEK insan enfeksiyonu ÇİÇEK HASTALIĞIDIR (Smallpox - 1980 DSÖ ilanı); hayvanlarda ise Sığır Vebası (Rinderpest) eradike edilmiştir."
        ],
        "keyBullets": [
            {"title": "Eliminasyon Tuzağı", "desc": "Eliminasyona ulaşıldığında aşılamayı bırakırsanız dışarıdan gelen (importe) tek bir vaka duyarlı havuzda yeni bir salgın başlatır (örn: Kızamık)."},
            {"title": "Eradikasyon Kriterleri", "desc": "Bir hastalığın eradike edilebilmesi için hayvan rezervuarının olmaması, etkili bir aşısının bulunması ve kolay teşhis edilmesi şarttır."},
            {"title": "Polio (Çocuk Felci) Durumu", "desc": "Polio dünyada eliminasyon aşamasını geçmiş, eradikasyonun eşiğine gelmiş ancak henüz son vakalar sıfırlanamamıştır."}
        ],
        "table": {
            "title": "Halk Sağlığında Bulaşıcı Hastalık Mücadele Düzeyleri Karşılaştırma Matrisi",
            "headers": ["Özellik", "Kontrol", "Eliminasyon", "Eradikasyon"],
            "rows": [
                ["Hedef Alan", "Belirli bir bölge / ülke", "Belirli bir bölge / ülke / kıta", "TÜM DÜNYA (Küresel)"],
                ["Vaka Durumu", "Kabul edilebilir hedef sayıya indirilmiş", "Yerli (otokton) vaka sayısı SIFIR", "Dünya genelinde vaka sayısı KESİN SIFIR"],
                ["Müdahale Devamı", "Kesintisiz devam eder", "Müdahale ve aşı ZORUNLU DEVAM EDER", "Aşı ve kontrol önlemleri SONLANDIRILIR"],
                ["Sürveyans İhtiyacı", "Aktif sürveyans", "Aktif ve alarmda sürveyans", "Sadece laboratuvar arşiv güvenliği"],
                ["Prototip Örnek", "Mevsimsel influenza kontrolü", "Türkiye'de Sıtma ve Polio eliminasyonu", "Çiçek Hastalığı (Smallpox, 1980)"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ep-15",
                "question": "Bir hastalığın etkeni dünyadan tamamen silinmemişken belirli bir ülkede yerli (otokton) vakanın artık görülmemesine ne ad verilir ve aşılamaya devam edilir mi?",
                "answer": "Eliminasyon adı verilir; eliminasyon durumunda aşı ve sürveyans önlemleri kesintisiz olarak DEVAM ETMELİDİR.",
                "hint": "Eliminasyon; aşı ve önlemler devam eder."
            },
            {
                "id": "fc-ep-16",
                "question": "Bir patojenin dünya çapında kalıcı olarak tamamen yok edilmesine ne ad verilir ve insanda bugüne kadar eradike edilen tek hastalık hangisidir?",
                "answer": "Eradikasyon adı verilir; insanlık tarihinde eradike edilen tek hastalık Çiçek Hastalığıdır (Smallpox).",
                "hint": "Eradikasyon ve Çiçek Hastalığı."
            }
        ]
    },
    {
        "slideNumber": 9,
        "title": "Salgına Yanıt Sisteminin 4 Temel Ayağı",
        "subtitle": "Kurumlar arası koordinasyon, sağlık enformasyonu, risk iletişimi ve eksiksiz müdahaleler",
        "badge": "Sistemik Yönetim",
        "badgeColor": "blue",
        "target_ids": [],
        "keywords": ["salgın yanıtı", "dört ayak", "sağlık sistemi", "koordinasyon"],
        "lead": "Kapsamlı bir salgın yanıtı son derece karmaşık ve çok aktörlü bir süreçtir; Dünya Sağlık Örgütü ve amfi müfredatı bu yanıtı kusursuz işlemesi gereken dört temel sistemik özellikle tanımlar.",
        "spotPearls": [
            "SALGIN YANITININ 4 DİREĞİ: 1) KURUMLAR ARASI KOORDİNASYON, 2) TAM VE EKSİKSİZ SAĞLIK ENFORMASYONU, 3) RİSKİ TAM VE DOĞRU BİR ŞEKİLDE AKTARMA (Risk İletişimi), 4) TAM VE EKSİKSİZ SAĞLIK MÜDAHALELERİ.",
            "İSTİSNAİ OLAY DOĞASI: Salgınlar olağan sağlık kapasitesinin katbekat üzerinde insan ve finansman kaynağı gerektirir; bu nedenle diğer bakanlıklar, belediyeler ve sivil toplumla ortaklaşa yürütülmelidir.",
            "ENFORMASYONSUZ YÖNETİLEMEZ: Veriye dayanmayan hiçbir kriz yönetilemez; sahadan gelen anlık veriler olmadan doğru kararlar alınamaz.",
            "GÜVEN YOKSA MÜDAHALE ÇÖKER: Risk iletişimi başarısızsa halk aşıyı reddeder, karantinayı deler ve en mükemmel tıbbi müdahale dahi havada kalır."
        ],
        "keyBullets": [
            {"title": "Sektörler Arası İşbirliği", "desc": "İçişleri (karantina/güvenlik), Ulaştırma (seyahat kısıtlamaları) ve Tarım Bakanlığı (zoonoz takibi) Sağlık Bakanlığı ile tek çatı altında çalışmalıdır."},
            {"title": "Bütüncül Müdahale Paketi", "desc": "Yalnızca hastane tedavisi yetmez; halk eğitimi, su-besin hijyeni, atık yönetimi ve aşılama aynı anda uygulanmalıdır."},
            {"title": "Hiyerarşik Komuta", "desc": "Kriz anlarında çift başlılığı önlemek için tek bir liderlik ve sözcülük mekanizması kurulmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-17",
                "question": "Dr. Erkay Nacar amfi ders notuna göre kapsamlı bir salgın müdahale sisteminde bulunması gereken 4 temel özellik nedir?",
                "answer": "1) Kurumlar arası koordinasyon, 2) Tam ve eksiksiz sağlık enformasyonu, 3) Riski tam ve doğru aktarma, 4) Tam ve eksiksiz sağlık müdahaleleri.",
                "hint": "Koordinasyon, Enformasyon, Risk İletişimi, Sağlık Müdahaleleri."
            },
            {
                "id": "fc-ep-18",
                "question": "Salgın yanıtında sadece sağlık sektörünün değil diğer kamu kurumlarının da dahil edilmesini zorunlu kılan temel gerçek nedir?",
                "answer": "Salgının olağan sağlık bütçesini ve işgücünü çok aşan istisnai bir kriz olması ve lojistik, güvenlik, ulaşım gibi alanlara doğrudan dayanmasıdır.",
                "hint": "İstisnai kaynak ihtiyacı ve çok sektörlü yapı."
            }
        ]
    },
    {
        "slideNumber": 10,
        "title": "Kurumlar Arası Koordinasyon ve Acil Operasyon Merkezleri (EOC)",
        "subtitle": "Fiziksel kriz merkezi, ortak eylem planı, irtibat matrisi ve paydaş yönetimi",
        "badge": "Koordinasyon & EOC",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["acil operasyon merkezi", "eoc", "kurumlar arası koordinasyon", "eylem planı"],
        "lead": "Etkili bir koordinasyon soyut bir temenni değil; fiziksel altyapısı, protokolleri ve iletişim ağları önceden hazırlanmış operasyonel bir mekanizmadır.",
        "spotPearls": [
            "ACİL OPERASYON MERKEZİ (AOM / EOC): Salgını yönetmek için özel bir fiziksel alana (Acil Operasyon Merkezi) ihtiyaç vardır; tüm veriler ve kararlar burada toplanır.",
            "ORTAK EYLEM PLANI: Durum geliştikçe güncellenen, gereken müdahaleleri ve paydaşların rol/sorumluluk dağılımını kesin çizgilerle tanımlayan dinamik belgedir.",
            "İLETİŞİM VE İZLEME ARAÇLARI: İrtibat listesi, toplantı izleme sistemi, coğrafi bilgi sistemi (haritalar), gösterge panelleri (dashboard) ve 7/24 açık iletişim dizini şarttır.",
            "ROL ÇATIŞMALARINI ÖNLEME: Hangi kurumun lojistik sağlayacağı, hangisinin güvenliği koruyacağı önceden belirlenmezse salgın sahada kaos yaratır."
        ],
        "keyBullets": [
            {"title": "Gösterge Tabloları (Dashboards)", "desc": "Yatak doluluk oranları, solunum cihazı stokları ve aşı envanteri anlık dijital ekranlarda izlenmelidir."},
            {"title": "Periyodik Durum Raporları (SitRep)", "desc": "Günde en az bir kez yayınlanan durum raporları sahadaki tüm ekiplerin aynı bilgi düzeyinde kalmasını sağlar."},
            {"title": "Uluslararası Entegrasyon", "desc": "DSÖ ve uluslararası halk sağlığı ağları ile anlık veri paylaşımı küresel izolasyon önlemlerini senkronize eder."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-19",
                "question": "Salgınlarda kurumlar arası etkili bir koordinasyon yürütebilmek için tahsis edilmesi gereken özel fiziksel alanın adı nedir?",
                "answer": "Acil Operasyon Merkezi (AOM / Emergency Operations Center - EOC).",
                "hint": "Acil Operasyon Merkezi (EOC)."
            },
            {
                "id": "fc-ep-20",
                "question": "Acil Operasyon Merkezinde paydaşların görev dağılımını ve operasyon adımlarını belirleyen dinamik belgenin adı nedir?",
                "answer": "Ortak Eylem Planı (Action Plan).",
                "hint": "Ortak Eylem Planı."
            }
        ]
    },
    {
        "slideNumber": 11,
        "title": "Sağlık Enformasyonu ve Sürveyans Sistemi: Kişi, Zaman ve Yer",
        "subtitle": "Epidemiyolojik üçlü (Kişi, Yer, Zaman), vaka tanımları, süreç ve çıktı göstergeleri",
        "badge": "Sürveyans & Enformasyon",
        "badgeColor": "indigo",
        "target_ids": [],
        "keywords": ["sürveyans", "kişi yer zaman", "sağlık enformasyonu", "çıktı göstergeleri"],
        "lead": "Sürveyans; sağlığı etkileyen olayların sistematik olarak toplanması, analiz edilmesi, yorumlanması ve gerekli müdahaleleri yapacak birimlere kesintisiz aktarılmasıdır.",
        "spotPearls": [
            "İKİ ÖZEL BİLGİ TÜRÜ: Salgın yönetiminde iki hayati veri kaynağı vardır: 1) HASTALIĞIN SÜRVEYANSI (vaka ve ölümler), 2) MÜDAHALE BİLGİLERİ (yapılan eylemlerin kapsamı ve etkisi; süreç ve çıktı göstergeleri).",
            "SÜRVEYANSIN 3 KLASİK BİLEŞENİ: KİŞİ (Kimler hastalanıyor? Yaş, cinsiyet, meslek), ZAMAN (Ne zaman başladı? Salgın eğrisi), YER (Nerede kümelendi? Coğrafi harita).",
            "STANDART VAKA TANIMLARI: Sahada karmaşayı önlemek için 'Olası Vaka', 'Şüpheli Vaka' ve 'Kesin Vaka' kriterleri netleştirilmelidir.",
            "MÜDAHALENİN ETKİSİNİ ÖLÇME: Alınan kapanma veya aşılama kararlarının işe yarayıp yaramadığı ancak sürveyans eğrisinin yönüyle anlaşılır."
        ],
        "keyBullets": [
            {"title": "Filyasyon Ekiplerinin Rolü", "desc": "Sürveyansın saha ayağını temaslı taraması (filyasyon) yapan mobil sağlık çalışanları oluşturur."},
            {"title": "Gecikme Süreleri (Lag Time)", "desc": "Semptom başlangıcı ile bildirim arasındaki gün farkının azaltılması sürveyans kalitesinin en hassas metriğidir."},
            {"title": "Süreç vs Çıktı Göstergesi", "desc": "Dağıtılan maske sayısı süreç göstergesi iken; yeni vaka insidansındaki %40 düşüş çıktı göstergesidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-21",
                "question": "Hastalık sürveyansı vaka ve ölümler hakkında hangi üç temel epidemiyolojik değişken üzerinden bilgi sağlar?",
                "answer": "Kişi (kim?), Zaman (ne zaman?) ve Yer (nerede?) değişkenleri üzerinden bilgi sağlar.",
                "hint": "Kişi, Zaman ve Yer."
            },
            {
                "id": "fc-ep-22",
                "question": "Salgın yönetiminde toplanan sağlık enformasyonunun iki temel bilgi türü nedir?",
                "answer": "1) Hastalığın sürveyans bilgisi (vaka/ölüm sayıları), 2) Müdahalelerin kapsam ve etkisini gösteren müdahale bilgisi (süreç ve çıktı göstergeleri).",
                "hint": "Sürveyans bilgisi ve Müdahale bilgisi."
            }
        ]
    },
    {
        "slideNumber": 12,
        "title": "Risk İletişimi ve İnfodemi ile Mücadele: Üç Altın Kural",
        "subtitle": "İnfodemi kavramı, panik yönetimi, dedikoduları engelleme, konuşma ve dinleme",
        "badge": "Risk İletişimi & İnfodemi",
        "badgeColor": "amber",
        "target_ids": [],
        "keywords": ["infodemi", "risk iletişimi", "dedikodu", "panik yönetimi"],
        "lead": "Salgın dönemlerinde yalnızca mikrobik patojen yayılmaz; aynı zamanda büyük paniklere ve can kayıplarına yol açan yalan, manipülatif ve kontrolsüz bir bilgi seli (İnfodemi) yayılır.",
        "spotPearls": [
            "İNFODEMİ TANIMI: Bir salgın sırasında doğru bilgilerin yanında aşırı miktarda yanlış, gereksiz ve paniğe yol açan abartılı bilginin kontrolsüzce yayılmasıdır.",
            "İNFODEMİYLE MÜCADELENİN 3 KURALI: 1) KONUŞMA (şeffaf, doğru ve düzenli bilgilendirme yap), 2) DİNLEME (halkın kaygılarını, algılarını ve şüphelerini duy), 3) DEDİKODULARI ENGELLE (asılsız iddialara hızla bilimsel yanıt ver!).",
            "BİLGİ BOŞLUĞU FELAKETTİR: Resmi otoriteler sessiz kalır veya bilgi gizlerse ortaya çıkan bilgi boşluğu komplo teorileri ve hurafelerle dolar.",
            "AŞI REDDİNİN MOTORU: İnfodemi özellikle aşı tereddüdünün ve tıbbi tedaviye güvensizliğin bir numaralı tetikleyicisidir."
        ],
        "keyBullets": [
            {"title": "Sosyal Medya Yangınları", "desc": "Dijital çağda sahte haberler bilimsel makalelerden 6 kat daha hızlı dolaşıma girer."},
            {"title": "Tek ve Güvenilir Sözcü", "desc": "Çelişkili açıklamaları önlemek için basın karşısına her gün aynı bilimsel sözcü veya heyet çıkmalıdır."},
            {"title": "Empatik Dil", "desc": "Halkı suçlayan veya azarlayan kibirli dil direnci artırır; anlayışlı ve rehberlik edici bir üslup benimsenmelidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-23",
                "question": "Salgınlarda patojenle birlikte yanlış, abartılı ve paniğe yol açan asılsız bilgilerin kontrolsüz yayılmasına ne ad verilir?",
                "answer": "İnfodemi adı verilir.",
                "hint": "İnfodemi."
            },
            {
                "id": "fc-ep-24",
                "question": "Dr. Erkay Nacar amfi sunumuna göre infodemi ve yanlış bilgileri önlemek için hayati önem taşıyan 3 eylem nedir?",
                "answer": "1) Konuşma, 2) Dinleme, 3) Dedikoduları engelleme.",
                "hint": "Konuşma, Dinleme, Dedikoduları engelleme."
            }
        ]
    },
    {
        "slideNumber": 13,
        "title": "Toplumsal Boyut: Sosyokültürel Faktörler ve Toplumun Katılımı",
        "subtitle": "Toplumun yekpare olmaması, risk algısı, inançlar ve eğitimli toplum gücü",
        "badge": "Toplumsal Katılım",
        "badgeColor": "cyan",
        "target_ids": [],
        "keywords": ["toplum katılımı", "sosyokültürel", "risk algısı", "toplumsal baz"],
        "lead": "Hiçbir salgın halkın aktif katılımı ve rızası olmadan yalnızca hastanelerde kazanılamaz; toplum yekpare bir blok değildir ve müdahaleler bu çeşitliliğe uyarlanmalıdır.",
        "spotPearls": [
            "İNSAN TOPLULUKLARI YEKPARE DEĞİLDİR: Risk algısı sosyoekonomik düzeye, dine, kültürel inançlara, etnik kökene ve dile göre taban tabana zıtlık gösterebilir.",
            "EĞİTİMLİ TOPLUMUN GÜCÜ: İyi eğitilmiş ve hazırlanmış bir toplum salgını uzman desteği gelmeden kendisi bile erkenden fark edebilir ve önlem alabilir.",
            "MÜDAHALENİN ETKİSİ TOPLUMLA ARTAR: Karantina ve izolasyon ancak halkın kendi rızasıyla kurallara uyması durumunda sahada başarı sağlar.",
            "KURTULANLARIN ENTEGRASYONU: Hastalıktan iyileşen bireyler (survivor) damgalanmamalı (stigmatizasyon önlenmeli), aksine plazma bağışı ve saha dayanışmasında öncü yapılmalıdır."
        ],
        "keyBullets": [
            {"title": "Kültürel Cenaze ve Dini Ritüeller", "desc": "Örneğin Ebola'da ölü bedenlerin yıkanması gibi cenaze ritüelleri yasaklanmak yerine güvenli dini alternatiflerle dönüştürülmelidir."},
            {"title": "Kırılgan Grupların Korunması", "desc": "Mülteciler, evsizler ve yoksul kesimler sağlık mesajlarına ve temiz suya en zor ulaşan gruplardır."},
            {"title": "Yerel Kanaat Önderleri", "desc": "Muhtarlar, din görevlileri ve öğretmenler sağlık mesajlarının benimsenmesinde doktordan daha etkili olabilir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-25",
                "question": "Salgın müdahalesinde 'Toplumsal bazda düşünün' ilkesinin temel gerekçesi nedir?",
                "answer": "İnsan topluluklarının yekpare olmaması; risk algısının din, kültür, ekonomik gelişmişlik ve dile göre farklılık göstermesidir.",
                "hint": "Toplumun yekpare olmaması ve sosyokültürel farklılıklar."
            },
            {
                "id": "fc-ep-26",
                "question": "Salgın dönemlerinde hastalıktan iyileşen bireylerle (survivors) ilgili halk sağlığı yaklaşımı nasıl olmalıdır?",
                "answer": "Damgalanmaları (stigmatizasyon) engellenmeli ve topluma güvenle kaynaştırılarak mücadelede destekçi haline getirilmelidirler.",
                "hint": "Damgalamayı önleme ve topluma kaynaştırma."
            }
        ]
    },
    {
        "slideNumber": 14,
        "title": "21. Yüzyılda İletişim Paradigması: Güven İnşası ve Dinleme Sanatı",
        "subtitle": "Tek taraflı buyurgan dilin iflası, uzman güven erozyonu ve iki yönlü iletişim",
        "badge": "İletişim Paradigması",
        "badgeColor": "rose",
        "target_ids": [],
        "keywords": ["iletişim problemleri", "güven inşası", "buyurgan dil", "iki yönlü iletişim"],
        "lead": "21. yüzyılda tıp otoritelerinin halka yukarıdan bakan buyurgan üslubu iflas etmiştir; sağlık iletişimi insanları emirlerle yönetmek değil, onları dinleyerek güven inşa etmektir.",
        "spotPearls": [
            "BUYURGAN DİLİN REDDİ: 21. yüzyılda insanlar artık tek taraflı, otoriter ve buyurgan dili kesinlikle benimsememektedir.",
            "UZMAN GÖRÜŞÜNE GÜVEN AZALIYOR: Halk sağlık bilgilerini konvansiyonel hekimlerden ziyade internet ve sosyal medyadan almaya başlamıştır; mesafeler kısalmış, infial hızı artmıştır.",
            "ÖNCE GÜVEN TESİSİ: Uzman görüşünüzü aktarabilmek için önce karşı tarafla sarsılmaz bir güven köprüsü kurmanız gerekir.",
            "DİNLEMEK EN AZ ANLATMAK KADAR ÖNEMLİDİR: İnsanların inançlarını, kaygılarını ve algılarını dinlemek ve anlamak; onlara tıbbi gerçekleri ve tavsiyeleri vermek kadar hayati bir halk sağlığı görevidir."
        ],
        "keyBullets": [
            {"title": "Karşılıklı Diyalog", "desc": "Halkın sorularını yanıtlamayan ve korkularını hafife alan yaklaşımlar kitleleri aşı karşıtlığına iter."},
            {"title": "Şeffaf Belirsizlik Yönetimi", "desc": "'Henüz her şeyi bilmiyoruz ama araştırıyoruz' dürüstlüğü, sahte kesinlik iddialarından çok daha fazla güven üretir."},
            {"title": "Geri Bildirim Döngüleri", "desc": "Sahadaki anket ve sosyal medya dinlemeleri halkın hangi konularda tereddüt yaşadığını anında tespit etmelidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-27",
                "question": "21. yüzyıl salgın yönetiminde sağlık otoritelerinin 'tek taraflı buyurgan dil' kullanmasının halk üzerindeki olumsuz etkisi nedir?",
                "answer": "Halk tarafından benimsenmez, uzmanlara olan güven erozyonunu artırır ve bireyleri sosyal medyadaki alternatif yanlış bilgilere yönlendirir.",
                "hint": "Güven kaybı ve buyurgan dilin reddi."
            },
            {
                "id": "fc-ep-28",
                "question": "Tıbbi tavsiyelerin halka kabul ettirilmesinde en az gerçekleri anlatmak kadar kritik olan iletişim basamağı nedir?",
                "answer": "İnsanların inançlarını, korkularını, kaygılarını ve algılarını sabırla dinlemek ve anlamaktır.",
                "hint": "Dinlemek ve anlamak."
            }
        ]
    },
    {
        "slideNumber": 15,
        "title": "Tedavi, Aşılar ve Destekleyici Bakımın Hayat Kurtaran Gücü",
        "subtitle": "Aşı devrimi, DBT aşısı (%86 koruma) ve 2014 Ebola'da destek tedavisiyle mortalitenin %75'ten %33'e düşüşü",
        "badge": "Tedavi & Aşı Devrimi",
        "badgeColor": "emerald",
        "target_ids": [],
        "keywords": ["aşı devrimi", "dbt aşısı", "ebola destek tedavisi", "monoklonal antikor"],
        "lead": "Modern tıp aşılar, antibiyotikler ve antivirallerle devrim yaratmıştır; ancak en pahalı ilaçların yokluğunda dahi kaliteli klinik destekleyici bakım binlerce hayatı kurtarabilir.",
        "spotPearls": [
            "AŞILARIN KÜRESEL GÜCÜ: DSÖ verilerine göre bebeklerde uygulanan kombine difteri-tetanoz-boğmaca (DBT) aşısı küresel anlamda çocukların %86'SINI korumaktadır.",
            "İLAÇ DEVRİMİ: 20. yüzyıl sonuna doğru HIV tedavisinde çığır açan antiretroviraller ve günümüzde monoklonal antikorlar salgınların kontrolünde dev adımlardır.",
            "DESTEKLEYİCİ BAKIMIN MUCİZESİ (EBOLA DERSİ): Belirli bir hastalık için spesifik ilaç bulunmadığında dahi iyi klinik önleyici ve destekleyici bakım hayat kurtarır!",
            "EBOLA MORTALİTE DÜŞÜŞÜ (%75'TEN %33'E): 2014 Batı Afrika Ebola salgınında spesifik ilaç olmadan, yalnızca hastalara daha iyi hidrasyon ve destekleyici bakım sağlanarak ölüm oranı %75'TEN %33'E İNDİRİLMİŞTİR!"
        ],
        "keyBullets": [
            {"title": "Kalifiye Personel Zorunluluğu", "desc": "İlaç ve aşılar ancak onları özveriyle ve doğru protokolle uygulayacak eğitimli personel varsa işe yarar."},
            {"title": "Sıvı-Elektrolit Dengesinin Gücü", "desc": "Kolera ve viral kanamalı ateşlerde ölümün birincil nedeni patojen değil ağır dehidratasyon ve şoktur; oral rehidrasyon sıvısı (ORS) mucizedir."},
            {"title": "Monoklonal Antikor Kısıtı", "desc": "Monoklonal antikorlar çok etkili olmakla birlikte maliyetlerinin aşırı yüksekliği kitlesel salgınlarda kullanımını sınırlar."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-29",
                "question": "DSÖ verilerine göre kombine difteri-tetanoz-boğmaca (DBT) aşısı dünya genelindeki çocukların yaklaşık yüzde kaçını korumaktadır?",
                "answer": "Yaklaşık %86'sını (yüzde seksen altısını) korumaktadır.",
                "hint": "%86 koruma."
            },
            {
                "id": "fc-ep-30",
                "question": "2014 Batı Afrika Ebola salgınında spesifik antiviral ilaç bulunmamasına rağmen ölüm oranı yalnızca iyi klinik destekleyici bakımla yüzde kaçtan kaça düşürülmüştür?",
                "answer": "%75'ten %33'e kadar dramatik şekilde düşürülmüştür.",
                "hint": "%75'ten %33'e."
            }
        ]
    },
    {
        "slideNumber": 16,
        "title": "Sağlık İşgücünün Korunması ve Sağlık Sisteminin Güçlendirilmesi",
        "subtitle": "Kişisel koruyucu ekipman (KKD), tükenmişliğin önlenmesi ve sağlık finansmanı yatırımları",
        "badge": "Sağlık İşgücü & KKD",
        "badgeColor": "teal",
        "target_ids": [],
        "keywords": ["sağlık işgücü", "kişisel koruyucu", "kkd", "sağlık finansmanı"],
        "lead": "Salgın cephesinde en kritik savunma hattı sağlık çalışanlarıdır; hekimleri, hemşireleri ve toplum sağlığı çalışanlarını koruyamayan hiçbir sistem salgını durduramaz.",
        "spotPearls": [
            "SAĞLIK İŞGÜCÜNÜN KORUNMASI: Salgında toplum sağlığı çalışanları, ebeler, hemşireler ve hekimler hayati fark yaratır; onların hastalıktan ve tükenmişlikten korunması hizmetin sürekliliği için şarttır.",
            "KİŞİSEL KORUYUCU EKİPMAN (KKD): Sağlık çalışanlarına yeterli, güvenli ve amaca uygun KKD (N95/FFP2 maske, tulum, siperlik, eldiven) sağlanması ertelenemez bir zorunluluktur.",
            "SAĞLIK FİNANSMANI: Epidemiler sistemleri devasa stres altında bırakır; çok sayıda hastanın sağlık tesislerine ani akışı kapasiteyi kilitler.",
            "UZUN VADELİ YATIRIM ŞARTI: Sağlık sistemlerini salgından önce güçlendirecek uzun vadeli bütçe ve insan kaynağı yatırımları yapılmalıdır."
        ],
        "keyBullets": [
            {"title": "Çalışan Enfeksiyonunun Domino Etkisi", "desc": "Bir hemşire veya doktor enfekte olduğunda hem bir sağlık personeli kaybedilir hem de hastane içi nozokomiyal salgın başlar."},
            {"title": "Psikososyal Destek", "desc": "Salgın sürecindeki aşırı çalışma, ölüm tanıklığı ve izolasyon sağlık personelinde travma sonrası stres ve tükenmişlik yaratır."},
            {"title": "Yedek İşgücü Havuzları", "desc": "Karantinaya giren personelin yerini alacak yedek tıbbi kadrolar önceden planlanmalıdır."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-31",
                "question": "Salgınlarda sağlık hizmetlerinin aksamadan sürdürülebilmesi için sağlık çalışanlarına sağlanması gereken en temel lojistik güvence nedir?",
                "answer": "Yeterli, amaca uygun ve güvenli Kişisel Koruyucu Ekipman (KKD) temini ve güvenli çalışma koşullarıdır.",
                "hint": "Kişisel Koruyucu Ekipman (KKD)."
            },
            {
                "id": "fc-ep-32",
                "question": "Salgın dönemlerinde hastaneleri ve sağlık tesislerini kilitleyen temel epidemiyolojik dinamik nedir?",
                "answer": "Çok sayıda hasta bireyin çok kısa bir zaman diliminde aniden sağlık tesislerine akın etmesi ve kapasiteyi aşmasıdır.",
                "hint": "Ani ve kitlesel hasta akını."
            }
        ]
    },
    {
        "slideNumber": 17,
        "title": "Halk Sağlığında Koruma Düzeyleri ve Salgınla İlişkisi",
        "subtitle": "Primordial, birincil (aşılama), ikincil (tarama/filyasyon) ve üçüncül (tedavi/rehabilitasyon) koruma",
        "badge": "Koruma Düzeyleri",
        "badgeColor": "purple",
        "target_ids": ["d3-k1-hs-004", "d3-k1-hs-005"],
        "keywords": ["birincil koruma", "ikincil koruma", "üçüncül koruma", "koruma basamakları"],
        "lead": "Halk sağlığının koruyucu hekimlik piramidi hastalıkların henüz ortaya çıkmadan önlenmesinden, komplikasyonların engellenmesine kadar dört evrede kurgulanır.",
        "spotPearls": [
            "BİRİNCİL (PRİMER) KORUMA: Hastalık henüz ortaya çıkmadan, sağlıklı bireylerin korunmasıdır. EN TİPİK ÖRNEKLER: BAĞIŞIKLAMA (Aşılama), sağlık eğitimi, temiz su ve gıda temini, aile planlaması ve dengeli beslenme (Kurul 1 Çıkmış Soru!).",
            "İKİNCİL (SEKONDER) KORUMA: Hastalığın belirtisiz (preklinik) veya erken evrede yakalanarak tedavi edilmesidir. EN TİPİK ÖRNEKLER: TARAMALAR (Tansiyon ölçümü, mamografi, Pap-smear, filyasyon testleri) (Kurul 1 Çıkmış Soru!).",
            "ÜÇÜNCÜL (TERSİYER) KORUMA: Klinik hastalık oluştuktan sonra sakatlık ve komplikasyonların önlenmesi, rehabilitasyondur. EN TİPİK ÖRNEKLER: DİYABETİK HASTADA AYAK BAKIMI, inme sonrası fizyoterapi, körlüğü önleme (Kurul 1 Çıkmış Soru!).",
            "PRİMORDİAL KORUMA: Risk faktörlerinin toplumda hiç yerleşmemesi için yasal ve sosyal düzenlemeler yapılmasıdır (örneğin kapalı alanda sigara yasağı, trans yağ kısıtlaması)."
        ],
        "keyBullets": [
            {"title": "Sınav Tuzakları", "desc": "Tansiyon ölçümü bir erken tanıdır, dolayısıyla BİRİNCİL değil İKİNCİL korumadır!"},
            {"title": "Salgında Birincil Mücadele", "desc": "Aşılama, maske kullanımı ve el yıkama doğrudan birincil koruma uygulamalarıdır."},
            {"title": "Salgında İkincil Mücadele", "desc": "Filyasyon ekiplerinin PCR testleriyle temaslıları erken yakalaması ikincil korumadır."}
        ],
        "table": {
            "title": "Halk Sağlığında Koruma Düzeyleri ve Fakülte Sınav Sınıflaması",
            "headers": ["Koruma Düzeyi", "Uygulanan Kişi Grubu", "Temel Amaç", "Klasik Sınav Örnekleri"],
            "rows": [
                ["Primordial Koruma", "Tüm toplum", "Risk faktörlerinin ortaya çıkışını önlemek", "Sigara yasaları, temiz hava mevzuatı, kent planlaması"],
                ["Birincil (Primer)", "Sağlıklı bireyler", "Hastalığın insidansını sıfıra indirmek", "BAĞIŞIKLAMA (Aşı), Sağlık eğitimi, Güvenli su, Beslenme"],
                ["İkincil (Sekonder)", "Erken evre / Asemptomatik", "Erken tanı ve ilerlemeyi durdurma", "TARAMALAR: Tansiyon ölçümü, Mamografi, Filyasyon PCR"],
                ["Üçüncül (Tersiyer)", "Klinik tanılı hastalar", "Sakatlık, ölüm ve komplikasyonu önleme", "DİYABETİK AYAK BAKIMI, İnme rehabilitasyonu, Kalp cerrahisi"]
            ]
        },
        "flashcards": [
            {
                "id": "fc-ep-33",
                "question": "Aşılama (bağışıklama) ve sağlık eğitimi halk sağlığında hangi koruma düzeyine girer?",
                "answer": "Birincil (Primer) koruma düzeyine girer.",
                "hint": "Birincil (Primer) koruma."
            },
            {
                "id": "fc-ep-34",
                "question": "Hipertansiyon taraması amacıyla yapılan tansiyon ölçümü ile diyabetik hastaların ayak bakımı sırasıyla hangi koruma düzeylerindedir?",
                "answer": "Tansiyon ölçümü = İkincil (sekonder) koruma; Diyabetik ayak bakımı = Üçüncül (tersiyer) korumadır.",
                "hint": "Tansiyon ölçümü = İkincil; Diyabetik ayak bakımı = Üçüncül."
            }
        ]
    },
    {
        "slideNumber": 18,
        "title": "Büyük Sentez: Salgın Yönetim Algoritması ve Kurul 1 Altın İpuçları",
        "subtitle": "Uzm. Dr. Erkay Nacar amfi dersi çekirdek sentezi, filyasyon, karantina vs izolasyon ve sınav spotları",
        "badge": "Büyük Sentez",
        "badgeColor": "sky",
        "target_ids": ["d3-k1-hs-007", "d3-k1-hs-016", "d3-k1-hs-017"],
        "keywords": ["büyük sentez", "altın spotlar", "karantina", "izolasyon", "filyasyon"],
        "lead": "Salgın hastalıkların kontrolü bilimsel sürveyans, erken teşhis, şeffaf risk iletişimi ve güçlü bir sağlık altyapısının kusursuz senkronizasyonuyla mümkündür.",
        "spotPearls": [
            "EPİDEMİ VS SPORADİ: Beklenenden fazla görülme = EPİDEMİ; ara sıra tek tük görülme = SPORADİ; dünya geneline yayılma = PANDEMİ.",
            "ELİMİNASYON VS ERADİKASYON: Bölgesel sıfırlama (aşı/önlem devam eder) = ELİMİNASYON; Küresel ve kalıcı sıfırlama (dünyada tek örnek: Çiçek) = ERADİKASYON.",
            "KARANTİNA VS İZOLASYON AYRIMI: İzolasyon HASTA bireylerin ayrılmasıdır; Karantina ise TEMASLI OLAN ANCAK HENÜZ HASTA OLMAYAN şüpheli kişilerin kuluçka süresince hareketinin kısıtlanmasıdır!",
            "İLK VAKA KURALI: Sınırlama ilk vaka görüldüğünde derhal başlamalıdır; etkenin tam izolasyonu beklenmez.",
            "ZOONOZLAR: Ortaya çıkan patojenlerin %70'i hayvan kaynaklıdır (Tek Sağlık zorunluluğu).",
            "İNFODEMİ FORMÜLÜ: Konuşma + Dinleme + Dedikoduları Engelleme."
        ],
        "keyBullets": [
            {"title": "Klinisyenin Uyanıklığı", "desc": "Salgını ilk fark eden poliklinikteki hekimdir; sürveyans klinisyenle başlar."},
            {"title": "Destek Tedavisi Kanıtı", "desc": "Ebola'da ilaçsız yalnızca iyi destek bakımıyla ölüm %75'ten %33'e indirilmiştir."},
            {"title": "Aşı Gücü", "desc": "DBT aşısı dünya çocuklarının %86'sını koruyan en maliyet-etkili halk sağlığı zaferidir."}
        ],
        "flashcards": [
            {
                "id": "fc-ep-35",
                "question": "Salgın kontrolünde 'İzolasyon' ile 'Karantina' arasındaki temel kavramsal fark nedir?",
                "answer": "İzolasyon hasta/enfekte bireylerin sağlamlardan ayrılmasıdır; Karantina ise hasta olmayan ancak temaslı şüpheli kişilerin kuluçka süresince kısıtlanmasıdır.",
                "hint": "İzolasyon = Hasta; Karantina = Temaslı/şüpheli sağlıklı."
            },
            {
                "id": "fc-ep-36",
                "question": "Kurul 1 Halk Sağlığı sınavında 'Hastalığın etkeni dünyadan tamamen silinmemişken belirli bir bölgede yerli vakanın görülmemesi' sorulduğunda doğru yanıt nedir?",
                "answer": "Eliminasyon.",
                "hint": "Eliminasyon."
            }
        ]
    }
]

def build_synthesis_narrative(slide_data):
    lines = []
    lines.append(f"### {slide_data['title']}")
    lines.append(f"#### {slide_data['subtitle']}")
    lines.append("")
    lines.append(f"• **Temel Halk Sağlığı ve Epidemiyolojik Çerçeve:** {slide_data['lead']}")
    lines.append("")
    
    for kb in slide_data.get('keyBullets', []):
        lines.append(f"• **{kb['title']}:** {kb['desc']}")
        lines.append("")

    lines.append("💡 **Halk Sağlığı Sentezi ve Fakülte Sınav İncileri (Uzm. Dr. Erkay Nacar):**")
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
            f"Uzm. Dr. Erkay Nacar'ın amfi dersinde '{title_clean}' konusunda vurguladığı en kritik sınav spotları nelerdir?",
            f"Halk sağlığı pratiğinde '{title_clean}' ilkeleri doğrultusunda bir salgın yönetim algoritması nasıl kurgulanır?",
            f"Dönem 3 Kurul 1 Halk Sağlığı sınavında '{title_clean}' konusundan çıkabilecek soru tuzakları ve ayırt edici noktalar nelerdir?"
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
        "id": "learn-halk-sagligi-salgin-has",
        "title": "Salgın Hastalıklarda Kontrol, Sürveyans ve Korunma",
        "shortTitle": "Salgın Kontrolü & Sürveyans",
        "discipline": "Halk Sağlığı",
        "committee": "Dönem 3 Kurul 1",
        "instructor": "Uzm. Dr. Erkay Nacar",
        "sourceFile": "4)'Salgın Hastalıklarda Kontrol ve Korunma'.txt",
        "totalSlides": len(slides),
        "matchedQuestionsCount": total_questions,
        "totalFlashcardsCount": total_cards,
        "themeColor": "teal",
        "overview": "Dönem 3 Kurul 1 Halk Sağlığı müfredatında yer alan Salgın Hastalıklarda Kontrol ve Korunma Yöntemleri dersinin %500 derinlikte kapsamlı interaktif öğrenim sunumu. 1970 yanılgısı ve yeni çıkan patojenler, zoonozlar (%70 kuralı), epidemiyolojik dağılım kalıpları (endemi, epidemi, pandemi, sporadi), 4 epidemik faz, ilk vaka kuralı ve mitigasyon, mücadele düzeyleri (kontrol, eliminasyon, eradikasyon), 4 ayaklı salgın yanıt sistemi, acil operasyon merkezleri (EOC), sağlık enformasyonu ve sürveyans (kişi, zaman, yer), risk iletişimi ve infodemi, iki yönlü iletişim, destekleyici bakımın hayat kurtaran gücü (Ebola örneği), koruma düzeyleri (primer, sekonder, tersiyer), 36 adet 3D akıl kartını, 5 adet karşılaştırma tablosunu ve Kurul 1 çıkmış sınav sorularını içerir.",
        "keyExamPearls": [
            "1970 yanılgısı: Bulaşıcı hastalıkların bittiği sanılırken 1500'den fazla yeni patojen tanımlanmıştır.",
            "Yeni ortaya çıkan patojenlerin yaklaşık %70'i hayvan kaynaklıdır (Zoonozlar; 'Tek Sağlık' yaklaşımı).",
            "Epidemi: Bir hastalığın belli bir bölgede beklenenden anlamlı ölçüde daha fazla görülmesidir.",
            "Sporadi: Bir hastalığın bir bölgede ara sıra ve tek tük olgular halinde görülmesidir.",
            "Eliminasyon: Belirli bir bölgede yerli (otokton) vakanın görülmemesidir; aşı ve sürveyans KESİNTİSİZ DEVAM EDER.",
            "Eradikasyon: Patojenin dünya çapında kalıcı olarak sıfırlanmasıdır (insanda tek örnek: Çiçek Hastalığı).",
            "Sınırlama (containment) ilk vaka teşhis edildiği anda başlatılmalıdır; etkenin tam izolasyonu beklenmez.",
            "Salgın yanıtının 4 ayağı: Koordinasyon, Sağlık Enformasyonu, Risk İletişimi, Eksiksiz Müdahaleler.",
            "Sürveyans 3 temel değişkene dayanır: KİŞİ, ZAMAN ve YER.",
            "İnfodemiyle mücadelede 3 altın kural: Konuşma, Dinleme ve Dedikoduları Engelleme.",
            "2014 Ebola salgınında spesifik ilaç olmadan yalnızca iyi klinik destekleyici bakımla ölüm oranı %75'ten %33'e düşürülmüştür.",
            "Koruma düzeyleri: Bağışıklama ve sağlık eğitimi = BİRİNCİL; Tansiyon ölçümü ve taramalar = İKİNCİL; Diyabetik ayak bakımı = ÜÇÜNCÜL korumadır."
        ],
        "slides": slides
    }

    return deck_obj

def main():
    print("Generating comprehensive %500 detail deck for Salgın Hastalıklarda Kontrol, Sürveyans ve Korunma...")
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
            elif item.get('id') == 'learn-enfeksiyon-izolasyon':
                item['status'] = 'next_in_queue'
        with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Updated learning_batch_queue.json: Salgın Hastalıklar completed, Enfeksiyon İzolasyon next!")

    print("Success! Epidemic control deck generation completed.")

if __name__ == '__main__':
    main()
