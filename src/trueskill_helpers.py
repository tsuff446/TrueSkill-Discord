from trueskill import TrueSkill, Rating, quality_1vs1, rate_1vs1

def check_fair(p1, p2):
    ts = TrueSkill(draw_probability=0)
    p1_rating = Rating(mu=p1.mu, sigma=p1.sigma)
    p2_rating = Rating(mu=p2.mu, sigma=p2.sigma)
    quality = quality_1vs1(p1_rating, p2_rating, env=ts)
    if quality < .3:
        return False
    return True

def report_match(winner, loser):
    ts = TrueSkill(draw_probability=0)
    winner_rating = Rating(mu=winner.mu, sigma=winner.sigma)
    loser_rating = Rating(mu=loser.mu, sigma=loser.sigma)
    new_winner_rating, new_loser_rating = rate_1vs1(winner_rating, loser_rating, drawn=False, min_delta=0.0001, env=ts)
    winner.update_rating(new_winner_rating.sigma, new_winner_rating.mu)
    loser.update_rating(new_loser_rating.sigma, new_loser_rating.mu)

