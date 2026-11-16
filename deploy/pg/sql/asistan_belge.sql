-- Tıp Asistanı belge indeksi (F1, 2026-10-29). Idempotent. rag_chunks'tan BAĞIMSIZDIR: hat yeniden üretince silinmez.
-- Uygula: docker exec -i meds-pg psql -U meds -d meds < deploy/pg/sql/asistan_belge.sql
create extension if not exists vector;
create extension if not exists pg_trgm;

create table if not exists asistan_belge (
  id          text primary key,            -- tur:kimlik (scripts/asistan/kaynaklar.py)
  tur         text not null,
  baslik      text not null default '',
  metin       text not null,
  ders        text not null default '',
  kurul       int,
  brans       text not null default '',
  url         text not null,
  kaynak      text not null default '',
  meta        jsonb not null default '{}'::jsonb,
  ozet        text not null,               -- md5(baslik|metin): değişen belge yeniden vektörlenir
  baslik_f    text not null default '',    -- katlanmış başlık (trigram)
  arama       text not null default '',    -- katlanmış tam sözcük + 5 harfli kök (scripts/asistan/metin.py)
  tsv         tsvector generated always as (
                setweight(to_tsvector('simple', baslik_f), 'A') || setweight(to_tsvector('simple', arama), 'B')
              ) stored,
  embedding   vector(1024),                -- bge-m3, L2 normlu
  guncel      timestamptz not null default now()
);
create index if not exists asistan_belge_tsv   on asistan_belge using gin (tsv);
create index if not exists asistan_belge_trgm  on asistan_belge using gin (baslik_f gin_trgm_ops);
create index if not exists asistan_belge_tur   on asistan_belge (tur);
create index if not exists asistan_belge_hnsw  on asistan_belge using hnsw (embedding vector_cosine_ops);

-- Karma arama (RRF: vektör + tam metin + başlık benzerliği). qf: katlanmış sorgu, qk: katlanmış + kök (metin.py::sorgu)
create or replace function asistan_ara(qv vector(1024), qf text, qk text, n int default 20,
                                       turler text[] default null, kurul_f int default null)
returns table(id text, tur text, baslik text, url text, ders text, kurul int, skor double precision)
language sql stable as $$
  with v as (
    select b.id, row_number() over (order by b.embedding <=> qv) r
    from (select * from asistan_belge where embedding is not null order by embedding <=> qv limit 120) b
  ), tok as (  -- sözcük başına belge sıklığı: sık sözcük (ilaç, hasta…) nadir sözcüğü (nistatin) bastırmasın
    select w, d from (
      select w, (select count(*) from asistan_belge x where x.tsv @@ to_tsquery('simple', w)) d
      from (select distinct w from regexp_split_to_table(btrim(regexp_replace(qk, '[^a-z0-9 ]', ' ', 'g')), '\s+') w where w <> '') s
    ) z where d > 0
  ), tk as (
    select w, d from tok where d <= 6000 or not exists (select 1 from tok where d <= 6000)
  ), f as (
    select b.id, row_number() over (order by sum(ln(40000.0 / tk.d)) desc) r
    from tk cross join lateral (select id from asistan_belge x where x.tsv @@ to_tsquery('simple', tk.w)) b
    group by b.id order by sum(ln(40000.0 / tk.d)) desc limit 120
  ), t as (
    select b.id, row_number() over (order by similarity(b.baslik_f, qf) desc) r
    from asistan_belge b where b.baslik_f % qf order by similarity(b.baslik_f, qf) desc limit 60
  ), k as (
    select id, sum(1.0 / (60 + r)) s from (select * from v union all select * from f union all select * from t) x group by id
  )
  select b.id, b.tur, b.baslik, b.url, b.ders, b.kurul, k.s
  from k join asistan_belge b using (id)
  where (turler is null or b.tur = any(turler)) and (kurul_f is null or b.kurul = kurul_f)
  order by k.s desc limit n
$$;
