# Retrieval interface (MOCK today).
# Replace `retrieve()` with teammate's FAISS implementation later.
#
# IMPORTANT: You requested no RAG installs here.
# So this file has NO faiss dependency, and the real retrieval snippet is kept as comments.

from typing import Any, Dict, List

def retrieve(vector_embedding_768: List[float], k: int = 3) -> List[Dict[str, Any]]:
    """Mock retrieval output.

    Expected output format (top-k):
      [
        {"doc_id": "D1", "score": 0.82, "label_intent": "claim_opening", "snippet": "...."},
        ...
      ]

    score should be normalized to ~[0,1], higher=better.
    label_intent is optional but very helpful for latency (lets AI Core skip extra reasoning).
    """
    # MOCK - replace with real retrieval later
    return [
        {"doc_id": "D1", "score": 0.82, "label_intent": "claim_opening", "snippet": "Déclarer un accident de la vie..."},
        {"doc_id": "D3", "score": 0.61, "label_intent": "status_followup", "snippet": "Suivi de dossier sinistre..."},
        {"doc_id": "D2", "score": 0.56, "label_intent": "medical_docs", "snippet": "Envoyer certificat, arrêt de travail..."},
    ]

    # ----------------------------
    # REAL FAISS (comment-only):
    # ----------------------------
    # import numpy as np
    # import faiss
    # q = np.array([vector_embedding_768], dtype="float32")
    # scores, idxs = faiss_index.search(q, k)  # your teammate builds faiss_index + KB_DOCS
    # hits = []
    # for score, idx in zip(scores[0], idxs[0]):
    #     doc = KB_DOCS[idx]
    #     hits.append({
    #        "doc_id": doc.id,
    #        "score": float(score),
    #        "label_intent": getattr(doc, "intent", None),
    #        "snippet": getattr(doc, "snippet", "")[:200],
    #     })
    # return hits
