# Decision engine: merges retrieval + base knowledge + LLM (optional) into strict schema output.

from typing import Dict, Any, List
from .rules import score_urgency, keyword_intent_prior, confidence_from_retrieval
from .schema import validate_decision_schema

def retrieval_brief(retrieved: List[Dict[str, Any]], max_items: int = 2) -> str:
    if not retrieved:
        return "Aucun résultat."
    lines = []
    for h in retrieved[:max_items]:
        lines.append(f"- doc_id={h.get('doc_id')} score={h.get('score')} label_intent={h.get('label_intent')} snippet={str(h.get('snippet',''))[:160]}")
    return "\n".join(lines)

def decide_rules_only(text_query: str, text_context: str, retrieved: List[Dict[str, Any]]) -> Dict[str, Any]:
    combined = (text_context.strip() + "\n" + text_query.strip()).strip()
    urgency = score_urgency(combined)
    prior_intent, prior_strength = keyword_intent_prior(combined)

    top_intent = retrieved[0].get("label_intent") if retrieved else None
    top_score = float(retrieved[0].get("score", 0.0)) if retrieved else 0.0

    if top_intent and top_score >= 0.70:
        intent = str(top_intent)
    elif prior_intent != "unknown":
        intent = prior_intent
    else:
        intent = "unknown"

    conf = confidence_from_retrieval(retrieved, prior_strength)

    # action policy (tune later with feedback)
    action = "escalate" if (urgency == "high" or conf < 0.55 or intent == "unknown") else "rag_query"

    out = {"intent": intent, "urgency": urgency, "action": action, "confidence": round(conf, 3)}
    validate_decision_schema(out)
    return out
