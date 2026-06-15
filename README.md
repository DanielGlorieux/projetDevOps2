# CEquality (Credit Equality) - Projet Cloud & DevOps

## 1. Vue d'ensemble

**CEquality** est une application web de scoring de crédit qui analyse l'historique de transactions Wave d'un utilisateur (importé via PDF) pour prédire sa capacité d'emprunt, son score de remboursement et sa santé financière globale. Elle s'adresse aux particuliers et aux institutions financières (MFI, banques) qui souhaitent évaluer la solvabilité de clients non bancarisés mais actifs sur Mobile Money.

## 2. Problème résolu

La majorité des populations en Afrique de l'Ouest n'ont pas d'historique bancaire traditionnel, ce qui les exclut du système de crédit classique. Pourtant, elles effectuent des dizaines à des centaines de transactions Wave par mois. **Wave Credit Score** transforme cet historique en signal financier exploitable.

L'objectif de ce livrable (n°2) est de valider le déploiement Cloud, l'approche CI/CD et l'architecture logicielle via des conteneurs.

## Architecture

L'application est découpée en micro-services :
1. **Frontend** : Application Angular 16 servie via Nginx.
2. **Backend API** : Application FastAPI pour le traitement ML, la validation Google Auth, et la distribution des scores.
3. **Database** : PostgreSQL (bien que testable en SQLite) pour la persistance locale des recommandations de profil.

*(NB - Écart au plan: Bien que l'application soit testable avec SQLite et initialement développée ainsi pour la simplicité locale, le fichier docker-compose utilise une instance `PostgreSQL` pour satisfaire aux attentes explicites d'extensibilité du Livrable 2.)*

## Lancer le projet en local (Docker Compose)

Assurez-vous d'avoir installé **Docker** et **Docker Compose** sur votre machine. Depuis la racine du projet, lancez :

```bash
docker compose up --build -d
```

1. **Frontend** : Accessible via [http://localhost:4200](http://localhost:4200)
2. **Backend (API)** : Accessible via [http://localhost:8000](http://localhost:8000)
3. **Base de données** : Expose le port PostgreSQL classique `5432`

> Note : une URL publique temporaire est disponible pendant que le déploiement AWS est en cours de finalisation : https://cequality-frontend.onrender.com

## Documentation et Rapports

Vous trouverez tous les rapports de planification et de validation liés au livrable dans le dossier `docs/` (le rapport final PDF a été généré localement).

## Pipeline CI/CD

Un pipeline automatisé tourne à chaque `push` via **GitHub Actions**. Il valide les règles suivantes :
- Scans de sécurité : `trufflehog` (recherche de clefs d'API exposées) et `pip-audit` / `Trivy`.
- Lancement de tests unitaire `pytest`.
- Construction des images Docker.
- (Optionnel/Activé) : Redirection vers Amazon ECR si branché.

## Développement technique

- La capacité d'emprunt a été repensée pour être extraite dynamiquement depuis le Backend ML et calculée avec les revenus plutôt qu'inscrite en dur côté UI.
- L'authentification utilise la vérification de jetons JWT sécurisés via OAuth Google. 
