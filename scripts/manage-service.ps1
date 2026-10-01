param(
    [ValidateSet("install-and-start", "status", "stop", "sync-now", "notify")]
    [string]$Action = "install-and-start",
    [string]$Title = "MedSoru Otomasyon Servisi 🚀",
    [string]$Message = "Windows başlangıcına eklendi ve arka planda başlatıldı."
)

$ErrorActionPreference = "Stop"

$desktopPath = [Environment]::GetFolderPath('Desktop')
$startupPath = [Environment]::GetFolderPath('Startup')
$medsDir = "C:\Users\indui\Desktop\meds"

$desktopShortcut = Join-Path $desktopPath "MedSoru Otomasyon Servisi.lnk"
$startupShortcut = Join-Path $startupPath "MedSoru Otomasyon Servisi.lnk"
$daemonVbs = Join-Path $medsDir "start-meds-daemon.vbs"
$serviceBat = Join-Path $medsDir "start-meds-service.bat"
$notificationScript = Join-Path $medsDir "scripts\show-notification.ps1"

function Show-Toast([string]$t, [string]$m) {
    if (Test-Path $notificationScript) {
        try {
            powershell.exe -NoProfile -ExecutionPolicy Bypass -File $notificationScript -Title $t -Message $m
        } catch {}
    }
}

function Get-RunningProcesses() {
    return @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -eq "node.exe" -and $_.CommandLine -like "*meds-local-sync.mjs*"
    })
}

function Create-Shortcut([string]$shortcutPath, [string]$targetPath, [string]$arguments, [string]$workingDir, [string]$description, [string]$icon) {
    $wsh = New-Object -ComObject WScript.Shell
    $s = $wsh.CreateShortcut($shortcutPath)
    $s.TargetPath = $targetPath
    if ($arguments) { $s.Arguments = $arguments }
    $s.WorkingDirectory = $workingDir
    $s.Description = $description
    if ($icon) { $s.IconLocation = $icon }
    $s.Save()
}

switch ($Action) {
    "notify" {
        Show-Toast $Title $Message
        Write-Output "Notification sent."
    }

    "status" {
        $procs = @(Get-RunningProcesses)
        $isRunning = ($procs.Count -gt 0)
        $pids = @($procs | ForEach-Object { $_.ProcessId })
        $result = @{
            isInstalledOnDesktop = (Test-Path $desktopShortcut)
            isRegisteredInStartup = (Test-Path $startupShortcut)
            isRunning = $isRunning
            pids = $pids
            desktopShortcutPath = $desktopShortcut
            startupShortcutPath = $startupShortcut
        }
        $json = $result | ConvertTo-Json -Compress
        Write-Output $json
    }

    "stop" {
        $procs = Get-RunningProcesses
        $count = $procs.Count
        foreach ($p in $procs) {
            Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
        }
        Show-Toast "MedSoru Otomasyon Servisi ⏹️" "$count adet arka plan işleyici süreci durduruldu."
        Write-Output "Stopped $count processes."
    }

    "sync-now" {
        Write-Output "Triggering immediate sync..."
        Show-Toast "MedSoru: Senkronizasyon Başlatıldı ⏳" "Google Drive ve yerel klasör taranıyor..."
        Start-Process -FilePath "node.exe" -ArgumentList "`"$medsDir\scripts\meds-local-sync.mjs`"", "--sync-now" -WorkingDirectory $medsDir -WindowStyle Hidden
    }

    "install-and-start" {
        Write-Output "1. Creating Desktop shortcut..."
        Create-Shortcut -shortcutPath $desktopShortcut `
                        -targetPath $serviceBat `
                        -arguments "" `
                        -workingDir $medsDir `
                        -description "MedSoru Tıp Fakültesi Günlük Senkronizasyon ve Windows Başlangıç Servisi" `
                        -icon "shell32.dll,238"

        Write-Output "2. Registering in Windows Startup ($startupPath)..."
        Create-Shortcut -shortcutPath $startupShortcut `
                        -targetPath "wscript.exe" `
                        -arguments "`"$daemonVbs`"" `
                        -workingDir $medsDir `
                        -description "MedSoru Günlük Arka Plan Senkronizasyon Servisi (Otomatik Başlangıç)" `
                        -icon "shell32.dll,238"

        Write-Output "3. Checking running service processes..."
        $procs = Get-RunningProcesses
        if ($procs.Count -eq 0) {
            Write-Output "Starting background daemon..."
            Start-Process -FilePath "wscript.exe" -ArgumentList "`"$daemonVbs`"" -WorkingDirectory $medsDir
            Start-Sleep -Milliseconds 600
        } else {
            Write-Output "Service is already running (PID: $(($procs | ForEach-Object { $_.ProcessId }) -join ', '))."
        }

        Write-Output "4. Sending Windows Toast Notification..."
        Show-Toast "MedSoru Otomasyon Servisi Aktif 🚀" "Windows Başlangıcına Eklendi! Servis arka planda çalışıyor. Her gün 16:00 - 18:00 arasında otomatik eşitlenecektir."

        Write-Output "SUCCESS: Installed on Desktop, registered in Startup, and service started."
    }
}
