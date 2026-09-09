from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.ml.create_dataset import build_dataset


TRAIN_RATIO = 0.80


def evaluate_model() -> None:
    """Evalúa el modelo baseline de Logistic Regression."""

    print("Evaluando modelo Logistic Regression...")

    # ---------------------------------------------------------
    # 1. Construir dataset
    # ---------------------------------------------------------

    X, y = build_dataset()

    if not X or not y:
        raise ValueError("El dataset está vacío.")

    if len(X) != len(y):
        raise ValueError(
            "El número de features y targets no coincide."
        )

    # ---------------------------------------------------------
    # 2. Separación temporal
    # ---------------------------------------------------------

    train_size = int(len(X) * TRAIN_RATIO)

    X_train = X[:train_size]
    y_train = y[:train_size]

    X_test = X[train_size:]
    y_test = y[train_size:]

    print()
    print("1. División temporal")
    print(f"   Entrenamiento: {len(X_train)}")
    print(f"   Prueba: {len(X_test)}")

    # ---------------------------------------------------------
    # 3. Crear modelo
    # ---------------------------------------------------------

    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    # ---------------------------------------------------------
    # 4. Entrenar
    # ---------------------------------------------------------

    model.fit(
        X_train,
        y_train,
    )

    print()
    print("2. Modelo entrenado correctamente.")

    # ---------------------------------------------------------
    # 5. Obtener probabilidades
    # ---------------------------------------------------------

    probabilities = model.predict_proba(X_test)[:, 1]

    # ---------------------------------------------------------
    # 6. Evaluación con umbral 50%
    # ---------------------------------------------------------

    threshold = 0.50

    predictions = [
        1 if probability >= threshold else 0
        for probability in probabilities
    ]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    print()
    print("3. Evaluación con umbral 50%")
    print(
        f"   Accuracy:  {accuracy:.4f}"
    )
    print(
        f"   Precision: {precision:.4f}"
    )
    print(
        f"   Recall:    {recall:.4f}"
    )

    # ---------------------------------------------------------
    # 7. Matriz de confusión
    # ---------------------------------------------------------

    true_negative = matrix[0][0]
    false_positive = matrix[0][1]
    false_negative = matrix[1][0]
    true_positive = matrix[1][1]

    print()
    print("4. Matriz de confusión")
    print()
    print(
        "                    Predicción"
    )
    print(
        "                  0          1"
    )
    print(
        f"Real 0       {true_negative:5d}      {false_positive:5d}"
    )
    print(
        f"Real 1       {false_negative:5d}      {true_positive:5d}"
    )

    # ---------------------------------------------------------
    # 8. Distribución de probabilidades
    # ---------------------------------------------------------

    minimum_probability = min(probabilities)
    maximum_probability = max(probabilities)
    average_probability = sum(probabilities) / len(
        probabilities
    )

    print()
    print("5. Distribución de probabilidades")
    print(
        f"   Mínima:   {minimum_probability:.4f}"
    )
    print(
        f"   Máxima:   {maximum_probability:.4f}"
    )
    print(
        f"   Promedio: {average_probability:.4f}"
    )

    # ---------------------------------------------------------
    # 9. Evaluación con diferentes umbrales
    # ---------------------------------------------------------

    print()
    print("6. Evaluación por umbral")
    print()
    print(
        "Umbral | Accuracy | Precision | Recall"
    )
    print(
        "-------|----------|-----------|-------"
    )

    for threshold in (
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
    ):
        threshold_predictions = [
            1 if probability >= threshold else 0
            for probability in probabilities
        ]

        threshold_accuracy = accuracy_score(
            y_test,
            threshold_predictions,
        )

        threshold_precision = precision_score(
            y_test,
            threshold_predictions,
            zero_division=0,
        )

        threshold_recall = recall_score(
            y_test,
            threshold_predictions,
            zero_division=0,
        )

        print(
            f"{threshold:6.2f} | "
            f"{threshold_accuracy:8.4f} | "
            f"{threshold_precision:9.4f} | "
            f"{threshold_recall:6.4f}"
        )

    print()
    print("Evaluación completada correctamente.")


if __name__ == "__main__":
    evaluate_model()