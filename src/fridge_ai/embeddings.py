from functools import lru_cache

from fastembed import TextEmbedding

from fridge_ai.config import get_settings


@lru_cache
def get_embedding_model() -> TextEmbedding:
    settings = get_settings()
    return TextEmbedding(model_name=settings.embedding_model)


def create_embedding(text: str) -> list[float]:
    cleaned_text = " ".join(text.split())

    if not cleaned_text:
        raise ValueError("Text cannot be empty")

    embeddings = get_embedding_model().embed([cleaned_text])
    return next(embeddings).tolist()
