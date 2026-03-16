import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from potential locations
load_dotenv() # Load from CWD
load_dotenv(os.path.join(os.getcwd(), "backend", ".env")) # Load from backend/ if running from root

class NvidiaEmbedder:
    """
    Handles connections to NVIDIA NIM for generating vector embeddings.
    Model: nvidia/nv-embedqa-e5-v5
    """
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "nvidia/nv-embedqa-e5-v5"
        
        if not self.api_key:
            print("Warning: NVIDIA_API_KEY not found in environment variables.")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def get_embeddings(self, texts: List[str], input_type: str = "passage") -> List[List[float]]:
        """
        Retrieves embeddings from NVIDIA NIM.
        input_type: "query" or "passage" (NIM expects 'passage' for documents)
        """
        # The nv-embedqa-e5-v5 model expects type prefixes or specific formatting usually
        # but the NIM API handles this if configured via the OpenAI-compatible endpoint.
        try:
            print(f"Requesting embeddings for {len(texts)} chunks (type: {input_type})...")
            response = self.client.embeddings.create(
                input=texts,
                model=self.model,
                extra_body={"input_type": input_type, "truncate": "NONE"}
            )
            print(f"NIM Response Status: Successfully generated {len(response.data)} embeddings.")
            return [data.embedding for data in response.data]
        except Exception as e:
            print(f"!!! Error fetching embeddings from NIM: {e}")
            # If it's an API error, print the response content if possible
            if hasattr(e, 'response'):
                print(f"API Response: {e.response.text}")
            return []

if __name__ == "__main__":
    # Quick test
    embedder = NvidiaEmbedder()
    test_text = ["This is a test of the Scout RAG pipeline."]
    embeddings = embedder.get_embeddings(test_text)
    if embeddings:
        print(f"Successfully retrieved embedding of length: {len(embeddings[0])}")
