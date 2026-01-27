"""
Script pour visualiser toutes les données de la base callbot_interactions
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# Charger .env
load_dotenv()

def connect_db():
    """Connexion PostgreSQL"""
    return psycopg2.connect(
        os.getenv('DATABASE_URL'),
        cursor_factory=RealDictCursor
    )

def view_all_interactions():
    """Afficher toutes les interactions"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Compter total
    cursor.execute("SELECT COUNT(*) as total FROM callbot_interactions")
    total = cursor.fetchone()['total']
    
    print(f"\n{'='*100}")
    print(f"📊 BASE DE DONNÉES CALLBOT - Total : {total} interaction(s)")
    print(f"{'='*100}\n")
    
    # Récupérer toutes les interactions
    cursor.execute("""
        SELECT 
            interaction_id,
            created_at,
            customer_id,
            session_id,
            intent,
            urgency,
            emotion,
            confidence,
            customer_message,
            bot_response,
            action_taken,
            action_type,
            success,
            is_handoff,
            handoff_reason,
            assigned_agent,
            ticket_status,
            status,
            priority,
            resolved_at,
            resolution_time_seconds
        FROM callbot_interactions 
        ORDER BY created_at DESC
    """)
    
    interactions = cursor.fetchall()
    
    if not interactions:
        print("ℹ️  Aucune interaction dans la base de données.\n")
        return
    
    for idx, inter in enumerate(interactions, 1):
        print(f"\n{'─'*100}")
        print(f"#{idx} - 🆔 {inter['interaction_id']}")
        print(f"{'─'*100}")
        
        print(f"📅 Créé : {inter['created_at']}")
        print(f"👤 Client : {inter['customer_id']}")
        print(f"🔗 Session : {inter['session_id']}")
        
        print(f"\n🎯 ANALYSE")
        print(f"   Intent    : {inter['intent']}")
        print(f"   Urgence   : {inter['urgency']}")
        print(f"   Émotion   : {inter['emotion']}")
        print(f"   Confiance : {inter['confidence']}")
        
        if inter['customer_message']:
            print(f"\n💬 MESSAGE CLIENT")
            msg = inter['customer_message']
            print(f"   {msg[:150]}{'...' if len(msg) > 150 else ''}")
        
        if inter['bot_response']:
            print(f"\n🤖 RÉPONSE BOT")
            resp = inter['bot_response']
            print(f"   {resp[:150]}{'...' if len(resp) > 150 else ''}")
        
        print(f"\n⚙️  ACTION")
        print(f"   Type      : {inter['action_taken']}")
        if inter['action_type']:
            print(f"   Détail    : {inter['action_type']}")
        print(f"   Succès    : {'✅ Oui' if inter['success'] else '❌ Non'}")
        
        if inter['is_handoff']:
            print(f"\n🎫 HANDOFF")
            print(f"   Raison        : {inter['handoff_reason']}")
            print(f"   Statut ticket : {inter['ticket_status']}")
            if inter['assigned_agent']:
                print(f"   Agent assigné : {inter['assigned_agent']}")
        
        print(f"\n📊 STATUT")
        print(f"   État     : {inter['status']}")
        print(f"   Priorité : {inter['priority']}")
        
        if inter['resolved_at']:
            print(f"   Résolu   : {inter['resolved_at']}")
            if inter['resolution_time_seconds']:
                minutes = inter['resolution_time_seconds'] // 60
                seconds = inter['resolution_time_seconds'] % 60
                print(f"   Durée    : {minutes}m {seconds}s")
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*100}")
    print(f"✅ Affichage terminé - {total} interaction(s)")
    print(f"{'='*100}\n")

def view_statistics():
    """Afficher des statistiques"""
    conn = connect_db()
    cursor = conn.cursor()
    
    print(f"\n{'='*80}")
    print(f"📈 STATISTIQUES")
    print(f"{'='*80}")
    
    # Stats globales
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN is_handoff THEN 1 ELSE 0 END) as handoffs,
            SUM(CASE WHEN success THEN 1 ELSE 0 END) as success_count,
            AVG(confidence) as avg_confidence
        FROM callbot_interactions
    """)
    
    stats = cursor.fetchone()
    
    print(f"\n📊 Résumé Global")
    print(f"   Total interactions : {stats['total']}")
    print(f"   Handoffs          : {stats['handoffs']}")
    print(f"   Succès            : {stats['success_count']}")
    if stats['avg_confidence']:
        print(f"   Confiance moyenne : {stats['avg_confidence']:.2f}")
    
    # Stats par intent
    cursor.execute("""
        SELECT 
            intent,
            COUNT(*) as count
        FROM callbot_interactions
        GROUP BY intent
        ORDER BY count DESC
    """)
    
    intents = cursor.fetchall()
    
    if intents:
        print(f"\n🎯 Par Intent")
        for intent_stat in intents:
            print(f"   {intent_stat['intent']:30} : {intent_stat['count']:3} interaction(s)")
    
    # Stats par statut
    cursor.execute("""
        SELECT 
            status,
            COUNT(*) as count
        FROM callbot_interactions
        GROUP BY status
        ORDER BY count DESC
    """)
    
    statuses = cursor.fetchall()
    
    if statuses:
        print(f"\n📊 Par Statut")
        for status_stat in statuses:
            print(f"   {status_stat['status']:20} : {status_stat['count']:3} interaction(s)")
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*80}\n")

def view_conversation_history(interaction_id: str):
    """Voir l'historique de conversation d'une interaction"""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT conversation_history
        FROM callbot_interactions
        WHERE interaction_id = %s
    """, (interaction_id,))
    
    row = cursor.fetchone()
    
    if not row or not row['conversation_history']:
        print(f"❌ Aucun historique trouvé pour {interaction_id}")
        return
    
    print(f"\n{'='*80}")
    print(f"💬 HISTORIQUE CONVERSATION - {interaction_id}")
    print(f"{'='*80}\n")
    
    history = row['conversation_history']
    
    for msg in history:
        speaker = msg.get('speaker', 'unknown')
        text = msg.get('message_text', '')
        timestamp = msg.get('timestamp', '')
        
        icon = "👤" if speaker == "customer" else "🤖"
        print(f"{icon} {speaker.upper()} ({timestamp})")
        print(f"   {text}\n")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("\n🚀 Visualisation Base de Données Callbot\n")
    
    # Menu
    print("Choisissez une option :")
    print("1. Voir toutes les interactions")
    print("2. Voir les statistiques")
    print("3. Voir l'historique d'une conversation")
    print("4. Tout afficher")
    
    choice = input("\nVotre choix (1-4) : ").strip()
    
    if choice == "1":
        view_all_interactions()
    elif choice == "2":
        view_statistics()
    elif choice == "3":
        interaction_id = input("ID de l'interaction : ").strip()
        view_conversation_history(interaction_id)
    elif choice == "4":
        view_statistics()
        view_all_interactions()
    else:
        print("❌ Choix invalide")
