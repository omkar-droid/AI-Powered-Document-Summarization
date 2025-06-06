# Placeholder for ai_doc_summarizer/src/api/server.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings
from src.api.routes import router
from src.utils.logger import configure_logging

configure_logging()  # Initialize logging early

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

settings = Settings()

app = FastAPI(title="AI Document Summarizer API")
app.include_router(router, prefix="/", tags=["summarization"])

def run_api():
    uvicorn.run("src.api.server:app", host=settings.host, port=settings.port, reload=settings.reload)
