class Player():
    
    default_sigma = 25/3
    default_mu = 25

    def __init__(self, discord_name):
        self.discord_name = discord_name
        self.sigma = self.default_sigma
        self.mu = self.default_mu
        self.rating = -1
        self.recalc_rating()

        self.wins = 0
        self.losses = 0

    def skill_report(self, verbose=False):
        print("-------------------------------------")
        print("Skill Report For: ", self.discord_name)
        print("Rating: ", self.rating)
        print("W/L: ", self.wins, "/", self.losses)
        if verbose:
            print("Sigma: ", self.sigma)
            print("Mu: ", self.mu)

    def recalc_rating(self):
        self.rating = self.mu - 3*self.sigma
    
    def update_rating(self, sigma, mu):
        self.sigma = sigma
        self.mu = mu
        self.recalc_rating()
    
    def win(self):
        self.wins += 1
    
    def lose(self):
        self.losses += 1