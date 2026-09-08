from pathlib import Path

import pandas as pd
from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import Game, TeamGameStats


CSV_FILE = Path("data/raw/games_2024-25.csv")


def load_team_game_stats() -> None:
    """Carga las estadísticas de los equipos en PostgreSQL."""

    print("Leyendo CSV RAW...")

    stats_df = pd.read_csv(
        CSV_FILE,
        dtype={"GAME_ID": str},
    )

    print(f"Registros encontrados en CSV: {len(stats_df)}")

    session = SessionLocal()

    try:
        # Obtener la información de localía desde la tabla games.
        games = session.execute(
            select(
                Game.game_id,
                Game.home_team_id,
                Game.away_team_id,
            )
        ).all()

        game_map = {
            game_id: {
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
            }
            for game_id, home_team_id, away_team_id in games
        }

        print(f"Partidos encontrados en PostgreSQL: {len(game_map)}")

        team_stats = []

        for _, row in stats_df.iterrows():
            game_id = str(row["GAME_ID"])
            team_id = int(row["TEAM_ID"])

            if game_id not in game_map:
                raise ValueError(
                    f"El partido {game_id} no existe en la tabla games."
                )

            game = game_map[game_id]

            if team_id == game["home_team_id"]:
                is_home = True
            elif team_id == game["away_team_id"]:
                is_home = False
            else:
                raise ValueError(
                    f"El equipo {team_id} no pertenece al partido {game_id}."
                )

            stats = TeamGameStats(
                game_id=game_id,
                team_id=team_id,
                team_abbreviation=row["TEAM_ABBREVIATION"],
                team_name=row["TEAM_NAME"],
                is_home=is_home,
                points=int(row["PTS"]),
                fgm=int(row["FGM"]),
                fga=int(row["FGA"]),
                fg_pct=float(row["FG_PCT"]),
                fg3m=int(row["FG3M"]),
                fg3a=int(row["FG3A"]),
                fg3_pct=float(row["FG3_PCT"]),
                ftm=int(row["FTM"]),
                fta=int(row["FTA"]),
                ft_pct=float(row["FT_PCT"]),
                oreb=int(row["OREB"]),
                dreb=int(row["DREB"]),
                reb=int(row["REB"]),
                ast=int(row["AST"]),
                stl=int(row["STL"]),
                blk=int(row["BLK"]),
                tov=int(row["TOV"]),
                pf=int(row["PF"]),
                plus_minus=float(row["PLUS_MINUS"]),
            )

            team_stats.append(stats)

        session.add_all(team_stats)
        session.commit()

        print(
            "Estadísticas de equipos cargadas correctamente: "
            f"{len(team_stats)}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    load_team_game_stats()