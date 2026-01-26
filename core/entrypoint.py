from typing import Dict, Any, List
from core.graph import build_app
from core.state import CoreState

_APP = build_app(use_llm=True)

def run_ai_core(text_query: str, text_context: str, vector_embedding) -> Dict[str, Any]:
    if hasattr(vector_embedding, "tolist"):
        vector_embedding = vector_embedding.tolist()

    state = CoreState(
        text_query=text_query,
        text_context=text_context,
        vector_embedding=vector_embedding
    )
    out = _APP.invoke(state)      
    return out["decision"]

def warmup():
    dummy = [0.0] * 768
    run_ai_core("ping", "warmup", dummy)

