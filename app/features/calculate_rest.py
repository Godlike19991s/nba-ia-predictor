from collections import defaultdict
from datetime import date

from sqlalchemy import text

from app.database.connection import SessionLocal


def calculate_rest() -> None:
    """
    Calcula los días de descanso de cada equipo antes de cada partido.

    También identifica si el partido corresponde a un
    back-to-back.

    El primer partido registrado de cada equipo no tiene
    un partido anterior conocido, por lo que rest_days
    queda como NULL.
    """

    print("Calculando días de descanso...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,
                g.game_date,
                g.home_team_id,
                g.away_team_id
            FROM games g
            ORDER BY
                g.game_date,
                g.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Partidos analizados: {len(results)}")

        # Guarda la última fecha conocida de cada equipo.
        last_game_date = defaultdict(lambda: None)

        updated = 0

        for row in results:

            # -------------------------------------------------
            # EQUIPO LOCAL
            # -------------------------------------------------

            home_previous_date = last_game_date[
                row.home_team_id
            ]

            if home_previous_date is None:
                home_rest_days = None
                home_is_back_to_back = False

            else:
                home_rest_days = (
                    row.game_date - home_previous_date
                ).days

                home_is_back_to_back = (
                    home_rest_days == 1
                )

            # -------------------------------------------------
            # EQUIPO VISITANTE
            # -------------------------------------------------

            away_previous_date = last_game_date[
                row.away_team_id
            ]

            if away_previous_date is None:
                away_rest_days = None
                away_is_back_to_back = False

            else:
                away_rest_days = (
                    row.game_date - away_previous_date
                ).days

                away_is_back_to_back = (
                    away_rest_days == 1
                )

            # -------------------------------------------------
            # ACTUALIZAR EQUIPO LOCAL
            # -------------------------------------------------

            update_home = text(
                """
                UPDATE team_game_features
                SET
                    rest_days = :rest_days,
                    is_back_to_back = :is_back_to_back
                WHERE game_id = :game_id
                  AND team_id = :team_id;
                """
            )

            session.execute(
                update_home,
                {
                    "rest_days": home_rest_days,
                    "is_back_to_back": home_is_back_to_back,
                    "game_id": row.game_id,
                    "team_id": row.home_team_id,
                },
            )

            # -------------------------------------------------
            # ACTUALIZAR EQUIPO VISITANTE
            # -------------------------------------------------

            update_away = text(
                """
                UPDATE team_game_features
                SET
                    rest_days = :rest_days,
                    is_back_to_back = :is_back_to_back
                WHERE game_id = :game_id
                  AND team_id = :team_id;
                """
            )

            session.execute(
                update_away,
                {
                    "rest_days": away_rest_days,
                    "is_back_to_back": away_is_back_to_back,
                    "game_id": row.game_id,
                    "team_id": row.away_team_id,
                },
            )

            updated += 2

            # -------------------------------------------------
            # ACTUALIZAR ÚLTIMO PARTIDO DE CADA EQUIPO
            # -------------------------------------------------

            last_game_date[row.home_team_id] = row.game_date
            last_game_date[row.away_team_id] = row.game_date

        session.commit()

        print(
            f"Registros de descanso actualizados: {updated}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_rest()