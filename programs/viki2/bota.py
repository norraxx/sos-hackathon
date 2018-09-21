import sys

LEFT = 'LEFT'
RIGHT = 'RIGHT'
UP = 'UP'
DOWN = 'DOWN'


class Fighter:
    def __init__(self, x, y, homeboy=False):
        self.x = x
        self.y = y
        self.homeboy = homeboy

    def repr(self):
        return "{}:{}".format(self.x, self.y)

    def do(self, action, message=""):
        return "{} {} {}".format(self.repr(), action, message)

    def __repr__(self):
        return "<{}{}>".format(
            "*" if self.homeboy else "+",
            self.repr()
        )


class Botka:

    def __init__(self):
        self.map = None
        self.symbol = None
        self.width = None
        self.height = None

    def load_state(self):
        data = [l.strip() for l in sys.stdin if l.strip() != ""]
        self.map = data[:-1]
        self.symbol = data[-1][0]
        self.width = len(self.map[0])
        self.height = len(self.map)

    def print_map(self):
        for i in self.map:
            print(i)
        print("")
        print("ME:", self.symbol)

    def win(self):
        #self.print_map()
        self.load_state()
        print(self.fight())

    def fight(self):
        shooting = list(self.analyze_shooting())
        for fighter, outcome, *xxx in sorted(shooting, key=lambda x: x[1], reverse=True):
            # we're men, we fight!
            if outcome > 0:
                return fighter.do("BUM!", "Be my bitch")
            break

        # OK, time to be wise
        return self.run_forest_run(shooting)

    def run_forest_run(self, shooting):
        for fighter, _, enemies, _ in sorted(shooting, key=lambda x: len(x[2]), reverse=True):
            escape_path = self.run_direction(fighter, enemies)
            if escape_path:
                return fighter.do(escape_path, message="Catch me if you can!")

        # fallback
        return shooting[0][0].do(LEFT, message="Just sightseeing :-)")

    def run_direction(self, fighter, enemies):
        # x is safe
        if not any(map(lambda e: e.x == fighter.x, enemies)):
            if fighter.x < (self.width - 1):
                enemies, _ = self.find_victims(Fighter(fighter.x + 1, fighter.y))
                if not enemies:
                    return RIGHT
            if fighter.x > 0:
                enemies, _ = self.find_victims(Fighter(fighter.x - 1, fighter.y))
                if not enemies:
                    return LEFT

        # y is safe
        if not any(map(lambda e: e.y == fighter.y, enemies)):
            if fighter.y < (self.height - 1):
                enemies, _ = self.find_victims(Fighter(fighter.x, fighter.y + 1))
                if not enemies:
                    return DOWN
            if fighter.y > 0:
                enemies, _ = self.find_victims(Fighter(fighter.x, fighter.y - 1))
                if not enemies:
                    return UP

        return None

    def analyze_shooting(self):
        for fighter in self.get_fighters():
            targets, victims = self.find_victims(fighter)
            yield fighter, len(targets) * 2 - len(victims), targets, victims

    def find_victims(self, fighter):
        targets = []
        casualties = []

        # horizontal
        to_check = [
            # horizontal
            [(x, fighter.y) for x in range(fighter.x + 1, self.width)],
            [(x, fighter.y) for x in range(fighter.x)[::-1]],
            # vertical
            [(fighter.x, y) for y in range(fighter.y + 1, self.height)],
            [(fighter.x, y) for y in range(fighter.y)[::-1]],
        ]
        for direction in to_check:
            for coords in direction:
                symbol = self.map[coords[1]][coords[0]]
                if symbol == "#":  # wall
                    break
                elif symbol == " ":
                    continue
                elif symbol == self.symbol:
                    casualties.append(Fighter(*coords, homeboy=True))
                else:
                    targets.append(Fighter(*coords))

        return targets, casualties

    def get_fighters(self):
        for y in range(self.height):
            for x in range(self.width):
                symbol = self.map[y][x]
                if symbol == self.symbol:
                    yield Fighter(x, y, homeboy=True)


if __name__ == '__main__':
    bot = Botka()
    bot.win()
