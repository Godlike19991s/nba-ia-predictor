from pathlib import Path

import joblib
from sqlalchemy import text

from app.database.connection import SessionLocal


MODEL_PATH = Path("models/logistic_regression.joblib")


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
]


def load_model():
    """Carga el modelo de Machine Learning desde disco."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def get_game_features(
    game_id: str,
) -> tuple[list[float], dict]:
    """
    Obtiene las 13 features de un partido desde PostgreSQL.
    """

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,
                g.game_date,

                g.home_team_id,
                g.home_team_abbreviation,
                g.home_team_name,

                g.away_team_id,
                g.away_team_abbreviation,
                g.away_team_name,

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
                gf.net_rating_diff

            FROM games g

            JOIN team_game_features home
                ON home.game_id = g.game_id
                AND home.team_id = g.home_team_id

            JOIN team_game_features away
                ON away.game_id = g.game_id
                AND away.team_id = g.away_team_id

            JOIN game_features gf
                ON gf.game_id = g.game_id

            WHERE g.game_id = :game_id;
            """
        )

        row = session.execute(
            query,
            {"game_id": game_id},
        ).fetchone()

        if row is None:
            raise ValueError(
                f"No se encontró información completa "
                f"para el partido {game_id}."
            )

        features = [
            float(getattr(row, column))
            for column in FEATURE_COLUMNS
        ]

        game_info = {
            "game_id": row.game_id,
            "game_date": row.game_date,
            "home_team_id": row.home_team_id,
            "home_team_abbreviation": (
                row.home_team_abbreviation
            ),
            "home_team_name": row.home_team_name,
            "away_team_id": row.away_team_id,
            "away_team_abbreviation": (
                row.away_team_abbreviation
            ),
            "away_team_name": row.away_team_name,
        }

        return features, game_info

    finally:
        session.close()


def predict_game(game_id: str) -> dict:
    """
    Genera una predicción para un partido existente.
    """

    model = load_model()

    features, game_info = get_game_features(
        game_id
    )

    probability_home = float(
        model.predict_proba([features])[0][1]
    )

    probability_away = 1.0 - probability_home

    if probability_home >= 0.5:
        prediction = "HOME"
    else:
        prediction = "AWAY"

    return {
        **game_info,
        "probability_home": probability_home,
        "probability_away": probability_away,
        "prediction": prediction,
    }


def main() -> None:
    """Ejecuta una predicción de prueba."""

    game_id = "0022400061"

    print("=" * 60)
    print("PREDICCIÓN DE PARTIDO")
    print("=" * 60)

    print()
    print(f"Game ID: {game_id}")

    result = predict_game(game_id)

    print()
    print("Partido")
    print("-" * 60)

    print(
        f"{result['home_team_name']} "
        f"({result['home_team_abbreviation']})"
    )

    print(
        f"vs "
        f"{result['away_team_name']} "
        f"({result['away_team_abbreviation']})"
    )

    print()
    print("Predicción")
    print("-" * 60)

    print(
        f"Probabilidad local: "
        f"{result['probability_home']:.2%}"
    )

    print(
        f"Probabilidad visitante: "
        f"{result['probability_away']:.2%}"
    )

    print(
        f"Predicción: "
        f"{result['prediction']}"
    )

    print()
    print("=" * 60)
    print("PREDICCIÓN COMPLETADA CORRECTAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()