from datetime import datetime, timezone
from pathlib import Path
import json

import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.ml.create_dataset import (
    FEATURE_COLUMNS,
    build_dataset,
)


MODEL_DIR = Path("models")

MODEL_PATH = MODEL_DIR / "logistic_regression.joblib"

METADATA_PATH = (
    MODEL_DIR / "logistic_regression_metadata.json"
)


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
    """
    Divide el dataset respetando el orden temporal.

    Los partidos más antiguos se utilizan para entrenamiento
    y los partidos más recientes para evaluación.
    """

    split_index = int(len(X) * train_ratio)

    X_train = X[:split_index]
    X_test = X[split_index:]

    y_train = y[:split_index]
    y_test = y[split_index:]

    return X_train, X_test, y_train, y_test


def create_model() -> Pipeline:
    """
    Crea el pipeline de Logistic Regression.

    El StandardScaler normaliza las variables antes
    de enviarlas al modelo.
    """

    return Pipeline(
        [
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )


def save_metadata(
    total_records: int,
    train_records: int,
    test_records: int,
) -> None:
    """
    Guarda la información necesaria para identificar
    cómo fue construido el modelo.
    """

    metadata = {
        "model_name": "Logistic Regression",
        "model_type": "LogisticRegression",
        "framework": "scikit-learn",
        "trained_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "dataset_records": total_records,
        "train_records": train_records,
        "test_records": test_records,
        "train_ratio": 0.8,
        "feature_count": len(FEATURE_COLUMNS),
        "features": FEATURE_COLUMNS,
    }

    with METADATA_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False,
        )


def train_and_save_model() -> None:
    """
    Entrena Logistic Regression y guarda el modelo
    junto con sus metadatos.
    """

    print("=" * 60)
    print("ENTRENAMIENTO Y GUARDADO DEL MODELO")
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

    X_train, X_test, y_train, y_test = temporal_split(
        X,
        y,
    )

    print(f"   Entrenamiento: {len(X_train)}")
    print(f"   Prueba: {len(X_test)}")

    print()
    print("3. Creando modelo")

    model = create_model()

    print(
        "   Logistic Regression creado correctamente."
    )

    print()
    print("4. Entrenamiento")

    model.fit(
        X_train,
        y_train,
    )

    print(
        "   Modelo entrenado correctamente."
    )

    print()
    print("5. Guardando modelo")

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )

    print(
        f"   Modelo guardado en: {MODEL_PATH}"
    )

    print()
    print("6. Guardando metadatos")

    save_metadata(
        total_records=len(X),
        train_records=len(X_train),
        test_records=len(X_test),
    )

    print(
        f"   Metadatos guardados en: "
        f"{METADATA_PATH}"
    )

    print()
    print("7. Verificación")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo en "
            f"{MODEL_PATH}"
        )

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontraron los metadatos en "
            f"{METADATA_PATH}"
        )

    model_size = MODEL_PATH.stat().st_size
    metadata_size = METADATA_PATH.stat().st_size

    print("   Modelo: OK")
    print(
        f"   Tamaño modelo: "
        f"{model_size:,} bytes"
    )

    print("   Metadatos: OK")
    print(
        f"   Tamaño metadatos: "
        f"{metadata_size:,} bytes"
    )

    print()
    print("=" * 60)
    print("MODELO Y METADATOS GUARDADOS CORRECTAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    train_and_save_model()