from typing import Dict, Any
from data.Service import Service

service = Service()

def get_places(location: str, page: int = 1) -> Dict[str, Any]:
    """Returns all places from the database"""

    return service.get(
        "places",
        {
            "location": location,
            "page": page,
            "fields": "id,title,images,subway"
        }
    )

def get_place_detail(place_id: int) -> Dict[str, Any]:
    """Returns detailed location information"""

    return service.get(f"places/{place_id}")

def get_place_comments(place_id: int) -> Dict[str, Any]:
    """Returns comments to a place"""

    return service.get(f"places/{place_id}/comments")