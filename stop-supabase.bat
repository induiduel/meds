@echo off
chcp 65001 >nul
echo ========================================================
echo        MEDS - YEREL SUPABASE SUNUCUSU DURDURULUYOR
echo ========================================================
set "PATH=%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin;%PATH%"
cd /d "%~dp0\supabase-server"

docker compose down
echo.
echo Supabase servisleri basariyla durduruldu.
pause
