from sqlalchemy import text

from app.database.connection import SessionLocal


FEATURE_COLUMNS = [
    "home_win_pct_last_5",
    "away_win_pct_last_5",
    "home_recent_point_diff",
    "away_recent_point_diff",
    "home_avg_offensive_rating_last_5",
    "away_avg_offensive_rating_last_5",
    "home_avg_defensive_rating_last_5",
    "away_avg_defensive_rating_last_5",
    "home_avg_net_rating_last_5",
    "away_avg_net_rating_last_5",
    "offensive_rating_diff",
    "defensive_rating_diff",
    "net_rating_diff",
    "home_rest_days",
    "away_rest_days",
    "rest_days_diff",
    "home_is_back_to_back",
    "away_is_back_to_back",
]


def build_dataset() -> tuple[list[list[float]], list[int]]:
    """Construye y devuelve el dataset para Machine Learning."""

    print("Construyendo dataset de Machine Learning...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,
                g.game_date,

                home.win_pct_last_5
                    AS home_win_pct_last_5,

                away.win_pct_last_5
                    AS away_win_pct_last_5,

                home.recent_point_diff
                    AS home_recent_point_diff,

                away.recent_point_diff
                    AS away_recent_point_diff,

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
                    AS away_avg_net_rating_last_5,

                gf.offensive_rating_diff,
                gf.defensive_rating_diff,
                gf.net_rating_diff,
                home.rest_days AS home_rest_days,

                away.rest_days AS away_rest_days,

                home.rest_days - away.rest_days
                    AS rest_days_diff,

                home.is_back_to_back AS home_is_back_to_back,

                away.is_back_to_back AS away_is_back_to_back,

                CASE
                    WHEN g.home_points > g.away_points
                    THEN 1
                    ELSE 0
                END AS target_home_win

            FROM games g

            JOIN team_game_features home
                ON home.game_id = g.game_id
                AND home.team_id = g.home_team_id

            JOIN team_game_features away
                ON away.game_id = g.game_id
                AND away.team_id = g.away_team_id

            JOIN game_features gf
                ON gf.game_id = g.game_id

            ORDER BY
                g.game_date,
                g.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Partidos encontrados: {len(results)}")

        if not results:
            return [], []

        feature_data = []

        for row in results:
            features = [
                getattr(row, column)
                for column in FEATURE_COLUMNS
            ]

            feature_data.append(features)

        targets = [
            row.target_home_win
            for row in results
        ]

        print(f"Features preparadas: {len(feature_data)}")
        print(f"Targets preparados: {len(targets)}")
        print(f"Victorias locales: {sum(targets)}")
        print(
            f"Victorias visitantes: "
            f"{len(targets) - sum(targets)}"
        )
        print(
            f"Número de features por partido: "
            f"{len(FEATURE_COLUMNS)}"
        )

        return feature_data, targets

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def create_dataset() -> None:
    """Construye el dataset y muestra un resumen."""

    build_dataset()


if __name__ == "__main__":
    create_dataset()