from src.player import Player

#helper converts Player() to row
def player_to_row(player):
    return (str(player.discord_id), str(player.discord_alias), str(player.rating), str(player.mu), str(player.sigma), str(player.wins), str(player.losses))

#converts list of players to csv
def players_to_spreadsheet(path, players):
    f = open(path, 'w')
    #first line:
    f.write("Discord ID, Discord Name, Rating, Mu, Sigma, Wins, Losses \n")
    for player in players:
        f.write(','.join(player_to_row(player)) + "\n")
    f.close()

#helper converts csv row to player object
def row_to_player(row):
    return Player(int(row[0]), str(row[1]), mu=float(row[3]), sigma=float(row[4]), wins=int(row[5]), losses=int(row[6]))

#constructs player list from csv
def spreadsheet_to_players(path):
    players = []
    try:
        f = open(path, 'r')
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
