from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.ml.create_dataset import build_dataset

from catboost import CatBoostClassifier
from xgboost import XGBClassifier


def create_models() -> list[tuple[str, object]]:
    """Crea los modelos que serán comparados."""

    models = [
        (
            "Logistic Regression",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "model",
                        LogisticRegression(
                            max_iter=1000,
                            random_state=42,
                        ),
                    ),
                ]
            ),
        ),
        (
            "Random Forest",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                random_state=42,
                n_jobs=-1,
            ),
        ),
        (
            "XGBoost",
            XGBClassifier(
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
        ),
        (
            "CatBoost",
            CatBoostClassifier(
                iterations=300,
                depth=6,
                learning_rate=0.05,
                loss_function="Logloss",
                eval_metric="Logloss",
                random_seed=42,
                verbose=False,
            ),
        ),
    ]

    return models


def evaluate_model(
    model,
    X_train: list[list[float]],
    X_test: list[list[float]],
    y_train: list[int],
    y_test: list[int],
) -> dict[str, float]:
    """Entrena y evalúa un modelo en una ventana temporal."""

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "log_loss": log_loss(y_test, probabilities),
        "brier": brier_score_loss(y_test, probabilities),
    }


def walk_forward_compare() -> None:
    """Compara los modelos mediante validación Walk-Forward."""

    print("=" * 70)
    print("COMPARACIÓN WALK-FORWARD DE MODELOS")
    print("=" * 70)

    print()
    print("1. Construyendo dataset...")

    X, y = build_dataset()

    total_records = len(X)

    print()
    print(f"Registros totales: {total_records}")
    print(f"Features: {len(X[0])}")

    windows = [
        (0.50, 0.60),
        (0.60, 0.70),
        (0.70, 0.80),
        (0.80, 0.90),
    ]

    models = create_models()

    # Guardamos los resultados de cada modelo
    # para posteriormente calcular sus promedios.
    all_results = {
        name: []
        for name, _ in models
    }

    print()
    print("2. Ejecutando validación Walk-Forward")

    for window_number, (train_ratio, test_ratio) in enumerate(
        windows,
        start=1,
    ):

        train_end = int(total_records * train_ratio)
        test_end = int(total_records * test_ratio)

        X_train = X[:train_end]
        y_train = y[:train_end]

        X_test = X[train_end:test_end]
        y_test = y[train_end:test_end]

        print()
        print("-" * 70)
        print(f"VENTANA {window_number}")
        print("-" * 70)

        print(
            f"Entrenamiento: {len(X_train)} registros"
        )

        print(
            f"Prueba:        {len(X_test)} registros"
        )

        if len(set(y_train)) < 2:
            print(
                "ERROR: el conjunto de entrenamiento "
                "contiene una sola clase."
            )
            continue

        if len(set(y_test)) < 2:
            print(
                "ERROR: el conjunto de prueba "
                "contiene una sola clase."
            )
            continue

        for name, model in models:

            print()
            print(f"   Entrenando {name}...")

            result = evaluate_model(
                model,
                X_train,
                X_test,
                y_train,
                y_test,
            )

            all_results[name].append(result)

            print(
                f"   Accuracy: {result['accuracy']:.4f}"
            )

            print(
                f"   ROC-AUC:  {result['roc_auc']:.4f}"
            )

            print(
                f"   Log Loss: {result['log_loss']:.4f}"
            )

            print(
                f"   Brier:    {result['brier']:.4f}"
            )

    print()
    print("=" * 70)
    print("3. RESULTADOS POR MODELO")
    print("=" * 70)

    print()

    for name, results in all_results.items():

        print(name)
        print("-" * len(name))

        for index, result in enumerate(results, start=1):

            print(
                f"Ventana {index}: "
                f"Accuracy={result['accuracy']:.4f} | "
                f"ROC-AUC={result['roc_auc']:.4f} | "
                f"Log Loss={result['log_loss']:.4f} | "
                f"Brier={result['brier']:.4f}"
            )

        print()

    print("=" * 70)
    print("4. PROMEDIOS")
    print("=" * 70)

    print()

    print(
        f"{'Modelo':<22}"
        f"{'Accuracy':>10}"
        f"{'ROC-AUC':>10}"
        f"{'Log Loss':>12}"
        f"{'Brier':>10}"
    )

    print("-" * 64)

    averages = []

    for name, results in all_results.items():

        if not results:
            continue

        average_accuracy = sum(
            result["accuracy"]
            for result in results
        ) / len(results)

        average_roc_auc = sum(
            result["roc_auc"]
            for result in results
        ) / len(results)

        average_log_loss = sum(
            result["log_loss"]
            for result in results
        ) / len(results)

        average_brier = sum(
            result["brier"]
            for result in results
        ) / len(results)

        averages.append(
            {
                "model": name,
                "accuracy": average_accuracy,
                "roc_auc": average_roc_auc,
                "log_loss": average_log_loss,
                "brier": average_brier,
            }
        )

        print(
            f"{name:<22}"
            f"{average_accuracy:>10.4f}"
            f"{average_roc_auc:>10.4f}"
            f"{average_log_loss:>12.4f}"
            f"{average_brier:>10.4f}"
        )

    print()
    print("=" * 70)
    print("5. MEJOR MODELO")
    print("=" * 70)

    if averages:

        # Para este proyecto priorizamos ROC-AUC como
        # métrica principal de discriminación.
        best_model = max(
            averages,
            key=lambda result: result["roc_auc"],
        )

        print()
        print(
            f"Mejor modelo por ROC-AUC: "
            f"{best_model['model']}"
        )

        print(
            f"ROC-AUC promedio: "
            f"{best_model['roc_auc']:.4f}"
        )

        print(
            f"Accuracy promedio: "
            f"{best_model['accuracy']:.4f}"
        )

        print(
            f"Log Loss promedio: "
            f"{best_model['log_loss']:.4f}"
        )

        print(
            f"Brier promedio: "
            f"{best_model['brier']:.4f}"
        )

    print()
    print("=" * 70)
    print("COMPARACIÓN WALK-FORWARD COMPLETADA")
    print("=" * 70)


if __name__ == "__main__":
    walk_forward_compare()