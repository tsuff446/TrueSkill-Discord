class Player():
    
    default_sigma = 25/3
    default_mu = 25

    def __init__(self, discord_id, discord_alias, sigma=None, mu=None, wins=None, losses=None):
        self.discord_id = discord_id
        self.discord_alias = discord_alias

        self.sigma = sigma
        if not sigma:
            self.sigma = self.default_sigma
        self.mu = mu
        if not mu:
            self.mu = self.default_mu
        self.wins = wins
        if not wins:
            self.wins = 0
        self.losses = losses
        if not losses:
            self.losses = 0
        self.rating = -1
        self.recalc_rating()

    def skill_report(self, verbose=False):
        print("-------------------------------------")
        print("Skill Report For: ", self.discord_alias)
        print("Rating: ", self.rating)
        print("W/L: ", self.wins, "/", self.losses)
        if verbose:
            print("Sigma: ", self.sigma)
            print("Mu: ", self.mu)

    #calculates rating (rounds to nearest int, cannot be negative)
    def recalc_rating(self):
        self.rating = max(0, round(self.mu - 3*self.sigma))
    
    #updates all trueskill parameters
    def update_rating(self, sigma, mu):
        self.sigma = sigma
        self.mu = mu
        self.recalc_rating()
    
    def win(self):
        self.wins += 1
    
    def lose(self):
        self.losses += 1

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.discord_id == other.discord_id
        return False



#implements hash table of players
class PlayerList():
    def __init__(self, p_list=None, backup_path=None):
        self._p_list = {}
        if p_list:
            for player in p_list:
                self._p_list[player.discord_id] = player

        if backup_path:
            self.load_from_spreadsheet(backup_path)

    def check_player_exist(self, check):
        return self._p_list.get(check.discord_id, None) != None
    
    def find_player_by_id(self, id):
        return self._p_list.get(id, None)

    def add_player(self, player):
        if self.check_player_exist(player):
            return False
        self._p_list[player.discord_id] = player
        return True

    def to_list(self):
        return self._p_list.values()
    
    # functions for dealing with backups
    def _player_to_row(self, player):
        return (str(player.discord_id), str(player.discord_alias), str(player.rating), str(player.mu), str(player.sigma), str(player.wins), str(player.losses))

    #converts list of players to csv
    def backup_to_spreadsheet(self, path):
        players = self.to_list()
        f = open(path, 'w')
        #first line:
        f.write("Discord ID, Discord Name, Rating, Mu, Sigma, Wins, Losses \n")
        for player in players:
            f.write(','.join(self._player_to_row(player)) + "\n")
        f.close()

    #helper converts csv row to player object
    def _row_to_player(self, row):
        return Player(int(row[0]), str(row[1]), mu=float(row[3]), sigma=float(row[4]), wins=int(row[5]), losses=int(row[6]))

    #constructs player list from csv
    def load_from_spreadsheet(self, path):
        players = []
        try:
            f = open(path, 'r')
            #skip first line
            line = f.readline()
            line = f.readline()
            while line:
                players.append(self._row_to_player(line.split(',')))
                line = f.readline()
            f.close()
        except:
            return

        for player in players:
            self.add_player(player)


