from src.player import Player
from src.trueskill_helpers import check_fair, report_match

p1 = Player("poop")
p2 = Player("pee")

p1.skill_report()
p2.skill_report()
print(check_fair(p1, p2))
report_match(p1, p2)
p1.skill_report()
p2.skill_report()