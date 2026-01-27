# 🚀 Guide de Démarrage Rapide - Base de Données Unifiée

## Prérequis

✅ Python 3.12.0 installé  
✅ PostgreSQL installé  
✅ Clé API OpenAI

## Installation en 5 étapes

### 1️⃣ Installer PostgreSQL

**Windows:**
```powershell
# Option 1: Télécharger l'installeur
https://www.postgresql.org/download/windows/

# Option 2: Via Chocolatey
choco install postgresql
```

Pendant l'installation:
- Port: `5432` (par défaut)
- Mot de passe: Choisissez un mot de passe sécurisé
- Note: Mémorisez ce mot de passe!

### 2️⃣ Créer la base de données

Ouvrez **pgAdmin** ou le terminal PostgreSQL:

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE callbot_db;

-- Créer un utilisateur
CREATE USER callbot_user WITH PASSWORD 'votre_mot_de_passe';

-- Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE callbot_db TO callbot_user;

-- Se connecter à la nouvelle base
\c callbot_db

-- Activer l'extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Quitter
\q
```

### 3️⃣ Exécuter le schéma SQL

```powershell
# Dans le dossier du projet
cd "c:\Users\IBRAHIM NASSIH\Documents\VSCode\callbot V1"

# Appliquer le schéma
psql -U callbot_user -d callbot_db -f database_schema.sql
```

Si ça demande un mot de passe, entrez celui que vous avez créé à l'étape 2.

### 4️⃣ Configurer l'environnement

Créez un fichier `.env` à partir de `.env.example`:

```powershell
Copy-Item .env.example .env
```

Éditez `.env` et remplissez:

```env
# OpenAI
OPENAI_API_KEY=sk-...votre_clé_ici...

# PostgreSQL (IMPORTANT: Remplacez par vos vraies valeurs)
DATABASE_URL=postgresql://callbot_user:votre_mot_de_passe@localhost:5432/callbot_db

# CRM API (mock pour l'instant)
CRM_API_URL=http://localhost:8003/api

# App
APP_ENV=development
DEBUG=True
```

### 5️⃣ Installer les dépendances Python

```powershell
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Installer les packages
pip install -r requirements.txt
```

## ✅ Vérification de l'installation

### Test 1: Connexion à la base de données

```python
# test_db_connection.py
from src.database.db_service import db_service

try:
    conn = db_service._get_connection()
    if conn:
        print("✅ Connexion réussie!")
        conn.close()
    else:
        print("❌ Échec de connexion")
except Exception as e:
    print(f"❌ Erreur: {e}")
```

Exécutez:
```powershell
python test_db_connection.py
```

### Test 2: Démonstration complète

```powershell
python demo_with_database.py
```

Vous devriez voir:
- ✅ Création d'interactions
- ✅ Actions CRM loggées
- ✅ Tickets handoff créés
- ✅ Historique de conversation
- ✅ Métriques quotidiennes

## 🎯 Architecture Complète

```
Client appelle
    ↓
Route_request() → Crée interaction en BDD
    ↓
Tool Router → Décide CRM ou Handoff
    ↓
┌─────────────────────┬─────────────────────┐
│   CRM Agent         │   Handoff Agent     │
│   (cas simple)      │   (cas complexe)    │
│                     │                     │
│ - log_crm_action()  │ - create_ticket()   │
│ - update_status()   │ - assign_agent()    │
└─────────────────────┴─────────────────────┘
    ↓
Response Builder → Génère réponse
    ↓
log_response() → Enregistre en BDD
    ↓
Tout est tracé dans la base unifiée! ✨
```

## 📊 Vérifier les données

### Option 1: pgAdmin (GUI)

1. Ouvrez **pgAdmin**
2. Connectez-vous au serveur `localhost`
3. Base de données → `callbot_db`
4. Schemas → public → Tables

Vous verrez les 8 tables:
- ✅ interactions
- ✅ conversation_messages
- ✅ crm_actions
- ✅ handoff_tickets
- ✅ agent_notifications
- ✅ response_logs
- ✅ customers
- ✅ analytics_metrics

### Option 2: Terminal psql

```sql
-- Se connecter
psql -U callbot_user -d callbot_db

-- Lister les tables
\dt

-- Voir les interactions
SELECT * FROM interactions ORDER BY created_at DESC LIMIT 5;

-- Voir les actions CRM
SELECT action_type, COUNT(*) FROM crm_actions GROUP BY action_type;

-- Voir les tickets
SELECT status, COUNT(*) FROM handoff_tickets GROUP BY status;

-- Quitter
\q
```

## 🔧 Commandes Utiles

### Réinitialiser la base

```sql
-- Se connecter
psql -U callbot_user -d callbot_db

-- Supprimer toutes les données (ATTENTION!)
TRUNCATE TABLE interactions CASCADE;

-- Ou supprimer et recréer
DROP DATABASE callbot_db;
CREATE DATABASE callbot_db;
-- Puis réexécuter database_schema.sql
```

### Backup

```powershell
# Créer un backup
pg_dump -U callbot_user callbot_db > backup_$(Get-Date -Format "yyyyMMdd").sql

# Restore depuis backup
psql -U callbot_user callbot_db < backup_20241218.sql
```

## 🐛 Troubleshooting

### Erreur: "FATAL: password authentication failed"

➡️ Vérifiez `DATABASE_URL` dans `.env`  
➡️ Vérifiez que l'utilisateur existe: `psql -U postgres -c "\du"`

### Erreur: "could not connect to server"

➡️ PostgreSQL est-il démarré?
```powershell
# Vérifier le service
Get-Service postgresql*
# Démarrer si arrêté
Start-Service postgresql-x64-14  # Adaptez le nom
```

### Erreur: "relation does not exist"

➡️ Avez-vous exécuté `database_schema.sql`?
```powershell
psql -U callbot_user -d callbot_db -f database_schema.sql
```

### Erreur: "No module named 'psycopg2'"

➡️ Installez les dépendances:
```powershell
pip install -r requirements.txt
```

## 📚 Documentation Complète

- 📖 **DATABASE_README.md** - Documentation complète de la BDD
- 📖 **IBRAHIM_GUIDE.md** - Guide complet de votre partie
- 📖 **ARCHITECTURE.md** - Architecture globale du projet

## 🎓 Exemples d'Utilisation

### Créer une interaction CRM

```python
from src.routers.tools_router import route_request

result = route_request(
    intent="check_policy_status",
    urgency="low",
    emotion="neutral",
    confidence=0.95,
    text="Je veux vérifier ma police",
    customer_id="CUST-001",
    channel="phone"
)

print(f"Interaction ID: {result['interaction_id']}")
print(f"Réponse: {result['response']}")
```

### Créer une escalade

```python
result = route_request(
    intent="declare_claim",
    urgency="high",
    emotion="stressed",
    confidence=0.88,
    text="J'ai eu un accident!",
    customer_id="CUST-002",
    channel="phone"
)
# → Crée automatiquement un ticket handoff
```

### Consulter l'historique

```python
from src.database.db_service import db_service

# Récupérer l'interaction
interaction = db_service.get_interaction(interaction_id)

# Récupérer la conversation
messages = db_service.get_conversation_history(interaction_id)

for msg in messages:
    print(f"[{msg['speaker']}]: {msg['message']}")
```

## 🚀 Prochaines Étapes

1. ✅ Base de données fonctionnelle
2. ✅ Agents adaptés pour logging
3. ⏳ Tester avec des vrais appels
4. ⏳ Connecter à l'audio (Abdellah)
5. ⏳ Intégrer Knowledge Base (Hatim)
6. ⏳ Connecter AI Core (Redouane)
7. ⏳ Dashboard analytics

## 💡 Astuces

- 🔍 Utilisez les **vues** pour des requêtes rapides
- 📊 Consultez `v_daily_metrics` pour les stats
- 🎯 Chaque interaction a un ID unique → traçabilité complète
- ⚡ Les index sont optimisés pour la performance
- 🔐 N'oubliez pas de sécuriser vos credentials!

---

**Besoin d'aide?** Consultez `DATABASE_README.md` ou contactez IBRAHIM! 🚀
