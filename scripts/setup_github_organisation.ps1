param(
    [string]$Owner = "Berserkyr",
    [string]$Repo = "rpg-40k"
)

$ErrorActionPreference = "Stop"

function Ensure-GhAuth {
    gh auth status | Out-Null
}

function Get-RepoSlug {
    return "$Owner/$Repo"
}

function Ensure-Label {
    param(
        [string]$RepoSlug,
        [string]$Name,
        [string]$Color,
        [string]$Description
    )

    $allLabels = gh label list --repo $RepoSlug --limit 200 --json name | ConvertFrom-Json
    $exists = $allLabels | Where-Object { $_.name -eq $Name }
    if ($exists) {
        gh label edit "$Name" --repo $RepoSlug --color "$Color" --description "$Description" | Out-Null
        Write-Host "[OK] Label maj: $Name"
    } else {
        gh label create "$Name" --repo $RepoSlug --color "$Color" --description "$Description" | Out-Null
        Write-Host "[OK] Label cree: $Name"
    }
}

function Ensure-Milestone {
    param(
        [string]$RepoSlug,
        [string]$Title,
        [string]$Description
    )

    $allMilestones = gh api "repos/$RepoSlug/milestones?state=all" | ConvertFrom-Json
    $existing = $allMilestones | Where-Object { $_.title -eq $Title } | Select-Object -First 1
    if ($existing) {
        gh api "repos/$RepoSlug/milestones/$($existing.number)" --method PATCH -f title="$Title" -f description="$Description" -f state="open" | Out-Null
        Write-Host "[OK] Jalon maj: $Title"
    } else {
        gh api "repos/$RepoSlug/milestones" --method POST -f title="$Title" -f description="$Description" -f state="open" | Out-Null
        Write-Host "[OK] Jalon cree: $Title"
    }
}

function Main {
    Ensure-GhAuth
    $repoSlug = Get-RepoSlug

    $labelsPath = Join-Path $PSScriptRoot "..\.github\labels.json"
    $milestonesPath = Join-Path $PSScriptRoot "..\.github\milestones.json"

    $labels = Get-Content $labelsPath -Raw | ConvertFrom-Json
    $milestones = Get-Content $milestonesPath -Raw | ConvertFrom-Json

    Write-Host "--- Synchronisation labels ---"
    foreach ($label in $labels) {
        Ensure-Label -RepoSlug $repoSlug -Name $label.name -Color $label.color -Description $label.description
    }

    Write-Host "--- Synchronisation jalons ---"
    foreach ($ms in $milestones) {
        Ensure-Milestone -RepoSlug $repoSlug -Title $ms.title -Description $ms.description
    }

    Write-Host "Termine: organisation GitHub synchronisee pour $repoSlug"
}

Main
