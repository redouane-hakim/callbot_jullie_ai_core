import os, json
from core.graph import build_app
from core.state import CoreState
from core.embedding import Embedder
from core.static import DEFAULT_EMBED_MODEL, DEFAULT_OLLAMA_MODEL

def main():
    # Switch modes:
    # - use_llm=True: uses Ollama LLM to output strict schema JSON
    # - use_llm=False: rules-only (fast deterministic fallback)
    use_llm = os.getenv("AI_CORE_USE_LLM", "true").lower() in ("1","true","yes")
    ollama_model = os.getenv("AI_CORE_OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)

    app = build_app(use_llm=use_llm, ollama_model=ollama_model)

    # For pipeline testing: if embedding isn't provided by upstream yet,
    # we compute it locally (optional).
    embedder = Embedder(model_name=os.getenv("AI_CORE_EMBED_MODEL", DEFAULT_EMBED_MODEL))

    text_query = "Bonjour, j'ai fait une chute et j'ai très mal au poignet, fracture possible."
    text_context = "Appel entrant - accidents de la vie. Client demande quoi faire."

    # In production you already get vector_embedding from upstream.
    vector = embedder.embed_768(text_context + "\n" + text_query)

    state = CoreState(text_query=text_query, text_context=text_context, vector_embedding=vector)

    out = app.invoke(state)
    decision = out["decision"]  
    print("DECISION JSON:")
    print(json.dumps(decision, ensure_ascii=False))
    # print("DEBUG:")
    # print(json.dumps(out.debug, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
