@echo off
chcp 65001 >nul
echo ========================================================
echo   MEDS - SUPABASE CLOUDFLARE PUBLIC TUNNEL BAŞLATILIYOR
echo ========================================================
echo.
echo Bu islem yerel Supabase sunucunuzu (port 8000) guvenli
echo ve ucretsiz bir https://*.trycloudflare.com baglantisiyla
echo internete acar. Modemden port acmaniza gerek kalmaz!
echo.
cd /d "%~dp0"

if not exist "cloudflared.exe" (
    echo [HATA] cloudflared.exe bulunamadi!
    pause
    exit /b 1
)

cloudflared.exe tunnel --url http://localhost:8000
pause
