from typing import Dict, Any
from data.Service import Service

service = Service()

def get_news(page: int = 1) -> Dict[str, Any]:
    """Returns all news from the database"""

    return service.get(
        "news",
        {
            "page": page,
            "fields": "id,title,images,publication_date"
         }
    )

def get_news_detail(news_id: int) -> Dict[str, Any]:
    """Returns detailed information of the news"""

    return service.get(f"news/{news_id}")

def get_news_comments(news_id: int) -> Dict[str, Any]:
    """Returns comments to the news"""

    return service.get(f"news/{news_id}/comments")