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
import random
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


def generate_maze(width, height):
    # размеры должны быть нечетными, чтобы были стены
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    maze = [["#" for _ in range(width)] for _ in range(height)]

    # начинаем с точки (1,1)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = "."

    stack = [(start_x, start_y)]
    directions = [(0,2),(2,0),(0,-2),(-2,0)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        carved = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == "#":
                maze[ny][nx] = "."
                maze[y + dy//2][x + dx//2] = "."
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()

    return maze

def print_maze():
    # os.system("cls" if os.name == "nt" else "clear")
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
    # print(visited)
    path = []
    cur = goal
    while cur and cur in visited:
        path.append(cur)
        cur = visited[cur]
    path.reverse()
    print(path)
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
maze = generate_maze(21, 15) 

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




# ---------- Поиск пути для бота ----------
def find_path(start, goal):
    queue = deque([start])
    visited = {start: None}

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x+dx, y+dy
            if maze[ny][nx] in [".","@"] and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    path = []
    cur = goal
    while cur and cur in visited:
        path.append(cur)
        cur = visited[cur]
    path.reverse()
    return path


# ---------- Бот-охотник ----------
def move_bot():
    global bot_x, bot_y
    # Проверяем: видит ли бот игрока в радиусе 2 клеток
    if abs(player_x - bot_x) <= 2 and abs(player_y - bot_y) <= 2:
        path = find_path((bot_x, bot_y), (player_x, player_y))
        if len(path) > 1:
            new_x, new_y = path[1]
        else:
            new_x, new_y = bot_x, bot_y
    else:
        # случайный ход, если игрока не видно
        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(moves)
        new_x, new_y = bot_x, bot_y
        for dx, dy in moves:
            nx, ny = bot_x+dx, bot_y+dy
            if maze[ny][nx] == ".":
                new_x, new_y = nx, ny
                break

    # Проверка на поимку
    if (new_x, new_y) == (player_x, player_y):
        maze[bot_y][bot_x] = "."
        bot_x, bot_y = new_x, new_y
        maze[bot_y][bot_x] = "B"
        print_maze()
        print("Бот поймал игрока!")
        exit()

    maze[bot_y][bot_x] = "."
    bot_x, bot_y = new_x, new_y
    maze[bot_y][bot_x] = "B"
