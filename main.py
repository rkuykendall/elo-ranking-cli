import random
import operator
from elo import Rating, rate_1vs1


def main():
    rankings = Ranking()

    while True:
        one, two = random.sample(rankings.options.keys(), 2)
        winner = raw_input("\n\nCompare {} vs {}: ".format(one, two))

        if winner in (one, two):
            loser = one if two == winner else two
            rankings.choices.append(Choice(winner, loser))
        elif winner.lower() in ('show', 'rank', 'r'):
            rankings.show()
        elif winner.lower() in ('exit', 'quit', 'q', 'x'):
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
    choices_file = "choices.txt"
    options_file = "options.txt"

    def __init__(self):
        defaults = [
            'one',
            'two',
            'three'
        ]

        with open(self.options_file) as f:
            lines = f.readlines()
        defaults = [d.strip() for d in lines]

        for option in defaults:
            self.options[option] = Rating(1000)

        self.load_choices()

    def save_choices(self):
        target = open(self.choices_file, 'w')
        target.truncate()

        for choice in self.choices:
            target.write("{},{}\n".format(choice.winner, choice.loser))

    def load_choices(self):
        with open(self.choices_file) as f:
            lines = f.readlines()

        for line in lines:
            winner, loser = line.strip().split(',')
            self.choices.append(Choice(winner, loser))

    def show(self):
        for choice in self.choices:
            winner = self.options[choice.winner]
            loser = self.options[choice.loser]
            winner, loser = rate_1vs1(winner, loser)
            self.options[choice.winner] = winner
            self.options[choice.loser] = loser

        sorted_options = sorted(
            self.options.items(), key=operator.itemgetter(1))
        sorted_options.reverse()

        rank = 1
        for option, score in sorted_options:
            print "{}. {} ({})".format(rank, option, score)
            rank += 1


if __name__ == "__main__":
    main()
