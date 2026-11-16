$vbsPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Start_MeDSor_Audio_Watcher.vbs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$vbsPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "MeDSor_Transcription_Watcher" -Action $action -Trigger $trigger -Description "MeDSor Google Drive Ses Transkripsiyon Servisi" -Force
Write-Output "✅ Windows Scheduled Task 'MeDSor_Transcription_Watcher' başarıyla kaydedildi."
