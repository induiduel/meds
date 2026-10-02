#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_learning_decks.py
========================
Bu script:
1. c:\\Users\\indui\\Desktop\\meds_database\\transcriptions altındaki ses transkriptlerini okur.
2. Transkriptteki hocanın dakika dakika vurgularını, "buradan soru sorarız", "slaytta yok beni dinleyin" gibi
   amfi sınav uyarılarını tespit eder.
3. src/data/lecture_notes.json içerisindeki ilgili ders notu slaytları ile eşler.
4. src/data/pastQuestions.json içerisindeki geçmiş kurul çıkmış sorularıyla eşleştirir.
5. c:\\Users\\indui\\Desktop\\meds_database\\redakte_ozet altındaki derin tıp özetleriyle zenginleştirir.
6. Hem tam ekran PPTX tarzı slayt sunusu olarak ilerleyebilen, hem de dikey kaydırılabilen zengin interaktif
   desteleri src/data/interactive_learning_decks.json dosyasına derler.
"""

import os
import sys
import json
import re
import glob

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MEDS_DB_ROOT = r'c:\Users\indui\Desktop\meds_database'
TRANSCRIPTIONS_DIR = os.path.join(MEDS_DB_ROOT, 'transcriptions')
REDAKTE_DIR = os.path.join(MEDS_DB_ROOT, 'redakte_ozet')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'src', 'data', 'interactive_learning_decks.json')
OUTPUT_META_FILE = os.path.join(PROJECT_ROOT, 'src', 'data', 'learning_decks_meta.json')

LECTURE_NOTES_PATH = os.path.join(PROJECT_ROOT, 'src', 'data', 'lecture_notes.json')
PAST_QUESTIONS_PATH = os.path.join(PROJECT_ROOT, 'src', 'data', 'pastQuestions.json')

def normalize_tr(text):
    if not text:
        return ""
    text = text.lower()
    rep = {
        'ı': 'i', 'i̇': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        'â': 'a', 'î': 'i', 'û': 'u'
    }
    for k, v in rep.items():
        text = text.replace(k, v)
    return text

def load_json(filepath):
    if not os.path.exists(filepath):
        print(f"[Uyarı] Dosya bulunamadı: {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def match_questions(keywords, discipline, all_questions, limit=8):
    if not all_questions:
        return []

    scored = []
    norm_keywords = [normalize_tr(k) for k in keywords if len(k) >= 3]
    norm_discipline = normalize_tr(discipline) if discipline else ""

    for q in all_questions:
        q_disc = normalize_tr(q.get('discipline') or '')
        q_topic = normalize_tr(q.get('topic') or '')
        q_stem = normalize_tr(q.get('stem') or '')
        q_opts = " ".join([normalize_tr(o.get('text', '')) for o in q.get('options', [])])
        q_full = f"{q_topic} {q_stem} {q_opts}"

        score = 0
        for kw in norm_keywords:
            if kw in q_topic:
                score += 4
            elif kw in q_stem:
                score += 2.5
            elif kw in q_opts:
                score += 1.5

        if norm_discipline and (norm_discipline in q_disc or q_disc in norm_discipline):
            score += 1.2

        if score > 0:
            scored.append((score, q))

    scored.sort(reverse=True, key=lambda x: x[0])
    
    res = []
    seen = set()
    for s, q in scored:
        qid = q.get('id')
        if qid in seen:
            continue
        seen.add(qid)
        res.append({
            'id': qid,
            'examYear': q.get('examYear') or 'Geçmiş Kurul',
            'committeeId': q.get('committeeId') or 'Kurul',
            'discipline': q.get('discipline') or discipline,
            'topic': q.get('topic') or '',
            'stem': q.get('stem') or '',
            'options': q.get('options') or [],
            'correctAnswer': q.get('correctAnswer') or q.get('claimedAnswer') or 'A',
            'explanation': q.get('explanation') or '',
            'matchScore': round(s, 1)
        })
        if len(res) >= limit:
            break
    return res

def parse_transcript_file(filename):
    path = os.path.join(TRANSCRIPTIONS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title
    title_m = re.search(r'^#\s*🩺?\s*(.+)$', content, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else filename

    # Extract pearls
    pearls = []
    pearls_sec = re.search(r'##\s*⭐\s*Amfi & Sınav Hap Bilgileri.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if pearls_sec:
        raw_bullets = re.findall(r'^[*-]\s*(.+)$', pearls_sec.group(1), re.MULTILINE)
        pearls = [b.strip() for b in raw_bullets if len(b.strip()) > 5]

    # Extract utterances
    utterances = []
    for m in re.finditer(r'\[(\d{2}:\d{2})\]\s*([^\[]+)', content):
        ts = m.group(1)
        text = clean_text(m.group(2))
        if text:
            utterances.append({'timestamp': ts, 'text': text})

    return {
        'title': title,
        'pearls': pearls,
        'utterances': utterances,
        'fullText': content
    }

def find_utterance(utterances, search_words):
    for u in utterances:
        norm_txt = normalize_tr(u['text'])
        if any(normalize_tr(w) in norm_txt for w in search_words):
            return u
    return None

def build_all_decks():
    print("Ders notları ve çıkmış sorular yükleniyor...")
    lecture_notes = load_json(LECTURE_NOTES_PATH) or []
    past_questions = load_json(PAST_QUESTIONS_PATH) or []
    manifest_path = os.path.join(TRANSCRIPTIONS_DIR, 'transcription_manifest.json')
    manifest = load_json(manifest_path) or {}

    print(f"Toplam {len(lecture_notes)} ders notu, {len(past_questions)} çıkmış soru mevcut.")

    decks = []

    # =========================================================================
    # 1. DECK: ANA ÇOCUK SAĞLIĞI DÜZEYİNİN İZLENMESİ
    # =========================================================================
    ac_trans = parse_transcript_file('Ana_Cocuk_Sagligi_Duzeyinin_Izlenmesi_Transkript.md')
    if ac_trans:
        deck_id = 'learn-ana-cocuk-sagligi'
        deck = {
            'id': deck_id,
            'title': 'Ana Çocuk Sağlığı Düzeyinin İzlenmesi',
            'shortTitle': 'Ana Çocuk Sağlığı',
            'discipline': 'Halk Sağlığı',
            'committee': 'Kurul 1 - Halk Sağlığı (Dönem 3)',
            'instructor': 'Doç. Dr. Nergiz Sevinç',
            'audioFile': 'Halk Sağlığı Anne çocuk Sağlığı İzleme.m4a',
            'audioDuration': '43.1 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'sky',
            'matchedNoteId': 'note-b825fa7e46',
            'matchedNoteTitle': '2)Ana çocuk sağ.izleme',
            'overview': 'Koruyucu hekimlik hizmetlerinde risk altındaki 15-49 yaş kadınlar, gebeler ve bebeklerin periyodik izlemleri, Anne Ölüm Hızı (AÖH), Bebek Ölüm Hızı (BÖH) formülleri ve Doğum Öncesi Bakım (DÖB) protokolleri.',
            'highYieldPearls': ac_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Koruyucu Hekimlik ve Birinci Öncelikli Risk Grupları',
                    'subtitle': 'Halk Sağlığı Hedef Kitle Hiyerarşisi',
                    'badge': 'AMFİ GİRİŞ VURGUSU',
                    'badgeColor': 'sky',
                    'professorAudioHighlight': {
                        'timestamp': '00:39',
                        'quote': 'Bunlar slaytlarda yok yani benim söylediklerimi dinleyin tamam mı? Bizim birinci basamak koruyucu hekimlikte ilk grubumuzda kimler var? Bebekler ve 15-49 yaş kadın grubu var.',
                        'emphasisType': 'slide_missing',
                        'note': 'Hoca slaytta açıkça yazmayan birincil hedef kitlenin (15-49 yaş kadın ve bebekler) amfide bizzat not alınmasını istedi.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Öncelikli Nüfus Dilimleri', 'desc': 'Kendi başına hayatta kalamayan veya bakım verilmediğinde morbidite/mortalite riski en yüksek gruplar.'},
                            {'title': '15-49 Yaş Doğurgan Çağ Kadınları', 'desc': 'Türkiye nüfusunun %25\'ini, dünya nüfusunun ise %24\'ünü oluşturur.'},
                            {'title': '0-14 Yaş Çocuk Grubu', 'desc': 'Türkiye nüfusunun %20\'sini teşkil eder ve koruyucu aşı/gelişim takibi zorunludur.'}
                        ],
                        'table': {
                            'title': 'Demografik Öncelik ve Risk Dağılımı',
                            'headers': ['Hedef Grup', 'Türkiye Nüfus Payı', 'Birincil İzlem Amacı'],
                            'rows': [
                                ['0-1 Yaş (Bebek)', '%1.4', 'Aşı takvimi, fenilketonüri/hipotiroidi taraması, büyüme takibi'],
                                ['15-49 Yaş Kadın', '%25.0', 'DÖB, üreme sağlığı, anemi taraması, aile planlaması'],
                                ['Gebeler & Lohusalar', 'Dinamik Risk', 'Maternal ve erken neonatal mortalitenin önlenmesi']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Koruyucu hekimlikte en öncelikli risk grubu: Bebekler ve 15-49 yaş doğurganlık çağındaki kadınlardır.',
                        'Türkiye nüfusunda 15-49 yaş kadın oranı yaklaşık %25, 0-14 yaş çocuk grubu ise %20 civarındadır.'
                    ],
                    'relatedQuestions': match_questions(['ana cocuk', 'dogurgan', 'risk grubu', 'koruyucu'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        '15-49 yaş kadın grubunun halk sağlığındaki stratejik önemi nedir?',
                        'Hoca amfide slaytta olmayan hangi risk gruplarını vurguladı?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Ülkelerin Kalkınmışlık Göstergesi: Anne ve Bebek Ölüm Hızları',
                    'subtitle': 'Sağlık Düzeyi ve Gelişmişlik Kriterleri',
                    'badge': 'SINAV KLASİĞİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '03:00',
                        'quote': 'Bir ülkenin kalkınmışlık düzeyine bakarken en önemli faktörlerden bir tanesi o ülkenin anne ölüm hızı ve bebek ölüm hızı oranlarıdır. Sağlık sistemimiz ne, teknoloji ne, ulaşım ne; hepsini bu iki kriter özetler.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca kalkınmışlık seviyesinin tespitinde GSYİH\'den bile önce AÖH ve BÖH\'e bakıldığının altını çizdi.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Anne Ölüm Hızı (AÖH)', 'desc': 'Sağlık hizmetine erişim, acil obstetrik bakım ve kadın statüsünün en duyarlı barometresidir.'},
                            {'title': 'Bebek Ölüm Hızı (BÖH)', 'desc': 'Sosyoekonomik durum, beslenme, çevre sağlığı ve birinci basamak etkinliğini yansıtır.'},
                            {'title': 'Uluslararası Kıyaslama', 'desc': 'Gelişmiş ülkelerde AÖH yüz binde tek haneli iken Sahra altı Afrika\'da yüz binde yüzleri bulmaktadır.'}
                        ],
                        'infographic': {
                            'type': 'metrics',
                            'items': [
                                {'label': 'Türkiye AÖH (2023)', 'value': '11.5 / 100.000', 'detail': 'Canlı doğum başına maternal kayıp', 'color': 'rose'},
                                {'label': 'Türkiye BÖH (2023)', 'value': '10.5 / 1.000', 'detail': 'Canlı doğum başına 1 yaş altı kayıp', 'color': 'sky'},
                                {'label': 'Hedef', 'value': '< 8 / 100.000', 'detail': 'DSÖ ve Sağlık Bakanlığı vizyonu', 'color': 'emerald'}
                            ]
                        }
                    },
                    'spotPearls': [
                        'Bir toplumun sağlık ve gelişmişlik düzeyini en iyi yansıtan iki gösterge: Anne Ölüm Hızı ve Bebek Ölüm Hızıdır.',
                        'Türkiye\'de 2023 verilerine göre AÖH yüz binde 11.5, BÖH binde 10.5 seviyelerindedir.'
                    ],
                    'relatedQuestions': match_questions(['bebek olum hizi', 'anne olum hizi', 'kalkinmislik', 'gosterge'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'AÖH ile BÖH arasındaki fark nedir ve neden farklı çarpanlarla (100.000 vs 1.000) hesaplanır?',
                        'Bir ülkenin sağlık düzeyini değerlendirmede bu göstergelerin rolü nedir?'
                    ]
                },
                {
                    'slideNumber': 3,
                    'title': 'Doğum Öncesi Bakım (DÖB) Altın Standartları',
                    'subtitle': 'Yeterli Bakım Sayılma Kriterleri ve İzlem Takvimi',
                    'badge': 'PROTOKOL & MEVZUAT',
                    'badgeColor': 'emerald',
                    'professorAudioHighlight': {
                        'timestamp': '05:02',
                        'quote': 'Bir gebenin yeterli doğum öncesi bakım almıştır diyebilmemiz için kriterlerimiz var: İlk izlem mutlaka ilk 3 ay içinde olmalı, gebelik boyunca en az 4 kez izlenmeli ve tecrübeli sağlık personeli (ebe/hekim) tarafından yapılmalı.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca "DÖB yeterlilik kriterleri"nin sınavda soru olarak gelebileceğini özellikle belirtti.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Kriter 1: Erken Başvuru', 'desc': 'İlk izlemin ilk trimesterda (ilk 3 ay / 14. haftadan önce) gerçekleşmesi şarttır.'},
                            {'title': 'Kriter 2: Asgari İzlem Sayısı', 'desc': 'Komplikasyonsuz bir gebelikte asgari 4 nitelikli izlem tamamlanmalıdır.'},
                            {'title': 'Kriter 3: Yetkin Personel', 'desc': 'İzlemin ebe, kadın doğum uzmanı veya aile hekimi tarafından yapılması gerekir.'}
                        ],
                        'table': {
                            'title': 'Sağlık Bakanlığı DÖB Asgari İzlem Takvimi',
                            'headers': ['İzlem', 'Gebelik Haftası', 'Temel Girişimler'],
                            'rows': [
                                ['1. İzlem', 'İlk 14 hafta (1. Trimester)', 'Kan grubu, Hb, idrar, açlık şekeri, TSH, USG, folik asit'],
                                ['2. İzlem', '18 - 24. Hafta', 'Fetal anomali taraması, tansiyon takibi, tetanoz aşısı 1'],
                                ['3. İzlem', '28 - 32. Hafta', 'Kan sayımı tekrarı, Gestasyonel DM taraması (OGTT), aşı 2'],
                                ['4. İzlem', '36 - 38. Hafta', 'Fetal pozisyon, pelvik uygunluk, doğum planlaması']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Yeterli DÖB şartları: 1) İlk izlemin ilk 3 ay içinde olması, 2) En az 4 izlem yapılması, 3) Tecrübeli sağlık personeli takibi.',
                        'Gebelik tespit edildiği anda başlanması gereken profilaksi: İlk trimesterda Folik Asit (400 mcg/gün), 16. haftadan itibaren Demir desteği.'
                    ],
                    'relatedQuestions': match_questions(['dogum oncesi bakim', 'dob', 'gebelik izlem', 'trimester'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'DÖB protokolünde 4 izlemin haftaları ve zorunlu tetkikleri nelerdir?',
                        'Aile sağlığı merkezlerinde gebenin takibinde ebenin rolü nedir?'
                    ]
                },
                {
                    'slideNumber': 4,
                    'title': 'Anne Ölüm Hızı (AÖH): Tanım, Sınır ve Formül',
                    'subtitle': 'Vaka Sorusu Çıkacak Matematiksel Formülasyon',
                    'badge': '⭐ HOCA VURGUSU: VAKA SORUSU GELİR',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '09:42',
                        'quote': 'Burada formülü var arkadaşlar. Buradan soru çıkar! Bir vaka gibi bir bilgi sorarız, siz de anne ölüm oranı nedir diye hesaplarsınız. Gebelikte, doğumda veya doğumdan sonraki 42 gün içindeki obstetrik ölümlerdir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca doğrudan amfide "Buradan vaka sorusu sorarız" ikazında bulundu. Çarpana (100.000) ve 42 günlük süreye dikkat!'
                    },
                    'coreContent': {
                        'formulaBox': {
                            'title': 'Anne Ölüm Hızı (AÖH / Maternal Mortality Ratio) Formülü',
                            'formula': 'AÖH = (Bir yılda obstetrik nedenlerle ölen anne sayısı / Aynı yıl gerçekleşen canlı doğum sayısı) × 100.000',
                            'explanation': 'Paydada TÜM GEBELİKLER DEĞİL, sadece CANLI DOĞUMLAR yer alır! Çarpan ise 100.000\'dir.'
                        },
                        'keyBullets': [
                            {'title': 'Süre Kriteri: 42 Gün', 'desc': 'Gebelik süresince, doğum anında veya gebeliğin sonlanmasından sonraki ilk 42 gün içinde meydana gelen ölümler.'},
                            {'title': 'Obstetrik Neden Şartı', 'desc': 'Gebelik komplikasyonları veya gebeliğin ağırlaştırdığı hastalıklardan kaynaklanmalıdır (Kaza veya tesadüfi nedenler hariçtir).'},
                            {'title': 'Direkt vs İndirekt Ölüm', 'desc': 'Direkt: Kanama, preeklampsi, emboli, sepsis. İndirekt: Önceden var olan kalp hastalığının gebelik yüküyle dekompanse olması.'}
                        ]
                    },
                    'spotPearls': [
                        'Anne ölümü zaman sınırı: Gebelik süresi + Doğum sonrası ilk 42 gün (6 hafta - lohusalık dönemi).',
                        'AÖH formülünde payda her zaman CANLI DOĞUM SAYISI, çarpan ise 100.000\'dir (Bebek ölümünde binde, anne ölümünde yüz binde!).',
                        'Trafik kazası, intihar gibi tesadüfi nedenler anne ölümü tanımına dahil edilmez.'
                    ],
                    'relatedQuestions': match_questions(['anne olum', 'aoh', 'maternal olum', 'canli dogum'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Örnek bir Anne Ölüm Hızı vaka sorusu çöz: 50.000 canlı doğumda 6 maternal ölüm olursa AÖH kaçtır?',
                        'Lohusalıkta 40. günde pulmoner emboliden ölen kadın anne ölümü sayılır mı?'
                    ]
                },
                {
                    'slideNumber': 5,
                    'title': 'Bebek ve Neonatal Ölüm Hızları Sınıflaması',
                    'subtitle': 'Erken Neonatal, Geç Neonatal ve Postneonatal Dönemler',
                    'badge': 'DÖNEM AYRIMI',
                    'badgeColor': 'amber',
                    'professorAudioHighlight': {
                        'timestamp': '02:31',
                        'quote': 'Ölü bildirim sistemi (ÖBS) doldururken sorar: Bebek ölümü kaçıncı günde oldu? Doğumdan sonraki ilk 7 gün içindeki ölüm erken neonataldir ve doğrudan sağlık hizmetinin niteliğini gösterir.',
                        'emphasisType': 'clinical_tip',
                        'note': 'Hoca ilk 7 günün (erken neonatal) hastane şartları ve doğum anı kalitesine en duyarlı dönem olduğunu belirtti.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Bebek Ölüm Hızı (BÖH)', 'desc': '(1 yılda 1 yaşını doldurmadan ölen bebek sayısı / Canlı doğum sayısı) × 1.000'},
                            {'title': 'Erken Neonatal Ölüm', 'desc': '0 - 6. gün (ilk 7 gün) içindeki ölümler. Doğum travması, asfiksi, konjenital anomaliler hakimdir.'},
                            {'title': 'Geç Neonatal Ölüm', 'desc': '7 - 27. gün arasındaki ölümler. Hastane enfeksiyonları, beslenme güçlükleri.'},
                            {'title': 'Postneonatal Ölüm', 'desc': '28 - 364. gün arasındaki ölümler. Çevre sağlığı, enfeksiyonlar (pnömoni, ishal) ve beslenme yetersizliklerine bağlıdır.'}
                        ],
                        'table': {
                            'title': 'Bebeklik Dönemi Ölüm Hızı Karşılaştırması',
                            'headers': ['Dönem', 'Gün Aralığı', 'Başlıca Nedenler', 'Hassas Olduğu Alan'],
                            'rows': [
                                ['Erken Neonatal', '0 - 6 gün', 'Prematürite, RDS, Asfiksi, Konjenital Anomali', 'Doğum salonu & YYBÜ kalitesi'],
                                ['Geç Neonatal', '7 - 27 gün', 'Sepsis, menenjit, metabolik bozukluklar', 'Yenidoğan bakımı'],
                                ['Postneonatal', '28 - 364 gün', 'Gastroenterit, alt solunum yolu enf., malnütrisyon', 'Sosyoekonomik & Çevre koşulları']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Erken Neonatal: 0-6 gün, Geç Neonatal: 7-27 gün, Postneonatal: 28-364 gün.',
                        'Erken neonatal ölümler tıbbi bakım kalitesine, postneonatal ölümler ise çevre ve hijyen koşullarına bağlıdır.',
                        'BÖH çarpanı 1.000 (binde), AÖH çarpanı ise 100.000 (yüz binde)\'dir.'
                    ],
                    'relatedQuestions': match_questions(['bebek olum', 'neonatal', 'erken neonatal', 'postneonatal'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Postneonatal ölüm hızını düşürmek için hangi halk sağlığı önlemleri alınmalıdır?',
                        'Perinatal ölüm hızı nedir ve hangi haftaları kapsar?'
                    ]
                },
                {
                    'slideNumber': 6,
                    'title': 'Aile Hekimliği Uygulamasında Performansa Dayalı İzlemler',
                    'subtitle': 'Lohusalık, Ev Ziyaretleri ve Birinci Basamak Sorumluluğu',
                    'badge': 'KLİNİK PRATİK & SAHA',
                    'badgeColor': 'indigo',
                    'professorAudioHighlight': {
                        'timestamp': '09:02',
                        'quote': 'Neden önemli? Çünkü bunlar aile hekimlerine dağıtılmış performansa dayalı izlemlerdir. İzlemler yapılmadığında hekimden maaş kesintisi yapılır. Lohusalıkta da ilk 40 gün içinde ev ziyaretleri zorunludur.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca birinci basamakta çalışan her hekimin gebe ve lohusa izlemlerini kaçırmaması gerektiğini pratik örnekle vurguladı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Performansa Dayalı Takip', 'desc': 'Aile hekimleri kendilerine kayıtlı her gebe ve bebeği sisteme girmek ve periyodik izlemek zorundadır.'},
                            {'title': 'Lohusa İzlem Protokolü', 'desc': 'Doğum sonrası ilk 24 saat, 3. gün, 7. gün ve 15-40. günler arasında en az 3 izlem yapılmalıdır.'},
                            {'title': 'Ev Ziyaretleri', 'desc': 'Sağlık personeli aile sağlığı merkezine gelemeyen yüksek riskli lohusaları hanesinde ziyaret eder.'}
                        ]
                    },
                    'spotPearls': [
                        'Lohusalık süresi 6 hafta (42 gün) olup, ilk izlem doğum taburculuğunu takiben ilk 3 gün içinde yapılmalıdır.',
                        'Bebek izlemleri: Doğumda, 15. günde, 41. günde ve ilk yıl içinde 2, 3, 4, 6, 9 ve 12. aylarda yapılır.'
                    ],
                    'relatedQuestions': match_questions(['aile hekimligi', 'lohusa', 'performans', 'izlem'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Aile hekimliğinde lohusalık izlem takvimi nasıldır?',
                        'Performansa tabi izlemlerde aksama olursa mevzuata göre ne olur?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 2. DECK: DİSMORFOLOJİDE GENETİK TERMİNOLOJİ
    # =========================================================================
    dis_trans = parse_transcript_file('Dismorfolojide_Genetik_Terminoloji_Transkript.md')
    if dis_trans:
        deck_id = 'learn-dismorfoloji-terminoloji'
        deck = {
            'id': deck_id,
            'title': 'Dismorfolojide Genetik Terminoloji',
            'shortTitle': 'Dismorfoloji Terminolojisi',
            'discipline': 'Tıbbi Genetik',
            'committee': 'Kurul 1 - Tıbbi Genetik (Dönem 3)',
            'instructor': 'Öğretim Üyesi',
            'audioFile': 'Dismorfolojide Genetik Terminoloji TBG.m4a',
            'audioDuration': '61.6 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'indigo',
            'matchedNoteId': 'note-476343950c',
            'matchedNoteTitle': '1)DİSMORFOLOJİDE GENETİK TERMİNOLOJİ',
            'overview': 'Dismorfolojinin temel morfolojik defektleri (Malformasyon, Deformasyon, Disrupsiyon, Displazi), Sendrom, Sekans ve Asosiasyon tanımları, majör/minör anomalilerin klinik ayrımı.',
            'highYieldPearls': dis_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Dismorfolojiye Giriş ve Temel Kavramlar',
                    'subtitle': 'Doğuştan Yapısal Kusurların İncelenmesi',
                    'badge': 'TEMEL GENETİK',
                    'badgeColor': 'indigo',
                    'professorAudioHighlight': {
                        'timestamp': '04:12',
                        'quote': 'Dismorfoloji; anormal formların bilimidir. Doğumsal yapısal defektleri inceler. Klinik genetikçinin en önemli görevi hastanın yüzüne ve vücuduna bakarak bu örüntüyü tanımaktır.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca dismorfolojide fenotipik gözlem ve doğru terminolojiyi kullanmanın tanıdaki belirleyici rolünü anlattı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Dismorfoloji Tanımı', 'desc': 'Embriyolojik gelişim sürecindeki sapmalar sonucu ortaya çıkan yapısal ve anatomik bozuklukları inceleyen bilim dalı.'},
                            {'title': 'Anomali Tipleri', 'desc': 'Kusurlar etki düzeyine göre Malformasyon, Deformasyon, Disrupsiyon ve Displazi olarak 4 ana kategoriye ayrılır.'},
                            {'title': 'Sıklık', 'desc': 'Canlı doğan bebeklerin %2-3\'ünde doğumda saptanan en az bir majör konjenital anomali bulunur.'}
                        ]
                    },
                    'spotPearls': [
                        'Dismorfolojik değerlendirmede 4 temel yapısal defekt: Malformasyon, Deformasyon, Disrupsiyon ve Displazi.',
                        'Yeni doğan her 100 bebekten 2-3\'ünde majör bir yapısal malformasyon saptanır.'
                    ],
                    'relatedQuestions': match_questions(['dismorfoloji', 'anomali', 'konjenital'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Dismorfolojik muayenede nelere dikkat edilmelidir?',
                        'Dismorfolojide 4 temel morfolojik defekt kategorisi nedir?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Malformasyon: İntrinsik Morfogenez Bozukluğu',
                    'subtitle': 'Hücresel Düzeyde Başlayan Primer Hata',
                    'badge': 'SINAV KLASİĞİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '12:45',
                        'quote': 'Malformasyon İNTRİNSİKTİR arkadaşlar! Yani baştan beri dokunun kendi genetik programında hata vardır. Dışarıdan bir baskı yoktur. Yarık dudak, yarık damak, konjenital kalp defektleri en tipik örnekleridir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca sınavda "intrinsik" kelimesinin malformasyonun anahtar sözcüğü olduğunu özellikle hatırlattı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Mekanizma', 'desc': 'Organ veya vücut bölgesinin oluşumu sırasında dokunun kendi iç gelişimsel potansiyelindeki primer aksaklık.'},
                            {'title': 'Zamanlama', 'desc': 'Embriyonik dönemde (ilk 8 hafta / organogenez evresinde) meydana gelir.'},
                            {'title': 'Klinik Örnekler', 'desc': 'Yarık dudak/damak, Nöral tüp defektleri (Spina bifida), Fallot tetralojisi, Polidaktili, Sindaktili.'}
                        ],
                        'table': {
                            'title': 'Sık Karşılaşılan Malformasyonlar',
                            'headers': ['Malformasyon', 'Embriyolojik Hata', 'Genetik / Çevresel Risk'],
                            'rows': [
                                ['Nöral Tüp Defekti', 'Nöral tüpün 28. günde kapanamaması', 'Folik asit eksikliği, çok genli kalıtım'],
                                ['Yarık Dudak/Damak', 'Maksiller ve mediyal nazal çıkıntı birleşme hatası', 'Multifaktöriyel kalıtım'],
                                ['Ventriküler Septal Defekt (VSD)', 'İnterventriküler septum kapanma defekti', 'Trizomiler (21, 18, 13), teratojenler']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Malformasyon = İntrinsik (yapısal/genetik) primer gelişim hatası.',
                        'Malformasyonlar organogenez evresinde (ilk 8 hafta) meydana gelir ve geri dönüşümsüzdür.',
                        'En sık rastlanan malformasyonlar: Konjenital kalp hastalıkları ve nöral tüp defektleridir.'
                    ],
                    'relatedQuestions': match_questions(['malformasyon', 'yarik dudak', 'intrinsik', 'spina bifida'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Malformasyon ile deformasyon arasındaki en temel fark nedir?',
                        'Yarık dudak ve damak embriyolojik olarak hangi haftada oluşur?'
                    ]
                },
                {
                    'slideNumber': 3,
                    'title': 'Deformasyon vs Disrupsiyon: Ekstrinsik Mekanizmalar',
                    'subtitle': 'Mekanik Kuvvetler ve Vasküler Yıkımlar',
                    'badge': 'AYIRICI TANI TUZAĞI',
                    'badgeColor': 'amber',
                    'professorAudioHighlight': {
                        'timestamp': '21:30',
                        'quote': 'Deformasyon mekanik güçtür! Uterus daralır, oligohidramnioz olur, fetüs sıkışır; ayak çarpılır (clubfoot). Doğumdan sonra düzelme şansı vardır. Ama disrupsiyon yıkımdır; amniyotik bant parmağı koparır!',
                        'emphasisType': 'pearl',
                        'note': 'Hoca deformasyonun mekanik/dönüşümlü, disrupsiyonun ise yıkıcı/amputasyon yapıcı farkına odaklandı.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'Deformasyon ve Disrupsiyon Karşılaştırması',
                            'headers': ['Özellik', 'Deformasyon', 'Disrupsiyon'],
                            'rows': [
                                ['Temel Neden', 'Ekstrinsik anormal mekanik bası/kuvvet', 'Önceden normal dokunun dış etkenle yıkımı'],
                                ['Doku Başlangıcı', 'Normal doku ve organ taslağı', 'Tamamen normal gelişmiş doku'],
                                ['Tipik Etkenler', 'Oligohidramnioz, uterus anomalisi, çoğul gebelik', 'Amniyotik bantlar, iskemi, teratojen, enfeksiyon'],
                                ['Prognoz / Düzelme', 'Fizyoterapi/alçı ile düzelebilir (reversible)', 'Kalıcı doku kaybı / amputasyon (irreversible)'],
                                ['Klasik Örnek', 'Pes ekinovarus (clubfoot), kalça çıkığı', 'Amniyotik bant amputasyonu, barsak atrezisi']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Deformasyon: Mekanik kuvvetlere bağlı şekil bozukluğudur, doku normaldir ve doğum sonrası düzelebilir.',
                        'Disrupsiyon: Önceden normal olan dokunun vasküler, mekanik veya enfektif yıkımıdır (Örn: Amniyotik bant amputasyonu).',
                        'Potter sekansındaki basık burun ve clubfoot tipik bir DEFORMASYONDUR.'
                    ],
                    'relatedQuestions': match_questions(['deformasyon', 'disrupsiyon', 'amniyotik bant', 'pes ekinovarus'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Amniyotik bant sendromu neden bir disrupsiyondur?',
                        'Oligohidramnioz fetüste hangi deformasyonlara yol açar?'
                    ]
                },
                {
                    'slideNumber': 4,
                    'title': 'Displazi: Hücresel Organizasyon Bozukluğu',
                    'subtitle': 'Doku Düzeyinde Hatalı Diferansiyasyon',
                    'badge': 'HÜCRESEL PATOLOJİ',
                    'badgeColor': 'purple',
                    'professorAudioHighlight': {
                        'timestamp': '28:15',
                        'quote': 'Displazi dendiğinde aklınıza spesifik bir doku tipi gelecek: kemik displazileri, ektodermal displazi. Hücrelerin doku içindeki organizasyonu ve dizilimi bozulmuştur. Akondroplazi FGFR3 mutasyonuyla en ünlü örnektir.',
                        'emphasisType': 'clinical_tip',
                        'note': 'Hoca displazinin tek bir organı değil, vücuttaki o dokunun bulunduğu tüm sahaları etkileyebileceğini belirtti.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Displazi Tanımı', 'desc': 'Hücrelerin doku içerisindeki anormal organizasyonu veya hücre mimarisinin fonksiyonel bozukluğudur.'},
                            {'title': 'Kalıtım Deseni', 'desc': 'Çoğunlukla tek gen mutasyonlarına (Otozomal dominant vb.) bağlı olarak ortaya çıkar.'},
                            {'title': 'Klasik Örnek: Akondroplazi', 'desc': 'FGFR3 gen mutasyonu sonucu kıkırdak proliferasyonunun durması ve rizomelik ekstremite kısalığı.'},
                            {'title': 'Osteogenezis İmperfekta', 'desc': 'Tip 1 kollajen sentez defektine bağlı kemik kırılganlığı ve mavi sklera tablosu.'}
                        ]
                    },
                    'spotPearls': [
                        'Displazi = Hücrelerin belirli bir doku türünde (kemik, kıkırdak, deri vb.) anormal organizasyonudur.',
                        'Akondroplazi ve Thanatoforik displazi FGFR3 gen mutasyonuna bağlı iskelet displazileridir.',
                        'Displaziler embriyonik döneme hapsolmaz, doğum sonrasında da doku büyüdükçe etkileri devam eder.'
                    ],
                    'relatedQuestions': match_questions(['displazi', 'akondroplazi', 'fgfr3', 'iskelet'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Displazinin diğer yapısal anomalilerden farkı nedir?',
                        'FGFR3 geni ve akondroplazinin klinik bulguları nelerdir?'
                    ]
                },
                {
                    'slideNumber': 5,
                    'title': 'Sekans vs Sendrom vs Asosiasyon',
                    'subtitle': 'Çoklu Anomalilerin Sınıflandırılması ve Tanı Mantığı',
                    'badge': '⭐ HOCA VURGUSU: SINAVIN EN ÇOK SORULAN YERİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '36:40',
                        'quote': 'Buraya yıldız koyun! Sekans, sendrom ve asosiasyon farkını bilmeyen genetik sınavından geçemez. Bir tek primer hata domino taşı gibi diğerlerini deviriyorsa buna SEKANS diyoruz. Potter sekansı buna en güzel örnektir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca domino taşı analojisi ile sekans kavramını ve VACTERL asosiasyonunu sınavın garanti soruları olarak açıkladı.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'Çoklu Anomali Örüntüleri',
                            'headers': ['Kavram', 'Tanım Mekanizması', 'Klasik Klinik Örnek'],
                            'rows': [
                                ['Sekans (Sequence)', 'Tek bir primer anomalinin zincirleme sonuçları (Kaskad)', 'Potter Sekansı (Bilateral renal agenezi -> Oligohidramnioz -> Akciğer hipoplazisi + Clubfoot)'],
                                ['Sendrom (Syndrome)', 'Tek bir ortak etyolojiye (kromozom/gen) bağlı birden çok organda tutulum', 'Down Sendromu (Trizomi 21), Marfan Sendromu (FBN1)'],
                                ['Asosiasyon (Association)', 'Tesadüften daha sık bir arada görülen fakat nedeni henüz bilinmeyen anomali grubu', 'VACTERL Asosiasyonu (Vertebral, Anal, Kardiyak, TE fistül, Renal, Limb)']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Sekans: Tek bir primer olay başlatır, gerisi zincirleme gelişir (Örn: Potter sekansı, Pierre Robin sekansı).',
                        'Sendrom: Birden fazla sistem tutulur ve ortak bir genetik/çevresel neden vardır (Örn: Turner, Down, Edward).',
                        'Asosiasyon: İstatistiksel birlikteliktir, ortak bir neden veya sekans kanıtlanmamıştır (Örn: VACTERL/VATER).'
                    ],
                    'relatedQuestions': match_questions(['sekans', 'sendrom', 'asosiasyon', 'potter', 'vacterl'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Potter sekansında zincirleme olaylar nasıl gelişir?',
                        'VACTERL asosiasyonunun bileşenleri nelerdir?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 3. DECK: İZOLASYON YÖNTEMLERİ
    # =========================================================================
    iz_trans = parse_transcript_file('Izolasyon_Yontemleri_Transkript.md')
    if iz_trans:
        deck_id = 'learn-izolasyon-yontemleri'
        deck = {
            'id': deck_id,
            'title': 'İzolasyon Yöntemleri ve Hastane Enfeksiyon Kontrolü',
            'shortTitle': 'İzolasyon Yöntemleri',
            'discipline': 'Enfeksiyon Hastalıkları',
            'committee': 'Kurul 1 - Enfeksiyon Hastalıkları (Dönem 3)',
            'instructor': 'Öğretim Üyesi',
            'audioFile': 'Enfeksiyon Hastalıkları 1.m4a',
            'audioDuration': '33.3 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'emerald',
            'matchedNoteId': 'note-e2df90f5dc',
            'matchedNoteTitle': '3)İzolasyon yöntemleri',
            'overview': 'Hastane enfeksiyonlarının önlenmesi, el hijyeni ve standart önlemler, bulaşma yoluna dayalı izolasyonlar (Temas, Damlacık, Solunum) ve sembolleri/renkleri.',
            'highYieldPearls': iz_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'İzolasyonun Temel Amacı ve Standart Önlemler',
                    'subtitle': 'Her Hastada İstisnasız Uygulanması Gereken Kurallar',
                    'badge': 'TEMEL ENFEKSİYON',
                    'badgeColor': 'emerald',
                    'professorAudioHighlight': {
                        'timestamp': '01:15',
                        'quote': 'Standart önlemler tanısı ne olursa olsun hastaneye yatan HER hastaya uygulanır. Kan, tüm vücut sıvıları, salgılar ve hasarlı deri potansiyel olarak bulaşıcı kabul edilir. En ucuz ve en etkili önlem el hijyenidir.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca standart önlemlerin tanı beklenmeksizin her hastaya uygulanmasının önemini anlattı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'El Hijyeninin 5 Endikasyonu (DSÖ)', 'desc': '1) Hastaya dokunmadan önce, 2) Temiz/aseptik işlemden önce, 3) Vücut sıvısı maruziyetinden sonra, 4) Hastaya dokunduktan sonra, 5) Hasta çevresindeki nesnelere dokunduktan sonra.'},
                            {'title': 'Kişisel Koruyucu Ekipman (KKE)', 'desc': 'Eldiven, önlük, maske ve yüz siperliği bulaş riskine göre seçilir.'},
                            {'title': 'Kesici-Delici Alet Güvenliği', 'desc': 'Kullanılmış enjektör iğneleri kesinlikle kılıfına tekrar takılmaz, doğrudan sarı tıbbi atık kutusuna atılır.'}
                        ]
                    },
                    'spotPearls': [
                        'Standart önlemler: Tanısı ne olursa olsun tüm hastalara uygulanır (Ter hariç tüm vücut sıvıları enfeksiyöz kabul edilir).',
                        'Hastane enfeksiyonlarını önlemede en etkili, en kolay ve en maliyet-etkin yöntem: Doğru el hijyenidir.'
                    ],
                    'relatedQuestions': match_questions(['standart onlem', 'el hijyeni', 'hastane enfeksiyon'], 'Enfeksiyon Hastalıkları', past_questions, 2),
                    'aiPromptSuggestions': [
                        'El hijyeninin 5 altın anı nedir?',
                        'Standart önlemler hangi vücut sıvılarını kapsar, hangisini kapsamaz?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Bulaşma Yoluna Dayalı İzolasyonlar ve Renk Kodları',
                    'subtitle': 'Temas, Damlacık ve Solunum İzolasyonlarının Karşılaştırması',
                    'badge': '⭐ HOCA VURGUSU: RENKLER VE MASKE TİPLERİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '08:40',
                        'quote': 'Sınavda sorarız: Hangi izolasyonda hangi renk ve sembol kullanılır, hangi maske takılır? Tüberkülozda N95 takılır, negatif basınç gerekir. Meningokokta cerrahi maske yeterlidir. Renkleri sakın karıştırmayın!',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca semboller (Kırmızı El, Mavi Çiçek, Sarı Yaprak), maske tipleri ve oda basınçlarının kesinlikle sınav sorusu olduğunu vurguladı.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'İzolasyon Tipleri & Kuralları Tablosu',
                            'headers': ['İzolasyon Tipi', 'Sembol & Renk', 'Partikül Boyutu', 'Gereken Maske & Oda', 'Örnek Hastalıklar / Etkenler'],
                            'rows': [
                                ['Temas İzolasyonu', 'Kırmızı El', 'Direkt/İndirekt temas', 'Önlük + Eldiven (Maske şart değil), Tek kişilik oda', 'VRE, MRSA, C. difficile, Acinetobacter, Uyuz'],
                                ['Damlacık İzolasyonu', 'Mavi Çiçek', '> 5 mikron (ağır damlacık)', 'Cerrahi Maske (1 metre mesafe), Normal oda', 'Meningokok, İnfluenza, Boğmaca, Kabakulak, Adenovirüs'],
                                ['Solunum (Hava Yolu)', 'Sarı Yaprak', '< 5 mikron (havada asılı)', 'N95 / FFP2 Maske, Negatif Basınçlı Oda (Hava dışarı atılır)', 'Akciğer Tüberkülozu, Kızamık, Suçiçeği, Yaygın Zona'],
                                ['Koruyucu (Ters)', 'Beyaz Melek / Kart', 'Hastayı koruma', 'Pozitif Basınçlı Oda, Steril önlük, HEPA filtre', 'Ağır nötropeni, Kemik iliği / Organ nakli alıcıları']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Kırmızı El = Temas İzolasyonu (VRE, MRSA, C. difficile). Önlük ve eldiven zorunludur.',
                        'Mavi Çiçek = Damlacık İzolasyonu (>5 µm). Cerrahi maske yeterlidir, hasta ile 1 metre mesafe korunmalıdır.',
                        'Sarı Yaprak = Solunum / Hava Yolu İzolasyonu (<5 µm). N95/FFP2 maske ve NEGATİF basınçlı oda şarttır (Tüberküloz, Kızamık, Suçiçeği).',
                        'Negatif basınçlı oda: Havanın koridora kaçmasını önler. Pozitif basınçlı oda: Ters izolasyonda bağışıklığı baskılanmış hastaya dışarıdan mikrop girmesini önler.'
                    ],
                    'relatedQuestions': match_questions(['temas izolasyonu', 'damlacik', 'solunum izolasyonu', 'n95', 'tüberküloz'], 'Enfeksiyon Hastalıkları', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Tüberkülozlu hastaya yaklaşırken neden cerrahi maske yetersizdir?',
                        'Clostridium difficile enfeksiyonunda alkollü el antiseptiği neden yetersizdir?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 4. DECK: SALGIN HASTALIKLARDA KONTROL VE KORUNMA
    # =========================================================================
    sg_trans = parse_transcript_file('Halk_Sagligi_-_Salgin_Hastaliklarda_Kontrol_ve_Korunma_Transkript.md')
    if sg_trans:
        deck_id = 'learn-salgin-hastaliklar'
        deck = {
            'id': deck_id,
            'title': 'Halk Sağlığı - Salgın Hastalıklarda Kontrol ve Korunma',
            'shortTitle': 'Salgın Hastalıklar',
            'discipline': 'Halk Sağlığı',
            'committee': 'Kurul 1 - Halk Sağlığı (Dönem 3)',
            'instructor': 'Uzm. Dr. Erkay Nacar',
            'audioFile': 'Halk Sağlığı Giriş Dersi.m4a',
            'audioDuration': '39.9 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'sky',
            'matchedNoteId': 'note-86e7d188a4',
            'matchedNoteTitle': "4)'Salgın Hastalıklarda Kontrol ve Korunma'",
            'overview': 'Salgın (epidemi) dinamikleri, bulaşma zinciri bileşenleri (Kaynak, Bulaşma Yolu, Duyarlı Kişi), salgın inceleme basamakları, filyasyon ve karantina prensipleri.',
            'highYieldPearls': sg_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Bulaşıcı Hastalıkların Bulaş Zinciri',
                    'subtitle': 'Hastalık Yayılımının 3 Temel Halkası',
                    'badge': 'EPİDEMİYOLOJİ ÇEKİRDEĞİ',
                    'badgeColor': 'sky',
                    'professorAudioHighlight': {
                        'timestamp': '05:20',
                        'quote': 'Bulaşıcı bir hastalığı kontrol etmek istiyorsanız bu üç halkadan en az birini kırmak zorundasınız: Kaynak, bulaşma yolu ve duyarlı kişi. Aşı duyarlı kişiyi korur; filyasyon ve izolasyon kaynağı sınırlar.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca halk sağlığı müdahalelerinin daima bu 3 basamaktan birine hedeflendiğini anlattı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': '1. Kaynağa Yönelik Önlemler', 'desc': 'Erken tanı, bildirim, filyasyon (temaslı takibi), izolasyon ve hastanın tedavisi.'},
                            {'title': '2. Bulaşma Yoluna Yönelik Önlemler', 'desc': 'İçme suyu klorlaması, gıda güvenliği denetimleri, vektör (sivrisinek vb.) mücadelesi, havalandırma.'},
                            {'title': '3. Duyarlı Konağa Yönelik Önlemler', 'desc': 'Aktif bağışıklama (aşılar), pasif bağışıklama (serum/immünglobulin), kemoprofilaksi ve sağlık eğitimi.'}
                        ],
                        'table': {
                            'title': 'Bulaş Zinciri Kırma Stratejileri',
                            'headers': ['Halka', 'Halk Sağlığı Müdahalesi', 'Örnek Uygulama'],
                            'rows': [
                                ['Kaynak', 'Vaka bulma ve İzolasyon', 'COVID-19 pozitif hastanın evde karantinası'],
                                ['Bulaşma Yolu', 'Vektör ve Çevre Kontrolü', 'Sıtma için bataklık kurutma, kolerada su klorlama'],
                                ['Duyarlı Konak', 'Aşılama ve Profilaksi', 'Kızamık aşısı, meningokok temaslısına rifampisin']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Bulaş zincirinin 3 halkası: Kaynak -> Bulaşma Yolu -> Duyarlı Kişi.',
                        'İzolasyon: HASTA olan bireyin ayrılmasıdır. Karantina: ŞÜPHELİ/TEMASLI sağlıklı bireyin kuluçka süresince gözetimidir.',
                        'Duyarlı konağı korumanın en radikal ve kalıcı yolu kitlesel aşılamadır.'
                    ],
                    'relatedQuestions': match_questions(['bulas zinciri', 'filyasyon', 'karantina', 'vektor'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'İzolasyon ile karantina arasındaki fark nedir?',
                        'Salgın kontrolünde bulaşma yoluna yönelik önlemler nelerdir?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Salgın İnceleme Basamakları ve Atak Hızı',
                    'subtitle': 'Sahada Bir Salgın Nasıl Yönetilir?',
                    'badge': 'SAHA METODOLOJİSİ',
                    'badgeColor': 'emerald',
                    'professorAudioHighlight': {
                        'timestamp': '14:10',
                        'quote': 'Salgın var mı yok mu? İlk basamak tanının doğrulanması ve beklenen vaka sayısının aşılıp aşılmadığıdır. Atak hızı ise o salgına özgü insidanstır, paydada risk altındaki nüfus yer alır.',
                        'emphasisType': 'clinical_tip',
                        'note': 'Hoca salgın inceleme adımlarının sıralamasının sık sorulan bir klasik olduğunu belirtti.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': '1. Tanının Doğrulanması', 'desc': 'Klinik ve laboratuvar bulgularının teyidi.'},
                            {'title': '2. Salgının Varlığının Belirlenmesi', 'desc': 'Mevcut vaka sayısının o bölge ve mevsim için beklenen sınırın üzerine çıkması.'},
                            {'title': '3. Vaka Tanımının Yapılması', 'desc': 'Kesin, olası ve şüpheli vaka kriterlerinin netleştirilmesi.'},
                            {'title': '4. Atak Hızı Hesabı', 'desc': 'Atak Hızı = (Salgında hastalanan kişi sayısı / Risk altındaki toplam kişi sayısı) × 100'}
                        ]
                    },
                    'spotPearls': [
                        'Salgın incelemesinde ilk basamak: Tanının laboratuvar ve klinik olarak doğrulanmasıdır.',
                        'Atak hızı: Belirli bir salgın süresince risk altındaki grupta hastalığa yakalanma oranıdır (özel bir kümülatif insidans türüdür).',
                        'İkincil Atak Hızı: Primer vakayla temas edenler arasında kuluçka süresinde hastalananların oranıdır.'
                    ],
                    'relatedQuestions': match_questions(['salgin basamaklari', 'atak hizi', 'ikincil atak', 'vaka tanimi'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Atak hızı ile ikincil atak hızı arasındaki fark nedir?',
                        'Salgın eğrisinden (epidemiyolojik eğri) bulaş türü nasıl anlaşılır?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 5. DECK: HALK SAĞLIĞI TARİHÇESİ VE KORUYUCU HEKİMLİK
    # =========================================================================
    th_trans = parse_transcript_file('Halk_Sagligi_Tarihcesi_Transkript.md')
    if th_trans:
        deck_id = 'learn-halk-sagligi-tarihcesi'
        deck = {
            'id': deck_id,
            'title': 'Halk Sağlığı Tarihçesi ve Sağlık Hizmetlerinin Sosyalleştirilmesi',
            'shortTitle': 'Halk Sağlığı Tarihçesi',
            'discipline': 'Halk Sağlığı',
            'committee': 'Kurul 1 - Halk Sağlığı (Dönem 3)',
            'instructor': 'Öğretim Üyesi',
            'audioFile': 'Halk Saülığı Tarihçesi.m4a',
            'audioDuration': '24.2 dk',
            'confidence': '%90 Doğrulandı',
            'themeColor': 'sky',
            'matchedNoteId': 'note-e947c6e0b3',
            'matchedNoteTitle': '1)Halk SağlığıTarihçesi',
            'overview': 'Dünya ve Türkiye halk sağlığı tarihi, John Snow ve Broad Street kolerası, Alma-Ata Bildirgesi (1978), Dr. Refik Saydam ve Prof. Dr. Nusret Fişek\'in 224 Sayılı Sosyalleştirme Kanunu.',
            'highYieldPearls': th_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Dünya Halk Sağlığı Öncüleri ve Dönüm Noktaları',
                    'subtitle': 'Modern Epidemiyolojinin Doğuşu',
                    'badge': 'TARİHİ KİLOMETRE TAŞLARI',
                    'badgeColor': 'sky',
                    'professorAudioHighlight': {
                        'timestamp': '03:15',
                        'quote': 'John Snow epidemiyolojinin babasıdır. 1854 Londra kolera salgınında etken bilinmiyorken harita üzerinde vakaları işaretleyerek Broad Street su pompasının kolunu söktürmüştür. Bu halk sağlığının en çarpıcı müdahalesidir.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca John Snow\'un Broad Street su pompası vakasının epidemiyolojinin temeli olduğunu belirtti.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'John Snow (1854)', 'desc': 'Koleranın suyla bulaştığını haritalama yöntemiyle kanıtlayan modern epidemiyolojinin kurucusu.'},
                            {'title': 'Edward Jenner (1796)', 'desc': 'Çiçek aşısını geliştirerek kitlesel eradikasyonun temelini atan bilim insanı.'},
                            {'title': 'Robert Koch & Louis Pasteur', 'desc': 'Miasma (pis hava) teorisini yıkarak mikrop teorisini (Germ Theory) ispatladılar.'},
                            {'title': 'Alma-Ata Konferansı (1978)', 'desc': 'DSÖ ve UNICEF öncülüğünde "2000 Yılında Herkese Sağlık" hedefi ve Temel Sağlık Hizmetleri (TSH) felsefesi ilan edildi.'}
                        ]
                    },
                    'spotPearls': [
                        'Modern epidemiyolojinin babası: John Snow (1854 Londra Kolera Salgını - Broad Street Pompası).',
                        'İlk aşı: 1796\'da Edward Jenner tarafından çiçek hastalığına (Variola) karşı geliştirilmiştir.',
                        'Alma-Ata Bildirgesi (1978): Temel Sağlık Hizmetleri (TSH) yaklaşımının küresel manifestosudur.'
                    ],
                    'relatedQuestions': match_questions(['john snow', 'edward jenner', 'alma ata', 'tarihce'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        'John Snow kolera salgınını mikroorganizma keşfedilmeden önce nasıl durdurdu?',
                        'Alma-Ata Bildirgesi\'nin temel sağlık hizmetleri ilkeleri nelerdir?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Türkiye\'de Halk Sağlığı ve 224 Sayılı Kanun',
                    'subtitle': 'Prof. Dr. Nusret Fişek ve Sağlık Ocakları Sistemi',
                    'badge': '⭐ HOCA VURGUSU: KURULUN EN BÜYÜK KLASİĞİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '12:50',
                        'quote': 'Türkiye halk sağlığının mimarı Prof. Dr. Nusret Fişek\'tir. 1961 yılında çıkarılan 224 Sayılı Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun dünyada örnek gösterilmiş bir modeldir. Sağlık ocağı entegre hizmet verir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca 224 Sayılı Kanun\'un ilkeleri (entegrasyon, sosyalleştirme, kademelendirme) hakkında her sınavda mutlaka soru geldiğini vurguladı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': '224 Sayılı Kanun (1961)', 'desc': 'Sağlık Hizmetlerinin Sosyalleştirilmesi Hakkında Kanun ile Türkiye genelinde köylere kadar uzanan sağlık ocakları kuruldu.'},
                            {'title': 'Entegre Sağlık Hizmeti', 'desc': 'Tedavi edici ve koruyucu sağlık hizmetleri aynı çatı (sağlık ocağı) altında birleştirildi.'},
                            {'title': 'Kademeli Sevk Zinciri', 'desc': 'Sağlık Ocağı (1. Basamak) -> Devlet Hastanesi (2. Basamak) -> Üniversite/İhtisas (3. Basamak).'},
                            {'title': 'Nüfusa ve Bölgeye Dayalı Hizmet', 'desc': 'Her sağlık ocağı sorumlu olduğu coğrafi alan ve kayıtlı nüfusun tüm sağlık kayıtlarını tutar.'}
                        ]
                    },
                    'spotPearls': [
                        'Türkiye\'de sağlık hizmetlerinin sosyalleştirilmesinin mimarı: Prof. Dr. Nusret Fişek.',
                        '1961 tarihli 224 Sayılı Kanun: Koruyucu ve tedavi edici hizmetleri entegre eden sağlık ocağı modelini kurmuştur.',
                        'Türkiye Cumhuriyeti\'nin ilk Sağlık Bakanı: Dr. Adnan Adıvar; uzun dönem bakanlık yapan ve Hıfzıssıhha\'yı kuran: Dr. Refik Saydam.'
                    ],
                    'relatedQuestions': match_questions(['224 sayili', 'nusret fisek', 'sosyallestirme', 'saglik ocagi'], 'Halk Sağlığı', past_questions, 2),
                    'aiPromptSuggestions': [
                        '224 Sayılı Kanun\'un getirdiği en önemli 4 ilke nedir?',
                        'Sağlık ocakları sisteminde sevk zinciri nasıl işliyordu?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 6. DECK: KROMOZOMAL HASTALIKLAR VE GENETİK DANIŞMA
    # =========================================================================
    kr_trans = parse_transcript_file('Kromozomal_Hastaliklar_ve_Genetik_Danisma_Transkript.md')
    if kr_trans:
        deck_id = 'learn-kromozomal-hastaliklar'
        deck = {
            'id': deck_id,
            'title': 'Kromozomal Hastalıklar ve Genetik Danışma',
            'shortTitle': 'Kromozomal Hastalıklar',
            'discipline': 'Tıbbi Genetik',
            'committee': 'Kurul 1 - Tıbbi Genetik (Dönem 3)',
            'instructor': 'Dr. Öğr. Üyesi Serap ARSLAN',
            'audioFile': 'TBG - Kromozom hastalıkları ve genetşk danışmanlık.m4a',
            'audioDuration': '81.7 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'indigo',
            'matchedNoteId': 'note-661ebdda0e',
            'matchedNoteTitle': '2)KROMOZOMAL HASTALIKLAR VE GENETİK DANIŞMA',
            'overview': 'Sayısal ve yapısal kromozom anomalileri, trizomiler (Down, Edwards, Patau), gonozom anomalileri (Turner, Klinefelter), mikrodelesyon sendromları ve genetik danışma ilkeleri.',
            'highYieldPearls': kr_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Sayısal Kromozom Anomalileri ve Otozomal Trizomiler',
                    'subtitle': 'Down, Edwards ve Patau Sendromlarının Karşılaştırması',
                    'badge': 'KLİNİK GENETİK ÇEKİRDEĞİ',
                    'badgeColor': 'indigo',
                    'professorAudioHighlight': {
                        'timestamp': '14:20',
                        'quote': 'Trizomi 21 yaşla birlikte en çok artan aneuploididir. Serbest trizomi %95 oranında maternal mayoz 1 ayrılmama (nondisjunction) hatasıdır. Robertsonian translokasyon ise ailevi tekrarlama riski taşır.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca serbest trizomide anne yaşının, translokasyonlu Down sendromunda ise ebeveyn karyotipinin belirleyici olduğunu anlattı.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'En Sık Görülen Otozomal Trizomiler',
                            'headers': ['Sendrom', 'Karyotip', 'Temel Klinik Bulgular', 'Ortalama Yaşam'],
                            'rows': [
                                ['Down Sendromu', '47,XX/XY,+21', 'Brakisefali, epikantus, simian çizgisi, AVSD, Hirschsprung, Alzheimer eğilimi', '50-60 yıl'],
                                ['Edwards Sendromu', '47,XX/XY,+18', 'Prominent oksiput, mikrognati, üst üste binen parmaklar (clenched hand), rocker-bottom ayak, VSD', '< 1 yıl (%90 ilk haftalarda)'],
                                ['Patau Sendromu', '47,XX/XY,+13', 'Holoprozensefali, mikroftalmi, yarık dudak/damak, postaksiyal polidaktili, skalp defekti (aplazia kutis)', '< 1 yıl (%95 ilk günlerde)']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Down Sendromu (Trizomi 21): En sık canlı doğan trizomidir. %95 nondisjunction (maternal mayoz I), %4 Robertsonian translokasyon.',
                        'Edwards Sendromu (Trizomi 18): Üst üste binen parmaklar (2 ve 5, 3 ve 4 üzerine biner) ve rocker-bottom ayak patognomoniktir.',
                        'Patau Sendromu (Trizomi 13): Holoprozensefali, mikroftalmi, yarık dudak-damak ve polidaktili triadı ile karakterizedir.'
                    ],
                    'relatedQuestions': match_questions(['down sendromu', 'trizomi', 'edwards', 'patau', 'nondisjunction'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Down sendromunda serbest trizomi ile Robertsonian translokasyon arasındaki tekrarlama riski farkı nedir?',
                        'Edwards sendromunun en tipik fizik muayene bulguları nelerdir?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Cinsiyet Kromozomu Anomalileri ve Karyotip Analizi',
                    'subtitle': 'Turner (45,X) ve Klinefelter (47,XXY) Sendromları',
                    'badge': 'GONADAL DİSGENEZİ',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '32:10',
                        'quote': 'Turner sendromu anne yaşıyla İLİŞKİSİZ tek aneuploididir! Genellikle babanın spermindeki X kaybından kaynaklanır. Aort koarktasyonu ve yele boyun çok tipiktir. Klinefelter ise boyu uzun, jinekomastili, azospermik erkektir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca Turner sendromunun anne yaşı ile ilgisiz olmasının sınavların en popüler şaşırtmacası olduğunu hatırlattı.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'Gonozomal Anöploidi Karşılaştırması',
                            'headers': ['Özellik', 'Turner Sendromu', 'Klinefelter Sendromu'],
                            'rows': [
                                ['Karyotip', '45,X (veya mozaik 45,X/46,XX)', '47,XXY (veya 48,XXXY)'],
                                ['Fenotip', 'Dişi', 'Erkek'],
                                ['Boy', 'Kısa boy (<150 cm)', 'Uzun boy, uzun ekstremiteler (öストrojenik yağ dağılımı)'],
                                ['Gonadlar', 'Çizgi (streak) gonadlar, primer amenore', 'Küçük, sert testisler, azospremi, infertilite'],
                                ['Kardiyovasküler', 'Aort koarktasyonu, biküspit aort kapağı', 'Mitral kapak prolapsusu, venöz tromboemboli riski'],
                                ['Anne Yaşı İlişkisi', 'YOK (Paternal mayoz hatası hakimdir)', 'VAR (Anne yaşı arttıkça risk artar)']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Turner Sendromu (45,X): Anne yaşı ile ilişkisizdir! Kısa boy, yele boyun (pterigium kolli), aort koarktasyonu ve primer amenore ile seyreder.',
                        'Klinefelter Sendromu (47,XXY): Anne yaşı ile ilişkilidir. Uzun boy, jinekomasti, küçük sert testisler, yüksek FSH/LH ve azospremi görülür.',
                        'Tek canlı doğabilen monozomi: Turner Sendromudur (45,X).'
                    ],
                    'relatedQuestions': match_questions(['turner', 'klinefelter', 'gonozom', 'aort koarktasyonu', 'jinekomasti'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Turner sendromu neden anne yaşıyla ilişkili değildir?',
                        'Klinefelter sendromunda hormon profili (FSH, LH, Testosteron) nasıldır?'
                    ]
                },
                {
                    'slideNumber': 3,
                    'title': 'Genetik Danışma Prensipleri ve Prenatal Tanı',
                    'subtitle': 'Non-Direktif Yaklaşım ve Risk Değerlendirmesi',
                    'badge': 'ETİK VE KLİNİK',
                    'badgeColor': 'emerald',
                    'professorAudioHighlight': {
                        'timestamp': '55:40',
                        'quote': 'Genetik danışmanın bir numaralı altın kuralı NON-DİREKTİF olmasıdır! Hekim asla aileye ne yapacağını söylemez, karar vermez; olasılıkları ve riskleri açıklar, kararı aileye bırakır.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca hekimin yönlendirici değil, bilgilendirici ve destekleyici konumda kalması gerektiğini vurguladı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Non-Direktif Yaklaşım', 'desc': 'Ailenin inanç, değer ve kararlarına tam saygı gösterilir. "Çocuğu aldırın" veya "doğurun" denmez.'},
                            {'title': 'Genetik Danışma Endikasyonları', 'desc': 'İleri anne yaşı (>=35), önceki çocukta anomali öyküsü, ailede akraba evliliği, tekrarlayan düşükler (>=2 abortus).'},
                            {'title': 'Prenatal İnvaziv Yöntemler', 'desc': 'Koryon Villus Örneklemesi (KVS - 11-14. hafta), Amniyosentez (15-20. hafta), Kordosentez (20. haftadan sonra).'},
                            {'title': 'Non-İnvaziv Prenatal Test (NIPT)', 'desc': 'Anne kanındaki serbest fetal DNA (cffDNA) analizi ile trizomi taraması (kesin tanı değil taramadır).'}
                        ]
                    },
                    'spotPearls': [
                        'Genetik danışma NON-DİREKTİF (yönlendirici olmayan) ilkeyle verilir.',
                        'Koryon Villus Örneklemesi (KVS) en erken uygulanan invaziv yöntemdir (11-14. hafta).',
                        'NIPT bir tarama testidir; pozitif çıkarsa amniyosentez ile karyotip doğrulaması şarttır.'
                    ],
                    'relatedQuestions': match_questions(['genetik danisma', 'non-direktif', 'amniyosentez', 'kvs', 'nipt'], 'Tıbbi Genetik', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Non-direktif genetik danışma ne demektir ve hekimin sınırları nelerdir?',
                        'KVS ile amniyosentez arasındaki uygulama haftası ve risk farkları nelerdir?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # =========================================================================
    # 7. DECK: ÜRİNER SİSTEM OBSTRÜKSİYONLARI VE EĞİLİMLERİ
    # =========================================================================
    ur_trans = parse_transcript_file('Uriner_Sistem_Obstruksiyonlari_ve_Egilimleri_Transkript.md')
    if ur_trans:
        deck_id = 'learn-uriner-obstruksiyon'
        deck = {
            'id': deck_id,
            'title': 'Üriner Sistem Obstrüksiyonları, Patofizyoloji ve Tedavi',
            'shortTitle': 'Üriner Obstrüksiyon',
            'discipline': 'Üroloji',
            'committee': 'Kurul 1 - Üroloji (Dönem 3)',
            'instructor': 'Öğretim Üyesi',
            'audioFile': 'Üoloji.m4a',
            'audioDuration': '49.7 dk',
            'confidence': '%95 Doğrulandı',
            'themeColor': 'amber',
            'matchedNoteId': 'note-dfc1077833',
            'matchedNoteTitle': '1)Üriner Obstrüksiyon; Patofizyoloji, Klinik ve Tedavi',
            'overview': 'Üriner obstrüksiyon etyolojisi (intrinsik/ekstrinsik), böbrek hemodinamiği ve tübüler fonksiyon bozuklukları, renal kolik, tanı modaliteleri (USG, BT) ve acil dekompresyon (DJ stent, PCN).',
            'highYieldPearls': ur_trans['pearls'],
            'slides': [
                {
                    'slideNumber': 1,
                    'title': 'Üriner Obstrüksiyonun Etyolojisi ve Sınıflaması',
                    'subtitle': 'İntrinsik ve Ekstrinsik Nedenlerin Ayrımı',
                    'badge': 'ETYOLOJİK AYRIM',
                    'badgeColor': 'amber',
                    'professorAudioHighlight': {
                        'timestamp': '06:15',
                        'quote': 'Üriner obstrüksiyonu lümenin içinden mi kaynaklanıyor yoksa dışarıdan bası mı yapıyor diye ikiye ayırıyoruz. Genç erişkinde en sık intrinsik neden taştır (ürolitiyazis). Yaşlı erkekte ise BPH ve prostat kanseri ekstrinsik basıdır.',
                        'emphasisType': 'pearl',
                        'note': 'Hoca yaş gruplarına göre en sık obstrüksiyon nedenlerinin sınavda vaka olarak sorulduğunu ifade etti.'
                    },
                    'coreContent': {
                        'table': {
                            'title': 'Etyolojik Sınıflama',
                            'headers': ['Kategori', 'Gelişim Mekanizması', 'Sık Karşılaşılan Nedenler'],
                            'rows': [
                                ['İntrinsik Nedenler (Lümen İçi)', 'Üriner traktüsün kendi lümeni içindeki tıkanıklık', 'Böbrek/üreter taşı (en sık), ürotelyal tümör, kan pıhtısı, papiller nekroz döküntüsü, UPJ darlık'],
                                ['Ekstrinsik Nedenler (Dıştan Bası)', 'Komşu organ veya dokuların üretere/mesaneye basısı', 'Benign Prostat Hiperplazisi (BPH), Prostat Ca, Serviks/Kolon Ca, Retroperitoneal Fibrozis, Gebelik'],
                                ['Fonksiyonel / Nörojenik', 'Peristaltizm veya sfinkter koordinasyon kaybı', 'Nörojenik mesane, vezikoüreteral reflü (VUR), dissinerji']
                            ]
                        }
                    },
                    'spotPearls': [
                        'Genç ve orta yaş erişkinde akut tek taraflı obstrüksiyonun en sık nedeni: Üreteral taştır.',
                        'Yaşlı erkeklerde bilateral obstrüksiyon ve infravezikal tıkanıklığın en sık nedeni: BPH (Benign Prostat Hiperplazisi).',
                        'Çocuklarda konjenital obstrüksiyonun en sık nedeni: Üreteropelvik Bileşke (UPJ) darlığıdır.'
                    ],
                    'relatedQuestions': match_questions(['uriner obstruksiyon', 'urolitiyazis', 'bph', 'hidronefroz', 'upj'], 'Üroloji', past_questions, 2),
                    'aiPromptSuggestions': [
                        'İntrinsik ve ekstrinsik obstrüksiyon nedenleri nelerdir?',
                        'UPJ darlığı çocuklarda nasıl tanı alır?'
                    ]
                },
                {
                    'slideNumber': 2,
                    'title': 'Obstrüksiyon Patofizyolojisi: Hemodinamik ve Tübüler Fazlar',
                    'subtitle': 'Böbrek İçi Basınç Değişimleri ve GFR Kinetiği',
                    'badge': '⭐ HOCA VURGUSU: GRAFİK VE EVRE SORUSU',
                    'badgeColor': 'rose',
                    'professorAudioHighlight': {
                        'timestamp': '18:40',
                        'quote': 'Buraya dikkat edin: Akut tam tıkanmada ilk 1.5-2 saatte böbrek kan akımı ve üreter basıncı artar, çünkü prostaglandin E2 salınır. Ama 5. saatten sonra afferent arteriyol kasılır (tromboksan A2), renal kan akımı ve GFR hızla düşer!',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca üreter içi basınç ve renal kan akımının bifazik eğrisinin (PGE2 vs TxA2 / Anjiotensin II) fizyopatoloji sınavlarının gözdeleri olduğunu söyledi.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Faz 1: Erken Hiperemik Faz (0 - 1.5 Saat)', 'desc': 'Üreter basıncı tepe noktaya çıkar. Vazodilatatör prostaglandinler (PGE2, PGI2) salınır, renal kan akımı geçici olarak artar.'},
                            {'title': 'Faz 2: Geç İskemik Faz (> 5 Saat)', 'desc': 'Vazokonstriktör mediyatörler (Tromboksan A2, Anjiotensin II, Endotelin) devreye girer. Renal kan akımı ve üreter içi basınç düşer, doku iskemisi başlar.'},
                            {'title': 'Kronik Faz (> 24-48 Saat)', 'desc': 'GFR kalıcı olarak azalır. Medüller iskemi, tübüler konsantrasyon yeteneği kaybı ve parankim atrofisi (hidronefroz) gelişir.'}
                        ]
                    },
                    'spotPearls': [
                        'Akut üreter tıkanmasında ilk saatte renal kan akımını artıran mediyatör: Prostaglandin E2 (PGE2).',
                        '5. saatten sonra vazokonstriksiyon yaparak kan akımını ve GFR\'yi düşüren mediyatörler: Tromboksan A2 ve Anjiotensin II.',
                        'Obstrüksiyon giderilmediğinde ilk bozulan tübüler fonksiyon: İdrarı konsantre etme yeteneğidir (hipostenüri gelişir).'
                    ],
                    'relatedQuestions': match_questions(['hemodinami', 'gfr', 'prostaglandin', 'tromboksan', 'ureter basinci'], 'Üroloji', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Akut üreter obstrüksiyonunun bifazik hemodinamik yanıtı nasıldır?',
                        'Obstrüksiyon kalktıktan sonra görülen postobstrüktif diürez neden olur?'
                    ]
                },
                {
                    'slideNumber': 3,
                    'title': 'Klinik Belirtiler, Tanı ve Acil Tedavi Stratejileri',
                    'subtitle': 'Renal Kolik Ağrısından Perkütan Nefrostomiye',
                    'badge': 'ACİL ÜROLOJİ',
                    'badgeColor': 'emerald',
                    'professorAudioHighlight': {
                        'timestamp': '38:20',
                        'quote': 'Hastada tıkanıklık var VE ateş yüksekse bu ÜROLOJİK ACİLDİR! Piyonefroz gelişebilir, hasta saatler içinde ürosepsise girer. Hemen Double J stent veya perkütan nefrostomi (PCN) ile böbrek dekomprese edilmelidir.',
                        'emphasisType': 'direct_exam_warning',
                        'note': 'Hoca "Tıkanıklık + Enfeksiyon/Ateş = Acil Drenaj" kuralının hekimlik hayatının en kritik reflekslerinden biri olduğunu vurguladı.'
                    },
                    'coreContent': {
                        'keyBullets': [
                            {'title': 'Klinik: Renal Kolik', 'desc': 'Kapsül gerilmesine bağlı şiddetli, kıvrandırıcı, dalgalı yan ağrısı. Kasık ve genital bölgeye yayılır.'},
                            {'title': 'Görüntüleme: Kontrassız Helikal BT', 'desc': 'Üriner taş ve obstrüksiyonda altın standarttır (%99 duyarlılık). İndinavir taşı hariç tüm taşları gösterir.'},
                            {'title': 'Ultrasonografi (USG)', 'desc': 'Radyasyonsuzdur; gebelerde ve çocuklarda ilk tercihtir. Hidronefroz derecesini mükemmel gösterir.'},
                            {'title': 'Acil Dekompresyon Endikasyonları', 'desc': '1) Obstrüksiyona eşlik eden enfeksiyon/ürosepsis, 2) Tek böbrekli hastada tıkanıklık, 3) Tedaviye dirençli ağrı, 4) Akut böbrek hasarı.'}
                        ]
                    },
                    'spotPearls': [
                        'Üriner sistem taşları ve akut obstrüksiyonda altın standart tanı yöntemi: Kontrassız Helikal BT\'dir.',
                        'Gebelerde ve çocuklarda ilk tercih görüntüleme: Üriner Sistem USG\'dir.',
                        'Obstrükte + Enfekte böbrek mutlak bir ÜROLOJİK ACİLDİR: Bekletilmeden Double J (DJ) stent veya Perkütan Nefrostomi (PCN) uygulanmalıdır.'
                    ],
                    'relatedQuestions': match_questions(['renal kolik', 'kontrassiz bt', 'perkutan nefrostomi', 'double j', 'piyonefroz'], 'Üroloji', past_questions, 2),
                    'aiPromptSuggestions': [
                        'Akut renal kolik tedavisinde ilk tercih analjezik grubu neden NSAİİ\'lerdir?',
                        'Obstrükte enfekte böbrekte neden acil drenaj şarttır?'
                    ]
                }
            ]
        }
        deck['totalSlides'] = len(deck['slides'])
        deck['matchedPastQuestionsCount'] = sum(len(s.get('relatedQuestions', [])) for s in deck['slides'])
        decks.append(deck)

    # Save to JSON
    print(f"\nToplam {len(decks)} interaktif öğrenim destesi üretildi.")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(decks, f, ensure_ascii=False, indent=2)
    print(f"[Başarılı] Desteler kaydedildi: {OUTPUT_FILE}")

    # Build lightweight metadata list
    meta_list = []
    for d in decks:
        meta_list.append({
            'id': d['id'],
            'title': d['title'],
            'shortTitle': d['shortTitle'],
            'discipline': d['discipline'],
            'committee': d['committee'],
            'instructor': d['instructor'],
            'audioDuration': d['audioDuration'],
            'themeColor': d['themeColor'],
            'totalSlides': d['totalSlides'],
            'matchedPastQuestionsCount': d['matchedPastQuestionsCount'],
            'overview': d['overview'],
            'highYieldPearlsCount': len(d.get('highYieldPearls', []))
        })

    with open(OUTPUT_META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta_list, f, ensure_ascii=False, indent=2)
    print(f"[Başarılı] Deste indeks özeti kaydedildi: {OUTPUT_META_FILE}")

if __name__ == '__main__':
    build_all_decks()
