#!/usr/bin/env python3
"""Mesure des indicateurs de performance (C4.3.1).

Produit les relevés chiffrés servant de base aux recommandations
d'amélioration : latence des routes, poids des bundles livrés au navigateur,
croissance du contexte envoyé au LLM et volumétrie de la base.

L'objectif est de fonder les préconisations sur des mesures reproductibles
plutôt que sur une appréciation qualitative.

Usage :
    python scripts/benchmark.py
    python scripts/benchmark.py --json
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Le script est lance depuis scripts/ : la racine du depot doit etre importable.
sys.path.insert(0, str(REPO))

# Approximation usuelle pour du texte français en tokenisation BPE.
CARACTERES_PAR_TOKEN = 4.0
# Tarif public gpt-4o-mini au 19/08/2026, en dollars par million de tokens
# d'entrée. Sert d'ordre de grandeur, non de facturation exacte.
COUT_ENTREE_PAR_MTOKEN = 0.15


def _percentile(valeurs: list[float], centile: float) -> float:
    if not valeurs:
        return 0.0
    ordonnees = sorted(valeurs)
    rang = min(int(len(ordonnees) * centile), len(ordonnees) - 1)
    return ordonnees[rang]


# ---------------------------------------------------------------------------
# 1. Latence des routes
# ---------------------------------------------------------------------------
def mesurer_latence_api(iterations: int = 60) -> dict:
    """Mesure la latence des routes en sollicitant l'application en direct."""
    from fastapi.testclient import TestClient
    import backend.api as api

    client = TestClient(api.app)
    identifiants = {"username": "benchmark-perf", "password": "motdepasse1"}
    client.post("/api/auth/register", json=identifiants)
    jeton = client.post("/api/auth/login", json=identifiants).json()["access_token"]
    entetes = {"Authorization": f"Bearer {jeton}"}

    scenarios = {
        "GET /api/health": lambda: client.get("/api/health"),
        "GET /api/health/ready": lambda: client.get("/api/health/ready"),
        "POST /api/roll": lambda: client.post("/api/roll", headers=entetes),
        "GET /api/state": lambda: client.get("/api/state", headers=entetes),
        "GET /api/metrics": lambda: client.get("/api/metrics"),
        "POST /api/auth/login": lambda: client.post("/api/auth/login", json=identifiants),
    }

    resultats = {}
    for nom, appel in scenarios.items():
        # Le login est volontairement lent (bcrypt) : on limite les iterations.
        n = 10 if "login" in nom else iterations
        appel()  # amorçage, hors mesure
        durees = []
        for _ in range(n):
            depart = time.perf_counter()
            appel()
            durees.append((time.perf_counter() - depart) * 1000)
        resultats[nom] = {
            "iterations": n,
            "p50_ms": round(statistics.median(durees), 2),
            "p95_ms": round(_percentile(durees, 0.95), 2),
            "max_ms": round(max(durees), 2),
        }
    return resultats


# ---------------------------------------------------------------------------
# 2. Poids livré au navigateur
# ---------------------------------------------------------------------------
def mesurer_bundles() -> dict:
    """Relève la taille des fichiers produits par le build de production."""
    dist = REPO / "frontend" / "dist" / "assets"
    if not dist.is_dir():
        return {"erreur": "dist absent — executer 'npm run build' au prealable"}

    fichiers = []
    for chemin in sorted(dist.glob("*")):
        if chemin.suffix in (".js", ".css"):
            fichiers.append({
                "fichier": chemin.name,
                "ko": round(chemin.stat().st_size / 1024, 1),
            })
    fichiers.sort(key=lambda f: f["ko"], reverse=True)
    total_js = sum(f["ko"] for f in fichiers if f["fichier"].endswith(".js"))
    return {
        "fichiers": fichiers[:8],
        "total_js_ko": round(total_js, 1),
        "total_ko": round(sum(f["ko"] for f in fichiers), 1),
    }


# ---------------------------------------------------------------------------
# 3. Croissance du contexte LLM
# ---------------------------------------------------------------------------
def mesurer_contexte_llm(scenes: int = 30) -> dict:
    """Projette le coût d'une partie, l'historique n'étant jamais tronqué."""
    from src.state import CharacterState
    from src.prompt_builder import build_system_prompt

    personnage = CharacterState.from_file(REPO / "character_sheet.yaml")
    prompt_systeme = build_system_prompt(REPO / "prompt_survivant.md", personnage)
    base = len(prompt_systeme)

    # Ordres de grandeur releves sur les narrations produites par l'application.
    taille_message_joueur = 60
    taille_reponse_mj = 900

    cumul_caracteres = 0
    total_envoye = 0
    projection = []
    for scene in range(1, scenes + 1):
        cumul_caracteres += taille_message_joueur + taille_reponse_mj
        contexte = base + cumul_caracteres
        total_envoye += contexte
        if scene in (1, 5, 10, 20, 30):
            projection.append({
                "scene": scene,
                "contexte_tokens": int(contexte / CARACTERES_PAR_TOKEN),
                "cumul_envoye_tokens": int(total_envoye / CARACTERES_PAR_TOKEN),
            })

    tokens_total = total_envoye / CARACTERES_PAR_TOKEN
    tokens_si_fenetre = (base + (taille_message_joueur + taille_reponse_mj) * 10) / CARACTERES_PAR_TOKEN * scenes

    return {
        "prompt_systeme_tokens": int(base / CARACTERES_PAR_TOKEN),
        "projection": projection,
        "cout_partie_usd": round(tokens_total / 1_000_000 * COUT_ENTREE_PAR_MTOKEN, 4),
        "cout_avec_fenetre_glissante_usd": round(
            tokens_si_fenetre / 1_000_000 * COUT_ENTREE_PAR_MTOKEN, 4
        ),
    }


# ---------------------------------------------------------------------------
# 4. Volumétrie de la base
# ---------------------------------------------------------------------------
def mesurer_base() -> dict:
    """Relève la volumétrie et l'indexation de la base SQLite."""
    import sqlite3

    chemin = REPO / "data" / "rpg40k.sqlite3"
    if not chemin.exists():
        return {"erreur": "base absente"}

    connexion = sqlite3.connect(chemin)
    try:
        tables = {}
        for table in ("users", "session_events"):
            tables[table] = connexion.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        index = [
            r[0] for r in connexion.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL"
            )
        ]
    finally:
        connexion.close()

    return {
        "taille_ko": round(chemin.stat().st_size / 1024, 1),
        "lignes": tables,
        "index_explicites": index or ["aucun"],
    }


# ---------------------------------------------------------------------------
# 5. Temps de démarrage
# ---------------------------------------------------------------------------
def mesurer_demarrage() -> dict:
    """Mesure le coût d'import de l'application (démarrage à froid)."""
    import subprocess
    import sys

    depart = time.perf_counter()
    subprocess.run(
        [sys.executable, "-c", "import backend.api"],
        cwd=REPO, capture_output=True, timeout=120,
    )
    return {"import_backend_s": round(time.perf_counter() - depart, 2)}


def rendre(mesures: dict) -> str:
    lignes = ["INDICATEURS DE PERFORMANCE", "=" * 64, ""]

    lignes.append("1. LATENCE DES ROUTES (ms)")
    lignes.append(f"   {'route':<26} {'p50':>8} {'p95':>8} {'max':>8}")
    for route, m in mesures["latence"].items():
        lignes.append(f"   {route:<26} {m['p50_ms']:>8} {m['p95_ms']:>8} {m['max_ms']:>8}")

    lignes.append("")
    lignes.append("2. POIDS LIVRE AU NAVIGATEUR")
    bundles = mesures["bundles"]
    if "erreur" in bundles:
        lignes.append(f"   {bundles['erreur']}")
    else:
        for f in bundles["fichiers"]:
            lignes.append(f"   {f['fichier']:<40} {f['ko']:>9} Ko")
        lignes.append(f"   {'TOTAL JS':<40} {bundles['total_js_ko']:>9} Ko")

    lignes.append("")
    lignes.append("3. CROISSANCE DU CONTEXTE LLM (historique non tronque)")
    ctx = mesures["contexte_llm"]
    lignes.append(f"   prompt systeme : {ctx['prompt_systeme_tokens']} tokens")
    lignes.append(f"   {'scene':>8} {'contexte':>12} {'cumul envoye':>15}")
    for p in ctx["projection"]:
        lignes.append(f"   {p['scene']:>8} {p['contexte_tokens']:>12} {p['cumul_envoye_tokens']:>15}")
    lignes.append(f"   cout d'une partie de 30 scenes : ~{ctx['cout_partie_usd']} USD")
    lignes.append(f"   avec fenetre glissante (10)    : ~{ctx['cout_avec_fenetre_glissante_usd']} USD")

    lignes.append("")
    lignes.append("4. BASE DE DONNEES")
    bdd = mesures["base"]
    if "erreur" in bdd:
        lignes.append(f"   {bdd['erreur']}")
    else:
        lignes.append(f"   taille : {bdd['taille_ko']} Ko")
        for table, n in bdd["lignes"].items():
            lignes.append(f"   {table:<20} {n:>8} lignes")
        lignes.append(f"   index explicites : {', '.join(bdd['index_explicites'])}")

    lignes.append("")
    lignes.append("5. DEMARRAGE")
    lignes.append(f"   import du backend : {mesures['demarrage']['import_backend_s']} s")

    return "\n".join(lignes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    mesures = {
        "latence": mesurer_latence_api(),
        "bundles": mesurer_bundles(),
        "contexte_llm": mesurer_contexte_llm(),
        "base": mesurer_base(),
        "demarrage": mesurer_demarrage(),
    }

    if args.json:
        print(json.dumps(mesures, indent=2, ensure_ascii=False))
    else:
        print(rendre(mesures))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
