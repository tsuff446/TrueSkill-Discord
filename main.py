from src.player import Player
from src.trueskill_helpers import check_fair, report_match
import numpy as np
from src.spreadsheet_helpers import players_to_spreadsheet, spreadsheet_to_players
import matplotlib.pyplot as plt

players = []
num_players = 100
num_matches = 100000

for i in range(num_players):
    players.append(Player(str(i), str(i)))

for match in range(num_matches):
    participants = np.random.choice(players, 2, replace=False)
    if int(participants[1].discord_id) < int(participants[0].discord_id):
        report_match(participants[1], participants[0])
        continue
    report_match(participants[0], participants[1])

for player in players:
    player.skill_report()

plt.hist([player.rating for player in players])
plt.show()