import logging
from typing import List, Dict, Any
from retrieval.vector_store import VectorStoreManager

logger = logging.getLogger(__name__)

class RetrieveContextTool:
    """
    Tool for agents to query the RAG vector store.
    Returns relevant nonprofit document chunks for grounding agent reasoning.
    """
    def __init__(self):
        self.vector_store = VectorStoreManager()
        logger.info("RetrieveContextTool initialized with ChromaDB.")

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the vector store for the most relevant document chunks.
        Returns a list of {text, metadata, distance} dicts.
        """
        logger.info(f"Retrieving context for: '{query[:80]}...'")
        results = self.vector_store.query(query, n_results=n_results)
        logger.info(f"Retrieved {len(results)} chunks from vector store.")
        return results

    def retrieve_as_text(self, query: str, n_results: int = 3) -> str:
        """
        Returns retrieved chunks as a single formatted string,
        ready to be injected into an LLM prompt.
        """
        results = self.retrieve(query, n_results=n_results)
        if not results:
            return "No relevant documents found in the knowledge base."

        context_parts = []
        for i, r in enumerate(results, 1):
            source = r.get("metadata", {}).get("source", "unknown")
            context_parts.append(f"--- Document Chunk {i} (Source: {source}) ---\n{r['text']}")

        return "\n\n".join(context_parts)
