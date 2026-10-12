#!/bin/bash
# İlk açılışta: uzantılar + PostgREST rolleri (yalnız cihazdaki eski betikler için).
set -e
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v pw="$POSTGRES_PASSWORD" <<'SQL'
create extension if not exists vector;
create extension if not exists pg_stat_statements;
create role anon nologin;
create role authenticated nologin;
create role service_role nologin bypassrls;
create role authenticator login noinherit password :'pw';
grant anon, authenticated, service_role to authenticator;
grant usage on schema public to anon, authenticated, service_role;
alter default privileges for role meds in schema public grant all on tables to service_role;
alter default privileges for role meds in schema public grant all on sequences to service_role;
alter default privileges for role meds in schema public grant execute on functions to service_role, anon, authenticated;
SQL
