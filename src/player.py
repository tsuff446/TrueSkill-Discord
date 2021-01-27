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


def check_already_exists(check, players):
    for player in players:
        if check == player:
            return True
    return False

def find_player(id, players):
    for player in players:
        if id == player.discord_id:
            return player
    return None
