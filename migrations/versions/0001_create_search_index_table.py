"""create search_index table

Revision ID: 0001
Revises:
Create Date: 2026-04-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "search_index",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ad_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column(
            "ts_vector",
            postgresql.TSVECTOR(),
            sa.Computed(
                "to_tsvector('russian', title || ' ' || description)",
                persisted=True,
            ),
            nullable=False,
        ),
        sa.Column(
            "indexed_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "ix_search_index_ad_id", "search_index", ["ad_id"], unique=True
    )
    op.create_index(
        "ix_search_index_ts_vector",
        "search_index",
        ["ts_vector"],
        postgresql_using="gin",
    )
    op.create_index("ix_search_index_category", "search_index", ["category"])
    op.create_index("ix_search_index_city", "search_index", ["city"])


def downgrade() -> None:
    op.drop_index("ix_search_index_city", table_name="search_index")
    op.drop_index("ix_search_index_category", table_name="search_index")
    op.drop_index("ix_search_index_ts_vector", table_name="search_index")
    op.drop_index("ix_search_index_ad_id", table_name="search_index")
    op.drop_table("search_index")
