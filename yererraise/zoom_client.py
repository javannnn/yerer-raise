import base64
import requests
from datetime import datetime, timedelta
from typing import List, Dict


class ZoomClient:
    """Simple Zoom API client using OAuth."""

    def __init__(self, config: dict):
        self.config = config
        self.access_token = None
        self.token_expires_at = datetime.utcnow()

    def _encode_credentials(self) -> str:
        cid = self.config.get('client_id')
        secret = self.config.get('client_secret')
        credentials = f"{cid}:{secret}"
        return base64.b64encode(credentials.encode()).decode()

    def _fetch_access_token(self):
        token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={self.config['account_id']}"
        headers = {
            'Authorization': f'Basic {self._encode_credentials()}',
        }
        response = requests.post(token_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        self.access_token = data['access_token']
        self.token_expires_at = datetime.utcnow() + timedelta(seconds=data['expires_in'])

    def _ensure_token(self):
        if not self.access_token or datetime.utcnow() >= self.token_expires_at:
            self._fetch_access_token()

    def get_meeting_participants(self, meeting_id: str) -> List[Dict[str, str]]:
        """Fetch current meeting participants."""
        self._ensure_token()
        url = f"https://api.zoom.us/v2/metrics/meetings/{meeting_id}/participants"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }
        params = {'type': 'live'}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('participants', [])

