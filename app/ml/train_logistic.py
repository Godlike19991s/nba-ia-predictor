from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATASET_PATH = Path("data/processed/nba_ml_dataset.csv")
MODEL_PATH = Path("data/models/logistic_regression.pkl")
METRICS_PATH = Path("data/metrics/logistic_regression.json")


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


def train_logistic() -> None:
    """Entrena y evalúa el modelo Logistic Regression."""

    print("Entrenando Logistic Regression...")

    # ---------------------------------------------------------
    # Validar que exista el dataset
    # ---------------------------------------------------------

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"No existe el dataset: {DATASET_PATH}"
        )

    # ---------------------------------------------------------
    # Cargar dataset
    # ---------------------------------------------------------

    df = pd.read_csv(DATASET_PATH)

    print(f"Registros cargados: {len(df)}")

    # ---------------------------------------------------------
    # Preparar fechas
    # ---------------------------------------------------------

    df["game_date"] = pd.to_datetime(df["game_date"])

    # ---------------------------------------------------------
    # Orden temporal
    # ---------------------------------------------------------
    #
    # Ordenamos los partidos cronológicamente.
    #
    # Esto es MUY importante en un sistema de predicción
    # deportiva porque no queremos entrenar utilizando
    # información de partidos que ocurrieron después.
    # ---------------------------------------------------------

    df = df.sort_values(
        ["game_date", "game_id"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # División temporal
    # ---------------------------------------------------------
    #
    # 80 % más antiguo -> entrenamiento
    # 20 % más reciente -> prueba
    # ---------------------------------------------------------

    split_index = int(len(df) * 0.80)

    train_df = df.iloc[:split_index].copy()
    test_df = df.iloc[split_index:].copy()

    print(
        f"Registros de entrenamiento: {len(train_df)}"
    )

    print(
        f"Registros de prueba: {len(test_df)}"
    )

    # ---------------------------------------------------------
    # Separar variables y target
    # ---------------------------------------------------------

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df[TARGET_COLUMN]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df[TARGET_COLUMN]

    # ---------------------------------------------------------
    # Crear Pipeline
    # ---------------------------------------------------------
    #
    # StandardScaler:
    #   Normaliza las variables para que tengan escalas
    #   comparables.
    #
    # LogisticRegression:
    #   Aprende la relación entre nuestras variables y
    #   la probabilidad de que gane el equipo local.
    # ---------------------------------------------------------

    model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "logistic_regression",
                LogisticRegression(
                    max_iter=1000
                ),
            ),
        ]
    )

    # ---------------------------------------------------------
    # Entrenamiento
    # ---------------------------------------------------------

    model.fit(
        X_train,
        y_train
    )

    # ---------------------------------------------------------
    # Predicciones
    # ---------------------------------------------------------

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    # ---------------------------------------------------------
    # Calcular métricas
    # ---------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions
    )

    recall = recall_score(
        y_test,
        predictions
    )

    f1 = f1_score(
        y_test,
        predictions
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    logloss = log_loss(
        y_test,
        probabilities
    )

    brier = brier_score_loss(
        y_test,
        probabilities
    )

    # ---------------------------------------------------------
    # Resultados en consola
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("RESULTADOS LOGISTIC REGRESSION")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {roc_auc:.4f}")
    print(f"Log Loss : {logloss:.4f}")
    print(f"Brier    : {brier:.4f}")

    print("\nMatriz de confusión:")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    # ---------------------------------------------------------
    # Coeficientes
    # ---------------------------------------------------------
    #
    # Como utilizamos Pipeline, primero obtenemos el modelo
    # Logistic Regression que está dentro del Pipeline.
    # ---------------------------------------------------------

    logistic_model = model.named_steps[
        "logistic_regression"
    ]

    coefficients = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "coefficient": logistic_model.coef_[0],
        }
    )

    coefficients["abs_coefficient"] = (
        coefficients["coefficient"].abs()
    )

    coefficients = coefficients.sort_values(
        "abs_coefficient",
        ascending=False
    )

    print("\nImportancia de las variables:")
    print("-" * 60)

    print(
        coefficients[
            ["feature", "coefficient"]
        ].to_string(index=False)
    )

    # ---------------------------------------------------------
    # Guardar modelo
    # ---------------------------------------------------------

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        f"\nModelo guardado correctamente en: "
        f"{MODEL_PATH}"
    )

    # ---------------------------------------------------------
    # Guardar métricas
    # ---------------------------------------------------------
    #
    # Guardamos las métricas en JSON para poder utilizarlas
    # posteriormente en un sistema automático de comparación
    # entre modelos.
    # ---------------------------------------------------------

    metrics = {
        "model": "Logistic Regression",
        "dataset": str(DATASET_PATH),
        "total_records": len(df),
        "training_records": len(train_df),
        "test_records": len(test_df),
        "features": FEATURE_COLUMNS,
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
            "roc_auc": float(roc_auc),
            "log_loss": float(logloss),
            "brier_score": float(brier),
        },
    }

    METRICS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        METRICS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Métricas guardadas correctamente en: "
        f"{METRICS_PATH}"
    )


if __name__ == "__main__":
    train_logistic()