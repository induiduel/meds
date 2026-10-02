@echo off
chcp 65001 >nul
echo ========================================================
echo   MEDS - VERİTABANI ŞEMALARI VE MİGRATİONLAR YÜKLENİYOR
echo ========================================================
cd /d "%~dp0"

docker ps | findstr supabase-db >nul
if %ERRORLEVEL% NEQ 0 (
    echo [HATA] supabase-db konteyneri calismiyor!
    echo Lutfen once start-supabase.bat ile sunucuyu baslatin.
    pause
    exit /b 1
)

echo [1/3] 20261001_initial_schema.sql yukleniyor...
docker exec -i supabase-db psql -U postgres -d postgres < "supabase\migrations\20261001_initial_schema.sql"

echo [2/3] 20261002_ai_interactions_and_chunks.sql yukleniyor...
docker exec -i supabase-db psql -U postgres -d postgres < "supabase\migrations\20261002_ai_interactions_and_chunks.sql"

echo [3/3] 20261003_rag_vector_schema.sql yukleniyor...
docker exec -i supabase-db psql -U postgres -d postgres < "supabase\migrations\20261003_rag_vector_schema.sql"

echo.
echo ========================================================
echo TUM MIGRATION'LAR VE RAG VEKTOR TABLOLARI YUKLENDI!
echo ========================================================
pause
