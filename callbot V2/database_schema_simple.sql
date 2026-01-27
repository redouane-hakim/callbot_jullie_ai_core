-- ==========================================
-- CALLBOT JULIE - SCHÉMA SIMPLIFIÉ
-- UNE SEULE TABLE POUR TOUT
-- Version: 1.0 Simple
-- Date: 2026-01-24
-- ==========================================

-- Extension UUID pour générer des IDs uniques
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- TABLE UNIQUE : CALLBOT_INTERACTIONS
-- Regroupe TOUT : client, conversation, action
-- ==========================================

CREATE TABLE IF NOT EXISTS callbot_interactions (
    -- ID et Métadonnées
    interaction_id VARCHAR(50) PRIMARY KEY DEFAULT ('INT-' || EXTRACT(YEAR FROM CURRENT_DATE) || '-' || SUBSTRING(uuid_generate_v4()::TEXT, 1, 8)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- INFORMATIONS CLIENT
    customer_id VARCHAR(50),
    customer_name VARCHAR(200),
    customer_email VARCHAR(150),
    customer_phone VARCHAR(20),
    
    -- INFORMATIONS SESSION
    session_id VARCHAR(100),
    channel VARCHAR(20) DEFAULT 'phone',
    
    -- ANALYSE DE L'INTENT
    intent VARCHAR(50) NOT NULL,
    urgency VARCHAR(20) DEFAULT 'medium',
    emotion VARCHAR(20) DEFAULT 'neutral',
    confidence DECIMAL(3,2),
    
    -- CONVERSATION (JSON pour simplicité)
    customer_message TEXT,
    bot_response TEXT,
    conversation_history JSONB DEFAULT '[]'::jsonb,
    
    -- DÉCISION ET ACTION
    action_taken VARCHAR(50) NOT NULL,
    action_type VARCHAR(50),
    action_result JSONB,
    success BOOLEAN DEFAULT TRUE,
    
    -- CAS SIMPLE (CRM)
    crm_action_details JSONB,
    execution_time_ms INTEGER,
    
    -- CAS COMPLEXE (HANDOFF)
    is_handoff BOOLEAN DEFAULT FALSE,
    handoff_reason TEXT,
    handoff_queue VARCHAR(20),
    handoff_department VARCHAR(50),
    assigned_agent VARCHAR(50),
    ticket_status VARCHAR(20),
    estimated_wait_seconds INTEGER,
    
    -- STATUT GLOBAL
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'normal',
    resolved_at TIMESTAMP,
    resolution_time_seconds INTEGER,
    
    -- MÉTRIQUES ET FEEDBACK
    customer_satisfaction INTEGER,
    feedback_comment TEXT,
    
    -- DONNÉES ADDITIONNELLES (flexibilité)
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ==========================================
-- INDEX pour performance
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_callbot_customer ON callbot_interactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_callbot_created ON callbot_interactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_callbot_status ON callbot_interactions(status);
CREATE INDEX IF NOT EXISTS idx_callbot_intent ON callbot_interactions(intent);
CREATE INDEX IF NOT EXISTS idx_callbot_handoff ON callbot_interactions(is_handoff) WHERE is_handoff = TRUE;

-- ==========================================
-- TRIGGER pour auto-update
-- ==========================================

CREATE OR REPLACE FUNCTION update_callbot_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    
    -- Calculer le temps de résolution si l'interaction est résolue
    IF NEW.status IN ('completed', 'resolved') AND OLD.status != NEW.status THEN
        NEW.resolved_at = CURRENT_TIMESTAMP;
        NEW.resolution_time_seconds = EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - NEW.created_at))::INTEGER;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_callbot_timestamp
BEFORE UPDATE ON callbot_interactions
FOR EACH ROW EXECUTE FUNCTION update_callbot_timestamp();

-- ==========================================
-- VUES UTILES
-- ==========================================

-- Vue 1 : Interactions actives
CREATE OR REPLACE VIEW v_active_interactions AS
SELECT 
    interaction_id,
    customer_name,
    intent,
    urgency,
    action_taken,
    status,
    created_at,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - created_at))::INTEGER as duration_seconds
FROM callbot_interactions
WHERE status IN ('pending', 'in_progress');

-- Vue 2 : Handoffs en attente
CREATE OR REPLACE VIEW v_pending_handoffs AS
SELECT 
    interaction_id,
    customer_name,
    customer_phone,
    handoff_reason,
    handoff_queue,
    handoff_department,
    ticket_status,
    estimated_wait_seconds,
    created_at
FROM callbot_interactions
WHERE is_handoff = TRUE 
  AND ticket_status IN ('pending', 'assigned');

-- Vue 3 : Statistiques quotidiennes
CREATE OR REPLACE VIEW v_daily_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_interactions,
    COUNT(*) FILTER (WHERE action_taken = 'automated_response') as automated,
    COUNT(*) FILTER (WHERE action_taken = 'crm_action') as crm_actions,
    COUNT(*) FILTER (WHERE is_handoff = TRUE) as handoffs,
    ROUND(AVG(confidence)::numeric, 2) as avg_confidence,
    AVG(resolution_time_seconds) as avg_resolution_time,
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(*) FILTER (WHERE status = 'completed') as completed,
    COUNT(*) FILTER (WHERE status = 'failed') as failed
FROM callbot_interactions
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- ==========================================
-- DONNÉES DE TEST (optionnel)
-- ==========================================

-- Exemple 1 : Cas simple CRM
INSERT INTO callbot_interactions (
    customer_id,
    customer_name,
    customer_email,
    customer_phone,
    session_id,
    intent,
    urgency,
    emotion,
    confidence,
    customer_message,
    bot_response,
    action_taken,
    action_type,
    crm_action_details,
    success,
    status
) VALUES (
    'CUST-001',
    'Jean Dupont',
    'jean.dupont@example.com',
    '+33612345678',
    'SESSION-001',
    'update_address',
    'low',
    'neutral',
    0.95,
    'Je veux mettre à jour mon adresse',
    'Bien sûr, je peux vous aider à mettre à jour votre adresse.',
    'crm_action',
    'update_address',
    '{"old_address": "123 Rue Paris", "new_address": "456 Av Champs-Élysées"}'::jsonb,
    TRUE,
    'completed'
);

-- Exemple 2 : Cas complexe Handoff
INSERT INTO callbot_interactions (
    customer_id,
    customer_name,
    customer_email,
    customer_phone,
    session_id,
    intent,
    urgency,
    emotion,
    confidence,
    customer_message,
    bot_response,
    action_taken,
    is_handoff,
    handoff_reason,
    handoff_queue,
    handoff_department,
    ticket_status,
    estimated_wait_seconds,
    status,
    priority
) VALUES (
    'CUST-002',
    'Marie Dubois',
    'marie.dubois@example.com',
    '+33687654321',
    'SESSION-002',
    'declare_claim',
    'high',
    'stressed',
    0.88,
    'Mon fils a eu un accident grave ! C''est urgent !',
    'Je comprends votre situation. Je vous mets en relation avec un agent spécialisé.',
    'human_handoff',
    TRUE,
    'Cas urgent - accident grave',
    'urgent',
    'sinistres',
    'pending',
    120,
    'in_progress',
    'high'
);

-- ==========================================
-- COMMENTAIRES
-- ==========================================

COMMENT ON TABLE callbot_interactions IS 'Table unique regroupant toutes les interactions du callbot';
COMMENT ON COLUMN callbot_interactions.conversation_history IS 'Historique complet en JSON [{turn: 1, speaker: "customer", text: "..."}]';
COMMENT ON COLUMN callbot_interactions.action_result IS 'Résultat de l''action en JSON';
COMMENT ON COLUMN callbot_interactions.crm_action_details IS 'Détails spécifiques de l''action CRM en JSON';
COMMENT ON COLUMN callbot_interactions.metadata IS 'Données additionnelles flexibles en JSON';

-- ==========================================
-- VÉRIFICATION
-- ==========================================

-- Compter le nombre de colonnes
SELECT COUNT(*) as nombre_colonnes
FROM information_schema.columns
WHERE table_name = 'callbot_interactions';

-- Afficher toutes les colonnes
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'callbot_interactions'
ORDER BY ordinal_position;

-- ==========================================
-- FIN DU SCHÉMA SIMPLIFIÉ
-- ==========================================
