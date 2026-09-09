from sqlalchemy import text

from app.database.connection import SessionLocal


# ============================================================
# CONFIGURACIÓN DEL MODELO ELO
# ============================================================

INITIAL_ELO = 1500.0

K_FACTOR = 20.0

HOME_ADVANTAGE = 100.0


# ============================================================
# FUNCIONES ELO
# ============================================================


def calculate_expected_score(
    home_elo: float,
    away_elo: float,
) -> float:
    """
    Calcula la probabilidad esperada de victoria del
    equipo local.

    Se incorpora una ventaja de localía al ELO del
    equipo que juega en casa.
    """

    home_elo_adjusted = (
        home_elo + HOME_ADVANTAGE
    )

    exponent = (
        -(home_elo_adjusted - away_elo)
        / 400.0
    )

    expected_home = (
        1.0
        / (1.0 + 10.0 ** exponent)
    )

    return expected_home


def update_elo(
    home_elo: float,
    away_elo: float,
    home_score: int,
    away_score: int,
) -> tuple[float, float]:
    """
    Actualiza los ratings ELO después de un partido.
    """

    expected_home = calculate_expected_score(
        home_elo,
        away_elo,
    )

    expected_away = 1.0 - expected_home

    if home_score > away_score:
        actual_home = 1.0
        actual_away = 0.0

    elif home_score < away_score:
        actual_home = 0.0
        actual_away = 1.0

    else:
        actual_home = 0.5
        actual_away = 0.5

    new_home_elo = (
        home_elo
        + K_FACTOR
        * (actual_home - expected_home)
    )

    new_away_elo = (
        away_elo
        + K_FACTOR
        * (actual_away - expected_away)
    )

    return new_home_elo, new_away_elo


# ============================================================
# PROCESO PRINCIPAL
# ============================================================


def calculate_elo() -> None:
    """
    Calcula el ELO histórico de todos los equipos.

    Para cada partido:

    1. Obtiene el ELO actual de ambos equipos.
    2. Guarda esos valores como ELO previo al partido.
    3. Calcula elo_diff.
    4. Actualiza los ratings después del partido.
    """

    print("Calculando ELO histórico...")

    session = SessionLocal()

    try:
        # ----------------------------------------------------
        # Obtener todos los partidos en orden cronológico.
        # ----------------------------------------------------

        query = text(
            """
            SELECT
                game_id,
                game_date,
                home_team_id,
                away_team_id,
                home_points,
                away_points
            FROM games
            ORDER BY
                game_date,
                game_id;
            """
        )

        games = session.execute(query).fetchall()

        print(
            f"Partidos analizados: {len(games)}"
        )

        # ----------------------------------------------------
        # Diccionario donde almacenaremos el ELO actual
        # de cada equipo.
        #
        # Ejemplo:
        #
        # {
        #     1610612747: 1542.3,
        #     1610612738: 1587.6
        # }
        # ----------------------------------------------------

        elo_ratings: dict[int, float] = {}

        updated = 0

        # ----------------------------------------------------
        # Procesar partido por partido.
        # ----------------------------------------------------

        for game in games:

            home_team_id = game.home_team_id
            away_team_id = game.away_team_id

            # -----------------------------------------------
            # Si el equipo nunca apareció antes,
            # comienza con INITIAL_ELO.
            # -----------------------------------------------

            home_elo = elo_ratings.get(
                home_team_id,
                INITIAL_ELO,
            )

            away_elo = elo_ratings.get(
                away_team_id,
                INITIAL_ELO,
            )

            # -----------------------------------------------
            # IMPORTANTE:
            #
            # Estos son los ELO ANTES del partido.
            # -----------------------------------------------

            elo_diff = (
                home_elo - away_elo
            )

            # -----------------------------------------------
            # Guardamos el ELO previo al partido.
            # -----------------------------------------------

            update_query = text(
                """
                UPDATE game_features
                SET
                    home_elo = :home_elo,
                    away_elo = :away_elo,
                    elo_diff = :elo_diff
                WHERE game_id = :game_id;
                """
            )

            session.execute(
                update_query,
                {
                    "home_elo": home_elo,
                    "away_elo": away_elo,
                    "elo_diff": elo_diff,
                    "game_id": game.game_id,
                },
            )

            # -----------------------------------------------
            # Actualizamos el ELO DESPUÉS del partido.
            # -----------------------------------------------

            new_home_elo, new_away_elo = update_elo(
                home_elo,
                away_elo,
                game.home_points,
                game.away_points,
            )

            elo_ratings[home_team_id] = new_home_elo
            elo_ratings[away_team_id] = new_away_elo

            updated += 1

        session.commit()

        print(
            "ELO calculado correctamente: "
            f"{updated}"
        )

        print(
            f"Equipos con rating: "
            f"{len(elo_ratings)}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_elo()