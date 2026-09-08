from datetime import date

from sqlalchemy import Boolean, Date, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base para todos los modelos de la aplicación."""


class Game(Base):
    """Representa un partido de la NBA."""

    __tablename__ = "games"

    game_id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
    )

    game_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    home_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    home_team_abbreviation: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    home_team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    away_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    away_team_abbreviation: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    away_team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    home_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    away_points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


class TeamGameStats(Base):
    """Estadísticas de un equipo en un partido."""

    __tablename__ = "team_game_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    game_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    team_abbreviation: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    is_home: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    points: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fgm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fga: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fg_pct: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    fg3m: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fg3a: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fg3_pct: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    ftm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    fta: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ft_pct: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    oreb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    dreb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reb: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    ast: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    stl: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    blk: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    tov: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pf: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    plus_minus: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


class TeamGameFeatures(Base):

    __tablename__ = "team_game_features"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    game_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    rest_days: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    is_back_to_back: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
