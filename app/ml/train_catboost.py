from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from catboost import CatBoostClassifier

from app.ml.create_dataset import FEATURE_COLUMNS, build_dataset


def train_catboost() -> None:
    """Entrena y evalúa un modelo CatBoost."""

    print("Entrenando modelo CatBoost...")

    X, y = build_dataset()

    total_records = len(X)
    split_index = int(total_records * 0.80)

    X_train = X[:split_index]
    X_test = X[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]

    print()
    print("1. División temporal")
    print(f"   Registros totales: {total_records}")
    print(f"   Entrenamiento: {len(X_train)}")
    print(f"   Prueba: {len(X_test)}")
    print("   Proporción entrenamiento: 80%")

    print()
    print("2. Entrenamiento")

    model = CatBoostClassifier(
        iterations=300,
        depth=5,
        learning_rate=0.03,
        loss_function="Logloss",
        eval_metric="Logloss",
        random_seed=42,
        verbose=False,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=(X_test, y_test),
        verbose=False,
    )

    print("   Modelo entrenado correctamente.")

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)
    roc_auc = roc_auc_score(y_test, probabilities)
    logloss = log_loss(y_test, probabilities)
    brier = brier_score_loss(y_test, probabilities)

    print()
    print("3. Resultados del modelo")
    print(f"   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1 Score:  {f1:.4f}")
    print(f"   ROC-AUC:   {roc_auc:.4f}")
    print(f"   Log Loss:  {logloss:.4f}")
    print(f"   Brier:     {brier:.4f}")

    print()
    print("4. Importancia de las features")

    importances = model.get_feature_importance()

    feature_importance = sorted(
        zip(FEATURE_COLUMNS, importances),
        key=lambda item: item[1],
        reverse=True,
    )

    for position, (feature, importance) in enumerate(
        feature_importance,
        start=1,
    ):
        print(
            f"   {position:2d}. "
            f"{feature}: {importance:.4f}"
        )

    print()
    print("Entrenamiento CatBoost completado correctamente.")


if __name__ == "__main__":
    train_catboost()