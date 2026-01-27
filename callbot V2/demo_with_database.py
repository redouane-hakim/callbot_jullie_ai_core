"""
Example Script - Démontre l'utilisation complète du système avec base de données unifiée
"""
import os
from dotenv import load_dotenv

# ⚠️ IMPORTANT: Charger .env AVANT les imports du système
load_dotenv()

from src.routers.tools_router import route_request
from src.teams.response_builder import generate_response
from src.database.db_service import db_service


def example_1_simple_crm_query():
    """Exemple 1: Requête CRM simple - Consultation de police"""
    print("\n" + "="*60)
    print("EXEMPLE 1: Consultation de police (CRM)")
    print("="*60)
    
    # Simuler l'input du client
    customer_text = "Je voudrais vérifier le statut de ma police d'assurance"
    customer_id = "CUST-001"
    
    # Router la requête (crée interaction en BDD)
    result = route_request(
        intent="check_policy_status",
        urgency="low",
        emotion="neutral",
        confidence=0.92,
        text=customer_text,
        customer_id=customer_id
    )
    
    print(f"\n✅ Interaction créée: {result['interaction_id']}")
    print(f"\n🤖 Réponse de l'agent:\n{result['response']}")
    
    # Générer réponse finale via Response Builder
    final_response = generate_response(
        intent="check_policy_status",
        urgency="low",
        emotion="neutral",
        confidence=0.92,
        text=customer_text,
        customer_id=customer_id,
        interaction_id=result['interaction_id']
    )
    
    print(f"\n📝 Réponse finale (Response Builder):")
    print(f"   Texte: {final_response['response']}")
    print(f"   Ton: {final_response['tone']}")
    print(f"   Temps: {final_response['execution_time_ms']}ms")
    
    return result['interaction_id']


def example_2_urgent_handoff():
    """Exemple 2: Escalade urgente vers agent humain"""
    print("\n" + "="*60)
    print("EXEMPLE 2: Déclaration de sinistre urgente (HANDOFF)")
    print("="*60)
    
    customer_text = "Je dois déclarer un accident grave, c'est urgent!"
    customer_id = "CUST-002"
    
    # Router la requête
    result = route_request(
        intent="declare_claim",
        urgency="high",
        emotion="stressed",
        confidence=0.88,
        text=customer_text,
        customer_id=customer_id
    )
    
    print(f"\n✅ Interaction créée: {result['interaction_id']}")
    print(f"\n🚨 Escalade vers agent humain:")
    print(f"{result['response']}")
    
    # Générer réponse empathique
    final_response = generate_response(
        intent="declare_claim",
        urgency="high",
        emotion="stressed",
        confidence=0.88,
        text=customer_text,
        customer_id=customer_id,
        interaction_id=result['interaction_id']
    )
    
    print(f"\n📝 Réponse empathique:")
    print(f"   Texte: {final_response['response']}")
    print(f"   Ton: {final_response['tone']}")
    
    return result['interaction_id']


def example_3_crm_update():
    """Exemple 3: Mise à jour CRM (adresse)"""
    print("\n" + "="*60)
    print("EXEMPLE 3: Mise à jour d'adresse (CRM)")
    print("="*60)
    
    customer_text = "Je veux changer mon adresse, j'ai déménagé"
    customer_id = "CUST-001"
    
    result = route_request(
        intent="update_info",
        urgency="low",
        emotion="neutral",
        confidence=0.95,
        text=customer_text,
        customer_id=customer_id
    )
    
    print(f"\n✅ Interaction créée: {result['interaction_id']}")
    print(f"\n🔄 Mise à jour CRM:")
    print(f"{result['response']}")
    
    return result['interaction_id']


def view_interaction_history(interaction_id: str):
    """Afficher l'historique complet d'une interaction"""
    print("\n" + "="*60)
    print(f"HISTORIQUE DE L'INTERACTION: {interaction_id}")
    print("="*60)
    
    try:
        # Récupérer l'interaction
        interaction = db_service.get_interaction(interaction_id)
        if interaction:
            print(f"\n📊 Détails de l'interaction:")
            print(f"   Client: {interaction.get('customer_id')}")
            print(f"   Canal: {interaction.get('channel')}")
            print(f"   Intent: {interaction.get('intent')}")
            print(f"   Émotion: {interaction.get('emotion')}")
            print(f"   Urgence: {interaction.get('urgency')}")
            print(f"   Statut: {interaction.get('status')}")
            print(f"   Agent assigné: {interaction.get('assigned_agent')}")
            
            # Récupérer l'historique de conversation
            messages = db_service.get_conversation_history(interaction_id)
            if messages:
                print(f"\n💬 Historique de conversation ({len(messages)} messages):")
                for msg in messages:
                    speaker = msg.get('speaker', 'unknown')
                    message = msg.get('message', '')
                    print(f"   [{speaker.upper()}]: {message[:100]}...")
        else:
            print(f"❌ Interaction {interaction_id} non trouvée")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")


def view_daily_metrics():
    """Afficher les métriques du jour"""
    print("\n" + "="*60)
    print("MÉTRIQUES QUOTIDIENNES")
    print("="*60)
    
    try:
        metrics = db_service.get_daily_metrics()
        if metrics:
            for metric in metrics[:5]:  # Derniers 5 jours
                print(f"\n📈 Date: {metric.get('metric_date')}")
                print(f"   Total interactions: {metric.get('total_interactions')}")
                print(f"   Complétées: {metric.get('completed_interactions')}")
                print(f"   Échouées: {metric.get('failed_interactions')}")
                print(f"   Temps moyen résolution: {metric.get('avg_resolution_seconds')}s")
                print(f"   Clients uniques: {metric.get('unique_customers')}")
        else:
            print("Aucune métrique disponible")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    """Fonction principale - Exécute tous les exemples"""
    print("\n" + "="*70)
    print("  CNP ASSURANCES CALLBOT - DÉMONSTRATION BASE DE DONNÉES UNIFIÉE  ")
    print("="*70)
    
    # Vérifier connexion BDD
    print("\n🔍 Vérification de la connexion à la base de données...")
    try:
        conn = db_service._get_connection()
        if conn:
            print("✅ Connexion à la base de données réussie!")
            conn.close()
        else:
            print("❌ Échec de connexion à la base de données")
            print("⚠️  Assurez-vous que PostgreSQL est démarré et que DATABASE_URL est configuré dans .env")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("⚠️  Conseil: Exécutez d'abord 'database_schema.sql' pour créer les tables")
        return
    
    # Exemples
    print("\n📚 Exécution des exemples...\n")
    
    # Exemple 1: CRM simple
    interaction_1 = example_1_simple_crm_query()
    input("\n[Appuyez sur Entrée pour continuer...]")
    
    # Exemple 2: Handoff urgent
    interaction_2 = example_2_urgent_handoff()
    input("\n[Appuyez sur Entrée pour continuer...]")
    
    # Exemple 3: Mise à jour CRM
    interaction_3 = example_3_crm_update()
    input("\n[Appuyez sur Entrée pour continuer...]")
    
    # Afficher historique
    if interaction_1:
        view_interaction_history(interaction_1)
        input("\n[Appuyez sur Entrée pour continuer...]")
    
    # Afficher métriques
    view_daily_metrics()
    
    print("\n" + "="*70)
    print("  ✅ DÉMONSTRATION TERMINÉE  ")
    print("="*70)
    print("\n💡 Toutes les interactions sont stockées dans la base de données unifiée!")
    print("💡 Vous pouvez consulter les tables: interactions, conversation_messages,")
    print("   crm_actions, handoff_tickets, response_logs")


if __name__ == "__main__":
    main()
