from collections import defaultdict, deque

from sqlalchemy import text

from app.database.connection import SessionLocal


WINDOW_SIZE = 5


def calculate_home_away_form() -> None:
    """Calcula la forma reciente de los equipos como local y visitante."""

    print("Calculando forma local/visitante...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                s.game_id,
                s.team_id,
                g.game_date,
                s.is_home,
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

        history = defaultdict(
            lambda: {
                "home": deque(maxlen=WINDOW_SIZE),
                "away": deque(maxlen=WINDOW_SIZE),
            }
        )

        updated = 0

        for row in results:
            location = "home" if row.is_home else "away"

            team_history = history[row.team_id][location]

            if len(team_history) < WINDOW_SIZE:
                wins = None
                losses = None
                win_pct = None
                avg_points = None
                avg_points_allowed = None
                point_diff = None

            else:
                wins = sum(
                    1
                    for game in team_history
                    if game["points"] > game["points_allowed"]
                )

                losses = sum(
                    1
                    for game in team_history
                    if game["points"] < game["points_allowed"]
                )

                win_pct = wins / WINDOW_SIZE

                avg_points = (
                    sum(game["points"] for game in team_history)
                    / WINDOW_SIZE
                )

                avg_points_allowed = (
                    sum(
                        game["points_allowed"]
                        for game in team_history
                    )
                    / WINDOW_SIZE
                )

                point_diff = (
                    avg_points - avg_points_allowed
                )

            if location == "home":
                update_query = text(
                    """
                    UPDATE team_game_features
                    SET
                        home_wins_last_5 = :wins,
                        home_losses_last_5 = :losses,
                        home_win_pct_last_5 = :win_pct,
                        home_avg_points_last_5 = :avg_points,
                        home_avg_points_allowed_last_5 =
                            :avg_points_allowed,
                        home_recent_point_diff = :point_diff
                    WHERE game_id = :game_id
                      AND team_id = :team_id;
                    """
                )

            else:
                update_query = text(
                    """
                    UPDATE team_game_features
                    SET
                        away_wins_last_5 = :wins,
                        away_losses_last_5 = :losses,
                        away_win_pct_last_5 = :win_pct,
                        away_avg_points_last_5 = :avg_points,
                        away_avg_points_allowed_last_5 =
                            :avg_points_allowed,
                        away_recent_point_diff = :point_diff
                    WHERE game_id = :game_id
                      AND team_id = :team_id;
                    """
                )

            session.execute(
                update_query,
                {
                    "wins": wins,
                    "losses": losses,
                    "win_pct": win_pct,
                    "avg_points": avg_points,
                    "avg_points_allowed": avg_points_allowed,
                    "point_diff": point_diff,
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
            f"Forma local/visitante calculada correctamente: {updated}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_home_away_form()