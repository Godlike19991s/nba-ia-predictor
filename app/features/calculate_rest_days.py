from sqlalchemy import text

from app.database.connection import SessionLocal


def calculate_rest_days() -> None:
    """Calcula y guarda los días de descanso de cada equipo."""

    print("Calculando rest_days...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                s.game_id,
                s.team_id,
                g.game_date,
                LAG(g.game_date) OVER (
                    PARTITION BY s.team_id
                    ORDER BY g.game_date, s.game_id
                ) AS previous_game_date
            FROM team_game_stats s
            JOIN games g
                ON s.game_id = g.game_id
            ORDER BY s.team_id, g.game_date, s.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        inserted = 0

        for row in results:

            if row.previous_game_date is None:
                rest_days = None
            else:
                rest_days = (
                    row.game_date - row.previous_game_date
                ).days

            insert_query = text(
                """
                INSERT INTO team_game_features (
                    game_id,
                    team_id,
                    rest_days
                )
                VALUES (
                    :game_id,
                    :team_id,
                    :rest_days
                );
                """
            )

            session.execute(
                insert_query,
                {
                    "game_id": row.game_id,
                    "team_id": row.team_id,
                    "rest_days": rest_days,
                },
            )

            inserted += 1

        session.commit()

        print(
            f"Características insertadas correctamente: {inserted}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_rest_days()