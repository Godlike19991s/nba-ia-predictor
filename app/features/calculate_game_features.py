from sqlalchemy import text

from app.database.connection import SessionLocal


def calculate_game_features() -> None:
    """Calcula las características comparativas de cada partido."""

    print("Calculando características de los partidos...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,

                home.team_id AS home_team_id,
                away.team_id AS away_team_id,

                home.avg_offensive_rating_last_5
                    AS home_avg_offensive_rating_last_5,

                away.avg_offensive_rating_last_5
                    AS away_avg_offensive_rating_last_5,

                home.avg_defensive_rating_last_5
                    AS home_avg_defensive_rating_last_5,

                away.avg_defensive_rating_last_5
                    AS away_avg_defensive_rating_last_5,

                home.avg_net_rating_last_5
                    AS home_avg_net_rating_last_5,

                away.avg_net_rating_last_5
                    AS away_avg_net_rating_last_5

            FROM games g

            JOIN team_game_features home
                ON home.game_id = g.game_id
                AND home.team_id = g.home_team_id

            JOIN team_game_features away
                ON away.game_id = g.game_id
                AND away.team_id = g.away_team_id

            ORDER BY
                g.game_date,
                g.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        inserted = 0
        skipped = 0

        for row in results:

            # No podemos calcular diferencias si alguno de los
            # equipos todavía no tiene suficientes partidos previos.
            if (
                row.home_avg_offensive_rating_last_5 is None
                or row.away_avg_offensive_rating_last_5 is None
                or row.home_avg_defensive_rating_last_5 is None
                or row.away_avg_defensive_rating_last_5 is None
                or row.home_avg_net_rating_last_5 is None
                or row.away_avg_net_rating_last_5 is None
            ):
                skipped += 1
                continue

            offensive_rating_diff = (
                row.home_avg_offensive_rating_last_5
                - row.away_avg_offensive_rating_last_5
            )

            defensive_rating_diff = (
                row.home_avg_defensive_rating_last_5
                - row.away_avg_defensive_rating_last_5
            )

            net_rating_diff = (
                row.home_avg_net_rating_last_5
                - row.away_avg_net_rating_last_5
            )

            update_query = text(
                """
                INSERT INTO game_features (
                    game_id,
                    offensive_rating_diff,
                    defensive_rating_diff,
                    net_rating_diff
                )
                VALUES (
                    :game_id,
                    :offensive_rating_diff,
                    :defensive_rating_diff,
                    :net_rating_diff
                )
                """
            )

            session.execute(
                update_query,
                {
                    "game_id": row.game_id,
                    "offensive_rating_diff": offensive_rating_diff,
                    "defensive_rating_diff": defensive_rating_diff,
                    "net_rating_diff": net_rating_diff,
                },
            )

            inserted += 1

        session.commit()

        print(
            f"Características calculadas correctamente: {inserted}"
        )
        print(
            f"Partidos omitidos por falta de datos históricos: {skipped}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_game_features()