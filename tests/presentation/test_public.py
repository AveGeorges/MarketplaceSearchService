import pytest
from httpx import AsyncClient

from src.application.usecases.index_ad import IndexAd
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


async def _seed(uow: FakeUnitOfWork, ad_source: FakeAdSource) -> None:
    ad_source.set(make_snapshot(ad_id=1, title="MacBook Pro 14", price=180000,
                                category="Электроника", city="Москва"))
    ad_source.set(make_snapshot(ad_id=2, title="MacBook Air", price=90000,
                                category="Электроника", city="Питер"))
    for ad_id in (1, 2):
        await IndexAd(uow, ad_source).execute(ad_id)


@pytest.mark.asyncio
async def test_search_returns_items(
    client: AsyncClient,
    fake_uow: FakeUnitOfWork,
) -> None:
    await _seed(fake_uow, FakeAdSource())

    response = await client.get("/search", params={"q": "macbook"})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert {item["ad_id"] for item in data["items"]} == {1, 2}
    assert data["query"] == "macbook"


@pytest.mark.asyncio
async def test_search_filters_by_category(
    client: AsyncClient,
    fake_uow: FakeUnitOfWork,
) -> None:
    await _seed(fake_uow, FakeAdSource())

    response = await client.get(
        "/search",
        params={"category": "Электроника", "city": "Москва"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["ad_id"] == 1


@pytest.mark.asyncio
async def test_search_empty_query_returns_empty_query_field(
    client: AsyncClient,
) -> None:
    response = await client.get("/search")

    assert response.status_code == 200
    assert response.json()["query"] == ""


@pytest.mark.asyncio
async def test_suggest_returns_titles(
    client: AsyncClient,
    fake_uow: FakeUnitOfWork,
) -> None:
    await _seed(fake_uow, FakeAdSource())

    response = await client.get("/search/suggest", params={"q": "Mac"})

    assert response.status_code == 200
    suggestions = response.json()["suggestions"]
    assert set(suggestions) == {"MacBook Pro 14", "MacBook Air"}


@pytest.mark.asyncio
async def test_suggest_rejects_short_prefix(client: AsyncClient) -> None:
    response = await client.get("/search/suggest", params={"q": "M"})

    assert response.status_code == 422
