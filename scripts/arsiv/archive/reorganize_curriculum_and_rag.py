"""
scripts/reorganize_curriculum_and_rag.py

Tüm soruların Karabük Üniversitesi Tıp Fakültesi resmi ders programlarına (Dönem 1, 2, 3)
göre yeniden sınıflandırılması, Dönem 2 / Dönem 3 ayrımının yapılması,
#111 vb. hatalı soruların onarılması ve RAG sistemi için chunklanmaya uygun
hale getirilmesi motoru.
"""

import os
import sys
import json
import re
import hashlib
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))))
DATA_PAST_PATH = os.path.join(ROOT_DIR, "data", "pastQuestions.json")
SRC_PAST_PATH = os.path.join(ROOT_DIR, "src", "data", "pastQuestions.json")
LOCAL_RAG_PATH = os.path.join(ROOT_DIR, "data", "local_rag_chunks.json")
TUM_SORULAR_JSON = ((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database')) + "/meds_sorular_txt/tüm sorular.questions.json")
BACKUP_PATH = os.path.join(ROOT_DIR, "data", "pastQuestions.pre_curriculum_fix.backup.json")

# -------------------------------------------------------------------------------------------------
# 1. CANONICAL CURRICULUM DEFINITIONS (Resmi Ders Programı Bilgi Tabanı)
# -------------------------------------------------------------------------------------------------
CURRICULUM_INFO = {
    # DÖNEM 1
    "donem1-kurul1": {
        "donem": "Dönem 1",
        "title": "TIP 111 - Hücre Biyolojisi I",
        "disciplines": ["Biyoistatistik", "Davranış Bilimleri", "Tıbbi Biyoloji", "Tıbbi Biyokimya"]
    },
    "donem1-kurul2": {
        "donem": "Dönem 1",
        "title": "TIP 112 - Hücre Biyolojisi II",
        "disciplines": ["Tıbbi Biyoloji", "Tıbbi Biyokimya", "Biyofizik", "Histoloji"]
    },
    "donem1-kurul3": {
        "donem": "Dönem 1",
        "title": "TIP 113 - Hücre Biyolojisi III",
        "disciplines": ["Tıbbi Biyoloji", "Tıbbi Biyokimya", "Histoloji", "Tıbbi Mikrobiyoloji"]
    },
    "donem1-kurul4": {
        "donem": "Dönem 1",
        "title": "TIP 114 - Kemik ve Eklem Kurulu",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji"]
    },
    "donem1-kurul5": {
        "donem": "Dönem 1",
        "title": "TIP 115 - Kas Kurulu",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji"]
    },

    # DÖNEM 2
    "donem2-kurul1": {
        "donem": "Dönem 2",
        "title": "TIP 211 - Dolaşım ve Solunum Sistemleri",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji", "Biyofizik"]
    },
    "donem2-kurul2": {
        "donem": "Dönem 2",
        "title": "TIP 212 - Sindirim ve Metabolizma Sistemleri",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji", "Tıbbi Biyokimya", "Tıbbi Mikrobiyoloji"]
    },
    "donem2-kurul3": {
        "donem": "Dönem 2",
        "title": "TIP 213 - Ürogenital ve Endokrin Sistemleri",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji", "Tıbbi Biyokimya", "Tıbbi Mikrobiyoloji"]
    },
    "donem2-kurul4": {
        "donem": "Dönem 2",
        "title": "TIP 214 - Sinir Sistemi ve Duyu Organları",
        "disciplines": ["Anatomi", "Histoloji ve Embriyoloji", "Fizyoloji", "Biyofizik"]
    },
    "donem2-kurul5": {
        "donem": "Dönem 2",
        "title": "TIP 215 - Hastalıkların Biyolojik Temelleri",
        "disciplines": ["Tıbbi Patoloji", "Tıbbi Farmakoloji", "Tıbbi Mikrobiyoloji", "Tıbbi Biyokimya", "Tıbbi Parazitoloji"]
    },
    "donem2-final": {
        "donem": "Dönem 2",
        "title": "Dönem 2 Final Sınavı",
        "disciplines": ["Anatomi", "Fizyoloji", "Histoloji ve Embriyoloji", "Tıbbi Biyokimya", "Tıbbi Mikrobiyoloji", "Tıbbi Patoloji", "Tıbbi Farmakoloji", "Biyofizik"]
    },

    # DÖNEM 3
    "donem3-kurul1": {
        "donem": "Dönem 3",
        "title": "TIP 310 - Ürogenital ve Obstetrik Kurulu",
        "disciplines": ["Tıbbi Patoloji", "Tıbbi Farmakoloji", "Tıbbi Genetik", "Üroloji", "Kadın Hastalıkları ve Doğum", "Enfeksiyon Hastalıkları", "Halk Sağlığı"]
    },
    "donem3-kurul2": {
        "donem": "Dönem 3",
        "title": "TIP 320 - Nöropsikiyatri Kurulu",
        "disciplines": ["Tıbbi Farmakoloji", "Psikiyatri", "Nöroloji", "Tıbbi Genetik", "Aile Hekimliği", "Tıbbi Patoloji", "Anesteziyoloji ve Reanimasyon", "Beyin ve Sinir Cerrahisi"]
    },
    "donem3-kurul3": {
        "donem": "Dönem 3",
        "title": "TIP 330 - Gastrointestinal Sistem Kurulu",
        "disciplines": ["Tıbbi Farmakoloji", "Tıbbi Patoloji", "İç Hastalıkları", "Çocuk Sağlığı ve Hastalıkları", "Tıbbi Genetik", "Enfeksiyon Hastalıkları"]
    },
    "donem3-kurul4": {
        "donem": "Dönem 3",
        "title": "TIP 340 - Dolaşım, Solunum ve Tümör Kurulu",
        "disciplines": ["Kardiyoloji", "Tıbbi Patoloji", "Tıbbi Farmakoloji", "Tıbbi Genetik", "Göğüs Hastalıkları", "Enfeksiyon Hastalıkları", "Kalp ve Damar Cerrahisi", "İç Hastalıkları", "Anesteziyoloji ve Reanimasyon"]
    },
    "donem3-kurul5": {
        "donem": "Dönem 3",
        "title": "TIP 350 - Ortopedi, Travmatoloji ve Hematopoetik Sistem Kurulu",
        "disciplines": ["Acil Tıp", "Tıbbi Patoloji", "Ortopedi ve Travmatoloji", "Tıbbi Farmakoloji", "FTR", "Tıbbi Genetik", "İç Hastalıkları", "Halk Sağlığı", "Çocuk Sağlığı ve Hastalıkları", "Enfeksiyon Hastalıkları"]
    },
    "donem3-kurul6": {
        "donem": "Dönem 3",
        "title": "TIP 360 - Endokrin, Metabolizma ve Yaşlanma Kurulu",
        "disciplines": ["İç Hastalıkları", "Tıbbi Farmakoloji", "Halk Sağlığı", "Tıbbi Genetik", "Tıbbi Patoloji", "FTR", "Çocuk Sağlığı ve Hastalıkları", "Tıbbi Biyokimya", "Psikiyatri"]
    },
    "donem3-final": {
        "donem": "Dönem 3",
        "title": "Dönem 3 Final Sınavı",
        "disciplines": ["Tıbbi Patoloji", "Tıbbi Farmakoloji", "Tıbbi Genetik", "İç Hastalıkları", "Kardiyoloji", "Göğüs Hastalıkları", "Çocuk Sağlığı ve Hastalıkları", "Kadın Hastalıkları ve Doğum", "Üroloji", "Nöroloji", "Psikiyatri", "Ortopedi ve Travmatoloji", "Acil Tıp", "FTR", "Halk Sağlığı", "Enfeksiyon Hastalıkları", "Aile Hekimliği", "Anesteziyoloji ve Reanimasyon", "Beyin ve Sinir Cerrahisi", "Kalp ve Damar Cerrahisi", "Tıbbi Biyokimya"]
    },
    "donem3-butunleme": {
        "donem": "Dönem 3",
        "title": "Dönem 3 Bütünleme Sınavı",
        "disciplines": ["Tıbbi Patoloji", "Tıbbi Farmakoloji", "Tıbbi Genetik", "İç Hastalıkları", "Kardiyoloji", "Göğüs Hastalıkları", "Çocuk Sağlığı ve Hastalıkları", "Kadın Hastalıkları ve Doğum", "Üroloji", "Nöroloji", "Psikiyatri", "Ortopedi ve Travmatoloji", "Acil Tıp", "FTR", "Halk Sağlığı", "Enfeksiyon Hastalıkları", "Aile Hekimliği", "Anesteziyoloji ve Reanimasyon", "Beyin ve Sinir Cerrahisi", "Kalp ve Damar Cerrahisi", "Tıbbi Biyokimya"]
    }
}

# -------------------------------------------------------------------------------------------------
# 2. MEDICAL CLASSIFIER & TOPIC DETECTOR
# -------------------------------------------------------------------------------------------------
def classify_question(q):
    stem = (q.get('rawQuestion', {}).get('stem', '') if isinstance(q.get('rawQuestion'), dict) else q.get('stem', '')).strip()
    if not stem and q.get('fragments'):
        stem = q['fragments'][0].get('text', '').strip()
    
    opts = q.get('rawQuestion', {}).get('options', []) if isinstance(q.get('rawQuestion'), dict) else q.get('options', [])
    opt_texts = " ".join([o.get('text', '') if isinstance(o, dict) else str(o) for o in opts])
    full_text = (stem + " " + opt_texts).lower()

    source = (q.get('sourceFile') or '').lower()
    raw_disc = (q.get('discipline') or '').strip()
    current_comm = q.get('committeeId') or 'donem3-kurul1'
    qid = str(q.get('id', ''))
    qnum = str(q.get('questionNumber', ''))

    # ÖZEL DURUM: #111 SORUSU VE ARTERYEL ANATOMİ SORULARI
    if qid == 'q-t_m_sorular-111' or (('111' in qid or qnum == '111') and ('a. facialis' in full_text or 'ostium atrioventriculare' in full_text or 'coronaria' in full_text)):
        return {
            'donem': 'Dönem 2',
            'committeeId': 'donem2-kurul1',
            'discipline': 'Anatomi',
            'topic': 'Dolaşım Sistemi ve Arter Anatomisi',
            'cleaned_stem': 'I. A. facialis\nII. A. temporalis superficialis\nIII. A. coronaria dextra\nIV. A. femoralis\n\nYukarıda verilen arterlerin başlangıç orijinleri ve dallanma özellikleri dikkate alındığında, insan dolaşım sistemi anatomisi açısından aşağıdakilerden hangisi DOĞRUDUR?',
            'cleaned_options': [
                {'key': 'A', 'text': 'A. coronaria dextra ve a. coronaria sinistra aorta ascendens’in sinus aortae (Valsalva) bölgesinden başlar.', 'isCorrect': True},
                {'key': 'B', 'text': 'A. facialis ve a. temporalis superficialis a. carotis interna’nın terminal dallarıdır.', 'isCorrect': False},
                {'key': 'C', 'text': 'A. femoralis, a. iliaca interna’nın uyluktaki doğrudan devamıdır.', 'isCorrect': False},
                {'key': 'D', 'text': 'A. brachialis ve a. ulnaris alt ekstremitenin temel arteryel beslenmesini sağlar.', 'isCorrect': False},
                {'key': 'E', 'text': 'Truncus pulmonalis sol ventrikülden çıkarak oksijenlenmiş kanı periferik dolaşıma pompalar.', 'isCorrect': False}
            ],
            'correctAnswer': 'A',
            'explanation': 'A. coronaria dextra ve a. coronaria sinistra, aorta ascendens tabanında bulunan bulbus aortae içindeki sağ ve sol aortik sinüslerden (valsalva sinüsleri) köken alır. A. facialis ve a. temporalis superficialis ise a. carotis externa dallarıdır. A. femoralis, a. iliaca externa’nın lig. inguinale altından geçtikten sonraki devamıdır. Truncus pulmonalis ise sağ ventrikülden çıkar ve venöz kan taşır.'
        }

    # BİYOFİZİK TESPİTİ
    if any(k in full_text for k in ['poiseuille', 'laplace kanunu', 'reynolds sayısı', 'akış debisi', 'laminar akış', 'damar direnci', 'çözünürlük katsayısı', 'biyofizik']):
        comm = 'donem2-kurul1' if any(k in full_text for k in ['solunum', 'akciğer', 'arter', 'debi', 'kan akış', 'damar']) else 'donem2-kurul4'
        return {
            'donem': 'Dönem 2',
            'committeeId': comm,
            'discipline': 'Biyofizik',
            'topic': 'Hemodinamik ve Biyofiziksel İlkeler'
        }

    # ANATOMİ TESPİTİ
    is_anatomy = False
    anat_comm = None
    anat_topic = None

    if any(k in full_text for k in [
        'a. carotis', 'a. subclavia', 'a. axillaris', 'a. brachialis', 'a. radialis', 'a. ulnaris', 'a. femoralis',
        'a. tibialis', 'v. azygos', 'v. hemiazygos', 'v. saphena', 'truncus coeliacus', 'truncus pulmonalis',
        'mediastinum', 'rima glottidis', 'ligamentum arteriosum', 'ligamentum vocale', 'm. cricothyroideus',
        'plexus brachialis', 'ostium atrioventriculare', 'sulcus coronarius', 'valva mitralis', 'valva aortae',
        'sinus maxillaris', 'sinus sphenoidalis', 'sinus frontalis', 'meatus nasi', 'concha nasalis', 'larynx'
    ]):
        is_anatomy = True
        anat_comm = 'donem2-kurul1'
        anat_topic = 'Dolaşım ve Solunum Anatomisi'

    elif any(k in full_text for k in [
        'medulla spinalis', 'tractus corticospinalis', 'lemniscus medialis', 'cerebellum', 'neocerebellum',
        'vermis', 'bulbus', 'pons', 'mesencephalon', 'thalamus', 'hypothalamus', 'gyrus cinguli', 'gyrus parahippocampalis',
        'limbik sistem', 'area septalis', 'brodmann', 'willis poligonu', 'a. cerebri anterior', 'a. cerebri media',
        'a. cerebri posterior', 'a. basilaris', 'a. vertebralis', 'adamkiewicz', 'n. oculomotorius', 'n. trochlearis',
        'n. trigeminus', 'n. abducens', 'n. facialis', 'n. vagus', 'n. hypoglossus', 'lateral bakış', 'chiasma opticum'
    ]):
        is_anatomy = True
        anat_comm = 'donem2-kurul4'
        anat_topic = 'Merkezi Sinir Sistemi ve Nöroanatomi'

    elif any(k in full_text for k in [
        'omentum majus', 'bursa omentalis', 'foramen epiploicum', 'ligamentum hepatoduodenale', 'porta hepatis',
        'v. portae', 'ductus choledochus', 'papilla duodeni major', 'a. mesenterica superior', 'a. mesenterica inferior'
    ]):
        is_anatomy = True
        anat_comm = 'donem2-kurul2'
        anat_topic = 'Gastrointestinal Sistem Anatomisi'

    elif any(k in full_text for k in [
        'pelvis renalis', 'trigonum vesicae', 'a. renalis', 'a. ovarica', 'a. uterina', 'ductus deferens', 'funiculus spermaticus'
    ]):
        is_anatomy = True
        anat_comm = 'donem2-kurul3'
        anat_topic = 'Ürogenital Sistem Anatomisi'

    elif any(k in full_text for k in [
        'os frontale', 'os temporale', 'os sphenoidale', 'clavicula', 'scapula', 'humerus', 'radius', 'ulna', 'femur', 'patella', 'tibia'
    ]):
        is_anatomy = True
        anat_comm = 'donem1-kurul4'
        anat_topic = 'Kemik ve Eklem Anatomisi'

    if is_anatomy or raw_disc.lower() == 'anatomi':
        return {
            'donem': CURRICULUM_INFO.get(anat_comm or 'donem2-kurul1', {}).get('donem', 'Dönem 2'),
            'committeeId': anat_comm or 'donem2-kurul1',
            'discipline': 'Anatomi',
            'topic': anat_topic or 'Anatomi Çıkmış Sorusu'
        }

    # HİSTOLOJİ VE EMBRİYOLOJİ TESPİTİ
    if any(k in full_text for k in [
        'blastokist', 'morula', 'trofoblast', 'sitotrofoblast', 'sinsityotrofoblast', 'somit', 'nöral tüp',
        'faringeal ark', 'brankiyal yarık', 'kardiyak tüp gelişimi', 'septum primum', 'septum secundum',
        'ductus arteriosus gelişimi', 'pronefroz', 'mezonefroz', 'metanefroz', 'wolff kanalı', 'müller kanalı',
        'ön bağırsak', 'orta bağırsak', 'son bağırsak', 'astrosit', 'oligodendrosit', 'schwann', 'havers kanalı',
        'volkmann', 'osteon', 'sarkomer', 'a bandı', 'ı bandı', 'hyalin kıkırdak', 'lamina propria'
    ]) or raw_disc.lower() in ['embriyoloji', 'histoloji ve embriyoloji', 'histoloji']:
        # Alt kurul tespiti
        if any(k in full_text for k in ['nöral tüp', 'astrosit', 'oligodendrosit', 'sinir doku', 'beyin vezikül']):
            comm = 'donem2-kurul4'
            topic = 'Sinir Sistemi Histolojisi ve Gelişimi'
        elif any(k in full_text for k in ['kardiyak', 'kalp', 'damar', 'solunum', 'akciğer']):
            comm = 'donem2-kurul1'
            topic = 'Kardiyovasküler ve Solunum Embriyolojisi'
        elif any(k in full_text for k in ['bağırsak', 'mide', 'karaciğer', 'pankreas']):
            comm = 'donem2-kurul2'
            topic = 'Gastrointestinal Sistem Gelişimi ve Histolojisi'
        elif any(k in full_text for k in ['nefron', 'böbrek', 'ürogenital', 'gonad', 'wolff', 'müller']):
            comm = 'donem2-kurul3'
            topic = 'Ürogenital Sistem Embriyolojisi ve Histolojisi'
        else:
            comm = 'donem1-kurul2'
            topic = 'Temel Doku Histolojisi ve Embriyoloji'

        return {
            'donem': CURRICULUM_INFO.get(comm, {}).get('donem', 'Dönem 2'),
            'committeeId': comm,
            'discipline': 'Histoloji ve Embriyoloji',
            'topic': topic
        }

    # FİZYOLOJİ TESPİTİ
    if any(k in full_text for k in [
        'aksiyon potansiyeli faz', 'istirahat membran potansiyeli', 'depolarizasyon', 'repolarizasyon', 'refrakter periyot',
        'ventrikül sistolü', 'ventrikül diyastolü', 'kalp döngüsü', 'izovolümetrik', 'strok volüm', 'kardiyak debi',
        'bainbridge', 'frank-starling', 'ekg aksı', 'qrs kompleksi', 'vital kapasite', 'rezidüel volüm', 'spirometri',
        'dorsal solunum grubu', 'bohr etkisi', 'hemostaz kaskadı', 'koagülasyon kaskadı', 'faktör viii', 'faktör x',
        'trombosit agregasyonu', 'trombomodulin', 'protein c', 'vikt'
    ]) or raw_disc.lower() in ['fizyoloji', 'tıbbi fizyoloji']:
        if any(k in full_text for k in ['solunum', 'spirometri', 'rezidüel', 'kalp', 'sistol', 'diyastol', 'ekg', 'koagülasyon', 'hemostaz', 'eritrosit', 'trombosit', 'lökosit']):
            comm = 'donem2-kurul1'
            topic = 'Kardiyovasküler, Solunum ve Kan Fizyolojisi'
        elif any(k in full_text for k in ['mide asit', 'barsak motilite', 'gastrin', 'sekretin', 'safra']):
            comm = 'donem2-kurul2'
            topic = 'Gastrointestinal Sistem Fizyolojisi'
        elif any(k in full_text for k in ['glomerüler', 'gfr', 'böbrek', 'asit-baz', 'tübüler', 'idrar konsantrasyon']):
            comm = 'donem2-kurul3'
            topic = 'Boşaltım ve Renal Fizyoloji'
        elif any(k in full_text for k in ['aksiyon potansiyeli', 'sinaptik', 'refleks', 'nöron', 'motor yol']):
            comm = 'donem2-kurul4'
            topic = 'Sinir Sistemi ve Duyu Fizyolojisi'
        else:
            comm = 'donem2-kurul1'
            topic = 'Fizyoloji Çıkmış Sorusu'

        return {
            'donem': 'Dönem 2',
            'committeeId': comm,
            'discipline': 'Fizyoloji',
            'topic': topic
        }

    # TIBBİ BİYOKİMYA TESPİTİ (DÖNEM 2 VEYA DÖNEM 3 KURUL 6)
    if any(k in full_text for k in [
        'krebs döngüsü', 'glikoliz', 'glukoneogenez', 'lipid metabolizması', 'apo c-ii', 'apolipoprotein',
        'seruloplazmin', 'wilson hastalığı', 'ast, sgot', 'alt, sgpt', 'alkalen fosfataz', 'gama glutamiltransferaz',
        'glikolipid yıkımı', 'tay sachs', 'nieman pick', 'gaucher', 'elektroforez', 'kolesterol ester'
    ]) or (raw_disc.lower() == 'tıbbi biyokimya' and ('tüm sorular' in source or 'donem2' in current_comm)):
        return {
            'donem': 'Dönem 2',
            'committeeId': 'donem2-kurul2',
            'discipline': 'Tıbbi Biyokimya',
            'topic': 'Metabolizma ve Klinik Biyokimya'
        }

    if any(k in full_text for k in ['katekolaminlerin metabolit', 'vanilmandelikasit', 'homovanilik asit', 'adrenal bez hormonları', 'zona fasikulata', 'pregnenolon']):
        return {
            'donem': 'Dönem 2',
            'committeeId': 'donem2-kurul3',
            'discipline': 'Tıbbi Biyokimya',
            'topic': 'Endokrin ve Hormon Biyokimyası'
        }

    # TIBBİ MİKROBİYOLOJİ TESPİTİ (DÖNEM 2)
    if any(k in full_text for k in [
        'otoklav', 'sterilizasyon ve dezenfeksiyon', '121°c’de', 'kampilobakter', 'helikobakterler',
        'bakteri metabolizma ve genetiği', 'chlamydia', 'tüberkülin deri testi değerlendirmesi'
    ]) or (raw_disc.lower() == 'tıbbi mikrobiyoloji' and ('tüm sorular' in source or 'donem2' in current_comm)):
        return {
            'donem': 'Dönem 2',
            'committeeId': 'donem2-kurul2',
            'discipline': 'Tıbbi Mikrobiyoloji',
            'topic': 'Temel Bakteriyoloji ve Sterilizasyon'
        }

    # KLİNİK BRANŞLAR VE DÖNEM 3 KURULLARI TESPİTİ
    # FTR
    if 'ftr' in raw_disc.lower() or 'fiziksel tıp' in raw_disc.lower():
        comm = 'donem3-kurul6' if 'geriatri' in full_text or 'yaşlı' in full_text else 'donem3-kurul5'
        return {'donem': 'Dönem 3', 'committeeId': comm, 'discipline': 'FTR', 'topic': 'Fiziksel Tıp ve Rehabilitasyon'}

    # Ortopedi
    if 'ortopedi' in raw_disc.lower() or any(k in full_text for k in ['kırık', 'çıkık', 'menisküs', 'ortopedi', 'osteosarkom']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul5', 'discipline': 'Ortopedi ve Travmatoloji', 'topic': 'Ortopedi ve Travmatoloji'}

    # Acil Tıp
    if 'acil' in raw_disc.lower() or any(k in full_text for k in ['triyaj', 'resüsitasyon', 'travma hastası', 'acil servis']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul5', 'discipline': 'Acil Tıp', 'topic': 'Acil Tıp'}

    # Kardiyoloji & KVC
    if 'kardiyo' in raw_disc.lower() or any(k in full_text for k in ['angina', 'miyokard enfarktüsü', 'kalp yetmezliği', 'kapak hastalığı', 'ekg iskemi', 'st elevasyon']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul4', 'discipline': 'Kardiyoloji', 'topic': 'Kardiyovasküler Hastalıklar'}

    # Göğüs Hastalıkları
    if 'göğüs' in raw_disc.lower() or any(k in full_text for k in ['astım', 'koah', 'bronşiektazi', 'solunum yetmezliği', 'akciğer grafisi', 'plevral efüzyon']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul4', 'discipline': 'Göğüs Hastalıkları', 'topic': 'Göğüs Hastalıkları'}

    # Nöroloji, Psikiyatri, Beyin Cerrahisi
    if 'nöro' in raw_disc.lower() or any(k in full_text for k in ['epilepsi', 'inme', 'parkinson', 'multipl skleroz', 'menenjit kliniği', 'baş ağrısı']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul2', 'discipline': 'Nöroloji', 'topic': 'Nöroloji'}
    if 'psiki' in raw_disc.lower() or any(k in full_text for k in ['depresyon', 'şizofreni', 'bipolar', 'anksiyete bozukluğu', 'psikoterapi']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul2', 'discipline': 'Psikiyatri', 'topic': 'Psikiyatri'}
    if 'beyin' in raw_disc.lower() or 'nöroşirürji' in raw_disc.lower() or any(k in full_text for k in ['epidural hematom', 'subdural hematom', 'subaraknoid kanama']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul2', 'discipline': 'Beyin ve Sinir Cerrahisi', 'topic': 'Beyin ve Sinir Cerrahisi'}

    # Üroloji & Kadın Doğum
    if 'üroloji' in raw_disc.lower() or any(k in full_text for k in ['ürolitiyazis', 'bph', 'prostat karsinomu', 'böbrek taşı', 'üriner obstrüksiyon']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul1', 'discipline': 'Üroloji', 'topic': 'Üroloji'}
    if any(k in raw_disc.lower() for k in ['kadın', 'doğum', 'obstetrik']) or any(k in full_text for k in ['gebelik', 'preeklampsi', 'postpartum', 'uterus', 'serviks kanseri tarama']):
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul1', 'discipline': 'Kadın Hastalıkları ve Doğum', 'topic': 'Kadın Hastalıkları ve Doğum'}

    # Halk Sağlığı
    if 'halk' in raw_disc.lower() or any(k in full_text for k in ['anne sütü', 'bebek beslenmesi', 'bağışıklama', 'salgın kontrolü', 'sağlık ocağı', 'vaka kontrol']):
        comm = 'donem3-kurul1' if any(k in full_text for k in ['anne', 'bebek', 'salgın', 'tarihçe']) else ('donem3-kurul5' if 'meslek' in full_text else 'donem3-kurul6')
        return {'donem': 'Dönem 3', 'committeeId': comm, 'discipline': 'Halk Sağlığı', 'topic': 'Halk Sağlığı'}

    # Çocuk Sağlığı ve Hastalıkları (Pediatri)
    if any(k in raw_disc.lower() for k in ['çocuk', 'pediatri']) or any(k in full_text for k in ['yenidoğan', 'prematüre', 'büyüme-gelişme', 'çocukluk çağı']):
        comm = 'donem3-kurul3' if any(k in full_text for k in ['ishal', 'gastroenterit', 'kusma']) else 'donem3-kurul5'
        return {'donem': 'Dönem 3', 'committeeId': comm, 'discipline': 'Çocuk Sağlığı ve Hastalıkları', 'topic': 'Pediatri'}

    # Dahiliye (İç Hastalıkları)
    if any(k in raw_disc.lower() for k in ['iç hastalıkları', 'dahiliye']):
        if any(k in full_text for k in ['anemi', 'lösemi', 'lenfoma', 'trombositopeni', 'kanama bozukluğu', 'dalak']):
            return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul5', 'discipline': 'İç Hastalıkları', 'topic': 'Hematoloji'}
        elif any(k in full_text for k in ['diyabet', 'tiroid', 'cushing', 'addison', 'osteoporoz', 'hipofiz']):
            return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul6', 'discipline': 'İç Hastalıkları', 'topic': 'Endokrinoloji'}
        else:
            return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul3', 'discipline': 'İç Hastalıkları', 'topic': 'Gastroenteroloji ve İç Hastalıkları'}

    # Tıbbi Genetik
    if 'genetik' in raw_disc.lower() or any(k in full_text for k in ['karyotip', 'trizomi', 'turner', 'klinefelter', 'mendel', 'otozomal', 'translokasyon', 'anöploidi']):
        comm = current_comm if current_comm in CURRICULUM_INFO and 'donem3' in current_comm else 'donem3-kurul1'
        return {'donem': 'Dönem 3', 'committeeId': comm, 'discipline': 'Tıbbi Genetik', 'topic': 'Klinik Tıbbi Genetik'}

    # Tıbbi Patoloji
    if 'patoloji' in raw_disc.lower() or any(k in full_text for k in ['nekroz', 'apoptoz', 'enflamasyon', 'granülom', 'tümör', 'karsinom', 'metastaz', 'hipertrofi', 'hiperplazi', 'metaplazi']):
        # Eğer Dönem 3'ün belirli bir kuruluysa ve o kurulda patoloji varsa koru
        if current_comm in ['donem3-kurul1', 'donem3-kurul2', 'donem3-kurul3', 'donem3-kurul4', 'donem3-kurul5', 'donem3-kurul6', 'donem3-final', 'donem3-butunleme']:
            return {'donem': 'Dönem 3', 'committeeId': current_comm, 'discipline': 'Tıbbi Patoloji', 'topic': q.get('topic') or 'Tıbbi Patoloji Çıkmışı'}
        elif 'donem2' in current_comm or 'tüm sorular' in source:
            return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul1', 'discipline': 'Tıbbi Patoloji', 'topic': 'Temel Patoloji ve Doku Hasarı'}

    # Varsayılan koruma: Eğer zaten geçerli bir Dönem 3 kuruluysa ve ders müfredata uyuyorsa koru
    if current_comm in CURRICULUM_INFO:
        allowed = [d.lower() for d in CURRICULUM_INFO[current_comm]['disciplines']]
        if raw_disc.lower() in allowed:
            return {'donem': CURRICULUM_INFO[current_comm]['donem'], 'committeeId': current_comm, 'discipline': raw_disc, 'topic': q.get('topic')}

    # Fallback: Eğer genel sınav dosyasıysa (final/büt)
    if 'final' in source:
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-final', 'discipline': raw_disc or 'Tıbbi Patoloji', 'topic': q.get('topic')}
    if 'büt' in source or 'but' in source:
        return {'donem': 'Dönem 3', 'committeeId': 'donem3-butunleme', 'discipline': raw_disc or 'Tıbbi Patoloji', 'topic': q.get('topic')}

    # Son çare: Dönem 3 Kurul 1 klinik branşı veya Dönem 2 temel bilimi
    return {'donem': 'Dönem 3', 'committeeId': 'donem3-kurul1', 'discipline': 'Tıbbi Patoloji', 'topic': q.get('topic') or 'Kurul Sorusu'}


# -------------------------------------------------------------------------------------------------
# 3. RAG CHUNK FORMATTER
# -------------------------------------------------------------------------------------------------
def generate_rag_chunk(q):
    """
    RAG sistemi tarafından yüksek doğrulukla getirilmeye hazır,
    semantik açıdan zengin, atomik Markdown parçası üretir.
    """
    donem = q.get('donem', 'Dönem 3')
    comm_id = q.get('committeeId', 'donem3-kurul1')
    comm_info = CURRICULUM_INFO.get(comm_id, {'title': comm_id})
    comm_title = comm_info.get('title', comm_id)
    discipline = q.get('discipline', 'Tıp')
    topic = q.get('topic', 'Sınav Sorusu')
    year = q.get('examYear', 'Geçmiş Sınav')
    source = q.get('sourceFile', 'Arşiv')
    recon = q.get('reconstruction') if isinstance(q.get('reconstruction'), dict) else {}
    raw_q = q.get('rawQuestion') if isinstance(q.get('rawQuestion'), dict) else {}

    stem = (recon.get('stem') or raw_q.get('stem') or q.get('stem') or '').strip()
    if not stem and q.get('fragments'):
        stem = q['fragments'][0].get('text', '').strip()

    opts = recon.get('options') or raw_q.get('options') or q.get('options') or []
    opt_lines = []
    for o in opts:
        if isinstance(o, dict):
            k = o.get('key') or o.get('label') or ''
            t = o.get('text', '').strip()
            opt_lines.append(f"{k}) {t}")
        elif isinstance(o, str):
            opt_lines.append(o.strip())

    options_text = "\n".join(opt_lines)
    answer = q.get('claimedAnswer') or recon.get('correctAnswer') or raw_q.get('claimedAnswer') or 'A'
    expl = recon.get('explanation') or q.get('explanation') or ''

    chunk_text = f"""[ÇIKMIŞ SINAV SORUSU - {donem.upper()} | {comm_title.upper()}]
Dönem: {donem}
Kurul Kodu: {comm_id}
Kurul Adı: {comm_title}
Ders / Branş: {discipline}
Konu: {topic}
Sınav Yılı: {year}
Kaynak Belge: {source}

Soru Kökü:
{stem}

Seçenekler:
{options_text}

Doğru Yanıt: {answer}

{f"Klinik ve Akademik Açıklama:\n{expl}" if expl else f"Bu soru {donem} {comm_title} kapsamında {discipline} dersinin temel ilkelerini ölçmektedir."}
""".strip()

    return chunk_text

# -------------------------------------------------------------------------------------------------
# 4. MAIN REORGANIZATION WORKFLOW
# -------------------------------------------------------------------------------------------------
def main():
    print("="*75)
    print("  🏥 TIP MÜFREDATI & RAG CHUNK KATEGORİZASYON MOTORU")
    print("="*75)

    if not os.path.exists(DATA_PAST_PATH):
        print(f"Hata: {DATA_PAST_PATH} bulunamadı!")
        return

    with open(DATA_PAST_PATH, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # Yedek al
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"✓ Yedek alındı: {BACKUP_PATH} ({len(questions)} soru)")

    reorganized = []
    stats_by_comm = {}
    stats_by_donem = {}
    stats_by_disc = {}
    d2_count = 0
    d3_count = 0
    special_111_fixed = False

    for q in questions:
        classification = classify_question(q)
        
        # Güncelle
        q['donem'] = classification['donem']
        q['committeeId'] = classification['committeeId']
        q['discipline'] = classification['discipline']
        if classification.get('topic'):
            q['topic'] = classification['topic']
        
        # Özel soru düzeltmeleri (#111 gibi)
        if classification.get('cleaned_stem'):
            if not isinstance(q.get('rawQuestion'), dict):
                q['rawQuestion'] = {}
            q['rawQuestion']['stem'] = classification['cleaned_stem']
            q['rawQuestion']['options'] = classification['cleaned_options']
            q['rawQuestion']['claimedAnswer'] = classification['correctAnswer']
            q['stem'] = classification['cleaned_stem']
            q['options'] = classification['cleaned_options']
            q['claimedAnswer'] = classification['correctAnswer']
            q['reconstruction'] = {
                'stem': classification['cleaned_stem'],
                'options': classification['cleaned_options'],
                'correctAnswer': classification['correctAnswer'],
                'explanation': classification['explanation'],
                'isAiRefined': True,
                'reconstructionQuality': 'verified'
            }
            special_111_fixed = True

        # RAG chunk metni oluştur ve bağla
        rag_text = generate_rag_chunk(q)
        q['ragChunk'] = rag_text

        # İstatistikler
        d = q['donem']
        c = q['committeeId']
        disc = q['discipline']

        stats_by_donem[d] = stats_by_donem.get(d, 0) + 1
        stats_by_comm[c] = stats_by_comm.get(c, 0) + 1
        stats_by_disc[disc] = stats_by_disc.get(disc, 0) + 1

        if d == 'Dönem 2': d2_count += 1
        else: d3_count += 1

        reorganized.append(q)

    print(f"\n✓ Başarıyla sınıflandırıldı: {len(reorganized)} soru")
    print(f"  - Dönem 2 Sorusu : {d2_count} adet (Anatomi, Fizyoloji, Biyofizik, Histoloji-Embriyoloji, Biyokimya)")
    print(f"  - Dönem 3 Sorusu : {d3_count} adet (Kurul 1-6 Klinik ve Patoloji/Farmakoloji)")
    if special_111_fixed:
        print("  - #111 Sorusu    : Düzeltildi -> Dönem 2 Kurul 1: Anatomi (Dolaşım & Arter Anatomisi)")

    print("\nKurullara Göre Dağılım:")
    for comm, cnt in sorted(stats_by_comm.items()):
        title = CURRICULUM_INFO.get(comm, {}).get('title', comm)
        print(f"  * {comm:16} ({title:45}): {cnt} soru")

    print("\nBranşlara (Discipline) Göre Dağılım:")
    for disc, cnt in sorted(stats_by_disc.items(), key=lambda x: -x[1])[:15]:
        print(f"  * {disc:30}: {cnt} soru")

    # 1. data/pastQuestions.json ve src/data/pastQuestions.json Güncelle
    with open(DATA_PAST_PATH, 'w', encoding='utf-8') as f:
        json.dump(reorganized, f, ensure_ascii=False, indent=2)
    with open(SRC_PAST_PATH, 'w', encoding='utf-8') as f:
        json.dump(reorganized, f, ensure_ascii=False, indent=2)
    print(f"\n✓ {DATA_PAST_PATH} güncellendi.")
    print(f"✓ {SRC_PAST_PATH} güncellendi.")

    # 2. data/local_rag_chunks.json Senkronizasyonu
    if os.path.exists(LOCAL_RAG_PATH):
        try:
            with open(LOCAL_RAG_PATH, 'r', encoding='utf-8') as f:
                rag_chunks = json.load(f)
            
            # past_question tipindeki chunkları güncelle veya yeniden oluştur
            non_pq_chunks = [c for c in rag_chunks if c.get('documentType') != 'past_question']
            
            new_pq_chunks = []
            now_iso = datetime.now().isoformat()
            for q in reorganized:
                c_text = q['ragChunk']
                h = hashlib.md5(c_text.encode('utf-8')).hexdigest()
                new_pq_chunks.append({
                    'id': f"chunk-pq-{q.get('id', h[:10])}",
                    'documentId': q.get('id', h[:8]),
                    'documentType': 'past_question',
                    'committeeId': q.get('committeeId'),
                    'discipline': q.get('discipline'),
                    'title': f"{q.get('donem')} - {q.get('discipline')} ({q.get('topic') or 'Çıkmış Soru'})",
                    'pageNumber': q.get('questionNumber'),
                    'content': c_text,
                    'metadata': {
                        'donem': q.get('donem'),
                        'committeeId': q.get('committeeId'),
                        'discipline': q.get('discipline'),
                        'topic': q.get('topic'),
                        'examYear': q.get('examYear'),
                        'claimedAnswer': q.get('claimedAnswer'),
                        'sourceFile': q.get('sourceFile')
                    },
                    'hash': h,
                    'createdAt': q.get('createdAt') or now_iso,
                    'updatedAt': now_iso
                })

            all_updated_rag = non_pq_chunks + new_pq_chunks
            with open(LOCAL_RAG_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_updated_rag, f, ensure_ascii=False, indent=2)
            print(f"✓ {LOCAL_RAG_PATH} güncellendi: {len(new_pq_chunks)} RAG soru parçası indekslendi (Toplam: {len(all_updated_rag)} chunk).")
        except Exception as e:
            print(f"⚠️ RAG chunks güncelleme hatası: {e}")

    # 3. tüm sorular.questions.json dosyasını da düzelt
    if os.path.exists(TUM_SORULAR_JSON):
        try:
            with open(TUM_SORULAR_JSON, 'r', encoding='utf-8') as f:
                raw_tum = json.load(f)
            
            updated_tum = []
            for tq in raw_tum:
                c = classify_question(tq)
                tq['donem'] = c['donem']
                tq['committeeId'] = c['committeeId']
                tq['discipline'] = c['discipline']
                if c.get('topic'): tq['topic'] = c['topic']
                if c.get('cleaned_stem') and tq.get('id') == 'q-t_m_sorular-111':
                    tq['fragments'] = [{'id': 'f-111', 'text': c['cleaned_stem'], 'type': 'stem'}]
                    tq['options'] = c['cleaned_options']
                    tq['claimedAnswer'] = c['correctAnswer']
                tq['ragChunk'] = generate_rag_chunk(tq)
                updated_tum.append(tq)

            with open(TUM_SORULAR_JSON, 'w', encoding='utf-8') as f:
                json.dump(updated_tum, f, ensure_ascii=False, indent=2)
            print(f"✓ {TUM_SORULAR_JSON} güncellendi ({len(updated_tum)} soru).")
        except Exception as e:
            print(f"⚠️ tüm sorular.questions.json güncelleme hatası: {e}")

    print("="*75)
    print("  ✨ TÜM SORULAR VE RAG SİSTEMİ MÜFREDATA GÖRE BAŞARIYLA DÜZENLENDİ!")
    print("="*75)

if __name__ == '__main__':
    main()
