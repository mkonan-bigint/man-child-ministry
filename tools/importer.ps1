# Importe les prédications (PDF / Word) dans l'application Man Child Ministry.
# Chaque sous-dossier du dossier source = une convention (ex. "2025-12 Abidjan", "2026-04 Lomé").
param(
  [string]$Source = "$env:USERPROFILE\OneDrive - BigInt Analytics\Documents\Man Child Ministry"
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Write-Host "Vérification des modules Python (pymupdf, python-docx)..."
python -m pip install --quiet --disable-pip-version-check pymupdf python-docx
Write-Host "Import depuis : $Source"
python "$PSScriptRoot\extract.py" "$Source" "$repo\www\library.json"
if ($LASTEXITCODE -ne 0) { throw "L'import a échoué." }
Write-Host ""
Write-Host "Bibliothèque mise à jour : $repo\www\library.json" -ForegroundColor Green
Write-Host "Publiez ensuite avec Git (add, commit, push) : l'APK et la version iPhone se mettent à jour automatiquement."
