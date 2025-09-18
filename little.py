import os

maze = [
    list("##########"),
    list("#        #"),
    list("# ###### #"),
    list("#        #"),
    list("##########")
]

player_x = 1
player_y = 1
maze[player_y][player_x] = 'П'


def print_maze():
    os.system('cls')
    for row in maze:
        print(''.join(row))


def find_path():
    """ BFS """
    ...

def move_bot():
    ...

def move(x, y):
    global player_x, player_y
    new_x, new_y = player_x + x, player_y + y
    if maze[new_y][new_x] == ' ':
        maze[player_y][player_x] = ' '
        player_x, player_y = new_x, new_y
        maze[player_y][player_x] = 'П'
    print_maze()

def keyboard():
    command = input(f"Ход w/a/s/d").lower()
    match command:
        case 'w': move(0, -1)
        case 's': move(0, 1)
        case 'a': move(-1, 0)
        case 'd': move(1, 0)


def main():
    keyboard()


if __name__ == "__main__":
    while True:
        main()