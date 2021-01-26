from src.player import Player

def player_to_row(player):
    return (str(player.discord_id), str(player.discord_alias), str(player.rating), str(player.mu), str(player.sigma), str(player.wins), str(player.losses))

def players_to_spreadsheet(name, players):
    f = open(name, 'w')
    #first line:
    f.write("Discord ID, Discord Name, Rating, Mu, Sigma, Wins, Losses \n")
    for player in players:
        f.write(','.join(player_to_row(player)) + "\n")
    f.close()

def row_to_player(row):
    return Player(int(row[0]), str(row[1]), mu=float(row[3]), sigma=float(row[4]), wins=int(row[5]), losses=int(row[6]))

def spreadsheet_to_players(name):
    players = []
    try:
        f = open(name, 'r')
        #skip first line
        line = f.readline()
        line = f.readline()
        while line:
            players.append(row_to_player(line.split(',')))
            line = f.readline()
        f.close()
    except:
        return []
    return players
