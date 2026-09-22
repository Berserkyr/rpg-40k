param(
    [string]$Owner = "Berserkyr",
    [string]$Repo = "rpg-40k"
)

$ErrorActionPreference = "Stop"
$repoSlug = "$Owner/$Repo"

$allIssues = gh issue list --repo $repoSlug --state all --limit 300 --json number,title,url | ConvertFrom-Json

$epicTitles = @{
    M1 = '[EPIC] M1 - Stabilisation API et securite'
    M2 = '[EPIC] M2 - Gameplay et persistance'
    M3 = '[EPIC] M3 - Frontend UX et narration'
    M4 = '[EPIC] M4 - Livraison et exploitation'
    M5 = '[EPIC] M5 - Documentation et soutenance RNCP'
}

$milestones = @{
    M1 = 'M1 - Stabilisation API et securite'
    M2 = 'M2 - Gameplay et persistance'
    M3 = 'M3 - Frontend UX et narration'
    M4 = 'M4 - Livraison et exploitation'
    M5 = 'M5 - Documentation et soutenance RNCP'
}

$epics = @{}
foreach ($k in $epicTitles.Keys) {
    $epic = $allIssues | Where-Object { $_.title -eq $epicTitles[$k] } | Select-Object -First 1
    if (-not $epic) {
        throw "EPIC introuvable: $($epicTitles[$k])"
    }
    $epics[$k] = $epic
}

$tasks = @(
    # M1
    @{Epic='M1'; Domain='backend'; Type='type:chore'; Prio='prio:P1'; Title='Durcir validation des payloads auth et erreurs API'},
    @{Epic='M1'; Domain='frontend'; Type='type:feature'; Prio='prio:P2'; Title='Uniformiser messages UX de connexion et session expiree'},
    @{Epic='M1'; Domain='infra'; Type='type:chore'; Prio='prio:P1'; Title='Verifier healthchecks et metriques de disponibilite'},
    @{Epic='M1'; Domain='docs'; Type='type:docs'; Prio='prio:P2'; Title='Documenter procedure de diagnostic incident auth/API'},
    @{Epic='M1'; Domain='tests'; Type='type:test'; Prio='prio:P1'; Title='Completer tests non-regression auth et permissions'},

    # M2
    @{Epic='M2'; Domain='backend'; Type='type:feature'; Prio='prio:P1'; Title='Consolider coherences progression-combat-quetes'},
    @{Epic='M2'; Domain='frontend'; Type='type:feature'; Prio='prio:P2'; Title='Rendre lisibles les retours gameplay et etats joueur'},
    @{Epic='M2'; Domain='infra'; Type='type:chore'; Prio='prio:P2'; Title='Automatiser backup/restore des saves de test'},
    @{Epic='M2'; Domain='docs'; Type='type:docs'; Prio='prio:P2'; Title='Tracer regles de persistance et limites connues'},
    @{Epic='M2'; Domain='tests'; Type='type:test'; Prio='prio:P1'; Title='Ajouter tests de persistence multi-sessions'},

    # M3
    @{Epic='M3'; Domain='backend'; Type='type:chore'; Prio='prio:P2'; Title='Stabiliser contrats SSE utilises par l interface'},
    @{Epic='M3'; Domain='frontend'; Type='type:feature'; Prio='prio:P1'; Title='Refondre parcours chat/narration et gestion erreurs UI'},
    @{Epic='M3'; Domain='infra'; Type='type:chore'; Prio='prio:P3'; Title='Optimiser build frontend Docker pour boucle rapide'},
    @{Epic='M3'; Domain='docs'; Type='type:docs'; Prio='prio:P2'; Title='Documenter design decisions animation et UX'},
    @{Epic='M3'; Domain='tests'; Type='type:test'; Prio='prio:P1'; Title='Renforcer tests frontend des etats d interaction'},

    # M4
    @{Epic='M4'; Domain='backend'; Type='type:chore'; Prio='prio:P2'; Title='Verifier endpoints readiness/liveness pour exploitation'},
    @{Epic='M4'; Domain='frontend'; Type='type:chore'; Prio='prio:P3'; Title='Verifier configuration runtime API par environnement'},
    @{Epic='M4'; Domain='infra'; Type='type:chore'; Prio='prio:P1'; Title='Fiabiliser pipeline CI CD et strategie rollback'},
    @{Epic='M4'; Domain='docs'; Type='type:docs'; Prio='prio:P1'; Title='Formaliser runbook deploiement et restauration'},
    @{Epic='M4'; Domain='tests'; Type='type:test'; Prio='prio:P1'; Title='Automatiser smoke tests post-deploiement'},

    # M5
    @{Epic='M5'; Domain='backend'; Type='type:docs'; Prio='prio:P2'; Title='Lister preuves backend attendues pour soutenance'},
    @{Epic='M5'; Domain='frontend'; Type='type:docs'; Prio='prio:P2'; Title='Lister preuves frontend et parcours de demonstration'},
    @{Epic='M5'; Domain='infra'; Type='type:docs'; Prio='prio:P2'; Title='Lister preuves exploitation monitoring et deploiement'},
    @{Epic='M5'; Domain='docs'; Type='type:docs'; Prio='prio:P1'; Title='Verifier coherence transversale Bloc 1 3 4'},
    @{Epic='M5'; Domain='tests'; Type='type:docs'; Prio='prio:P2'; Title='Consolider synthese resultats tests reutilisable oral'}
)

$created = 0
$skipped = 0

foreach ($t in $tasks) {
    $epic = $epics[$t.Epic]
    $title = "[TASK][$($t.Epic)][$($t.Domain)] $($t.Title)"

    $exists = $allIssues | Where-Object { $_.title -eq $title } | Select-Object -First 1
    if ($exists) {
        Write-Host "[SKIP] Existe deja: $title"
        $skipped++
        continue
    }

    $body = @"
Parent EPIC: #$($epic.number)

Objectif
- $($t.Title)

Definition of done
- livrable verifiable
- labels et jalon renseignes
- preuves (tests/logs/captures) jointes si applicable
"@

    gh issue create --repo $repoSlug --title $title --body $body --milestone $milestones[$t.Epic] --label "$($t.Type),$($t.Prio),domain:$($t.Domain),status:ready" | Out-Null
    Write-Host "[OK] Cree: $title"
    $created++
}

Write-Host "Termine. Crees=$created, Skips=$skipped"
