def generate_round_of_32(group_tables, third_place):

    winners = {}
    runners_up = {}

    # Determine winners/runners-up

    for group, table in group_tables.items():

        standings = sorted(
            table.items(),
            key=lambda x: (
                x[1]["pts"],
                x[1]["wins"]
            ),
            reverse=True
        )

        winners[group] = standings[0][0]
        runners_up[group] = standings[1][0]

    # Rank third-place teams

    ranked_third = sorted(
        third_place,
        key=lambda x: (
            x["pts"],
            x["wins"]
        ),
        reverse=True
    )

    ranked_third = ranked_third[:8]

    # Highest-ranked third-place
    T1 = ranked_third[0]["team"]
    T2 = ranked_third[1]["team"]
    T3 = ranked_third[2]["team"]
    T4 = ranked_third[3]["team"]
    T5 = ranked_third[4]["team"]
    T6 = ranked_third[5]["team"]
    T7 = ranked_third[6]["team"]
    T8 = ranked_third[7]["team"]

    fixtures = [

        # Group winners vs best 3rd-place teams
        (winners["A"], T8),
        (winners["B"], T7),
        (winners["C"], T6),
        (winners["D"], T5),
        (winners["E"], T4),
        (winners["F"], T3),
        (winners["G"], T2),
        (winners["H"], T1),

        # Remaining group winners
        (winners["I"], runners_up["J"]),
        (winners["J"], runners_up["I"]),
        (winners["K"], runners_up["L"]),
        (winners["L"], runners_up["K"]),

        # Remaining runners-up
        (runners_up["A"], runners_up["B"]),
        (runners_up["C"], runners_up["D"]),
        (runners_up["E"], runners_up["F"]),
        (runners_up["G"], runners_up["H"])
    ]

    return fixtures