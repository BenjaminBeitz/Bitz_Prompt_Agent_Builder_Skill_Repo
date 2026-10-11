<#
.SYNOPSIS
    Installs the Bitz Prompt & Agent Builder Skills Suite to global Antigravity config.
.PARAMETER DestinationPath
    Target directory for global skills (defaults to $HOME\.gemini\config\skills)
.PARAMETER DryRun
    Simulate installation without making file modifications
.PARAMETER Force
    Overwrite existing skills without prompting
.EXAMPLE
    powershell -File scripts/install-global.ps1 -DryRun
    powershell -File scripts/install-global.ps1 -Force
#>
param (
    [string]$DestinationPath = "$env:USERPROFILE\.gemini\config\skills",
    [switch]$DryRun,
    [switch]$Force
)

$baseDir = Split-Path -Parent $PSScriptRoot
$skillsSource = Join-Path $baseDir 'skills'

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Bitz Prompt & Agent Builder Skills Suite Global Installer" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Source:      $skillsSource"
Write-Host "Destination: $DestinationPath"
Write-Host "DryRun:      $($DryRun.IsPresent)"
Write-Host ""

if (!(Test-Path $skillsSource)) {
    Write-Error "[ERROR] Source skills directory not found: $skillsSource"
    exit 1
}

$categories = @(
    '01-prompt-engineering',
    '02-agent-builder'
)

$totalCopied = 0
$totalSkipped = 0

foreach ($cat in $categories) {
    $catDir = Join-Path $skillsSource $cat
    if (!(Test-Path $catDir)) { continue }

    $skillFolders = Get-ChildItem -Path $catDir -Directory
    Write-Host "`n[$cat] ($($skillFolders.Count) skills)" -ForegroundColor Yellow

    foreach ($folder in $skillFolders) {
        $skillName = $folder.Name
        $targetDir = Join-Path $DestinationPath $skillName
        
        $exists = Test-Path $targetDir

        if ($exists -and !$Force) {
            Write-Host "  [-] $skillName (already exists, skipping - use -Force to overwrite)" -ForegroundColor DarkGray
            $totalSkipped++
            continue
        }

        if ($DryRun) {
            Write-Host "  [+] [DRY-RUN] Would install '$skillName' -> $targetDir" -ForegroundColor Green
            $totalCopied++
        } else {
            if (!(Test-Path $DestinationPath)) {
                New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
            }
            Copy-Item -Path $folder.FullName -Destination $targetDir -Recurse -Force
            Write-Host "  [+] Installed '$skillName'" -ForegroundColor Green
            $totalCopied++
        }
    }
}

Write-Host "`n----------------------------------------------------------"
if ($DryRun) {
    Write-Host "Dry-Run Complete: $totalCopied skills eligible to install, $totalSkipped skipped." -ForegroundColor Cyan
} else {
    Write-Host "Installation Complete: $totalCopied skills installed to $DestinationPath." -ForegroundColor Green
    Write-Host "Google Antigravity will now auto-discover these skills globally across all workspaces!" -ForegroundColor Cyan
}
