"""Supervision applicative : sondes, métriques et journalisation (C4.1.2).

Ce module centralise l'instrumentation du backend. Il expose :

* un **registre Prometheus** et les sondes métier propres au jeu ;
* un **middleware HTTP** mesurant trafic, latence et taux d'erreur ;
* des **sondes de disponibilité** (`liveness` / `readiness`) qui vérifient
  réellement les dépendances au lieu de renvoyer un statut figé ;
* une **journalisation structurée** exploitable par un agrégateur de logs.

Choix de conception
-------------------
Les métriques ne sont pas génériques : elles ciblent les modes de défaillance
propres à ce logiciel — dépendance à un LLM externe pouvant basculer
silencieusement en mode dégradé, sessions conservées en mémoire, contexte de
conversation croissant, et flux SSE de longue durée.
"""
from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    Info,
    generate_latest,
)

# ---------------------------------------------------------------------------
# Registre dédié
# ---------------------------------------------------------------------------
# Un registre explicite (plutôt que le registre global) évite les collisions
# lors des tests, où l'application peut être instanciée plusieurs fois.
REGISTRY = CollectorRegistry()

BUILD_INFO = Info("rpg40k_build", "Informations de version du service", registry=REGISTRY)

# ---------------------------------------------------------------------------
# Sondes techniques : trafic, latence, erreurs
# ---------------------------------------------------------------------------
HTTP_REQUESTS = Counter(
    "rpg40k_http_requests_total",
    "Nombre total de requêtes HTTP traitées.",
    ["method", "endpoint", "status_class"],
    registry=REGISTRY,
)

HTTP_DURATION = Histogram(
    "rpg40k_http_request_duration_seconds",
    "Durée de traitement des requêtes HTTP.",
    ["method", "endpoint"],
    # Paliers resserrés sous la seconde : hors streaming, l'API doit répondre
    # en quelques dizaines de millisecondes (calculs de jeu en mémoire).
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=REGISTRY,
)

HTTP_EXCEPTIONS = Counter(
    "rpg40k_http_exceptions_total",
    "Exceptions non gérées remontées par le middleware.",
    ["endpoint", "exception"],
    registry=REGISTRY,
)

# ---------------------------------------------------------------------------
# Sondes de dépendance externe : le maître du jeu (LLM)
# ---------------------------------------------------------------------------
# Sonde la plus critique du dispositif. L'application est conçue pour basculer
# automatiquement sur un narrateur local quand l'API OpenAI est indisponible :
# le service reste debout, mais l'expérience est dégradée sans aucun signal
# visible côté exploitant. Cette sonde rend la dégradation observable.
GM_GENERATIONS = Counter(
    "rpg40k_gm_generations_total",
    "Générations de narration, par mode de production.",
    ["mode"],  # openai | local_fallback | local_no_key
    registry=REGISTRY,
)

GM_DURATION = Histogram(
    "rpg40k_gm_generation_duration_seconds",
    "Durée complète d'une génération de narration.",
    ["mode"],
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 60.0),
    registry=REGISTRY,
)

GM_ERRORS = Counter(
    "rpg40k_gm_errors_total",
    "Échecs d'appel au fournisseur LLM, par type d'erreur.",
    ["reason"],
    registry=REGISTRY,
)

# Sondes issues du traitement de l'anomalie ANO-2026-001 : le texte produit
# par le LLM peut contenir des marqueurs d'etat mal formes. Ces sondes rendent
# le phenomene mesurable au lieu de le laisser silencieux.
STATE_MARKERS_REJECTED = Counter(
    "rpg40k_state_markers_rejected_total",
    "Marqueurs [ETAT: ...] ignores car inexploitables.",
    registry=REGISTRY,
)

STATE_PARSE_FAILURES = Counter(
    "rpg40k_state_parse_failures_total",
    "Echecs inattendus lors de l'application des marqueurs d'etat.",
    ["reason"],
    registry=REGISTRY,
)

GM_CONTEXT_MESSAGES = Histogram(
    "rpg40k_gm_context_messages",
    "Taille du contexte de conversation envoyé au LLM (nombre de messages).",
    # L'historique n'est jamais tronqué : cette sonde surveille sa croissance,
    # qui pèse directement sur le coût et sur la latence.
    buckets=(5, 10, 25, 50, 100, 200, 400, 800),
    registry=REGISTRY,
)

# ---------------------------------------------------------------------------
# Sondes de sécurité
# ---------------------------------------------------------------------------
AUTH_ATTEMPTS = Counter(
    "rpg40k_auth_attempts_total",
    "Tentatives d'authentification, par type et résultat.",
    ["action", "result"],  # action: login|register — result: success|failure
    registry=REGISTRY,
)

# ---------------------------------------------------------------------------
# Sondes métier et de capacité
# ---------------------------------------------------------------------------
ACTIVE_SESSIONS = Gauge(
    "rpg40k_active_sessions",
    "Sessions de jeu conservées en mémoire par le processus.",
    registry=REGISTRY,
)

SSE_STREAMS_ACTIVE = Gauge(
    "rpg40k_sse_streams_active",
    "Flux SSE de narration actuellement ouverts.",
    registry=REGISTRY,
)

COMBATS_STARTED = Counter(
    "rpg40k_combats_started_total",
    "Combats engagés, par faction adverse.",
    ["faction"],
    registry=REGISTRY,
)

SAVE_DURATION = Histogram(
    "rpg40k_save_duration_seconds",
    "Durée d'écriture d'une sauvegarde de partie sur disque.",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
    registry=REGISTRY,
)

SAVE_FAILURES = Counter(
    "rpg40k_save_failures_total",
    "Échecs d'écriture de sauvegarde.",
    registry=REGISTRY,
)

# ---------------------------------------------------------------------------
# Sondes de disponibilité des dépendances
# ---------------------------------------------------------------------------
DEPENDENCY_UP = Gauge(
    "rpg40k_dependency_up",
    "État des dépendances internes (1 = disponible, 0 = indisponible).",
    ["dependency"],  # database | character_sheet | prompt_file | save_dir
    registry=REGISTRY,
)

READINESS = Gauge(
    "rpg40k_ready",
    "Aptitude du service à traiter le trafic (1 = prêt, 0 = non prêt).",
    registry=REGISTRY,
)


# ---------------------------------------------------------------------------
# Journalisation structurée
# ---------------------------------------------------------------------------
def configure_logging(level: str | None = None) -> logging.Logger:
    """Configure une journalisation lisible par un agrégateur de logs.

    Le niveau est piloté par la variable d'environnement ``LOG_LEVEL`` afin de
    pouvoir passer en DEBUG sur incident sans modifier le code.
    """
    resolved = (level or os.getenv("LOG_LEVEL", "INFO")).upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt='ts=%(asctime)s level=%(levelname)s logger=%(name)s msg="%(message)s"',
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )
    root = logging.getLogger()
    # Évite l'empilement de handlers si la fonction est appelée plusieurs fois
    # (rechargement uvicorn, instanciations successives en test).
    for existing in list(root.handlers):
        root.removeHandler(existing)
    root.addHandler(handler)
    root.setLevel(getattr(logging, resolved, logging.INFO))
    return logging.getLogger("rpg40k")


logger = logging.getLogger("rpg40k")


# ---------------------------------------------------------------------------
# Normalisation des libellés
# ---------------------------------------------------------------------------
def normalize_endpoint(raw_path: str) -> str:
    """Réduit un chemin concret à son gabarit de route.

    Sans cette normalisation, un chemin porteur d'identifiant (par exemple
    ``/api/animations/tir_bolter``) créerait une série temporelle distincte par
    valeur, provoquant une explosion de cardinalité côté Prometheus.
    """
    path = (raw_path or "/").split("?", 1)[0].rstrip("/") or "/"
    segments = path.strip("/").split("/")
    if len(segments) >= 3 and segments[0] == "api" and segments[1] == "animations":
        return "/api/animations/{skill_id}"
    return path


def _status_class(status_code: int) -> str:
    """Regroupe les codes HTTP par famille (2xx, 4xx, 5xx)."""
    return f"{status_code // 100}xx"


# ---------------------------------------------------------------------------
# Sondes de disponibilité
# ---------------------------------------------------------------------------
def probe_dependencies(
    database_path: Path,
    character_file: Path,
    prompt_file: Path,
    save_dir: Path,
) -> dict[str, Any]:
    """Vérifie activement les dépendances nécessaires au service.

    Contrairement à une sonde de vivacité — qui atteste seulement que le
    processus répond — cette sonde effectue une lecture réelle de la base et un
    contrôle d'accès aux fichiers indispensables au démarrage d'une partie.
    """
    import sqlite3

    checks: dict[str, dict[str, Any]] = {}

    # Base de données : requête réelle, et non simple test d'existence.
    try:
        connection = sqlite3.connect(database_path, timeout=3)
        try:
            connection.execute("SELECT count(*) FROM users").fetchone()
        finally:
            connection.close()
        checks["database"] = {"ok": True}
    except Exception as exc:  # sqlite3.Error, OSError...
        checks["database"] = {"ok": False, "detail": type(exc).__name__}

    # Fichiers indispensables au démarrage d'une partie.
    for name, path in (
        ("character_sheet", character_file),
        ("prompt_file", prompt_file),
    ):
        try:
            ok = path.is_file() and path.stat().st_size > 0
            checks[name] = {"ok": ok} if ok else {"ok": False, "detail": "absent ou vide"}
        except OSError as exc:
            checks[name] = {"ok": False, "detail": type(exc).__name__}

    # Répertoire de sauvegarde : accessible en écriture.
    try:
        save_dir.mkdir(parents=True, exist_ok=True)
        probe_file = save_dir / ".healthcheck"
        probe_file.write_text("ok", encoding="utf-8")
        probe_file.unlink(missing_ok=True)
        checks["save_dir"] = {"ok": True}
    except OSError as exc:
        checks["save_dir"] = {"ok": False, "detail": type(exc).__name__}

    for dependency, result in checks.items():
        DEPENDENCY_UP.labels(dependency=dependency).set(1 if result["ok"] else 0)

    ready = all(result["ok"] for result in checks.values())
    READINESS.set(1 if ready else 0)

    return {"ready": ready, "checks": checks}


def render_metrics() -> tuple[bytes, str]:
    """Sérialise le registre au format d'exposition Prometheus."""
    return generate_latest(REGISTRY), CONTENT_TYPE_LATEST


# ---------------------------------------------------------------------------
# Middleware HTTP
# ---------------------------------------------------------------------------
async def metrics_middleware(request, call_next: Callable):
    """Mesure trafic, latence et erreurs de chaque requête HTTP."""
    endpoint = normalize_endpoint(request.url.path)

    # Le point de collecte ne s'observe pas lui-même : il fausserait le trafic.
    if endpoint == "/api/metrics":
        return await call_next(request)

    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        HTTP_EXCEPTIONS.labels(endpoint=endpoint, exception=type(exc).__name__).inc()
        HTTP_REQUESTS.labels(
            method=request.method, endpoint=endpoint, status_class="5xx"
        ).inc()
        HTTP_DURATION.labels(method=request.method, endpoint=endpoint).observe(
            time.perf_counter() - started
        )
        logger.exception("Exception non gérée sur %s", endpoint)
        raise

    elapsed = time.perf_counter() - started
    HTTP_REQUESTS.labels(
        method=request.method,
        endpoint=endpoint,
        status_class=_status_class(response.status_code),
    ).inc()
    HTTP_DURATION.labels(method=request.method, endpoint=endpoint).observe(elapsed)

    # Trace exploitable pour le diagnostic des lenteurs.
    if elapsed > 1.0 and endpoint not in ("/api/start", "/api/chat"):
        logger.warning(
            "Requête lente endpoint=%s methode=%s duree=%.3fs status=%s",
            endpoint, request.method, elapsed, response.status_code,
        )

    return response
