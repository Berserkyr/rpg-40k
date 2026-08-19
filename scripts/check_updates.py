#!/usr/bin/env python3
"""Veille d'obsolescence des dépendances (compétence C4.1.1).

Recense les dépendances obsolètes des deux écosystèmes du projet et les classe
selon la politique de mise à jour définie dans
``docs/bloc4/01_processus_maj_dependances.md`` :

* MAJEURE  -> montée manuelle, évaluation d'impact obligatoire ;
* MINEURE / CORRECTIF -> intégration automatique après passage de la CI.

Utilisation :
    python scripts/check_updates.py            # rapport lisible
    python scripts/check_updates.py --json     # sortie machine (CI, ticket)

Code de sortie : 0 si aucune montée majeure n'est en attente, 1 sinon. Cela
permet de brancher le script sur une CI informative sans bloquer les
correctifs de routine.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = REPO_ROOT / "frontend"

MAJOR = "majeure"
MINOR = "mineure/correctif"


def _major_of(version: str) -> int | None:
    """Extrait le numéro de version majeure d'une chaîne ``x.y.z``."""
    head = version.strip().lstrip("^~=<>v ").split(".", 1)[0]
    try:
        return int(head)
    except ValueError:
        return None


def classify(current: str, latest: str) -> str:
    """Détermine si l'écart entre deux versions constitue une montée majeure."""
    cur, new = _major_of(current), _major_of(latest)
    if cur is None or new is None:
        return MINOR
    return MAJOR if new > cur else MINOR


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    """Exécute une commande et retourne (code de sortie, sortie standard)."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=180, shell=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, f"__ERROR__{exc}"
    return proc.returncode, proc.stdout


def check_python() -> list[dict]:
    """Liste les paquets Python obsolètes de l'environnement courant."""
    code, out = _run(
        [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"], REPO_ROOT
    )
    if out.startswith("__ERROR__") or not out.strip():
        return []
    try:
        packages = json.loads(out)
    except json.JSONDecodeError:
        return []
    return [
        {
            "ecosysteme": "python",
            "paquet": pkg["name"],
            "actuelle": pkg["version"],
            "disponible": pkg["latest_version"],
            "type": classify(pkg["version"], pkg["latest_version"]),
        }
        for pkg in packages
    ]


def check_npm() -> list[dict]:
    """Liste les paquets npm obsolètes du frontend."""
    npm = shutil.which("npm")
    if npm is None or not (FRONTEND_DIR / "package.json").exists():
        return []

    # `npm outdated` sort en code 1 quand il trouve des paquets obsolètes :
    # ce n'est pas une erreur, on exploite malgré tout la sortie JSON.
    _, out = _run([npm, "outdated", "--json"], FRONTEND_DIR)
    if out.startswith("__ERROR__") or not out.strip():
        return []
    try:
        packages = json.loads(out)
    except json.JSONDecodeError:
        return []

    results = []
    for name, info in packages.items():
        if not isinstance(info, dict):
            continue
        current = info.get("current") or info.get("wanted") or "?"
        latest = info.get("latest", "?")
        results.append(
            {
                "ecosysteme": "npm",
                "paquet": name,
                "actuelle": current,
                "disponible": latest,
                "type": classify(current, latest),
                "dev": info.get("type") == "devDependencies",
            }
        )
    return results


def render(findings: list[dict]) -> str:
    """Met en forme le rapport de veille."""
    if not findings:
        return "Aucune dépendance obsolète détectée. Rien à planifier cette semaine."

    majors = [f for f in findings if f["type"] == MAJOR]
    minors = [f for f in findings if f["type"] == MINOR]

    lines = ["VEILLE D'OBSOLESCENCE DES DEPENDANCES", "=" * 60, ""]

    def block(title: str, items: list[dict], note: str) -> None:
        lines.append(f"{title} ({len(items)})")
        lines.append("-" * 60)
        if not items:
            lines.append("  (aucune)")
        for item in items:
            flag = " [dev]" if item.get("dev") else ""
            lines.append(
                f"  {item['ecosysteme']:<7} {item['paquet']:<28}"
                f" {item['actuelle']:>12} -> {item['disponible']}{flag}"
            )
        lines.append(f"  => {note}")
        lines.append("")

    block(
        "MONTEES MAJEURES - traitement MANUEL",
        majors,
        "Ouvrir un ticket par montee, evaluer l'impact, brancher sur feature/.",
    )
    block(
        "MINEURES ET CORRECTIFS - traitement AUTOMATIQUE",
        minors,
        "Regrouper dans le lot mensuel, valider par la CI.",
    )

    lines.append(f"Total : {len(findings)} dependance(s) obsolete(s).")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="sortie JSON brute")
    args = parser.parse_args()

    findings = check_python() + check_npm()

    if args.json:
        print(json.dumps(findings, indent=2, ensure_ascii=False))
    else:
        print(render(findings))

    return 1 if any(f["type"] == MAJOR for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
