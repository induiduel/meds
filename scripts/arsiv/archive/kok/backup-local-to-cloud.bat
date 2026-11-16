@echo off
chcp 65001 >nul
echo ========================================================
echo   MEDS - YEREL SUPABASE'DEN ONLINE BULUTA YEDEKLEME
echo ========================================================
echo.
echo Bilgisayarinizdaki veriler online Supabase bulutuna aktariliyor...
echo.
cd /d "%~dp0"
node scripts\backup-local-to-cloud.mjs
echo.
pause
