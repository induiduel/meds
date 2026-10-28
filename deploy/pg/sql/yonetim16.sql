-- Yönetim v16: yönetici denetim kaydı (2026-10-28). İdempotent; sunucu açılışta kendisi uygular
-- (src/services/yonetim16/denetim.ts). Yalnız sunucu okur/yazar; /api/db/query beyaz listesinde YOK.
-- tur: 'yazma' (POST/PUT/PATCH/DELETE /api/admin/*) | 'okuma' (kişisel veri okuma: profil, sohbet mesajı…)
create table if not exists public.yonetici_denetim (
  id bigserial primary key,
  at timestamptz not null default now(),
  tur text not null default 'yazma',
  kim text not null default '',
  via text not null default '',
  ip text not null default '',
  yontem text not null default '',
  uc text not null default '',
  hedef text not null default '',
  durum integer not null default 0,
  sure_ms integer not null default 0,
  ozet jsonb not null default '{}'::jsonb
);
create index if not exists yonetici_denetim_at_idx on public.yonetici_denetim (at desc);
create index if not exists yonetici_denetim_hedef_idx on public.yonetici_denetim (hedef, at desc);
create index if not exists yonetici_denetim_uc_idx on public.yonetici_denetim (uc, at desc);
create index if not exists yonetici_denetim_tur_idx on public.yonetici_denetim (tur, at desc);
