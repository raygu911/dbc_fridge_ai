import pytest

from fridge_ai.embeddings import create_embedding


def test_empty_text_cannot_be_embedded() -> None:
    with pytest.raises(ValueError, match="Text cannot be empty"):
        create_embedding("   ")


