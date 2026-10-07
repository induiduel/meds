$vbsPath = "$PSScriptRoot\start-git-sync-silent.vbs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$vbsPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "MedSoru_Git_Auto_Sync" -Action $action -Trigger $trigger -Description "MedSoru 20 Dakikalık Otomatik Git Senkronizasyon Servisi" -Force
Write-Output "✅ Windows Görev Zamanlayıcı 'MedSoru_Git_Auto_Sync' başarıyla kaydedildi."
