from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import SearchPort, SuggestPort
from src.application.usecases.search import Search
from src.application.usecases.suggest import Suggest
from src.infrastructure.persistence.uow import SQLAlchemyUnitOfWork
from src.settings import Settings

_settings: Settings | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def setup(
    settings: Settings,
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    global _settings, _session_factory
    _settings = settings
    _session_factory = session_factory


def get_settings() -> Settings:
    assert _settings is not None
    return _settings


def get_uow() -> UnitOfWork:
    assert _session_factory is not None
    return SQLAlchemyUnitOfWork(_session_factory)


SettingsDep = Annotated[Settings, Depends(get_settings)]
UowDep = Annotated[UnitOfWork, Depends(get_uow)]


def get_search(uow: UowDep) -> SearchPort:
    return Search(uow)


def get_suggest(uow: UowDep) -> SuggestPort:
    return Suggest(uow)


SearchDep = Annotated[SearchPort, Depends(get_search)]
SuggestDep = Annotated[SuggestPort, Depends(get_suggest)]
