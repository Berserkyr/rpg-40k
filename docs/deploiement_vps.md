# Déploiement sur VPS

Ce guide décrit un déploiement simple sur un VPS Linux avec Docker Compose.

## Architecture cible

```text
Internet
   |
   v
VPS:80
   |
   v
frontend Nginx React
   |
   +-- /api/* --> backend FastAPI:8000

Volumes Docker persistants :
- rpg40k_data  : base SQLite `rpg40k.sqlite3`
- rpg40k_saves : sauvegardes YAML par utilisateur
```

## Fichiers ajoutés

| Fichier | Rôle |
|---|---|
| [Dockerfile.backend](../Dockerfile.backend) | Image backend FastAPI |
| [frontend/Dockerfile](../frontend/Dockerfile) | Build React + Nginx |
| [frontend/nginx.conf](../frontend/nginx.conf) | Reverse proxy `/api` vers le backend |
| [docker-compose.yml](../docker-compose.yml) | Orchestration VPS |
| [.dockerignore](../.dockerignore) | Exclusion secrets/caches |
| [.env.example](../.env.example) | Variables d’environnement |
| [scripts/deploy_vps.sh](../scripts/deploy_vps.sh) | Script de déploiement Ubuntu |
| [scripts/backup_vps.sh](../scripts/backup_vps.sh) | Sauvegarde des volumes Docker |

## Prérequis VPS

- Ubuntu 22.04 ou 24.04 recommandé.
- Accès SSH avec un utilisateur sudo.
- Git installé.
- Docker + Docker Compose v2 installés.
- Ports ouverts : `22`, `80` et, si HTTPS ajouté ensuite, `443`.

## Installation de Docker sur Ubuntu

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc >/dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

Déconnecte-toi puis reconnecte-toi en SSH pour activer le groupe `docker`.

## Premier déploiement

```bash
export APP_DIR=/opt/rpg-40k
export REPO_URL=https://github.com/Berserkyr/rpg-40k.git
export BRANCH=main
curl -fsSL https://raw.githubusercontent.com/Berserkyr/rpg-40k/main/scripts/deploy_vps.sh | bash
```

Puis édite le fichier `.env` sur le VPS :

```bash
cd /opt/rpg-40k
nano .env
```

Exemple minimal :

```env
OPENAI_API_KEY=
VITE_API_BASE=/api
DOMAIN=ton-domaine.fr
APP_DIR=/opt/rpg-40k
```

Relance ensuite :

```bash
docker compose up -d --build
```

## Vérification

```bash
docker compose ps
curl http://127.0.0.1/api/health
```

Depuis un navigateur :

```text
http://IP_DU_VPS/
```

## Mise à jour applicative

```bash
cd /opt/rpg-40k
git pull --ff-only origin main
docker compose up -d --build
```

## Logs

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

## Sauvegarde

```bash
cd /opt/rpg-40k
bash scripts/backup_vps.sh
```

Les archives sont créées dans `~/rpg-40k-backups` par défaut.

## HTTPS et nom de domaine

La configuration fournie expose l’application en HTTP sur le port `80`.

Pour une démonstration RNCP, c’est suffisant si le VPS est accessible par IP. Pour une mise en production publique, ajouter ensuite :

1. un nom de domaine pointant vers le VPS ;
2. un reverse proxy HTTPS avec Caddy, Traefik ou Nginx + Certbot ;
3. une restriction CORS côté backend.

## Commandes utiles

```bash
# Arrêter
cd /opt/rpg-40k
docker compose down

# Redémarrer
cd /opt/rpg-40k
docker compose restart

# Reconstruire complètement
cd /opt/rpg-40k
docker compose build --no-cache
docker compose up -d
```

## Points de preuve pour la soutenance

- Déploiement reproductible via `docker-compose.yml`.
- BDD persistée dans un volume Docker.
- Sauvegardes de parties persistées dans un volume Docker.
- Healthcheck backend disponible via `/api/health`.
- Reverse proxy frontend/API documenté.
- Script de sauvegarde exploitable.
