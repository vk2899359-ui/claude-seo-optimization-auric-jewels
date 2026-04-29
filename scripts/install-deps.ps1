# Auric Jewels — One-time dependency installer
# Run once from PowerShell (as Administrator if needed):
#   .\scripts\install-deps.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Auric Jewels SEO — Dependency Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Install Python packages
Write-Host "Installing Python packages..." -ForegroundColor Yellow
pip install anthropic playwright
if ($LASTEXITCODE -ne 0) {
    Write-Host "pip install failed. Make sure Python is in PATH." -ForegroundColor Red
    exit 1
}

# 2. Install Playwright's Chromium browser
Write-Host ""
Write-Host "Installing Playwright Chromium browser..." -ForegroundColor Yellow
playwright install chromium
if ($LASTEXITCODE -ne 0) {
    # Try via python -m
    python -m playwright install chromium
}

# 3. Verify
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
python -c "import anthropic; print('  anthropic:', anthropic.__version__)"
python -c "from playwright.sync_api import sync_playwright; print('  playwright: OK')"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup complete." -ForegroundColor Green
Write-Host "  Next step: set your API key, then run setup-task-scheduler.ps1" -ForegroundColor Green
Write-Host ""
Write-Host "  Set API key (current PowerShell session):" -ForegroundColor White
Write-Host '  $env:ANTHROPIC_API_KEY = "sk-ant-..."' -ForegroundColor Gray
Write-Host ""
Write-Host "  Set API key permanently (all future sessions):" -ForegroundColor White
Write-Host '  [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY","sk-ant-...","User")' -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
