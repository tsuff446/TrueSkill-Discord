from src.player import Player
from src.trueskill_helpers import check_fair, report_match
import numpy as np
from src.spreadsheet_helpers import players_to_spreadsheet, spreadsheet_to_players
import matplotlib.pyplot as plt
from src.matchmaking import PlayerQueue

players = []
num_players = 5

for i in range(num_players):
    players.append(Player(str(i), str(i)))

mm_queue = PlayerQueue()
for player in players:
    #choose random amount of minutes
    mins = np.random.choice([5, 10, 20])
    print(mins)
    mm_queue.enqueue_player(player, mins)

print(mm_queue._queue)