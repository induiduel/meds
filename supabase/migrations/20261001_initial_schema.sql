-- MedSoru Supabase PostgreSQL Veritabanı Şeması
-- Supabase Dashboard > SQL Editor sekmesine yapıştırıp "Run" butonuna basarak tabloları oluşturun.

-- 1. Kurullar Tablosu
CREATE TABLE IF NOT EXISTS public.committees (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  academic_year TEXT DEFAULT '2026-2027',
  target_questions INTEGER DEFAULT 100,
  color TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  data JSONB
);

-- 2. Aktif Öğrenci Soru Havuzu Tablosu
CREATE TABLE IF NOT EXISTS public.questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  question_number INTEGER,
  discipline TEXT,
  topic TEXT,
  status TEXT DEFAULT 'gathering',
  claimed_answer TEXT,
  upvotes INTEGER DEFAULT 0,
  tags JSONB DEFAULT '[]'::jsonb,
  fragments JSONB DEFAULT '[]'::jsonb,
  options JSONB DEFAULT '[]'::jsonb,
  reconstruction JSONB,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Çıkmış Sorular & Yapay Zeka Soru Arşivi Tablosu
CREATE TABLE IF NOT EXISTS public.past_questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  discipline TEXT,
  topic TEXT,
  exam_year TEXT,
  source_file TEXT,
  ai_category TEXT,
  claimed_answer TEXT,
  raw_question JSONB,
  reconstruction JSONB,
  is_suspect BOOLEAN DEFAULT FALSE,
  is_ambiguous BOOLEAN DEFAULT FALSE,
  is_locked BOOLEAN DEFAULT FALSE,
  upvotes INTEGER DEFAULT 0,
  comments JSONB DEFAULT '[]'::jsonb,
  reports JSONB DEFAULT '[]'::jsonb,
  custom_redacted_by TEXT,
  custom_redacted_at TIMESTAMPTZ,
  custom_redaction_prompt TEXT,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Amfi Ders Notları & Slaytlar Tablosu
CREATE TABLE IF NOT EXISTS public.lecture_notes (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  discipline TEXT,
  title TEXT,
  pages JSONB DEFAULT '[]'::jsonb,
  page_count INTEGER DEFAULT 0,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Kullanıcılar & Profiller Tablosu
CREATE TABLE IF NOT EXISTS public.users (
  uid TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  display_name TEXT,
  student_number TEXT,
  role TEXT DEFAULT 'student',
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Sistem Durumu & Telemetri Tablosu
CREATE TABLE IF NOT EXISTS public.system_status (
  id TEXT PRIMARY KEY,
  data JSONB,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. İndeksler (Hızlı Sorgulama İçin)
CREATE INDEX IF NOT EXISTS idx_questions_committee ON public.questions (committee_id);
CREATE INDEX IF NOT EXISTS idx_past_questions_committee ON public.past_questions (committee_id);
CREATE INDEX IF NOT EXISTS idx_past_questions_discipline ON public.past_questions (discipline);
CREATE INDEX IF NOT EXISTS idx_lecture_notes_committee ON public.lecture_notes (committee_id);

-- 8. Row Level Security (RLS) İzinleri (MedSoru İçin Okuma ve Yazma İzni)
ALTER TABLE public.committees ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.past_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lecture_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_status ENABLE ROW LEVEL SECURITY;

-- Politikalar: Anonim/Giriş yapmış kullanıcılara okuma ve yazma izni
DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read committees') THEN
    CREATE POLICY "Allow public read committees" ON public.committees FOR SELECT USING (true);
    CREATE POLICY "Allow public insert committees" ON public.committees FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update committees" ON public.committees FOR UPDATE USING (true);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read questions') THEN
    CREATE POLICY "Allow public read questions" ON public.questions FOR SELECT USING (true);
    CREATE POLICY "Allow public insert questions" ON public.questions FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update questions" ON public.questions FOR UPDATE USING (true);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read past_questions') THEN
    CREATE POLICY "Allow public read past_questions" ON public.past_questions FOR SELECT USING (true);
    CREATE POLICY "Allow public insert past_questions" ON public.past_questions FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update past_questions" ON public.past_questions FOR UPDATE USING (true);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read lecture_notes') THEN
    CREATE POLICY "Allow public read lecture_notes" ON public.lecture_notes FOR SELECT USING (true);
    CREATE POLICY "Allow public insert lecture_notes" ON public.lecture_notes FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update lecture_notes" ON public.lecture_notes FOR UPDATE USING (true);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read users') THEN
    CREATE POLICY "Allow public read users" ON public.users FOR SELECT USING (true);
    CREATE POLICY "Allow public insert users" ON public.users FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update users" ON public.users FOR UPDATE USING (true);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read system_status') THEN
    CREATE POLICY "Allow public read system_status" ON public.system_status FOR SELECT USING (true);
    CREATE POLICY "Allow public insert system_status" ON public.system_status FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update system_status" ON public.system_status FOR UPDATE USING (true);
  END IF;
END $$;
