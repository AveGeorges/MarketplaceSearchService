from pydantic import BaseModel

from src.domain.entities import SearchDocument


class SearchHit(BaseModel):
    ad_id: int
    title: str
    description: str
    price: int
    category: str
    city: str

    @classmethod
    def from_entity(cls, doc: SearchDocument) -> "SearchHit":
        return cls(
            ad_id=doc.ad_id,
            title=doc.title,
            description=doc.description,
            price=doc.price,
            category=doc.category,
            city=doc.city,
        )


class SearchResponse(BaseModel):
    items: list[SearchHit]
    total: int
    query: str
    limit: int
    offset: int


class SuggestResponse(BaseModel):
    suggestions: list[str]
