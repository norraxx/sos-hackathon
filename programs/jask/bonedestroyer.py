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
        self.score = defaultdict(int)

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
        players = deepcopy(self.players)

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
                    players[color].remove((tx, ty))
                else:
                    score += 2
                    arena[ty][tx] = " "
                    players[target].remove((tx, ty))

        return self.play(arena, score, players)

    def move(self, x, y, delta):
        dx, dy = delta
        arena = deepcopy(self.arena)
        players = deepcopy(self.players)
        color = arena[y][x]
        arena[y][x] = " "
        players[color].remove((x, y))

        while True:
            nx, ny = x + dx, y + dy
            if arena[ny][nx] != " ":
                arena[y][x] = color
                players[color].append((x, y))
                break
            x, y = nx, ny

        return self.play(arena, 0, players)

    def next_player(self, players=None):
        if players is None:
            players = self.players
        players = list(players.keys())
        return players[(players.index(self.color) + 1) % len(players)]

    def play(self, arena, score, players):
        new = self.__class__(arena, self.next_player(players), players)
        new.score = self.score.copy()
        new.score[self.color] += score
        return new

    def win_chance(self, color=None, score=None):
        if color is None:
            color = self.color
        if score is None:
            score = self.score
        whole = sum(score.values())
        if whole == 0:
            return 0
        return score[color] - whole / len(score)

    def write(self, x, y, action):
        return "{}:{} {} {}".format(x, y, action, choice(self.voices))

    def simulate(self, n=3):
        n -= 1
        if n < 1:
            return self.score, None

        score = None
        plays = []
        for x, y in self.players[self.color]:
            for action, delta in self.moves.items():
                new = self.move(x, y, delta)
                score, _ = new.simulate(n)
                plays.append((score, (x, y), action, new))

            new = self.boom(x, y)
            score, _ = new.simulate(n)
            plays.append((score, (x, y), "BUM!", new))

        if score is None:
            return self.score, None

        best = max(plays, key=lambda obj: self.win_chance(score=obj[0]))
        score = best[0]
        return score, best

    def compete(self):
        _, play = self.simulate()
        _, delta, action, _ = play
        x, y = delta
        return self.write(x, y, action)


def main():
    game = Game.load(stdin)
    print(game.compete(), file=stdout)


if __name__ == "__main__":
    main()
