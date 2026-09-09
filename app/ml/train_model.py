from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    log_loss,
    brier_score_loss,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.ml.create_dataset import FEATURE_COLUMNS, build_dataset


TRAIN_RATIO = 0.80


def train_model() -> None:
    """Entrena el modelo baseline de Logistic Regression."""

    print("Entrenando modelo Logistic Regression...")

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

    total_records = len(X)

    train_size = int(total_records * TRAIN_RATIO)

    if train_size <= 0 or train_size >= total_records:
        raise ValueError(
            "La proporción de entrenamiento no produce "
            "una división válida."
        )

    X_train = X[:train_size]
    y_train = y[:train_size]

    X_test = X[train_size:]
    y_test = y[train_size:]

    print()
    print("1. División temporal")
    print(f"   Registros totales: {total_records}")
    print(f"   Entrenamiento: {len(X_train)}")
    print(f"   Prueba: {len(X_test)}")
    print(f"   Proporción entrenamiento: {TRAIN_RATIO:.0%}")

    # ---------------------------------------------------------
    # 3. Crear pipeline
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
    # 4. Entrenamiento
    # ---------------------------------------------------------

    print()
    print("2. Entrenamiento")

    model.fit(X_train, y_train)

    print("   Modelo entrenado correctamente.")

    # ---------------------------------------------------------
    # 5. Predicciones
    # ---------------------------------------------------------

    y_pred = model.predict(X_test)

    y_probability = model.predict_proba(X_test)[:, 1]

    # ---------------------------------------------------------
    # 6. Métricas
    # ---------------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred,
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability,
    )

    logloss = log_loss(
        y_test,
        y_probability,
    )

    brier = brier_score_loss(
        y_test,
        y_probability,
    )

    # ---------------------------------------------------------
    # 7. Resultados
    # ---------------------------------------------------------

    print()
    print("3. Resultados del modelo")
    print(
        f"   Accuracy:  {accuracy:.4f}"
    )
    print(
        f"   Precision: {precision:.4f}"
    )
    print(
        f"   Recall:    {recall:.4f}"
    )
    print(
        f"   F1 Score:  {f1:.4f}"
    )
    print(
        f"   ROC-AUC:   {roc_auc:.4f}"
    )
    print(
        f"   Log Loss:  {logloss:.4f}"
    )
    print(
        f"   Brier:     {brier:.4f}"
    )

    # ---------------------------------------------------------
    # 8. Información del dataset
    # ---------------------------------------------------------

    print()
    print("4. Features utilizadas")

    for index, feature in enumerate(
        FEATURE_COLUMNS,
        start=1,
    ):
        print(f"   {index}. {feature}")

    print()
    print("Entrenamiento completado correctamente.")


if __name__ == "__main__":
    train_model()