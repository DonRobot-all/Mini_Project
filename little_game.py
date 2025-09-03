import os

# Лабиринт: # - стена, . - дорога, @ - игрок
maze = [
    list("##########"),
    list("#@.......#"),
    list("#.######.#"),
    list("#........#"),
    list("##########")
]

player_x, player_y = 1, 1  # начальная позиция игрока

def print_maze():
    os.system("cls" if os.name == "nt" else "clear")  # очистка экрана
    for row in maze:
        print("".join(row))

def move(dx, dy):
    global player_x, player_y
    new_x = player_x + dx
    new_y = player_y + dy
    if maze[new_y][new_x] == ".":  # можно ходить только по точкам
        maze[player_y][player_x] = "."
        player_x, player_y = new_x, new_y
        maze[player_y][player_x] = "@"

while True:
    print_maze()
    command = input("Ход (w/a/s/d): ").lower()
    if command == "w":
        move(0, -1)
    elif command == "s":
        move(0, 1)
    elif command == "a":
        move(-1, 0)
    elif command == "d":
        move(1, 0)


# import random

# def generate_maze(width, height):
#     maze = [["#" for _ in range(width)] for _ in range(height)]

#     for y in range(1, height, 2):
#         for x in range(1, width, 2):
#             maze[y][x] = "."
#             if x > 1:
#                 if random.choice([True, False]):
#                     maze[y][x - 1] = "."
#                 else:
#                     maze[y - 1][x] = "."

#     maze[1][1] = "@"
#     return maze

# def print_maze(maze):
#     for row in maze:
#         print("".join(row))

# lab = generate_maze(15, 15)
# print_maze(lab)
