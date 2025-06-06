# Placeholder for ai_doc_summarizer/src/ingestion/kafka_consumer.py
import asyncio
import json
import logging
from kafka import KafkaConsumer
from src.schemas.document_schema import DocumentMessage
from src.services.rag_service import RAGService
from src.services.cache_service import CacheService
from src.storage.cassandra_client import CassandraClient
from src.utils.helpers import load_config

logger = logging.getLogger("ai_summarizer.ingestion")

async def run_consumer():
    cfg = load_config()
    kafka_servers = cfg["kafka"]["bootstrap_servers"]
    topic = cfg["kafka"]["topic"]

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda b: json.loads(b.decode("utf-8"))
    )
    rag_service = RAGService()
    cache = CacheService()
    db_client = CassandraClient()

    logger.info(f"Listening to Kafka topic: {topic}")
    for message in consumer:
        try:
            doc_msg = DocumentMessage(**message.value)
            text = doc_msg.text
            doc_id = doc_msg.doc_id
            logger.debug(f"Consumed message for doc_id={doc_id}")

            # Summarize
            summary = rag_service.summarize_text(text)

            # Store in Cassandra
            db_client.insert_summary_id(doc_id, text, summary)

            # Cache
            cache_key = f"summary:{doc_id}"
            cache.set(cache_key, summary, expire=3600)
            logger.info(f"Summary stored for doc_id={doc_id}")

        except Exception as e:
            logger.error(f"Error processing Kafka message: {e}")

    await asyncio.sleep(0)  # keep loop alive if needed
