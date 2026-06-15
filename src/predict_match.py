import pickle
import pandas as pd
import random

# Load model
with open("models/logistic_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load scaler
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

elo_df = pd.read_csv("data/worldcup_elo.csv")
stats_df = pd.read_csv("data/worldcup_team_stats.csv")

stats_df["form"] = stats_df["form"].fillna(0.5)
stats_df["avg_scored"] = stats_df["avg_scored"].fillna(1.0)
stats_df["avg_conceded"] = stats_df["avg_conceded"].fillna(1.0)

def get_elo(team):
    row = elo_df[elo_df["team"] == team]

    if row.empty:
        raise ValueError(f"Team not found: {team}")

    return row.iloc[0]["elo"]


def get_stats(team):
    row = stats_df[stats_df["team"] == team]

    if row.empty:
        raise ValueError(f"Team not found: {team}")

    return row.iloc[0]


def predict_match(home_team, away_team):

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    home_stats = get_stats(home_team)
    away_stats = get_stats(away_team)

    features = pd.DataFrame([{
        "elo_difference": home_elo - away_elo,

        "form_difference":
            home_stats["form"] - away_stats["form"],

        "goal_difference":
            (
                home_stats["avg_scored"]
                - home_stats["avg_conceded"]
            )
            -
            (
                away_stats["avg_scored"]
                - away_stats["avg_conceded"]
            )
    }])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]

    if prediction == 2:
        result_text = f"{home_team} Win"
    elif prediction == 0:
        result_text = f"{away_team} Win"
    else:
        result_text = "Draw"

    print(f"\n{home_team} vs {away_team}")
    print(f"Prediction: {result_text}")

    print("\nProbabilities:")
    print(f"{away_team} Win: {probabilities[0]*100:.2f}%")
    print(f"Draw:           {probabilities[1]*100:.2f}%")
    print(f"{home_team} Win: {probabilities[2]*100:.2f}%")

    return {
        "prediction": prediction,
        "away_win": probabilities[0],
        "draw": probabilities[1],
        "home_win": probabilities[2]
    }

if __name__ == "__main__":
    predict_match("Japan", "Netherlands")
