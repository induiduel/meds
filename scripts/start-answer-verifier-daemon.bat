@echo off
chcp 65001 >nul
title MedSoru - Otomatik Soru İzleyici ve Doğrulama Servisi (Watcher)
color 0A

echo ======================================================================
echo    MEDSORU - KESİNTİSİZ SORU VE CEVAP İZLEYİCİSİ (WATCHER DAEMON)
echo    Her yeni soru eklendiğinde otomatik olarak %%90 kuralını işletir.
echo ======================================================================
echo.

cd /d "%~dp0\.."

node scripts/verify-question-answers.mjs --watch

pause
