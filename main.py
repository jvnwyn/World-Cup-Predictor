import pandas as pd

# Load data
df = pd.read_csv("data/results.csv")

# Convert the data column
df["date"] = pd.to_datetime(df["date"])

# Keep only the matches from World Cup 2014 onwards
df = df[df["date"] >= "2014-01-01"]

# Sort by date
df = df.sort_values("date")

# Add result labels
def get_result(row):
    if row["home_score"] > row["away_score"]:
        return 2
    elif row["home_score"] < row["away_score"]:
        return 0
    else:
        return 1
    
df["result"] = df.apply(get_result, axis=1)

# Home Advantage
df["home_advantage"] = (~df["neutral"]).astype(int)

# Recent Form
team_history = {}

home_form = []
away_form = []

def calculate_form(team):
    if team not in team_history:
        return 0.5

    last_five = team_history[team][-5:]

    if len(last_five) == 0:
        return 0.5
    
    return sum(last_five) / (len(last_five) * 3)

for _, row in df.iterrows():
    home_team = row["home_team"]
    away_team = row["away_team"]

    home_form.append(calculate_form(home_team))
    away_form.append(calculate_form(away_team))

    # Determine match points

    if row["home_score"] > row["away_score"]:
        home_points = 3
        away_points = 0
    elif row["home_score"] < row["away_score"]:
        home_points = 0
        away_points = 3
    else:
        home_points = 1
        away_points = 1
    
    if home_team not in team_history:
        team_history[home_team] = []

    if away_team not in team_history:
        team_history[away_team] = []    
    
    team_history[home_team].append(home_points)
    team_history[away_team].append(away_points)

df["home_form"] = home_form
df["away_form"] = away_form

# Goals scored and conceded
goal_history_scored = {}
goal_history_conceded = {}

home_avg_scored = []
away_avg_scored = []

home_avg_conceded = []
away_avg_conceded = []

def calculate_average(values):
    if len(values) == 0:
        return 1.0

    last_five = values[-5:]

    return sum(last_five) / len(last_five)        

for _, row in df.iterrows():

    home_team = row["home_team"]
    away_team = row["away_team"]

    # Initialize teams

    if home_team not in goal_history_scored:
        goal_history_scored[home_team] = []
        goal_history_conceded[home_team] = []

    if away_team not in goal_history_scored:
        goal_history_scored[away_team] = []
        goal_history_conceded[away_team] = []

    # Get averages BEFORE current match

    home_avg_scored.append(
        calculate_average(
            goal_history_scored[home_team]
        )
    )

    away_avg_scored.append(
        calculate_average(
            goal_history_scored[away_team]
        )
    )

    home_avg_conceded.append(
        calculate_average(
            goal_history_conceded[home_team]
        )
    )

    away_avg_conceded.append(
        calculate_average(
            goal_history_conceded[away_team]
        )
    )

    # Update history AFTER current match

    goal_history_scored[home_team].append(
        row["home_score"]
    )

    goal_history_conceded[home_team].append(
        row["away_score"]
    )

    goal_history_scored[away_team].append(
        row["away_score"]
    )

    goal_history_conceded[away_team].append(
        row["home_score"]
    )

df["home_avg_scored"] = home_avg_scored
df["away_avg_scored"] = away_avg_scored

df["home_avg_conceded"] = home_avg_conceded
df["away_avg_conceded"] = away_avg_conceded

df["form_difference"] = (
    df["home_form"] - df["away_form"]
)

df["goal_difference"] = (
    (df["home_avg_scored"] - df["home_avg_conceded"])
    -
    (df["away_avg_scored"] - df["away_avg_conceded"])
)

df["form_difference"] = (
    df["home_form"] -
    df["away_form"]
)

df["goal_difference"] = (
    (df["home_avg_scored"] - df["home_avg_conceded"])
    -
    (df["away_avg_scored"] - df["away_avg_conceded"])
)

# Elo Ratings

INITIAL_ELO = 1500
K = 20

elo_ratings = {}

home_elos = []
away_elos = []
elo_differences = []

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

for _, row in df.iterrows():

    home_team = row["home_team"]
    away_team = row["away_team"]

    if home_team not in elo_ratings:
        elo_ratings[home_team] = INITIAL_ELO

    if away_team not in elo_ratings:
        elo_ratings[away_team] = INITIAL_ELO

    home_elo = elo_ratings[home_team]
    away_elo = elo_ratings[away_team]

    # Save ratings BEFORE match
    home_elos.append(home_elo)
    away_elos.append(away_elo)
    elo_differences.append(home_elo - away_elo)

    # Actual result
    if row["home_score"] > row["away_score"]:
        actual_home = 1
        actual_away = 0

    elif row["home_score"] < row["away_score"]:
        actual_home = 0
        actual_away = 1

    else:
        actual_home = 0.5
        actual_away = 0.5

    # Expected result
    HOME_ADVANTAGE_ELO = 100

    expected_home = expected_score(
        home_elo + HOME_ADVANTAGE_ELO,
        away_elo
    )

    expected_away = expected_score(
        away_elo,
        home_elo
    )

    # Update ratings
    elo_ratings[home_team] = (
        home_elo +
        K * (actual_home - expected_home)
    )

    elo_ratings[away_team] = (
        away_elo +
        K * (actual_away - expected_away)
    )

df["home_elo"] = home_elos
df["away_elo"] = away_elos
df["elo_difference"] = elo_differences

print(
    df[
        [
            "home_team",
            "away_team",
            "home_elo",
            "away_elo",
            "elo_difference"
        ]
    ].head(10)
)

# Create latest Elo ratings for each team

latest_elo = {}

for _, row in df.iterrows():
    latest_elo[row["home_team"]] = row["home_elo"]
    latest_elo[row["away_team"]] = row["away_elo"]

elo_df = pd.DataFrame(
    list(latest_elo.items()),
    columns=["team", "elo"]
)

elo_df.to_csv(
    "data/latest_elo.csv",
    index=False
)

print("Latest Elo ratings saved!")

team_stats = []

teams = set(df["home_team"]).union(
    set(df["away_team"])
)

for team in teams:

    recent_matches = df[
        (df["home_team"] == team) |
        (df["away_team"] == team)
    ].tail(5)

    points = 0
    scored = 0
    conceded = 0

    for _, row in recent_matches.iterrows():

        if row["home_team"] == team:

            scored += row["home_score"]
            conceded += row["away_score"]

            if row["home_score"] > row["away_score"]:
                points += 3
            elif row["home_score"] == row["away_score"]:
                points += 1

        else:

            scored += row["away_score"]
            conceded += row["home_score"]

            if row["away_score"] > row["home_score"]:
                points += 3
            elif row["away_score"] == row["home_score"]:
                points += 1

    matches_played = len(recent_matches)

    team_stats.append({
        "team": team,
        "form": points / (matches_played * 3) if matches_played else 0.5,
        "avg_scored": scored / matches_played if matches_played else 1.0,
        "avg_conceded": conceded / matches_played if matches_played else 1.0
    })

stats_df = pd.DataFrame(team_stats)

stats_df.to_csv(
    "data/team_stats.csv",
    index=False
)

print("Team stats saved!")

# Save the processed data
df.to_csv(
    "data/matches_2014_present.csv", index=False
)

print("Saved successfully!")
