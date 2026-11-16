$startupDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcutPath = Join-Path $startupDir "DownloadsOrganizer.lnk"

# Locate pythonw (or python as fallback)
$pythonwCmd = Get-Command pythonw -ErrorAction SilentlyContinue
if ($pythonwCmd) {
    $pythonw = $pythonwCmd.Source
} else {
    $pythonw = (Get-Command python -ErrorAction Stop).Source
}

# Resolve paths dynamically relative to this script
$workDir = $PSScriptRoot
$scriptPath = Join-Path $workDir "automates-files.py"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonw
$shortcut.Arguments = "`"$scriptPath`""
$shortcut.WorkingDirectory = $workDir
$shortcut.WindowStyle = 7 # Minimized / Hidden
$shortcut.Description = "Automated Downloads Organizer"
$shortcut.Save()

Write-Host "Success! Startup shortcut created at:" -ForegroundColor Green
Write-Host $shortcutPath -ForegroundColor Cyan
Write-Host "The organizer will now start automatically in the background whenever you log into Windows." -ForegroundColor Green
