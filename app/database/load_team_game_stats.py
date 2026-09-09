import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import select

from app.database.connection import SessionLocal
from app.database.models import Game, TeamGameStats


def load_team_game_stats(season: str) -> None:
    """Carga las estadísticas de equipos de una temporada en PostgreSQL."""

    csv_file = Path(f"data/raw/games_{season}.csv")

    print("=" * 60)
    print("CARGA DE ESTADÍSTICAS DE EQUIPOS")
    print("=" * 60)
    print()

    print(f"Temporada: {season}")
    print(f"Archivo: {csv_file}")
    print()

    # ---------------------------------------------------------
    # 1. Verificar que exista el archivo
    # ---------------------------------------------------------

    if not csv_file.exists():
        raise FileNotFoundError(
            f"No existe el archivo RAW: {csv_file}"
        )

    # ---------------------------------------------------------
    # 2. Leer CSV
    # ---------------------------------------------------------

    print("1. Leyendo CSV RAW...")

    stats_df = pd.read_csv(
        csv_file,
        dtype={"GAME_ID": str},
    )

    # GAME_ID siempre debe conservar sus ceros iniciales.
    stats_df["GAME_ID"] = (
        stats_df["GAME_ID"]
        .astype(str)
        .str.zfill(10)
    )

    print(f"   Registros encontrados: {len(stats_df)}")
    print()

    # ---------------------------------------------------------
    # 3. Abrir conexión con PostgreSQL
    # ---------------------------------------------------------

    session = SessionLocal()

    try:
        # -----------------------------------------------------
        # 4. Obtener partidos existentes
        # -----------------------------------------------------

        print("2. Consultando partidos en PostgreSQL...")

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

        print(
            f"   Partidos encontrados en PostgreSQL: "
            f"{len(game_map)}"
        )
        print()

        # -----------------------------------------------------
        # 5. Obtener estadísticas ya existentes
        # -----------------------------------------------------

        print("3. Comprobando estadísticas existentes...")

        existing_stats = session.execute(
            select(TeamGameStats.game_id)
        ).all()

        existing_game_ids = {
            game_id
            for (game_id,) in existing_stats
        }

        print(
            f"   Partidos con estadísticas existentes: "
            f"{len(existing_game_ids)}"
        )
        print()

        # -----------------------------------------------------
        # 6. Preparar registros nuevos
        # -----------------------------------------------------

        print("4. Preparando nuevas estadísticas...")

        team_stats = []

        skipped_existing = 0
        skipped_invalid = 0

        for _, row in stats_df.iterrows():

            game_id = str(row["GAME_ID"])
            team_id = int(row["TEAM_ID"])

            # -------------------------------------------------
            # Evitar duplicados
            # -------------------------------------------------

            if game_id in existing_game_ids:
                skipped_existing += 1
                continue

            # -------------------------------------------------
            # Verificar que el partido exista
            # -------------------------------------------------

            if game_id not in game_map:
                print(
                    f"   ADVERTENCIA - "
                    f"El partido {game_id} no existe en games."
                )

                skipped_invalid += 1
                continue

            game = game_map[game_id]

            # -------------------------------------------------
            # Determinar local / visitante
            # -------------------------------------------------

            if team_id == game["home_team_id"]:
                is_home = True

            elif team_id == game["away_team_id"]:
                is_home = False

            else:
                raise ValueError(
                    f"El equipo {team_id} no pertenece "
                    f"al partido {game_id}."
                )

            # -------------------------------------------------
            # Crear registro
            # -------------------------------------------------

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

        print(
            f"   Registros nuevos preparados: "
            f"{len(team_stats)}"
        )

        print(
            f"   Registros ignorados por existir: "
            f"{skipped_existing}"
        )

        print(
            f"   Registros ignorados por partido inválido: "
            f"{skipped_invalid}"
        )

        print()

        # -----------------------------------------------------
        # 7. Insertar registros
        # -----------------------------------------------------

        if not team_stats:
            print("5. No hay nuevas estadísticas para insertar.")
            print()

            print("=" * 60)
            print("CARGA COMPLETADA")
            print("=" * 60)

            return

        print("5. Insertando estadísticas...")

        session.add_all(team_stats)
        session.commit()

        print(
            f"   Estadísticas insertadas correctamente: "
            f"{len(team_stats)}"
        )

        print()

        # -----------------------------------------------------
        # 8. Resultado
        # -----------------------------------------------------

        print("=" * 60)
        print("ESTADÍSTICAS CARGADAS CORRECTAMENTE")
        print("=" * 60)

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
            "python -m app.database.load_team_game_stats "
            "<temporada>"
        )
        print()
        print("Ejemplo:")
        print(
            "python -m app.database.load_team_game_stats "
            "2025-26"
        )
        raise SystemExit(1)

    season = sys.argv[1]

    load_team_game_stats(season)


if __name__ == "__main__":
    main()