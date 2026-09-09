from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier


DATASET_PATH = Path("data/processed/nba_ml_dataset.csv")
OUTPUT_PATH = Path("data/metrics/time_series_validation.csv")


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


def create_models() -> dict:
    """Crea los modelos que serán evaluados."""

    models = {
        "Logistic Regression": Pipeline(
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
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=6,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        ),
    }

    return models


def calculate_metrics(
    y_true: pd.Series,
    predictions: np.ndarray,
    probabilities: np.ndarray,
) -> dict:
    """Calcula las métricas principales."""

    return {
        "accuracy": accuracy_score(
            y_true,
            predictions,
        ),
        "precision": precision_score(
            y_true,
            predictions,
        ),
        "recall": recall_score(
            y_true,
            predictions,
        ),
        "f1": f1_score(
            y_true,
            predictions,
        ),
        "roc_auc": roc_auc_score(
            y_true,
            probabilities,
        ),
        "log_loss": log_loss(
            y_true,
            probabilities,
        ),
        "brier_score": brier_score_loss(
            y_true,
            probabilities,
        ),
    }


def validate_models() -> None:
    """Evalúa los modelos mediante validación temporal."""

    print("Validando modelos mediante TimeSeriesSplit...")

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"No existe el dataset: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    print(f"Registros cargados: {len(df)}")

    df["game_date"] = pd.to_datetime(
        df["game_date"]
    )

    df = df.sort_values(
        ["game_date", "game_id"]
    ).reset_index(drop=True)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # ---------------------------------------------------------
    # Validación temporal
    # ---------------------------------------------------------

    n_splits = 5

    time_split = TimeSeriesSplit(
        n_splits=n_splits
    )

    models = create_models()

    results = []

    # ---------------------------------------------------------
    # Evaluar cada modelo
    # ---------------------------------------------------------

    for model_name, model in models.items():

        print("\n" + "=" * 70)
        print(f"MODELO: {model_name}")
        print("=" * 70)

        for fold, (train_index, test_index) in enumerate(
            time_split.split(X),
            start=1,
        ):

            X_train = X.iloc[train_index]
            X_test = X.iloc[test_index]

            y_train = y.iloc[train_index]
            y_test = y.iloc[test_index]

            print(
                f"\nFold {fold}: "
                f"train={len(X_train)} | "
                f"test={len(X_test)}"
            )

            # Entrenamiento
            model.fit(
                X_train,
                y_train,
            )

            # Predicciones
            predictions = model.predict(
                X_test
            )

            probabilities = model.predict_proba(
                X_test
            )[:, 1]

            # Métricas
            metrics = calculate_metrics(
                y_test,
                predictions,
                probabilities,
            )

            print(
                f"Accuracy : {metrics['accuracy']:.4f}"
            )

            print(
                f"ROC-AUC  : {metrics['roc_auc']:.4f}"
            )

            print(
                f"Log Loss : {metrics['log_loss']:.4f}"
            )

            print(
                f"Brier    : {metrics['brier_score']:.4f}"
            )

            results.append(
                {
                    "model": model_name,
                    "fold": fold,
                    "train_records": len(X_train),
                    "test_records": len(X_test),
                    **metrics,
                }
            )

    # ---------------------------------------------------------
    # Crear DataFrame
    # ---------------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    print("\n" + "=" * 70)
    print("RESULTADOS POR FOLD")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # Promedios
    # ---------------------------------------------------------

    summary_df = (
        results_df
        .groupby("model")
        [
            [
                "accuracy",
                "precision",
                "recall",
                "f1",
                "roc_auc",
                "log_loss",
                "brier_score",
            ]
        ]
        .mean()
        .reset_index()
    )

    print("\n" + "=" * 70)
    print("PROMEDIO DE VALIDACIÓN TEMPORAL")
    print("=" * 70)

    print(
        summary_df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # Guardar resultados
    # ---------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nResultados guardados correctamente en: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    validate_models()