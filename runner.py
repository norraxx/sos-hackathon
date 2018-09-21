import subprocess
from typing import List
import sys
# 1. nacitat mapu - V
# 2. spustit skript se vstupem a precist vystup - V
# 3. zvalidovat vystup
# 4. provest vystup, vyhodnotit a upravit mapu
# 5. ulozit mezivysledek nekam, at' vime co se deje

bot_colors = ["A", "B", "C", "D"]
ACTIONS = ["BUM!", "UP", "DOWN", "LEFT", "RIGHT"]


def read_map(file_name):
    # type: (str) -> List[str]
    with open(file_name, "r") as f:
        return [row.strip() for row in f.read().split("\n")]


def run_map(map, bot):
    pass


def run_script(bot_name, map_, robot_color):
    with open("programs/{}/run.txt".format(bot_name), "r") as f:
        run_command = f.readline().strip().split()
    p = subprocess.Popen(run_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.communicate(input=("\n".join(map_) + "\n" + robot_color + "\n").encode('raw_unicode_escape'))[0].decode()


def start():
    map_name = sys.argv[1]
    bot_names = sys.argv[2:]

    map_ = read_map(map_name)
    step_count = len(bot_names) * 50
    for i, bot_name in enumerate(bot_names):
        robot_color = bot_colors[i]
        robot_action = run_script(bot_name, map_, robot_color)

        validate(map_, robot_color, robot_action)


def validate(robot_map, robot_color, robot_action):
    # robot_action: str
    input = robot_action.split()
    action = input[1]

    if action not in ACTIONS:
        return False

    position = input[0]

    return True


if __name__ == "__main__":
    start()
