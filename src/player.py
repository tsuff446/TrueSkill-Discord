class Player():
    default_sigma = 25/3
    default_mu = 25
    def __init__(self, discord_name):
        self.discord_name = discord_name
        self.sigma = self.default_sigma
        self.mu = self.default_mu
        self.rating = -1
        self.recalc_rating()

    def skill_report(self):
        print("Skill Report For: ", self.discord_name)
        print("Rating: ", self.rating)
        print("Sigma: ", self.sigma)
        print("Mu: ", self.mu)
        
    def recalc_rating(self):
        self.rating = self.mu - 3*self.sigma
    
    def update_rating(self, sigma, mu):
        self.sigma = sigma
        self.mu = mu
        self.recalc_rating()