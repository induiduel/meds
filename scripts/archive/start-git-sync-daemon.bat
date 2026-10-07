@echo off
chcp 65001 >nul
title MedSoru - Otomatik Git Senkronizasyon Servisi (20 Dk)
color 0B

echo ======================================================================
echo    MEDSORU - OTOMATİK GİT İZLEYİCİ VE YEDEKLEME SERVİSİ
echo    Her 20 dakikada bir kontrol eder, değişiklik varsa commit & push yapar.
echo    Değişiklik yoksa GitHub'a hiçbir işlem yapmaz.
echo ======================================================================
echo.

cd /d "%~dp0\.."

node scripts/auto-git-sync.mjs --interval=20

pause
