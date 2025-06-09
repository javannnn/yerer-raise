import base64, requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .config import load_config

class ZoomClient:
    """Tiny wrapper around Zoom Dashboard API (Business plan)."""

    def __init__(self, cfg: Optional[dict] = None):
        self.cfg = cfg or load_config()
        self.access_token: Optional[str] = None
        self.expires: datetime = datetime.min

    # ── internal helpers ────────────────────────────────────────────────────
    def _encode(self) -> str:
        creds = f"{self.cfg['client_id']}:{self.cfg['client_secret']}"
        return base64.b64encode(creds.encode()).decode()

    def _refresh_token(self) -> None:
        url = (
            "https://zoom.us/oauth/token"
            f"?grant_type=account_credentials&account_id={self.cfg['account_id']}"
        )
        hdr = {"Authorization": f"Basic {self._encode()}"}
        data = requests.post(url, headers=hdr).json()
        self.access_token = data["access_token"]
        self.expires      = datetime.utcnow() + timedelta(seconds=data["expires_in"])

    def _ensure_token(self) -> None:
        if not self.access_token or datetime.utcnow() >= self.expires:
            self._refresh_token()

    # ── public API ───────────────────────────────────────────────
    def participants(self, meeting_id: str) -> List[Dict[str, str]]:
        """Return live participants list (names, ids, etc.)."""
        self._ensure_token()
        url = f"https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants"
        hdr = {"Authorization": f"Bearer {self.access_token}"}
        resp = requests.get(url, headers=hdr, params={"type": "live"}).json()
        return resp.get("participants", [])
