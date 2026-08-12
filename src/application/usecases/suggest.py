from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import SuggestPort


class Suggest(SuggestPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        prefix: str,
        limit: int,
    ) -> list[str]:
        async with self._uow:
            return await self._uow.search.suggest(prefix=prefix, limit=limit)
