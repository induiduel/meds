# ==============================================================================
# MedSoru Drive & Ders Notu Otomatik Senkronizasyon Zamanlayıcı Kurulumu
# ==============================================================================
# Bu PowerShell betiği, Windows Görev Zamanlayıcı'ya (Task Scheduler)
# her gün sabah 12:00 ve öğlen 15:00 saatlerinde 'orchestrate_drive_curriculum_ai.mjs'
# betiğini otomatik olarak arka planda çalıştıracak görevleri kaydeder.
# ==============================================================================

$ProjectDir = "C:\Users\indui\Desktop\meds"
$ScriptPath = "$ProjectDir\scripts\orchestrate_drive_curriculum_ai.mjs"
$NodeExe = (Get-Command node).Source

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  MedSoru Drive Sync - Windows Zamanlanmış Görev Kurulumu" -ForegroundColor Cyan
Write-Host "  Hedef Dizin: $ProjectDir" -ForegroundColor Gray
Write-Host "  Node Yolu:   $NodeExe" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

# 12:00 Görevi
$TaskName12 = "MedSoru_Drive_Sync_1200"
$Action12 = New-ScheduledTaskAction -Execute $NodeExe -Argument "$ScriptPath" -WorkingDirectory $ProjectDir
$Trigger12 = New-ScheduledTaskTrigger -Daily -At "12:00"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $TaskName12 -Action $Action12 -Trigger $Trigger12 -Settings $Settings -Force | Out-Null
Write-Host "✅ [12:00 Görevi] '$TaskName12' başarıyla kaydedildi." -ForegroundColor Green

# 15:00 Görevi
$TaskName15 = "MedSoru_Drive_Sync_1500"
$Action15 = New-ScheduledTaskAction -Execute $NodeExe -Argument "$ScriptPath" -WorkingDirectory $ProjectDir
$Trigger15 = New-ScheduledTaskTrigger -Daily -At "15:00"

Register-ScheduledTask -TaskName $TaskName15 -Action $Action15 -Trigger $Trigger15 -Settings $Settings -Force | Out-Null
Write-Host "✅ [15:00 Görevi] '$TaskName15' başarıyla kaydedildi." -ForegroundColor Green

Write-Host "`nHer iki görev de aktif. Görevleri görüntülemek için:" -ForegroundColor Yellow
Write-Host "Get-ScheduledTask -TaskName 'MedSoru_Drive_Sync_*'" -ForegroundColor Gray
