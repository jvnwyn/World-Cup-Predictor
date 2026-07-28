from predict_match import predict_match

groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Switzerland", "Qatar", "Bosnia and Herzegovina"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Tunisia", "Sweden"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Norway", "Iraq"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "Uzbekistan", "Colombia", "DR Congo"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}


def generate_group_fixtures(group):

    a, b, c, d = group

    return [
        (a, b),
        (c, d),
        (a, c),
        (b, d),
        (a, d),
        (b, c)
    ]

def head_to_head_winner(team1, team2, table):
    """
    Returns:
        1 if team1 beat team2
       -1 if team2 beat team1
        0 if they drew
    """

    result = table[team1]["head_to_head"][team2]

    if result == 2:
        return 1

    elif result == 0:
        return -1

    return 0

def simulate_group_stage():

    group_tables = {}

    # Initialize tables
    for group_name, teams in groups.items():

        group_tables[group_name] = {}

        for team in teams:

            group_tables[group_name][team] = {
                "pts": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "head_to_head": {}
            }

    # Simulate every group
    for group_name, teams in groups.items():

        fixtures = generate_group_fixtures(teams)

        table = group_tables[group_name]

        for home, away in fixtures:

            result = predict_match(home, away, verbose=False)

            # Save head-to-head result
            table[home]["head_to_head"][away] = result["prediction"]

            if result["prediction"] == 2:
                table[away]["head_to_head"][home] = 0
            elif result["prediction"] == 0:
                table[away]["head_to_head"][home] = 2
            else:
                table[away]["head_to_head"][home] = 1

            if result["prediction"] == 2:

                table[home]["wins"] += 1
                table[home]["pts"] += 3
                table[away]["losses"] += 1

            elif result["prediction"] == 0:

                table[away]["wins"] += 1
                table[away]["pts"] += 3
                table[home]["losses"] += 1

            else:

                table[home]["draws"] += 1
                table[away]["draws"] += 1

                table[home]["pts"] += 1
                table[away]["pts"] += 1

    print("\nGROUP STAGE STANDINGS")
    print("=" * 70)

    qualified = []
    third_place = []

    for group_name, table in group_tables.items():

        standings = sorted(
            table.items(),
                key=lambda x: (
                    x[1]["pts"],
                    x[1]["wins"]
                ),
                reverse=True
            )
        
        # Apply head-to-head for adjacent tied teams
        for i in range(len(standings) - 1):

            team1, stats1 = standings[i]
            team2, stats2 = standings[i + 1]

            if (
                stats1["pts"] == stats2["pts"]
                and stats1["wins"] == stats2["wins"]
            ):

                winner = head_to_head_winner(team1, team2, table)

                if winner == -1:
                    standings[i], standings[i + 1] = standings[i + 1], standings[i]

        print(f"\nGROUP {group_name}")
        print("=" * 70)
        print(f"{'Pos':<4}{'Team':<24}{'W':>4}{'D':>4}{'L':>4}{'Pts':>6}")
        print("-" * 70)

        for pos, (team, stats) in enumerate(standings, start=1):

            print(
                f"{pos:<4}"
                f"{team:<24}"
                f"{stats['wins']:>4}"
                f"{stats['draws']:>4}"
                f"{stats['losses']:>4}"
                f"{stats['pts']:>6}"
            )

        # Top 2 qualify automatically
        qualified.append(standings[0][0])
        qualified.append(standings[1][0])

        # Save third-place team
        third_place.append({
            "group": group_name,
            "team": standings[2][0],
            "pts": standings[2][1]["pts"],
            "wins": standings[2][1]["wins"]
        })

    return {
        "qualified": qualified,
        "third_place": third_place,
        "tables": group_tables
    }


if __name__ == "__main__":

    results = simulate_group_stage()

    print("\nAUTOMATIC QUALIFIERS")
    print("=" * 70)

    for team in results["qualified"]:
        print(team)

    print("\nTHIRD-PLACE TEAMS")
    print("=" * 70)

    for team in results["third_place"]:
        print(
            f"{team['group']} - "
            f"{team['team']} "
            f"({team['pts']} pts)"
        )

    # Rank the third-place teams
    best_third = sorted(
        results["third_place"],
        key=lambda x: (
            x["pts"],
            x["wins"]
        ),
        reverse=True
    )

    print("\nBEST THIRD-PLACE TEAMS")
    print("=" * 70)
    print(f"{'Rank':<6}{'Team':<22}{'Group':<8}{'Pts':<6}{'Status'}")
    print("-" * 70)

    qualified_third = []

    for rank, team in enumerate(best_third, start=1):

        status = "QUALIFIED" if rank <= 8 else "ELIMINATED"

        print(
            f"{rank:<6}"
            f"{team['team']:<22}"
            f"{team['group']:<8}"
            f"{team['pts']:<6}"
            f"{status}"
        )

        if rank <= 8:
            qualified_third.append(team["team"])

    print("\nBEST 8 THIRD-PLACE QUALIFIERS")
    print("=" * 70)

    for team in qualified_third:
        print(team)    