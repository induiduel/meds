#!/usr/bin/env python3
"""
# ARŞİV (2026-10-12): Yerini src/services/poolClusterService.ts aldı (sunucu içinde, ders/konu/terim tabanlı). Çağıran yok.
MeDSor Soru Havuzu Kümeleme, Eşleme ve Öneri Taslak Otomasyonu
Ücretsiz Yapay Zeka Ajanları ile Arka Planda Eşleme ve Birleştirme

Kural:
- Soru havuzundaki benzer/parçalı soruları gruplar (10 soru taslağı birleştirildi vb.).
- Her küme için tamamlanmış öneri soru taslağı (kök, şıklar, cevap, açıklama) oluşturur.
- Durum daima 'proposal' (öneri) kalır.
- Öğrenciler bu öneriye yalnızca ekleme yapabilir; asla silemez veya kabul edemez.
"""

import os
import sys
import json
import re
import time
import urllib.request
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = SRC_DIR / "data"
POOL_FILE = DATA_DIR / "pool_questions.json"
FALLBACK_POOL_FILE = DATA_DIR / "database.json"
OUTPUT_FILE = DATA_DIR / "pool_question_clusters.json"
ENV_PATH = BASE_DIR / ".env"

def load_env() -> Dict[str, str]:
    env = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

ENV = load_env()

GEMINI_KEYS = [
    ENV.get(k) for k in [
        "GEMINI_FREE_KEY_2", "GEMINI_FREE_KEY_3", "GEMINI_FREE_KEY_4",
        "GEMINI_FREE_KEY_5", "GEMINI_FREE_KEY_6", "GEMINI_FREE_KEY_7",
        "GEMINI_API_KEY"
    ] if ENV.get(k) and not ENV.get(k).startswith("MY_")
]
GROQ_KEYS = [
    ENV.get(k) for k in ["GROQ_API_KEY", "GROQ_API_KEY_2"]
    if ENV.get(k) and not ENV.get(k).startswith("MY_")
]

gemini_key_idx = 0
groq_key_idx = 0

def get_next_gemini_key():
    global gemini_key_idx
    if not GEMINI_KEYS: return None
    k = GEMINI_KEYS[gemini_key_idx % len(GEMINI_KEYS)]
    gemini_key_idx += 1
    return k

def get_next_groq_key():
    global groq_key_idx
    if not GROQ_KEYS: return None
    k = GROQ_KEYS[groq_key_idx % len(GROQ_KEYS)]
    groq_key_idx += 1
    return k

def load_pool_questions() -> List[Dict[str, Any]]:
    # 1. meds/data/questions.json dene
    data_questions_file = BASE_DIR / "data" / "questions.json"
    if data_questions_file.exists():
        try:
            with open(data_questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    questions = data.get("questions", [])
                    if questions:
                        return questions
                elif isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass

    # 2. pool_questions.json dene
    if POOL_FILE.exists():
        try:
            with open(POOL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass

    # 3. database.json dene
    if FALLBACK_POOL_FILE.exists():
        try:
            with open(FALLBACK_POOL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    questions = data.get("questions", [])
                    if questions:
                        return questions
                elif isinstance(data, list):
                    return data
        except Exception:
            pass

    return []

def question_text(q: Dict[str, Any]) -> str:
    """Sorunun öğrenci metni: stem/title yoksa kök ve ipucu parçaları."""
    t = q.get("stem") or q.get("title") or ""
    if t:
        return t
    frs = [f.get("text", "") for f in (q.get("fragments") or []) if f.get("type") in ("stem", "clue")]
    return " ".join(x for x in frs if x).strip()


def question_options(q: Dict[str, Any]) -> List[Dict[str, str]]:
    return [{"key": o.get("key"), "text": (o.get("text") or "").strip()} for o in (q.get("options") or []) if (o.get("text") or "").strip()]


MISSING_OPTION = "[EKSİK ŞIK]"


def evidence_only_proposal(chunk: List[Dict[str, Any]]) -> Dict[str, Any]:
    """AI yoksa uydurma yok: eksikler [EKSİK ŞIK], cevap boş. Kümedeki sorular aynı soru olduğu doğrulanmadığı
    için şıklar yalnız tek sorulu kümede alınır (farklı soruların şıkları karıştırılmaz)."""
    by_key: Dict[str, Dict[str, Any]] = {}
    for q in (chunk if len(chunk) == 1 else []):
        for o in question_options(q):
            k = str(o["key"] or "").upper()
            if k in "ABCDE" and len(k) == 1:
                by_key.setdefault(k, {}).setdefault(o["text"], 0)
                by_key[k][o["text"]] += 1
    opts = []
    for k in "ABCDE":
        if k in by_key:
            text = max(by_key[k].items(), key=lambda kv: kv[1])[0]
            opts.append({"key": k, "text": text})
        else:
            opts.append({"key": k, "text": MISSING_OPTION})
    first = next((question_text(q) for q in chunk if question_text(q)), "")
    return {
        "clusterTitle": f"Birleştirilmemiş soru grubu: {first[:40]}..." if first else "Birleştirilmemiş soru grubu",
        "discipline": chunk[0].get("discipline") or "Belirsiz",
        "mergedStem": f"[EKSİK KÖK] {len(chunk)} öğrenci parçası; yapay zekâ birleştirmesi henüz yapılmadı.",
        "mergedOptions": opts,
        "claimedAnswer": "",
        "explanation": "",
        "aiMerged": False,
    }


def group_questions_into_clusters(questions: List[Dict[str, Any]], max_per_cluster: int = 10) -> List[Dict[str, Any]]:
    """Soruları komite ve konu anahtar kelimelerine göre mantıksal gruplara böler."""
    groups_by_key: Dict[str, List[Dict[str, Any]]] = {}

    for q in questions:
        cid = q.get("committeeId") or "genel-kurul"
        stem = question_text(q)
        # Temel tıbbi anahtar kelime çıkarımı
        words = re.findall(r'\b[a-zA-ZğüşıöçĞÜŞİÖÇ]{4,}\b', stem.lower())
        topic = words[0] if words else "klinik-muhasebe"

        key = f"{cid}_{topic}"
        if key not in groups_by_key:
            groups_by_key[key] = []
        groups_by_key[key].append(q)

    # 3 ila 10 soru içeren grupları veya büyükleri 10'luk parçalara böl
    clusters = []
    cluster_idx = 1

    for key, q_list in groups_by_key.items():
        for i in range(0, len(q_list), max_per_cluster):
            chunk = q_list[i : i + max_per_cluster]
            first_q = chunk[0]
            cid = first_q.get("committeeId") or "donem3-kurul1"
            clusters.append({
                "cluster_index": cluster_idx,
                "committeeId": cid,
                "questions": chunk
            })
            cluster_idx += 1

    return clusters

def generate_cluster_proposal_with_ai(cluster: Dict[str, Any]) -> Dict[str, Any]:
    chunk = cluster["questions"]
    cid = cluster["committeeId"]

    stems_and_opts = []
    for idx, q in enumerate(chunk, 1):
        q_stem = question_text(q) or "(kök yok)"
        q_opts = q.get("options") or []
        opts_text = ", ".join([f"{o.get('key')}: {o.get('text')}" for o in q_opts]) if isinstance(q_opts, list) else str(q_opts)
        stems_and_opts.append(f"Parça #{idx}: {q_stem} | Şıklar: {opts_text}")

    context_str = "\n".join(stems_and_opts)

    prompt = f"""
Sen bir Tıp Fakültesi Sınav Komisyonu Akademisyenisin.
Aşağıda öğrencilerin girdiği {len(chunk)} adet eksik/parçalı soru taslağı bulunmaktadır.
Bu parçaları analiz et, ortak konuyu tespit et ve YALNIZ parçalarda bulunan bilgiyle tek bir soru taslağında birleştir. Eksik kalan yeri doldurma, işaretle.

KURALLAR
1. Yanıtın SADECE geçerli bir JSON objesi olmalıdır.
2. UYDURMA YOK: Öğrenci parçalarında geçmeyen şık yazma; o şıkkın metni "[EKSİK ŞIK]" olsun. Kökte eksik kısım varsa "[EKSİK KÖK PARÇASI]" yaz.
3. Parçalar farklı soruları anlatıyorsa birleştirme; "mergedStem" alanına "[BİRLEŞTİRİLEMEDİ] parçalar farklı sorulara ait" yaz.
4. "claimedAnswer": yalnız öğrencilerin işaretlediği/iddia ettiği harf; kanıt yoksa "" (boş).
5. Parçalarda "değildir / yanlıştır / beklenmez" geçiyorsa kökü olumsuz kur.

İstenen JSON formatı:
{{
  "clusterTitle": "Birleştirilen konunun açık tıbbi başlığı (örn: Akut Pankreatit Tanı Kriterleri ve Ranson Skoru)",
  "discipline": "İlgili ana bilim dalı (örn: Genel Cerrahi, Patoloji, Farmakoloji)",
  "mergedStem": "Öğrenci parçalarının birleşimiyle eksiksiz kurgulanmış, net, tek bir vaka veya mekanizma soru kökü",
  "mergedOptions": [
    {{"key": "A", "text": "A şıkkı metni"}},
    {{"key": "B", "text": "B şıkkı metni"}},
    {{"key": "C", "text": "C şıkkı metni"}},
    {{"key": "D", "text": "D şıkkı metni"}},
    {{"key": "E", "text": "E şıkkı metni"}}
  ],
  "claimedAnswer": "Öğrencilerin iddia ettiği harf ya da \"\"",
  "explanation": "Hangi parçanın neyi desteklediği; eksikler ve çelişkiler"
}}

ÖĞRENCİ PARÇALARI ({len(chunk)} soru birleştiriliyor):
{context_str[:2500]}
"""

    # 1. Gemini (yalnız ücretsiz anahtarlar)
    gemini_key = get_next_gemini_key()
    if gemini_key:
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={gemini_key}"
            req_data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json", "temperature": 0, "thinkingConfig": {"thinkingLevel": "low"}}
            }).encode('utf-8')

            req = urllib.request.Request(gemini_url, data=req_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as res:
                resp_json = json.loads(res.read().decode('utf-8'))
                raw_text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(raw_text)
        except Exception:
            pass

    # 2. Groq (ücretsiz) yedek
    groq_key = get_next_groq_key()
    if groq_key:
        try:
            req_data = json.dumps({
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {"role": "system", "content": "You are a professional medical exam committee expert. Output strictly JSON."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.2
            }).encode('utf-8')

            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=req_data,
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=40) as res:
                resp_json = json.loads(res.read().decode('utf-8'))
                raw_text = resp_json["choices"][0]["message"]["content"]
                return json.loads(raw_text)
        except Exception:
            pass

    # Yapay zekâ yanıt vermedi: yalnız kanıta dayalı taslak (uydurma şık/cevap yok)
    return evidence_only_proposal(chunk)

def run_clustering_pipeline():
    print("=" * 65)
    print("🚀 Soru Havuzu Kümeleme & Öneri Taslak Otomasyonu Başlatılıyor")
    print("=" * 65)

    questions = load_pool_questions()
    if not questions:
        print("[-] Soru havuzunda işlenecek soru bulunamadı.")
        return

    print(f"[*] Toplam {len(questions)} havuz sorusu taranıyor...")
    clusters = group_questions_into_clusters(questions)
    print(f"[+] Toplam {len(clusters)} adet mantıksal soru kümesi oluşturuldu.")

    existing_clusters: Dict[str, Dict[str, Any]] = {}
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for c in data:
                    existing_clusters[c["id"]] = c
        except Exception:
            pass

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results = []

    for c in clusters:
        q_ids = [str(q.get("id") or idx) for idx, q in enumerate(c["questions"])]
        cid = c["committeeId"]
        cluster_id = f"cluster-{cid}-{c['cluster_index']}"

        # Önceden işlenmiş ve korunmuş katkılar varsa al
        existing = existing_clusters.get(cluster_id)
        existing_contributions = existing.get("studentContributions", []) if existing else []

        print(f"[*] Küme {cluster_id} işleniyor ({len(q_ids)} soru parçası)...")
        proposal_data = generate_cluster_proposal_with_ai(c)
        if proposal_data.get("aiMerged") is False and existing and existing.get("aiMerged"):
            print(f"    [!] AI yanıt vermedi; önceki AI birleştirmesi korunuyor.")
            results.append(existing)
            continue
        got = {str(o.get("key", "")).upper(): (o.get("text") or "").strip() for o in (proposal_data.get("mergedOptions") or []) if isinstance(o, dict)}
        proposal_data["mergedOptions"] = [{"key": k, "text": got.get(k) or MISSING_OPTION} for k in "ABCDE"]
        ca = str(proposal_data.get("claimedAnswer") or "").strip().upper()
        proposal_data["claimedAnswer"] = ca if ca in ("A", "B", "C", "D", "E") else ""

        cluster_obj = {
            "id": cluster_id,
            "clusterTitle": proposal_data.get("clusterTitle") or f"Öneri Grubu #{c['cluster_index']}",
            "committeeId": cid,
            "discipline": proposal_data.get("discipline") or "Tıp",
            "sourceQuestionIds": q_ids,
            "mergedQuestionCount": len(q_ids),
            "mergedStem": proposal_data.get("mergedStem") or "",
            "mergedOptions": proposal_data.get("mergedOptions") or [],
            "claimedAnswer": proposal_data.get("claimedAnswer") or "",
            "aiMerged": proposal_data.get("aiMerged", True),
            "explanation": proposal_data.get("explanation") or "",
            "status": "proposal", # DAİMA ÖNERİ STATÜSÜNDE KALIR
            "isLockedForDeletion": True, # ÖĞRENCİLER SİLEMEZ VEYA ONAYLAYAMAZ
            "studentContributions": existing_contributions,
            "createdAt": existing.get("createdAt") if existing else now_iso,
            "updatedAt": now_iso
        }

        existing_clusters[cluster_id] = cluster_obj
        results.append(cluster_obj)

        # Anında diske yaz
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(list(existing_clusters.values()), f, ensure_ascii=False, indent=2)

        time.sleep(1)

    print("=" * 65)
    print(f"✅ Tamamlandı! {len(results)} adet birleştirilmiş soru taslağı {OUTPUT_FILE.name} dosyasına yazıldı.")
    print("=" * 65)

if __name__ == "__main__":
    run_clustering_pipeline()
