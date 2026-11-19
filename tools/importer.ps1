# Importe les prédications (PDF / Word) dans l'application Man Child Ministry.
# Chaque sous-dossier du dossier source = une convention (ex. "2025-12 Abidjan", "2026-04 Lomé").
param(
  [string]$Source = "$env:USERPROFILE\OneDrive - BigInt Analytics\Documents\Man Child Ministry"
)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$repo = Split-Path -Parent $PSScriptRoot

# --- Trouver un vrai Python (et pas le raccourci du Microsoft Store) ---
function Find-Python {
  $candidates = @()
  foreach ($name in @("python", "python3", "py")) {
    Get-Command $name -All -ErrorAction SilentlyContinue | ForEach-Object {
      if ($_.Source -and $_.Source -notmatch "WindowsApps") { $candidates += $_.Source }
    }
  }
  $roots = @("$env:USERPROFILE\MiniConda3", "$env:USERPROFILE\miniconda3", "$env:USERPROFILE\anaconda3",
             "$env:USERPROFILE\Anaconda3", "$env:LOCALAPPDATA\miniconda3", "$env:LOCALAPPDATA\anaconda3",
             "$env:ProgramData\miniconda3", "$env:ProgramData\anaconda3", "C:\miniconda3", "C:\anaconda3")
  foreach ($r in $roots) { if (Test-Path "$r\python.exe") { $candidates += "$r\python.exe" } }
  Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python3*\python.exe" -ErrorAction SilentlyContinue |
    Sort-Object FullName -Descending | ForEach-Object { $candidates += $_.FullName }
  foreach ($c in $candidates) {
    try { & $c -c "import sys; assert sys.version_info >= (3, 8)" 2>$null; if ($LASTEXITCODE -eq 0) { return $c } } catch {}
  }
  return $null
}

$python = Find-Python
if (-not $python) {
  Write-Host "Aucune installation de Python trouvée." -ForegroundColor Red
  Write-Host "Installez Python depuis https://www.python.org/downloads/ (cocher « Add python.exe to PATH »), puis relancez."
  exit 1
}
Write-Host "Python utilisé : $python"

Write-Host "Vérification des modules Python (pymupdf, python-docx, openpyxl)..."
& $python -m pip install --quiet --disable-pip-version-check pymupdf python-docx openpyxl --no-warn-script-location
if ($LASTEXITCODE -ne 0) { Write-Host "Installation des modules impossible (connexion Internet ?)." -ForegroundColor Red; exit 1 }

Write-Host "Import depuis : $Source"
& $python "$PSScriptRoot\extract.py" "$Source" "$repo\www\library.json" "$repo\conventions.xlsx"
if ($LASTEXITCODE -ne 0) { Write-Host "L'import a échoué (voir le message ci-dessus)." -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "Bibliothèque mise à jour : $repo\www\library.json" -ForegroundColor Green
Write-Host "Publiez ensuite avec Git (add, commit, push) : l'APK et la version iPhone se mettent à jour automatiquement."
