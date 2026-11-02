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

-- Öğrenci numarasıyla giriş (2026-11-02): hesap başına öğrenci no; boşsa users.student_number'a bakılır.
alter table auth_hesaplar add column if not exists ogrenci_no text;
update auth_hesaplar h set ogrenci_no = u.student_number
from users u where u.uid = h.uid and h.ogrenci_no is null and coalesce(u.student_number, '') ~ '^[0-9]{5,12}$';
create index if not exists auth_hesaplar_ogrenci_no on auth_hesaplar (ogrenci_no);

-- Yönetici onaylı şifre talebi (e-posta gerekmez): kullanıcı e-posta/öğrenci no + kimlik bilgisi + yeni şifre yazar,
-- şifre talep anında özetlenir; yönetici gerçek kişi olduğuna karar verip onaylarsa özet hesaba yazılır.
-- takip_ozeti: talebi yapan cihazdaki gizli anahtarın özeti (durum sorgusu ve onay sonrası tek seferlik oturum için).
create table if not exists auth_sifre_talepleri (
  id text primary key,
  uid text not null references auth_hesaplar(uid) on delete cascade,
  email text not null,
  sifre_ozeti text not null,
  takip_ozeti text not null,
  ad text,
  ogrenci_no text,
  aciklama text,
  durum text not null default 'bekliyor' check (durum in ('bekliyor', 'onaylandi', 'reddedildi', 'iptal')),
  karar_veren text,
  karar_notu text,
  karar_zamani timestamptz,
  oturum_verildi boolean not null default false,
  ip text,
  cihaz text,
  olusturma timestamptz not null default now()
);
create index if not exists auth_sifre_talepleri_durum on auth_sifre_talepleri (durum, olusturma desc);
create index if not exists auth_sifre_talepleri_uid on auth_sifre_talepleri (uid);
