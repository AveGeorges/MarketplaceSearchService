import pytest

from src.application.usecases.index_ad import IndexAd
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


@pytest.mark.asyncio
async def test_index_ad_active_upserts(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=42, title="MacBook Pro 14", price=180000))

    usecase = IndexAd(fake_uow, fake_ad_source)
    await usecase.execute(42)

    docs = fake_uow.search.snapshot()
    assert 42 in docs
    assert docs[42].title == "MacBook Pro 14"
    assert docs[42].price == 180000
    assert fake_ad_source.calls == [42]
    assert fake_uow.committed


@pytest.mark.asyncio
async def test_index_ad_active_twice_updates_in_place(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=1, title="Old", price=100))
    await IndexAd(fake_uow, fake_ad_source).execute(1)

    fake_ad_source.set(make_snapshot(ad_id=1, title="New", price=200))
    await IndexAd(fake_uow, fake_ad_source).execute(1)

    docs = fake_uow.search.snapshot()
    assert len(docs) == 1
    assert docs[1].title == "New"
    assert docs[1].price == 200


@pytest.mark.asyncio
async def test_index_ad_archived_deletes_from_index(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=7, status="active"))
    await IndexAd(fake_uow, fake_ad_source).execute(7)
    assert 7 in fake_uow.search.snapshot()

    fake_ad_source.set(make_snapshot(ad_id=7, status="archived"))
    await IndexAd(fake_uow, fake_ad_source).execute(7)

    assert 7 not in fake_uow.search.snapshot()
    assert fake_uow.committed


@pytest.mark.asyncio
async def test_index_ad_not_found_deletes_from_index(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=9))
    await IndexAd(fake_uow, fake_ad_source).execute(9)
    assert 9 in fake_uow.search.snapshot()

    fake_ad_source.remove(9)
    await IndexAd(fake_uow, fake_ad_source).execute(9)

    assert 9 not in fake_uow.search.snapshot()


@pytest.mark.asyncio
async def test_index_ad_missing_and_not_in_index_is_noop(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await IndexAd(fake_uow, fake_ad_source).execute(999)

    assert fake_uow.search.snapshot() == {}
    assert fake_uow.committed
