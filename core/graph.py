# LangGraph orchestration of the AI Core.
# Nodes: preprocess -> retrieve -> decide -> (optional feedback stub)

from typing import Any, Dict
from langgraph.graph import StateGraph, END

from .state import CoreState
from .retrieval import retrieve
from .decision_engine import decide_rules_only, retrieval_brief
from .prompts import decision_prompt
from .llm_ollama import OllamaDecisionLLM
from .static import DEFAULT_OLLAMA_MODEL

def node_preprocess(state: CoreState) -> CoreState:
    combined = (state.text_context.strip() + "\n" + state.text_query.strip()).strip()
    state.debug["combined_text"] = combined
    if len(state.vector_embedding) != 768:
        state.debug["warning"] = f"Expected 768-dim embedding, got {len(state.vector_embedding)}"
    return state

def node_retrieve(state: CoreState) -> CoreState:
    state.retrieved = retrieve(state.vector_embedding, k=3)
    state.debug["retrieved_n"] = len(state.retrieved)
    return state

def node_decide(state: CoreState) -> CoreState:
    # Version 1 (submission-safe): rules-only is fastest + deterministic.
    decision = decide_rules_only(state.text_query, state.text_context, state.retrieved)
    state.decision = decision
    state.debug["mode"] = "rules_only"
    return state

def node_decide_with_llm(state: CoreState, llm: OllamaDecisionLLM) -> CoreState:
    # Optional: LLM finalizer (still validates schema strictly)
    brief = retrieval_brief(state.retrieved)
    prompt = decision_prompt(state.text_query, state.text_context, brief)
    decision = llm.decide_json(prompt)
    state.decision = decision
    state.debug["mode"] = "ollama_llm"
    return state

def node_feedback_stub(state: CoreState) -> CoreState:
    # Placeholder: store after-call rating later.
    state.debug["feedback_placeholder"] = {
        "store": {
            "decision": state.decision,
            "retrieved_top": state.retrieved[:1],
            "advisor_rating": None
        }
    }
    return state

def build_app(use_llm: bool = True, ollama_model: str = DEFAULT_OLLAMA_MODEL) -> Any:
    g = StateGraph(CoreState)
    g.add_node("preprocess", node_preprocess)
    g.add_node("retrieve", node_retrieve)

    if use_llm:
        llm = OllamaDecisionLLM(model=ollama_model)
        g.add_node("decide", lambda s: node_decide_with_llm(s, llm))
    else:
        g.add_node("decide", node_decide)

    g.add_node("feedback", node_feedback_stub)

    g.set_entry_point("preprocess")
    g.add_edge("preprocess", "retrieve")
    g.add_edge("retrieve", "decide")
    g.add_edge("decide", "feedback")
    g.add_edge("feedback", END)

    return g.compile()
