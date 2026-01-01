# Software CRM 🚀

Application de gestion clientèle (CRM) pour l'entreprise EpicEvents, développée en **Python** avec **PostgreSQL**.

---

## 📋 Fonctionnalités

### 🔐 Authentification & sécurité

- Connexion par email / mot de passe  
- Hachage des mots de passe avec **bcrypt**  
- Tokens **JWT** pour les sessions (restauration de session)  
- Limitation des tentatives de connexion (anti brute force)  
- Permissions par département : **MANAGEMENT**, **SALES**, **SUPPORT**

### 👥 Gestion des clients

- CRUD complet : création, lecture, mise à jour, suppression  
- Attribution des clients aux commerciaux  
- Recherche avancée (par commercial, email, etc.)  
- Affichage enrichi en console (bibliothèque **rich**)  

### 📄 Gestion des contrats

- Création de contrats liés aux clients  
- Statut signé / non signé  
- Gestion des paiements et montants restants  
- Filtres sur contrats non signés, non soldés, etc.  

### 📅 Gestion des événements

- Création d’événements à partir de contrats **signés**  
- Attribution d’un membre du support  
- Filtres par date, lieu, client, support  
- Liste des événements sans support, événements à venir, en cours, passés  

### 📊 Reporting & audit

- Statistiques sur les événements (résumé global)  
- Modèle d’audit des actions utilisateurs (`AuditLog`)  
- Logging applicatif structuré + envoi des erreurs à **Sentry**  

---

## 📂 Structure du projet

Software_CRM/
app/
crud/
crud_users.py
crud_clients.py
crud_contracts.py
crud_events.py
init.py
database/
database.py
init.py
models/
users.py
clients.py
contracts.py
events.py
audit.py
init.py
utils/
auth.py
validators.py
logging_config.py
sentry_config.py
init.py
tests/
conftest.py
tests_unitaires/
test_auth.py
test_clients.py
test_contracts.py
test_events.py
test_logging_and_sentry.py
test_users.py
test_validators.py
test_audit.py
test_integration/
test_flow_end_to_end.py
main.py
README.md
requirements.txt
.env.example

text

---

## 🚀 Installation & configuration

### Prérequis

- Python **3.9+** (testé en 3.13.9)  
- PostgreSQL **12+**  
- `pip` installé  

### 1. Cloner le projet

git clone https://github.com/Imed7223/Software_CRM.git
cd Software_CRM

text

### 2. Créer et activer l’environnement virtuel

Création
`python -m venv venv`

Activation Windows
venv\Scripts\activate

Activation Linux / macOS
source venv/bin/activate

text

### 3. Installer les dépendances

`pip install -r requirements.txt`

text

### 4. Configurer l’environnement

`cp .env.example .env`

text

Édite le fichier `.env` avec tes paramètres :

- Connexion PostgreSQL (`DATABASE_URL`, `TEST_DATABASE_URL`)  
- Clé secrète JWT (`SECRET_KEY`)  
- DSN Sentry (`SENTRY_DSN`, optionnel)  
- Variables diverses (`ACCESS_TOKEN_EXPIRE_MINUTES`, `ENVIRONMENT`, etc.)  

### 5. Créer les bases de données

createdb epicevents
createdb epicevents_test

text

---

## 🧪 Lancer les tests & mesurer la couverture

Les tests sont organisés en :

- **Tests unitaires** : `tests/tests_unitaires/`  
- **Tests d’intégration** : `tests/test_integration/`  

Lancer toute la suite avec coverage :

`coverage run -m pytest`
`coverage report -m`
`coverage html`

text

-`coverage report -m` affiche la couverture en console (≈ **83 %** actuellement).  
- `coverage html` génère un rapport détaillé dans `htmlcov/` (ouvrir `htmlcov/index.html` dans un navigateur).  
---

## ✅ Qualité de code (PEP8)

Le projet utilise **flake8** pour vérifier le respect des conventions PEP8.

### Installation

pip install flake8

text

### Lancer l’analyse flake8

Depuis la racine du projet :

`python -m flake8 .`
---

## 🖥️ Utilisation via CLI

### 1. Supprimer toutes les tables (DROP) puis les recréer.
     (⚠️ IRRÉVERSIBLE : toutes les données sont perdues).
### 2. Initialiser l’application (données de démo)

`python python init_database.py

text

Cette commande :
-Donne 2 choix :
-Soit, Supprimer toutes les tables (DROP) puis les recréer.
- Soi, Crée les tables nécessaires en base  
- Ajoute des utilisateurs de démo (MANAGEMENT / SALES / SUPPORT)  
- Ajoute des clients, contrats et événements de test  

### 2. Lancer l’application (commande demandée par le cahier des charges)

`python main.py login`

text

Flux typique :

- Si un **jeton de session** valide existe :  
  - Affiche : `Session restaurée : <Nom> (<Rôle>)`  
  - Va directement au **menu principal** pour cet utilisateur  

- Sinon :  
  - Demande email + mot de passe  
  - Valide l’email (format)  
  - Vérifie email / mot de passe et limite les tentatives  
  - En cas de succès, enregistre un jeton JWT de session et affiche le menu  

### 3. Navigation dans les menus

Une fois connecté, menu principal par exemple :

==================================================
MENU PRINCIPAL - <Nom Utilisateur>
👥 Gestion des clients

📄 Gestion des contrats

📅 Gestion des événements

🚪 Déconnexion

text

Les options et sous-menus dépendent du **rôle** :

- **SALES** : principalement clients / contrats / ses événements  
- **SUPPORT** : événements, clients liés, contrats associés  
- **MANAGEMENT** : vision globale, gestion des utilisateurs, reporting  

Option `0` = **Déconnexion** :

- Supprime / invalide le token de session  
- Retour à l’écran de connexion  

---

Ce README présente :

- L’architecture principale (auth, CRUD, events, audit, logging/Sentry)  
- Les commandes CLI importantes (setup, login, tests avec coverage)  
- La démarche de tests et de couverture conforme au cahier des charges.