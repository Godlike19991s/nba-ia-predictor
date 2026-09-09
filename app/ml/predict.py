from pathlib import Path

import joblib


MODEL_PATH = Path("models/logistic_regression.joblib")


def load_model():
    """Carga el modelo previamente entrenado."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    print("Modelo cargado correctamente.")

    return model


def predict_home_win(
    model,
    features: list[float],
) -> float:
    """
    Calcula la probabilidad de victoria del equipo local.

    Parameters
    ----------
    model:
        Modelo de Machine Learning entrenado.

    features:
        Lista de las 13 características utilizadas por el modelo.

    Returns
    -------
    float:
        Probabilidad de victoria local.
    """

    if len(features) != 13:
        raise ValueError(
            f"Se esperaban 13 features, pero se recibieron {len(features)}."
        )

    probability = model.predict_proba([features])[0][1]

    return float(probability)


def main() -> None:
    """Ejecuta una predicción de prueba."""

    print("=" * 60)
    print("PRUEBA DE PREDICCIÓN")
    print("=" * 60)

    model = load_model()

    # Estas son características de ejemplo.
    #
    # El orden DEBE coincidir exactamente con FEATURE_COLUMNS
    # definido en create_dataset.py.
    features = [
        0.8,    # home_win_pct_last_5
        0.4,    # away_win_pct_last_5
        10.0,   # home_recent_point_diff
        -2.0,   # away_recent_point_diff
        112.0,  # home_avg_offensive_rating_last_5
        105.0,  # away_avg_offensive_rating_last_5
        104.0,  # home_avg_defensive_rating_last_5
        108.0,  # away_avg_defensive_rating_last_5
        8.0,    # home_avg_net_rating_last_5
        -3.0,   # away_avg_net_rating_last_5
        7.0,    # offensive_rating_diff
        -4.0,   # defensive_rating_diff
        11.0,   # net_rating_diff
    ]

    probability = predict_home_win(
        model,
        features,
    )

    print()
    print("Resultado")
    print("-" * 60)
    print(
        f"Probabilidad de victoria local: "
        f"{probability:.2%}"
    )
    print(
        f"Probabilidad de victoria visitante: "
        f"{1 - probability:.2%}"
    )

    print()
    print("=" * 60)
    print("PREDICCIÓN COMPLETADA CORRECTAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()