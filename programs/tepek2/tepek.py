import sys

def print_mapa(mapa):
    for line in mapa:
        print(''.join(line))

def load_data():
    mapa = []
    me = ""
    for line in sys.stdin:
        if not line.strip():
            continue
        if len(line.strip()) == 1:
            me = line.strip()
            break
        line_array = []
        for symbol in line:
            if symbol == '\n':
                continue
            line_array.append(symbol)
        mapa.append(line_array)
    return mapa, me

def copy_map(mapa):
    new_mapa = []
    for line in mapa:
        new_line = []
        for cell in line:
            new_line.append(cell)
        new_mapa.append(new_line)
    return new_mapa

def end_poziton(bot, mapa, direction):
    space = ' '
    me = mapa[bot['x']][bot['y']]
    new_mapa = copy_map(mapa)
    if direction == 'UP':
        delta = {'x': -1, 'y': 0}
    if direction == 'DOWN':
        delta = {'x': 1, 'y': 0}
    if direction == 'LEFT':
        delta = {'x': 0, 'y': -1}
    if direction == 'RIGHT':
        delta = {'x': 0, 'y': 1}
    x = bot['x']
    y = bot['y']
    while True:
        if new_mapa[x+delta['x']][y+delta['y']] == space:
            new_mapa[x][y] = space
            x += delta['x']
            y += delta['y']
            new_mapa[x][y] = me
        else:
            break
    return {'x': x, 'y': y}, new_mapa

def see_something(bot, mapa, alies):
    def am_i_out(x, y, mapa):
        x_max, y_max = map_size(mapa)
        if x < 0 or y < 0:
            return True
        if x == x_max or y == y_max:
            return True
        return False

    me = mapa[bot['x']][bot['y']]
    not_enemies = [me, '#', ' ']

    directions = [{'x': -1, 'y': 0}, {'x': 0, 'y': -1}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1}]

    for direction in directions:
        x = bot['x']
        y = bot['y']
        while True:
            x += direction['x']
            y += direction['y']
            if am_i_out(x, y, mapa):
                break
            if alies:
                if mapa[x][y] == me:
                    return True
            else:
                if mapa[x][y] not in not_enemies:
                    return True
    
    return False

def do_i_see_me(bot, mapa):
    return see_something(bot, mapa, True)

def do_i_see_enemies(bot, mapa):
    return see_something(bot, mapa, False)

def my_bots(mapa, me):
    bots = []
    x, y = map_size(mapa)
    for i in range(x):
        for j in range(y):
            if mapa[i][j] == me:
                bots.append({'x': i, 'y': j})
    return bots

def map_size(mapa):
    x = len(mapa)
    y = len(mapa[0])
    return x, y

def do_move(bot, mapa):
    action = None
    direction = 'UP'
    new_pozition, new_mapa = end_poziton(bot, mapa, direction)
    if not do_i_see_me(new_pozition, new_mapa) and not do_i_see_enemies(new_pozition, new_mapa):
        action = direction
    direction = 'DOWN'
    new_pozition, new_mapa = end_poziton(bot, mapa, direction)
    if not do_i_see_me(new_pozition, new_mapa) and not do_i_see_enemies(new_pozition, new_mapa):
        action = direction
    direction = 'LEFT'
    new_pozition, new_mapa = end_poziton(bot, mapa, direction)
    if not do_i_see_me(new_pozition, new_mapa) and not do_i_see_enemies(new_pozition, new_mapa):
        action = direction
    direction = 'RIGHT'
    new_pozition, new_mapa = end_poziton(bot, mapa, direction)
    if not do_i_see_me(new_pozition, new_mapa) and not do_i_see_enemies(new_pozition, new_mapa):
        action = direction

    return action

def do_action(mapa, me):
    action = None
    bots = my_bots(mapa, me)
    for bot in bots:
        if do_i_see_enemies(bot, mapa):
            action = (bot,"BUM!")
        if do_i_see_me(bot, mapa):
            action = (bot,do_move(bot, mapa)) if do_move(bot, mapa) else action

    return action

mapa, me = load_data()
action = do_action(mapa, me)
if action is None:
    bots = my_bots(mapa, me)
    action = (bots[0], 'RIGHT')

BOT, ACTION = action
X = BOT['y']
Y = BOT['x']
MESSAGE = 'JOOOO'

print("{}:{} {} {}".format(X, Y, ACTION, MESSAGE))
