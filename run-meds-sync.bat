@echo off
chcp 65001 > nul
title MedSoru Otomasyon ve Senkronizasyon Servisi
echo =========================================================================
echo   🏥 MEDSORU TIP FAKÜLTESİ - GÜNLÜK YEREL EŞİTLEME SERVİSİ
echo =========================================================================
echo Hedef Klasör: C:\Users\indui\Desktop\meds_database
echo Tarih/Saat: %DATE% %TIME%
echo.

cd /d "C:\Users\indui\Desktop\meds"

echo [1/2] Yerel Eşitleme Motoru Başlatılıyor...
node scripts/meds-local-sync.mjs

echo.
echo [2/2] Tamamlandı. Otomasyon başarıyla sonuçlandı.
echo Bu pencereyi kapatabilirsiniz veya 10 saniye sonra kendiliğinden kapanacaktır.
timeout /t 10
