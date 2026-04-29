# Auric Jewels — Windows Task Scheduler setup
# Creates a daily 9 AM task that runs daily-seo-routine.py
#
# Run from PowerShell (Administrator recommended):
#   .\scripts\setup-task-scheduler.ps1
#
# To remove the task later:
#   schtasks /delete /tn "AuricJewelsDailySEO" /f

$TaskName   = "AuricJewelsDailySEO"
$ScriptPath = Join-Path $PSScriptRoot "daily-seo-routine.py"
$LogPath    = Join-Path $PSScriptRoot "..\logs"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Auric Jewels — Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── Resolve Python path ───────────────────────────────────────────────────────
$PythonPath = $null
try {
    $PythonPath = (Get-Command python -ErrorAction Stop).Source
    Write-Host "  Python found: $PythonPath" -ForegroundColor Green
} catch {
    # Try common install locations
    $candidates = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) { $PythonPath = $c; break }
    }
}

if (-not $PythonPath) {
    Write-Host "  ERROR: Python not found. Install Python and add it to PATH." -ForegroundColor Red
    exit 1
}

# ── Resolve script path ───────────────────────────────────────────────────────
if (-not (Test-Path $ScriptPath)) {
    Write-Host "  ERROR: Script not found at: $ScriptPath" -ForegroundColor Red
    exit 1
}
Write-Host "  Script  : $ScriptPath" -ForegroundColor White

# ── Create logs directory ─────────────────────────────────────────────────────
if (-not (Test-Path $LogPath)) {
    New-Item -ItemType Directory -Path $LogPath | Out-Null
}
$LogFile = Join-Path $LogPath "daily-seo-%DATE:~-4,4%%DATE:~-7,2%%DATE:~-10,2%.log"

# ── Build the task command ────────────────────────────────────────────────────
# Wraps the python call in cmd /c so stdout/stderr are captured to a log file.
$Command = "cmd /c `"`"$PythonPath`" `"$ScriptPath`" >> `"$LogFile`" 2>&1`""

# ── Remove existing task if present ──────────────────────────────────────────
$exists = schtasks /query /tn $TaskName 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  Removing existing task '$TaskName'…" -ForegroundColor Yellow
    schtasks /delete /tn $TaskName /f | Out-Null
}

# ── Register the task ─────────────────────────────────────────────────────────
Write-Host "  Registering task '$TaskName' (daily at 09:00)…" -ForegroundColor Yellow

# Build environment variable passthrough for ANTHROPIC_API_KEY
$ApiKey = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
if (-not $ApiKey) {
    $ApiKey = $env:ANTHROPIC_API_KEY
}

# Use SchTasks for broadest compatibility (works on all Windows versions)
schtasks /create `
    /tn  $TaskName `
    /tr  $Command `
    /sc  daily `
    /st  09:00 `
    /ru  $env:USERNAME `
    /rl  HIGHEST `
    /f

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: schtasks /create failed (exit $LASTEXITCODE)." -ForegroundColor Red
    Write-Host "  Try running PowerShell as Administrator." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Task registered successfully." -ForegroundColor Green
Write-Host ""
Write-Host "  Name    : $TaskName" -ForegroundColor White
Write-Host "  Runs    : Daily at 09:00" -ForegroundColor White
Write-Host "  Script  : $ScriptPath" -ForegroundColor White
Write-Host "  Logs    : $LogPath\daily-seo-*.log" -ForegroundColor White
Write-Host ""

# ── Warn if API key not set ───────────────────────────────────────────────────
if (-not $ApiKey) {
    Write-Host "  !! ANTHROPIC_API_KEY is not set." -ForegroundColor Red
    Write-Host "  The routine will use template fallback blogs until you set it:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host '  [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY","sk-ant-...","User")' -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "  ANTHROPIC_API_KEY : set (${ApiKey.Substring(0,12)}…)" -ForegroundColor Green
}

Write-Host "  To run immediately:  schtasks /run /tn $TaskName" -ForegroundColor Cyan
Write-Host "  To view status:      schtasks /query /tn $TaskName /fo LIST" -ForegroundColor Cyan
Write-Host "  To remove:           schtasks /delete /tn $TaskName /f" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
