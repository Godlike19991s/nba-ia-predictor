from sqlalchemy import text

from app.database.connection import SessionLocal


def calculate_rest_days() -> None:
    """Calcula y reconstruye los días de descanso y back-to-back."""

    print("=" * 60)
    print("CÁLCULO DE REST DAYS")
    print("=" * 60)
    print()

    session = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Obtener todos los partidos
        # ---------------------------------------------------------

        query = text(
            """
            SELECT
                s.game_id,
                s.team_id,
                g.game_date,
                LAG(g.game_date) OVER (
                    PARTITION BY s.team_id
                    ORDER BY g.game_date, s.game_id
                ) AS previous_game_date
            FROM team_game_stats s
            JOIN games g
                ON s.game_id = g.game_id
            ORDER BY
                s.team_id,
                g.game_date,
                s.game_id;
            """
        )

        results = session.execute(query).fetchall()

        print("1. Partidos analizados")
        print(f"   Registros encontrados: {len(results)}")
        print()

        # ---------------------------------------------------------
        # 2. Limpiar las features existentes
        # ---------------------------------------------------------
        #
        # team_game_features depende temporalmente de los partidos.
        # La reconstruimos completamente para evitar duplicados y
        # garantizar que todos los partidos tengan el mismo proceso.
        # ---------------------------------------------------------

        print("2. Limpiando team_game_features...")

        delete_query = text(
            """
            DELETE FROM team_game_features;
            """
        )

        deleted = session.execute(delete_query).rowcount

        print(f"   Registros eliminados: {deleted}")
        print()

        # ---------------------------------------------------------
        # 3. Preparar las nuevas features
        # ---------------------------------------------------------

        print("3. Calculando rest_days y back-to-back...")

        insert_query = text(
            """
            INSERT INTO team_game_features (
                game_id,
                team_id,
                rest_days,
                is_back_to_back
            )
            VALUES (
                :game_id,
                :team_id,
                :rest_days,
                :is_back_to_back
            );
            """
        )

        features = []

        first_games = 0
        back_to_backs = 0

        for row in results:

            # -----------------------------------------------------
            # Primer partido histórico del equipo
            # -----------------------------------------------------

            if row.previous_game_date is None:
                rest_days = None
                is_back_to_back = False

                first_games += 1

            # -----------------------------------------------------
            # Partidos posteriores
            # -----------------------------------------------------

            else:
                rest_days = (
                    row.game_date - row.previous_game_date
                ).days

                is_back_to_back = rest_days == 1

                if is_back_to_back:
                    back_to_backs += 1

            features.append(
                {
                    "game_id": row.game_id,
                    "team_id": row.team_id,
                    "rest_days": rest_days,
                    "is_back_to_back": is_back_to_back,
                }
            )

        # ---------------------------------------------------------
        # 4. Insertar todas las features
        # ---------------------------------------------------------

        session.execute(
            insert_query,
            features,
        )

        session.commit()

        # ---------------------------------------------------------
        # 5. Resultado
        # ---------------------------------------------------------

        print(f"   Registros insertados: {len(features)}")
        print(f"   Primeros partidos: {first_games}")
        print(f"   Back-to-back detectados: {back_to_backs}")
        print()

        print("=" * 60)
        print("REST DAYS CALCULADO CORRECTAMENTE")
        print("=" * 60)

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    calculate_rest_days()