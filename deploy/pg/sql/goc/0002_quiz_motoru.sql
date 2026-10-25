-- 0002 · Otomatik Quiz ve Aktif Geri Çağırma (Active Recall) Motoru Şeması.
-- Ders-bağımsız (course-agnostic), 2x Çapraz Sorgulama (N -> 2N) ve Solo/Multiplayer oturum desteği.
-- Sadece ekleme (append-only) / idempotence kurallarına uygun DDL.

-- 1. Atomik Bilgi Envanteri (Knowledge Atoms)
CREATE TABLE IF NOT EXISTS quiz_atomik_bilgiler (
  knowledge_atom_id     text PRIMARY KEY,
  course_id             text NOT NULL,               -- 'pharmacology', 'pathology' vb.
  board_id              text NOT NULL,               -- '2026_2027_kurul_2'
  schedule_ref          text NOT NULL,
  topic_id              text NOT NULL,               -- 'k2-07' vb.
  audio_lesson_id       text NOT NULL,               -- Sesli ders referansı (State bağımlılığı)
  learning_objective_id text,
  category              text NOT NULL,               -- 'drug', 'receptor', 'enzyme' vb.
  title                 text NOT NULL,
  statement             text NOT NULL,
  subtopic              text,
  page_number           integer NOT NULL,
  evidence              jsonb NOT NULL,              -- {"page": 12, "quote": "..."}
  past_exam_relevance   jsonb NOT NULL DEFAULT '{}'::jsonb, -- {"has_appeared": true, "question_ids": [...]}
  tags                  text[] DEFAULT '{}',
  created_at            timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_quiz_atom_topic_cat ON quiz_atomik_bilgiler (topic_id, category);
CREATE INDEX IF NOT EXISTS idx_quiz_atom_course_board ON quiz_atomik_bilgiler (course_id, board_id);

-- 2. Soru Çiftleri (2x Matrix: Pozitif ve Negatif Çifti)
CREATE TABLE IF NOT EXISTS quiz_soru_ciftleri (
  question_pair_id      text PRIMARY KEY,
  knowledge_atom_id     text NOT NULL REFERENCES quiz_atomik_bilgiler (knowledge_atom_id) ON DELETE CASCADE,
  positive_question_id  text NOT NULL,
  inverse_question_id   text NOT NULL,
  created_at            timestamptz NOT NULL DEFAULT now()
);

-- 3. Quiz Soruları (Active Recall: 5-15 sn hedefli, kısa ve net)
CREATE TABLE IF NOT EXISTS quiz_sorulari (
  id                    text PRIMARY KEY,
  question_pair_id      text NOT NULL REFERENCES quiz_soru_ciftleri (question_pair_id) ON DELETE CASCADE,
  knowledge_atom_id     text NOT NULL REFERENCES quiz_atomik_bilgiler (knowledge_atom_id) ON DELETE CASCADE,
  course_id             text NOT NULL,
  board_id              text NOT NULL,
  topic_id              text NOT NULL,
  audio_lesson_id       text NOT NULL,
  direction             text NOT NULL,               -- 'positive_direct' | 'negative_inverse'
  archetype             text NOT NULL,               -- 'receptor_ligand', 'drug_class_membership' vb.
  prompt                text NOT NULL,               -- Soru kökü
  options               jsonb NOT NULL,              -- {"A": "...", "B": "...", ...}
  correct_option        text NOT NULL,               -- "A", "B", ...
  option_explanations   jsonb NOT NULL,              -- {"A": "...", ...} gerekçeli şık açıklamaları
  recall_hint           text,
  estimated_reading_sec integer NOT NULL DEFAULT 10, -- 5-15 sn aralığı
  difficulty            text NOT NULL DEFAULT 'medium',
  evidence              jsonb NOT NULL,
  created_at            timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_quiz_sorulari_topic ON quiz_sorulari (topic_id, difficulty);
CREATE INDEX IF NOT EXISTS idx_quiz_sorulari_atom ON quiz_sorulari (knowledge_atom_id);

-- 4. Bireysel Çalışma (Solo / Active Recall) Oturumları ve İlerleme
CREATE TABLE IF NOT EXISTS quiz_solo_oturumlar (
  session_id            text PRIMARY KEY,
  user_id               text NOT NULL,
  course_id             text NOT NULL,
  topic_ids             text[] NOT NULL,
  total_answered        integer NOT NULL DEFAULT 0,
  correct_count         integer NOT NULL DEFAULT 0,
  wrong_atom_ids        text[] DEFAULT '{}',
  incomplete_pair_ids   text[] DEFAULT '{}',
  started_at            timestamptz NOT NULL DEFAULT now(),
  last_activity_at      timestamptz NOT NULL DEFAULT now()
);

-- 5. Multiplayer Rekabet Odaları
CREATE TABLE IF NOT EXISTS quiz_multiplayer_odalar (
  room_id               text PRIMARY KEY,
  course_id             text NOT NULL,
  topic_id              text NOT NULL,
  question_ids          text[] NOT NULL,
  time_per_question_sec integer NOT NULL DEFAULT 10,
  status                text NOT NULL DEFAULT 'waiting', -- 'waiting' | 'in_progress' | 'completed'
  participants          jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at            timestamptz NOT NULL DEFAULT now()
);
