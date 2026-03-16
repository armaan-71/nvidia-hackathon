import os
from typing import List, Dict
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title

class DocumentProcessor:
    """
    Handles text extraction and chunking of documents using the Unstructured library.
    """
    def __init__(self):
        pass

    def process_file(self, file_path: str) -> List[Dict[str, str]]:
        """
        Partitions and chunks a document into a list of text segments with metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Try partitioning with unstructured
        try:
            elements = partition(filename=file_path)
            # Chunk elements by title/section
            chunks = chunk_by_title(
                elements,
                max_characters=1000,
                new_after_n_chars=800
            )
            
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                processed_chunks.append({
                    "text": str(chunk),
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "chunk_id": i,
                        "type": "document_segment"
                    }
                })
            return processed_chunks

        except Exception as e:
            print(f"Unstructured partitioning failed, falling back to simple text read: {e}")
            # Simple fallback for text-based files
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple chunking by paragraph/newlines
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            
            processed_chunks = []
            for i, p in enumerate(paragraphs):
                processed_chunks.append({
                    "text": p,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "chunk_id": i,
                        "type": "text_fallback_segment"
                    }
                })
            return processed_chunks

if __name__ == "__main__":
    # Test with a dummy file if needed
    processor = DocumentProcessor()
    print("DocumentProcessor initialized.")
