-- Öğrenci profili: hesabın (ya da girişsiz cihazın) tüm kişisel verisi tek satırda (jsonb).
-- Sunucu /api/user-data/backup her kayıtta birleştirilmiş paketi buraya yansıtır; dosya kopyası data/user_backups/.
-- Tarayıcının /api/db/query kapısında bu tablo YOK (kişisel veri; yalnız sunucu okur/yazar). İdempotent.
create table if not exists public.user_data (
  uid text primary key,
  email text,
  verified boolean not null default false,
  data jsonb not null default '{}'::jsonb,
  rev bigint not null default 0,
  updated_at timestamptz not null default now()
);
create index if not exists user_data_email_idx on public.user_data (lower(email));
alter table public.user_data enable row level security;
-- Sahip rol (meds) RLS'den muaf; PostgREST rollerine (anon/authenticated) hiçbir politika verilmez.
revoke all on public.user_data from anon, authenticated;
