from abc import ABC, abstractmethod
from typing import List, Literal

from src.domain.entities import SearchDocument

SortKey = Literal["date", "price_asc", "price_desc"]


class SearchRepository(ABC):
    @abstractmethod
    async def upsert(
        self,
        ad_id: int,
        title: str,
        description: str,
        price: int,
        category: str,
        city: str,
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        ad_id: int,
    ) -> None: ...

    @abstractmethod
    async def search(
        self,
        query: str | None,
        category: str | None,
        city: str | None,
        min_price: int | None,
        max_price: int | None,
        sort: SortKey | None,
        limit: int,
        offset: int,
    ) -> tuple[List[SearchDocument], int]: ...

    @abstractmethod
    async def suggest(
        self,
        prefix: str,
        limit: int,
    ) -> list[str]: ...
