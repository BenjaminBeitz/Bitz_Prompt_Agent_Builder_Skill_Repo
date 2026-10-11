# Antigravity Skills Frontmatter Validator
# Scans all SKILL.md files and verifies YAML frontmatter schemas

$baseDir = Split-Path -Parent $PSScriptRoot
$skillsDir = Join-Path $baseDir 'skills'

if (!(Test-Path $skillsDir)) {
    Write-Error "[ERROR] Skills directory not found at $skillsDir"
    exit 1
}

$skillFiles = Get-ChildItem -Path $skillsDir -Filter 'SKILL.md' -Recurse
Write-Host "[INFO] Validating $($skillFiles.Count) SKILL.md files in '$skillsDir'..."

$errors = @()
$checked = 0

foreach ($file in $skillFiles) {
    $relPath = $file.FullName.Substring($baseDir.Length + 1)
    $content = Get-Content -Path $file.FullName -Raw
    $checked++

    if (!$content.StartsWith('---')) {
        $errors += "[$relPath] Missing starting YAML frontmatter delimiter"
        continue
    }

    $parts = $content -split '---', 3
    if ($parts.Count -lt 3) {
        $errors += "[$relPath] Malformed YAML frontmatter"
        continue
    }

    $frontmatter = $parts[1]

    if ($frontmatter -notmatch '(?m)^name:\s*[\w\.\-]+') {
        $errors += "[$relPath] Missing or invalid 'name:' in frontmatter"
    }

    if ($frontmatter -notmatch '(?m)^description:\s*\S+') {
        $errors += "[$relPath] Missing or empty 'description:' in frontmatter"
    }
}

Write-Host "[INFO] Checked $checked skill files."

if ($errors.Count -gt 0) {
    Write-Host "`n[ERROR] Validation Failed with $($errors.Count) error(s):" -ForegroundColor Red
    foreach ($err in $errors) {
        Write-Host "  - $err" -ForegroundColor Red
    }
    exit 1
} else {
    Write-Host "`n[OK] All $checked Antigravity skills have 100% VALID YAML frontmatter!" -ForegroundColor Green
    exit 0
}
