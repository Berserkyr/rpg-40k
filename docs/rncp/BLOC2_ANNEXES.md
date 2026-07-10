# Annexes — Bloc 2

Ces annexes complètent le dossier Bloc 2. Elles ne sont pas destinées à être comptées dans la limite des 30 pages du dossier principal.

## Annexe A — Cartographie des preuves

| Attendu Bloc 2 | Preuve projet |
|---|---|
| Code source | Dépôt GitHub `https://github.com/Berserkyr/rpg-40k` |
| Version stable | Tag `v1.0.0-rncp` |
| Environnement de développement | `README.md`, `requirements.txt`, `frontend/package.json` |
| Intégration continue | `.github/workflows/ci.yml`, `.gitlab-ci.yml` |
| Déploiement manuel VPS | `.github/workflows/deploy-vps.yml`, `docs/deploiement_vps.md` |
| Architecture logicielle | `docs/rncp/BLOC2_DOSSIER_FINAL.md`, `docs/architecture_bdd_multiutilisateur.md` |
| Tests backend | `tests/` |
| Tests frontend | `frontend/src/**/__tests__` |
| Tests E2E | `frontend/e2e/game.spec.js` |
| Recette | `docs/rncp/05_plan_de_recette.md` |
| Exploitation | `docs/deploiement_vps.md` |

## Annexe B — Commandes de validation

### Backend

```powershell
python -m pytest
```

Résultat attendu : tous les tests backend passent.

### Frontend unitaires

```powershell
cd frontend
npm test
```

Résultat attendu : tests Vitest / React Testing Library OK.

### Build frontend

```powershell
cd frontend
npm run build
```

Résultat attendu : génération du dossier `dist`.

### End-to-end

```powershell
cd frontend
npm run e2e
```

Résultat attendu : parcours navigateur validé.

### Docker Compose

```bash
docker compose config --quiet
docker compose -p rpg40k ps
```

Résultat attendu : configuration valide et conteneurs actifs.

## Annexe C — URLs utiles

| Élément | URL |
|---|---|
| Dépôt GitHub | `https://github.com/Berserkyr/rpg-40k` |
| Application VPS | `http://89.116.111.166:8081/` |
| Healthcheck VPS | `http://89.116.111.166:8081/api/health` |

## Annexe D — Captures recommandées à insérer dans le PDF final

Prévoir les captures suivantes :

1. page d’accueil de l’application ;
2. écran après initialisation d’une partie ;
3. résultat d’un jet `2D6` ;
4. panneau combat actif ;
5. GitHub Actions en succès ;
6. terminal avec `pytest` en succès ;
7. terminal avec `npm test` en succès ;
8. terminal avec `docker compose -p rpg40k ps` ;
9. réponse `/api/health` ;
10. tag Git `v1.0.0-rncp` visible sur GitHub.

## Annexe E — Glossaire

| Terme | Définition |
|---|---|
| API | Interface permettant au frontend de communiquer avec le backend |
| CI | Intégration continue : tests automatisés à chaque modification |
| CD | Déploiement continu ou semi-continu |
| E2E | Test end-to-end simulant un parcours utilisateur complet |
| RGAA | Référentiel Général d’Amélioration de l’Accessibilité |
| OWASP | Référentiel des risques de sécurité applicative |
| SSE | Server-Sent Events, flux texte serveur vers navigateur |
| VPS | Serveur privé virtuel |
