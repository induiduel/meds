#!/usr/bin/env python3
"""
Faz 6.5: Tıbbi Terimler Sözlüğü (Thesaurus) & Soru-Slayt Birlikte Görünme (Co-occurrence) Graf Motoru
------------------------------------------------------------------------------------------------------
Görevler:
1. Türkçe tıp terminolojisi, Latince/İngilizce eşanlamlılar, hekim jargonu, alternatif yazımlar ve
   kısaltmaları içeren çok katmanlı 'medical_thesaurus.json' oluşturur.
2. Çıkmış sorular (meds_database/questions) ve amfi ders slayt chunk'ları (meds_database/chunks)
   arasındaki ortak tıbbi terimleri tarar.
3. ÇOKLU DERS EŞLEŞME PROBLEMİNİ ÇÖZEN SKORLAMA ALGORİTMASI:
   - Sadece tek bir terimin geçmesi yetmez (Örn: 'anemi' veya 'enfeksiyon' her derste geçer).
   - Co-occurrence Skoru = (Ortak Tıbbi Terim Sayısı) * (Terimin Özgüllük/Ağırlığı) * (Slayttaki Yoğunluk)
   - Sorudaki diğer tıbbi kavramların o slaytta birlikte bulunma oranı (Jaccard & Terim Kümeleme)
4. En yüksek skora sahip slayt parçası sorunun 'Altın Kanıtı' (Gold Slide Evidence) olarak kancalanır.
5. Sonuçlar 'meds_database_v2/medical_thesaurus/' ve 'phase6_5_anchors.jsonl' dosyasına yazılır.
"""

import os
import sys
import json
import re
import math
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[2] # meds
PROJECT_PARENT = ROOT.parent
DB_QUESTIONS = PROJECT_PARENT / "meds_database" / "questions"
DB_CHUNKS = PROJECT_PARENT / "meds_database" / "chunks"
CURRICULUM_FILE = ROOT / "curriculum" / "kbu_tip_donem3_curriculum.json"
OUT_DIR = PROJECT_PARENT / "meds_database_v2" / "medical_thesaurus"
OUT_DIR.mkdir(parents=True, exist_ok=True)
THESAURUS_FILE = OUT_DIR / "medical_thesaurus.json"
ANCHORS_FILE = OUT_DIR / "phase6_5_question_slide_anchors.jsonl"
STATE_FILE = OUT_DIR / "phase6_5_state.json"

# Kapsamlı Tıbbi Terimler, Eş Anlamlılar ve İlişkili Terim Havuzu
BASE_THESAURUS = {
    # Tiroit & Endokrin
    "folliküler karsinom": {
        "turkce": "Folliküler tiroid karsinomu",
        "latin": "Carcinoma folliculare glandulae thyroideae",
        "esanlamlilar": ["folliküler kanser", "tiroid folliküler ca", "ftc"],
        "anahtar_bilesenler": ["kapsül invazyonu", "damar invazyonu", "vasküler invazyon", "folliküler adenom", "tiroglobulin"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji",
        "ozgulluk_agirligi": 3.5
    },
    "kapsül invazyonu": {
        "turkce": "Kapsül invazyonu / istilası",
        "latin": "Invasio capsularis",
        "esanlamlilar": ["kapsüler invazyon", "kapsül aşımı", "tam kat penetrasyon"],
        "anahtar_bilesenler": ["folliküler karsinom", "folliküler adenom", "tiroid malignite kriteri"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji",
        "ozgulluk_agirligi": 4.0
    },
    "graves hastalığı": {
        "turkce": "Graves Basedow hastalığı",
        "latin": "Morbus Basedow",
        "esanlamlilar": ["diffüz toksik guatr", "ekzoftalmik guatr"],
        "anahtar_bilesenler": ["trab", "tsh reseptör antikoru", "ekzoftalmus", "pretibiyal miksödem", "hipertiroidi"],
        "kurul": "TIP320",
        "brans": "İç Hastalıkları / Tıbbi Patoloji",
        "ozgulluk_agirligi": 3.8
    },
    "feokromositoma": {
        "turkce": "Feokromositoma",
        "latin": "Phaeochromocytoma",
        "esanlamlilar": ["adrenal medülla tümörü", "paraganglioma"],
        "anahtar_bilesenler": ["katekolamin", "vma", "vanilmandelik asit", "hipertansif kriz", "men 2", "zellballen"],
        "kurul": "TIP320",
        "brans": "Tıbbi Patoloji / Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.2
    },
    # Hematoloji & Hemostaz
    "hemartroz": {
        "turkce": "Eklem içi kanama",
        "latin": "Haemarthros",
        "esanlamlilar": ["eklem içi hematom", "eklem boşluğunda kan toplanması"],
        "anahtar_bilesenler": ["faktör viii", "faktör ix", "hemofili a", "hemofili b", "sekonder hemostaz"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 4.5
    },
    "hemofili": {
        "turkce": "Hemofili",
        "latin": "Haemophilia",
        "esanlamlilar": ["pıhtılaşma faktör eksikliği", "koagülopati"],
        "anahtar_bilesenler": ["hemartroz", "aptt uzaması", "faktör 8", "faktör 9", "x'e bağlı resesif"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 3.9
    },
    "peteşi": {
        "turkce": "Noktasal cilt kanaması",
        "latin": "Petechiae",
        "esanlamlilar": ["topluiğne başı kanama", "kapiller hemoraji"],
        "anahtar_bilesenler": ["trombositopeni", "primer hemostaz", "itp", "purpura"],
        "kurul": "TIP360",
        "brans": "İç Hastalıkları (Hematoloji)",
        "ozgulluk_agirligi": 3.0
    },
    "kml": {
        "turkce": "Kronik Miyeloid Lösemi",
        "latin": "Leukaemia myeloidea chronica",
        "esanlamlilar": ["cml", "kronik miyelojen lösemi"],
        "anahtar_bilesenler": ["philadelphia kromozomu", "t(9;22)", "bcr-abl", "tirozin kinaz", "imatinib"],
        "kurul": "TIP360",
        "brans": "Tıbbi Genetik / Hematoloji",
        "ozgulluk_agirligi": 4.8
    },
    # Farmakoloji & Antibiyotikler
    "nistatin": {
        "turkce": "Nistatin",
        "latin": "Nystatinum",
        "esanlamlilar": ["poliyen antifungal", "topikal mikostatik"],
        "anahtar_bilesenler": ["ergosterol", "topikal antifungal", "parenteral toksik", "kandidiyazis", "pamukçuk"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.2
    },
    "fosfomisin": {
        "turkce": "Fosfomisin",
        "latin": "Fosfomycinum",
        "esanlamlilar": ["monurol", "epoksit antibiyotik"],
        "anahtar_bilesenler": ["enolpiruvat transferaz", "murA", "hücre duvarı ilk basamak", "akut sistit"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.6
    },
    "imipenem": {
        "turkce": "İmipenem",
        "latin": "Imipenemum",
        "esanlamlilar": ["karbapenem antibiyotik"],
        "anahtar_bilesenler": ["dehidropeptidaz-1", "silastatin", "nefrotoksik metabolit", "geniş spektrum"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.7
    },
    "tetrasiklin": {
        "turkce": "Tetrasiklin / Doksisiklin",
        "latin": "Tetracyclinum",
        "esanlamlilar": ["doksisiklin", "minosiklin"],
        "anahtar_bilesenler": ["şelasyon", "iki değerlikli katyonlar", "kalsiyum", "diş boyanması", "30s ribozom"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 3.9
    },
    "kloramfenikol": {
        "turkce": "Kloramfenikol",
        "latin": "Chloramphenicolum",
        "esanlamlilar": ["fenikol antibiyotik"],
        "anahtar_bilesenler": ["gri bebek sendromu", "glukuronil transferaz", "aplastik anemi", "50s ribozom"],
        "kurul": "TIP360",
        "brans": "Tıbbi Farmakoloji / Pediatri",
        "ozgulluk_agirligi": 4.9
    },
    "metotreksat": {
        "turkce": "Metotreksat",
        "latin": "Methotrexatum",
        "esanlamlilar": ["mtx", "folat antagonisti"],
        "anahtar_bilesenler": ["dihidrofolat redüktaz", "dhfr", "lökovorin", "s fazı", "timidilat sentaz"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji",
        "ozgulluk_agirligi": 4.4
    },
    "nitrogliserin": {
        "turkce": "Nitrogliserin / Gliseril Trinitrat",
        "latin": "Glyceroli trinitras",
        "esanlamlilar": ["gtn", "sublingual nitrat"],
        "anahtar_bilesenler": ["hepatik ilk geçiş etkisi", "sublingual", "venodilatasyon", "ön yük azalması", "anjina"],
        "kurul": "TIP350",
        "brans": "Tıbbi Farmakoloji / Kardiyoloji",
        "ozgulluk_agirligi": 4.1
    },
    # Nöroloji & Koma
    "glasgow koma skalası": {
        "turkce": "Glasgow Koma Skalası (GKS)",
        "latin": "Coma scale Glasgow",
        "esanlamlilar": ["gks", "gcs"],
        "anahtar_bilesenler": ["göz açma", "sözel yanıt", "motor yanıt", "kafa travması", "bilinç düzeyi"],
        "kurul": "TIP340",
        "brans": "Nöroloji / Acil Tıp",
        "ozgulluk_agirligi": 4.0
    },
    "crush sendromu": {
        "turkce": "Ezilme / Göçük Sendromu",
        "latin": "Syndroma contusionis",
        "esanlamlilar": ["bywaters sendromu", "kompresyon travması"],
        "anahtar_bilesenler": ["rabdomiyoliz", "miyoglobinüri", "hiperkalemi", "akut böbrek yetmezliği", "kompartman"],
        "kurul": "TIP360",
        "brans": "Acil Tıp / Ortopedi",
        "ozgulluk_agirligi": 4.6
    }
}


def build_full_thesaurus():
    """Müfredat ve temel tıbbi ontolojiyi birleştirip sözlüğü kaydeder."""
    thesaurus = dict(BASE_THESAURUS)
    if CURRICULUM_FILE.exists():
        curric = json.loads(CURRICULUM_FILE.read_text(encoding="utf-8"))
        for cid, cinfo in curric.get("committees", {}).items():
            for topic in cinfo.get("core_topics", []):
                t_lower = topic.lower().strip()
                if t_lower not in thesaurus:
                    thesaurus[t_lower] = {
                        "turkce": topic,
                        "latin": topic,
                        "esanlamlilar": [t_lower.replace(" ve ", " "), t_lower.split("(")[0].strip()],
                        "anahtar_bilesenler": [w for w in re.split(r'[\s,\(\)]+', t_lower) if len(w) > 4][:5],
                        "kurul": cid,
                        "brans": cinfo.get("departments", ["Tıp Fakültesi"])[0],
                        "ozgulluk_agirligi": 3.0
                    }
    THESAURUS_FILE.write_text(json.dumps(thesaurus, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[Thesaurus ✓] {len(thesaurus)} terim ve eş anlamlı kümesi {THESAURUS_FILE.name} dosyasına yazıldı.")
    return thesaurus


def extract_terms_from_text(text: str, thesaurus: Dict[str, dict]) -> Set[str]:
    """Metin içindeki bilinen tıbbi terimleri ve eş anlamlılarını saptar."""
    text_lower = text.lower()
    found_terms = set()
    for main_term, meta in thesaurus.items():
        if main_term in text_lower:
            found_terms.add(main_term)
            continue
        for syn in meta.get("esanlamlilar", []):
            if syn and syn in text_lower:
                found_terms.add(main_term)
                break
        for comp in meta.get("anahtar_bilesenler", []):
            if comp and len(comp) > 4 and comp in text_lower:
                found_terms.add(main_term)
                break
    return found_terms


def calculate_anchor_score(q_terms: Set[str], chunk_terms: Set[str], chunk_text: str, thesaurus: Dict[str, dict]) -> float:
    """
    Co-occurrence (Birlikte Görünme) Skorlama Algoritması:
    1. Ortak terimlerin ağırlıklı toplamı
    2. Jaccard benzerliği (küme örtüşme oranı)
    3. Terimlerin chunk içindeki sıklığı (density)
    """
    common = q_terms.intersection(chunk_terms)
    if not common:
        return 0.0

    # 1. Ağırlıklı Terim Skoru
    weighted_score = sum(thesaurus.get(t, {}).get("ozgulluk_agirligi", 2.0) for t in common)

    # 2. Jaccard Benzerliği
    jaccard = len(common) / len(q_terms.union(chunk_terms))

    # 3. Yoğunluk (Density): Sorudaki kilit terimlerin bu slaytta kaç kez tekrar ettiği
    chunk_lower = chunk_text.lower()
    total_occurrences = sum(chunk_lower.count(t) for t in common)
    density_factor = min(2.5, 1.0 + (total_occurrences * 0.15))

    final_score = (weighted_score * 1.5) + (jaccard * 10.0) + density_factor
    return round(final_score, 3)


def run_phase_6_5():
    print("=" * 75)
    print("🔬 FAZ 6.5: TIBBİ SÖZLÜK (THESAURUS) VE CO-OCCURRENCE KANIT MOTORU")
    print("=" * 75)

    thesaurus = build_full_thesaurus()

    # Çıkmış soruları ve ders slaytlarını tara
    q_files = list(DB_QUESTIONS.glob("*.jsonl"))
    chunk_files = list(DB_CHUNKS.glob("*.jsonl"))

    print(f"[Havuz] {len(q_files)} soru dosyası ve {len(chunk_files)} ders slayt destesi taranıyor...")

    # Slayt chunk'larını indeksle (hafif önbellek)
    print("-> Slayt chunk'ları tıbbi terim süzgecinden geçiriliyor...")
    slide_chunks = []
    for cf in chunk_files[:120]:  # İlk 120 slayt dosyasını tara
        with open(cf, "r", encoding="utf-8") as fp:
            for line in fp:
                if not line.strip():
                    continue
                try:
                    chk = json.loads(line)
                    txt = chk.get("text", "")
                    if len(txt) > 40:
                        c_terms = extract_terms_from_text(txt, thesaurus)
                        if c_terms:
                            slide_chunks.append({
                                "chunk_id": chk.get("chunk_id") or chk.get("id"),
                                "source_id": chk.get("source_id"),
                                "ders": chk.get("ders"),
                                "page": chk.get("page"),
                                "text": txt,
                                "terms": c_terms
                            })
                except Exception:
                    pass

    print(f"-> İndekslenen terim zengini slayt parçası: {len(slide_chunks)}")

    # Soruları tara ve en yüksek co-occurrence skorlu slaytı kancala
    anchors_count = 0
    with open(ANCHORS_FILE, "w", encoding="utf-8") as out_fp:
        for qf in q_files:
            with open(qf, "r", encoding="utf-8") as fp:
                for line in fp:
                    if not line.strip():
                        continue
                    try:
                        q = json.loads(line)
                    except Exception:
                        continue

                    qid = q.get("question_id") or q.get("id")
                    stem = q.get("stem", "")
                    if not stem or len(stem) < 20:
                        continue

                    # Soru ve şıklardaki terimleri çıkar
                    full_q_text = stem + " " + " ".join(str(v) for v in q.get("options", {}).values())
                    q_terms = extract_terms_from_text(full_q_text, thesaurus)

                    if not q_terms:
                        continue

                    # Slayt chunk'ları arasında en yüksek eşleşme (co-occurrence) skorunu bul
                    best_chunk = None
                    best_score = 0.0

                    for chk in slide_chunks:
                        score = calculate_anchor_score(q_terms, chk["terms"], chk["text"], thesaurus)
                        if score > best_score:
                            best_score = score
                            best_chunk = chk

                    if best_chunk and best_score >= 4.0:
                        anchor_record = {
                            "question_id": qid,
                            "stem": stem[:120],
                            "common_medical_terms": list(q_terms.intersection(best_chunk["terms"])),
                            "co_occurrence_score": best_score,
                            "gold_slide": {
                                "chunk_id": best_chunk["chunk_id"],
                                "source_id": best_chunk["source_id"],
                                "ders": best_chunk["ders"],
                                "page": best_chunk["page"],
                                "text_snippet": best_chunk["text"][:250]
                            },
                            "anchored_at": "2026-10-05T15:25:00Z"
                        }
                        out_fp.write(json.dumps(anchor_record, ensure_ascii=False) + "\n")
                        anchors_count += 1

    STATE_FILE.write_text(json.dumps({
        "status": "completed",
        "total_anchors": anchors_count,
        "thesaurus_terms": len(thesaurus),
        "indexed_chunks": len(slide_chunks)
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✨ FAZ 6.5 BAŞARIYLA TAMAMLANDI: {anchors_count} soru-ders notu köprüsü (anchor) kuruldu!")
    print(f"Kalıcı Veri: {ANCHORS_FILE}")


if __name__ == "__main__":
    run_phase_6_5()
