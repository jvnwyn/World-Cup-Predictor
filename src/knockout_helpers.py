from predict_match import predict_match


def play_knockout_match(home, away):

    result = predict_match(home, away, verbose=False)

    print(f"\n{home} vs {away}")

    print(
        f"{away} Win: {result['away_probability']:.2%}\n"
        f"Draw: {result['draw_probability']:.2%}\n"
        f"{home} Win: {result['home_probability']:.2%}"
    )

    if result["prediction"] == 2:
        winner = home

    elif result["prediction"] == 0:
        winner = away

    else:
        print("Draw after 90 minutes")

        # Higher win probability advances (penalty shootout simulation)
        if result["home_probability"] >= result["away_probability"]:
            winner = home
        else:
            winner = away

        print(f"Winner after penalties: {winner}")

    print(f"Winner: {winner}")

    return winner