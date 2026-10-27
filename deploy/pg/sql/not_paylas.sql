-- Not paylaşımı (v15 › K05 Notu paylaş, K06 Benimle paylaşılanlar). İdempotent; sunucu açılışta uygular (src/services/notPaylas.ts).
-- Hedef her zaman bir sohbet odasıdır: grup odası = topluluk, birebir (dm) oda = kişi. Görme yetkisi oda üyeliğinden gelir.
-- topluluk_sohbet.sql'e bağlıdır (sohbet_odalari).
create table if not exists paylasilan_notlar (
  id bigserial primary key,
  oda_id bigint not null references sohbet_odalari(id) on delete cascade,
  sahip text not null,
  sahip_ad text not null,
  baslik text not null default '',
  metin text not null default '',
  renk text not null default 'none',
  silindi boolean not null default false,
  olusturma timestamptz not null default now()
);
create index if not exists paylasilan_notlar_oda on paylasilan_notlar (oda_id, id desc) where not silindi;
create index if not exists paylasilan_notlar_sahip on paylasilan_notlar (sahip, id desc) where not silindi;
