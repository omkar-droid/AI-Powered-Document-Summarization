# Placeholder for ai_doc_summarizer/src/schemas/document_schema.py
from pydantic import BaseModel
from typing import List, Optional

class DocumentMessage(BaseModel):
    doc_id: str
    text: str

class DocumentInput(BaseModel):
    text: str

class SummaryOutput(BaseModel):
    summary: List[str]
