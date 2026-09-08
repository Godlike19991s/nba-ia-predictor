from pathlib import Path

import pandas as pd

from app.database.connection import SessionLocal
from app.database.models import Game


CSV_FILE = Path("data/processed/games_2024-25.csv")


def load_games() -> None:
    """Carga los partidos procesados en PostgreSQL."""

    print("Leyendo CSV...")

    games_df = pd.read_csv(
        CSV_FILE,
        dtype={"GAME_ID": str},
    )

    print(f"Registros encontrados en CSV: {len(games_df)}")

    session = SessionLocal()

    try:
        games = []

        for _, row in games_df.iterrows():
            game = Game(
                game_id=row["GAME_ID"],
                game_date=pd.to_datetime(row["GAME_DATE"]).date(),
                home_team_id=int(row["HOME_TEAM_ID"]),
                home_team_abbreviation=row["HOME_TEAM_ABBREVIATION"],
                home_team_name=row["HOME_TEAM_NAME"],
                away_team_id=int(row["AWAY_TEAM_ID"]),
                away_team_abbreviation=row["AWAY_TEAM_ABBREVIATION"],
                away_team_name=row["AWAY_TEAM_NAME"],
                home_points=int(row["HOME_POINTS"]),
                away_points=int(row["AWAY_POINTS"]),
            )

            games.append(game)

        session.add_all(games)
        session.commit()

        print(f"Partidos cargados correctamente: {len(games)}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    load_games()