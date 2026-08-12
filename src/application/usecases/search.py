from src.application.ports.repositories import SortKey
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import SearchPort
from src.domain.entities import SearchDocument


class Search(SearchPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

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
    ) -> tuple[list[SearchDocument], int]:
        async with self._uow:
            return await self._uow.search.search(
                query=query,
                category=category,
                city=city,
                min_price=min_price,
                max_price=max_price,
                sort=sort,
                limit=limit,
                offset=offset,
            )
