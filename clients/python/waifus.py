"""
Official Python SDK for Waifu Database API (https://wafus.vercel.app)
Supports synchronous and asynchronous requests with typing.
"""

from typing import Dict, Any, Optional, List
import requests

DEFAULT_BASE_URL = "https://wafus.vercel.app"

class WaifuClient:
    """Synchronous Client for Waifu Database API."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

    def get_api_key(self) -> Dict[str, Any]:
        """Generate/fetch an API key."""
        resp = self.session.get(f"{self.base_url}/")
        resp.raise_for_status()
        data = resp.json()
        if "api_key" in data:
            self.api_key = data["api_key"]
            self.session.headers.update({"x-api-key": self.api_key})
        return data

    def ping(self) -> Dict[str, Any]:
        """Health check ping."""
        resp = self.session.get(f"{self.base_url}/Ping")
        resp.raise_for_status()
        return resp.json()

    def stats(self) -> Dict[str, Any]:
        """Get database statistics (total records, collection name)."""
        resp = self.session.get(f"{self.base_url}/Stats")
        resp.raise_for_status()
        return resp.json()

    def random(self) -> Dict[str, Any]:
        """Roll and get a random waifu with image URL and metadata."""
        resp = self.session.get(f"{self.base_url}/Random")
        resp.raise_for_status()
        return resp.json()

    def find_by_name(self, name: str) -> Dict[str, Any]:
        """Search waifu by character name."""
        resp = self.session.get(f"{self.base_url}/Find", params={"name": name})
        resp.raise_for_status()
        return resp.json()

    def find_by_id(self, waifu_id: str) -> Dict[str, Any]:
        """Find waifu by unique ID."""
        resp = self.session.get(f"{self.base_url}/FindById/{waifu_id}")
        resp.raise_for_status()
        return resp.json()

    def list(self, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get paginated list of waifus."""
        resp = self.session.get(f"{self.base_url}/List", params={"skip": skip, "limit": limit})
        resp.raise_for_status()
        return resp.json()

    def add_waifu(self, name: str, img_url: str, added_by: str, rarity: str = "Common", event_tag: str = "Standard", source_message_id: int = 0) -> Dict[str, Any]:
        """Add a new waifu (Requires API Key)."""
        payload = {
            "name": name,
            "img_url": img_url,
            "added_by": added_by,
            "rarity": rarity,
            "event_tag": event_tag,
            "source_message_id": source_message_id
        }
        resp = self.session.post(f"{self.base_url}/Waifuadd", json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_waifu(self, name: str, **fields) -> Dict[str, Any]:
        """Update an existing waifu (Requires API Key)."""
        resp = self.session.put(f"{self.base_url}/Update", params={"name": name}, json=fields)
        resp.raise_for_status()
        return resp.json()

    def remove_waifu(self, name: str) -> Dict[str, Any]:
        """Delete a waifu by name (Requires API Key)."""
        resp = self.session.delete(f"{self.base_url}/Rmwafus", params={"name": name})
        resp.raise_for_status()
        return resp.json()

    def remove_by_id(self, waifu_id: str) -> Dict[str, Any]:
        """Delete a waifu by ID (Requires API Key)."""
        resp = self.session.delete(f"{self.base_url}/RmById/{waifu_id}")
        resp.raise_for_status()
        return resp.json()
