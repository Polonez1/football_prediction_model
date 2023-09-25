import sys

sys.path.append(f"./scraping/")

import scraping_elo


def get_team_stats(home_team: str, away_team: str):
    print("start")
    home_team_elo = scraping_elo.get_elo_by_team(team=home_team)
    away_team = scraping_elo.get_elo_by_team(team=away_team)

    return home_team, away_team


if "__main__" == __name__:
    a, b = get_team_stats(
        home_team="Tottenham Hotspur", away_team="Wolverhampton Wanderers"
    )
    print(a, b)
