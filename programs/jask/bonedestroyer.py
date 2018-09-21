from collections import defaultdict
from copy import deepcopy
from sys import stdin, stdout
from random import choice


class Game:
    moves = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (0, 1),
    }

    directions = list(moves.values())

    voices = [
        "Choookity!",
        "BrmBrrrrmBRM!",
        "MortalCombat!",
        "DIEEEEEE!!!",
        "Mercy, please!",
        "Killing monsters",
        "Lok'tar Ogar",
        "Indeed",
        "I see dead bots",
    ]

    def __init__(self, arena, color, players=None):
        self.arena = arena
        self.color = color
        self.players = players

        if self.players is None:
            self.read_players()

    @classmethod
    def load(cls, fp):
        arena = []

        for line in fp:
            line = line.strip()
            if not line:
                continue
            arena.append(list(line))

        color = arena.pop()[0]
        return cls(arena, color)

    def read_players(self):
        players = defaultdict(list)
        for y, line in enumerate(self.arena):
            for x, char in enumerate(line):
                if char in " #":
                    continue
                players[char].append((x, y))

        self.players = players

    def boom(self, x, y):
        score = 0
        color = self.arena[y][x]
        arena = deepcopy(self.arena)

        for dx, dy in self.directions:
            tx, ty = x, y
            while True:
                tx, ty = tx + dx, ty + dy
                target = arena[ty][tx]
                if target == "#":
                    break
                elif target == " ":
                    continue
                elif target == color:
                    score -= 1
                    arena[ty][tx] = " "
                else:  # todo new items
                    score += 2
                    arena[ty][tx] = " "

        return score, arena

    def move(self, x, y, delta):
        dx, dy = delta
        arena = deepcopy(self.arena)
        color = arena[y][x]
        arena[y][x] = " "

        while True:
            nx, ny = x + dx, y + dy
            if arena[ny][nx] != " ":
                arena[y][x] = color
                break
            x, y = nx, ny

        return 0, arena

    def play(self, x, y, action):
        if self.arena[y][x] != self.color:
            return False

        if action == "BUM!":
            return self.boom(x, y)
        else:
            return self.move(x, y, self.directions[action])

    def write(self, x, y, action):
        return "{}:{} {} {}".format(x, y, action, choice(self.voices))

    def simulate(self):
        options = (
            (self.boom(x, y), (x, y)) for x, y in self.players[self.color])

        out, target = max(
            options,
            key=lambda o: o[0][0])

        x, y = target
        if out[0] > 0:
            return self.write(x, y, "BUM!")
        else:
            x, y = choice(self.players[self.color])
            return self.write(x, y, choice(list(self.moves.keys())))


def main():
    game = Game.load(stdin)
    print(game.simulate(), file=stdout)


if __name__ == "__main__":
    main()
