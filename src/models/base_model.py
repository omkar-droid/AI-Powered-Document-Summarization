# Placeholder for ai_doc_summarizer/src/models/base_model.py
from transformers import pipeline
import logging

logger = logging.getLogger("ai_summarizer.base_model")

class BaseSummarizer:
    """
    Fallback summarization using Hugging Face transformers
    (e.g., facebook/bart-large-cnn).
    """
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text: str):
        try:
            result = self.summarizer(text, max_length=150, min_length=40, do_sample=False)
            summary_text = result[0]["summary_text"]
            return [s.strip() for s in summary_text.split(".") if s.strip()]
        except Exception as e:
            logger.error("Local summarization failed: %s", e)
            return ["Error: Unable to summarize locally."]
