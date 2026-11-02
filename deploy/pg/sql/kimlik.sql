-- MeDSor kendi kimlik sistemi (2026-11-02; Firebase Auth kaldırıldı). İdempotent; sunucu açılışta uygular
-- (src/services/yerelKimlik.ts). uid'ler eski Firebase uid'leriyle aynıdır: kullanıcı verisi (user_data, users,
-- user_backups, notlar) bağlı kalır. Şifre yalnız scrypt özeti olarak tutulur; yenileme jetonu ve e-posta kodu da özettir.
create table if not exists auth_hesaplar (
  uid text primary key,
  email text not null,
  sifre_ozeti text,                       -- null: hesap Firebase'den taşındı, kullanıcı henüz şifre belirlemedi
  ad text,
  foto text,
  eposta_dogrulandi boolean not null default false,
  devre_disi boolean not null default false,
  kaynak text not null default 'yerel',  -- 'yerel' | 'firebase-gocu'
  olusturma timestamptz not null default now(),
  guncelleme timestamptz not null default now(),
  son_giris timestamptz
);
create unique index if not exists auth_hesaplar_email on auth_hesaplar (lower(email));

create table if not exists auth_oturumlar (
  id text primary key,                    -- sha256(yenileme jetonu)
  uid text not null references auth_hesaplar(uid) on delete cascade,
  giris_zamani timestamptz not null default now(),
  son_kullanim timestamptz not null default now(),
  bitis timestamptz not null,
  cihaz text
);
create index if not exists auth_oturumlar_uid on auth_oturumlar (uid);

create table if not exists auth_kodlar (
  email text not null,
  amac text not null,                     -- 'sifre' (belirle/sıfırla) | 'giris' (şifresiz kodla giriş)
  kod_ozeti text not null,
  deneme int not null default 0,
  bitis timestamptz not null,
  olusturma timestamptz not null default now(),
  primary key (email, amac)
);

-- Firebase dönemindeki hesapları taşı (uid korunur). Önce users (profil), sonra doğrulanmış user_data e-postaları.
insert into auth_hesaplar (uid, email, ad, eposta_dogrulandi, kaynak)
select distinct on (lower(u.email)) u.uid, lower(u.email), u.display_name, true, 'firebase-gocu'
from users u
where coalesce(u.email, '') like '%@%' and u.email not like '%@medsoru.local'
  and u.uid !~ '^(std-|local-admin-|admin-)'
order by lower(u.email), u.updated_at desc nulls last
on conflict do nothing;

insert into auth_hesaplar (uid, email, eposta_dogrulandi, kaynak)
select distinct on (lower(d.email)) d.uid, lower(d.email), true, 'firebase-gocu'
from user_data d
where d.verified and coalesce(d.email, '') like '%@%'
  and not exists (select 1 from auth_hesaplar h where lower(h.email) = lower(d.email))
  and not exists (select 1 from auth_hesaplar h where h.uid = d.uid)
order by lower(d.email), d.updated_at desc
on conflict do nothing;
