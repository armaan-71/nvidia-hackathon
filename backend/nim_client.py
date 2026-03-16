from openai import OpenAI
from typing import Generator, Optional
from config import get_settings

settings = get_settings()

_client = OpenAI(
    api_key=settings.nvidia_api_key or "no-key-yet",
    base_url=settings.nim_base_url,
)


def chat(messages: list[dict], model: Optional[str] = None, **kwargs) -> str:
    """Single-turn chat completion. Returns the response text."""
    target_model = model or settings.primary_model
    try:
        response = _client.chat.completions.create(
            model=target_model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content
    except Exception as e:
        if target_model == settings.primary_model:
            response = _client.chat.completions.create(
                model=settings.fallback_model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content
        raise e


def chat_stream(messages: list[dict], model: Optional[str] = None, **kwargs) -> Generator[str, None, None]:
    """Streaming chat completion. Yields text chunks as they arrive."""
    target_model = model or settings.primary_model
    stream = _client.chat.completions.create(
        model=target_model,
        messages=messages,
        stream=True,
        **kwargs,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            yield delta


def embed(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings. Returns a list of float vectors."""
    response = _client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
        encoding_format="float",
    )
    return [item.embedding for item in response.data]
