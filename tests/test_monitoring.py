"""Tests du dispositif de supervision (C4.1.2).

Vérifient que les sondes existent, qu'elles s'incrémentent réellement sur les
parcours instrumentés, et que la sonde d'aptitude détecte une dépendance en
panne au lieu de renvoyer un statut figé.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import monitoring
from backend.api import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def _metric_value(payload: str, metric: str, **labels: str) -> float:
    """Extrait la valeur d'une série dans une exposition Prometheus.

    Les libellés sont triés par ordre alphabétique : c'est l'ordre utilisé par
    ``prometheus_client`` dans le format d'exposition, indépendamment de l'ordre
    de déclaration de la métrique.
    """
    if labels:
        rendered = ",".join(f'{k}="{labels[k]}"' for k in sorted(labels))
        needle = f"{metric}{{{rendered}}}"
    else:
        needle = metric
    for line in payload.splitlines():
        if line.startswith("#"):
            continue
        name, _, value = line.rpartition(" ")
        if name.strip() == needle:
            return float(value)
    return 0.0


# ---------------------------------------------------------------------------
# Normalisation des libellés
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "raw, attendu",
    [
        ("/api/health", "/api/health"),
        ("/api/health/", "/api/health"),
        ("/api/state?x=1", "/api/state"),
        # Les identifiants variables sont ramenés au gabarit de route pour
        # éviter l'explosion de cardinalité côté Prometheus.
        ("/api/animations/tir_bolter", "/api/animations/{skill_id}"),
        ("/api/animations/coup_de_grace", "/api/animations/{skill_id}"),
    ],
)
def test_normalisation_des_endpoints(raw: str, attendu: str) -> None:
    assert monitoring.normalize_endpoint(raw) == attendu


def test_normalisation_borne_la_cardinalite() -> None:
    """Cent identifiants distincts ne doivent produire qu'un seul libellé."""
    libelles = {monitoring.normalize_endpoint(f"/api/animations/skill_{i}") for i in range(100)}
    assert libelles == {"/api/animations/{skill_id}"}


# ---------------------------------------------------------------------------
# Point de collecte
# ---------------------------------------------------------------------------
def test_endpoint_metrics_expose_le_format_prometheus(client: TestClient) -> None:
    response = client.get("/api/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "rpg40k_http_requests_total" in response.text


def test_metriques_essentielles_declarees(client: TestClient) -> None:
    """Les sondes couvrant chaque famille de risque doivent être exposées."""
    payload = client.get("/api/metrics").text
    for metric in (
        "rpg40k_http_requests_total",
        "rpg40k_http_request_duration_seconds",
        "rpg40k_gm_generations_total",
        "rpg40k_auth_attempts_total",
        "rpg40k_active_sessions",
        "rpg40k_dependency_up",
        "rpg40k_ready",
    ):
        assert metric in payload, f"sonde manquante : {metric}"


def test_le_point_de_collecte_ne_s_observe_pas_lui_meme(client: TestClient) -> None:
    """Compter /api/metrics fausserait le trafic mesuré."""
    client.get("/api/metrics")
    payload = client.get("/api/metrics").text
    assert '/api/metrics' not in payload.split("rpg40k_http_requests_total")[-1][:2000]


# ---------------------------------------------------------------------------
# Middleware HTTP
# ---------------------------------------------------------------------------
def test_le_middleware_compte_les_requetes(client: TestClient) -> None:
    avant = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_http_requests_total",
        method="GET", endpoint="/api/health", status_class="2xx",
    )
    client.get("/api/health")
    apres = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_http_requests_total",
        method="GET", endpoint="/api/health", status_class="2xx",
    )
    assert apres == avant + 1


def test_le_middleware_distingue_les_familles_de_codes(client: TestClient) -> None:
    """Une requête non authentifiée doit être comptée en 4xx, pas en 2xx."""
    avant = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_http_requests_total",
        method="GET", endpoint="/api/state", status_class="4xx",
    )
    assert client.get("/api/state").status_code == 401
    apres = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_http_requests_total",
        method="GET", endpoint="/api/state", status_class="4xx",
    )
    assert apres == avant + 1


def test_la_latence_est_mesuree(client: TestClient) -> None:
    client.get("/api/health")
    payload = client.get("/api/metrics").text
    assert "rpg40k_http_request_duration_seconds_bucket" in payload
    assert 'endpoint="/api/health"' in payload


# ---------------------------------------------------------------------------
# Sondes de sécurité
# ---------------------------------------------------------------------------
def test_les_echecs_d_authentification_sont_comptes(client: TestClient) -> None:
    avant = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_auth_attempts_total", action="login", result="failure",
    )
    client.post(
        "/api/auth/login",
        json={"username": "inconnu-supervision", "password": "mauvais-mot-de-passe"},
    )
    apres = _metric_value(
        client.get("/api/metrics").text,
        "rpg40k_auth_attempts_total", action="login", result="failure",
    )
    assert apres == avant + 1, "l'echec d'authentification doit alimenter la sonde de securite"


# ---------------------------------------------------------------------------
# Sondes de disponibilité
# ---------------------------------------------------------------------------
def test_sonde_de_vivacite(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_sonde_d_aptitude_nominale(client: TestClient) -> None:
    response = client.get("/api/health/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    for dependance in ("database", "character_sheet", "prompt_file", "save_dir"):
        assert body["checks"][dependance]["ok"] is True


def test_sonde_d_aptitude_detecte_une_base_illisible(tmp_path: Path) -> None:
    """Une base corrompue doit faire échouer la sonde d'aptitude.

    C'est précisément le cas que l'ancienne sonde statique laissait passer :
    elle renvoyait « ok » sans jamais interroger la base.
    """
    base_corrompue = tmp_path / "corrompue.sqlite3"
    base_corrompue.write_bytes(b"ceci n'est pas une base sqlite")

    resultat = monitoring.probe_dependencies(
        database_path=base_corrompue,
        character_file=Path("character_sheet.yaml"),
        prompt_file=Path("prompt_survivant.md"),
        save_dir=tmp_path / "saves",
    )

    assert resultat["ready"] is False
    assert resultat["checks"]["database"]["ok"] is False


def test_sonde_d_aptitude_detecte_un_fichier_de_jeu_absent(tmp_path: Path) -> None:
    base = tmp_path / "vide.sqlite3"
    connexion = sqlite3.connect(base)
    connexion.execute("CREATE TABLE users (id TEXT)")
    connexion.close()

    resultat = monitoring.probe_dependencies(
        database_path=base,
        character_file=tmp_path / "fiche-absente.yaml",
        prompt_file=Path("prompt_survivant.md"),
        save_dir=tmp_path / "saves",
    )

    assert resultat["ready"] is False
    assert resultat["checks"]["character_sheet"]["ok"] is False
    assert resultat["checks"]["database"]["ok"] is True


def test_la_sonde_d_aptitude_met_a_jour_les_jauges(client: TestClient) -> None:
    client.get("/api/health/ready")
    payload = client.get("/api/metrics").text
    assert _metric_value(payload, "rpg40k_ready") == 1.0
    assert _metric_value(payload, "rpg40k_dependency_up", dependency="database") == 1.0


# ---------------------------------------------------------------------------
# Classification des générations de narration
# ---------------------------------------------------------------------------
def test_la_sonde_de_narration_distingue_les_modes(client: TestClient) -> None:
    """Les trois modes de production doivent être des séries distinctes."""
    monitoring.GM_GENERATIONS.labels(mode="openai").inc(0)
    monitoring.GM_GENERATIONS.labels(mode="local_fallback").inc(0)
    monitoring.GM_GENERATIONS.labels(mode="local_no_key").inc(0)
    payload = client.get("/api/metrics").text
    assert 'mode="openai"' in payload
    assert 'mode="local_fallback"' in payload
    assert 'mode="local_no_key"' in payload


def test_configuration_du_journal_sans_empilement() -> None:
    """Des appels répétés ne doivent pas dupliquer les gestionnaires de journal."""
    import logging

    monitoring.configure_logging("INFO")
    premier = len(logging.getLogger().handlers)
    monitoring.configure_logging("INFO")
    assert len(logging.getLogger().handlers) == premier
