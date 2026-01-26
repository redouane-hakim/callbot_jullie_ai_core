# Prompts are isolated for easier iteration.
# This is designed for "JSON only" decision output.

from .static import INTENTS, ALLOWED_URGENCY, ALLOWED_ACTION

def decision_prompt(text_query: str, text_context: str, retrieval_brief: str) -> str:
    intents = ", ".join(INTENTS)
    urg = ", ".join(ALLOWED_URGENCY)
    act = ", ".join(ALLOWED_ACTION)

    # Keep prompt short to reduce latency.
    return f"""Tu es un moteur de décision pour un callbot d'assurance (accidents de la vie).
    Ta tâche: produire UNIQUEMENT un JSON valide selon le schéma EXACT ci-dessous.

    SCHÉMA JSON (clés exactes, aucune clé en plus):
    {{
      "intent": "<un des intents>",
      "urgency": "<low|med|high>",
      "action": "<rag_query|escalate>",
      "confidence": <float entre 0.0 et 1.0>
    }}

    INTENTS autorisés: {intents}
    URGENCY autorisés: {urg}
    ACTION autorisés: {act}

    RÈGLES:
    - Retourne seulement le JSON (pas de texte avant/après).
    - Si danger/urgence médicale probable -> urgency="high" et action="escalate".
    - Si confiance faible ou intent incertain -> action="escalate".
    - Sinon -> action="rag_query".

    CONTEXTE:
    {text_context}

    REQUÊTE CLIENT:
    {text_query}

    RÉSULTATS RETRIEVAL (top-k, peut aider):
    {retrieval_brief}

    JSON:
    """
