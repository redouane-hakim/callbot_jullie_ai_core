# Base de Données Unifiée - CNP Assurances Callbot 🗄️

## Vue d'ensemble

La base de données unifiée centralise **toutes les données** du callbot :
- ✅ Interactions CRM (cas simples)
- ✅ Escalades Human Handoff (cas complexes)
- ✅ Historique de conversations
- ✅ Logs de réponses
- ✅ Métriques et analytics

## Architecture

### 🎯 Table Centrale: `interactions`

Toutes les interactions passent par cette table, qu'elles soient:
- Traitées par le **CRM Agent** (cas simples)
- Escaladées vers **Human Handoff Agent** (cas complexes)

```
interactions (table centrale)
    ├── conversation_messages (historique complet)
    ├── crm_actions (actions CRM exécutées)
    ├── handoff_tickets (tickets d'escalade)
    └── response_logs (réponses générées)
```

## Tables

### 1. **interactions** - Table Centrale
```sql
interaction_id (UUID)           -- ID unique
customer_id (VARCHAR)           -- ID client
channel (VARCHAR)               -- phone, chat, email
intent (VARCHAR)                -- Intent détecté
emotion (VARCHAR)               -- Émotion du client
urgency (VARCHAR)               -- low, medium, high
confidence_score (FLOAT)        -- Confiance intent
status (VARCHAR)                -- pending, in_progress, completed, failed
assigned_agent (VARCHAR)        -- Agent qui a traité
created_at, updated_at          -- Timestamps
resolved_at                     -- Temps de résolution
resolution_time_seconds (INT)   -- Durée totale
```

**Statuts possibles:**
- `pending` → Interaction créée, en attente de traitement
- `in_progress` → En cours de traitement (handoff assigné)
- `completed` → Terminée avec succès
- `failed` → Échouée

### 2. **conversation_messages** - Historique
```sql
message_id (UUID)
interaction_id (UUID FK)        -- Lien vers interaction
turn_number (INT)               -- Numéro du tour
speaker (VARCHAR)               -- customer, agent, system
message (TEXT)                  -- Contenu du message
timestamp
metadata (JSONB)                -- Données additionnelles
```

### 3. **crm_actions** - Actions CRM
```sql
action_id (UUID)
interaction_id (UUID FK)
customer_id (VARCHAR)
action_type (VARCHAR)           -- update_address, check_policy_status, etc.
input_data (JSONB)              -- Données en entrée
output_data (JSONB)             -- Résultat de l'action
success (BOOLEAN)               -- Succès ou échec
error_message (TEXT)
execution_time_ms (INT)
executed_at
```

**Types d'actions CRM:**
- `update_address`
- `check_policy_status`
- `get_customer_info`
- `update_payment_method`

### 4. **handoff_tickets** - Escalades
```sql
ticket_id (UUID)
interaction_id (UUID FK)
customer_id (VARCHAR)
reason (TEXT)                   -- Raison de l'escalade
priority (VARCHAR)              -- low, medium, high
status (VARCHAR)                -- queued, assigned, in_progress, resolved
queue_name (VARCHAR)            -- File d'attente
assigned_agent_id (VARCHAR)
assigned_at
resolved_at
resolution_notes (TEXT)
context_data (JSONB)            -- Contexte complet
created_at
```

**Statuts de tickets:**
- `queued` → En attente dans la file
- `assigned` → Assigné à un agent
- `in_progress` → Agent en train de traiter
- `resolved` → Résolu

### 5. **agent_notifications** - Alertes agents
```sql
notification_id (UUID)
ticket_id (UUID FK)
agent_id (VARCHAR)
notification_type (VARCHAR)     -- new_ticket, urgent, reminder
message (TEXT)
is_read (BOOLEAN)
created_at
read_at
```

### 6. **response_logs** - Logs réponses
```sql
log_id (UUID)
interaction_id (UUID FK)
response_text (TEXT)
tone (VARCHAR)                  -- empathetic, professional, friendly
confidence_score (FLOAT)
execution_time_ms (INT)
model_used (VARCHAR)            -- gpt-4o-min
created_at
```

### 7. **customers** - Mini CRM
```sql
customer_id (VARCHAR PK)
name (VARCHAR)
email (VARCHAR)
phone (VARCHAR)
segment (VARCHAR)               -- premium, standard
created_at, updated_at
metadata (JSONB)
```

### 8. **analytics_metrics** - Métriques
```sql
metric_id (UUID)
metric_date (DATE)
metric_type (VARCHAR)
metric_value (FLOAT)
dimensions (JSONB)
created_at
```

## Flux de Données

### 🔹 Cas Simple (CRM)
```
1. Client appelle → Route_request()
   └── Crée interaction (status: pending)
   └── Ajoute message client (conversation_messages)

2. Tool Router → Délègue au CRM Agent
   └── CRM Agent exécute action
   └── Log action dans crm_actions
   └── Update interaction (status: completed)

3. Response Builder génère réponse
   └── Log réponse dans response_logs
   └── Ajoute message agent (conversation_messages)
```

### 🔹 Cas Complexe (Handoff)
```
1. Client appelle → Route_request()
   └── Crée interaction (status: pending)
   └── Ajoute message client

2. Tool Router → Détecte escalade nécessaire
   └── Délègue au Human Handoff Agent
   └── Crée handoff_ticket (status: queued)
   └── Update interaction (status: in_progress)

3. Agent humain traite le ticket
   └── Update ticket (status: assigned → in_progress → resolved)
   └── Update interaction (status: completed, resolved_at)

4. Response Builder génère réponse empathique
   └── Log réponse
```

## Installation

### 1. Installer PostgreSQL

**Windows:**
```powershell
# Télécharger depuis https://www.postgresql.org/download/windows/
# Ou via Chocolatey:
choco install postgresql
```

### 2. Créer la base de données

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base
CREATE DATABASE callbot_db;

# Créer un utilisateur
CREATE USER callbot_user WITH PASSWORD 'votre_mot_de_passe';

# Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE callbot_db TO callbot_user;

# Quitter
\q
```

### 3. Exécuter le schéma

```bash
# Appliquer le schéma SQL
psql -U callbot_user -d callbot_db -f database_schema.sql
```

### 4. Configurer .env

```env
DATABASE_URL=postgresql://callbot_user:votre_mot_de_passe@localhost:5432/callbot_db
```

## Utilisation avec Python

### DatabaseService - API Complète

```python
from src.database.db_service import db_service

# 1. Créer une interaction
interaction_id = db_service.create_interaction(
    customer_id="CUST-001",
    channel="phone",
    intent="check_policy_status",
    emotion="neutral",
    urgency="low",
    confidence_score=0.95
)

# 2. Ajouter un message
db_service.add_conversation_message(
    interaction_id=interaction_id,
    speaker="customer",
    message="Je veux vérifier ma police",
    turn_number=1
)

# 3. Logger une action CRM
db_service.log_crm_action(
    interaction_id=interaction_id,
    customer_id="CUST-001",
    action_type="check_policy_status",
    input_data={"policy_number": "POL-001"},
    output_data={"status": "active"},
    success=True,
    execution_time_ms=120
)

# 4. Mettre à jour le statut
db_service.update_interaction_status(
    interaction_id, 
    "completed", 
    "crm_agent"
)

# 5. Récupérer l'historique
messages = db_service.get_conversation_history(interaction_id)

# 6. Créer un ticket handoff
ticket_id = db_service.create_handoff_ticket(
    interaction_id=interaction_id,
    customer_id="CUST-001",
    reason="Sinistre complexe",
    priority="high",
    queue_name="sinistres"
)

# 7. Assigner à un agent
db_service.assign_ticket_to_agent(
    ticket_id=ticket_id,
    agent_id="AGENT-123",
    queue_name="sinistres"
)

# 8. Résoudre le ticket
db_service.resolve_ticket(
    ticket_id=ticket_id,
    resolution_notes="Sinistre traité avec succès"
)

# 9. Logger une réponse
db_service.log_response(
    interaction_id=interaction_id,
    response_text="Votre police est active",
    tone="professional",
    confidence_score=0.95,
    execution_time_ms=250
)

# 10. Métriques
metrics = db_service.get_daily_metrics()
```

## Vues Utiles

### v_interactions_with_last_message
Interactions avec le dernier message échangé
```sql
SELECT * FROM v_interactions_with_last_message 
WHERE DATE(created_at) = CURRENT_DATE;
```

### v_handoff_tickets_full
Tickets avec contexte complet de l'interaction
```sql
SELECT * FROM v_handoff_tickets_full 
WHERE status = 'queued' 
ORDER BY priority DESC;
```

### v_daily_metrics
Métriques quotidiennes agrégées
```sql
SELECT * FROM v_daily_metrics 
WHERE metric_date >= CURRENT_DATE - INTERVAL '7 days';
```

## Requêtes Utiles

### 1. Interactions du jour
```sql
SELECT 
    interaction_id,
    customer_id,
    intent,
    status,
    created_at
FROM interactions
WHERE DATE(created_at) = CURRENT_DATE
ORDER BY created_at DESC;
```

### 2. Top actions CRM
```sql
SELECT 
    action_type,
    COUNT(*) as count,
    AVG(execution_time_ms) as avg_time,
    SUM(CASE WHEN success THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as success_rate
FROM crm_actions
WHERE DATE(executed_at) = CURRENT_DATE
GROUP BY action_type
ORDER BY count DESC;
```

### 3. Tickets en attente
```sql
SELECT 
    t.ticket_id,
    t.customer_id,
    t.priority,
    t.reason,
    i.intent,
    i.emotion,
    EXTRACT(EPOCH FROM (NOW() - t.created_at))/60 as wait_minutes
FROM handoff_tickets t
JOIN interactions i ON t.interaction_id = i.interaction_id
WHERE t.status = 'queued'
ORDER BY 
    CASE t.priority 
        WHEN 'high' THEN 1 
        WHEN 'medium' THEN 2 
        ELSE 3 
    END,
    t.created_at ASC;
```

### 4. Performance quotidienne
```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
    ROUND(AVG(resolution_time_seconds)::numeric, 2) as avg_resolution_sec,
    COUNT(DISTINCT customer_id) as unique_customers
FROM interactions
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

## Avantages de l'Architecture Unifiée

✅ **Traçabilité complète**: Chaque interaction a un ID unique qui lie tous les événements

✅ **Analytics simplifiés**: Une seule source de vérité pour les métriques

✅ **Debugging facile**: Historique complet de conversation + logs d'actions

✅ **Évolutivité**: Facile d'ajouter de nouvelles tables liées à `interactions`

✅ **Cohérence**: Pas de désynchronisation entre plusieurs bases

✅ **Performance**: Index optimisés sur les colonnes fréquemment utilisées

## Maintenance

### Backup quotidien
```bash
pg_dump -U callbot_user callbot_db > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
psql -U callbot_user callbot_db < backup_20241218.sql
```

### Nettoyage old data (>90 jours)
```sql
DELETE FROM interactions 
WHERE created_at < NOW() - INTERVAL '90 days';
```

## Support

Pour toute question sur la base de données:
- 📧 Contact: IBRAHIM (Tool Router & Response Builder)
- 📚 Documentation: `IBRAHIM_GUIDE.md`

---

**Note**: Cette base de données unifiée remplace l'ancienne architecture avec bases séparées pour CRM et Handoff. 🎉
