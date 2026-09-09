import sys

import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder

from app.collectors.transform_games import transform_games


def get_games(season: str) -> pd.DataFrame:
    """Obtiene los registros de partidos de una temporada NBA."""

    finder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season
    )

    games = finder.get_data_frames()[0]

    # GAME_ID es un identificador, no una cantidad numérica.
    # Lo conservamos como texto para evitar perder ceros iniciales.
    games["GAME_ID"] = (
        games["GAME_ID"]
        .astype(str)
        .str.zfill(10)
    )

    return games


def main() -> None:
    """Descarga y transforma una temporada NBA."""

    # ---------------------------------------------------------
    # Validar argumentos
    # ---------------------------------------------------------

    if len(sys.argv) != 2:
        print("Uso:")
        print(
            "python -m app.collectors.games 2025-26"
        )
        return

    # ---------------------------------------------------------
    # Configuración
    # ---------------------------------------------------------

    season = sys.argv[1]

    # Por ahora trabajamos con temporada regular.
    # Posteriormente podremos extender el recolector para:
    # - Preseason
    # - Playoffs
    # - Play-In Tournament
    season_type = "Regular Season"

    print(
        f"Descargando datos de la temporada {season}..."
    )

    print(
        f"Tipo de temporada: {season_type}"
    )

    # ---------------------------------------------------------
    # Descargar datos
    # ---------------------------------------------------------

    games = get_games(season)

    print(
        f"Registros originales: {len(games)}"
    )

    # ---------------------------------------------------------
    # Transformar datos
    # ---------------------------------------------------------

    print("Transformando partidos...")

    transformed_games = transform_games(
        games,
        season_type,
    )

    print(
        f"Partidos transformados: "
        f"{len(transformed_games)}"
    )

    # ---------------------------------------------------------
    # Guardar datos RAW
    # ---------------------------------------------------------

    raw_file = (
        f"data/raw/games_{season}.csv"
    )

    games.to_csv(
        raw_file,
        index=False,
        encoding="utf-8",
    )

    print(
        f"Datos RAW guardados en: {raw_file}"
    )

    # ---------------------------------------------------------
    # Guardar datos procesados
    # ---------------------------------------------------------

    processed_file = (
        f"data/processed/games_{season}.csv"
    )

    transformed_games.to_csv(
        processed_file,
        index=False,
        encoding="utf-8",
    )

    print(
        f"Datos procesados guardados en: "
        f"{processed_file}"
    )


if __name__ == "__main__":
    main()