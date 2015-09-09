from elo import Rating, rate_1vs1
import random

# alice, bob = Rating(1000), Rating(1400)
# print alice, bob
# bob, alice = rate_1vs1(bob, alice)
# print alice, bob


def main():
    rankings = Ranking()

    while True:
        one, two = random.sample(rankings.options.keys(), 2)
        winner = raw_input("\n\nCompare {} vs {}: ".format(one, two))

        if winner in (one, two):
            loser = one if two == winner else two
            rankings.choices.append(Choice(winner, loser))
        elif 'rank' in winner:
            rankings.show()
        elif 'quit' in winner:
            break
        else:
            print "WAT?"

    rankings.save_choices()


class Choice():
    winner = None
    loser = None

    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser


class Ranking():
    choices = []
    options = {}
    filename = "choices.txt"

    def __init__(self):
        defaults = [
            'one',
            'two',
            'three'
        ]

        for option in defaults:
            self.options[option] = Rating(1000)

        self.load_choices()

    def save_choices(self):
        target = open(self.filename, 'w')
        target.truncate()

        for choice in self.choices:
            target.write("{},{}\n".format(choice.winner, choice.loser))

    def load_choices(self):
        with open(self.filename) as f:
            lines = f.readlines()

        for line in lines:
            winner, loser = line.strip().split(',')
            self.choices.append(Choice(winner, loser))

    def show(self):
        print self.choices
        for choice in self.choices:
            winner = self.options[choice.winner]
            loser = self.options[choice.loser]
            winner, loser = rate_1vs1(winner, loser)
            self.options[choice.winner] = winner
            self.options[choice.loser] = loser

        for option, score in self.options.iteritems():
            print "{}: {}".format(option, score)


if __name__ == "__main__":
    main()
