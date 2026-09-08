from collections import deque

from sqlalchemy import text

from app.database.connection import SessionLocal


WINDOW_SIZE = 5


def validate_no_leakage() -> None:
    """Valida que las features de forma no utilicen información futura."""

    print("Validando ausencia de data leakage...")

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
                END AS points_allowed,
                f.wins_last_5,
                f.losses_last_5,
                f.win_pct_last_5,
                f.avg_points_last_5,
                f.avg_points_allowed_last_5,
                f.recent_point_diff
            FROM team_game_stats s
            JOIN games g
                ON s.game_id = g.game_id
            JOIN team_game_features f
                ON f.game_id = s.game_id
                AND f.team_id = s.team_id
            ORDER BY
                s.team_id,
                g.game_date,
                s.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        history = {}

        errors = 0
        validated = 0

        for row in results:
            team_history = history.setdefault(
                row.team_id,
                deque(maxlen=WINDOW_SIZE),
            )

            if len(team_history) < WINDOW_SIZE:
                expected = {
                    "wins_last_5": None,
                    "losses_last_5": None,
                    "win_pct_last_5": None,
                    "avg_points_last_5": None,
                    "avg_points_allowed_last_5": None,
                    "recent_point_diff": None,
                }

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

                expected = {
                    "wins_last_5": wins,
                    "losses_last_5": losses,
                    "win_pct_last_5": wins / WINDOW_SIZE,
                    "avg_points_last_5": avg_points,
                    "avg_points_allowed_last_5": avg_points_allowed,
                    "recent_point_diff": (
                        avg_points - avg_points_allowed
                    ),
                }

            actual = {
                "wins_last_5": row.wins_last_5,
                "losses_last_5": row.losses_last_5,
                "win_pct_last_5": row.win_pct_last_5,
                "avg_points_last_5": row.avg_points_last_5,
                "avg_points_allowed_last_5":
                    row.avg_points_allowed_last_5,
                "recent_point_diff": row.recent_point_diff,
            }

            row_has_error = False

            for feature_name in expected:
                expected_value = expected[feature_name]
                actual_value = actual[feature_name]

                if expected_value is None and actual_value is None:
                    continue

                if expected_value is None or actual_value is None:
                    row_has_error = True
                    break

                if abs(expected_value - actual_value) > 1e-9:
                    row_has_error = True
                    break

            if row_has_error:
                errors += 1

                if errors <= 10:
                    print(
                        f"ERROR: {row.game_id} - "
                        f"team_id={row.team_id}"
                    )

            else:
                validated += 1

            team_history.append(
                {
                    "points": row.points,
                    "points_allowed": row.points_allowed,
                }
            )

        print()
        print(f"Registros validados correctamente: {validated}")
        print(f"Errores encontrados: {errors}")

        if errors == 0:
            print()
            print("VALIDACION EXITOSA")
            print("No se detectaron discrepancias en las features.")

        else:
            print()
            print("VALIDACION FALLIDA")
            print("Se detectaron discrepancias.")

    finally:
        session.close()


if __name__ == "__main__":
    validate_no_leakage()