# Placeholder for ai_doc_summarizer/src/services/embedding_service.py
import os
import logging
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
import pinecone
from src.utils.helpers import load_config

logger = logging.getLogger("ai_summarizer.embedding_service")

class EmbeddingService:
    def __init__(self):
        cfg = load_config()
        pinecone_api_key = os.getenv("PINECONE_API_KEY") or cfg["pinecone"]["api_key"]
        pinecone_env = cfg["pinecone"]["environment"]
        self.index_name = cfg["pinecone"]["index_name"]

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        # If index doesn't exist, create it
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=1536, metric="cosine")
        self.client = pinecone.Index(self.index_name)
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def index_document(self, text: str):
        """
        Splits text into chunks, generates embeddings, and upserts into Pinecone.
        """
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        from langchain.docstore.document import Document
        docs = [Document(page_content=chunk) for chunk in splitter.split_text(text)]
        vectors = self.embeddings.embed_documents([doc.page_content for doc in docs])

        # Prepare upsert payload
        # Use hash of text-chunk as id, but here: sequential or UUID
        upserts = [(str(idx), vector) for idx, vector in enumerate(vectors)]
        self.client.upsert(vectors=upserts)
        logger.debug("Indexed %d chunks into Pinecone", len(vectors))

    def get_retriever(self):
        return Pinecone.from_existing_index(self.index_name, self.embeddings).as_retriever()
