from src.player import Player

def player_to_row(player):
    return (player.discord_name, str(player.rating), str(player.mu), str(player.sigma), str(player.wins), str(player.losses))

def players_to_spreadsheet(name, players):
    f = open(name, 'w')
    for player in players:
        f.write(','.join(player_to_row(player)) + "\n")
    f.close()

def row_to_player(row):
    return Player(row[0], mu=float(row[2]), sigma=float(row[3]), wins=int(row[4]), losses=int(row[5]))

def spreadsheet_to_players(name):
    players = []
    f = open(name, 'r')
    line = f.readline()
    while line:
        players.append(row_to_player(line.split(',')))
        line = f.readline()
    f.close()
    return players
