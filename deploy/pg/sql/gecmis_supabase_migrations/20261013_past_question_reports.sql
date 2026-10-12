-- MedSoru: hata bildirimi tablosu (cihazda da Oracle local'de de yoktu; kod "varsa yaz" diyordu).
-- Birincil depo past_questions.reports JSON kolonu olmaya devam eder; bu tablo dayanıklılık katmanıdır.
CREATE TABLE IF NOT EXISTS public.past_question_reports (
  id TEXT PRIMARY KEY,
  question_id TEXT,
  reason TEXT,
  details TEXT,
  reported_by TEXT,
  reporter_uid TEXT,
  reporter_email TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  data JSONB
);
CREATE INDEX IF NOT EXISTS idx_past_question_reports_question ON public.past_question_reports (question_id);
CREATE INDEX IF NOT EXISTS idx_past_question_reports_status ON public.past_question_reports (status);

ALTER TABLE public.past_question_reports ENABLE ROW LEVEL SECURITY;
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read past_question_reports') THEN
    CREATE POLICY "Allow public read past_question_reports" ON public.past_question_reports FOR SELECT USING (true);
    CREATE POLICY "Allow public insert past_question_reports" ON public.past_question_reports FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update past_question_reports" ON public.past_question_reports FOR UPDATE USING (true);
    CREATE POLICY "Allow public delete past_question_reports" ON public.past_question_reports FOR DELETE USING (true);
  END IF;
END $$;

NOTIFY pgrst, 'reload schema';
