@echo off
chcp 65001 >nul
title MedSoru - Soru ve Cevap Doğrulama Motoru (%%90 Kuralı)
color 0B

echo ======================================================================
echo    MEDSORU - ÇIKMIŞ SORU VE CEVAP DOĞRULAMA MOTORU
echo    (Amfi Ders Notları ve Tıp Literatürü ile %%90 Eşleşme Kontrolü)
echo ======================================================================
echo.
echo Bu işlem:
echo 1. Soru havuzundaki doğrulanmamış soruları tespit eder.
echo 2. Amfi ders notları (meds_database) ve tıp literatürüyle karşılaştırır.
echo 3. %%90 eşleşme sağlayamayan soruların güvenilirlik derecesini düşürür,
echo    doğru cevabı boş bırakır ve soruyu 'ŞÜPHELİ CEVAP' olarak işaretler.
echo.

cd /d "%~dp0\.."

node scripts/verify-question-answers.mjs --unverified --limit 25

echo.
echo ======================================================================
echo Denetim tamamlandı! Rapor: data/verification_report.json
echo ======================================================================
pause
