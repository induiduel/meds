@echo off
title MedSoru - Cloudflare Quick Tunnel

echo ========================================================
echo       MEDSORU CLOUDFLARE QUICK TUNNEL BASLATICI
echo ========================================================
echo.

cd /d "%~dp0"
if exist "meds\scripts\start-cloudflare-tunnel.mjs" (
    cd /d "%~dp0meds"
) else (
    cd /d "C:\Users\indui\Desktop\meds"
)

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [HATA] Node.js bulunamadi! Lutfen Node.js yukleyin.
    pause
    exit /b 1
)

node scripts/start-cloudflare-tunnel.mjs

if %errorlevel% neq 0 (
    echo.
    echo [BILGI] Program sonlandi.
    pause
)
