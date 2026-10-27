-- Topluluk (v15): kanal mesajları ve ders yorumları. İdempotent; sunucu açılışta uygular (src/services/topluluk.ts).
create table if not exists topluluk_mesajlar (
  id bigserial primary key,
  kanal text not null,
  uid text not null,
  ad text not null,
  metin text not null,
  yanit_id bigint,
  olusturma timestamptz not null default now(),
  silindi boolean not null default false,
  silen text,
  sikayet_uid text[] not null default '{}'
);
create index if not exists topluluk_kanal_id on topluluk_mesajlar (kanal, id desc) where not silindi;
create index if not exists topluluk_uid_zaman on topluluk_mesajlar (uid, olusturma desc);
