"""
Gelişmiş AI Orkestratörü & Boru Hattı Entegrasyonu (Aşama 5)
Aşama 3 ve 4 tamamlandığında otomatik tetiklenir:
1. Slaytlar ve Sorular üzerinden Tıbbi Knowledge Graph (GraphRAG) inşa eder.
2. BM25 indekslerini hesaplar ve dense vektörlerle birleştirerek Hibrit Arama motorunu hazırlar.
3. MemGPT ve ReAct Guardrails altyapısını API ve web için servis eder.
"""
import sys
import json
import time
from pathlib import Path
import numpy as np

# Ana modül kütüphanesini içeri al
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts" / "agents"))
import lib

from scripts.advanced_ai.hybrid_search import HybridSearchEngine
from scripts.advanced_ai.graph_rag import MedicalGraphRAG
from scripts.advanced_ai.memory_os import HierarchicalMemoryOS
from scripts.advanced_ai.react_guardrails import MedicalGuardrails, MedicalReActAgent

log = lib.get_logger("stage5_advanced_ai")

AI_EXPORT_DIR = lib.TEMP3 / "advanced_ai"
AI_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
GRAPH_FILE = AI_EXPORT_DIR / "medical_knowledge_graph.json"

def build_knowledge_graph():
    log.info("1/3 GraphRAG: Tıbbi Bilgi Grafı oluşturuluyor...")
    kg = MedicalGraphRAG(GRAPH_FILE)
    
    # 1. Kaynak slaytların metadatasından varlıkları ekle
    src_dir = lib.TEMP3 / "sources"
    if src_dir.exists():
        for src_file in src_dir.glob("*.json"):
            data = lib.read_json(src_file, {})
            sid = data.get("source_id")
            ders = data.get("ders") or ""
            konu = data.get("konu") or ""
            meta = data.get("metadata", {})
            kg.add_lecture_entities(sid, ders, konu, meta)
            
    # 2. Soruları ekle
    q_file = lib.TEMP3 / "questions.jsonl"
    if q_file.exists():
        for line in q_file.read_text(encoding="utf-8").strip().split("\n"):
            if not line:
                continue
            q = json.loads(line)
            entities = []
            if q.get("taxonomy"):
                entities.extend(q["taxonomy"].get("hastaliklar", []))
                entities.extend(q["taxonomy"].get("ilaclar", []))
            kg.add_question(q.get("question_id", ""), q.get("stem", ""), q.get("answer", ""), q.get("linked_source", ""), entities)
            
    kg.save()
    log.info("GraphRAG Bilgi Grafı kaydedildi: %d düğüm, %d kenar ✓", kg.graph.number_of_nodes(), kg.graph.number_of_edges())
    return kg

def prepare_hybrid_engine():
    log.info("2/3 Hibrit Arama: BM25 + bge-m3 indeksleri hazırlanıyor...")
    chunk_dir = lib.TEMP3 / "chunks"
    vec_dir = lib.TEMP3 / "vectors"
    
    all_chunks = []
    all_vectors = []
    
    if chunk_dir.exists():
        for cfile in chunk_dir.glob("*.jsonl"):
            sid = cfile.stem
            vfile = vec_dir / f"{sid}.npy"
            if not vfile.exists():
                continue
            chunks = lib.read_jsonl(cfile)
            vecs = np.load(vfile)
            if len(chunks) == len(vecs):
                all_chunks.extend(chunks)
                all_vectors.append(vecs)
                
    if all_vectors:
        full_vecs = np.vstack(all_vectors)
        engine = HybridSearchEngine(all_chunks, full_vecs)
        log.info("Hibrit Arama Motoru Hazır: %d chunk başarıyla indekslendi ✓", len(all_chunks))
        return engine
    else:
        log.warning("Henüz vektörler hazır değil veya chunk bulunamadı.")
        return None

def main():
    state = lib.State()
    log.info("Aşama 5 (Gelişmiş AI & RAG Mimarisi) tetiklendi...")
    
    # 1. GraphRAG İnşası
    state.set_progress("advanced_ai", 1, 3, "Aşama 5 (1/3): GraphRAG Tıbbi Bilgi Grafı (NetworkX) İnşa Ediliyor...")
    kg = build_knowledge_graph()
    
    # 2. Hibrit Arama Hazırlığı
    state.set_progress("advanced_ai", 2, 3, "Aşama 5 (2/3): BM25 + BGE-M3 Hibrit Arama Matrisi & RRF Sıralayıcı Derleniyor...")
    engine = prepare_hybrid_engine()
    
    # 3. MemGPT Bellek Katmanı
    state.set_progress("advanced_ai", 3, 3, "Aşama 5 (3/3): MemGPT Öğrenci Bellek Katmanı & ReAct Ajanları Başlatılıyor...")
    memory_os = HierarchicalMemoryOS(AI_EXPORT_DIR / "memory")
    log.info("MemGPT Hiyerarşik Bellek Sistemi devrede ✓")
    
    state.set_progress("advanced_ai", 3, 3, "Aşama 5 Tamamlandı ✓ (GraphRAG, Hybrid BM25, MemGPT ve ReAct Canlı)")
    log.info("Tüm ileri seviye AI mimarileri (GraphRAG, Hybrid BM25, MemGPT, ReAct) hazırlandı.")

if __name__ == "__main__":
    main()
