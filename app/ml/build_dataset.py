from pathlib import Path

import pandas as pd
from sqlalchemy import text

from app.database.connection import SessionLocal


OUTPUT_PATH = Path("data/processed/nba_ml_dataset.csv")


FEATURE_COLUMNS = [
    "offensive_rating_diff",
    "defensive_rating_diff",
    "net_rating_diff",
    "elo_diff",
    "rest_days_diff",
    "home_is_back_to_back",
    "away_is_back_to_back",
    "win_pct_last_5_diff",
    "avg_points_last_5_diff",
    "avg_points_allowed_last_5_diff",
    "recent_point_diff_diff",
    "avg_offensive_rating_last_5_diff",
    "avg_defensive_rating_last_5_diff",
    "avg_net_rating_last_5_diff",
]


TARGET_COLUMN = "target"


def build_dataset() -> None:
    """Construye el dataset final para Machine Learning."""

    print("Construyendo dataset para Machine Learning...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,
                g.game_date,

                gf.offensive_rating_diff,
                gf.defensive_rating_diff,
                gf.net_rating_diff,
                gf.elo_diff,
                gf.rest_days_diff,
                gf.home_is_back_to_back,
                gf.away_is_back_to_back,

                home_features.win_pct_last_5
                    AS home_win_pct_last_5,

                away_features.win_pct_last_5
                    AS away_win_pct_last_5,

                home_features.avg_points_last_5
                    AS home_avg_points_last_5,

                away_features.avg_points_last_5
                    AS away_avg_points_last_5,

                home_features.avg_points_allowed_last_5
                    AS home_avg_points_allowed_last_5,

                away_features.avg_points_allowed_last_5
                    AS away_avg_points_allowed_last_5,

                home_features.recent_point_diff
                    AS home_recent_point_diff,

                away_features.recent_point_diff
                    AS away_recent_point_diff,

                home_features.avg_offensive_rating_last_5
                    AS home_avg_offensive_rating_last_5,

                away_features.avg_offensive_rating_last_5
                    AS away_avg_offensive_rating_last_5,

                home_features.avg_defensive_rating_last_5
                    AS home_avg_defensive_rating_last_5,

                away_features.avg_defensive_rating_last_5
                    AS away_avg_defensive_rating_last_5,

                home_features.avg_net_rating_last_5
                    AS home_avg_net_rating_last_5,

                away_features.avg_net_rating_last_5
                    AS away_avg_net_rating_last_5,

                g.home_points,
                g.away_points

            FROM games g

            INNER JOIN game_features gf
                ON g.game_id = gf.game_id

            INNER JOIN team_game_stats home_stats
                ON home_stats.game_id = g.game_id
                AND home_stats.is_home = TRUE

            INNER JOIN team_game_stats away_stats
                ON away_stats.game_id = g.game_id
                AND away_stats.is_home = FALSE

            INNER JOIN team_game_features home_features
                ON home_features.game_id = g.game_id
                AND home_features.team_id = home_stats.team_id

            INNER JOIN team_game_features away_features
                ON away_features.game_id = g.game_id
                AND away_features.team_id = away_stats.team_id

            WHERE
                g.home_points IS NOT NULL
                AND g.away_points IS NOT NULL

                AND gf.offensive_rating_diff IS NOT NULL
                AND gf.defensive_rating_diff IS NOT NULL
                AND gf.net_rating_diff IS NOT NULL
                AND gf.elo_diff IS NOT NULL
                AND gf.rest_days_diff IS NOT NULL
                AND gf.home_is_back_to_back IS NOT NULL
                AND gf.away_is_back_to_back IS NOT NULL

                AND home_features.win_pct_last_5 IS NOT NULL
                AND away_features.win_pct_last_5 IS NOT NULL

                AND home_features.avg_points_last_5 IS NOT NULL
                AND away_features.avg_points_last_5 IS NOT NULL

                AND home_features.avg_points_allowed_last_5 IS NOT NULL
                AND away_features.avg_points_allowed_last_5 IS NOT NULL

                AND home_features.recent_point_diff IS NOT NULL
                AND away_features.recent_point_diff IS NOT NULL

                AND home_features.avg_offensive_rating_last_5 IS NOT NULL
                AND away_features.avg_offensive_rating_last_5 IS NOT NULL

                AND home_features.avg_defensive_rating_last_5 IS NOT NULL
                AND away_features.avg_defensive_rating_last_5 IS NOT NULL

                AND home_features.avg_net_rating_last_5 IS NOT NULL
                AND away_features.avg_net_rating_last_5 IS NOT NULL

            ORDER BY
                g.game_date,
                g.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Partidos obtenidos: {len(results)}")

        if not results:
            raise ValueError(
                "No se encontraron partidos válidos "
                "para construir el dataset."
            )

        data = []

        for row in results:

            target = int(
                row.home_points > row.away_points
            )

            data.append(
                {
                    "game_id": row.game_id,
                    "game_date": row.game_date,

                    "offensive_rating_diff":
                        row.offensive_rating_diff,

                    "defensive_rating_diff":
                        row.defensive_rating_diff,

                    "net_rating_diff":
                        row.net_rating_diff,

                    "elo_diff":
                        row.elo_diff,

                    "rest_days_diff":
                        row.rest_days_diff,

                    "home_is_back_to_back":
                        int(row.home_is_back_to_back),

                    "away_is_back_to_back":
                        int(row.away_is_back_to_back),

                    "win_pct_last_5_diff": (
                        row.home_win_pct_last_5
                        - row.away_win_pct_last_5
                    ),

                    "avg_points_last_5_diff": (
                        row.home_avg_points_last_5
                        - row.away_avg_points_last_5
                    ),

                    "avg_points_allowed_last_5_diff": (
                        row.home_avg_points_allowed_last_5
                        - row.away_avg_points_allowed_last_5
                    ),

                    "recent_point_diff_diff": (
                        row.home_recent_point_diff
                        - row.away_recent_point_diff
                    ),

                    "avg_offensive_rating_last_5_diff": (
                        row.home_avg_offensive_rating_last_5
                        - row.away_avg_offensive_rating_last_5
                    ),

                    "avg_defensive_rating_last_5_diff": (
                        row.home_avg_defensive_rating_last_5
                        - row.away_avg_defensive_rating_last_5
                    ),

                    "avg_net_rating_last_5_diff": (
                        row.home_avg_net_rating_last_5
                        - row.away_avg_net_rating_last_5
                    ),

                    "target": target,
                }
            )

        df = pd.DataFrame(data)

        print(f"Registros del dataset: {len(df)}")

        print("\nDistribución del target:")
        print(
            df["target"].value_counts()
        )

        print("\nValores nulos:")
        print(
            df.isnull().sum()
        )

        print("\nPartidos duplicados:")
        print(
            df["game_id"].duplicated().sum()
        )

        print("\nVariables utilizadas:")
        for feature in FEATURE_COLUMNS:
            print(f" - {feature}")

        OUTPUT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        df.to_csv(
            OUTPUT_PATH,
            index=False,
        )

        print(
            "\nDataset guardado correctamente en: "
            f"{OUTPUT_PATH}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    build_dataset()