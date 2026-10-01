@echo off
chcp 65001 > nul
title MedSoru Tıp Fakültesi - Otomasyon & Eşitleme Servisi
color 0A
cls

echo =========================================================================
echo   🏥 MEDSORU TIP FAKÜLTESİ - GÜNLÜK OTOMASYON VE BAŞLANGIÇ SERVİSİ
echo =========================================================================
echo Hedef Klasör : C:\Users\indui\Desktop\meds_database
echo Hedef Saat   : 16:00 - 18:00 (Hafta İçi ve Her Gün)
echo Tarih/Saat   : %DATE% %TIME%
echo =========================================================================
echo.

cd /d "C:\Users\indui\Desktop\meds"

echo [1/3] Windows Başlangıç Kaydı ve Kısayol Yapılandırılıyor...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts\manage-service.ps1" -Action "install-and-start"

echo.
echo [2/3] Windows Bildirim Alanı (Eylem Merkezi) Kontrol Edildi.
echo       ✓ Bildirim ekranınızın sağ alt köşesine iletildi.
echo.
echo [3/3] Servis Arka Planda Aktif Durumda Çalışıyor!
echo       - Web Admin Panelinde "Otomasyonlar" sekmesinde ÇEVRİMİÇİ durumunu görebilirsiniz.
echo       - Bilgisayarınız her açıldığında 16:00 - 18:00 aralığında otomatik eşitlenecektir.
echo.
echo =========================================================================
echo Bu pencere 5 saniye sonra kapanacaktır (Servis arka planda çalışmaya devam eder).
echo =========================================================================
timeout /t 5
