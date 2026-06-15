# Rapport Livrable 2 — Projet Cloud

## 1. Contexte et objectif (0,5 page)

Ce projet vise à déployer une application de scoring de crédit sur le cloud en respectant le plan défini dans le Livrable 1. L'objectif est de proposer un frontend accessible, une API FastAPI exposant des services de prédiction et de santé, une base de données PostgreSQL persistante et une architecture conteneurisée.

La version actuelle met en place le même périmètre fonctionnel, avec une disponibilité provisoire sur Render pendant que le déploiement AWS est finalisé.

---

## 2. Architecture (schéma final, comparaison L1) (1 page)

### Architecture finale

L'application est composée de trois services principaux :

- **Frontend** : application web Angular servie via Nginx dans un container Docker.
- **Backend** : API FastAPI servant les points d'entrée métiers et la logique ML.
- **Base de données** : PostgreSQL, exécutée dans un container Docker pour persistance locale.

Le déploiement local est géré par `docker-compose.yml`, qui orchestre les services et garantit l'accès au backend depuis le frontend.

### Comparaison avec le Livrable 1

| Élément prévu L1 | État actuel | Commentaire |
|------------------|-------------|-------------|
| Frontend web conteneurisé | Oui | Angular + Nginx au lieu de React. Écart documenté. |
| Backend FastAPI | Oui | Service en place et testable. |
| Base PostgreSQL | Oui | Utilisée par Docker Compose. |
| Déploiement cloud AWS | En cours | AWS prévu, mais provisionnement non finalisé. URL Render disponible. |
| CI/CD avec scans | Oui | GitHub Actions implémenté avec trufflehog, pip-audit, Trivy. |

---

## 3. Développement (back, front, BDD, ML) (2 pages)

### Backend

Le backend FastAPI se trouve dans `Backend/app`.

- Route `/health` pour vérifier l'état du service.
- API de scoring exposée sous `/api/v1/predict/{user_id}`
- Authentification API basée sur une clé / JWT, avec validation dans `app/core/security.py`.
- Base SQL gérée via SQLAlchemy et initialisation dans `Backend/app/db.py`.

### Frontend

Le frontend est développé en Angular 16 dans `Frontend/`.

- Interface utilisateur pour l'affichage de score et des résultats.
- Consommation de l'API backend via un endpoint configurable.
- Construction avec `npm run build` et diffusion par Nginx dans Docker.

### Base de données

PostgreSQL est configuré dans `docker-compose.yml` :

- Utilisation de `postgres:15`.
- Volume Docker `postgres_data` pour persistance des données.
- Variables d'environnement `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`.

### Machine Learning

Le moteur ML est intégré dans le backend via une logique de scoring.

- Le projet entraîne un modèle depuis les données de training.
- La prédiction est exécutée en backend (via `model.predict(...)`).
- Le service expose les résultats calculés en score, profil de risque, capacité d'emprunt et autres métriques.

---

## 4. Conteneurisation et déploiement (1,5 page)

### Conteneurisation Docker

- `Backend/Dockerfile` construit l'API FastAPI.
- `Frontend/Dockerfile` construit l'application Angular et sert le build via Nginx.
- `docker-compose.yml` orchestre les containers `backend`, `frontend` et `db`.

Les conteneurs sont exposés localement sur :

- frontend : `http://localhost:4200`
- backend : `http://localhost:8000`

### Déploiement cloud

L'objectif de déploiement est AWS, avec :

- GitHub Actions pour build/push et déploiement.
- Beanstalk / ECS / ECR comme cible prévue.
- Utilisation de GitHub Secrets pour les clés AWS et les variables sensibles.

### État actuel

Le déploiement AWS n'est pas encore complètement opérationnel. En attendant la finalisation, nous avons rendu disponible une URL publique sur Render :

- `https://cequality-frontend.onrender.com`

Cette URL permet de présenter une version fonctionnelle du frontend et de montrer la disponibilité de l'application pendant que l'infrastructure AWS est stabilisée.

---

## 5. Sécurité (exécution du plan L1, écarts) (1 page)

### Mesures prévues et état

| Mesure prévue (L1) | Faite ? | Preuve / explication de l'écart |
|--------------------|---------|---------------------------------|
| Secrets en variables d'environnement | Oui | `.env` et les secrets de pipeline sont exclus du dépôt. |
| Trufflehog en CI | Oui | Workflow `ci-cd.yml` exécute `trufflehog`. |
| pip-audit en CI | Oui | Audit Python activé dans `Backend`. |
| Trivy en CI | Oui | Scan d'image Docker inclus. |
| HTTPS en production | En attente / partiel | URL Render disponible en HTTPS. AWS en cours. |
| JWT auth API | Oui | Authentification implémentée côté backend. |

### Sécurité des dépendances

- `requirements.txt` gère les dépendances Python.
- `npm install` et `npm build` isolent le frontend.
- Les fichiers secrets et les assets sensibles sont dans `.gitignore`.

### Écarts

- Déploiement AWS pas encore stabilisé : la production définitive AWS n'est pas livrée à ce stade.
- L'URL Render est utilisée comme solution provisoire pour garantir une démonstration publique.

---

## 6. Coûts (réel vs estimé) (0,5 page)

### Estimation du Livrable 1

| Poste | Service | Coût mensuel estimé |
|-------|---------|---------------------|
| **Compute (Backend ML)** | AWS ECS Fargate (0.25 vCPU, 0.5 GB) ou AppRunner | ~ 4 $ |
| **Hébergement Frontend** | Nginx dans ECS (Idem Fargate) ou S3/CloudFront | ~ 1 $ |
| **Base de données** | AWS RDS (db.t4g.micro) - Free Tier | ~ 0 $ à 15 $ |
| **Stockage image conteneurs** | Amazon ECR | ~ 0,5 $ |
| **Bande Passante (Egress)** | AWS Data Transfer (< 1 GB) | ~ 0 $ (Inclus) |
| **Total estimé** | | **~ 5,5 $** *(avec Free Tier)* |

**Hypothèses Livrable 1 :** ~100-300 utilisateurs finaux, 2-3 prévisions de scoring par mois, faible trafic réseau.

### État réel et comparaison

**AWS :** Le déploiement AWS n'étant **pas encore finalisé**, aucune donnée réelle de consommation n'est disponible. Les ressources ne sont pas encore provisionnées en production, donc pas de coûts AWS effectifs à rapporter.

**Infrastructure locale :** Coûts nuls en environnement Docker Compose (développement).

**Démonstration publique :** URL Render utilisée (`https://cequality-frontend.onrender.com`) avec plan gratuit. Coût réel actuel : **0 €**.

### Évaluation future

Une fois le déploiement AWS finalisé, une comparaison plan vs réalité pourra être effectuée. Le coût réel dépendra de :
- Le taux d'utilisation réel (requêtes/jour, durée de life des tâches ECS)
- La région AWS choisie (eu-west-1 vs autre)
- L'application du Free Tier (disponible 12 mois)

Actuellement, le projet reste dans les limites estimées.

---

## 7. Difficultés et solutions (0,5 page)

### Difficultés rencontrées

- Gestion des environnements et des secrets entre local, CI et AWS.
- Adaptation du frontend prévu en React vers une implémentation Angular.
- Finalisation du déploiement AWS, notamment l'intégration de la configuration OIDC et des variables d'environnement GitHub.

### Solutions appliquées

- Centralisation des variables sensibles dans `.gitignore` et GitHub Secrets.
- Mise en place d'un pipeline GitHub Actions solide avec scans de sécurité.
- Usage de Render comme solution temporaire pour répondre à la contrainte d'URL active.

---

## 8. Conclusion (0,5 page)

Le projet est fonctionnel en mode conteneurisé localement et dispose d'une démonstration publique accessible sur Render. La CI/CD est en place avec des scans de sécurité et des tests automatisés. Le déploiement AWS est encore en travail, mais la structure du projet permet d'enchaîner vers une mise en production complète rapidement.

> Note : l'URL provisoire est `https://cequality-frontend.onrender.com` le temps que le déploiement AWS soit finalisé.
