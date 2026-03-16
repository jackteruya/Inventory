"""create inventory items

Revision ID: 0001
Revises:
Create Date: 2026-03-13
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "inventory_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("identifier", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column(
            "last_updated", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
    )
    op.create_index("ix_inventory_items_identifier", "inventory_items", ["identifier"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_inventory_items_identifier", table_name="inventory_items")
    op.drop_table("inventory_items")
