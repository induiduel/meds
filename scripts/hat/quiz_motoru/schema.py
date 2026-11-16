#!/usr/bin/env python3
"""Quiz Motoru Veri Şeması ve Tip Doğrulayıcısı.

Ders-bağımsız (course-agnostic), 2x Çapraz Sorgulama ve Active Recall formatını
doğrulayan Pydantic/Dataclass ve JSON yardımcıları.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Literal, Any
import json

# Bilgi Kategorileri
KNOWLEDGE_CATEGORIES = {
    "drug", "drug_class", "receptor", "enzyme", "protein", "gene",
    "disease", "symptom", "pharmacokinetics", "pharmacodynamics",
    "side_effect", "clinical_note"
}

# Soru Arketipleri
QUESTION_ARCHETYPES = {
    "receptor_ligand",
    "drug_class_membership",
    "disease_treatment",
    "pathophysiological_target",
    "toxicity_side_effect",
    "pharmacokinetics_pharmacodynamics",
    "slide_specific_pearl"
}

QUESTION_DIRECTIONS = {"positive_direct", "negative_inverse"}


@dataclass
class Evidence:
    page: int
    quote: str
    reference: Optional[str] = None


@dataclass
class PastExamRelevance:
    has_appeared: bool = False
    question_ids: List[str] = field(default_factory=list)
    details: Optional[str] = None
    frequency: Optional[int] = None


@dataclass
class KnowledgeAtom:
    knowledge_atom_id: str
    course_id: str
    board_id: str
    schedule_ref: str
    topic_id: str
    audio_lesson_id: str
    learning_objective_id: str
    category: str
    title: str
    statement: str
    page_number: int
    evidence: Evidence
    past_exam_relevance: PastExamRelevance = field(default_factory=PastExamRelevance)
    subtopic: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class QuizQuestion:
    id: str
    question_pair_id: str
    knowledge_atom_id: str
    course_id: str
    board_id: str
    schedule_ref: str
    topic_id: str
    audio_lesson_id: str
    learning_objective_id: str
    direction: Literal["positive_direct", "negative_inverse"]
    archetype: str
    prompt: str
    options: Dict[str, str]
    correct_option: str
    option_explanations: Dict[str, str]
    estimated_reading_sec: int
    difficulty: Literal["easy", "medium", "hard"]
    evidence: Evidence
    recall_hint: Optional[str] = None


@dataclass
class QuestionPair:
    question_pair_id: str
    knowledge_atom_id: str
    positive_question_id: str
    inverse_question_id: str


@dataclass
class TopicQuizPool:
    course_id: str
    board_id: str
    topic_id: str
    audio_lesson_id: str
    audio_lesson_status: Literal["COMPLETED"]
    generated_at: str
    total_atoms: int
    total_questions: int
    pairs: List[QuestionPair]
    questions: List[QuizQuestion]
