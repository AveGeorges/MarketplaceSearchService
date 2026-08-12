from typing import Annotated, Literal

from fastapi import APIRouter, Query

from src.presentation.api.dependencies import SearchDep, SuggestDep
from src.presentation.api.schemas import SearchHit, SearchResponse, SuggestResponse

router = APIRouter(prefix="/search", tags=["search"])

SortQuery = Annotated[
    Literal["date", "price_asc", "price_desc"] | None,
    Query(description="Сортировка"),
]


@router.get("")
async def search(
    usecase: SearchDep,
    q: str | None = Query(default=None, description="Поисковый запрос"),
    category: str | None = None,
    city: str | None = None,
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    sort: SortQuery = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> SearchResponse:
    docs, total = await usecase.execute(
        query=q,
        category=category,
        city=city,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        limit=limit,
        offset=offset,
    )
    return SearchResponse(
        items=[SearchHit.from_entity(d) for d in docs],
        total=total,
        query=q or "",
        limit=limit,
        offset=offset,
    )


@router.get("/suggest")
async def suggest(
    usecase: SuggestDep,
    q: str = Query(..., min_length=2, description="Начало запроса"),
    limit: int = Query(default=5, ge=1, le=10),
) -> SuggestResponse:
    suggestions = await usecase.execute(prefix=q, limit=limit)
    return SuggestResponse(suggestions=suggestions)
