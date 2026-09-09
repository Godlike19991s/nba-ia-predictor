from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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

    return (
        X[:split_index],
        X[split_index:],
        y[:split_index],
        y[split_index:],
    )


def select_columns(
    X: list[list[float]],
    columns: list[str],
    selected_columns: list[str],
) -> list[list[float]]:
    """Construye un nuevo dataset utilizando únicamente determinadas features."""

    indexes = [
        columns.index(column)
        for column in selected_columns
    ]

    return [
        [row[index] for index in indexes]
        for row in X
    ]


def evaluate_feature_set(
    name: str,
    X: list[list[float]],
    y: list[int],
) -> dict[str, float]:

    X_train, X_test, y_train, y_test = temporal_split(
        X,
        y,
    )

    model = Pipeline(
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

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    return {
        "name": name,
        "features": len(X[0]),
        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
        "log_loss": log_loss(
            y_test,
            probabilities,
        ),
        "brier": brier_score_loss(
            y_test,
            probabilities,
        ),
    }


def feature_selection() -> None:
    """Analiza el impacto de eliminar features redundantes."""

    print("=" * 70)
    print("SELECCIÓN EXPERIMENTAL DE FEATURES")
    print("=" * 70)

    print()
    print("1. Construyendo dataset...")

    X, y = build_dataset()

    print()
    print(f"Registros: {len(X)}")
    print(f"Features originales: {len(FEATURE_COLUMNS)}")

    # ---------------------------------------------------------
    # CONJUNTO A
    # Todas las features
    # ---------------------------------------------------------

    all_features = FEATURE_COLUMNS.copy()

    # ---------------------------------------------------------
    # CONJUNTO B
    # Eliminar recent_point_diff
    # ---------------------------------------------------------

    without_recent_point_diff = [
        column
        for column in FEATURE_COLUMNS
        if column not in {
            "home_recent_point_diff",
            "away_recent_point_diff",
        }
    ]

    # ---------------------------------------------------------
    # CONJUNTO C
    # Eliminar win_pct_last_5
    # ---------------------------------------------------------

    without_win_pct = [
        column
        for column in FEATURE_COLUMNS
        if column not in {
            "home_win_pct_last_5",
            "away_win_pct_last_5",
        }
    ]

    # ---------------------------------------------------------
    # CONJUNTO D
    # Eliminar recent_point_diff y win_pct
    # ---------------------------------------------------------

    reduced_features = [
        column
        for column in FEATURE_COLUMNS
        if column not in {
            "home_recent_point_diff",
            "away_recent_point_diff",
            "home_win_pct_last_5",
            "away_win_pct_last_5",
        }
    ]

    feature_sets = [
        (
            "Baseline - 18 features",
            all_features,
        ),
        (
            "Sin recent_point_diff",
            without_recent_point_diff,
        ),
        (
            "Sin win_pct_last_5",
            without_win_pct,
        ),
        (
            "Reducido - 14 features",
            reduced_features,
        ),
    ]

    print()
    print("=" * 70)
    print("2. CONFIGURACIONES A COMPARAR")
    print("=" * 70)

    for name, columns in feature_sets:

        print()
        print(name)
        print("-" * len(name))

        for column in columns:
            print(f"   - {column}")

    # ---------------------------------------------------------
    # EVALUACIÓN
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("3. EVALUACIÓN")
    print("=" * 70)

    results = []

    for name, columns in feature_sets:

        print()
        print(f"Evaluando: {name}")
        print(f"Features: {len(columns)}")

        X_selected = select_columns(
            X,
            FEATURE_COLUMNS,
            columns,
        )

        result = evaluate_feature_set(
            name,
            X_selected,
            y,
        )

        results.append(result)

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

    # ---------------------------------------------------------
    # RESULTADOS
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("4. RESULTADOS COMPARATIVOS")
    print("=" * 70)

    print()

    print(
        f"{'Configuración':<32}"
        f"{'Features':>10}"
        f"{'Accuracy':>10}"
        f"{'ROC-AUC':>10}"
        f"{'Log Loss':>11}"
        f"{'Brier':>10}"
    )

    print("-" * 83)

    for result in results:

        print(
            f"{result['name']:<32}"
            f"{result['features']:>10}"
            f"{result['accuracy']:>10.4f}"
            f"{result['roc_auc']:>10.4f}"
            f"{result['log_loss']:>11.4f}"
            f"{result['brier']:>10.4f}"
        )

    # ---------------------------------------------------------
    # MEJOR CONFIGURACIÓN
    # ---------------------------------------------------------

    best_auc = max(
        results,
        key=lambda result: result["roc_auc"],
    )

    best_log_loss = min(
        results,
        key=lambda result: result["log_loss"],
    )

    best_brier = min(
        results,
        key=lambda result: result["brier"],
    )

    print()
    print("=" * 70)
    print("5. MEJORES CONFIGURACIONES")
    print("=" * 70)

    print()

    print(
        f"Mejor ROC-AUC:  "
        f"{best_auc['name']} "
        f"({best_auc['roc_auc']:.4f})"
    )

    print(
        f"Mejor Log Loss: "
        f"{best_log_loss['name']} "
        f"({best_log_loss['log_loss']:.4f})"
    )

    print(
        f"Mejor Brier:    "
        f"{best_brier['name']} "
        f"({best_brier['brier']:.4f})"
    )

    print()
    print("=" * 70)
    print("ANÁLISIS DE SELECCIÓN DE FEATURES COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    feature_selection()