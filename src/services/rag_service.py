# Placeholder for ai_doc_summarizer/src/services/rag_service.py
import os
import logging
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from src.services.embedding_service import EmbeddingService
from src.utils.helpers import load_config

logger = logging.getLogger("ai_summarizer.rag_service")

class RAGService:
    def __init__(self):
        cfg = load_config()
        openai_api_key = os.getenv("OPENAI_API_KEY") or cfg["openai"]["api_key"]
        self.openai = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.embedding_service = EmbeddingService()

    def summarize_text(self, text: str):
        """
        1) Ensure text is indexed in Pinecone
        2) Use RetrievalQA to generate a bullet-point summary
        """
        # Ensure embeddings exist
        self.embedding_service.index_document(text)
        retriever = self.embedding_service.get_retriever()

        qa = RetrievalQA.from_chain_type(
            llm=self.openai,
            retriever=retriever,
            chain_type="stuff"
        )
        prompt = "Summarize the document in 5 bullet points."
        try:
            result = qa.run(prompt)
            # Split into bullets if needed
            bullets = [line.strip() for line in result.split("\n") if line.strip()]
            logger.info("Generated summary with %d lines", len(bullets))
            return bullets
        except Exception as e:
            logger.error("RAG summarization failed: %s", e)
            # Fallback to local Hugging Face summarizer
            from src.models.base_model import BaseSummarizer
            fallback = BaseSummarizer()
            return fallback.summarize(text)
