import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import Game


def load_games(season: str) -> None:
    """Carga los partidos procesados de una temporada en PostgreSQL."""

    csv_file = Path(
        f"data/processed/games_{season}.csv"
    )

    print("Leyendo CSV...")
    print(f"Archivo: {csv_file}")

    if not csv_file.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {csv_file}"
        )

    games_df = pd.read_csv(
        csv_file,
        dtype={"GAME_ID": str},
    )

    print(
        f"Registros encontrados en CSV: "
        f"{len(games_df)}"
    )

    session = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Obtener partidos existentes
        # ---------------------------------------------------------

        existing_game_ids = set(
            session.scalars(
                select(Game.game_id)
            ).all()
        )

        print(
            f"Partidos existentes en PostgreSQL: "
            f"{len(existing_game_ids)}"
        )

        # ---------------------------------------------------------
        # 2. Filtrar partidos nuevos
        # ---------------------------------------------------------

        new_games_df = games_df[
            ~games_df["GAME_ID"].isin(existing_game_ids)
        ]

        print(
            f"Partidos nuevos para insertar: "
            f"{len(new_games_df)}"
        )

        if new_games_df.empty:
            print()
            print("No hay partidos nuevos para insertar.")
            return

        # ---------------------------------------------------------
        # 3. Crear objetos Game
        # ---------------------------------------------------------

        games = []

        for _, row in new_games_df.iterrows():

            game = Game(
                game_id=row["GAME_ID"],
                game_date=pd.to_datetime(
                    row["GAME_DATE"]
                ).date(),
                home_team_id=int(row["HOME_TEAM_ID"]),
                home_team_abbreviation=row[
                    "HOME_TEAM_ABBREVIATION"
                ],
                home_team_name=row[
                    "HOME_TEAM_NAME"
                ],
                away_team_id=int(row["AWAY_TEAM_ID"]),
                away_team_abbreviation=row[
                    "AWAY_TEAM_ABBREVIATION"
                ],
                away_team_name=row[
                    "AWAY_TEAM_NAME"
                ],
                home_points=int(row["HOME_POINTS"]),
                away_points=int(row["AWAY_POINTS"]),
            )

            games.append(game)

        # ---------------------------------------------------------
        # 4. Insertar
        # ---------------------------------------------------------

        session.add_all(games)
        session.commit()

        print()
        print(
            f"Partidos nuevos cargados correctamente: "
            f"{len(games)}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def main() -> None:
    """Punto de entrada del cargador."""

    if len(sys.argv) != 2:
        print(
            "Uso:"
        )
        print(
            "python -m app.database.load_games 2025-26"
        )
        return

    season = sys.argv[1]

    load_games(season)


if __name__ == "__main__":
    main()