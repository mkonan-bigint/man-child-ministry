# Renomme les prédications et les dossiers de conventions (opération ponctuelle, nov. 2026).
param([string]$Racine = "$env:USERPROFILE\OneDrive - BigInt Analytics\Documents\Man Child Ministry")
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ok = 0; $absents = 0
function Renommer($dossier, $ancien, $nouveau) {
  $base = if ($dossier) { Join-Path $Racine $dossier } else { $Racine }
  $src = Join-Path $base $ancien
  if (Test-Path -LiteralPath $src) { Rename-Item -LiteralPath $src -NewName $nouveau; Write-Host "  ✔ $nouveau"; $script:ok++ }
  elseif (Test-Path -LiteralPath (Join-Path $base $nouveau)) { Write-Host "  = déjà fait : $nouveau" }
  else { Write-Host "  ✖ introuvable : $ancien" -ForegroundColor Yellow; $script:absents++ }
}

Write-Host "1. Fichiers"
Renommer '' '2019 0421 - Michaël la voix de l’archange il est ici maintenant pour la délivrance de chaque nom qui est dans ce livre _ Pst John Conteh..pdf' '2019 0421 Michaël la voix de l’archange il est ici maintenant pour la délivrance de chaque nom qui est dans ce livre _ Pst John Conteh.pdf'
Renommer '2021-12 Abidjan' '2021 1224 - La Vertu-Puissance pour le service est ici pour une Naissance et l''Adoption _ Pasteur John Conteh. prt 1 docx.docx' '2021 1224 La Vertu-Puissance pour le service est ici pour une Naissance et l''Adoption (partie 1) _ Pst John Conteh.docx'
Renommer '2021-12 Abidjan' '2021 1225 - Né de nouveau de la parole et l''esprit comme parlé par Mal 4  _ Pasteur John Conteh. CONV  prt 2 docx.docx' '2021 1225 Né de nouveau de la parole et l''esprit comme parlé par Mal 4 (partie 2) _ Pst John Conteh.docx'
Renommer '2023-05 Abidjan' '2023 05228 Qui est ce Melchisédek _ Pst John Conteh.docx' '2023 0528M Qui est ce Melchisédek _ Pst John Conteh.docx'
Renommer '2023-05 Abidjan' '2023 0527 Reconstruisant l''Epouse par la puissance de l''Esprit _ Pst John Conteh.docx' '2023 0527S Reconstruisant l''Epouse par la puissance de l''Esprit _ Pst John Conteh.docx'
Renommer '2023-05 Abidjan' '2023 0528 La résurrection est là _ Pst John Conteh.docx' '2023 0528S La résurrection est là _ Pst John Conteh.docx'
Renommer '2025-06 Abidjan' '2025 0606S Prédestinés à recevoir la plenitude de Dieu dans la dispensation de la plénitude des temps _ Pst .pdf' '2025 0606S Prédestinés à recevoir la plénitude de Dieu dans la dispensation de la plénitude des temps _ Pst John Conteh.pdf'
Renommer '2025-06 Abidjan' '2025 0607M Parvenir à la résurrection des morts qui est un appel final à la résurrection _ Pst John CONTEH.pdf' '2025 0607M Parvenir à la résurrection des morts qui est un appel final à la résurrection _ Pst John Conteh.pdf'
Renommer '2025-06 Abidjan' '2025 0607S La révélation de Jésus-Christ en tant que Roi Melchisédech, la Pierre de Faîte _ Part1Pst J. CONTEH.pdf' '2025 0607S La révélation de Jésus-Christ en tant que Roi Melchisédech, la Pierre de Faîte (partie 1) _ Pst John Conteh.pdf'
Renommer '2025-06 Abidjan' '2025 0608M La révélation de Jésus-Christ en tant que Roi Melchisédek, la Pierre de Faîte _ Pst John CONTEH.pdf' '2025 0608M La révélation de Jésus-Christ en tant que Roi Melchisédek, la Pierre de Faîte _ Pst John Conteh.pdf'
Renommer '2025-06 Abidjan' '2025 0608S L’omnipotence a frayé un chemin pour le miraculeux _ Pst John CONTEH.pdf' '2025 0608S L’omnipotence a frayé un chemin pour le miraculeux _ Pst John Conteh.pdf'
Renommer '2025-08 Tamatave' '2025 0814M La Charité, soit Melchisédek, est la croissance dans cette saison de la Plénitude des temps _.pdf' '2025 0814M La Charité, soit Melchisédek, est la croissance dans cette saison de la Plénitude des temps _ Pst John Conteh.pdf'
Renommer '2025-08 Tamatave' '2025 0817S Les Fils de Dieu sont de retour_ Pst John Conteh.pdf' '2025 0817S Les Fils de Dieu sont de retour _ Pst John Conteh.pdf'

Write-Host "2. Message de 2019 rangé dans son dossier de convention"
$dest = Join-Path $Racine '2019-04 Abidjan'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$src = Join-Path $Racine '2019 0421 Michaël la voix de l’archange il est ici maintenant pour la délivrance de chaque nom qui est dans ce livre _ Pst John Conteh.pdf'
if (Test-Path -LiteralPath $src) { Move-Item -LiteralPath $src -Destination $dest; Write-Host "  ✔ 2019-04 Abidjan"; $ok++ } else { Write-Host "  = déjà fait ou introuvable" }

Write-Host "3. Dossiers (ville des en-têtes)"
Renommer '' '2021-12 Abidjan' '2021-12 Dabou'
Renommer '' '2025-08 Tamatave' '2025-08 Tananarive'

Write-Host ""
Write-Host "Terminé : $ok renommage(s), $absents introuvable(s)." -ForegroundColor Green
Write-Host "Relancez ensuite l'import (tools\importer.ps1)."
