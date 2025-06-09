import json
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load JSON config (Zoom OAuth creds)."""
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy config.sample.json \u2794 config.json "
            "and fill in your Zoom account_id / client_id / client_secret."
        )
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)
