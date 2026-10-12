-- Canlı yayın: satır değişince 'meds_changes' kanalına küçük bir bildirim gider (anahtar + işlem).
-- Sunucu (pgListen) bunu alır, gerekirse satırı toplu okur ve SSE ile tüm ziyaretçilere dağıtır.
-- NOTIFY yükü 8 KB ile sınırlı olduğundan satırın kendisi gönderilmez. İdempotent.
create or replace function public.meds_notify_change() returns trigger
language plpgsql as $$
declare
  r jsonb := to_jsonb(coalesce(new, old));
  k text;
begin
  k := coalesce(r->>'id', r->>'uid', r->>'question_id');
  perform pg_notify('meds_changes', json_build_object(
    't', tg_table_name,
    'op', tg_op,
    'id', k,
    'q', case when tg_table_name = 'answer_votes' then r->>'question_id' end,
    'c', r->>'committee_id'
  )::text);
  return null;
end $$;

do $$
declare t text;
begin
  foreach t in array array['past_questions','questions','past_question_reports','answer_votes',
                           'committees','lecture_notes','practice_questions','system_status','users']
  loop
    if to_regclass('public.' || t) is not null then
      execute format('drop trigger if exists meds_notify on public.%I', t);
      execute format('create trigger meds_notify after insert or update or delete on public.%I
                      for each row execute function public.meds_notify_change()', t);
    end if;
  end loop;
end $$;

-- Delta eşitleme (updated_at > since) ve sıralı listeler için eksik indeksler
create index if not exists idx_past_questions_updated_at on public.past_questions (updated_at);
create index if not exists idx_questions_updated_at on public.questions (updated_at);
create index if not exists idx_past_question_reports_created on public.past_question_reports (created_at desc);

-- PostgREST (cihaz betikleri) için tablo/fonksiyon yetkileri
grant all on all tables in schema public to service_role;
grant all on all sequences in schema public to service_role;
grant execute on all functions in schema public to service_role, anon, authenticated;
grant select on all tables in schema public to anon, authenticated;
