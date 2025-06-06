# Placeholder for ai_doc_summarizer/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.api.server import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_summarize_endpoint(monkeypatch):
    sample_text = "This is a test document. It needs summarization."
    fake_summary = ["Test summary line."]
    # Patch RAGService to return fake summary
    class DummyRAG:
        def summarize_text(self, text):
            return fake_summary
    monkeypatch.setattr("src.api.routes.rag_service", DummyRAG())

    response = client.post("/summarize", json={"text": sample_text})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary"] == fake_summary
