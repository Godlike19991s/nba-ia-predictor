import pandas as pd


def transform_games(games: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte los registros de equipos de la NBA en partidos.

    Cada partido tendrá una única fila con:
    - equipo local
    - equipo visitante
    - puntos del local
    - puntos del visitante
    """

    games = games.copy()

    # Lista donde guardaremos los partidos transformados.
    transformed_games = []

    # Cada GAME_ID representa un partido.
    for game_id, group in games.groupby("GAME_ID"):

        # Un partido debe tener exactamente dos equipos.
        if len(group) != 2:
            continue

        # Tomamos el texto MATCHUP.
        matchup = group.iloc[0]["MATCHUP"]

        # --------------------------------------------------
        # Caso 1: formato "TEAM vs. OPPONENT"
        # --------------------------------------------------
        #
        # TEAM es el equipo local.
        #
        # Ejemplo:
        # OKC vs. IND
        #
        # OKC = local
        # IND = visitante
        #
        if "vs." in matchup:

            home_abbreviation = matchup.split("vs.")[0].strip()
            away_abbreviation = matchup.split("vs.")[1].strip()

        # --------------------------------------------------
        # Caso 2: formato "TEAM @ OPPONENT"
        # --------------------------------------------------
        #
        # TEAM es el visitante.
        #
        # Ejemplo:
        # IND @ OKC
        #
        # IND = visitante
        # OKC = local
        #
        elif "@" in matchup:

            away_abbreviation = matchup.split("@")[0].strip()
            home_abbreviation = matchup.split("@")[1].strip()

        else:
            # No conocemos el formato.
            continue

        # Buscamos el registro del equipo local.
        home_team = group[
            group["TEAM_ABBREVIATION"] == home_abbreviation
        ]

        # Buscamos el registro del equipo visitante.
        away_team = group[
            group["TEAM_ABBREVIATION"] == away_abbreviation
        ]

        # Si no encontramos ambos equipos, no podemos
        # construir correctamente el partido.
        if home_team.empty or away_team.empty:
            continue

        home_team = home_team.iloc[0]
        away_team = away_team.iloc[0]

        # Construimos una fila para nuestro partido.
        transformed_games.append(
            {
                "GAME_ID": game_id,
                "GAME_DATE": home_team["GAME_DATE"],
                "HOME_TEAM_ID": home_team["TEAM_ID"],
                "HOME_TEAM_ABBREVIATION": home_team[
                    "TEAM_ABBREVIATION"
                ],
                "HOME_TEAM_NAME": home_team["TEAM_NAME"],
                "AWAY_TEAM_ID": away_team["TEAM_ID"],
                "AWAY_TEAM_ABBREVIATION": away_team[
                    "TEAM_ABBREVIATION"
                ],
                "AWAY_TEAM_NAME": away_team["TEAM_NAME"],
                "HOME_POINTS": home_team["PTS"],
                "AWAY_POINTS": away_team["PTS"],
            }
        )

    # Convertimos nuestra lista en DataFrame.
    return pd.DataFrame(transformed_games)