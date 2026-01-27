"""
Test Database Connection - Vérifie que la base de données est correctement configurée
"""
import os
from dotenv import load_dotenv

# ⚠️ IMPORTANT: Charger variables d'environnement AVANT d'importer db_service
load_dotenv()

from src.database.db_service import db_service


def test_connection():
    """Test la connexion à la base de données"""
    print("\n" + "="*60)
    print("  TEST DE CONNEXION À LA BASE DE DONNÉES")
    print("="*60)
    
    # Récupérer DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("\n❌ ERREUR: DATABASE_URL non trouvé dans .env")
        print("📝 Conseil: Créez un fichier .env avec DATABASE_URL")
        print("   Exemple: DATABASE_URL=postgresql://user:pass@localhost:5432/callbot_db")
        return False
    
    # Masquer le mot de passe dans l'affichage
    safe_url = db_url.replace(db_url.split(':')[2].split('@')[0], '****')
    print(f"\n📡 DATABASE_URL trouvé: {safe_url}")
    
    # Test de connexion
    print("\n🔍 Tentative de connexion...")
    try:
        conn = db_service._get_connection()
        if conn:
            print("✅ Connexion réussie!")
            
            # Test d'une requête simple
            print("\n🔍 Test d'une requête...")
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print(f"✅ PostgreSQL version: {version.split(',')[0]}")
                
                # Vérifier les tables
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                
                if tables:
                    print(f"\n✅ Tables trouvées ({len(tables)}):")
                    expected_tables = ['callbot_interactions']  # Architecture simplifiée
                    for table in tables:
                        table_name = table[0]
                        status = "✅" if table_name in expected_tables else "⚠️"
                        print(f"   {status} {table_name}")
                    
                    # Vérifier si la table unique est présente
                    found_tables = [t[0] for t in tables]
                    if 'callbot_interactions' in found_tables:
                        print("\n✅ Table unique callbot_interactions présente!")
                    else:
                        print("\n⚠️  Table callbot_interactions manquante!")
                        print("📝 Conseil: Exécutez database_schema_simple.sql")
                        print("   psql -U callbot_user -d callbot_db -f database_schema_simple.sql")
                else:
                    print("\n⚠️  Aucune table trouvée!")
                    print("📝 Conseil: Exécutez le script database_schema.sql")
                    print("   psql -U callbot_user -d callbot_db -f database_schema.sql")
            
            conn.close()
            print("\n" + "="*60)
            print("  ✅ TEST RÉUSSI - Base de données opérationnelle!")
            print("="*60)
            return True
            
        else:
            print("❌ La connexion a échoué (conn = None)")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR DE CONNEXION: {e}")
        print("\n📝 Vérifications à faire:")
        print("   1. PostgreSQL est-il démarré?")
        print("      → Windows: Services → postgresql")
        print("   2. DATABASE_URL est-il correct dans .env?")
        print("   3. L'utilisateur et la base existent-ils?")
        print("      → psql -U postgres -c '\\du'")
        print("      → psql -U postgres -c '\\l'")
        print("   4. Le mot de passe est-il correct?")
        return False


def test_crud_operations():
    """Test les opérations CRUD de base"""
    print("\n" + "="*60)
    print("  TEST DES OPÉRATIONS CRUD")
    print("="*60)
    
    try:
        # 1. CREATE - Créer une interaction
        print("\n1️⃣ Test CREATE - Création d'une interaction...")
        interaction_id = db_service.create_interaction(
            customer_id="TEST-CUST-001",
            session_id="TEST-SESSION-001",
            intent="test_connection",
            urgency="low",
            emotion="neutral",
            confidence=0.95,
            action_taken="automated_response",
            priority="normal",
            reason="Test de connexion base de données"
        )
        print(f"   ✅ Interaction créée: {interaction_id}")
        
        # 2. READ - Lire l'interaction
        print("\n2️⃣ Test READ - Lecture de l'interaction...")
        interaction = db_service.get_interaction(interaction_id)
        if interaction:
            print(f"   ✅ Interaction lue: {interaction.get('customer_id')}")
        else:
            print("   ❌ Échec lecture")
            return False
        
        # 3. UPDATE - Mettre à jour le statut
        print("\n3️⃣ Test UPDATE - Mise à jour du statut...")
        db_service.update_interaction_status(
            interaction_id,
            "completed",
            "test_agent"
        )
        updated = db_service.get_interaction(interaction_id)
        if updated.get('status') == 'completed':
            print(f"   ✅ Statut mis à jour: {updated.get('status')}")
        else:
            print("   ❌ Échec mise à jour")
            return False
        
        # 4. Ajouter un message
        print("\n4️⃣ Test INSERT - Ajout d'un message...")
        db_service.add_conversation_message(
            interaction_id=interaction_id,
            speaker="customer",
            message_text="Test message de connexion à la base de données",
            turn_number=1,
            detected_intent="test_connection",
            detected_emotion="neutral",
            confidence=0.95
        )
        messages = db_service.get_conversation_history(interaction_id)
        if messages and len(messages) > 0:
            print(f"   ✅ Message ajouté: {len(messages)} message(s)")
        else:
            print("   ❌ Échec ajout message")
            return False
        
        # 5. Logger une action CRM
        print("\n5️⃣ Test LOG - Log d'action CRM...")
        db_service.log_crm_action(
            interaction_id=interaction_id,
            customer_id="TEST-CUST-001",
            action_type="test_action",
            input_data={"test": "input"},
            output_data={"test": "output"},
            success=True,
            execution_time_ms=100
        )
        print("   ✅ Action CRM loggée")
        
        # 6. Créer un ticket handoff
        print("\n6️⃣ Test HANDOFF - Création ticket...")
        ticket_id = db_service.create_handoff_ticket(
            interaction_id=interaction_id,
            customer_id="TEST-CUST-001",
            queue_type="test_queue",
            department="test_department",
            estimated_wait_time_seconds=300,
            context_summary="Test escalation pour vérification connexion DB",
            key_information={"test": True, "connection": "ok"}
        )
        print(f"   ✅ Ticket créé: {ticket_id}")
        
        # 7. Logger une réponse
        print("\n7️⃣ Test RESPONSE - Log de réponse...")
        db_service.log_response(
            interaction_id=interaction_id,
            response_text="Test response",
            tone="professional",
            language="fr",
            confidence=0.95,
            generation_method="template",
            generation_time_ms=200
        )
        print("   ✅ Réponse loggée")
        
        print("\n" + "="*60)
        print("  ✅ TOUS LES TESTS CRUD RÉUSSIS!")
        print("="*60)
        print(f"\n💡 Interaction de test créée: {interaction_id}")
        print("   Vous pouvez la consulter dans la base:")
        print(f"   SELECT * FROM interactions WHERE interaction_id = '{interaction_id}';")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CRUD: {e}")
        return False


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("  🗄️  TEST DE LA BASE DE DONNÉES UNIFIÉE - CNP CALLBOT")
    print("="*70)
    
    # Test 1: Connexion
    if not test_connection():
        print("\n❌ Test de connexion échoué. Arrêt.")
        return
    
    # Demander si l'utilisateur veut tester les CRUD
    print("\n" + "-"*60)
    response = input("\n❓ Voulez-vous tester les opérations CRUD? (o/n): ").strip().lower()
    
    if response == 'o':
        test_crud_operations()
    else:
        print("\n✅ Test de connexion terminé avec succès!")
    
    print("\n" + "="*70)
    print("  🎉 TESTS TERMINÉS")
    print("="*70)
    print("\n💡 Prochaine étape: Exécutez demo_with_database.py pour voir le système complet!")


if __name__ == "__main__":
    main()
