import pytest

from src.application.usecases.index_ad import IndexAd
from src.application.usecases.suggest import Suggest
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


@pytest.mark.asyncio
async def test_suggest_returns_prefix_matches(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    for ad_id, title in enumerate(["MacBook Pro", "MacBook Air", "BMW X5"], start=1):
        fake_ad_source.set(make_snapshot(ad_id=ad_id, title=title))
        await IndexAd(fake_uow, fake_ad_source).execute(ad_id)

    result = await Suggest(fake_uow).execute(prefix="Mac", limit=5)

    assert result == ["MacBook Air", "MacBook Pro"]


@pytest.mark.asyncio
async def test_suggest_respects_limit(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    for ad_id, title in enumerate(["Apple 1", "Apple 2", "Apple 3"], start=1):
        fake_ad_source.set(make_snapshot(ad_id=ad_id, title=title))
        await IndexAd(fake_uow, fake_ad_source).execute(ad_id)

    result = await Suggest(fake_uow).execute(prefix="Apple", limit=2)

    assert len(result) == 2
