# Mesures de sécurité et d'accessibilité — C2.2.3

**Compétence visée.** Développer le logiciel en veillant à l'évolutivité et à la sécurisation du code source, aux exigences d'accessibilité et aux spécifications techniques et fonctionnelles.

**Projet support.** RPG 40K Survivor / Survivant de Ruche  
**Version analysée.** `v1.0.0-rncp`  
**Application déployée.** `http://89.116.111.166:8081/`

---

## 1. Objectif du livrable

Ce document formalise les mesures réellement mises en œuvre pour satisfaire le critère **C2.2.3** du Bloc 2 :

- sécurisation du code et des accès ;
- prise en compte du référentiel **OWASP Top 10 (2021)** ;
- prise en compte de l'accessibilité numérique ;
- justification du référentiel retenu ;
- mini-audit de conformité appliqué au prototype.

---

## 2. Référentiels retenus

### 2.1 Référentiel sécurité

Le projet s'appuie sur **OWASP Top 10 (2021)**, car il s'agit du référentiel le plus reconnu pour cartographier les principaux risques applicatifs web.

### 2.2 Référentiel accessibilité

Le référentiel retenu est le **RGAA** (*Référentiel Général d'Amélioration de l'Accessibilité*), pour trois raisons :

1. il constitue le référentiel français le plus pertinent pour une application web présentable en contexte de certification ;
2. il couvre les besoins essentiels observables sur ce prototype : formulaires, navigation clavier, lisibilité, messages d'erreur et structure des composants ;
3. il permet de justifier des mesures concrètes, même sur un prototype non encore totalement industrialisé.

Le niveau visé pour ce projet n'est pas une conformité RGAA exhaustive, mais une **prise en compte explicite et vérifiable** des exigences d'accessibilité prioritaires.

---

## 3. Mesures de sécurité effectivement mises en œuvre

### 3.1 Authentification et contrôle d'accès

Le backend implémente une chaîne d'authentification complète :

- mots de passe **hachés avec bcrypt** ;
- émission de **jetons JWT** signés ;
- extraction du jeton depuis l'en-tête `Authorization: Bearer <token>` ;
- vérification de validité et d'expiration du jeton ;
- gestion des rôles `player` et `admin` ;
- protection des routes sensibles via dépendances FastAPI.

### 3.2 Gestion des secrets

Les secrets sensibles ne sont pas codés en dur dans les workflows de déploiement :

- la clé OpenAI est lue via `OPENAI_API_KEY` ;
- la signature JWT est pilotée par `JWT_SECRET` ;
- les secrets de déploiement VPS sont stockés dans les secrets GitHub (`VPS_HOST`, `VPS_USER`, `VPS_PORT`, `VPS_SSH_KEY_B64`).

### 3.6 CORS restreignable en production

La politique CORS n'est plus figée sur `*`. Elle est pilotée par la variable
d'environnement `CORS_ALLOWED_ORIGINS` (liste d'origines séparées par des virgules).
En développement, l'ouverture par défaut facilite les tests ; en production, il suffit
de définir les domaines autorisés pour restreindre l'accès (OWASP A05).

### 3.7 Audit automatisé des dépendances

La CI GitHub exécute un job `security-audit` qui lance `pip-audit` (dépendances Python)
et `npm audit` (dépendances frontend) à chaque push. Ce contrôle informe en continu sur
les vulnérabilités connues des composants tiers (OWASP A06).

### 3.3 Réduction du risque de panne externe

Le projet prévoit un **fallback local** si `OPENAI_API_KEY` est absente. Cela permet de maintenir la jouabilité du prototype sans dépendance stricte à un fournisseur externe.

### 3.4 Validation et structuration des données

L'API FastAPI s'appuie sur des modèles et des structures typées, ce qui réduit les erreurs d'entrées et homogénéise les échanges JSON entre frontend et backend.

### 3.5 Déploiement contrôlé

Le passage en production est filtré par la CI :

- tests backend ;
- tests frontend ;
- build frontend ;
- tests end-to-end ;
- puis seulement déploiement automatique sur VPS si la chaîne est verte.

Cette stratégie limite le risque de mise en production d'une version cassée ou régressive.

---

## 4. Cartographie OWASP Top 10 (2021)

| Catégorie OWASP | Niveau de couverture | Mesures mises en œuvre | Preuve projet |
|---|---|---|---|
| **A01 — Broken Access Control** | **Couvert partiellement à correctement** | Routes protégées par `get_current_user` et `require_admin`, séparation des rôles `player` / `admin` | `backend/auth.py`, `backend/api.py` |
| **A02 — Cryptographic Failures** | **Couvert** | Hachage des mots de passe avec `bcrypt`, jetons JWT signés, secrets externalisés via variables d'environnement | `backend/auth.py` |
| **A03 — Injection** | **Couvert partiellement** | API typée, validation des données, pas de concaténation SQL libre côté logique métier, usage de structures contrôlées | `backend/api.py`, `backend/database.py` |
| **A04 — Insecure Design** | **Couvert partiellement** | Séparation frontend / API / domaine, rôles, persistance isolée par utilisateur, fallback maîtrisé | `docs/rncp/BLOC2_DOSSIER_FINAL.md`, `backend/api.py`, `src/` |
| **A05 — Security Misconfiguration** | **Couvert** | Variables d'environnement, workflow de déploiement contrôlé, **CORS restreignable** via `CORS_ALLOWED_ORIGINS` | `backend/api.py`, `.github/workflows/deploy-vps.yml` |
| **A06 — Vulnerable and Outdated Components** | **Couvert** | Dépendances déclarées, **audit automatisé `pip-audit` + `npm audit`** en CI, harnais de tests entretenu | `requirements.txt`, `frontend/package.json`, `.github/workflows/ci.yml` |
| **A07 — Identification and Authentication Failures** | **Couvert** | Vérification du mot de passe, tokens expirables, extraction stricte du bearer token, refus 401/403 | `backend/auth.py` |
| **A08 — Software and Data Integrity Failures** | **Couvert partiellement** | Déploiement depuis dépôt versionné, pipeline automatisée, build contrôlé, persistance structurée | `.github/workflows/ci.yml`, `.github/workflows/deploy-vps.yml` |
| **A09 — Security Logging and Monitoring Failures** | **Couvert partiellement** | Healthcheck `/api/health`, traces applicatives et suivi par pipeline, mais absence de SIEM/alerting avancé | `backend/api.py`, `docs/rncp/PROTOCOLE_DEPLOIEMENT_CONTINU_QUALITE_PERF.md` |
| **A10 — Server-Side Request Forgery (SSRF)** | **Couvert** | Aucune URL utilisateur arbitraire n'est résolue côté serveur ; les appels externes restent bornés au fournisseur IA prévu | `backend/api.py` |

### Synthèse OWASP

Le prototype couvre correctement les risques critiques liés à l'authentification, au contrôle d'accès, à la gestion des secrets, à la configuration et à la stabilité de déploiement. Les mesures suivantes ont été **implémentées** durant la finalisation :

1. **CORS restreignable** en production via `CORS_ALLOWED_ORIGINS` (A05) ;
2. **audit automatisé des dépendances** (`pip-audit` + `npm audit`) intégré à la CI (A06).

L'axe d'amélioration restant pour une industrialisation complète est le **renforcement de
l'observabilité** (journalisation structurée et alertes centralisées).

---

## 5. Mesures d'accessibilité mises en œuvre

### 5.1 Principes retenus

Le prototype vise une interface simple, textuelle et rapidement compréhensible :

- vocabulaire d'action explicite ;
- hiérarchie visuelle stable ;
- boutons clairement libellés ;
- limitation des parcours complexes ;
- compatibilité avec la navigation clavier sur les actions principales.

### 5.2 Mesures concrètes observées dans l'interface

| Mesure | Mise en œuvre constatée |
|---|---|
| Libellés explicites | Boutons d'action nommés (`JET 2D6`, `FOUILLER`, `RENCONTRE`, `SAUVER`, `RESET`) |
| Étiquettes accessibles | Usage de `aria-label` sur formulaires, champs et boutons d'action |
| Groupement sémantique | Usage de `role="group"` pour regrouper les actions de combat et les déplacements |
| Messages d'erreur perceptibles | Usage de `role="alert"` sur les erreurs d'authentification |
| Navigation clavier | Formulaires HTML standards, boutons `submit`, champs activables sans souris |
| Prévention des erreurs | Désactivation des boutons non disponibles (`disabled`) selon l'état du jeu |
| Réduction des effets visuels | Bouton d'en-tête « effets réduits » (`aria-pressed`) qui désactive scanlines et animations, préférence persistée |
| Respect des préférences système | Prise en charge de `prefers-reduced-motion` pour limiter automatiquement les animations |
| État annoncé | Zone de statut d'en-tête en `aria-live="polite"` |

### 5.3 Exemples représentatifs

- formulaire d'authentification avec labels explicites et message d'erreur accessible ;
- barre d'action libre avec champ nommé et bouton d'envoi identifié ;
- panneau d'actions rapides avec groupes d'actions ;
- panneau de combat structuré pour les commandes principales.

---

## 6. Mini-audit d'accessibilité (RGAA simplifié)

Le mini-audit ci-dessous est un **contrôle manuel ciblé** sur les parcours essentiels du prototype. Il ne remplace pas un audit RGAA exhaustif, mais constitue une preuve exploitable de prise en compte de l'accessibilité.

| Point contrôlé | Statut | Observation |
|---|---|---|
| Identification des champs de formulaire | ✅ Conforme | Les champs d'authentification et d'action libre disposent d'intitulés et/ou `aria-label`. |
| Boutons compréhensibles hors contexte visuel | ✅ Conforme | Les boutons disposent d'un libellé lisible et, sur les actions critiques, d'un `aria-label` explicite. |
| Messages d'erreur annoncés | ✅ Conforme | Les erreurs d'authentification sont portées par un conteneur `role="alert"`. |
| Navigation clavier de base | ✅ Conforme | Les interactions principales reposent sur des éléments HTML standards (`form`, `input`, `button`). |
| Prévention des actions invalides | ✅ Conforme | Les commandes impossibles sont désactivées en combat ou selon le contexte. |
| Réduction des effets visuels | ✅ Conforme | Un bouton « effets réduits » désactive scanlines/animations et la préférence est persistée. |
| Respect de `prefers-reduced-motion` | ✅ Conforme | Les animations sont automatiquement limitées si l'OS le demande. |
| Contrastes et confort visuel | ⚠️ Partiellement conforme | L'interface sombre est lisible, mais un contrôle outilisé des contrastes reste recommandé. |
| Parcours lecteur d'écran global | ⚠️ À approfondir | La base est saine, mais un audit complet avec lecteur d'écran reste à réaliser. |

### Forces principales

1. **Formulaires déjà accessibles** grâce aux labels et attributs ARIA.
2. **Actions principales compréhensibles** sans dépendre uniquement du contexte visuel.
3. **Gestion d'état claire** grâce à la désactivation des actions indisponibles.
4. **Option d'accessibilité intégrée** (réduction des effets visuels) et respect de `prefers-reduced-motion`.

### Améliorations planifiées

1. ajouter un contrôle automatisé complémentaire (Lighthouse ou axe) avant soutenance finale ;
2. vérifier et documenter les ratios de contraste ;
3. mener un audit complet au lecteur d'écran.

---

## 7. Conclusion d'évaluation C2.2.3

Le projet répond de manière crédible à l'attendu **« mesures sécurité + mesures accessibilité »** :

- la sécurité applicative est matérialisée par des mécanismes réels d'authentification, d'autorisation, de gestion des secrets et de déploiement contrôlé ;
- les 10 familles de risques **OWASP Top 10 (2021)** sont analysées et rattachées à des mesures ou limites identifiées ;
- l'accessibilité est cadrée par le **RGAA**, avec plusieurs mesures déjà visibles dans l'interface ;
- un mini-audit manuel formalise l'état courant du prototype et les améliorations prévues.

Ce livrable peut donc être utilisé comme **preuve principale C2.2.3** dans le dossier Bloc 2.