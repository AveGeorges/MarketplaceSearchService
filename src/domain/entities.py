from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchDocument:
    id: int
    ad_id: int
    title: str
    description: str
    price: int
    category: str
    city: str
    indexed_at: datetime
