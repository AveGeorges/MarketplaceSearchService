import pytest

from src.application.usecases.index_ad import IndexAd
from src.application.usecases.search import Search
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


async def _seed(uow: FakeUnitOfWork, ad_source: FakeAdSource) -> None:
    ad_source.set(make_snapshot(ad_id=1, title="MacBook Pro 14", price=180000,
                                category="Электроника", city="Москва"))
    ad_source.set(make_snapshot(ad_id=2, title="MacBook Air", price=90000,
                                category="Электроника", city="Питер"))
    ad_source.set(make_snapshot(ad_id=3, title="BMW X5", price=3500000,
                                category="Автомобили", city="Москва"))
    for ad_id in (1, 2, 3):
        await IndexAd(uow, ad_source).execute(ad_id)


@pytest.mark.asyncio
async def test_search_filters_by_query(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await _seed(fake_uow, fake_ad_source)

    docs, total = await Search(fake_uow).execute(
        query="macbook",
        category=None,
        city=None,
        min_price=None,
        max_price=None,
        sort=None,
        limit=10,
        offset=0,
    )

    assert total == 2
    assert {d.ad_id for d in docs} == {1, 2}


@pytest.mark.asyncio
async def test_search_filters_by_category_and_city(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await _seed(fake_uow, fake_ad_source)

    docs, total = await Search(fake_uow).execute(
        query=None,
        category="Электроника",
        city="Москва",
        min_price=None,
        max_price=None,
        sort=None,
        limit=10,
        offset=0,
    )

    assert total == 1
    assert docs[0].ad_id == 1


@pytest.mark.asyncio
async def test_search_sort_price_asc(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await _seed(fake_uow, fake_ad_source)

    docs, _ = await Search(fake_uow).execute(
        query=None,
        category=None,
        city=None,
        min_price=None,
        max_price=None,
        sort="price_asc",
        limit=10,
        offset=0,
    )

    assert [d.ad_id for d in docs] == [2, 1, 3]


@pytest.mark.asyncio
async def test_search_price_range(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    await _seed(fake_uow, fake_ad_source)

    _, total = await Search(fake_uow).execute(
        query=None,
        category=None,
        city=None,
        min_price=100000,
        max_price=200000,
        sort=None,
        limit=10,
        offset=0,
    )

    assert total == 1
