-- Taş Masası (Oyunlar › Yedili Okey, Takım, 101, Uno). İdempotent; sunucu açılışta uygular (src/services/masa/sunucu.ts).
-- masa_oda: oda durumunun tamamı (dağıtımda/yeniden başlatmada oyun kaldığı yerden sürsün). uid yalnız sunucuda kalır.
create table if not exists masa_oda (
  kod text primary key,
  veri jsonb not null,
  asama text not null,
  uidler text[] not null default '{}',
  guncel timestamptz not null default now()
);

-- Biten her el: bir satır + oyuncu başına bir satır (genel ve rakibe göre istatistik)
create table if not exists masa_el (
  id bigserial primary key,
  kod text not null,
  tur text not null,
  el_no int not null,
  neden text not null,
  at timestamptz not null default now()
);
create table if not exists masa_el_oyuncu (
  el_id bigint not null references masa_el (id) on delete cascade,
  uid text,
  kimlik text not null,
  ad text not null,
  bot boolean not null default false,
  takim text,
  puan int not null,
  kalan int not null,
  ceza int not null default 0,
  kazandi boolean not null default false
);
create index if not exists masa_el_oyuncu_uid on masa_el_oyuncu (uid);
create index if not exists masa_el_oyuncu_el on masa_el_oyuncu (el_id);
