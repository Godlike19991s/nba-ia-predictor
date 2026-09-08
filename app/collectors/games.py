import pandas as pd

from nba_api.stats.endpoints import leaguegamefinder

from transform_games import transform_games


def get_games(season: str) -> pd.DataFrame:
    """Obtiene los registros de partidos de una temporada NBA."""

    finder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season
    )

    games = finder.get_data_frames()[0]

# GAME_ID es un identificador, no una cantidad numérica.
# Lo conservamos como texto para evitar perder ceros iniciales.
games["GAME_ID"] = games["GAME_ID"].astype(str).str.zfill(10)

return games


def main():
    season = "2024-25"

    print(f"Descargando datos de la temporada {season}...")

    games = get_games(season)

    print(f"Registros originales: {len(games)}")

    print("Transformando partidos...")

    transformed_games = transform_games(games)

    print(f"Partidos transformados: {len(transformed_games)}")

    # ---------------------------------------------------------
    # Guardamos los datos originales.
    # ---------------------------------------------------------

    raw_file = f"data/raw/games_{season}.csv"

    games.to_csv(
        raw_file,
        index=False,
        encoding="utf-8",
    )

    print(f"Datos RAW guardados en: {raw_file}")

    # ---------------------------------------------------------
    # Guardamos los datos transformados.
    # ---------------------------------------------------------

    processed_file = f"data/processed/games_{season}.csv"

    transformed_games.to_csv(
        processed_file,
        index=False,
        encoding="utf-8",
    )

    print(f"Datos procesados guardados en: {processed_file}")


if __name__ == "__main__":
    main()