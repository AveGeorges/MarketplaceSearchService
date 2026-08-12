from datetime import datetime

from sqlalchemy import Computed, DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class SearchIndexModel(Base):
    __tablename__ = "search_index"
    __table_args__ = (
        Index("ix_search_index_ad_id", "ad_id", unique=True),
        Index("ix_search_index_ts_vector", "ts_vector", postgresql_using="gin"),
        Index("ix_search_index_category", "category"),
        Index("ix_search_index_city", "city"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ad_id: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    ts_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed(
            "to_tsvector('russian', title || ' ' || description)",
            persisted=True,
        ),
    )
    indexed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
