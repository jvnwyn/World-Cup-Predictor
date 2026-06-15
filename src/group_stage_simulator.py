from predict_match import predict_match

groups = {
    "A": ["Mexico","South Africa","South Korea","Czech Republic"],
    "B": ["Canada","Switzerland","Qatar","Bosnia and Herzegovina"],
    "C": ["Brazil","Morocco","Haiti","Scotland"],
    "D": ["United States","Paraguay","Australia","Turkey"],
    "E": ["Germany","Curaçao","Ivory Coast","Ecuador"],
    "F": ["Netherlands","Japan","Tunisia","Sweden"],
    "G": ["Belgium","Egypt","Iran","New Zealand"],
    "H": ["Spain","Cape Verde","Saudi Arabia","Uruguay"],
    "I": ["France","Senegal","Norway","Iraq"],
    "J": ["Argentina","Algeria","Austria","Jordan"],
    "K": ["Portugal","Uzbekistan","Colombia","DR Congo"],
    "L": ["England","Croatia","Ghana","Panama"]
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

fixtures = []

for group in groups.values():
    fixtures.extend(
        generate_group_fixtures(group)
    )

group_tables = {}

for group_name, teams in groups.items():

    group_tables[group_name] = {}

    for team in teams:
        group_tables[group_name][team] = {
            "pts": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0
        }

for group_name, teams in groups.items():

    fixtures = generate_group_fixtures(teams)

    print(f"\nGROUP {group_name}")
    print("=" * 40)

    for home, away in fixtures:

        result = predict_match(home, away)

        table = group_tables[group_name]

        if result["prediction"] == 2:

            table[home]["pts"] += 3
            table[home]["wins"] += 1
            table[away]["losses"] += 1

        elif result["prediction"] == 0:

            table[away]["pts"] += 3
            table[away]["wins"] += 1
            table[home]["losses"] += 1

        else:

            table[home]["pts"] += 1
            table[away]["pts"] += 1

            table[home]["draws"] += 1
            table[away]["draws"] += 1

for group_name, table in group_tables.items():

    standings = sorted(
        table.items(),
        key=lambda x: x[1]["pts"],
        reverse=True
    )

    print(f"\nGROUP {group_name} STANDINGS")
    print("=" * 40)

    for pos, (team, stats) in enumerate(standings, start=1):

        print(
            f"{pos}. {team:<20}"
            f"{stats['pts']} pts"
        )

