from src.player import Player
from src.trueskill_helpers import check_fair, report_match
import numpy as np

players = []
num_players = 10
num_matches = 1000

for i in range(num_players):
    players.append(Player(str(i)))

for match in range(num_matches):
    participants = np.random.choice(players, 2, replace=False)
    if int(participants[1].discord_name) < int(participants[0].discord_name):
        report_match(participants[1], participants[0])
        continue
    report_match(participants[0], participants[1])

for player in players:
    player.skill_report()