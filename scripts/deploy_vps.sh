#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/rpg-40k}"
REPO_URL="${REPO_URL:-https://github.com/Berserkyr/rpg-40k.git}"
BRANCH="${BRANCH:-main}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker n'est pas installé. Installe Docker avant de continuer." >&2
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 n'est pas disponible. Installe le plugin docker compose." >&2
  exit 1
fi

sudo mkdir -p "$APP_DIR"
sudo chown "$USER":"$USER" "$APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  git -C "$APP_DIR" fetch origin "$BRANCH"
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
fi

cd "$APP_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Fichier .env créé depuis .env.example. Renseigne OPENAI_API_KEY si nécessaire."
fi

docker compose -p rpg40k pull || true
docker compose -p rpg40k up -d --build

echo "Déploiement terminé. Vérification :"
docker compose -p rpg40k ps
