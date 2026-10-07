-- Cevabı belirsiz çıkmış sorular için kullanıcı anketi: kullanıcı başına soru başına tek oy.
CREATE TABLE IF NOT EXISTS public.answer_votes (
  question_id text NOT NULL,
  voter_uid   text NOT NULL,
  choice      char(1) NOT NULL CHECK (choice IN ('A','B','C','D','E')),
  created_at  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (question_id, voter_uid)
);
CREATE INDEX IF NOT EXISTS idx_answer_votes_question ON public.answer_votes (question_id);
ALTER TABLE public.answer_votes ENABLE ROW LEVEL SECURITY;
-- Yalnızca sunucu (service key) okur/yazar; istemci doğrudan erişemez.
