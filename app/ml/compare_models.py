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
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from app.ml.create_dataset import FEATURE_COLUMNS, build_dataset


def temporal_split(
    X: list[list[float]],
    y: list[int],
    train_ratio: float = 0.8,
) -> tuple[
    list[list[float]],
    list[list[float]],
    list[int],
    list[int],
]:
    """Divide el dataset respetando el orden temporal."""

    split_index = int(len(X) * train_ratio)

    X_train = X[:split_index]
    X_test = X[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]

    return X_train, X_test, y_train, y_test


def evaluate_model(
    name: str,
    model,
    X_train: list[list[float]],
    X_test: list[list[float]],
    y_train: list[int],
    y_test: list[int],
) -> dict[str, float]:
    """Entrena y evalúa un modelo."""

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "model": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
        "log_loss": log_loss(y_test, probabilities),
        "brier": brier_score_loss(y_test, probabilities),
    }


def print_logistic_coefficients(model) -> None:
    """Muestra los coeficientes estandarizados de Logistic Regression."""

    print()
    print("=" * 60)
    print("IMPORTANCIA DE FEATURES - LOGISTIC REGRESSION")
    print("=" * 60)
    print()

    logistic_model = model.named_steps["model"]

    coefficients = logistic_model.coef_[0]

    feature_importance = list(
        zip(
            FEATURE_COLUMNS,
            coefficients,
        )
    )

    feature_importance.sort(
        key=lambda item: abs(item[1]),
        reverse=True,
    )

    print(
        f"{'Feature':<40}"
        f"{'Coeficiente':>15}"
        f"{'Dirección':>15}"
    )

    print("-" * 72)

    for feature, coefficient in feature_importance:

        if coefficient > 0:
            direction = "HOME"
        elif coefficient < 0:
            direction = "AWAY"
        else:
            direction = "NEUTRAL"

        print(
            f"{feature:<40}"
            f"{coefficient:>15.4f}"
            f"{direction:>15}"
        )

    print()
    print("=" * 60)


def compare_models() -> None:
    """Compara los modelos de Machine Learning."""

    print("=" * 60)
    print("COMPARACIÓN DE MODELOS")
    print("=" * 60)

    print()
    print("1. Construyendo dataset...")

    X, y = build_dataset()

    print()
    print(f"Registros totales: {len(X)}")
    print(f"Features: {len(X[0])}")
    print(f"Targets: {len(y)}")

    print()
    print("2. División temporal")

    X_train, X_test, y_train, y_test = temporal_split(X, y)

    print(f"   Entrenamiento: {len(X_train)}")
    print(f"   Prueba: {len(X_test)}")

    print()
    print("3. Modelos")

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
    ]

    results = []
    logistic_model = None

    for name, model in models:

        print()
        print(f"   Entrenando {name}...")

        result = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        results.append(result)

        if name == "Logistic Regression":
            logistic_model = model

        print(f"   {name} entrenado correctamente.")

    print()
    print("=" * 60)
    print("4. RESULTADOS")
    print("=" * 60)

    print()
    print(
        f"{'Modelo':<22}"
        f"{'Accuracy':>10}"
        f"{'ROC-AUC':>10}"
        f"{'Log Loss':>10}"
        f"{'Brier':>10}"
    )

    print("-" * 62)

    for result in results:

        print(
            f"{result['model']:<22}"
            f"{result['accuracy']:>10.4f}"
            f"{result['roc_auc']:>10.4f}"
            f"{result['log_loss']:>10.4f}"
            f"{result['brier']:>10.4f}"
        )

    print()
    print("5. Métricas adicionales")
    print()

    for result in results:

        print(result["model"])

        print(
            f"   Precision: {result['precision']:.4f}"
        )

        print(
            f"   Recall:    {result['recall']:.4f}"
        )

        print(
            f"   F1 Score:  {result['f1']:.4f}"
        )

        print()

    if logistic_model is not None:
        print_logistic_coefficients(logistic_model)

    print()
    print("=" * 60)
    print("COMPARACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == "__main__":
    compare_models()