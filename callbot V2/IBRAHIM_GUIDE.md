# 📝 GUIDE PERSONNEL - IBRAHIM

## 🎯 Votre Mission

Vous êtes responsable de **2 composants critiques** du Callbot Julie :

### 1. Tool Router (Routeur d'Actions)
**Rôle** : Décider intelligemment où envoyer chaque requête

**Responsabilités** :
- ✅ Analyser l'urgence et le type de demande
- ✅ Router vers CRM pour les opérations simples
- ✅ Escalader vers humains pour les cas complexes/urgents
- ✅ Garantir la bonne priorisation

### 2. Response Builder (Générateur de Réponses)
**Rôle** : Créer des réponses naturelles et empathiques

**Responsabilités** :
- ✅ Générer des réponses adaptées au contexte
- ✅ Adapter le ton selon l'émotion du client
- ✅ Utiliser la knowledge base efficacement
- ✅ Déléguer au Tools Router quand nécessaire

---

## 📂 Fichiers Créés pour Vous

### Structure Complète

```
callbot V1/
│
├── 📄 README.md                          ✅ Documentation principale
├── 📄 QUICKSTART.md                      ✅ Guide de démarrage rapide
├── 📄 requirements.txt                   ✅ Dépendances Python
├── 📄 pyproject.toml                     ✅ Configuration pytest
├── 📄 setup.ps1                          ✅ Script d'installation
├── 📄 demo.py                            ✅ Démonstration visuelle
├── 📄 .env.example                       ✅ Template configuration
├── 📄 .gitignore                         ✅ Git ignore
│
├── 📁 src/
│   ├── 📄 __init__.py                    ✅ Package init
│   ├── 📄 main.py                        ✅ Point d'entrée principal
│   ├── 📄 api.py                         ✅ API FastAPI
│   ├── 📄 schemas.py                     ✅ Modèles de données
│   │
│   ├── 📁 agents/
│   │   ├── 📄 __init__.py                ✅ Package init
│   │   ├── 📄 crm_agent.py               ✅ Agent CRM
│   │   └── 📄 human_handoff_agent.py     ✅ Agent escalade
│   │
│   ├── 📁 routers/
│   │   ├── 📄 __init__.py                ✅ Package init
│   │   └── 📄 tools_router.py            ✅ Routeur principal
│   │
│   └── 📁 teams/
│       ├── 📄 __init__.py                ✅ Package init
│       └── 📄 response_builder.py        ✅ Générateur de réponses
│
└── 📁 tests/
    ├── 📄 __init__.py                    ✅ Package init
    ├── 📄 test_tools_router.py           ✅ Tests routeur
    ├── 📄 test_response_builder.py       ✅ Tests générateur
    └── 📄 test_integration.py            ✅ Tests intégration
```

---

## 🚀 Comment Démarrer (Étape par Étape)

### Étape 1 : Installation

```powershell
# Option A : Script automatique
.\setup.ps1

# Option B : Manuel
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Étape 2 : Configuration

```powershell
# Copier le template
Copy-Item .env.example .env

# Éditer .env et ajouter votre clé OpenAI
# OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### Étape 3 : Tester

```powershell
# Option 1 : Démo visuelle (recommandé pour commencer)
python demo.py

# Option 2 : Script de test
python src/main.py

# Option 3 : API
python src/api.py
# Puis ouvrir : http://localhost:8000/docs

# Option 4 : Tests unitaires
pytest tests/ -v
```

---

## 🔑 Concepts Clés à Comprendre

### 1. Framework Agno

**C'est quoi ?** Un framework pour créer des systèmes multi-agents

**Pourquoi ?** Permet de :
- Créer des agents avec des rôles spécifiques
- Les organiser en équipes (Team)
- Utiliser le pattern Router pour délégation intelligente

**Exemple** :
```python
from agno.agent import Agent
from agno.team import Team

# Agent simple
agent = Agent(
    name="CRM Agent",
    role="Gérer les opérations CRM",
    tools=[update_address, check_policy]
)

# Équipe avec pattern Router
team = Team(
    name="Tools Router",
    members=[crm_agent, handoff_agent],
    respond_directly=True  # Pattern Router
)
```

### 2. Pattern Router

**C'est quoi ?** Un pattern où l'équipe route directement vers un membre sans synthèse

**Configuration** :
```python
tools_router = Team(
    respond_directly=True,      # Active le pattern Router
    determine_input_for_members=False
)
```

**Avantage** : Réponse directe de l'agent choisi (pas de reformulation)

### 3. Schémas Pydantic

**C'est quoi ?** Des modèles de données avec validation automatique

**Exemple** :
```python
class IntentData(BaseModel):
    intent: IntentType
    urgency: UrgencyLevel
    confidence: float = Field(ge=0.0, le=1.0)
```

**Avantage** : Validation automatique + documentation API

---

## 🔄 Flux de Traitement

```
1. CLIENT
   ↓ (appel vocal)

2. ABDELLAH : Speech-to-Text + Emotion Analysis
   ↓ (text + emotion)

3. REDOUANE : AI Core (Intent Detection)
   ↓ (intent + urgency + confidence)

4. HATIM : Knowledge Base (RAG)
   ↓ (documents pertinents)

5. VOUS (IBRAHIM) : Tool Router
   ↓ (décision de routage)

6. VOUS (IBRAHIM) : Response Builder
   ↓ (réponse générée)

7. TTS : Text-to-Speech
   ↓ (audio)

8. CLIENT
```

---

## 💡 Exemples d'Utilisation

### Exemple 1 : Génération de Réponse Simple

```python
from src.teams.response_builder import generate_response

response = generate_response(
    intent="general_info",
    urgency="low",
    emotion="neutral",
    confidence=0.95,
    text="Quels sont vos horaires ?",
    documents=[{
        "title": "Horaires",
        "content": "Lundi-Vendredi 9h-18h"
    }]
)

print(response)
# Output: "Nos conseillers sont disponibles du lundi au vendredi..."
```

### Exemple 2 : Routage Urgent

```python
from src.routers.tools_router import route_request

response = route_request(
    intent="declare_claim",
    urgency="high",
    emotion="stressed",
    confidence=0.91,
    text="Accident grave, besoin d'aide"
)

# Va automatiquement :
# 1. Identifier l'urgence
# 2. Router vers Human Handoff Agent
# 3. Créer un ticket d'escalade
# 4. Retourner une réponse empathique
```

### Exemple 3 : API Request

```bash
curl -X POST "http://localhost:8000/api/generate-response" \
  -H "Content-Type: application/json" \
  -d '{
    "intent_data": {
      "intent": "update_info",
      "urgency": "medium",
      "confidence": 0.88,
      "emotion": "neutral",
      "text": "Je veux changer mon adresse"
    }
  }'
```

---

## 🛠️ Personnalisation

### Modifier les Règles de Routage

**Fichier** : `src/routers/tools_router.py`

```python
# Ajouter une nouvelle règle
if intent == "custom_intent":
    return self._create_decision(
        action=ActionType.CUSTOM_ACTION,
        reason="custom_reason",
        priority="medium"
    )
```

### Ajouter un Nouvel Outil CRM

**Fichier** : `src/agents/crm_agent.py`

```python
@tool
def new_crm_function(customer_id: str, param: str) -> Dict:
    """Description de la fonction"""
    # Votre logique ici
    return {"success": True, "data": {...}}

# Ajouter au agent
crm_agent = Agent(
    tools=[..., new_crm_function]
)
```

### Modifier le Ton des Réponses

**Fichier** : `src/teams/response_builder.py`

Modifiez les instructions dans :
```python
response_builder = Team(
    instructions=[
        "Ajouter vos instructions personnalisées ici",
        "Exemple: Utilise un ton plus formel",
        ...
    ]
)
```

---

## 🐛 Dépannage Rapide

### Problème : Module 'agno' not found

```powershell
pip install agno
# ou
pip install -r requirements.txt
```

### Problème : OpenAI API error

```powershell
# Vérifier que .env existe et contient
OPENAI_API_KEY=sk-proj-xxxxx
```

### Problème : Tests échouent

```powershell
# Réinstaller les dépendances
pip install -r requirements.txt

# Vérifier la structure
pytest tests/ -v
```

### Problème : Import errors

```powershell
# Ajouter le répertoire au PYTHONPATH
$env:PYTHONPATH = "c:\Users\IBRAHIM NASSIH\Documents\VSCode\callbot V1"
```

---

## 📊 KPIs à Suivre

### Métriques Techniques
- ⏱️ Temps de réponse < 3s
- 🎯 Précision de routage > 95%
- 📈 Taux d'automatisation = 90%
- ✅ Disponibilité > 99%

### Métriques Métier
- 😊 Satisfaction client > 4.5/5
- 📞 Appels escaladés < 10%
- ⚡ Résolution au premier contact > 85%
- 💰 Réduction coûts opérationnels

---

## 📚 Ressources

### Documentation
- **Agno Framework** : https://agno.dev/docs
- **FastAPI** : https://fastapi.tiangolo.com
- **OpenAI API** : https://platform.openai.com/docs

### Fichiers Importants
- `README.md` : Documentation complète
- `QUICKSTART.md` : Guide rapide
- `src/schemas.py` : Tous les modèles de données
- `src/api.py` : Endpoints API

### Commandes Utiles

```powershell
# Démarrer l'environnement
.\venv\Scripts\Activate.ps1

# Lancer la démo
python demo.py

# Tester l'API
python src/api.py

# Exécuter les tests
pytest tests/ -v

# Voir la couverture
pytest tests/ --cov=src --cov-report=html

# Linter
pylint src/

# Format
black src/
```

---

## ✅ Checklist de Complétion

### Phase 1 : Setup
- [ ] Installation complète
- [ ] Configuration .env
- [ ] Tests passent
- [ ] Démo fonctionne

### Phase 2 : Compréhension
- [ ] Architecture comprise
- [ ] Pattern Router maîtrisé
- [ ] Flux de données clair
- [ ] Interfaces définies

### Phase 3 : Développement
- [ ] Tool Router opérationnel
- [ ] Response Builder fonctionnel
- [ ] CRM Agent configuré
- [ ] Human Handoff Agent prêt

### Phase 4 : Intégration
- [ ] API testée
- [ ] Intégration avec autres composants
- [ ] Monitoring en place
- [ ] Documentation à jour

### Phase 5 : Production
- [ ] Tests de charge
- [ ] KPIs surveillés
- [ ] Feedback utilisateurs
- [ ] Optimisations appliquées

---

## 🎓 Prochaines Actions

1. **Aujourd'hui** :
   - ✅ Installer le projet
   - ✅ Lancer la démo
   - ✅ Comprendre l'architecture

2. **Cette Semaine** :
   - 📝 Personnaliser les règles de routage
   - 📝 Tester avec des cas réels
   - 📝 Intégrer avec composants upstream

3. **Semaine Prochaine** :
   - 🚀 Déploiement en environnement de test
   - 📊 Monitoring et métriques
   - 🔄 Itérations basées sur feedback

---

**Bon développement ! 💪**

*En cas de question, référez-vous à QUICKSTART.md ou README.md*
