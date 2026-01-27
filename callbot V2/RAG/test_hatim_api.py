"""
✅ YOUR RAG API SPECIFICATION - HATIM'S MODULE
===============================================

📥 INPUT FORMAT YOU ACCEPT:
---------------------------
{
  "query": "declare accident domestique"
}

📤 OUTPUT FORMAT YOU PROVIDE:
------------------------------
{
  "documents": [
    "Question: Comment déclarer... Réponse: ...",
    "Procédure sinistre accident de la vie...",
    "Documents nécessaires..."
  ]
}


🔧 HOW TO USE YOUR MODULE:
---------------------------
"""

from rag_api import RAGKnowledgeBase
import json


# Example 1: Simple usage
def example_basic():
    print("="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Initialize your module
    rag = RAGKnowledgeBase()
    
    # Input format
    input_data = {"query": "comment accéder à mon espace client"}
    
    print("\n📥 INPUT:")
    print(json.dumps(input_data, indent=2, ensure_ascii=False))
    
    # Call your API
    output_data = rag.search(input_data["query"], k=3)
    
    print("\n📤 OUTPUT:")
    print(json.dumps({
        "documents": [doc[:100] + "..." for doc in output_data["documents"]]
    }, indent=2, ensure_ascii=False))
    print(f"\n✅ Retrieved {len(output_data['documents'])} documents")


# Example 2: Integration with other modules
def example_integration():
    print("\n" + "="*80)
    print("EXAMPLE 2: Integration with LLM")
    print("="*80)
    
    rag = RAGKnowledgeBase()
    
    # Step 1: User query arrives
    user_input = {"query": "faire un rachat"}
    print(f"\n1️⃣ User query: {user_input['query']}")
    
    # Step 2: YOUR module processes it
    print("\n2️⃣ YOUR RAG module searches...")
    rag_output = rag.search(user_input["query"], k=3)
    
    # Step 3: Output goes to LLM
    print(f"\n3️⃣ YOUR output: {len(rag_output['documents'])} documents found")
    print(f"   First document preview: {rag_output['documents'][0][:150]}...")
    
    # Step 4: LLM uses your documents
    print("\n4️⃣ LLM will use these documents to generate answer")
    print("   ✅ YOUR PART DONE!")


# Example 3: What others need to know
def integration_spec():
    print("\n" + "="*80)
    print("📋 WHAT OTHER DEVELOPERS NEED TO KNOW")
    print("="*80)
    
    spec = """
To use Hatim's RAG module:

1. Import the class:
   from rag_api import RAGKnowledgeBase

2. Initialize once:
   rag = RAGKnowledgeBase()

3. Call the search method:
   result = rag.search(query="your question", k=3)

4. You receive:
   {
     "documents": [
       "Document 1 content...",
       "Document 2 content...",
       "Document 3 content..."
     ]
   }

5. Use these documents as context for your LLM

Parameters:
- query (str): The user's question
- k (int): Number of documents to retrieve (default: 3)

Returns:
- dict with "documents" key containing list of relevant texts
"""
    print(spec)


if __name__ == "__main__":
    print("\n🎯 HATIM'S RAG MODULE - READY TO USE")
    print("\nTo test, run:")
    print("   from rag_api import RAGKnowledgeBase")
    print("   rag = RAGKnowledgeBase()")
    print('   result = rag.search("comment accéder à mon espace client")')
    print("   print(result)")
    
    integration_spec()
