-- Öğren ekranı ortak katmanı (2026-10-13): herkese açık slayt notları (SPOT / ÖNEMLİ / VURGU) ve
-- seçili metin bildirimleri (kırmızı "!" + tartışma). Yalnız sunucu okur/yazar (src/services/learnSocialRoutes.ts);
-- tarayıcının /api/db/query beyaz listesinde YOK. Canlı yayın sunucudan SSE `learn_social` olayıyla yapılır
-- (tetikleyici gerekmez). İdempotent: iki makinede `docker exec -i meds-pg psql -U meds -d meds < learn_social.sql`.

create table if not exists public.learn_notes (
  id text primary key,
  deck_id text not null,
  step_number integer not null,
  kind text not null check (kind in ('spot', 'onemli', 'vurgu')),
  body text not null,
  anchor text,
  author_id text not null,
  author_name text not null,
  created_at timestamptz not null default now()
);
create index if not exists learn_notes_deck_idx on public.learn_notes (deck_id, step_number, created_at);
create index if not exists learn_notes_author_idx on public.learn_notes (author_id, created_at desc);

create table if not exists public.learn_threads (
  id text primary key,
  deck_id text not null,
  deck_title text not null default '',
  step_number integer not null,
  -- Bildirilen metin + yeniden konumlandırma için önü/arkası (içerik değişirse en yakın eşleşme aranır)
  quote text not null,
  prefix text not null default '',
  suffix text not null default '',
  status text not null default 'open' check (status in ('open', 'resolved')),
  reporter_id text not null,
  reporter_name text not null,
  message_count integer not null default 0,
  created_at timestamptz not null default now(),
  last_message_at timestamptz not null default now()
);
create index if not exists learn_threads_deck_idx on public.learn_threads (deck_id, step_number);
create index if not exists learn_threads_status_idx on public.learn_threads (status, last_message_at desc);

create table if not exists public.learn_thread_messages (
  id text primary key,
  thread_id text not null references public.learn_threads (id) on delete cascade,
  body text not null,
  author_id text not null,
  author_name text not null,
  is_admin boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists learn_thread_messages_thread_idx on public.learn_thread_messages (thread_id, created_at);

alter table public.learn_notes enable row level security;
alter table public.learn_threads enable row level security;
alter table public.learn_thread_messages enable row level security;
-- Sahip rol (meds) RLS'den muaf; PostgREST rollerine (anon/authenticated) hiçbir politika verilmez.
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'anon') then
    execute 'revoke all on public.learn_notes, public.learn_threads, public.learn_thread_messages from anon';
  end if;
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    execute 'revoke all on public.learn_notes, public.learn_threads, public.learn_thread_messages from authenticated';
  end if;
end $$;
