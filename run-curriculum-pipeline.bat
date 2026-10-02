@echo off
chcp 65001 >nul
title MedSoru Donem 3 Gunluk Mufredat ve Ogrenme Otomasyonu
cd /d "%~dp0"

echo ===============================================================================
echo          🎓 MEDSORU DÖNEM 3 GÜNLÜK MÜFREDAT VE ÖĞRENME OTOMASYONU 🎓
echo ===============================================================================
echo.
echo [1] DeepSeek JSONL Dosyasini Sisteme Entegre Et (deepseek_data)
echo [2] Donem 3 Ders Programina Gore Bugunun Derslerini Isle ve Ogren'e Ekle
echo [3] Tum Kurul 1 Mufredat Derslerini %%500 Derinlikte Insa Et
echo [4] Belirli Bir Dersi Isle (Orn: Salgin, Izolasyon, Doku Onarimi vb.)
echo [5] Tam Otomasyon: DeepSeek + Mufredat + RAG Chunking + Vite Build
echo [6] Cikis
echo.
set /p CHOICE="Seciminiz (1-6): "

if "%CHOICE%"=="1" (
    echo.
    echo [*] DeepSeek JSONL verileri isleniyor...
    python scripts\integrate_deepseek_jsonl.py
    pause
    exit /b
)

if "%CHOICE%"=="2" (
    echo.
    echo [*] Gunluk mufredat dersleri taranip isleniyor...
    python scripts\curriculum_daily_pipeline.py
    pause
    exit /b
)

if "%CHOICE%"=="3" (
    echo.
    echo [*] Tum Kurul 1 dersleri %%500 derinlikte insa ediliyor...
    python scripts\curriculum_daily_pipeline.py --all-kurul1
    pause
    exit /b
)

if "%CHOICE%"=="4" (
    echo.
    set /p LEC_NAME="Ders veya konu adi girin: "
    python scripts\curriculum_daily_pipeline.py --lecture "%LEC_NAME%"
    pause
    exit /b
)

if "%CHOICE%"=="5" (
    echo.
    echo [*] 1/3 DeepSeek JSONL entegrasyonu...
    python scripts\integrate_deepseek_jsonl.py
    echo.
    echo [*] 2/3 Gunluk mufredat pipeline calistiriliyor...
    python scripts\curriculum_daily_pipeline.py
    echo.
    echo [*] 3/3 Frontend derlemesi dogrulaniyor...
    call npm run build
    echo.
    echo [✓] Tum adimlar basariyla tamamlandi!
    pause
    exit /b
)

echo Cikis yapiliyor...
