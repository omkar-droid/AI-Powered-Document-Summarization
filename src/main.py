# Placeholder for ai_doc_summarizer/src/main.py
import argparse
import asyncio
from src.api.server import run_api
from src.ingestion.kafka_consumer import run_consumer

def main():
    parser = argparse.ArgumentParser(
        description="AI Document Summarizer: CLI entrypoint"
    )
    parser.add_argument(
        "--mode",
        choices=["api", "consumer"],
        default="api",
        help="Choose 'api' to run FastAPI server or 'consumer' to run Kafka consumer."
    )
    args = parser.parse_args()

    if args.mode == "api":
        run_api()
    elif args.mode == "consumer":
        asyncio.run(run_consumer())

if __name__ == "__main__":
    main()
