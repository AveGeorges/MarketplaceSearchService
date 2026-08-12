from abc import ABC, abstractmethod

from src.application.ports.repositories import SortKey
from src.domain.entities import SearchDocument


class SearchPort(ABC):
    @abstractmethod
    async def execute(
        self,
        query: str | None,
        category: str | None,
        city: str | None,
        min_price: int | None,
        max_price: int | None,
        sort: SortKey | None,
        limit: int,
        offset: int,
    ) -> tuple[list[SearchDocument], int]: ...


class SuggestPort(ABC):
    @abstractmethod
    async def execute(
        self,
        prefix: str,
        limit: int,
    ) -> list[str]: ...


class IndexAdPort(ABC):
    @abstractmethod
    async def execute(
        self,
        ad_id: int,
    ) -> None: ...


class RemoveAdPort(ABC):
    @abstractmethod
    async def execute(
        self,
        ad_id: int,
    ) -> None: ...
