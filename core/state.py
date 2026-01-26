from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class CoreState:
    text_query: str
    text_context: str
    vector_embedding: List[float]  # 768-dim expected
    retrieved: List[Dict[str, Any]] = field(default_factory=list)  # top-k retrieval hits
    decision: Optional[Dict[str, Any]] = None                     # strict schema decision JSON
    debug: Dict[str, Any] = field(default_factory=dict)           # traces for tests/demo
