import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load configuration from JSON file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy config.sample.json to config.json and fill it in."
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
