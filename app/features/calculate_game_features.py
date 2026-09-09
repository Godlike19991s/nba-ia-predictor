from sqlalchemy import text

from app.database.connection import SessionLocal


def calculate_game_features() -> None:
    """
    Calcula las características comparativas de cada partido.

    Las características se calculan utilizando únicamente
    información disponible antes del partido.
    """

    print("Calculando características de los partidos...")

    session = SessionLocal()

    try:
        query = text(
            """
            SELECT
                g.game_id,

                home.team_id AS home_team_id,
                away.team_id AS away_team_id,

                home.avg_offensive_rating_last_5
                    AS home_avg_offensive_rating_last_5,

                away.avg_offensive_rating_last_5
                    AS away_avg_offensive_rating_last_5,

                home.avg_defensive_rating_last_5
                    AS home_avg_defensive_rating_last_5,

                away.avg_defensive_rating_last_5
                    AS away_avg_defensive_rating_last_5,

                home.avg_net_rating_last_5
                    AS home_avg_net_rating_last_5,

                away.avg_net_rating_last_5
                    AS away_avg_net_rating_last_5,

                home.rest_days
                    AS home_rest_days,

                away.rest_days
                    AS away_rest_days,

                home.is_back_to_back
                    AS home_is_back_to_back,

                away.is_back_to_back
                    AS away_is_back_to_back

            FROM games g

            JOIN team_game_features home
                ON home.game_id = g.game_id
                AND home.team_id = g.home_team_id

            JOIN team_game_features away
                ON away.game_id = g.game_id
                AND away.team_id = g.away_team_id

            ORDER BY
                g.game_date,
                g.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print(f"Registros analizados: {len(results)}")

        inserted = 0
        updated = 0
        skipped = 0

        for row in results:

            # --------------------------------------------------
            # Validar características de eficiencia
            # --------------------------------------------------

            if (
                row.home_avg_offensive_rating_last_5 is None
                or row.away_avg_offensive_rating_last_5 is None
                or row.home_avg_defensive_rating_last_5 is None
                or row.away_avg_defensive_rating_last_5 is None
                or row.home_avg_net_rating_last_5 is None
                or row.away_avg_net_rating_last_5 is None
            ):
                skipped += 1
                continue

            # --------------------------------------------------
            # Diferencias de eficiencia
            # --------------------------------------------------

            offensive_rating_diff = (
                row.home_avg_offensive_rating_last_5
                - row.away_avg_offensive_rating_last_5
            )

            defensive_rating_diff = (
                row.home_avg_defensive_rating_last_5
                - row.away_avg_defensive_rating_last_5
            )

            net_rating_diff = (
                row.home_avg_net_rating_last_5
                - row.away_avg_net_rating_last_5
            )

            # --------------------------------------------------
            # Características de descanso
            # --------------------------------------------------

            home_rest_days = row.home_rest_days
            away_rest_days = row.away_rest_days

            if (
                home_rest_days is not None
                and away_rest_days is not None
            ):
                rest_days_diff = (
                    home_rest_days
                    - away_rest_days
                )
            else:
                rest_days_diff = None

            home_is_back_to_back = (
                row.home_is_back_to_back
            )

            away_is_back_to_back = (
                row.away_is_back_to_back
            )

            # --------------------------------------------------
            # Actualizar el partido
            # --------------------------------------------------

            update_query = text(
                """
                UPDATE game_features
                SET
                    offensive_rating_diff =
                        :offensive_rating_diff,

                    defensive_rating_diff =
                        :defensive_rating_diff,

                    net_rating_diff =
                        :net_rating_diff,

                    home_rest_days =
                        :home_rest_days,

                    away_rest_days =
                        :away_rest_days,

                    rest_days_diff =
                        :rest_days_diff,

                    home_is_back_to_back =
                        :home_is_back_to_back,

                    away_is_back_to_back =
                        :away_is_back_to_back

                WHERE game_id = :game_id;
                """
            )

            result = session.execute(
                update_query,
                {
                    "offensive_rating_diff":
                        offensive_rating_diff,

                    "defensive_rating_diff":
                        defensive_rating_diff,

                    "net_rating_diff":
                        net_rating_diff,

                    "home_rest_days":
                        home_rest_days,

                    "away_rest_days":
                        away_rest_days,

                    "rest_days_diff":
                        rest_days_diff,

                    "home_is_back_to_back":
                        home_is_back_to_back,

                    "away_is_back_to_back":
                        away_is_back_to_back,

                    "game_id":
                        row.game_id,
                },
            )

            if result.rowcount == 1:
                updated += 1

        session.commit()

        print(
            f"Características actualizadas correctamente: "
            f"{updated}"
        )

        print(
            f"Partidos omitidos por falta de datos históricos: "
            f"{skipped}"
        )

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_game_features()