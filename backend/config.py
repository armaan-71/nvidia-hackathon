from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # NVIDIA NIM
    nvidia_api_key: str = ""
    nim_base_url: str = "https://integrate.api.nvidia.com/v1"

    # Models (swap to ultra once you have credits for it)
    primary_model: str = "nvidia/llama-3.1-nemotron-nano-8b-v1"
    fallback_model: str = "nvidia/llama-3.1-nemotron-ultra-253b-v1"
    embedding_model: str = "nvidia/nv-embedqa-e5-v5"

    # Chroma
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "scout_docs"

    # App
    cors_origins: List[str] = ["http://localhost:3000"]
    max_upload_size_mb: int = 20

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
