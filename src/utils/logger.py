# Placeholder for ai_doc_summarizer/src/utils/logger.py
import logging
import yaml
import os

def configure_logging():
    """
    Loads logging.yaml and configures logging.
    """
    log_cfg_path = os.path.abspath("config/logging.yaml")
    if os.path.exists(log_cfg_path):
        with open(log_cfg_path, 'r') as f:
            cfg = yaml.safe_load(f.read())
            logging.config.dictConfig(cfg)
    else:
        logging.basicConfig(level=logging.INFO)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
