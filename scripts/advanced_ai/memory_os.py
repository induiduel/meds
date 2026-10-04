"""
MemGPT / Hiyerarşik Bellek Katmanı (MedSoru)
- Core Memory: Kullanıcı/Öğrenci profili, hedefler, zayıf kalınan tıbbi kurullar/dersler
- Recall Memory: Son etkileşimler, çözülen sorular, oturum bağlamı
- Archival Memory: Milyonlarca slayt chunk'ı ve doğrulanmış soru arşivi
"""
import json
import time
from pathlib import Path
from pydantic import BaseModel, Field

class StudentProfile(BaseModel):
    user_id: str = "default_student"
    donem: int = 3
    target_score: int = 85
    weak_topics: list[str] = Field(default_factory=list)
    mastered_topics: list[str] = Field(default_factory=list)
    notes: str = ""

class MemoryItem(BaseModel):
    timestamp: float
    role: str
    content: str
    metadata: dict = Field(default_factory=dict)

class HierarchicalMemoryOS:
    def __init__(self, storage_dir: Path):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.profile_path = self.storage_dir / "student_profile.json"
        self.recall_path = self.storage_dir / "recall_memory.jsonl"
        self.profile = self._load_profile()

    def _load_profile(self) -> StudentProfile:
        if self.profile_path.exists():
            try:
                return StudentProfile.model_validate_json(self.profile_path.read_text())
            except Exception:
                pass
        return StudentProfile()

    def save_profile(self):
        self.profile_path.write_text(self.profile.model_dump_json(indent=2))

    def update_weak_topic(self, topic: str):
        if topic not in self.profile.weak_topics:
            self.profile.weak_topics.append(topic)
            self.save_profile()

    def append_recall(self, role: str, content: str, metadata: dict = None):
        item = MemoryItem(
            timestamp=time.time(),
            role=role,
            content=content,
            metadata=metadata or {}
        )
        with open(self.recall_path, "a", encoding="utf-8") as f:
            f.write(item.model_dump_json() + "\n")

    def get_recent_recall(self, limit: int = 10) -> list[MemoryItem]:
        if not self.recall_path.exists():
            return []
        lines = self.recall_path.read_text(encoding="utf-8").strip().split("\n")
        items = []
        for line in lines[-limit:]:
            if line.strip():
                try:
                    items.append(MemoryItem.model_validate_json(line))
                except Exception:
                    pass
        return items

    def render_context(self) -> str:
        """LLM promptuna enjekte edilecek Core Memory özeti"""
        weak = ", ".join(self.profile.weak_topics) if self.profile.weak_topics else "Henüz tespit edilmedi"
        mastered = ", ".join(self.profile.mastered_topics) if self.profile.mastered_topics else "Yok"
        return (
            f"[ÖĞRENCİ BELLEK SİSTEMİ / MEMGPT CORE MEMORY]\n"
            f"- Dönem: {self.profile.donem}\n"
            f"- Zayıf Görülen Konular: {weak}\n"
            f"- Hakim Olunan Konular: {mastered}\n"
            f"- Öğrenci Notu: {self.profile.notes or 'Belirtilmedi'}\n"
        )
