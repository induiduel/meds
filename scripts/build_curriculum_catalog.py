#!/usr/bin/env python3
"""
Müfredat Kazanım Kataloğu Üretici (Curriculum Outcomes Generator) v2

Temel İlkeler:
1. "Her bir sorunun bir kazanımı olabilir" (Soru tekilleştirme: hiçbir soru birden fazla kazanıma kopyalanmaz).
2. "Her kazanımın illa bir sorusu olmak zorunda değil, aynısı örnek sorular için de geçerli" (Sorusu olmayan kazanım temiz [] kalır).
3. "Kazanımlarda uygun kazanımın altına uygun çıkmışı ekle" (Sorular veritabanındaki eşleşmelere ve anlamsal örtüşmeye göre en uygun tekil kazanıma bağlanır).
4. Müfredat paketi (Kurul -> Ders -> Konu) hiyerarşisi korunur.

Kaynaklar:
1. meds_database/ortak/veri/mufredat_baglantilari/mufredat_paketi.json (Resmî müfredat ağacı)
2. meds_database_v2/kurul1_ders_paketleri/*.json (Kurul 1 doğrulanmış kazanımları)
3. meds/src/data/ornek_sorular/k1/*.json (Kurul 1 örnek ve benzer çıkmış soru haritası)
4. meds_database/derived/curriculum_links/soru_kazanim.jsonl & phase8/soru_kazanim.jsonl (3.016 soru-kazanım eşleşmesi)
5. meds_database_core/questions/archive.jsonl (Core soru-kazanım veritabanı)
6. meds/src/data/pastQuestions.json & soru_mufredat.json (Çıkmış sorular)
7. meds/src/data/lectureSummariesCatalog.json (359 ders özeti ve anahtar noktaları)
8. meds/src/data/medical_glossary.json (Tıbbi sözlük)
"""

import json
import glob
import re
import os
from pathlib import Path

ROOT = Path("/home/indu/medsor")
MEDS = ROOT / "meds"
DATA_DIR = MEDS / "src" / "data"
OUT_DIR = DATA_DIR / "kazanimlar"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def norm_tokens(s: str) -> set:
    if not s:
        return set()
    s = s.lower().replace("’", "'").replace("`", "'").replace("–", "-").replace("—", "-")
    s = s.replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ğ", "g")
    return set(re.findall(r"[a-z0-9]{3,}", s))

def norm_key(s: str) -> str:
    if not s:
        return ""
    s = s.lower().replace("’", "'").replace("`", "'").replace("–", "-").replace("—", "-")
    s = s.replace("ı", "i").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ğ", "g")
    return re.sub(r"[^a-z0-9]", "", s)

print("1. Veri kaynakları ve soru haritaları yükleniyor...")

# 1. Resmî Müfredat Paketi
with open(ROOT / "meds_database/ortak/veri/mufredat_baglantilari/mufredat_paketi.json", encoding="utf-8") as f:
    mufredat_pkg = json.load(f)

# 2. Kurul 1 Ders Paketleri
k1_packages = {}
for path in glob.glob(str(ROOT / "meds_database_v2/kurul1_ders_paketleri/k1-*.json")):
    with open(path, encoding="utf-8") as fp:
        data = json.load(fp)
        k1_packages[norm_key(data.get("konu", ""))] = data

# 3. Kurul 1 Örnek Sorular ve Kazanım Eşleşmeleri
k1_ornek = {}
q_to_k1_explicit_kazanim = {}  # qid -> (konu_norm, kazanim_no)

for path in glob.glob(str(DATA_DIR / "ornek_sorular/k1/k1-*.json")):
    with open(path, encoding="utf-8") as fp:
        data = json.load(fp)
        konu_norm = norm_key(data.get("konu", ""))
        k1_ornek[konu_norm] = data
        for kz in data.get("kazanimlar", []):
            kz_no = kz.get("no")
            for cq in kz.get("ilgili_cikmis", []):
                qid = cq.get("id")
                if qid and qid not in q_to_k1_explicit_kazanim:
                    q_to_k1_explicit_kazanim[qid] = (konu_norm, kz_no)
            for sq in kz.get("sorular", []):
                for bq in sq.get("benzer_cikmis", []):
                    qid = bq.get("id") if isinstance(bq, dict) else bq
                    if qid and qid not in q_to_k1_explicit_kazanim:
                        q_to_k1_explicit_kazanim[qid] = (konu_norm, kz_no)

# 4. Soru-Kazanım Haritaları (soru_kazanim.jsonl)
q_to_soru_kazanim = {}
for path in [ROOT / "meds_database/derived/curriculum_links/soru_kazanim.jsonl", ROOT / "meds_temp/phase8/soru_kazanim.jsonl"]:
    if path.exists():
        with open(path, encoding="utf-8") as fp:
            for line in fp:
                try:
                    d = json.loads(line)
                    qid = d.get("soru_id")
                    if qid and qid not in q_to_soru_kazanim and d.get("kazanimlar"):
                        first_k = d["kazanimlar"][0]
                        q_to_soru_kazanim[qid] = {
                            "kurul": first_k.get("kurul"),
                            "ders": first_k.get("ders"),
                            "konu": first_k.get("konu"),
                            "kazanim_text": first_k.get("kazanim")
                        }
                except Exception:
                    pass

# 5. Core archive.jsonl Haritası
q_to_archive_kazanim = {}
p_arch = ROOT / "meds_database_core/questions/archive.jsonl"
if p_arch.exists():
    with open(p_arch, encoding="utf-8") as fp:
        for line in fp:
            try:
                d = json.loads(line)
                qid = d.get("question_id")
                if qid and (d.get("kazanim") or d.get("konu")):
                    q_to_archive_kazanim[qid] = {
                        "kurul": d.get("kurul") or (d.get("mufredat") or {}).get("kurul"),
                        "ders": d.get("ders") or (d.get("mufredat") or {}).get("ders"),
                        "konu": d.get("konu") or (d.get("mufredat") or {}).get("konu"),
                        "kazanim_text": d.get("kazanim") or (d.get("mufredat") or {}).get("kazanim")
                    }
            except Exception:
                pass

# 6. Soru-Müfredat JSON Haritası
with open(ROOT / "meds_database/ortak/veri/mufredat_baglantilari/soru_mufredat.json", encoding="utf-8") as f:
    soru_muf = json.load(f).get("sorular", {})

# 7. Çıkmış Sorular Kataloğu
with open(DATA_DIR / "pastQuestions.json", encoding="utf-8") as f:
    past_questions = json.load(f)
pq_by_id = {q["id"]: q for q in past_questions}

# 8. Ders Özetleri
with open(DATA_DIR / "lectureSummariesCatalog.json", encoding="utf-8") as f:
    lecture_summaries = json.load(f)

summaries_by_kurul = {}
for s in lecture_summaries:
    k = s.get("kurul")
    if k not in summaries_by_kurul:
        summaries_by_kurul[k] = []
    summaries_by_kurul[k].append(s)

# 9. Tıbbi Sözlük
glossary_by_term = {}
try:
    with open(DATA_DIR / "medical_glossary.json", encoding="utf-8") as f:
        glossary_by_term = json.load(f)
except Exception as e:
    print(f"Glossary load warning: {e}")

print(f"Müfredat Kurul sayısı: {len(mufredat_pkg['kurullar'])}")
print(f"Geçmiş Sınav Sorusu: {len(past_questions)}")
print(f"K1 Özel Eşleşmiş Çıkmış Soru: {len(q_to_k1_explicit_kazanim)}")
print(f"Soru-Kazanım DB Eşleşmesi: {len(q_to_soru_kazanim)}")
print(f"Archive DB Eşleşmesi: {len(q_to_archive_kazanim)}")

# Soru Tekilleştirme Kümeleri (Her soru yalnız 1 kere atanabilir)
assigned_question_ids = set()
assigned_ornek_ids = set()

def format_question(q: dict) -> dict:
    return {
        "id": q.get("id"),
        "questionNumber": q.get("questionNumber"),
        "stem": q.get("stem", ""),
        "correctAnswer": q.get("correctAnswer", ""),
        "options": [
            {"key": opt.get("key", opt.get("label", "")), "text": opt.get("text", "")}
            for opt in q.get("options", [])
        ],
        "year": q.get("year") or q.get("examYear") or "2023-2024",
        "discipline": q.get("discipline", ""),
        "topic": q.get("topic", ""),
        "explanation": q.get("explanation", "")
    }

index_summary = []

for kurul_info in mufredat_pkg["kurullar"]:
    k_num = kurul_info["kurul"]
    k_name = kurul_info["ad"]
    k_code = kurul_info["kod"]
    print(f"\n--- İşleniyor: Kurul {k_num} ({k_code}) - {k_name} ---")

    ders_groups = []
    kurul_total_kazanim = 0
    kurul_assigned_questions = 0

    k_summaries = summaries_by_kurul.get(k_num, [])

    # Bu kurula ait henüz atanmamış çıkmış soruları topla
    cid = f"donem3-kurul{k_num}"
    available_kurul_questions = [
        q for q in past_questions 
        if q.get("committeeId") in (cid, k_code) and q["id"] not in assigned_question_ids
    ]

    for d in kurul_info["dersler"]:
        ders_name = d["ders"].strip()
        ders_norm = norm_key(ders_name)
        konular = d["konular"]

        konu_groups = []
        ders_kazanim_count = 0

        for c_idx, konu_name in enumerate(konular):
            konu_name = konu_name.strip()
            konu_norm = norm_key(konu_name)

            # Bu konu ile eşleşen özet
            matched_summary = None
            for s in k_summaries:
                s_title_norm = norm_key(s.get("title", ""))
                s_disc_norm = norm_key(s.get("discipline", ""))
                if (konu_norm in s_title_norm or s_title_norm in konu_norm) and (not s_disc_norm or ders_norm in s_disc_norm or s_disc_norm in ders_norm):
                    matched_summary = s
                    break

            summary_text = matched_summary.get("content", "") if matched_summary else ""
            summary_key_points = matched_summary.get("keyPoints", []) if matched_summary else []

            # İlgili sözlük terimleri
            related_terms = []
            konu_words = [w for w in re.findall(r"[a-zA-ZğüşıöçĞÜŞİÖÇ]{4,}", konu_name)]
            for t_raw, t_val in glossary_by_term.items():
                t_term = t_val.get("term", t_raw)
                t_norm = norm_key(t_term)
                if any(w.lower() in t_norm for w in konu_words):
                    related_terms.append({
                        "term": t_term,
                        "definition": t_val.get("definition") or t_val.get("description", ""),
                        "pearl": t_val.get("clinicalPearl", "")
                    })
                if len(related_terms) >= 3:
                    break

            # Slayt bilgisi
            slaytlar = []
            if k_num == 1:
                k1_data = k1_packages.get(konu_norm)
                if not k1_data:
                    for kn, vd in k1_packages.items():
                        if kn in konu_norm or konu_norm in kn:
                            k1_data = vd
                            break
                if k1_data and k1_data.get("ogrenim_slaytlari"):
                    deck_id = k1_data.get("id", f"k1p-{c_idx+1}")
                    for s_item in k1_data["ogrenim_slaytlari"][:4]:
                        slaytlar.append({
                            "kaynak": f"{ders_name} - {konu_name}",
                            "sayfa": s_item.get("slaytNo", 1),
                            "alinti": s_item.get("baslik", "") + " (" + s_item.get("rozet", "") + ")",
                            "deckId": deck_id
                        })
            elif matched_summary:
                slaytlar.append({
                    "kaynak": f"{ders_name} - {konu_name}",
                    "sayfa": 1,
                    "alinti": matched_summary.get("title", konu_name),
                    "deckId": matched_summary.get("id", "")
                })

            # Bu konu altındaki aday soruları belirle (soru_mufredat, soru_kazanim, pastQuestions)
            candidate_topic_questions = []
            for q in available_kurul_questions:
                if q["id"] in assigned_question_ids:
                    continue
                qid = q["id"]
                is_match = False

                # 1. soru_muf kontrolü
                sm_info = soru_muf.get(qid)
                if sm_info and norm_key(sm_info.get("konu", "")) == konu_norm:
                    is_match = True
                
                # 2. soru_kazanim kontrolü
                sk_info = q_to_soru_kazanim.get(qid)
                if not is_match and sk_info and norm_key(sk_info.get("konu", "")) == konu_norm:
                    is_match = True

                # 3. archive kontrolü
                arch_info = q_to_archive_kazanim.get(qid)
                if not is_match and arch_info and norm_key(arch_info.get("konu", "")) == konu_norm:
                    is_match = True

                # 4. pastQuestions topic kontrolü
                q_top_norm = norm_key(q.get("topic", ""))
                if not is_match and q_top_norm and (q_top_norm == konu_norm or q_top_norm in konu_norm or konu_norm in q_top_norm):
                    is_match = True

                if is_match:
                    candidate_topic_questions.append(q)

            # Kazanımları üret
            kazanim_items = []

            if k_num == 1:
                k1_data = k1_packages.get(konu_norm)
                if not k1_data:
                    for kn, vd in k1_packages.items():
                        if kn in konu_norm or konu_norm in kn:
                            k1_data = vd
                            break

                k1_ornek_data = k1_ornek.get(konu_norm)
                if not k1_ornek_data:
                    for kn, vd in k1_ornek.items():
                        if kn in konu_norm or konu_norm in kn:
                            k1_ornek_data = vd
                            break

                raw_kazanimlar = k1_data.get("kazanimlar", []) if k1_data else []
                if not raw_kazanimlar:
                    raw_kazanimlar = [
                        f"{konu_name} ile ilgili temel mekanizmaları ve kavramları tanımlar.",
                        f"{konu_name} klinik özelliklerini ve tanı yaklaşımlarını açıklar."
                    ]

                for k_idx_num, kaz_text in enumerate(raw_kazanimlar, 1):
                    kaz_tokens = norm_tokens(kaz_text)

                    # Bu kazanıma ait ÖRNEK SORULAR (yalnızca bu kazanım no'ya ait olanlar!)
                    matched_ornek = []
                    if k1_ornek_data and "kazanimlar" in k1_ornek_data:
                        for okz in k1_ornek_data["kazanimlar"]:
                            if okz.get("no") == k_idx_num:
                                for q_item in okz.get("sorular", []):
                                    q_id = q_item.get("id")
                                    if q_id and q_id not in assigned_ornek_ids:
                                        assigned_ornek_ids.add(q_id)
                                        matched_ornek.append({
                                            "id": q_id,
                                            "kazanimNo": k_idx_num,
                                            "zorluk": q_item.get("zorluk", "orta"),
                                            "soru": q_item.get("soru", ""),
                                            "secenekler": q_item.get("secenekler", {}),
                                            "dogru": q_item.get("dogru", ""),
                                            "aciklama": q_item.get("aciklama", "")
                                        })

                    # Bu kazanıma ait ÇIKMIŞ SORULAR (Tekil atama!)
                    kazanim_cikmis = []

                    # 1. Öncelik: ornek_sorular'da doğrudan bu kazanım no'ya eşlenmiş çıkmış sorular
                    for q in list(candidate_topic_questions):
                        if q["id"] in assigned_question_ids:
                            continue
                        exp_map = q_to_k1_explicit_kazanim.get(q["id"])
                        if exp_map and exp_map[0] == konu_norm and exp_map[1] == k_idx_num:
                            kazanim_cikmis.append(format_question(q))
                            assigned_question_ids.add(q["id"])
                            candidate_topic_questions.remove(q)

                    # 2. Öncelik: Bu konunun diğer aday sorularından en yüksek benzerliğe sahip olanlar
                    # Her kazanım en fazla 3 soru alabilir, eğer benzerlik yüksekse (skor >= 2)
                    for q in list(candidate_topic_questions):
                        if len(kazanim_cikmis) >= 3:
                            break
                        if q["id"] in assigned_question_ids:
                            continue

                        q_text = (q.get("stem", "") + " " + q.get("explanation", ""))
                        q_tokens = norm_tokens(q_text)
                        
                        # soru_kazanim metni varsa onu da hesaba kat
                        sk = q_to_soru_kazanim.get(q["id"])
                        if sk and sk.get("kazanim_text"):
                            q_tokens.update(norm_tokens(sk["kazanim_text"]))

                        overlap = len(kaz_tokens.intersection(q_tokens))
                        if overlap >= 2:
                            kazanim_cikmis.append(format_question(q))
                            assigned_question_ids.add(q["id"])
                            candidate_topic_questions.remove(q)

                    kazanim_items.append({
                        "id": f"k{k_num}-{c_idx+1}-kz-{k_idx_num}",
                        "metin": kaz_text,
                        "slaytlar": slaytlar if k_idx_num <= 2 else slaytlar[:1],
                        "cikmisSorular": kazanim_cikmis,
                        "ornekSorular": matched_ornek,
                        "sozlukTerimleri": related_terms if k_idx_num == 1 else [],
                        "ozetler": [summary_text[:1200]] if summary_text and k_idx_num == 1 else []
                    })
                    kurul_assigned_questions += len(kazanim_cikmis)

            else:
                # Kurullar 2-6: Müfredat konusu uyumlu standart pedagojik öğrenim hedefleri
                base_objectives = [
                    f"{konu_name} konusunun temel kavramlarını, etiyolojisini ve patofizyolojik mekanizmalarını açıklar.",
                    f"{konu_name} ile ilişkili klinik semptomları, tanı kriterlerini ve ayırıcı tanı basamaklarını değerlendirir.",
                    f"{konu_name} klinik yönetimini, farmakoterapi ilkelerini ve komplikasyonlardan korunma yaklaşımlarını sıralar."
                ]

                # Anahtar noktalardan türetilen ek hedefler
                if summary_key_points:
                    for kp in summary_key_points[:2]:
                        kp_clean = kp.strip()
                        if len(kp_clean) > 15 and not kp_clean.lower().startswith("prof") and not kp_clean.lower().startswith("doç"):
                            base_objectives.append(f"{kp_clean} mekanizmasını ve klinik önemini analiz eder.")

                for k_idx_num, kaz_text in enumerate(base_objectives, 1):
                    kaz_tokens = norm_tokens(kaz_text)
                    kazanim_cikmis = []

                    # Bu kazanıma en uygun aday soruları tekil ata (en fazla 3 soru)
                    for q in list(candidate_topic_questions):
                        if len(kazanim_cikmis) >= 3:
                            break
                        if q["id"] in assigned_question_ids:
                            continue

                        q_text = (q.get("stem", "") + " " + q.get("explanation", ""))
                        q_tokens = norm_tokens(q_text)

                        sk = q_to_soru_kazanim.get(q["id"]) or q_to_archive_kazanim.get(q["id"])
                        if sk and sk.get("kazanim_text"):
                            q_tokens.update(norm_tokens(sk["kazanim_text"]))

                        overlap = len(kaz_tokens.intersection(q_tokens))
                        if overlap >= 2 or (k_idx_num == 1 and len(kazanim_cikmis) == 0):
                            kazanim_cikmis.append(format_question(q))
                            assigned_question_ids.add(q["id"])
                            candidate_topic_questions.remove(q)

                    kazanim_items.append({
                        "id": f"k{k_num}-{c_idx+1}-kz-{k_idx_num}",
                        "metin": kaz_text,
                        "slaytlar": slaytlar if k_idx_num == 1 else [],
                        "cikmisSorular": kazanim_cikmis,
                        "ornekSorular": [],
                        "sozlukTerimleri": related_terms if k_idx_num == 1 else [],
                        "ozetler": [summary_text[:1200]] if summary_text and k_idx_num == 1 else []
                    })
                    kurul_assigned_questions += len(kazanim_cikmis)

            konu_groups.append({
                "konu": konu_name,
                "kazanimlar": kazanim_items
            })
            ders_kazanim_count += len(kazanim_items)

        ders_groups.append({
            "ders": ders_name,
            "count": ders_kazanim_count,
            "konular": konu_groups
        })
        kurul_total_kazanim += ders_kazanim_count

    kurul_payload = {
        "kurul": k_num,
        "name": k_name,
        "code": k_code,
        "totalCount": kurul_total_kazanim,
        "dersler": ders_groups
    }

    out_file = OUT_DIR / f"k{k_num}.json"
    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(kurul_payload, fp, ensure_ascii=False, indent=1)

    print(f"Yazıldı: {out_file.name} ({out_file.stat().st_size // 1024} KB) - {len(ders_groups)} ders, {kurul_total_kazanim} kazanım, {kurul_assigned_questions} tekil çıkmış soru bağlandı.")

    index_summary.append({
        "kurul": k_num,
        "name": k_name,
        "code": k_code,
        "totalCount": kurul_total_kazanim,
        "dersler": [{"ders": dg["ders"], "count": dg["count"], "konuCount": len(dg["konular"])} for dg in ders_groups]
    })

with open(OUT_DIR / "index.json", "w", encoding="utf-8") as fp:
    json.dump(index_summary, fp, ensure_ascii=False, indent=2)

print(f"\nToplam tekil atanan soru sayısı: {len(assigned_question_ids)}")
print("Müfredat kazanımları ve tekil soru eşleştirmeleri tamamlandı.")
