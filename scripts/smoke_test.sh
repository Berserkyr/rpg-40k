#!/usr/bin/env bash
# Test de fumée post-déploiement (C4.2.2).
#
# Vérifie qu'une version fraîchement déployée est réellement opérationnelle,
# et non seulement "démarrée". Un conteneur qui répond n'est pas un service qui
# fonctionne : ce script contrôle les dépendances, l'exposition des sondes et
# l'application effective de l'authentification.
#
# Code de sortie 0 = déploiement validé, non nul = rollback à déclencher.
#
# Usage : ./scripts/smoke_test.sh [URL_DE_BASE] [TENTATIVES]
set -uo pipefail

BASE_URL="${1:-http://127.0.0.1:8081}"
MAX_TENTATIVES="${2:-30}"
ECHECS=0

vert()  { printf '  [OK]    %s\n' "$1"; }
rouge() { printf '  [ECHEC] %s\n' "$1"; ECHECS=$((ECHECS + 1)); }

echo "Test de fumee sur ${BASE_URL}"
echo "------------------------------------------------------------"

# --- 1. Attente du démarrage -------------------------------------------------
# Le build des images puis le démarrage d'Uvicorn prennent quelques secondes :
# on laisse au service le temps de répondre avant de conclure à une panne.
echo "1. Attente de la disponibilite"
DISPONIBLE=0
for tentative in $(seq 1 "${MAX_TENTATIVES}"); do
  if curl -fsS --max-time 5 "${BASE_URL}/api/health" >/dev/null 2>&1; then
    vert "service joignable apres ${tentative} tentative(s)"
    DISPONIBLE=1
    break
  fi
  sleep 2
done

if [ "${DISPONIBLE}" -eq 0 ]; then
  rouge "service injoignable apres ${MAX_TENTATIVES} tentatives"
  echo "------------------------------------------------------------"
  echo "RESULTAT : ECHEC (service indisponible)"
  exit 1
fi

# --- 2. Sonde d'aptitude -----------------------------------------------------
# Contrairement à la sonde de vivacité, elle interroge réellement la base et le
# système de fichiers. C'est le contrôle qui distingue un service démarré d'un
# service opérationnel.
echo "2. Sonde d'aptitude (dependances)"
REPONSE_READY=$(curl -fsS --max-time 10 "${BASE_URL}/api/health/ready" 2>/dev/null || echo '{}')
if echo "${REPONSE_READY}" | grep -q '"status"[[:space:]]*:[[:space:]]*"ready"'; then
  vert "toutes les dependances sont disponibles"
else
  rouge "service non apte au trafic : ${REPONSE_READY}"
fi

# --- 3. Exposition des sondes de supervision --------------------------------
echo "3. Point de collecte des metriques"
if curl -fsS --max-time 10 "${BASE_URL}/api/metrics" 2>/dev/null | grep -q 'rpg40k_http_requests_total'; then
  vert "metriques exposees"
else
  rouge "metriques absentes : la supervision serait aveugle sur cette version"
fi

# --- 4. Application effective de l'authentification -------------------------
# Une régression de configuration pourrait exposer les routes de jeu sans
# jeton. Le test vérifie que l'accès non authentifié est bien refusé.
echo "4. Protection des routes de jeu"
CODE_SANS_JETON=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "${BASE_URL}/api/state" 2>/dev/null || echo "000")
if [ "${CODE_SANS_JETON}" = "401" ]; then
  vert "acces non authentifie refuse (401)"
else
  rouge "acces non authentifie renvoie ${CODE_SANS_JETON} au lieu de 401"
fi

# --- 5. Service du frontend --------------------------------------------------
echo "5. Livraison de l'interface"
if curl -fsS --max-time 10 "${BASE_URL}/" 2>/dev/null | grep -qi '<div id="root"'; then
  vert "page applicative servie"
else
  rouge "interface non servie par le reverse proxy"
fi

echo "------------------------------------------------------------"
if [ "${ECHECS}" -eq 0 ]; then
  echo "RESULTAT : SUCCES — deploiement valide"
  exit 0
fi
echo "RESULTAT : ECHEC — ${ECHECS} controle(s) en echec, rollback requis"
exit 1
