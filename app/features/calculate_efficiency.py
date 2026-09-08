from sqlalchemy import text

from app.database.connection import SessionLocal


FTA_FACTOR = 0.44


def calculate_efficiency() -> None:
    """Calcula las métricas de eficiencia de cada equipo por partido."""

    print("Calculando métricas de eficiencia...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                s.game_id,
                s.team_id,
                s.points,
                s.fga,
                s.fta,
                s.oreb,
                s.tov,
                CASE
                    WHEN s.is_home THEN g.away_points
                    ELSE g.home_points
                END AS points_allowed
            FROM team_game_stats s
            JOIN games g
                ON s.game_id = g.game_id
            ORDER BY
                s.game_id,
                s.team_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        updated = 0

        for row in results:
            possessions = (
                row.fga
                + (FTA_FACTOR * row.fta)
                - row.oreb
                + row.tov
            )

            if possessions <= 0:
                offensive_rating = None
                defensive_rating = None
                net_rating = None
            else:
                offensive_rating = (
                    row.points / possessions
                ) * 100

                defensive_rating = (
                    row.points_allowed / possessions
                ) * 100

                net_rating = (
                    offensive_rating
                    - defensive_rating
                )

            update_query = text(
                """
                UPDATE team_game_features
                SET
                    possessions = :possessions,
                    offensive_rating = :offensive_rating,
                    defensive_rating = :defensive_rating,
                    net_rating = :net_rating
                WHERE game_id = :game_id
                  AND team_id = :team_id;
                """
            )

            session.execute(
                update_query,
                {
                    "possessions": possessions,
                    "offensive_rating": offensive_rating,
                    "defensive_rating": defensive_rating,
                    "net_rating": net_rating,
                    "game_id": row.game_id,
                    "team_id": row.team_id,
                },
            )

            updated += 1

        session.commit()

        print(
            f"Métricas de eficiencia calculadas correctamente: {updated}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_efficiency()