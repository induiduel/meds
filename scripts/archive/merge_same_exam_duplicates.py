#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
merge_same_exam_duplicates.py
-----------------------------------------------------------------------------
Bu script;
1. Birbiriyle eşleşen, birbirini tekrar eden veya birbirine aşırı benzeyip
   cevapları AYNI olan soruları tespit eder.
2. EĞER sorular AYNI SENE ve AYNI KURULDA sorulduysa:
   - Bunları mutlaka tek bir ana (master) soru altında BİRLEŞTİRİR (merge eder).
   - En kaliteli / redakte edilmiş versiyonu master seçer.
   - Diğer kopyaların ID, kaynak dosya (sourceFile) ve varyant bilgilerini
     ana sorunun `mergedQuestionIds`, `sourceFiles` ve `mergedVariants`
     alanlarına işler ve mükerrer kayıtları temizler.
3. EĞER sorular FARKLI KURULLARDA veya FARKLI SENELERDE sorulduysa:
   - Bu soruları ASLA silmez ve birleştirmez (veri tabanında kalırlar).
   - Çapraz referans (`crossExamReferences`) ve 'Tekrar Sorulan Soru' etiketi
     ekleyerek tıp fakültesi kurul sınavları arasındaki tarihsel tekrarı belgeler.
4. Zıt / çelişkili cevaplara sahip (örn: "hızlı etkili" vs "uzun etkili", 
   "Tifo" vs "Kolera", "minör" vs "majör") soruları ASLA birleştirmez.
=============================================================================
"""

import os
import re
import sys
import json
import shutil
import argparse
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict

# Windows konsolunda UTF-8 çıktı desteği
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ---------------------------------------------------------------------------
# TÜRKÇE VE METİN TEMİZLEME FONKSİYONLARI
# ---------------------------------------------------------------------------

def tr_lower(text: str) -> str:
    """Türkçe karakter duyarlı küçük harfe dönüştürme ve ASCII eşleme."""
    if not text:
        return ""
    t = (text.replace('İ', 'i')
             .replace('I', 'ı')
             .replace('Ö', 'o')
             .replace('ö', 'o')
             .replace('Ü', 'u')
             .replace('ü', 'u')
             .replace('Ş', 's')
             .replace('ş', 's')
             .replace('Ç', 'c')
             .replace('ç', 'c')
             .replace('Ğ', 'g')
             .replace('ğ', 'g')
             .lower()
             .replace('\u0307', '')
             .replace('\u0327', ''))
    return t

def clean_for_match(text: str) -> str:
    """Soru kökü veya seçenek metnini karşılaştırma için normalize eder."""
    if not text:
        return ""
    t = tr_lower(text)
    # Soru başı numaralandırmaları temizle: "1.", "25-", "Soru 14:", "a." vb.
    t = re.sub(r'^(?:soru\s*)?\d+[\.\)\-\:\s]+', '', t).strip()
    t = re.sub(r'^[a-e][\.\)\-\:\s]+', '', t).strip()
    # Sayfa sonu veya bölüm dipnotlarını temizle
    t = re.sub(r'(?:donem\s*\d|kurul\s*\d|enfeksiyon\s*hastaliklari|tibbi\s*patoloji|tibbi\s*farmakoloji|halk\s*sagligi).*$', '', t)
    # Alfanümerik dışındaki tüm karakterleri at
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

# Tıpta sık karşılaşılan zıt / çelişkili kavram çiftleri (farklı soru göstergesi)
ANTONYM_PAIRS = [
    ("minor", "major"),
    ("akut", "kronik"),
    ("artar", "azalir"),
    ("artis", "azalis"),
    ("hizli", "uzun"),
    ("hizli", "yavas"),
    ("benign", "malign"),
    ("pozitif", "negatif"),
    ("primer", "sekonder"),
    ("hipo", "hiper"),
    ("endojen", "ekzojen"),
    ("dogru", "yanlis"),
    ("komplike", "komplikeolmayan"),
    ("on", "arka"),
    ("anterior", "posterior"),
    ("drift", "shift")
]

def has_antonym_contradiction(text1: str, text2: str) -> bool:
    """İki metin arasında zıt tıbbi kavram çelişkisi olup olmadığını denetler."""
    t1 = clean_for_match(text1)
    t2 = clean_for_match(text2)
    for w1, w2 in ANTONYM_PAIRS:
        if (w1 in t1 and w2 in t2) or (w2 in t1 and w1 in t2):
            return True
    return False

# ---------------------------------------------------------------------------
# KURUL VE SENE NORMALİZASYONU
# ---------------------------------------------------------------------------

def normalize_committee(committee_id: str, source_file: str = "") -> str:
    """Kurul bilgisini standart dönemsel kimliğe eşler."""
    c = tr_lower(committee_id or "")
    sf = tr_lower(source_file or "")
    combined = f"{c} {sf}"

    if any(k in combined for k in ["kurul1", "kurul 1", "kurul i", "1.kurul", "1. kurul"]):
        return "donem3-kurul1"
    if any(k in combined for k in ["kurul2", "kurul 2", "kurul ii", "2.kurul", "2. kurul", "noropsikiyatri"]):
        return "donem3-kurul2"
    if any(k in combined for k in ["kurul3", "kurul 3", "kurul iii", "3.kurul", "3. kurul", "gis", "gastro"]):
        return "donem3-kurul3"
    if any(k in combined for k in ["kurul4", "kurul 4", "kurul iv", "4.kurul", "4. kurul", "dolasim", "solunum", "kardiyo"]):
        return "donem3-kurul4"
    if any(k in combined for k in ["kurul5", "kurul 5", "kurul v", "5.kurul", "5. kurul", "ortopedi", "urogenital"]):
        return "donem3-kurul5"
    if any(k in combined for k in ["kurul6", "kurul 6", "kurul vi", "6.kurul", "6. kurul", "endokrin"]):
        return "donem3-kurul6"
    if "final" in combined:
        return "donem3-final"
    if "but" in combined:
        return "donem3-butunleme"

    return c or "donem3-kurul1"

def normalize_year(year_val: str, source_file: str = "") -> str:
    """Sınav yılını standart YYYY-YYYY veya 'arsiv' formatına normalize eder."""
    y = str(year_val or "").strip()
    sf = str(source_file or "").strip()
    combined = f"{y} {sf}"

    m = re.search(r'20\d{2}[\-\/]20\d{2}', combined)
    if m:
        return m.group(0).replace('/', '-')

    if "2020-2021" in combined or "20 21" in combined: return "2020-2021"
    if "2021-2022" in combined or "21 22" in combined or "2021" in combined: return "2021-2022"
    if "2022-2023" in combined or "22 23" in combined or "2022" in combined: return "2022-2023"
    if "2023-2024" in combined or "2023" in combined: return "2023-2024"
    if "2024-2025" in combined or "2024" in combined: return "2024-2025"
    if "2025-2026" in combined or "25-26" in combined: return "2025-2026"
    if "2016-2017" in combined: return "2016-2017"

    if "arsiv" in tr_lower(combined) or "gecmis" in tr_lower(combined):
        return "arsiv"

    return y or "arsiv"

# ---------------------------------------------------------------------------
# SORU AYRIŞTIRMA VE BİLGİ ÇIKARMA
# ---------------------------------------------------------------------------

def extract_stem(q: dict) -> str:
    """Sorunun metnini (stem) en güvenilir alandan çıkarır."""
    stem = q.get('stem')
    if not stem and isinstance(q.get('reconstruction'), dict):
        stem = q['reconstruction'].get('stem')
    if not stem and isinstance(q.get('rawQuestion'), dict):
        stem = q['rawQuestion'].get('stem')
    return (stem or '').strip()

def extract_options(q: dict) -> list:
    """Sorunun seçeneklerini liste olarak standardize eder."""
    opts = q.get('options')
    if not opts and isinstance(q.get('reconstruction'), dict):
        opts = q['reconstruction'].get('options')
    if not opts and isinstance(q.get('rawQuestion'), dict):
        opts = q['rawQuestion'].get('options')
    if not opts:
        opts = []

    clean_opts = []
    for opt in opts:
        if isinstance(opt, dict):
            key = (opt.get('key') or '').strip().upper()
            text = (opt.get('text') or '').strip()
            is_correct = opt.get('isCorrect', False)
            clean_opts.append({
                'key': key,
                'text': text,
                'clean_text': clean_for_match(text),
                'isCorrect': bool(is_correct)
            })
    return clean_opts

def extract_correct_answer(q: dict, clean_opts: list) -> tuple:
    """(ans_key, ans_clean_text, ans_raw_text) üçlüsünü çıkarır."""
    ans_key = (q.get('correctAnswer') or '').strip().upper()
    if not ans_key and isinstance(q.get('rawQuestion'), dict):
        ans_key = (q['rawQuestion'].get('claimedAnswer') or '').strip().upper()
    if not ans_key and isinstance(q.get('reconstruction'), dict):
        ans_key = (q['reconstruction'].get('correctAnswer') or '').strip().upper()

    ans_text = ""
    # Seçenekler içinden doğru seçeneğin metnini bul
    for opt in clean_opts:
        if (ans_key and opt['key'] == ans_key) or opt['isCorrect']:
            ans_text = opt['text']
            if not ans_key and opt['key']:
                ans_key = opt['key']
            break

    return ans_key, clean_for_match(ans_text), ans_text

def calculate_quality_score(q: dict) -> int:
    """
    Bir sorunun redaksiyon ve veri zenginliği kalitesini puanlar.
    Daha yüksek puanlı soru, birleşmede master (ana soru) olarak seçilir.
    """
    score = 0
    qid = str(q.get('id', ''))
    if qid.startswith('d3-k'):
        score += 120  # Elle doğrulanmış / redakte soru
    if q.get('is_curated'):
        score += 60
    
    explanation = q.get('explanation') or ''
    if len(explanation) > 100:
        score += 50
    elif len(explanation) > 30:
        score += 25
        
    opts = q.get('options') or []
    if len(opts) == 5:
        score += 30
        if any(o.get('isCorrect') for o in opts if isinstance(o, dict)):
            score += 20
            
    if q.get('reconstruction'):
        score += 15
    if not q.get('isSuspect') and not q.get('isAmbiguous'):
        score += 10
        
    stem = extract_stem(q)
    if len(stem) > 40:
        score += 10
        
    return score

# ---------------------------------------------------------------------------
# EŞLEŞME VE BİRLEŞTİRME KARAR MOTORU
# ---------------------------------------------------------------------------

def evaluate_question_match(q1: dict, q2: dict, similarity_threshold: float = 0.82) -> dict:
    """
    İki soru arasındaki benzerliği ve cevap uyumunu değerlendirir.
    Dönen sözlükte:
      - is_match: bool
      - action: 'MERGE' | 'KEEP_SEPARATE' | None
      - reason: str
    """
    cid1, yr1 = q1['norm_cid'], q1['norm_yr']
    cid2, yr2 = q2['norm_cid'], q2['norm_yr']

    is_same_kurul = (cid1 == cid2)
    is_same_year = (yr1 == yr2)

    s1 = q1['clean_stem']
    s2 = q2['clean_stem']
    if len(s1) < 10 or len(s2) < 10:
        return None

    # Zıt kök çelişkisi varsa (örn: "hangisi görülür" vs "hangisi görülmez", "drift" vs "shift")
    if has_antonym_contradiction(q1['stem'], q2['stem']):
        return None

    # 1. Soru Kökü Benzerliği
    if s1 == s2:
        stem_sim = 1.0
    elif s1.startswith(s2) or s2.startswith(s1):
        stem_sim = min(len(s1), len(s2)) / max(len(s1), len(s2))
    elif s1[:60] == s2[:60] and len(s1) > 50 and len(s2) > 50:
        stem_sim = 0.95
    else:
        len_ratio = min(len(s1), len(s2)) / max(len(s1), len(s2))
        if len_ratio < 0.60:
            return None
        stem_sim = SequenceMatcher(None, s1, s2).ratio()

    if stem_sim < similarity_threshold:
        return None

    # 2. Seçeneklerin Karşılaştırılması
    opt_texts1 = [o['clean_text'] for o in q1['opts'] if len(o['clean_text']) > 3]
    opt_texts2 = [o['clean_text'] for o in q2['opts'] if len(o['clean_text']) > 3]
    set1, set2 = set(opt_texts1), set(opt_texts2)
    matching_opts = set1.intersection(set2)
    
    # 4 veya 5 seçeneğin metni birebir aynı mı?
    is_identical_option_set = len(matching_opts) >= 4 and len(opt_texts1) >= 4 and len(opt_texts2) >= 4

    # 3. Cevap Uyumu Denetimi ("ve cevapları aynı olan sorular")
    ans1_key, ans1_clean, ans1_raw = q1['ans_key'], q1['ans_clean'], q1['ans_raw']
    ans2_key, ans2_clean, ans2_raw = q2['ans_key'], q2['ans_clean'], q2['ans_raw']

    ans_match = False
    ans_reason = ""

    # İki cevabın doğrudan metinsel karşılaştırması
    if ans1_clean and ans2_clean:
        if has_antonym_contradiction(ans1_raw, ans2_raw):
            # Zıt tıbbi kavramlar (örn: minör vs majör, akut vs kronik)
            ans_match = False
        elif ans1_clean == ans2_clean:
            ans_match = True
            ans_reason = "exact_answer_text"
        elif SequenceMatcher(None, ans1_clean, ans2_clean).ratio() >= 0.75:
            ans_match = True
            ans_reason = "similar_answer_text"
        elif (len(ans1_clean) > 5 and ans1_clean in ans2_clean) or (len(ans2_clean) > 5 and ans2_clean in ans1_clean):
            ans_match = True
            ans_reason = "contained_answer_text"
        else:
            # Cevap metinleri farklı. Ancak biri OCR ham aktarımından gelen ve
            # tüm seçenekleri birebir aynı olan bir ikiz mi?
            if is_identical_option_set and stem_sim >= 0.90:
                if (q1['is_curated'] and not q2['is_curated']) or (q2['is_curated'] and not q1['is_curated']):
                    ans_match = True
                    ans_reason = "exact_options_twin_curated_override"
                else:
                    ans_match = False
            else:
                ans_match = False

    elif ans1_clean and not ans2_clean:
        # q2'nin doğru seçeneği q1'in doğru cevabıyla uyuşuyor mu?
        opt2 = next((o for o in q2['opts'] if o['key'] == ans2_key), None)
        if opt2 and (ans1_clean == opt2['clean_text'] or (len(ans1_clean) > 5 and ans1_clean in opt2['clean_text'])):
            ans_match = True
            ans_reason = "ans1_matches_opt2_key"
        elif is_identical_option_set and stem_sim >= 0.90:
            ans_match = True
            ans_reason = "twin_missing_ans2_text"

    elif ans2_clean and not ans1_clean:
        opt1 = next((o for o in q1['opts'] if o['key'] == ans1_key), None)
        if opt1 and (ans2_clean == opt1['clean_text'] or (len(ans2_clean) > 5 and ans2_clean in opt1['clean_text'])):
            ans_match = True
            ans_reason = "ans2_matches_opt1_key"
        elif is_identical_option_set and stem_sim >= 0.90:
            ans_match = True
            ans_reason = "twin_missing_ans1_text"

    elif not ans1_clean and not ans2_clean:
        if is_identical_option_set and stem_sim >= 0.90:
            ans_match = True
            ans_reason = "identical_options_both_no_text"
        elif ans1_key and ans2_key and ans1_key == ans2_key and stem_sim >= 0.92:
            ans_match = True
            ans_reason = "same_key_no_text"

    if not ans_match:
        return None

    # KULLANICI KURALI:
    # "eğerki aynı sene aynı kurulda sorulduysa mutlaka aynı soru altında birleştiren bir script yaz,
    #  eğer farklı kurullarda veya senelerde yazıldığı kesinse o halde sorular kalabilir."
    is_same_exam = (is_same_kurul and is_same_year)
    action = 'MERGE' if is_same_exam else 'KEEP_SEPARATE'

    return {
        'stem_sim': stem_sim,
        'opts_overlap': len(matching_opts),
        'ans_reason': ans_reason,
        'is_same_kurul': is_same_kurul,
        'is_same_year': is_same_year,
        'action': action
    }

# ---------------------------------------------------------------------------
# ANA BİRLEŞTİRME VE İŞLEME MOTORU
# ---------------------------------------------------------------------------

class ExamQuestionDeduplicator:
    def __init__(self, questions: list, similarity_threshold: float = 0.82):
        self.raw_questions = questions
        self.similarity_threshold = similarity_threshold
        self.processed = []
        self._preprocess()

    def _preprocess(self):
        for idx, q in enumerate(self.raw_questions):
            stem = extract_stem(q)
            c_stem = clean_for_match(stem)
            opts = extract_options(q)
            ans_key, ans_clean, ans_raw = extract_correct_answer(q, opts)
            norm_cid = normalize_committee(q.get('committeeId'), q.get('sourceFile') or q.get('source'))
            norm_yr = normalize_year(q.get('examYear') or q.get('year'), q.get('sourceFile') or q.get('source'))
            qid = str(q.get('id', ''))
            is_curated = qid.startswith('d3-k') or bool(q.get('explanation') and len(q.get('explanation')) > 40)
            score = calculate_quality_score(q)

            self.processed.append({
                'idx': idx,
                'id': qid or f"q-{idx}",
                'raw': q,
                'stem': stem,
                'clean_stem': c_stem,
                'opts': opts,
                'ans_key': ans_key,
                'ans_clean': ans_clean,
                'ans_raw': ans_raw,
                'norm_cid': norm_cid,
                'norm_yr': norm_yr,
                'is_curated': is_curated,
                'score': score
            })

    def run(self):
        """
        Deduplikasyon ve çapraz referanslama işlemini gerçekleştirir.
        Geriye (final_questions, audit_report) döndürür.
        """
        # Hızlı blok arama için shingle (n-gram) indeksi oluştur
        shingle_index = defaultdict(set)
        for idx, p in enumerate(self.processed):
            stem = p['clean_stem']
            if len(stem) < 10:
                continue
            for start in range(0, min(len(stem) - 8, 48), 6):
                shingle = stem[start:start+8]
                shingle_index[shingle].add(idx)

        candidate_pairs = set()
        for shingle, idx_set in shingle_index.items():
            if 1 < len(idx_set) < 120:
                s_list = sorted(list(idx_set))
                for i in range(len(s_list)):
                    for j in range(i + 1, len(s_list)):
                        candidate_pairs.add((s_list[i], s_list[j]))

        # Disjoint-set / Graph ile aynı sınavdaki mükerrer soruları kümele
        parent = {}
        def find(i):
            if parent.setdefault(i, i) != i:
                parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_j] = root_i

        merge_events = []
        cross_exam_references = defaultdict(list)

        for i, j in candidate_pairs:
            p1 = self.processed[i]
            p2 = self.processed[j]

            eval_res = evaluate_question_match(p1, p2, self.similarity_threshold)
            if not eval_res:
                continue

            if eval_res['action'] == 'MERGE':
                union(i, j)
                merge_events.append({
                    'q1_id': p1['id'],
                    'q2_id': p2['id'],
                    'committeeId': p1['norm_cid'],
                    'examYear': p1['norm_yr'],
                    'stem_similarity': round(eval_res['stem_sim'], 3),
                    'match_reason': eval_res['ans_reason'],
                    'q1_stem': p1['stem'][:90],
                    'q2_stem': p2['stem'][:90],
                    'answer': p1['ans_raw'] or p2['ans_raw']
                })
            elif eval_res['action'] == 'KEEP_SEPARATE':
                # Farklı yıl veya kurul: Kesinlikle korunur, sadece çapraz referans eklenir
                cross_exam_references[i].append({
                    'target_id': p2['id'],
                    'target_committee': p2['norm_cid'],
                    'target_year': p2['norm_yr'],
                    'similarity': round(eval_res['stem_sim'], 3)
                })
                cross_exam_references[j].append({
                    'target_id': p1['id'],
                    'target_committee': p1['norm_cid'],
                    'target_year': p1['norm_yr'],
                    'similarity': round(eval_res['stem_sim'], 3)
                })

        # Kümeleri grupla
        clusters = defaultdict(list)
        for idx in range(len(self.processed)):
            root = find(idx)
            clusters[root].append(idx)

        final_questions = []
        merged_clusters_audit = []

        for root, member_indices in clusters.items():
            if len(member_indices) == 1:
                idx = member_indices[0]
                q_obj = dict(self.processed[idx]['raw'])
                # Çapraz referansları ekle
                if idx in cross_exam_references:
                    q_obj['crossExamReferences'] = cross_exam_references[idx]
                    tags = list(q_obj.get('tags') or [])
                    if 'Tekrar Sorulan Soru' not in tags:
                        tags.append('Tekrar Sorulan Soru')
                    q_obj['tags'] = tags
                final_questions.append(q_obj)
            else:
                # Birden fazla soru aynı sınavda eşleşti: MASTER SEÇ VE BİRLEŞTİR!
                members = [self.processed[idx] for idx in member_indices]
                # En yüksek kaliteli olanı master yap
                members.sort(key=lambda m: (m['score'], len(m['stem'])), reverse=True)
                master = members[0]
                secondary_members = members[1:]

                merged_q = dict(master['raw'])

                # Birleşen ID'leri topla
                merged_ids = list(merged_q.get('mergedQuestionIds') or [])
                for sm in secondary_members:
                    if sm['id'] not in merged_ids and sm['id'] != master['id']:
                        merged_ids.append(sm['id'])
                merged_q['mergedQuestionIds'] = merged_ids

                # Kaynak dosyaları birleştir
                sources = set()
                primary_sf = merged_q.get('sourceFile') or merged_q.get('source')
                if primary_sf:
                    sources.add(str(primary_sf))
                for sm in secondary_members:
                    sec_sf = sm['raw'].get('sourceFile') or sm['raw'].get('source')
                    if sec_sf:
                        sources.add(str(sec_sf))
                merged_q['sourceFiles'] = sorted(list(sources))

                # Mükerrer kopya sayısı
                merged_q['duplicateExamOccurrences'] = len(member_indices)

                # Birleşen soru detayları
                merged_q['mergedVariants'] = [
                    {
                        'id': sm['id'],
                        'source': sm['raw'].get('sourceFile') or sm['raw'].get('source'),
                        'stem': sm['stem']
                    }
                    for sm in secondary_members
                ]

                # Çapraz referansları birleştir
                all_cross_refs = []
                for idx in member_indices:
                    if idx in cross_exam_references:
                        all_cross_refs.extend(cross_exam_references[idx])
                if all_cross_refs:
                    # Tekilleştir
                    seen_targets = set()
                    unique_refs = []
                    for cr in all_cross_refs:
                        if cr['target_id'] not in seen_targets and cr['target_id'] != master['id'] and cr['target_id'] not in merged_ids:
                            seen_targets.add(cr['target_id'])
                            unique_refs.append(cr)
                    if unique_refs:
                        merged_q['crossExamReferences'] = unique_refs
                        tags = list(merged_q.get('tags') or [])
                        if 'Tekrar Sorulan Soru' not in tags:
                            tags.append('Tekrar Sorulan Soru')
                        merged_q['tags'] = tags

                final_questions.append(merged_q)
                merged_clusters_audit.append({
                    'master_id': master['id'],
                    'master_stem': master['stem'][:100],
                    'committeeId': master['norm_cid'],
                    'examYear': master['norm_yr'],
                    'merged_count': len(secondary_members),
                    'merged_ids': [sm['id'] for sm in secondary_members],
                    'sources': list(sources)
                })

        # İnceleme Raporu
        audit_report = {
            'timestamp': datetime.now().isoformat(),
            'initial_question_count': len(self.raw_questions),
            'final_question_count': len(final_questions),
            'same_exam_duplicates_merged': len(self.raw_questions) - len(final_questions),
            'merge_clusters_count': len(merged_clusters_audit),
            'cross_exam_preserved_pairs_count': len([pair for pair in candidate_pairs if self._is_cross_exam_match(pair)]),
            'merged_clusters': merged_clusters_audit
        }

        return final_questions, audit_report

    def _is_cross_exam_match(self, pair):
        i, j = pair
        eval_res = evaluate_question_match(self.processed[i], self.processed[j], self.similarity_threshold)
        return eval_res and eval_res['action'] == 'KEEP_SEPARATE'

# ---------------------------------------------------------------------------
# RAPOR VE DOSYA İŞLEMLERİ
# ---------------------------------------------------------------------------

def generate_markdown_report(audit_report: dict, output_md_path: str):
    """Kullanıcı için detaylı ve şık bir Markdown denetim raporu üretir."""
    lines = [
        "# Sınav Soruları Birleştirme ve Deduplikasyon Raporu",
        f"**Tarih:** {audit_report['timestamp']}  ",
        f"**İlk Toplam Soru Sayısı:** {audit_report['initial_question_count']}  ",
        f"**Birleştirme Sonrası Soru Sayısı:** {audit_report['final_question_count']}  ",
        f"**Aynı Sene & Kurulda Birleştirilen Mükerrer Soru:** {audit_report['same_exam_duplicates_merged']}  ",
        f"**Farklı Yıl/Kurulda Olduğu İçin Korunan Tarihsel Tekrarlar:** {audit_report['cross_exam_preserved_pairs_count']}  ",
        "",
        "---",
        "## 1. Uygulanan Mantık ve Kurallar",
        "1. **Aynı Sene ve Aynı Kurul (BİRLEŞTİRİLDİ):** Birbirini tekrar eden, kök ve seçenekleri aşırı benzeyen ve aynı cevaba sahip olan sorular tespit edildi. En yüksek kaliteli / redakte edilmiş versiyon master soru yapıldı; mükerrer kopyaların ID ve kaynakları ana soru altında birleştirildi.",
        "2. **Farklı Sene veya Farklı Kurul (KORUNDU):** Aynı soru farklı bir yılda (örn: 2021 ve 2024) veya farklı bir kurulda (örn: Kurul 1 ve Final) sorulmuşsa bu sorular **ayrı bırakıldı** ve veri tabanında tutuldu. Ek olarak `crossExamReferences` ile birbirlerine bağlandı.",
        "3. **Zıt / Çelişkili Cevaplar (KORUNDU):** Kökleri benzer olsa bile farklı veya zıt cevaplara sahip olan sorular (örn: hızlı etkili vs uzun etkili insülin) farklı sorular kabul edilerek asla birleştirilmedi.",
        "",
        "## 2. Birleştirilen Soru Kümeleri (Örnekler)",
        "| Master Soru ID | Kurul | Sınav Yılı | Birleştirilen ID'ler | Kaynak Dosyalar |",
        "|---|---|---|---|---|"
    ]

    for c in audit_report['merged_clusters'][:35]:
        m_ids = ", ".join(c['merged_ids'])
        srcs = ", ".join(c['sources'])
        lines.append(f"| `{c['master_id']}` | {c['committeeId']} | {c['examYear']} | `{m_ids}` | {srcs} |")

    lines.append("")
    lines.append("*(Raporun tam detayları ve tüm küme listesi JSON raporunda mevcuttur)*")

    with open(output_md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

def process_file(file_path: str, apply_changes: bool = False, create_backup: bool = True, similarity: float = 0.82):
    """Tek bir JSON dosyasını okur, mükerrerleri birleştirir ve kaydeder."""
    print(f"\n📂 Dosya işleniyor: {file_path}")
    if not os.path.exists(file_path):
        print(f"❌ Dosya bulunamadı: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"⚠️ Dosya bir soru listesi (JSON array) içermiyor, atlandı.")
        return

    print(f"   Mevcut soru sayısı: {len(data)}")
    deduper = ExamQuestionDeduplicator(data, similarity_threshold=similarity)
    final_questions, report = deduper.run()

    print(f"   ✅ İşlem tamamlandı:")
    print(f"      - Başlangıç: {report['initial_question_count']}")
    print(f"      - Birleştirilen mükerrer: {report['same_exam_duplicates_merged']}")
    print(f"      - Nihai soru sayısı: {report['final_question_count']}")
    print(f"      - Farklı sene/kurul korunan: {report['cross_exam_preserved_pairs_count']}")

    if apply_changes and report['same_exam_duplicates_merged'] > 0:
        if create_backup:
            bak_path = f"{file_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            shutil.copy2(file_path, bak_path)
            print(f"   💾 Yedek alındı: {bak_path}")

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_questions, f, ensure_ascii=False, indent=2)
        print(f"   ✨ Değişiklikler başarıyla kaydedildi: {file_path}")
    elif not apply_changes:
        print(f"   ℹ️ DRY-RUN modu aktif: Dosya üzerinde değişiklik yapılmadı. Uygulamak için --apply ekleyin.")

    return report

# ---------------------------------------------------------------------------
# CLI GİRİŞ NOKTASI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Aynı sene ve aynı kurulda sorulan eşleşen / tekrar eden soruları birleştiren script."
    )
    parser.add_argument('--input', '-i', type=str, default=None,
                        help="İşlenecek JSON dosyasının yolu. Belirtilmezse varsayılan pastQuestions.json dosyaları işlenir.")
    parser.add_argument('--apply', '-a', action='store_true',
                        help="Değişiklikleri dosyalara doğrudan uygular (varsayılan: dry-run).")
    parser.add_argument('--no-backup', action='store_true',
                        help="Yedek (.bak) dosyası oluşturmayı atlar.")
    parser.add_argument('--similarity', '-s', type=float, default=0.82,
                        help="Soru kökü benzerlik eşik değeri (varsayılan: 0.82).")
    parser.add_argument('--report-dir', '-r', type=str, default=((__import__('os').environ.get('MEDS_DATABASE_DIR') or __import__('os').path.expanduser('~/meds_database'))),
                        help="Raporların kaydedileceği dizin.")

    args = parser.parse_args()

    default_targets = [
        (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/src/data/pastQuestions.json"),
        (__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))) + "/data/pastQuestions.json")
    ]

    import glob

    target_files = []
    if args.input:
        if os.path.isdir(args.input):
            target_files = [f for f in glob.glob(os.path.join(args.input, "*.json")) if "raporu" not in os.path.basename(f).lower()]
        elif "*" in args.input:
            target_files = [f for f in glob.glob(args.input) if "raporu" not in os.path.basename(f).lower()]
        elif os.path.exists(args.input):
            target_files = [args.input]
        else:
            print(f"❌ Belirtilen giriş yolu bulunamadı: {args.input}")
            sys.exit(1)
    else:
        target_files = [p for p in default_targets if os.path.exists(p)]

    print("=" * 70)
    print("🚀 TIP ÇIKMIŞ SORULARI AYNI SENE & AYNI KURUL BİRLEŞTİRME SCRIPTI")
    print("=" * 70)
    print(f"Mod: {'DEĞİŞİKLİKLERİ UYGULA (--apply)' if args.apply else 'DRY-RUN (Sadece Simülasyon)'}")
    print(f"Benzerlik Eşiği: {args.similarity}")
    print(f"Hedef Dosyalar: {len(target_files)}")

    all_reports = []
    for tf in target_files:
        rep = process_file(
            file_path=tf,
            apply_changes=args.apply,
            create_backup=not args.no_backup,
            similarity=args.similarity
        )
        if rep:
            all_reports.append(rep)

    # Genel rapor üret
    if all_reports and args.report_dir:
        os.makedirs(args.report_dir, exist_ok=True)
        primary_rep = all_reports[0]
        json_rep_path = os.path.join(args.report_dir, 'duplicate_merge_audit.json')
        md_rep_path = os.path.join(args.report_dir, 'duplicate_merge_report.md')

        with open(json_rep_path, 'w', encoding='utf-8') as f:
            json.dump(primary_rep, f, ensure_ascii=False, indent=2)
        generate_markdown_report(primary_rep, md_rep_path)

        print(f"\n📊 Detaylı denetim raporu üretildi:")
        print(f"   - Markdown: {md_rep_path}")
        print(f"   - JSON:     {json_rep_path}")

    print("\n✅ İşlem başarıyla sonlandırıldı.")

if __name__ == '__main__':
    main()
