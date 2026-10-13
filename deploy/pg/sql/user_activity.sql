-- Kişiler (yönetim paneli): cihazlar, kullanım süresi ve kullanıcı eylem günlüğü (2026-10-14).
-- Yalnız sunucu okur/yazar (src/services/peopleInsights.ts); tarayıcının /api/db/query beyaz listesinde YOK.
-- Canlı yayın: tetikleyici 'meds_changes' kanalına {t, op, id, c: uid, q: tür} yollar → server.ts hub →
-- yalnız yöneticilere SSE `people_changed`. Sunucu açılışta bu dosyayı kendisi de uygular. İdempotent.

create table if not exists public.user_devices (
  device_id text primary key,
  uid text,
  email text,
  display_name text,
  verified boolean not null default false,
  label text not null default '',
  platform text not null default '',
  browser text not null default '',
  model text not null default '',
  user_agent text not null default '',
  first_seen timestamptz not null default now(),
  last_seen timestamptz not null default now(),
  active_seconds bigint not null default 0,
  sessions integer not null default 1,
  last_path text not null default ''
);
create index if not exists user_devices_uid_idx on public.user_devices (uid);
create index if not exists user_devices_email_idx on public.user_devices (lower(email));
create index if not exists user_devices_seen_idx on public.user_devices (last_seen desc);

-- Günlük kullanım: cihaz × gün başına etkin saniye (grafik ve "kaç saat" için)
create table if not exists public.user_usage_daily (
  device_id text not null,
  day date not null,
  uid text,
  active_seconds integer not null default 0,
  primary key (device_id, day)
);
create index if not exists user_usage_daily_uid_idx on public.user_usage_daily (uid, day desc);

create table if not exists public.user_events (
  id bigserial primary key,
  uid text,
  email text,
  display_name text,
  device_id text,
  kind text not null,
  action text not null default 'create',
  ref text,
  label text not null default '',
  body text not null default '',
  link text not null default '',
  meta jsonb not null default '{}'::jsonb,
  at timestamptz not null default now()
);
create index if not exists user_events_uid_idx on public.user_events (uid, at desc);
create index if not exists user_events_device_idx on public.user_events (device_id, at desc);
create index if not exists user_events_kind_idx on public.user_events (kind, at desc);
create index if not exists user_events_at_idx on public.user_events (at desc);

create or replace function public.meds_notify_people() returns trigger
language plpgsql as $$
declare
  r jsonb := to_jsonb(coalesce(new, old));
begin
  perform pg_notify('meds_changes', json_build_object(
    't', tg_table_name,
    'op', tg_op,
    'id', coalesce(r->>'id', r->>'device_id'),
    'c', r->>'uid',
    'q', r->>'kind'
  )::text);
  return null;
end $$;

do $$
declare t text;
begin
  foreach t in array array['user_devices', 'user_events'] loop
    execute format('drop trigger if exists meds_notify on public.%I', t);
    execute format('create trigger meds_notify after insert or update or delete on public.%I
                    for each row execute function public.meds_notify_people()', t);
  end loop;
end $$;

alter table public.user_devices enable row level security;
alter table public.user_usage_daily enable row level security;
alter table public.user_events enable row level security;
do $$
begin
  if exists (select 1 from pg_roles where rolname = 'anon') then
    execute 'revoke all on public.user_devices, public.user_usage_daily, public.user_events from anon';
  end if;
  if exists (select 1 from pg_roles where rolname = 'authenticated') then
    execute 'revoke all on public.user_devices, public.user_usage_daily, public.user_events from authenticated';
  end if;
end $$;
