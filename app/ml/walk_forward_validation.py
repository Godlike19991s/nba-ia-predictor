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


def create_model() -> Pipeline:
    """Crea el modelo de Logistic Regression."""

    return Pipeline(
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
    )


def evaluate_window(
    X_train: list[list[float]],
    X_test: list[list[float]],
    y_train: list[int],
    y_test: list[int],
) -> dict[str, float]:
    """Entrena y evalúa una ventana temporal."""

    model = create_model()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "log_loss": log_loss(y_test, probabilities),
        "brier": brier_score_loss(y_test, probabilities),
    }


def walk_forward_validation() -> None:
    """Evalúa el modelo utilizando varias ventanas temporales."""

    print("=" * 60)
    print("WALK-FORWARD VALIDATION")
    print("=" * 60)

    print()
    print("1. Construyendo dataset...")

    X, y = build_dataset()

    print()
    print(f"Registros totales: {len(X)}")
    print(f"Features: {len(X[0])}")

    total_records = len(X)

    # Definimos varias ventanas temporales.
    # Cada ventana utiliza únicamente información anterior
    # para entrenar el modelo.

    windows = [
        (0.50, 0.60),
        (0.60, 0.70),
        (0.70, 0.80),
        (0.80, 0.90),
    ]

    results = []

    print()
    print("2. Ventanas temporales")

    for index, (train_end_ratio, test_end_ratio) in enumerate(
        windows,
        start=1,
    ):

        train_end = int(total_records * train_end_ratio)
        test_end = int(total_records * test_end_ratio)

        X_train = X[:train_end]
        y_train = y[:train_end]

        X_test = X[train_end:test_end]
        y_test = y[train_end:test_end]

        print()
        print(f"   Ventana {index}")
        print(
            f"   Entrenamiento: registros 0-{train_end - 1}"
        )
        print(
            f"   Prueba: registros {train_end}-{test_end - 1}"
        )
        print(
            f"   Train: {len(X_train)} | Test: {len(X_test)}"
        )

        # Verificamos que ambas clases existan en entrenamiento
        # y prueba antes de calcular ROC-AUC.

        if len(set(y_train)) < 2:
            print(
                "   ERROR: el entrenamiento contiene una sola clase."
            )
            continue

        if len(set(y_test)) < 2:
            print(
                "   ERROR: la prueba contiene una sola clase."
            )
            continue

        result = evaluate_window(
            X_train,
            X_test,
            y_train,
            y_test,
        )

        results.append(result)

        print("   Resultados:")
        print(
            f"      Accuracy: {result['accuracy']:.4f}"
        )
        print(
            f"      ROC-AUC:  {result['roc_auc']:.4f}"
        )
        print(
            f"      Log Loss: {result['log_loss']:.4f}"
        )
        print(
            f"      Brier:    {result['brier']:.4f}"
        )

    if not results:
        print()
        print("No fue posible evaluar ninguna ventana.")
        return

    print()
    print("=" * 60)
    print("3. RESULTADOS CONSOLIDADOS")
    print("=" * 60)

    print()
    print(
        f"{'Ventana':<12}"
        f"{'Accuracy':>10}"
        f"{'ROC-AUC':>10}"
        f"{'Log Loss':>10}"
        f"{'Brier':>10}"
    )

    print("-" * 52)

    for index, result in enumerate(results, start=1):

        print(
            f"{index:<12}"
            f"{result['accuracy']:>10.4f}"
            f"{result['roc_auc']:>10.4f}"
            f"{result['log_loss']:>10.4f}"
            f"{result['brier']:>10.4f}"
        )

    print()
    print("=" * 60)
    print("4. PROMEDIOS")
    print("=" * 60)

    average_accuracy = sum(
        result["accuracy"] for result in results
    ) / len(results)

    average_roc_auc = sum(
        result["roc_auc"] for result in results
    ) / len(results)

    average_log_loss = sum(
        result["log_loss"] for result in results
    ) / len(results)

    average_brier = sum(
        result["brier"] for result in results
    ) / len(results)

    print()
    print(
        f"Accuracy promedio: {average_accuracy:.4f}"
    )
    print(
        f"ROC-AUC promedio:  {average_roc_auc:.4f}"
    )
    print(
        f"Log Loss promedio: {average_log_loss:.4f}"
    )
    print(
        f"Brier promedio:    {average_brier:.4f}"
    )

    print()
    print("=" * 60)
    print("VALIDACIÓN WALK-FORWARD COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    walk_forward_validation()