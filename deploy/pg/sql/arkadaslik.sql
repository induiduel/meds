-- Arkadaşlık (v15 › Arkadaşlar, açık profil, arkadaş sıralaması). İdempotent; sunucu açılışta uygular (src/services/arkadaslik.ts).
-- Bir satır = bir istek (gonderen → alan). durum 'kabul' olunca iki kişi arkadaştır (yön önemsiz).
-- Reddedilen/çıkarılan istek satırı silinir. uid yalnız sunucuda kalır; istemciye açık profil kimliği (özet) gider.
create table if not exists arkadas_istek (
  gonderen text not null,
  alan text not null,
  durum text not null default 'bekliyor' check (durum in ('bekliyor', 'kabul')),
  olusturma timestamptz not null default now(),
  guncelleme timestamptz not null default now(),
  primary key (gonderen, alan),
  check (gonderen <> alan)
);
create index if not exists arkadas_istek_alan on arkadas_istek (alan);
