from collections import deque

from sqlalchemy import text

from app.database.connection import SessionLocal


WINDOW_SIZE = 5


def calculate_recent_form() -> None:
    """Calcula las estadísticas de forma de los últimos 5 partidos."""

    print("Calculando forma reciente...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                s.game_id,
                s.team_id,
                g.game_date,
                s.points,
                CASE
                    WHEN s.is_home THEN g.away_points
                    ELSE g.home_points
                END AS points_allowed
            FROM team_game_stats s
            JOIN games g
                ON s.game_id = g.game_id
            ORDER BY
                s.team_id,
                g.game_date,
                s.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        history = {}

        updated = 0

        for row in results:

            team_history = history.setdefault(
                row.team_id,
                deque(maxlen=WINDOW_SIZE),
            )

            if len(team_history) < WINDOW_SIZE:
                wins_last_5 = None
                losses_last_5 = None
                win_pct_last_5 = None
                avg_points_last_5 = None
                avg_points_allowed_last_5 = None
                recent_point_diff = None
            else:
                wins_last_5 = sum(
                    1 for game in team_history
                    if game["points"] > game["points_allowed"]
                )

                losses_last_5 = sum(
                    1 for game in team_history
                    if game["points"] < game["points_allowed"]
                )

                win_pct_last_5 = (
                    wins_last_5 / WINDOW_SIZE
                )

                avg_points_last_5 = (
                    sum(game["points"] for game in team_history)
                    / WINDOW_SIZE
                )

                avg_points_allowed_last_5 = (
                    sum(
                        game["points_allowed"]
                        for game in team_history
                    )
                    / WINDOW_SIZE
                )

                recent_point_diff = (
                    avg_points_last_5
                    - avg_points_allowed_last_5
                )

            update_query = text(
                """
                UPDATE team_game_features
                SET
                    wins_last_5 = :wins_last_5,
                    losses_last_5 = :losses_last_5,
                    win_pct_last_5 = :win_pct_last_5,
                    avg_points_last_5 = :avg_points_last_5,
                    avg_points_allowed_last_5 =
                        :avg_points_allowed_last_5,
                    recent_point_diff = :recent_point_diff
                WHERE game_id = :game_id
                  AND team_id = :team_id;
                """
            )

            session.execute(
                update_query,
                {
                    "wins_last_5": wins_last_5,
                    "losses_last_5": losses_last_5,
                    "win_pct_last_5": win_pct_last_5,
                    "avg_points_last_5": avg_points_last_5,
                    "avg_points_allowed_last_5":
                        avg_points_allowed_last_5,
                    "recent_point_diff": recent_point_diff,
                    "game_id": row.game_id,
                    "team_id": row.team_id,
                },
            )

            updated += 1

            team_history.append(
                {
                    "points": row.points,
                    "points_allowed": row.points_allowed,
                }
            )

        session.commit()

        print(
            f"Forma reciente calculada correctamente: {updated}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_recent_form()
