$vbsPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Start_MedSoru_Audio_Watcher.vbs"
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$vbsPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "MedSoru_Transcription_Watcher" -Action $action -Trigger $trigger -Description "MedSoru Google Drive Ses Transkripsiyon Servisi" -Force
Write-Output "✅ Windows Scheduled Task 'MedSoru_Transcription_Watcher' başarıyla kaydedildi."
