"""Add recent efficiency features

Revision ID: 8c6fe3340864
Revises: c3326f4fd262
Create Date: 2026-09-08 10:34:05.775181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c6fe3340864'
down_revision: Union[str, Sequence[str], None] = 'c3326f4fd262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "team_game_features",
        sa.Column(
            "avg_offensive_rating_last_5",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "team_game_features",
        sa.Column(
            "avg_defensive_rating_last_5",
            sa.Float(),
            nullable=True,
        ),
    )

    op.add_column(
        "team_game_features",
        sa.Column(
            "avg_net_rating_last_5",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "team_game_features",
        "avg_net_rating_last_5",
    )

    op.drop_column(
        "team_game_features",
        "avg_defensive_rating_last_5",
    )

    op.drop_column(
        "team_game_features",
        "avg_offensive_rating_last_5",
    )