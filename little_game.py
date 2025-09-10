# import os

# # Лабиринт: # - стена, . - дорога, @ - игрок
# maze = [
#     list("##########"),
#     list("#@.......#"),
#     list("#.######.#"),
#     list("#........#"),
#     list("##########")
# ]

# player_x, player_y = 1, 1  # начальная позиция игрока

# def print_maze():
#     os.system("cls" if os.name == "nt" else "clear")  # очистка экрана
#     for row in maze:
#         print("".join(row))

# def move(dx, dy):
#     global player_x, player_y
#     new_x = player_x + dx
#     new_y = player_y + dy
#     if maze[new_y][new_x] == ".":  # можно ходить только по точкам
#         maze[player_y][player_x] = "."
#         player_x, player_y = new_x, new_y
#         maze[player_y][player_x] = "@"

# while True:
#     print_maze()
#     command = input("Ход (w/a/s/d): ").lower()
#     if command == "w":
#         move(0, -1)
#     elif command == "s":
#         move(0, 1)
#     elif command == "a":
#         move(-1, 0)
#     elif command == "d":
#         move(1, 0)


# # import random

# # def generate_maze(width, height):
# #     maze = [["#" for _ in range(width)] for _ in range(height)]

# #     for y in range(1, height, 2):
# #         for x in range(1, width, 2):
# #             maze[y][x] = "."
# #             if x > 1:
# #                 if random.choice([True, False]):
# #                     maze[y][x - 1] = "."
# #                 else:
# #                     maze[y - 1][x] = "."

# #     maze[1][1] = "@"
# #     return maze

# # def print_maze(maze):
# #     for row in maze:
# #         print("".join(row))

# # lab = generate_maze(15, 15)
# # print_maze(lab)


import os
import time
from collections import deque

# Лабиринт: # - стена, . - дорога, @ - игрок, B - бот
maze = [
    list("##########"),
    list("#@.......#"),
    list("#.######.#"),
    list("#........#"),
    list("##########")
]

player_x, player_y = 1, 1   # человек
bot_x, bot_y = 8, 3         # бот начинает справа внизу


def print_maze():
    os.system("cls" if os.name == "nt" else "clear")
    for row in maze:
        print("".join(row))


def move(dx, dy):
    global player_x, player_y
    new_x, new_y = player_x + dx, player_y + dy
    if maze[new_y][new_x] == ".":  # игрок может ходить только по дорогам
        maze[player_y][player_x] = "."
        player_x, player_y = new_x, new_y
        maze[player_y][player_x] = "@"


# ---------- Поиск пути для бота (BFS) ----------
def find_path(start, goal):
    queue = deque([start])
    visited = {start: None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x+dx, y+dy
            if maze[ny][nx] in [".", "@"] and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    # восстанавливаем путь
    path = []
    cur = goal
    while cur and cur in visited:
        path.append(cur)
        cur = visited[cur]
    path.reverse()
    return path


def move_bot():
    global bot_x, bot_y
    path = find_path((bot_x, bot_y), (player_x, player_y))
    if len(path) > 1:  # первый шаг — текущая позиция
        new_x, new_y = path[1]
        if (new_x, new_y) == (player_x, player_y):
            print_maze()
            print("Бот поймал игрока!")
            exit()
        maze[bot_y][bot_x] = "."
        bot_x, bot_y = new_x, new_y
        maze[bot_y][bot_x] = "B"


# ---------- Игра ----------
maze[player_y][player_x] = "@"
maze[bot_y][bot_x] = "B"

while True:
    print_maze()
    command = input("Ход (w/a/s/d, q - выход): ").lower()
    if command == "q":
        break
    elif command == "w":
        move(0, -1)
    elif command == "s":
        move(0, 1)
    elif command == "a":
        move(-1, 0)
    elif command == "d":
        move(1, 0)

    move_bot()
    time.sleep(0.2)
