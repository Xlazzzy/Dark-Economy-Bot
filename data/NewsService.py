from typing import Dict, Any
from data.Service import Service

service = Service()

def get_news(page: int = 1) -> Dict[str, Any]:
    return service.get(
        "news",
        {
            "page": page,
            "fields": "id,title,images,publication_date"
         }
    )

def get_news_detail(news_id: int) -> Dict[str, Any]:
    return service.get(f"news/{news_id}")

def get_news_comments(news_id: int) -> Dict[str, Any]:
    return service.get(f"news/{news_id}/comments")