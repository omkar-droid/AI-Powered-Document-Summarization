# Placeholder for ai_doc_summarizer/src/pipelines/summarizer_pipeline.py
from src.services.embedding_service import EmbeddingService
from src.services.rag_service import RAGService
from src.utils.logger import get_logger

logger = get_logger("summarizer_pipeline")

class SummarizerPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.rag_service = RAGService()

    def run(self, text: str):
        """
        1) Embed document into Pinecone index (if not already).
        2) Use RAGService to retrieve and summarize.
        """
        logger.debug("Starting pipeline for text of length %d", len(text))
        # Step 1: index embeddings
        self.embedding_service.index_document(text)
        # Step 2: run RAG summarization
        summary = self.rag_service.summarize_text(text)
        return summary
