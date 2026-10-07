@echo off
chcp 65001 >nul
cd /d "C:\Users\indui\Desktop\meds"
echo =================================================================
echo 🩺 MedSoru - Google Drive & Tıbbi Ses Transkripsiyon İzleyici
echo =================================================================
node scripts/transcribe-drive-audio.mjs --watch --interval=60
pause
