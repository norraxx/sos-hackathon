import subprocess
import sys
# 1. nacitat mapu - V
# 2. spustit skript se vstupem a precist vystup - V
# 3. zvalidovat vystup - V
# 4. provest vystup, vyhodnotit a upravit mapu - ongoing
# 5. ulozit mezivysledek nekam, at' vime co se deje -
# 6. hlavni smycka na spusteni
# 7. killovat po 50ti tazich

bot_colors = ["A", "B", "C", "D"]
ACTIONS = ["BUM!", "UP", "DOWN", "LEFT", "RIGHT"]
MOVE = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
MAX_STEPS = 20


def read_map(file_name):
    # type: (str) -> List[str]
    with open(file_name, "r") as f:
        return [row.strip() for row in f.read().split("\n")]


def run_map(map_, position, action, robot_color):
    xmax = len(map_[0])
    ymax = len(map_)
    y, x = MOVE[ACTIONS.index(action)]
    xpos, ypos = position

    new_map = []
    for row in map_:
        new_map.append([row[i] for i, letter in enumerate(row)])
    map_ = new_map

    map_[ypos][xpos] = " "
    if action == ACTIONS[0]:  # BUM!
        while 0 <= xpos < xmax and map_[ypos][xpos+1] != "#":
            xpos += 1
            map_[ypos][xpos] = " "

        while 0 <= xpos < xmax and map_[ypos][xpos-1] != "#":
            xpos -= 1
            map_[ypos][xpos] = " "

        while 0 <= ypos < ymax and map_[ypos+1][xpos] != "#":
            ypos += 1
            map_[ypos][xpos] = " "

        while 0 <= ypos < ymax and map_[ypos-1][xpos] != "#":
            ypos -= 1
            map_[ypos][xpos] = " "
    else:
        while 0 <= xpos < xmax and 0 <= ypos < ymax and map_[ypos + y][xpos + x] == " ":
            xpos += x
            ypos += y
        map_[ypos][xpos] = robot_color

    map_ = ["".join(row) for row in map_]

    return map_


def run_script(bot_name, map_, robot_color):
    with open("programs/{}/run.txt".format(bot_name), "r") as f:
        run_command = f.readline().strip().split()
    p = subprocess.Popen(run_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.communicate(input=("\n".join(map_) + "\n" + robot_color + "\n").encode('raw_unicode_escape'))[0].decode().strip()


def start():
    map_name = sys.argv[1]
    bot_names = sys.argv[2:]

    map_ = read_map(map_name)
    step = 0
    max_step_count = len(bot_names) * MAX_STEPS

    for _ in range(MAX_STEPS):
        for i, bot_name in enumerate(bot_names):
            if step > max_step_count:
                print("WAT!??")
                break
            robot_color = bot_colors[i]
            print("\n".join(map_))
            robot_action = run_script(bot_name, map_, robot_color)
            print(bot_name, robot_action)
            valid, position, action, text = validate(map_, robot_color, robot_action)
            if not valid:
                raise Exception("WTF!", robot_action)
            # todo: klara
            map_ = run_map(map_, position, action, robot_color)

            step += 1
#        break


def validate(robot_map, robot_color, robot_action):
    # robot_map = pole radku mapy
    # robot_color = barva robota
    # robot_action = akce co dela robot
    try:
        input = robot_action.split()
        action = input[1]

        if action not in ACTIONS:
            print('invalid actions', action)
            return False, (None, None), None, None

        position = input[0]
        position_x, position_y = position.split(":", 2)
        position_x = int(position_x)
        position_y = int(position_y)

        if (
            position_y >= len(robot_map)
            or position_x >= len(robot_map[0])
            or position_x < 0
            or position_y < 0
        ):
            print('invalid positions', position)
            return False, (None, None), None, None

        real_robot = robot_map[position_y][position_x]
        if real_robot != robot_color:
            print('invalid wrong color "{}" {}, {}'.format(real_robot, robot_color, position))
            return False, (None, None), None, None

        return True, (position_x, position_y), action, input[2:]
    except Exception:
        return False, (None, None), None, None


def update_path_up(new_robot_map, new_robot_position, is_move=False):
    for index in range(new_robot_position[1] - 1, -1, -1):
        if new_robot_map[index][new_robot_position[0]] == "#":
            new_char = "#"
            new_row = (
                new_robot_map[index][:new_robot_position[0]]
                + new_char
                + new_robot_map[index][(new_robot_position[0] + 1):]
            )
            new_robot_map[index] = new_row
            break
        elif (
            new_robot_map[index][new_robot_position[0]] == " "
            or new_robot_map[index][new_robot_position[0]] == "~"
        ):
            new_char = "*"
        else:
            new_char = "@"
        new_row = (
            new_robot_map[index][:new_robot_position[0]]
            + new_char
            + new_robot_map[index][(new_robot_position[0] + 1):]
        )
        new_robot_map[index] = new_row
    return new_robot_map


def update_path_down(new_robot_map, new_robot_position, is_move=False):
    for index in range(new_robot_position[1] + 1, len(new_robot_map)):
        if new_robot_map[index][new_robot_position[0]] == "#":
            new_char = "#"
            new_row = (
                new_robot_map[index][:new_robot_position[0]]
                + new_char
                + new_robot_map[index][(new_robot_position[0] + 1):]
            )
            new_robot_map[index] = new_row
            break
        elif (
            new_robot_map[index][new_robot_position[0]] == " "
            or new_robot_map[index][new_robot_position[0]] == "~"
        ):
            new_char = "*"
        else:
            new_char = "@"
        new_row = (
            new_robot_map[index][:new_robot_position[0]]
            + new_char
            + new_robot_map[index][(new_robot_position[0] + 1):]
        )
        new_robot_map[index] = new_row
    return new_robot_map


def update_path_left(new_robot_map, new_robot_position, is_move=False):
    new_row = new_robot_map[new_robot_position[1]][new_robot_position[0]:]
    for index in range(new_robot_position[0] - 1, -1, -1):
        if new_robot_map[new_robot_position[1]][index] == "#":
            new_row = ("#" + new_row)
            break
        elif (
            new_robot_map[new_robot_position[1]][index] == " "
            or new_robot_map[new_robot_position[1]][index] == "~"
        ):
            new_row = ("*" + new_row)
        else:
            new_row = ("@" + new_row)

    new_robot_map[new_robot_position[1]] = new_row
    return new_robot_map


def update_path_right(new_robot_map, new_robot_position, is_move=False):
    new_row = new_robot_map[new_robot_position[1]][:(new_robot_position[0] + 1)]
    for index in range(new_robot_position[0] + 1, len(new_robot_map[0])):
        if new_robot_map[new_robot_position[1]][index] == "#":
            new_row += "#"
            break
        elif (
            new_robot_map[new_robot_position[1]][index] == " "
            or new_robot_map[new_robot_position[1]][index] == "~"
        ):
            new_row += "*"
        else:
            new_row += "@"

    new_robot_map[new_robot_position[1]] = new_row
    return new_robot_map


def get_map_to_log(old_robot_map, robot_color, new_robot_position, robot_action):
    new_robot_map = old_robot_map

    if robot_action == "BUM!":
        # oznacim vybuchleho bota
        new_robot_map[new_robot_position[1]] = (
            new_robot_map[new_robot_position[1]][:new_robot_position[0]]
            + "@"
            + new_robot_map[new_robot_position[1]][(new_robot_position[0] + 1):]
        )

        # vybuch nahoru
        new_robot_map = update_path_up(new_robot_map, new_robot_position)

        # vybuch dolu
        new_robot_map = update_path_down(new_robot_map, new_robot_position)

        # vybuch do leva
        new_robot_map = update_path_left(new_robot_map, new_robot_position)

        # vybuch do prava
        new_robot_map = update_path_right(new_robot_map, new_robot_position)

    else:
        if robot_action == "UP":
            pass
        elif robot_action == "DOWN":
            pass
        elif robot_action == "LEFT":
            pass
        elif robot_action == "RIGHT":
            pass

    return new_robot_map


if __name__ == "__main__":
    start()
