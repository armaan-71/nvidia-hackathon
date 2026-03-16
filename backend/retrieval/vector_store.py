import chromadb
from typing import List, Dict, Any
from .embedder import NvidiaEmbedder

class VectorStoreManager:
    """
    Manages the ChromaDB instance for storing and retrieving document embeddings.
    """
    def __init__(self, collection_name: str = "scout_knowledge"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedder = NvidiaEmbedder()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[Dict[str, Any]]):
        """
        Embeds and adds chunks to the vector database.
        """
        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [f"{m['source']}_{m['chunk_id']}" for m in metadatas]
        
        # Get embeddings from NVIDIA NIM (using 'passage' for documents)
        embeddings = self.embedder.get_embeddings(texts, input_type="passage")
        
        if embeddings:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            return True
        return False

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Queries the vector store for the most relevant documents.
        """
        query_embeddings = self.embedder.get_embeddings([query_text], input_type="query")
        
        if not query_embeddings:
            return []

        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return formatted_results
