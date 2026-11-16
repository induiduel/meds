$vbsPath = "$PSScriptRoot\start-git-sync-silent.vbs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$vbsPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "MeDSor_Git_Auto_Sync" -Action $action -Trigger $trigger -Description "MeDSor 20 Dakikalık Otomatik Git Senkronizasyon Servisi" -Force
Write-Output "✅ Windows Görev Zamanlayıcı 'MeDSor_Git_Auto_Sync' başarıyla kaydedildi."
