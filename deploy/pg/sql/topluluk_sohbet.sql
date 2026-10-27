-- Topluluk (v15 › L01 Sohbet listesi, L03 Yorumlar). İdempotent; sunucu açılışta uygular (src/services/toplulukSohbet.ts).
-- Sohbet mesajları ayrı tabloya değil topluluk_mesajlar'a `oda:<id>` kanalıyla yazılır (tek mesaj tablosu).
create table if not exists sohbet_odalari (
  id bigserial primary key,
  tur text not null check (tur in ('dm', 'grup')),
  ad text,
  kod text unique,
  olusturan text not null,
  dm_anahtar text unique,
  olusturma timestamptz not null default now(),
  son timestamptz not null default now()
);
create table if not exists sohbet_uyeleri (
  oda_id bigint not null references sohbet_odalari(id) on delete cascade,
  uid text not null,
  ad text not null,
  okundu_id bigint not null default 0,
  katilma timestamptz not null default now(),
  primary key (oda_id, uid)
);
create index if not exists sohbet_uyeleri_uid on sohbet_uyeleri (uid);
create table if not exists yorum_begeni (
  mesaj_id bigint not null,
  uid text not null,
  olusturma timestamptz not null default now(),
  primary key (mesaj_id, uid)
);
create index if not exists topluluk_yanit on topluluk_mesajlar (yanit_id) where yanit_id is not null;
