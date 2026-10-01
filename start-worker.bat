@echo off
title MedSoru Yerel Arka Plan Isleyicisi
color 0A
echo ======================================================================
echo    MEDSORU TIP FAKULTESI - YEREL ARKA PLAN SENKRONIZASYON ISLEYICISI
echo ======================================================================
echo Bilgisayariniz acik kaldigi surece Google Drive ders slaytlari ve
echo cikmis sorular otomatik olarak taranip veritabanina islenecektir.
echo AI token harcamadan kendi baglantinizla arkaplanda calisir.
echo.
echo Baslatiliyor...
node scripts/local-drive-sync-agent.mjs
pause
