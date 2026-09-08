from collections import defaultdict, deque
from sqlalchemy import text
from app.database.connection import SessionLocal
WINDOW_SIZE = 5
def calculate_recent_efficiency() -> None:
    """Calcula los promedios de eficiencia de los últimos 5 partidos."""
    print("Calculando eficiencia reciente...")
    session = SessionLocal()
    try:
        query = text(
            """
            SELECT
                f.game_id,
                f.team_id,
                g.game_date,
                f.offensive_rating,
                f.defensive_rating,
                f.net_rating
            FROM team_game_features f
            JOIN games g
                ON f.game_id = g.game_id
            WHERE f.offensive_rating IS NOT NULL
              AND f.defensive_rating IS NOT NULL
              AND f.net_rating IS NOT NULL
            ORDER BY
                f.team_id,
                g.game_date,
                f.game_id;
            """
        )
        results = session.execute(query).fetchall()
        print(f"Registros analizados: {len(results)}")
        history = defaultdict(
            lambda: deque(maxlen=WINDOW_SIZE)
        )
        updated = 0
        for row in results:
            team_history = history[row.team_id]
            if len(team_history) < WINDOW_SIZE:
                avg_offensive_rating = None
                avg_defensive_rating = None
                avg_net_rating = None
            else:
                avg_offensive_rating = (
                    sum(
                        game["offensive_rating"]
                        for game in team_history
                    )
                    / WINDOW_SIZE
                )
                avg_defensive_rating = (
                    sum(
                        game["defensive_rating"]
                        for game in team_history
                    )
                    / WINDOW_SIZE
                )
                avg_net_rating = (
                    sum(
                        game["net_rating"]
                        for game in team_history
                    )
                    / WINDOW_SIZE
                )
            update_query = text(
                """
                UPDATE team_game_features
                SET
                    avg_offensive_rating_last_5 =
                        :avg_offensive_rating,
                    avg_defensive_rating_last_5 =
                        :avg_defensive_rating,
                    avg_net_rating_last_5 =
                        :avg_net_rating
                WHERE game_id = :game_id
                  AND team_id = :team_id;
                """
            )
            session.execute(
                update_query,
                {
                    "avg_offensive_rating": avg_offensive_rating,
                    "avg_defensive_rating": avg_defensive_rating,
                    "avg_net_rating": avg_net_rating,
                    "game_id": row.game_id,
                    "team_id": row.team_id,
                },
            )
            updated += 1
            team_history.append(
                {
                    "offensive_rating": row.offensive_rating,
                    "defensive_rating": row.defensive_rating,
                    "net_rating": row.net_rating,
                }
            )
        session.commit()
        print(
            "Eficiencia reciente calculada correctamente: "
            f"{updated}"
        )
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
if __name__ == "__main__":
    calculate_recent_efficiency()
