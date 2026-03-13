# README - Securite BDD, Authentification et Conformite

Ce document complete le README principal et decrit les choix et pratiques de securite autour de la base de donnees pour le projet Futurisys ML API.

## Perimetre

- API FastAPI de prediction ML
- Persistance SQLAlchemy via variable d'environnement `DATABASE_URL`
- Base de test SQLite en memoire pour les tests automatiques

---

## Documenter le choix du systeme d'authentification des donnees

### Objectif
Documenter les methodes d'authentification et de gestion des acces a la base de donnees.

### Choix retenus

1. Authentification a la base via URL de connexion
- Le projet utilise une URL de connexion en variable d'environnement (`DATABASE_URL`) pour authentifier l'application aupres du SGBD.
- Cette URL embarque le type de SGBD, l'utilisateur, le mot de passe, l'hote et la base cible.

2. Separation des contextes d'acces
- En environnement applicatif: connexion via utilisateur technique dedie (exemple: `api_user`).
- En tests: base SQLite en memoire (`sqlite:///:memory:`), sans exposition reseau.

3. Gestion des acces
- Principe de moindre privilege: l'utilisateur applicatif ne doit avoir que les droits necessaires (SELECT/INSERT/UPDATE selon besoin).
- Pas d'usage de compte administrateur pour l'API.

### Preuves dans le code

- Chargement de `DATABASE_URL`: app/config.py
- Initialisation moteur SQLAlchemy via `DATABASE_URL`: app/core/database.py
- Base SQLite en memoire pour les tests: tests/conftest.py

### Etat actuel

- Conforme sur la partie authentification technique a la BDD via variable d'environnement.
- A completer sur l'authentification applicative des appels API (JWT/API Key) si l'exigence inclut aussi le controle d'acces aux endpoints.

---

## Assurer l'operationnalite et la conformite du systeme d'authentification des donnees

### Objectif
Verifier que le systeme d'authentification fonctionne en pratique et respecte les attentes de production.

### Elements operationnels en place

1. Initialisation conditionnelle de la connexion
- Si `DATABASE_URL` est defini, la connexion BDD est ouverte.
- Sinon, l'application reste fonctionnelle sans persistance, avec journalisation d'avertissement.

2. Session SQLAlchemy geree proprement
- Session ouverte/fermee via dependance FastAPI `get_db`.
- Evite les fuites de connexions.

3. Validation en tests
- Les tests fonctionnels utilisent une base SQLite isolee en memoire.
- Les schemas sont crees/supprimes a chaque test pour garantir la reproductibilite.

### Controles de conformite recommandes

- Verifier que l'utilisateur SQL de prod ne possede pas de privileges admin.
- Verifier que la rotation des secrets est possible sans modification du code.
- Verifier la non-presence de secrets en clair dans le depot et dans les logs.
- Verifier la disponibilite d'un mecanisme d'authentification API (ex: API key ou JWT) pour limiter l'acces aux routes sensibles.

### Etat actuel

- Operationnalite BDD: OK (connexion, session, tests).
- Conformite securite complete: partielle tant qu'il n'y a pas d'authentification applicative sur les endpoints et de politique formalisee de rotation des secrets.

---

## Respecter la legislation en vigueur et les bonnes pratiques de la profession

### Objectif
Demontrer l'application des bonnes pratiques de securite et de conformite.

### Bonnes pratiques appliquees

1. Gestion des secrets
- Les secrets sont externalises via variables d'environnement.
- Le fichier `.env.local` est ignore par Git (`.gitignore`).

2. Isolation des environnements
- Separation claire entre environnement de test (SQLite memoire) et environnement d'execution.

3. Journalisation
- Journalisation applicative presente pour le suivi d'execution.
- Les logs ne doivent pas contenir de secrets ni de donnees personnelles sensibles.

### Bonnes pratiques a renforcer pour validation complete

1. Mots de passe et identifiants
- Ne jamais stocker de mot de passe en clair dans les fichiers partages.
- Utiliser un coffre de secrets (GitHub Secrets, Azure Key Vault, etc.) en production.
- Rotation periodique des credentials DB.

2. Chiffrement et transport
- Activer TLS entre application et SGBD en production.
- Restreindre l'acces reseau a la base (pare-feu, allowlist IP, reseau prive).

3. Controle d'acces API
- Ajouter un mecanisme d'authentification (API key/JWT/OAuth2) pour les routes de prediction et d'ecriture BDD.
- Ajouter des roles (lecture/ecriture/admin) si besoin metier.

4. Donnees personnelles (RGPD)
- Minimisation des donnees stockees.
- Duree de retention definie.
- Traçabilite des traitements et suppression sur demande si applicable.

5. Hachage des mots de passe
- Si des comptes utilisateurs sont ajoutes plus tard, les mots de passe devront etre haches (Argon2 ou bcrypt), jamais stockes en clair.

---

## Explication de la base de donnees du projet

La base de donnees sert a tracer les donnees d'entree employees et les resultats de prediction produits par l'API.

### Technologie et connexion

- Couche ORM: SQLAlchemy
- Connexion: variable d'environnement `DATABASE_URL`
- Session BDD: dependance FastAPI `get_db`

En environnement de test, une base SQLite en memoire est utilisee pour isoler chaque test.

### Tables principales

1. `employee_data`
- Role: stocker les donnees d'entree d'un employe utilisees pour la prediction.
- Cle primaire: `id`
- Contenu: variables RH (age, revenu, experience, satisfaction, etc.) + champs categorels (`departement`, `poste`, `domaine_etude`, `statut_marital`).
- Metadonnee: `created_at`.

2. `predictions`
- Role: stocker la sortie du modele pour chaque employe traite.
- Cle primaire: `id`
- Champs metier: `prediction` (0/1), `probability`, `risk_level` (High/Low).
- Champs de suivi: `batch_id`, `created_at`, `employee_id`.

### Relation logique entre les tables

- `employee_id` dans `predictions` permet de rattacher une prediction a un employe enregistre dans `employee_data`.
- Dans l'etat actuel, ce lien est gere applicativement et non par une contrainte de cle etrangere explicite dans les modeles.

### Flux de persistance

1. L'endpoint `/predict/csv` recoit un fichier CSV.
2. Chaque ligne est validee puis enregistree dans `employee_data`.
3. La prediction associee est enregistree dans `predictions` avec un `batch_id` commun pour le lot.
4. En cas d'erreur de validation, la transaction est annulee (`rollback`) pour conserver la coherence des donnees.

### Ce que cela apporte

- Traçabilite complete entree/sortie pour audit et analyse.
- Possibilite de reconstituer un lot de prediction via `batch_id`.
- Base exploitable pour monitoring de performance du modele dans le temps.


