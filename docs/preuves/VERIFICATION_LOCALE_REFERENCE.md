# Vérification locale de référence — backend, frontend et build

**Contexte :** harmonisation documentaire des Blocs 1 et 3 ; code de référence `e116b88`, version déclarée 1.3.0, copie de travail non propre.  
**Date documentaire annoncée :** 20 septembre 2026. **Horloge du système d'exécution :** les traces backend portent le 21 septembre 2026, vers 11:17, fuseau +02:00. Cet écart est conservé plutôt que d'antidater les traces.  
**Nature :** compte rendu d'exécutions observées pendant cette session, avec extraits ; pas export intégral de journaux ni résultat d'une CI distante.

## 1. Conditions de vérification

- Windows, PowerShell, environnement Python virtuel du projet (3.13), Node 22.17.0, npm 10.9.2.
- Aucune modification du code métier, des tests ou des manifestes pour obtenir ces résultats.
- Une première tentative backend a échoué **avant les tests** : module `prometheus_client` absent. Installation de `prometheus-client 0.26.0` dans l'environnement virtuel, conformément à la contrainte déjà présente dans [requirements.txt](../../requirements.txt). Pas de changement de la contrainte.
- Pour ne pas utiliser les données des joueurs : processus Python dédié, `TemporaryDirectory`, redirection de `backend.database.DATA_DIR` et `DATABASE_PATH` avant import de l'API, puis `backend.api.SAVE_DIR` vers le répertoire temporaire. Appel de `pytest.main(['-q'])` dans ce processus.
- Clé OpenAI vide et secret JWT de test définis dans le processus, sans modifier la configuration privée du projet. Les réponses externes réelles et leur facturation ne sont pas validées.
- Frontend : exécution de `npm test`, puis `npm run build` depuis le dossier frontend avec les dépendances présentes. Aucun serveur public ni scénario navigateur Playwright lancé.

Ces conditions précisent ce qui a été exécuté ; elles ne démontrent pas qu'une installation neuve de toutes les dépendances est reproductible. Les tests temporaires ne remplacent pas un essai de restauration de données réelles.

## 2. Résultats effectivement observés

| Contrôle | Résultat | Code de sortie |
|---|---|---:|
| Backend après installation de la dépendance manquante | **138 passed, 1 warning in 12.80s** | 0 |
| Frontend Vitest 4.1.10 | **6 fichiers réussis, 30 tests réussis**, 27,88 s | 0 |
| Frontend Vite 8.0.14 | **62 modules transformés ; built in 1.14s** | 0 |

### Avertissements à conserver

- Backend : `PytestAssertRewriteWarning`, module `anyio` déjà importé par le processus d'isolation avant l'initialisation de pytest. Ce n'est pas un test échoué.
- Frontend : `HTMLCanvasElement.getContext()` non implémenté sans paquet Canvas dans l'environnement de test. Les tests passent, mais cela ne permet pas de conclure à la validation complète du rendu graphique.
- Les logs backend comprennent des refus d'authentification et une fiche volontairement illisible correspondant aux scénarios de test ; ne pas les interpréter isolément comme un incident de production.

## 3. Portée et suites

Ces résultats permettent de citer **138 tests backend, 30 tests frontend et un build Vite réussi** dans les deux blocs, avec cette même référence et ces limites. Ils ne valident ni le déploiement Docker, ni le VPS, ni un parcours humain complet, ni les critères d'accessibilité dans leur ensemble, ni l'acceptation par un client.

La vérification Git effectuée après exécution n'a montré aucune modification des fichiers applicatifs suivis dans les dossiers backend, domaine, tests et frontend. Les suppressions et modifications locales préexistantes sont conservées. Les artefacts générés de build ne sont pas un déploiement.

Les résultats historiques cités dans les archives restent attachés à leur contexte ; cette nouvelle campagne ne les remplace pas rétroactivement. Avant la soutenance, répéter la démonstration sur la version effectivement présentée et recueillir séparément les observations et la décision.