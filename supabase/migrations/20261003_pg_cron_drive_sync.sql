-- ==============================================================================
-- MedSoru AI Drive & Ders Notu Otomatik Senkronizasyon pg_cron Yapılandırması
-- ==============================================================================
-- Bu migration; Supabase PostgreSQL üzerinde 'pg_cron' kullanarak her gün
-- sabah 12:00 ve öğlen 15:00'te (Türkiye Saati: UTC+3 -> UTC 09:00 ve 12:00)
-- otomatik senkronizasyon tetikleyicisi ve loglama tablosunu kurar.
-- ==============================================================================

-- 1. pg_cron ve pg_net Eklentilerini Aktifleştir
CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_net;

-- 2. Senkronizasyon Takip ve Olay Kuyruğu Tablosu
CREATE TABLE IF NOT EXISTS public.drive_sync_logs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  trigger_source TEXT DEFAULT 'pg_cron',         -- 'pg_cron', 'manual', 'agent_orchestrator'
  scheduled_time TEXT,                           -- '12:00' veya '15:00'
  status TEXT DEFAULT 'pending',                 -- 'pending', 'running', 'completed', 'failed'
  total_drive_items INTEGER DEFAULT 0,
  total_drive_pdfs INTEGER DEFAULT 0,
  ready_decks_count INTEGER DEFAULT 0,
  pending_pdfs_count INTEGER DEFAULT 0,
  processed_decks JSONB DEFAULT '[]'::jsonb,
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

-- RLS İzinleri
ALTER TABLE public.drive_sync_logs ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read drive_sync_logs') THEN
    CREATE POLICY "Allow public read drive_sync_logs" ON public.drive_sync_logs FOR SELECT USING (true);
    CREATE POLICY "Allow public insert drive_sync_logs" ON public.drive_sync_logs FOR INSERT WITH CHECK (true);
    CREATE POLICY "Allow public update drive_sync_logs" ON public.drive_sync_logs FOR UPDATE USING (true);
  END IF;
END $$;

-- 3. Tetikleyici Stored Procedure
CREATE OR REPLACE FUNCTION public.trigger_drive_curriculum_sync(p_source TEXT DEFAULT 'pg_cron')
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_log_id UUID;
BEGIN
  INSERT INTO public.drive_sync_logs (trigger_source, scheduled_time, status, created_at)
  VALUES (
    p_source, 
    to_char(NOW() AT TIME ZONE 'Europe/Istanbul', 'HH24:MI'),
    'pending',
    NOW()
  )
  RETURNING id INTO v_log_id;

  RETURN v_log_id;
END;
$$;

-- 4. pg_cron Görevi Tanımlama
-- Türkiye Saati UTC+3 olduğundan:
-- TR 12:00 -> UTC 09:00 ('0 9 * * *')
-- TR 15:00 -> UTC 12:00 ('0 12 * * *')
-- İkisi birlikte: '0 9,12 * * *'

DO $$
BEGIN
  -- Varsa eski görevi kaldır
  PERFORM cron.unschedule('meds-daily-curriculum-sync');
EXCEPTION WHEN OTHERS THEN
  -- Görev yoksa hatayı yut
END $$;

SELECT cron.schedule(
  'meds-daily-curriculum-sync',
  '0 9,12 * * *',
  $$SELECT public.trigger_drive_curriculum_sync('pg_cron_scheduled')$$
);
