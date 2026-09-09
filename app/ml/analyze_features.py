from math import sqrt

from app.ml.create_dataset import FEATURE_COLUMNS, build_dataset


def calculate_mean(values: list[float]) -> float:
    """Calcula el promedio de una lista de valores."""

    if not values:
        return 0.0

    return sum(values) / len(values)


def calculate_std(values: list[float], mean: float) -> float:
    """Calcula la desviación estándar poblacional."""

    if not values:
        return 0.0

    variance = sum(
        (value - mean) ** 2
        for value in values
    ) / len(values)

    return sqrt(variance)


def calculate_correlation(
    x: list[float],
    y: list[float],
) -> float:
    """Calcula la correlación de Pearson entre dos variables."""

    if len(x) != len(y):
        raise ValueError(
            "Las variables deben tener el mismo número de registros."
        )

    if not x:
        return 0.0

    mean_x = calculate_mean(x)
    mean_y = calculate_mean(y)

    numerator = sum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(x, y)
    )

    denominator_x = sum(
        (x_value - mean_x) ** 2
        for x_value in x
    )

    denominator_y = sum(
        (y_value - mean_y) ** 2
        for y_value in y
    )

    denominator = sqrt(
        denominator_x * denominator_y
    )

    if denominator == 0:
        return 0.0

    return numerator / denominator


def analyze_features() -> None:
    """Analiza las relaciones estadísticas entre las features."""

    print("=" * 70)
    print("ANÁLISIS DE FEATURES")
    print("=" * 70)

    print()
    print("1. Construyendo dataset...")

    feature_data, targets = build_dataset()

    print()
    print(f"Registros: {len(feature_data)}")
    print(f"Features: {len(FEATURE_COLUMNS)}")
    print(f"Targets: {len(targets)}")

    if not feature_data:
        raise ValueError(
            "No existen registros para analizar."
        )

    # ---------------------------------------------------------
    # Convertir el dataset por filas a columnas
    # ---------------------------------------------------------

    feature_values: dict[str, list[float]] = {}

    for index, feature_name in enumerate(FEATURE_COLUMNS):

        feature_values[feature_name] = [
            float(row[index])
            for row in feature_data
        ]

    # ---------------------------------------------------------
    # 2. Estadísticas descriptivas
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("2. ESTADÍSTICAS DESCRIPTIVAS")
    print("=" * 70)
    print()

    print(
        f"{'Feature':<40}"
        f"{'Mínimo':>12}"
        f"{'Máximo':>12}"
        f"{'Promedio':>12}"
        f"{'Std':>12}"
    )

    print("-" * 88)

    for feature_name in FEATURE_COLUMNS:

        values = feature_values[feature_name]

        minimum = min(values)
        maximum = max(values)
        mean = calculate_mean(values)
        std = calculate_std(values, mean)

        print(
            f"{feature_name:<40}"
            f"{minimum:>12.4f}"
            f"{maximum:>12.4f}"
            f"{mean:>12.4f}"
            f"{std:>12.4f}"
        )

    # ---------------------------------------------------------
    # 3. Correlaciones
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("3. CORRELACIONES")
    print("=" * 70)
    print()

    correlations = []

    for index, feature_a in enumerate(FEATURE_COLUMNS):

        for feature_b in FEATURE_COLUMNS[index + 1:]:

            correlation = calculate_correlation(
                feature_values[feature_a],
                feature_values[feature_b],
            )

            correlations.append(
                (
                    feature_a,
                    feature_b,
                    correlation,
                    abs(correlation),
                )
            )

    correlations.sort(
        key=lambda item: item[3],
        reverse=True,
    )

    print(
        f"{'Feature A':<40}"
        f"{'Feature B':<40}"
        f"{'Correlación':>12}"
    )

    print("-" * 94)

    for feature_a, feature_b, correlation, _ in correlations:

        if abs(correlation) >= 0.50:

            print(
                f"{feature_a:<40}"
                f"{feature_b:<40}"
                f"{correlation:>12.4f}"
            )

    # ---------------------------------------------------------
    # 4. Correlaciones fuertes
    # ---------------------------------------------------------

    strong_correlations = [
        item
        for item in correlations
        if item[3] >= 0.80
    ]

    print()
    print("=" * 70)
    print("4. CORRELACIONES FUERTES")
    print("=" * 70)
    print()

    if strong_correlations:

        for feature_a, feature_b, correlation, _ in strong_correlations:

            print(
                f"{feature_a} <-> {feature_b}"
            )

            print(
                f"   Correlación: {correlation:.4f}"
            )

            print()

    else:

        print(
            "No se encontraron correlaciones "
            "con |r| >= 0.80."
        )

    # ---------------------------------------------------------
    # 5. Correlaciones moderadas
    # ---------------------------------------------------------

    moderate_correlations = [
        item
        for item in correlations
        if 0.60 <= item[3] < 0.80
    ]

    print("=" * 70)
    print("5. CORRELACIONES MODERADAS")
    print("=" * 70)
    print()

    if moderate_correlations:

        for feature_a, feature_b, correlation, _ in moderate_correlations:

            print(
                f"{feature_a} <-> {feature_b}"
            )

            print(
                f"   Correlación: {correlation:.4f}"
            )

            print()

    else:

        print(
            "No se encontraron correlaciones "
            "entre 0.60 y 0.80."
        )

    # ---------------------------------------------------------
    # 6. Interpretación
    # ---------------------------------------------------------

    print("=" * 70)
    print("6. INTERPRETACIÓN")
    print("=" * 70)
    print()

    print(
        "Una correlación cercana a +1 indica que dos "
        "variables tienden a aumentar juntas."
    )

    print(
        "Una correlación cercana a -1 indica que cuando "
        "una aumenta, la otra tiende a disminuir."
    )

    print(
        "Una correlación cercana a 0 indica poca relación "
        "lineal entre las variables."
    )

    print()

    if strong_correlations:

        print(
            "ATENCIÓN:"
        )

        print(
            "Se encontraron features con correlación fuerte."
        )

        print(
            "Antes de eliminar variables debemos analizar "
            "si existe redundancia real y su efecto sobre "
            "el modelo."
        )

    else:

        print(
            "No se detectaron pares de features con "
            "correlación extremadamente alta."
        )

    print()
    print("=" * 70)
    print("ANÁLISIS COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    analyze_features()