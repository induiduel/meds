@echo off
chcp 65001 >nul
echo ========================================================
echo        MEDS - YEREL SUPABASE SUNUCUSU BAŞLATILIYOR
echo ========================================================
cd /d "%~dp0"

set "PATH=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin;%PATH%"

echo [1/3] Docker durumu kontrol ediliyor...
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [HATA] Docker Desktop calismiyor veya henuz kurulmadi!
    echo Lutfen Docker Desktop uygulamasini baslatin ve tekrar deneyin.
    pause
    exit /b 1
)

echo [2/3] Supabase servisleri ayaga kaldiriliyor (docker compose)...
cd supabase-server
docker compose up -d

if %ERRORLEVEL% NEQ 0 (
    echo [HATA] Supabase baslatilirken bir hata olustu.
    pause
    exit /b 1
)

cd ..
echo [3/3] Servisler basariyla baslatildi!
echo.
echo ========================================================
echo        SUPABASE SUNUCUNUZ AKTIF VE CALISIYOR!
echo ========================================================
echo - Supabase Studio (Yonetim Paneli): http://localhost:8000
echo - REST API / Kong Gateway:          http://localhost:8000/rest/v1
echo - Auth API:                         http://localhost:8000/auth/v1
echo - PostgreSQL Baglanti Portu:        localhost:5432
echo.
echo Giris Bilgileri (local-supabase-keys.json dosyasinda mevcuttur):
type supabase-server\local-supabase-keys.json
echo.
echo ========================================================
echo Ipuclari:
echo - Veritabani semalarini yuklemek icin: apply-migrations-to-local.bat calistirin.
echo - Projeyi yerel veritabanina baglamak icin: switch-env-to-local.bat calistirin.
echo - Dis dunyaya / internete acmak icin: start-supabase-tunnel.bat calistirin.
echo ========================================================
pause
