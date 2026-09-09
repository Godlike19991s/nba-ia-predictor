from math import isfinite

from app.ml.create_dataset import FEATURE_COLUMNS, build_dataset


def validate_dataset() -> None:
    """Valida la estructura y calidad del dataset de Machine Learning."""

    print("Validando dataset de Machine Learning...")
    print()

    feature_data, targets = build_dataset()

    # ---------------------------------------------------------
    # 1. Dimensiones
    # ---------------------------------------------------------

    print("1. Dimensiones")

    print(f"   Registros: {len(feature_data)}")
    print(f"   Features: {len(FEATURE_COLUMNS)}")
    print(f"   Targets: {len(targets)}")
    print()

    if len(feature_data) != len(targets):
        raise ValueError(
            "Features y targets tienen diferente número de registros."
        )

    for row_index, row in enumerate(feature_data, start=1):
        if len(row) != len(FEATURE_COLUMNS):
            raise ValueError(
                f"El registro {row_index} tiene {len(row)} features, "
                f"pero se esperaban {len(FEATURE_COLUMNS)}."
            )

    # ---------------------------------------------------------
    # 2. Nombres de las features
    # ---------------------------------------------------------

    print("2. Features utilizadas")

    for index, column in enumerate(FEATURE_COLUMNS, start=1):
        print(f"   {index}. {column}")

    print()

    # ---------------------------------------------------------
    # 3. Validar valores faltantes
    # ---------------------------------------------------------

    print("3. Valores faltantes")

    missing_values = 0

    for row_index, row in enumerate(feature_data, start=1):
        for column_index, value in enumerate(row):

            if value is None:
                print(
                    f"   ERROR - Registro {row_index}, "
                    f"feature '{FEATURE_COLUMNS[column_index]}' es NULL."
                )
                missing_values += 1

    if missing_values == 0:
        print("   OK - No existen valores faltantes.")
    else:
        raise ValueError(
            f"El dataset contiene {missing_values} valores faltantes."
        )

    print()

    # ---------------------------------------------------------
    # 4. Validar valores infinitos
    # ---------------------------------------------------------

    print("4. Valores infinitos")

    infinite_values = 0

    for row_index, row in enumerate(feature_data, start=1):
        for column_index, value in enumerate(row):

            if isinstance(value, (int, float)) and not isfinite(value):
                print(
                    f"   ERROR - Registro {row_index}, "
                    f"feature '{FEATURE_COLUMNS[column_index]}' "
                    f"contiene un valor infinito."
                )
                infinite_values += 1

    if infinite_values == 0:
        print("   OK - No existen valores infinitos.")
    else:
        raise ValueError(
            f"El dataset contiene {infinite_values} valores infinitos."
        )

    print()

    # ---------------------------------------------------------
    # 5. Validar tipos numéricos
    # ---------------------------------------------------------

    print("5. Tipos de datos")

    non_numeric_values = 0

    for row_index, row in enumerate(feature_data, start=1):
        for column_index, value in enumerate(row):

            if not isinstance(value, (int, float)):
                print(
                    f"   ERROR - Registro {row_index}, "
                    f"feature '{FEATURE_COLUMNS[column_index]}' "
                    f"no es numérica."
                )
                non_numeric_values += 1

    if non_numeric_values == 0:
        print("   OK - Todas las features son numéricas.")
    else:
        raise ValueError(
            f"Se encontraron {non_numeric_values} valores no numéricos."
        )

    print()

    # ---------------------------------------------------------
    # 6. Distribución del target
    # ---------------------------------------------------------

    print("6. Distribución del target")

    home_wins = sum(targets)
    away_wins = len(targets) - home_wins

    home_percentage = (
        home_wins / len(targets) * 100
        if targets
        else 0
    )

    away_percentage = (
        away_wins / len(targets) * 100
        if targets
        else 0
    )

    print(
        f"   Target 1 - Victoria local: "
        f"{home_wins} ({home_percentage:.2f}%)"
    )

    print(
        f"   Target 0 - Victoria visitante: "
        f"{away_wins} ({away_percentage:.2f}%)"
    )

    print()

    # ---------------------------------------------------------
    # 7. Validar valores del target
    # ---------------------------------------------------------

    print("7. Valores del target")

    invalid_targets = [
        target
        for target in targets
        if target not in (0, 1)
    ]

    if not invalid_targets:
        print(
            "   OK - El target contiene únicamente 0 y 1."
        )
    else:
        raise ValueError(
            f"Se encontraron {len(invalid_targets)} "
            "targets inválidos."
        )

    print()

    # ---------------------------------------------------------
    # Resultado final
    # ---------------------------------------------------------

    print("=" * 60)
    print("VALIDACIÓN EXITOSA")
    print("=" * 60)
    print()
    print("El dataset está listo para la siguiente etapa.")


if __name__ == "__main__":
    validate_dataset()