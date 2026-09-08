"""Add unique constraint to game features

Revision ID: 2b835d5d166d
Revises: 3ebd3955d99b
Create Date: 2026-09-08 10:54:53.909355

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "2b835d5d166d"
down_revision: Union[str, Sequence[str], None] = "3ebd3955d99b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uq_game_features_game_id",
        "game_features",
        ["game_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_game_features_game_id",
        "game_features",
        type_="unique",
    )