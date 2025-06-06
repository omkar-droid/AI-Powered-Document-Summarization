# Placeholder for ai_doc_summarizer/src/utils/helpers.py
import yaml
import os

def load_config() -> dict:
    """
    Loads config/config.yaml into a Python dict.
    """
    cfg_path = os.path.abspath("config/config.yaml")
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"Config file not found: {cfg_path}")
    with open(cfg_path, 'r') as f:
        return yaml.safe_load(f)
