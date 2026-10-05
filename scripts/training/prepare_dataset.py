#!/usr/bin/env python3
"""
MedSoru Özel Tıp Yapay Zekası İçin İnce Ayar (Fine-Tuning) Veri Seti Hazırlayıcı.
Kaynak : meds_database/questions (2.194 doğrulanmış soru) & meds_database/chunks (amfi slayt kanıtları)
Çıktı  : meds/training_data/medsoru_train.jsonl, medsoru_val.jsonl, medsoru_alpaca_all.jsonl
Format : Standart Alpaca (instruction, input, output) & HuggingFace SFT uyumlu
"""

import argparse
import json
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if not (ROOT / "meds_database").exists():
    ROOT = Path(__file__).resolve().parents[3]

DB_QUESTIONS = ROOT / "meds_database" / "questions"
DB_CHUNKS = ROOT / "meds_database" / "chunks"
OUT_DIR = ROOT / "meds" / "training_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Standart Akademik Sistem İstemleri
SYSTEM_PROMPT_RAG = (
    "Sen Tıp Fakültesi Dönem 3 kurulları ve klinik sınavları konusunda uzmanlaşmış akademik bir tıp asistanısın. "
    "Sana sunulan amfi ders slaytı kanıtlarını ve klinik bağlamı titizlikle analiz ederek sorulan soruyu yanıtla, "
    "doğru seçeneği açıkla ve klinik/patolojik gerekçesini öğret."
)

SYSTEM_PROMPT_DIRECT = (
    "Sen Tıp Fakültesi Dönem 3 (Patoloji, Farmakoloji, Mikrobiyoloji, Dahiliye, Genel Cerrahi) kurullarında uzman bir tıp yapay zekasısın. "
    "Sorulan tıp sınav sorusunu hekimlik nosyonuna ve amfi kurul müfredatına tam sadık kalarak çöz, doğru seçeneği ve kanıt gerekçesini açıkla."
)

SYSTEM_PROMPT_SYNTHESIS = (
    "Sen Tıp Fakültesi Dönem 3 kurul sınav komitesi üyesi bir akademisyensin. "
    "Amfi slaytları ve çıkmış kurul soruları doğrultusunda konuların en kritik sınav noktalarını ve klinik püf noktalarını özetlersin."
)


class ChunkLoader:
    """Amfi slayt chunk'larını talep edildikçe önbelleğe alıp getiren sınıf."""

    def __init__(self, chunks_dir: Path):
        self.chunks_dir = chunks_dir
        self.cache: Dict[str, Dict[str, dict]] = {}

    def get_chunk(self, evidence_id: str) -> Optional[dict]:
        parts = evidence_id.split(":")
        sid = parts[0]
        if sid not in self.cache:
            chunk_file = self.chunks_dir / f"{sid}.jsonl"
            sid_dict = {}
            if chunk_file.exists():
                with open(chunk_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            c = json.loads(line)
                            cid = c.get("chunk_id") or c.get("id")
                            if cid:
                                sid_dict[cid] = c
                        except Exception:
                            continue
            self.cache[sid] = sid_dict

        return self.cache[sid].get(evidence_id)


def format_options(opts: dict) -> str:
    """Şıkları alfabetik sırada formatlar."""
    if not isinstance(opts, dict):
        return ""
    lines = []
    for k in sorted(opts.keys()):
        val = str(opts[k]).strip()
        lines.append(f"{k}) {val}")
    return "\n".join(lines)


def build_evidence_text(evidence_ids: List[str], chunk_loader: ChunkLoader) -> Tuple[str, str]:
    """Soruya ait kanıt chunk metinlerini ve başlıklarını derler."""
    texts = []
    heading = ""
    for eid in evidence_ids:
        c = chunk_loader.get_chunk(eid)
        if c:
            txt = c.get("text", "").strip()
            if txt:
                texts.append(txt)
            if not heading and c.get("heading_path"):
                hp = c.get("heading_path")
                if isinstance(hp, list):
                    heading = " > ".join(str(x) for x in hp if x)
                else:
                    heading = str(hp)

    combined_text = "\n\n---\n\n".join(texts)
    return combined_text, heading


def create_alpaca_records(q: dict, chunk_loader: ChunkLoader) -> List[dict]:
    """Tek bir doğrulanmış soru nesnesinden Alpaca eğitim örnekleri üretir."""
    stem = (q.get("stem_detailed") or q.get("stem") or "").strip()
    if not stem:
        return []

    opts = q.get("options", {})
    opts_str = format_options(opts)
    if not opts_str:
        return []

    ans = (q.get("answer") or "").strip().upper()
    if not ans:
        return []

    evidence_ids = q.get("evidence", [])
    if isinstance(evidence_ids, str):
        evidence_ids = [evidence_ids]

    ev_text, heading = build_evidence_text(evidence_ids, chunk_loader)

    ders = q.get("ders") or "Tıp Fakültesi Dönem 3"
    kurul = q.get("kurul")
    kurul_str = f"Kurul {kurul}" if kurul else "Dönem 3 Kurulu"
    meta_tag = f"[{kurul_str} - {ders.title()}]"
    if heading:
        meta_tag += f" [Konu: {heading}]"

    # Açıklama metni
    raw_exp = q.get("explanation")
    if raw_exp and len(raw_exp.strip()) > 20:
        clinical_exp = raw_exp.strip()
    elif ev_text:
        # Kanıt metninden temizlenmiş alıntı
        snippet = ev_text[:600].strip()
        clinical_exp = (
            f"Amfi ders slaytı ve kurul notlarında bu konu şu şekilde teyit edilmiştir:\n"
            f"\"\"\"\n{snippet}\n\"\"\"\n\n"
            f"Yukarıdaki kurul amfi kanıtı incelendiğinde, soruda aranan doğru ifadenin "
            f"'{ans}' seçeneğindeki ifade olduğu açıkça görülmektedir."
        )
    else:
        clinical_exp = f"Dönem 3 {ders} ders notları ve çıkmış sınav kanıtları doğrultusunda '{ans}' seçeneği teyit edilmiştir."

    tax = q.get("taxonomy_metadata") or {}
    ne_sormus = tax.get("ne_sormus")
    alt_konu = tax.get("alt_konu")

    records = []

    # 1. Format: Slayt Kanıtlı Soru Analizi (RAG / Grounded Reasoning)
    # Model, verilen slayt kanıtı eşliğinde soruyu çözmeyi ve kanıtı kullanmayı öğrenir.
    if ev_text:
        rag_input = (
            f"{meta_tag}\n\n"
            f"### İlgili Amfi Ders Slaytı Kanıtı:\n{ev_text[:1200]}\n\n"
            f"### Çıkmış Kurul Sınav Sorusu:\n{stem}\n\n"
            f"Seçenekler:\n{opts_str}"
        )
        rag_output = (
            f"Doğru Cevap: {ans}\n\n"
            f"### Klinik ve Patolojik Kanıt Gerekçesi:\n{clinical_exp}"
        )
        if ne_sormus:
            rag_output += f"\n\nAkademik Vurgu: Bu soru özellikle '{ne_sormus}' bilgisini sorgulamaktadır."

        records.append({
            "instruction": SYSTEM_PROMPT_RAG,
            "input": rag_input,
            "output": rag_output,
            "metadata": {
                "question_id": q.get("question_id"),
                "format": "rag_grounded",
                "ders": ders,
                "kurul": kurul
            }
        })

    # 2. Format: Doğrudan Sınav Sorusu Çözme (Closed-Book Expert Reasoning)
    # Model amfi bilgisi hafızasındayken soruyu çözer ve doğru cevabın gerekçesini kanıtıyla sunar.
    direct_input = f"{meta_tag}\n\n{stem}\n\nSeçenekler:\n{opts_str}"
    direct_output = (
        f"Doğru Cevap: {ans}\n\n"
        f"### Tıbbi Analiz ve Gerekçe:\n{clinical_exp}"
    )
    if ne_sormus:
        direct_output += f"\n\nSınav Analizi: {ne_sormus}"

    records.append({
        "instruction": SYSTEM_PROMPT_DIRECT,
        "input": direct_input,
        "output": direct_output,
        "metadata": {
            "question_id": q.get("question_id"),
            "format": "direct_solving",
            "ders": ders,
            "kurul": kurul
        }
    })

    # 3. Format: Hoca Tarzı Sentez / Hap Bilgi Eğitimi
    if alt_konu and ne_sormus:
        teach_input = (
            f"Bana Dönem 3 {ders.title()} kurulunda yer alan '{alt_konu}' konusundaki "
            f"en kritik noktaları ve hoca slaytlarının sınavda en çok sorduğu hususları açıkla."
        )
        teach_output = (
            f"### {alt_konu} - Sınav ve Amfi Odaklı Özet\n\n"
            f"**Hocaların En Çok Sorduğu Kritik Nokta:** {ne_sormus}\n\n"
            f"**Slayt ve Sınav Kanıtı:**\n{clinical_exp}"
        )
        records.append({
            "instruction": SYSTEM_PROMPT_SYNTHESIS,
            "input": teach_input,
            "output": teach_output,
            "metadata": {
                "question_id": q.get("question_id"),
                "format": "synthesis_summary",
                "ders": ders,
                "kurul": kurul
            }
        })

    return records


def main():
    parser = argparse.ArgumentParser(description="MedSoru Alpaca Fine-Tuning Veri Seti Hazırlayıcı")
    parser.add_argument("--val-split", type=float, default=0.10, help="Doğrulama (validation) kümesi oranı (varsayılan: 0.10)")
    parser.add_argument("--seed", type=int, default=42, help="Rastgele karıştırma tohumu (seed)")
    args = parser.parse_args()

    random.seed(args.seed)

    if not DB_QUESTIONS.exists():
        print(f"[HATA] Soru dizini bulunamadı: {DB_QUESTIONS}")
        return

    chunk_loader = ChunkLoader(DB_CHUNKS)

    question_files = sorted(list(DB_QUESTIONS.glob("*.jsonl")))
    print(f"[BİLGİ] {len(question_files)} soru dosyası taranıyor...")

    verified_questions = []
    seen_ids = set()

    for qf in question_files:
        with open(qf, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    q = json.loads(line)
                except Exception:
                    continue

                qid = q.get("question_id")
                if qid and qid in seen_ids:
                    continue

                # Sadece doğrulanmış veya düzeltilmiş VE kanıtı olan sorular
                if q.get("status") in ["verified", "fixed"] and q.get("evidence"):
                    seen_ids.add(qid)
                    verified_questions.append(q)

    print(f"[BİLGİ] Toplam {len(verified_questions)} adet benzersiz, kanıtlı ve doğrulanmış soru bulundu.")

    all_records = []
    stats = {
        "rag_grounded": 0,
        "direct_solving": 0,
        "synthesis_summary": 0,
        "total_questions": len(verified_questions)
    }

    for q in verified_questions:
        recs = create_alpaca_records(q, chunk_loader)
        for r in recs:
            fmt = r.get("metadata", {}).get("format")
            if fmt in stats:
                stats[fmt] += 1
            all_records.append(r)

    print(f"[BİLGİ] Toplam {len(all_records)} adet zenginleştirilmiş Alpaca eğitim örneği oluşturuldu.")
    print(f"  - RAG / Kanıtlı Soru Çözüm Çiftleri: {stats['rag_grounded']}")
    print(f"  - Doğrudan Kurul Soru Çözüm Çiftleri: {stats['direct_solving']}")
    print(f"  - Hoca Sentezi / Konu Anlatım Çiftleri: {stats['synthesis_summary']}")

    # Karıştır ve Train / Val Split uygula
    random.shuffle(all_records)
    val_count = int(len(all_records) * args.val_split)
    train_records = all_records[val_count:]
    val_records = all_records[:val_count]

    train_file = OUT_DIR / "medsoru_train.jsonl"
    val_file = OUT_DIR / "medsoru_val.jsonl"
    all_file = OUT_DIR / "medsoru_alpaca_all.jsonl"
    summary_file = OUT_DIR / "dataset_summary.json"

    def write_jsonl(path: Path, data: List[dict]):
        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                # Alpaca standart alanları: instruction, input, output
                alpaca_item = {
                    "instruction": item["instruction"],
                    "input": item["input"],
                    "output": item["output"]
                }
                f.write(json.dumps(alpaca_item, ensure_ascii=False) + "\n")

    write_jsonl(train_file, train_records)
    write_jsonl(val_file, val_records)
    write_jsonl(all_file, all_records)

    summary = {
        "verified_questions_count": len(verified_questions),
        "total_training_examples": len(all_records),
        "train_set_size": len(train_records),
        "validation_set_size": len(val_records),
        "formats_breakdown": stats,
        "output_files": {
            "train": str(train_file),
            "val": str(val_file),
            "all": str(all_file)
        }
    }

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[BAŞARILI] Veri seti kaydedildi:")
    print(f"  -> Eğitim Kümesi: {train_file} ({len(train_records)} örnek)")
    print(f"  -> Doğrulama Kümesi: {val_file} ({len(val_records)} örnek)")
    print(f"  -> Özet Rapor: {summary_file}")


if __name__ == "__main__":
    main()
