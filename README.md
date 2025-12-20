# Software CRM

Application de gestion clientèle pour l'entreprise Epicevents.

## 🚀 Installation

### 1. Prérequis
- Python 3.9+
- PostgreSQL 12+
- pip

### 2. Installation
```bash
# Cloner le projet
git clone https://github.com/Imed7223/Software_CRM.git
cd Epicevents-crm

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Créer la base de données
createdb epicevents

# Lancer l'application
python main.py