from pathlib import Path

import json

import pandas as pd


METRICS_DIRECTORY = Path("data/metrics")
OUTPUT_PATH = Path("data/metrics/model_comparison.csv")


MODEL_NAMES = {
    "logistic_regression": "Logistic Regression",
    "random_forest": "Random Forest",
    "xgboost": "XGBoost",
}


METRICS = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "roc_auc",
    "log_loss",
    "brier_score",
]


def load_model_metrics() -> list[dict]:
    """Carga las métricas de todos los modelos disponibles."""

    print("Cargando métricas de los modelos...")

    results = []

    for model_key, model_name in MODEL_NAMES.items():

        metrics_path = (
            METRICS_DIRECTORY
            / f"{model_key}.json"
        )

        if not metrics_path.exists():
            print(
                f"ADVERTENCIA: No existe "
                f"{metrics_path}"
            )
            continue

        with open(
            metrics_path,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        model_metrics = data.get("metrics", {})

        row = {
            "model": model_name,
        }

        for metric in METRICS:
            row[metric] = model_metrics.get(metric)

        results.append(row)

    return results


def compare_models() -> None:
    """Compara las métricas de los modelos entrenados."""

    print("Comparando modelos de Machine Learning...")

    results = load_model_metrics()

    if not results:
        raise FileNotFoundError(
            "No se encontraron archivos de métricas "
            "en data/metrics."
        )

    df = pd.DataFrame(results)

    print("\n" + "=" * 80)
    print("COMPARACIÓN DE MODELOS")
    print("=" * 80)

    print(
        df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # Identificar mejores modelos
    # ---------------------------------------------------------

    valid_accuracy = df.dropna(
        subset=["accuracy"]
    )

    valid_roc_auc = df.dropna(
        subset=["roc_auc"]
    )

    valid_log_loss = df.dropna(
        subset=["log_loss"]
    )

    valid_brier = df.dropna(
        subset=["brier_score"]
    )

    print("\n" + "=" * 80)
    print("MEJORES MODELOS POR MÉTRICA")
    print("=" * 80)

    if not valid_accuracy.empty:

        best_accuracy = valid_accuracy.loc[
            valid_accuracy["accuracy"].idxmax()
        ]

        print(
            f"Mejor Accuracy : "
            f"{best_accuracy['model']} "
            f"({best_accuracy['accuracy']:.4f})"
        )

    if not valid_roc_auc.empty:

        best_roc_auc = valid_roc_auc.loc[
            valid_roc_auc["roc_auc"].idxmax()
        ]

        print(
            f"Mejor ROC-AUC  : "
            f"{best_roc_auc['model']} "
            f"({best_roc_auc['roc_auc']:.4f})"
        )

    if not valid_log_loss.empty:

        best_log_loss = valid_log_loss.loc[
            valid_log_loss["log_loss"].idxmin()
        ]

        print(
            f"Mejor Log Loss : "
            f"{best_log_loss['model']} "
            f"({best_log_loss['log_loss']:.4f})"
        )

    if not valid_brier.empty:

        best_brier = valid_brier.loc[
            valid_brier["brier_score"].idxmin()
        ]

        print(
            f"Mejor Brier    : "
            f"{best_brier['model']} "
            f"({best_brier['brier_score']:.4f})"
        )

    # ---------------------------------------------------------
    # Guardar comparación
    # ---------------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"\nComparación guardada correctamente en: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    compare_models()