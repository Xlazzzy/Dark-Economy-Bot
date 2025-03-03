import requests
from typing import Any, Dict, Optional


class Service:
    BASE_URL = "https://kudago.com/public-api/v1.4"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Connects to the server API and returns data"""

        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()