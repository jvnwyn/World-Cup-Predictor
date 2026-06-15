import pandas as pd

# Load match results
results = pd.read_csv("data/results.csv")
results["date"] = pd.to_datetime(results["date"])

worldcup_teams = [
    "Argentina","Spain","France","England","Portugal","Brazil",
    "Morocco","Netherlands","Belgium","Germany","Croatia","Mexico",
    "Colombia","United States","Senegal","Uruguay","Japan","Switzerland",
    "Iran","South Korea","Turkey","Ecuador","Austria","Australia",
    "Algeria","Egypt","Norway","Canada","Ivory Coast","Panama",
    "Scotland","Sweden","Paraguay","Czech Republic","Tunisia",
    "DR Congo","Qatar","Uzbekistan","Iraq","Saudi Arabia",
    "South Africa","Bosnia and Herzegovina","Jordan","Cape Verde",
    "Ghana","Haiti","Curaçao","New Zealand"
]

# All team names that exist in results.csv
all_teams = set(results["home_team"]).union(
    set(results["away_team"])
)

team_stats = []
missing_teams = []

for team in worldcup_teams:

    if team not in all_teams:
        missing_teams.append(team)
        continue

    matches = results[
        (results["home_team"] == team) |
        (results["away_team"] == team)
    ]

    matches = matches.sort_values(
        "date",
        ascending=False
    ).head(5)

    points = 0
    goals_scored = 0
    goals_conceded = 0

    for _, match in matches.iterrows():

        if match["home_team"] == team:

            scored = match["home_score"]
            conceded = match["away_score"]

            if scored > conceded:
                points += 3
            elif scored == conceded:
                points += 1

        else:

            scored = match["away_score"]
            conceded = match["home_score"]

            if scored > conceded:
                points += 3
            elif scored == conceded:
                points += 1

        goals_scored += scored
        goals_conceded += conceded

    team_stats.append({
        "team": team,
        "form": round(points / 15, 3),
        "avg_scored": round(goals_scored / len(matches), 3),
        "avg_conceded": round(goals_conceded / len(matches), 3)
    })

stats_df = pd.DataFrame(team_stats)

stats_df.to_csv(
    "data/worldcup_team_stats.csv",
    index=False
)

print("\nFirst 10 teams:")
print(stats_df.head(10))

print(f"\nSaved {len(stats_df)} teams.")