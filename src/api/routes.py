# Placeholder for ai_doc_summarizer/src/api/routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from src.schemas.document_schema import DocumentInput, SummaryOutput
from src.services.rag_service import RAGService
from src.services.cache_service import CacheService
from src.storage.cassandra_client import CassandraClient

router = APIRouter()

# Initialize services
rag_service = RAGService()
cache = CacheService()
db_client = CassandraClient()

class SummarizeRequest(BaseModel):
    text: str

@router.post("/summarize", response_model=SummaryOutput)
async def summarize(req: SummarizeRequest):
    # Check cache first
    cache_key = f"summary:{hash(req.text)}"
    cached = cache.get(cache_key)
    if cached:
        return SummaryOutput(summary=cached)

    # Run RAG pipeline
    summary = rag_service.summarize_text(req.text)

    # Store in Cassandra (for later analytics)
    db_client.insert_summary(req.text, summary)

    # Cache result (e.g. 1 hour)
    cache.set(cache_key, summary, expire=3600)

    return SummaryOutput(summary=summary)

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
