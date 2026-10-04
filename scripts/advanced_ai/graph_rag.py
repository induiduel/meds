"""
GraphRAG & Tıbbi Bilgi Grafı (Medical Knowledge Graph)
- Düğümler (Nodes): Hastalık, Belirti, İlaç, Gen, Kurul, Ders, Konu, Soru ID
- Kenarlar (Edges): NEDEN_OLUR, TEDAVİ_EDER, İLİŞKİLİDİR, BULUNUR, SORULMUŞTUR
"""
import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Any

class MedicalGraphRAG:
    def __init__(self, graph_path: Path = None):
        self.graph = nx.DiGraph()
        self.graph_path = Path(graph_path) if graph_path else None
        if self.graph_path and self.graph_path.exists():
            self.load()

    def add_lecture_entities(self, source_id: str, ders: str, konu: str, metadata: Dict[str, Any]):
        """Slayt metadatası üzerinden grafiğe tıbbi varlıkları bağlar"""
        # Ders ve konu düğümleri
        if ders:
            self.graph.add_node(f"Ders:{ders}", type="Ders", name=ders)
        if konu:
            self.graph.add_node(f"Konu:{konu}", type="Konu", name=konu)
            if ders:
                self.graph.add_edge(f"Ders:{ders}", f"Konu:{konu}", relation="İÇERİR")

        # Hastalıklar, İlaçlar, Belirtiler
        for h in metadata.get("hastaliklar", []):
            h_id = f"Hastalik:{h}"
            self.graph.add_node(h_id, type="Hastalik", name=h)
            if konu:
                self.graph.add_edge(f"Konu:{konu}", h_id, relation="BAHSEDER")
            
            # Belirtiler ile bağla
            for b in metadata.get("belirtiler", []):
                b_id = f"Belirti:{b}"
                self.graph.add_node(b_id, type="Belirti", name=b)
                self.graph.add_edge(h_id, b_id, relation="SEMPTOM_GÖSTERİR")

            # İlaçlar ile bağla
            for i in metadata.get("ilaclar", []):
                i_id = f"Ilac:{i}"
                self.graph.add_node(i_id, type="Ilac", name=i)
                self.graph.add_edge(i_id, h_id, relation="TEDAVİ_EDER")

    def add_question(self, qid: str, stem: str, answer: str, linked_source: str, entities: List[str]):
        """Soruyu ve geçtiği tıbbi varlıkları grafiğe ekler"""
        q_node = f"Soru:{qid}"
        self.graph.add_node(q_node, type="Soru", id=qid, stem=stem[:100], answer=answer)
        if linked_source:
            self.graph.add_edge(q_node, f"Kaynak:{linked_source}", relation="REFERANS_ALIR")
        
        for ent in entities:
            # Grafikte mevcut olan herhangi bir varlıkla eşleşiyorsa bağ kur
            for node in self.graph.nodes:
                if ent.lower() in node.lower():
                    self.graph.add_edge(q_node, node, relation="SORGULAR")

    def query_subgraph(self, term: str, depth: int = 2) -> Dict[str, Any]:
        """Tıbbi bir terim için bilgi grafından alt ağ (subgraph) çıkarır"""
        matched_nodes = [n for n in self.graph.nodes if term.lower() in n.lower()]
        if not matched_nodes:
            return {"nodes": [], "edges": []}

        subgraph_nodes = set(matched_nodes)
        for node in matched_nodes:
            # N derinliğinde komşuları topla
            neighbors = nx.single_source_shortest_path_length(self.graph.to_undirected(), node, cutoff=depth)
            subgraph_nodes.update(neighbors.keys())

        sub = self.graph.subgraph(subgraph_nodes)
        nodes_out = [{"id": n, "data": sub.nodes[n]} for n in sub.nodes]
        edges_out = [{"source": u, "target": v, "relation": sub.edges[u, v].get("relation", "BAĞLI")} for u, v in sub.edges]
        return {"nodes": nodes_out, "edges": edges_out}

    def save(self, path: Path = None):
        target = path or self.graph_path
        if target:
            target.parent.mkdir(parents=True, exist_ok=True)
            data = nx.node_link_data(self.graph)
            target.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def load(self, path: Path = None):
        target = path or self.graph_path
        if target and target.exists():
            data = json.loads(target.read_text())
            self.graph = nx.node_link_graph(data)
