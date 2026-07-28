from group_stage_simulator import simulate_group_stage
from generate_round_of_32 import generate_round_of_32
from knockout_helpers import play_knockout_match


# Simulate the group stage
results = simulate_group_stage()

# Automatically generate the Round of 32 bracket
fixtures = generate_round_of_32(
    results["tables"],
    results["third_place"]
)

print("\nROUND OF 32")
print("=" * 60)

for match_number, (home, away) in enumerate(fixtures, start=1):
    print(f"Match {match_number:>2}: {home} vs {away}")

print("\nRESULTS")
print("=" * 60)

round_of_16 = []

for home, away in fixtures:

    winner = play_knockout_match(home, away)

    round_of_16.append(winner)

print("\nROUND OF 16 QUALIFIERS")
print("=" * 60)

for i, team in enumerate(round_of_16, start=1):
    print(f"{i:>2}. {team}")