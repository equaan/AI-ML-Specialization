$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$backendDir = Join-Path $repoRoot "backend"
$frontendDir = Join-Path $repoRoot "frontend"
$uvicornExe = Join-Path $repoRoot "venv\Scripts\uvicorn.exe"
$pythonExe = Join-Path $repoRoot "venv\Scripts\python.exe"
$ngrokWinGetPath = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links\ngrok.exe"
$ollamaExe = "D:\Ollama\ollama.exe"
$ollamaModelsDir = "D:\OllamaModels"

function Wait-ForHttpOk {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Url,
    [int]$TimeoutSeconds = 60,
    [int]$IntervalSeconds = 2,
    [hashtable]$Headers = @{}
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-WebRequest -Uri $Url -Headers $Headers -UseBasicParsing -TimeoutSec 5
      if ([int]$response.StatusCode -eq 200) {
        return $true
      }
    } catch {
      Start-Sleep -Seconds $IntervalSeconds
    }
  }

  return $false
}

function Get-NgrokTunnelInfo {
  param(
    [int]$TimeoutSeconds = 45,
    [string]$LogPath = ""
  )

  $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
  while ((Get-Date) -lt $deadline) {
    foreach ($port in 4040..4100) {
      try {
        $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$port/api/tunnels" -UseBasicParsing -TimeoutSec 3
        $payload = $resp.Content | ConvertFrom-Json
        $httpsTunnel = $payload.tunnels | Where-Object { $_.public_url -like "https://*" } | Select-Object -First 1
        if ($httpsTunnel -and $httpsTunnel.public_url) {
          return [pscustomobject]@{
            PublicUrl = [string]$httpsTunnel.public_url
            InspectPort = [int]$port
          }
        }
      } catch {
        continue
      }
    }

    if ($LogPath -and (Test-Path $LogPath)) {
      try {
        $tail = Get-Content -Path $LogPath -Tail 100 -Encoding Unicode -ErrorAction SilentlyContinue
        if (-not $tail) {
          $tail = Get-Content -Path $LogPath -Tail 100 -Encoding UTF8 -ErrorAction SilentlyContinue
        }
        $matchedLine = $tail | Where-Object { $_ -match "url=https://[^\s]+" } | Select-Object -Last 1
        if ($matchedLine) {
          $url = [regex]::Match($matchedLine, "https://[^\s]+").Value
          if ($url) {
            return [pscustomobject]@{
              PublicUrl = [string]$url
              InspectPort = -1
            }
          }
        }
      } catch {
      }
    }

    Start-Sleep -Seconds 2
  }

  return $null
}

function Kill-StaleProcessesAndPorts {
  Write-Output "Killing stale processes (ollama/backend/frontend/ngrok)..."

  foreach ($name in @("ngrok", "ollama", "uvicorn", "node", "npm")) {
    $procs = Get-Process -Name $name -ErrorAction SilentlyContinue
    if ($procs) {
      $procs | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
    }
  }

  foreach ($port in @(8000, 3000, 5173, 4040, 11434)) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
      $conns | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    }
  }
}

if (-not (Test-Path $uvicornExe)) {
  throw "uvicorn not found at '$uvicornExe'. Create venv and install backend requirements first."
}

if (-not (Test-Path $pythonExe)) {
  throw "python not found at '$pythonExe'. Create venv and install backend requirements first."
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  throw "npm is not available in this shell. Install Node.js and retry."
}

$ngrokExe = $null
$ngrokCmdInfo = Get-Command ngrok -ErrorAction SilentlyContinue
if ($ngrokCmdInfo) {
  $ngrokExe = $ngrokCmdInfo.Source
} elseif (Test-Path $ngrokWinGetPath) {
  $ngrokExe = $ngrokWinGetPath
} else {
  throw "ngrok command not found. Install ngrok or add it to PATH."
}

if (-not (Test-Path $ollamaExe)) {
  throw "Ollama executable not found at '$ollamaExe'."
}

Kill-StaleProcessesAndPorts

$ollamaCmd = "`$env:OLLAMA_MODELS='$ollamaModelsDir'; & '$ollamaExe' serve"
$backendCmd = "Set-Location '$repoRoot'; & '$uvicornExe' backend.main:app --host 127.0.0.1 --port 8000"
$frontendCmd = "Set-Location '$frontendDir'; npx vite --host 127.0.0.1 --port 3000"
$ngrokStdout = Join-Path $repoRoot "ngrok_runtime.log"
$ngrokStderr = Join-Path $repoRoot "ngrok_runtime.err.log"
if (Test-Path $ngrokStdout) { Remove-Item $ngrokStdout -Force }
if (Test-Path $ngrokStderr) { Remove-Item $ngrokStderr -Force }

# Clean up stale ngrok processes so inspect ports are not locked.
$existingNgrok = Get-Process ngrok -ErrorAction SilentlyContinue
if ($existingNgrok) {
  $existingNgrok | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", $ollamaCmd | Out-Null

Write-Output "Waiting for Ollama API..."
$ollamaReady = Wait-ForHttpOk -Url "http://127.0.0.1:11434/api/tags" -TimeoutSeconds 90
if (-not $ollamaReady) {
  throw "Ollama did not become healthy at http://127.0.0.1:11434/api/tags within timeout."
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd | Out-Null

Write-Output "Waiting for backend health check..."
$backendReady = Wait-ForHttpOk -Url "http://127.0.0.1:8000/health" -TimeoutSeconds 90
if (-not $backendReady) {
  throw "Backend did not become healthy at http://127.0.0.1:8000/health within timeout."
}

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd | Out-Null

Write-Output "Waiting for frontend to be available..."
$frontendReady = Wait-ForHttpOk -Url "http://127.0.0.1:3000" -TimeoutSeconds 120
if (-not $frontendReady) {
  throw "Frontend did not become available at http://127.0.0.1:3000 within timeout."
}

$ngrokProc = Start-Process -FilePath $ngrokExe -ArgumentList @("http", "3000", "--log", "stdout") -WorkingDirectory $repoRoot -RedirectStandardOutput $ngrokStdout -RedirectStandardError $ngrokStderr -PassThru
Start-Sleep -Seconds 1
if (-not (Get-Process -Id $ngrokProc.Id -ErrorAction SilentlyContinue)) {
  throw "ngrok process exited immediately. Check logs: $ngrokStdout and $ngrokStderr"
}

Write-Output "Waiting for ngrok tunnel..."
$tunnelInfo = Get-NgrokTunnelInfo -TimeoutSeconds 90 -LogPath $ngrokStdout
if (-not $tunnelInfo) {
  throw "ngrok tunnel URL was not detected from inspect API ports (4040-4100) or ngrok runtime logs."
}

$publicUrl = $tunnelInfo.PublicUrl
$inspectPort = $tunnelInfo.InspectPort

# These make /health and /stats appear in ngrok inspector history.
$ngrokHealthReady = Wait-ForHttpOk -Url "$publicUrl/health" -TimeoutSeconds 45 -Headers @{ Accept = "application/json" }
$ngrokStatsReady = Wait-ForHttpOk -Url "$publicUrl/stats" -TimeoutSeconds 45 -Headers @{ Accept = "application/json" }

Set-Content -Path (Join-Path $repoRoot "ngrok_url.txt") -Value $publicUrl

Write-Output "Started ollama, backend, frontend, and ngrok in separate PowerShell windows."
Write-Output "Open http://localhost:3000 on this PC."
Write-Output "Use this ngrok URL on your laptop: $publicUrl"
if ($inspectPort -gt 0) {
  Write-Output "ngrok inspector UI: http://127.0.0.1:$inspectPort"
} else {
  Write-Output "ngrok inspector UI port not detected from API (URL recovered from log fallback)."
}
Write-Output "Saved ngrok URL to: $repoRoot\ngrok_url.txt"
Write-Output "Saved ngrok runtime log to: $ngrokStdout"
Write-Output "Laptop health check URL: $publicUrl/health"
Write-Output "Laptop stats check URL: $publicUrl/stats"
if ($ngrokHealthReady) {
  Write-Output "ngrok health probe: OK (public /health is responding)."
} else {
  Write-Output "ngrok health probe: FAILED (public /health not responding yet)."
}
if ($ngrokStatsReady) {
  Write-Output "ngrok stats probe: OK (public /stats is responding)."
} else {
  Write-Output "ngrok stats probe: FAILED (public /stats not responding yet)."
}
