import pytest

from src.application.usecases.index_ad import IndexAd
from src.application.usecases.remove_ad import RemoveAd
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


@pytest.mark.asyncio
async def test_remove_ad_deletes_existing(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=5))
    await IndexAd(fake_uow, fake_ad_source).execute(5)
    assert 5 in fake_uow.search.snapshot()

    await RemoveAd(fake_uow).execute(5)

    assert 5 not in fake_uow.search.snapshot()
    assert fake_uow.committed


@pytest.mark.asyncio
async def test_remove_ad_missing_is_idempotent(fake_uow: FakeUnitOfWork) -> None:
    await RemoveAd(fake_uow).execute(999)

    assert fake_uow.search.snapshot() == {}
    assert fake_uow.committed


@pytest.mark.asyncio
async def test_remove_ad_does_not_call_ad_source(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await RemoveAd(fake_uow).execute(42)

    assert fake_ad_source.calls == []
