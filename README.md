EpicEvents CRM 🚀
Application de gestion clientèle (CRM) pour l'entreprise EpicEvents, développée en Python avec PostgreSQL.

📋 Fonctionnalités
🔐 Authentification & Sécurité
Connexion avec email/mot de passe
Hachage bcrypt des mots de passe
Tokens JWT pour les sessions
Limitation des tentatives de connexion
Permissions par département (Gestion, Commercial, Support)
👥 Gestion des Clients
Création, lecture, mise à jour, suppression (CRUD)
Attribution automatique aux commerciaux
Recherche avancée
Suivi des contacts
📄 Gestion des Contrats
Création de contrats
Signature électronique
Gestion des paiements
Filtres (non signés, non payés, etc.)
📅 Gestion des Événements
Planification d'événements
Attribution de support
Filtres par date, lieu, support
Événements sans support
📊 Reporting
Statistiques utilisateurs
Statistiques contrats
Statistiques événements
Rapports personnalisables
🚨 Monitoring
Journalisation avec Sentry
Audit des actions sensibles
Surveillance des erreurs en temps réel
🚀 Installation Rapide
Prérequis
Python 3.9+
PostgreSQL 12+
pip
Installation
# 1. Cloner le projet
git clone <repository-url>
cd Software_CRM

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# 6. Créer les bases de données
createdb epicevents
createdb epicevents_test

# 7. Initialiser l'application
python main.py setup --demo

# 8. Lancer l'application (COMMANDE DEMANDÉE PAR LE CAHIER DES CHARGES)
python main.py login