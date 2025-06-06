# Placeholder for ai_doc_summarizer/tests/test_ingestion.py
import pytest
from unittest.mock import patch, MagicMock
from src.ingestion.kafka_consumer import run_consumer

@pytest.mark.asyncio
async def test_run_consumer_no_messages(monkeypatch):
    """
    If Kafka has no messages, consumer should not crash.
    We patch KafkaConsumer to yield nothing.
    """
    class DummyConsumer:
        def __iter__(self):
            return iter([])

    monkeypatch.setattr("src.ingestion.kafka_consumer.KafkaConsumer", lambda *args, **kwargs: DummyConsumer())
    # We also patch RAGService so actual summarization isn't invoked
    with patch("src.ingestion.kafka_consumer.RAGService") as MockRAG, \
         patch("src.ingestion.kafka_consumer.CacheService") as MockCache, \
         patch("src.ingestion.kafka_consumer.CassandraClient") as MockDB:
        # Should complete without errors
        await run_consumer()
