import os
import logging
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from potential locations
load_dotenv() # Load from CWD
load_dotenv(os.path.join(os.getcwd(), "backend", ".env")) # Load from backend/ if running from root

class NvidiaEmbedder:
    """
    Handles connections to NVIDIA NIM for generating vector embeddings.
    Model: nvidia/nv-embedqa-e5-v5
    """
    def __init__(self):
        settings = get_settings()
        self.api_key = os.getenv("NVIDIA_API_KEY") or settings.nvidia_api_key
        self.base_url = settings.nim_base_url
        self.model = settings.embedding_model
        
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables or config. Please set it in your .env file.")
        
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
            logger.info(f"Requesting embeddings for {len(texts)} chunks (type: {input_type})...")
            response = self.client.embeddings.create(
                input=texts,
                model=self.model,
                extra_body={"input_type": input_type, "truncate": "NONE"}
            )
            logger.info(f"NIM Response Status: Successfully generated {len(response.data)} embeddings.")
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"!!! Error fetching embeddings from NIM: {e}")
            # If it's an API error, print the response content if possible
            if hasattr(e, 'response'):
                logger.error(f"API Response: {e.response.text}")
            return []

if __name__ == "__main__":
    # Quick test
    embedder = NvidiaEmbedder()
    test_text = ["This is a test of the Scout RAG pipeline."]
    embeddings = embedder.get_embeddings(test_text)
    if embeddings:
        print(f"Successfully retrieved embedding of length: {len(embeddings[0])}")
