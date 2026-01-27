"""
Script de démo DATABASE ONLY - Sans appeler OpenAI
Teste uniquement l'enregistrement dans la base de données
"""
import os
from dotenv import load_dotenv

# Charger .env
load_dotenv()

from src.database.db_service import db_service
from datetime import datetime
import uuid


def demo_interaction_simple():
    """Créer une interaction simple CRM"""
    print("\n" + "="*70)
    print("  DEMO 1: Création d'une interaction CRM simple")
    print("="*70)
    
    # 1. Créer l'interaction
    session_id = f"SESSION-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    interaction_id = db_service.create_interaction(
        customer_id="DEMO-CUST-001",
        session_id=session_id,
        intent="check_policy_status",
        urgency="low",
        emotion="neutral",
        confidence=0.92,
        action_taken="crm_action",
        priority="normal",
        reason="Client souhaite vérifier le statut de sa police"
    )
    
    print(f"✅ Interaction créée: {interaction_id}")
    
    # 2. Ajouter message client
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="customer",
        message_text="Bonjour, je voudrais vérifier le statut de ma police d'assurance",
        turn_number=1,
        detected_intent="check_policy_status",
        detected_emotion="neutral",
        confidence=0.92
    )
    
    print("✅ Message client enregistré")
    
    # 3. Logger action CRM
    db_service.log_crm_action(
        interaction_id=interaction_id,
        customer_id="DEMO-CUST-001",
        action_type="check_policy_status",
        input_data={"policy_id": "POL-12345"},
        output_data={"status": "active", "expiry_date": "2025-12-31"},
        success=True,
        execution_time_ms=150
    )
    
    print("✅ Action CRM loggée")
    
    # 4. Ajouter réponse agent
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="agent",
        message_text="Votre police d'assurance est active et valide jusqu'au 31 décembre 2025. Puis-je vous aider avec autre chose ?",
        turn_number=2
    )
    
    print("✅ Réponse agent enregistrée")
    
    # 5. Logger la réponse finale
    db_service.log_response(
        interaction_id=interaction_id,
        response_text="Votre police d'assurance est active et valide jusqu'au 31 décembre 2025. Puis-je vous aider avec autre chose ?",
        tone="professional",
        language="fr",
        confidence=0.92,
        generation_method="template",
        generation_time_ms=200
    )
    
    print("✅ Réponse finale loggée")
    
    # 6. Finaliser l'interaction
    db_service.update_interaction_status(
        interaction_id=interaction_id,
        status="completed"
    )
    
    print("✅ Interaction finalisée\n")
    
    return interaction_id


def demo_interaction_handoff():
    """Créer une interaction avec escalade humaine"""
    print("\n" + "="*70)
    print("  DEMO 2: Création d'une interaction avec HANDOFF")
    print("="*70)
    
    # 1. Créer l'interaction
    session_id = f"SESSION-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    interaction_id = db_service.create_interaction(
        customer_id="DEMO-CUST-002",
        session_id=session_id,
        intent="declare_claim",
        urgency="high",
        emotion="stressed",
        confidence=0.88,
        action_taken="human_handoff",
        priority="high",
        reason="Déclaration de sinistre urgent - accident grave"
    )
    
    print(f"✅ Interaction créée: {interaction_id}")
    
    # 2. Ajouter message client
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="customer",
        message_text="Bonjour, mon fils a eu un accident grave ! Je dois déclarer un sinistre immédiatement !",
        turn_number=1,
        detected_intent="declare_claim",
        detected_emotion="stressed",
        confidence=0.88
    )
    
    print("✅ Message client enregistré")
    
    # 3. Créer un ticket handoff
    ticket_id = db_service.create_handoff_ticket(
        interaction_id=interaction_id,
        customer_id="DEMO-CUST-002",
        queue_type="urgent",
        department="sinistres_graves",
        estimated_wait_time_seconds=180,
        context_summary="Client très stressé - fils victime d'accident grave - besoin intervention immédiate",
        key_information={
            "victim": "fils du client",
            "accident_type": "grave",
            "urgency": "high",
            "emotion": "stressed"
        },
        skills_required=["gestion_sinistres", "urgences", "empathie"]
    )
    
    print(f"✅ Ticket handoff créé: {ticket_id}")
    
    # 4. Ajouter réponse agent
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="agent",
        message_text="Je comprends votre situation et je vous assure que nous allons vous aider. Je vous transfère immédiatement vers un conseiller spécialisé en sinistres graves. Vous serez pris en charge dans les 3 prochaines minutes maximum.",
        turn_number=2
    )
    
    print("✅ Réponse agent enregistrée")
    
    # 5. Logger la réponse
    db_service.log_response(
        interaction_id=interaction_id,
        response_text="Je comprends votre situation et je vous assure que nous allons vous aider. Je vous transfère immédiatement vers un conseiller spécialisé en sinistres graves.",
        tone="empathetic",
        language="fr",
        confidence=0.88,
        generation_method="template",
        generation_time_ms=180
    )
    
    print("✅ Réponse finale loggée")
    
    # 6. Mettre à jour le statut
    db_service.update_interaction_status(
        interaction_id=interaction_id,
        status="in_progress"
    )
    
    print("✅ Interaction en cours de traitement\n")
    
    return interaction_id


def demo_interaction_with_failure():
    """Créer une interaction avec échec"""
    print("\n" + "="*70)
    print("  DEMO 3: Création d'une interaction avec ÉCHEC")
    print("="*70)
    
    # 1. Créer l'interaction
    session_id = f"SESSION-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    
    interaction_id = db_service.create_interaction(
        customer_id="DEMO-CUST-003",
        session_id=session_id,
        intent="update_payment_method",
        urgency="medium",
        emotion="neutral",
        confidence=0.85,
        action_taken="crm_action",
        priority="normal",
        reason="Client souhaite mettre à jour son moyen de paiement"
    )
    
    print(f"✅ Interaction créée: {interaction_id}")
    
    # 2. Ajouter message client
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="customer",
        message_text="Je veux changer ma carte bancaire pour les prélèvements",
        turn_number=1,
        detected_intent="update_payment_method",
        detected_emotion="neutral",
        confidence=0.85
    )
    
    print("✅ Message client enregistré")
    
    # 3. Logger action CRM avec échec
    db_service.log_crm_action(
        interaction_id=interaction_id,
        customer_id="DEMO-CUST-003",
        action_type="update_payment_method",
        input_data={"new_card_number": "****1234"},
        output_data={},
        success=False,
        error_message="Erreur de validation - carte expirée",
        execution_time_ms=120
    )
    
    print("❌ Action CRM échouée (carte expirée)")
    
    # 4. Ajouter réponse agent
    db_service.add_conversation_message(
        interaction_id=interaction_id,
        speaker="agent",
        message_text="Je suis désolé, mais je ne peux pas enregistrer cette carte car elle est expirée. Pourriez-vous fournir une autre carte bancaire valide ?",
        turn_number=2
    )
    
    print("✅ Réponse agent enregistrée")
    
    # 5. Finaliser avec échec
    db_service.update_interaction_status(
        interaction_id=interaction_id,
        status="failed"
    )
    
    print("❌ Interaction marquée comme échouée\n")
    
    return interaction_id


def view_all_data():
    """Afficher toutes les données créées"""
    print("\n" + "="*70)
    print("  📊 RÉSUMÉ DES DONNÉES DANS LA BASE")
    print("="*70)
    
    conn = db_service._get_connection()
    cursor = conn.cursor()
    
    # Compter interactions
    cursor.execute("SELECT COUNT(*) FROM callbot_interactions")
    total = cursor.fetchone()[0]
    
    # Par statut
    cursor.execute("""
        SELECT status, COUNT(*) 
        FROM callbot_interactions 
        GROUP BY status
    """)
    by_status = cursor.fetchall()
    
    # Par type d'action
    cursor.execute("""
        SELECT action_taken, COUNT(*) 
        FROM callbot_interactions 
        GROUP BY action_taken
    """)
    by_action = cursor.fetchall()
    
    print(f"\n📈 Total interactions : {total}")
    
    print(f"\n📊 Par statut :")
    for status, count in by_status:
        print(f"   {status:20} : {count}")
    
    print(f"\n⚙️  Par type d'action :")
    for action, count in by_action:
        print(f"   {action:20} : {count}")
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🗄️  DEMO DATABASE ONLY - Sans API OpenAI")
    print("="*70)
    print("\n💡 Ce script teste uniquement l'enregistrement en base de données")
    print("💡 Aucun appel à l'API OpenAI ne sera effectué\n")
    
    # Vérifier connexion
    print("🔍 Vérification de la connexion...")
    try:
        conn = db_service._get_connection()
        if conn:
            print("✅ Connexion PostgreSQL réussie!\n")
            conn.close()
        else:
            print("❌ Erreur de connexion\n")
            exit(1)
    except Exception as e:
        print(f"❌ Erreur: {e}\n")
        exit(1)
    
    # Exécuter les démos
    try:
        interaction_1 = demo_interaction_simple()
        input("[Appuyez sur Entrée pour continuer...]")
        
        interaction_2 = demo_interaction_handoff()
        input("[Appuyez sur Entrée pour continuer...]")
        
        interaction_3 = demo_interaction_with_failure()
        input("[Appuyez sur Entrée pour continuer...]")
        
        # Afficher résumé
        view_all_data()
        
        print("="*70)
        print("  ✅ DEMO TERMINÉE AVEC SUCCÈS")
        print("="*70)
        print("\n💡 Utilisez 'python view_database.py' pour voir toutes les données")
        print("💡 Ou consultez directement dans pgAdmin:\n")
        print("   SELECT * FROM callbot_interactions ORDER BY created_at DESC;\n")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant la démo: {e}\n")
