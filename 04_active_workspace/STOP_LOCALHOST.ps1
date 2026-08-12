param([int]$Port = 5051)

$connections = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($connections) {
    $connections | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
    Write-Host "Stopped the process listening on port $Port."
} else {
    Write-Host "No LearnSphere process is listening on port $Port."
}
