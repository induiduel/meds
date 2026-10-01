@echo off
setlocal enabledelayedexpansion
title MedSoru Tıp Fakültesi - Yerel Arka Plan Senkronizasyon İşleyicisi
color 0A
cls

:: Calisma dizinini bu bat dosyasinin bulundugu klasor olarak sabitle
cd /d "%~dp0"

echo ======================================================================
echo    MEDSORU TIP FAKULTESI - YEREL ARKA PLAN SENKRONIZASYON ISLEYICISI
echo ======================================================================
echo Bilgisayariniz acik kaldigi surece Google Drive ders slaytlari ve
echo cikmis sorular otomatik olarak taranip veritabanina islenecektir.
echo.
echo [DURUM KONTROLU]:
echo 1. Bu pencere acik kaldigi surece isleyici arkaplanda aktiftir.
echo 2. Ekranda her 20 saniyede bir "[Sinyal Gonderildi]" mesaji gorursunuz.
echo 3. MedSoru Admin Panelinde "Otomasyonlar" sekmesinde aninda "CEVRIMICI" yanar.
echo.

:: Node.js kontrolu
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  color 0C
  echo ======================================================================
  echo [HATA] Bilgisayarinizda Node.js bulunamadi!
  echo ======================================================================
  echo Bu otomasyonun arka planda dosyalarinizi okuyabilmesi icin Node.js gereklidir.
  echo Lutfen https://nodejs.org adresine gidip ucretsiz Node.js (LTS) surumunu kurunuz.
  echo Kurulum sonrasinda bu dosyaya tekrar cift tikladiginizda otomatik baslayacaktir.
  echo ======================================================================
  echo.
  pause
  exit /b 1
)

echo [KONTROL] Node.js surumu:
node -v
echo.
echo [BASLATILIYOR...] Lutfen bu pencereyi kapatmayiniz (simge durumuna kucultebilirsiniz).
echo ----------------------------------------------------------------------

if exist "%~dp0scripts\local-drive-sync-agent.mjs" (
  node "%~dp0scripts\local-drive-sync-agent.mjs"
) else if exist "scripts\local-drive-sync-agent.mjs" (
  node "scripts\local-drive-sync-agent.mjs"
) else (
  color 0C
  echo [HATA] scripts\local-drive-sync-agent.mjs dosyasi bulunamadi.
  echo Lutfen projenin tum dosyalarinin ayni klasorde oldugundan emin olunuz.
)

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo [UYARI] Isleyici durduruldu veya bir hata meydana geldi.
)
pause

