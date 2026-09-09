from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
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


DATASET_PATH = Path("data/processed/nba_ml_dataset.csv")
MODEL_PATH = Path("data/models/random_forest.pkl")
METRICS_PATH = Path("data/metrics/random_forest.json")


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


def train_random_forest() -> None:
    """Entrena y evalúa el modelo Random Forest."""

    print("Entrenando Random Forest...")

    # ---------------------------------------------------------
    # Validar dataset
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

    df = df.sort_values(
        ["game_date", "game_id"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # División temporal
    # ---------------------------------------------------------
    #
    # 80 % más antiguo -> entrenamiento
    # 20 % más reciente -> prueba
    #
    # Es importante mantener esta división para evitar
    # utilizar información futura durante el entrenamiento.
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
    # Crear modelo
    # ---------------------------------------------------------
    #
    # Random Forest está compuesto por muchos árboles de
    # decisión.
    #
    # Cada árbol aprende diferentes relaciones entre las
    # variables.
    #
    # Posteriormente todos los árboles participan en la
    # decisión final.
    # ---------------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
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
    # Métricas
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
    # Resultados
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("RESULTADOS RANDOM FOREST")
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
    # Importancia de variables
    # ---------------------------------------------------------

    feature_importance = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    )

    feature_importance = feature_importance.sort_values(
        "importance",
        ascending=False
    )

    print("\nImportancia de las variables:")
    print("-" * 60)

    print(
        feature_importance.to_string(
            index=False
        )
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
    # Guardamos las métricas en JSON para posteriormente
    # comparar automáticamente todos los modelos.
    # ---------------------------------------------------------

    metrics = {
        "model": "Random Forest",
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
    train_random_forest()