# Placeholder for ai_doc_summarizer/tests/test_rag_service.py
import pytest
from unittest.mock import patch, MagicMock
from src.services.rag_service import RAGService

def test_summarize_text_with_no_error(monkeypatch):
    # Prepare a fake retriever run
    class DummyEmbService:
        def index_document(self, text): pass
        def get_retriever(self): return MagicMock()

    class DummyLLM:
        def __call__(self, prompt): return "• Bullet 1\n• Bullet 2\n• Bullet 3"

    # Patch environment and dependencies
    monkeypatch.setenv("OPENAI_API_KEY", "fake_key")
    monkeypatch.setattr("src.services.rag_service.EmbeddingService", lambda *args, **kwargs: DummyEmbService())
    monkeypatch.setattr("langchain.llms.OpenAI", lambda *args, **kwargs: DummyLLM())

    rag = RAGService()
    bullets = rag.summarize_text("Some long text")
    assert isinstance(bullets, list)
    assert "Bullet 1" in bullets[0]
