param([int]$Port = 5051)

$workspaceRoot = Split-Path -Parent $PSScriptRoot
$codeRoot = Join-Path $workspaceRoot '06_code'
$venvPython = Join-Path $codeRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $venvPython)) {
    Write-Host 'Creating the active-workspace virtual environment...'
    python -m venv (Join-Path $codeRoot '.venv')
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r (Join-Path $codeRoot 'requirements.txt')
}

$env:PORT = $Port
$env:CORS_ORIGINS = "http://localhost:$Port,http://127.0.0.1:$Port"
$env:FLASK_DEBUG = '0'
Set-Location $codeRoot
Write-Host "LearnSphere AI active workspace is running at http://localhost:$Port"
& $venvPython backend\app.py

