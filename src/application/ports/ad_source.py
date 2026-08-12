from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AdSnapshot:
    ad_id: int
    title: str
    description: str
    price: int
    category: str
    city: str
    status: str


class AdSource(ABC):
    @abstractmethod
    async def get(
        self,
        ad_id: int,
    ) -> AdSnapshot | None: ...
