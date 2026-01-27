"""
🔍 DEBUG SCRIPT - Check actual distances and scores
"""

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from rag_api import RAGKnowledgeBase

# Initialize RAG
rag = RAGKnowledgeBase()

# Test query
query = "comment accéder à mon espace client"

print(f"\n{'='*80}")
print(f"🔍 Testing query: \"{query}\"")
print('='*80)

# Get results with metadata
result = rag.search_with_metadata(query, k=5)

print(f"\n📊 Found {len(result['documents'])} documents:")
print(f"⏱️  Response time: {result['response_time_ms']}ms\n")

for i, doc in enumerate(result['documents'], 1):
    print(f"\n📄 Document {i}:")
    print(f"   ID: {doc['id']}")
    print(f"   Section: {doc['section']}")
    print(f"   Relevance Score: {doc['relevance_score']:.4f}")
    print(f"   Content preview: {doc['content'][:150]}...")
    print()

print('='*80)
