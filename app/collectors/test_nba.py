from nba_api.stats.static import teams


def main():
    nba_teams = teams.get_teams()

    print(f"Equipos encontrados: {len(nba_teams)}")

    for team in nba_teams:
        print(team["full_name"])


if __name__ == "__main__":
    main()