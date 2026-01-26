# Static variables & base knowledge for AI Core.
# Keep this file "dumb": constants, regex lists, intent catalog.

ALLOWED_URGENCY = ("low", "med", "high")
ALLOWED_ACTION = ("rag_query", "escalate")

# Add/adjust intents here (10+ is fine).
# Keep IDs stable: frontend/backend will key off these strings.
INTENTS = (
    "claim_opening",
    "medical_docs",
    "status_followup",
    "beneficiary_info",
    "complaint",
    "unknown",
)

# Lightweight, deterministic prior knowledge (French keywords).
INTENT_KEYWORDS = {
    "claim_opening": [
        r"\bdéclar", r"\bdeclar", r"\bouvrir un dossier\b", r"\bsinistre\b", r"\baccident\b",
    ],
    "medical_docs": [
        r"\bcertificat\b", r"\bfacture\b", r"\barr[êe]t de travail\b", r"\bdocuments médicaux\b",
    ],
    "status_followup": [
        r"\bsuivi\b", r"\bavancement\b", r"\bstatut\b", r"\bdélais\b", r"\ben est où\b",
    ],
    "beneficiary_info": [
        r"\bgarantie\b", r"\bcouverture\b", r"\bcontrat\b", r"\bbénéficiaire\b",
    ],
    "complaint": [
        r"\bréclamation\b", r"\bmécontent\b", r"\blitige\b", r"\bcontestation\b",
    ],
}

# Urgency rules (hybrid rule+ML design: rules are cheap and reliable).
URG_HIGH = [
    r"\burgent\b", r"\burgence\b", r"\bh[ôo]pital\b", r"\bambulance\b",
    r"\bperte de connaissance\b", r"\bsang\b", r"\bgrave\b", r"\bfracture\b"
]
URG_MED = [
    r"\bdouleur\b", r"\bblessure\b", r"\bchute\b", r"\baccident\b",
    r"\barr[êe]t de travail\b", r"\btraumatisme\b"
]

# Default model names (override with env vars in prod)
DEFAULT_EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"  # 768-dim
DEFAULT_OLLAMA_MODEL = "llama3.2:1b-instruct"
