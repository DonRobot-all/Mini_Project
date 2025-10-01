import os
import time
import random
from collections import deque

# ---------- Генерация лабиринта ----------
def generate_maze(width, height):
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    maze = [["#" for _ in range(width)] for _ in range(height)]
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

    # список ловушек (10% свободных клеток)
    free_cells = [(x,y) for y in range(height) for x in range(width) if maze[y][x] == "."]
    traps = set(random.sample(free_cells, len(free_cells)//10))

    return maze, traps


# ---------- Отрисовка ----------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_maze():
    for row in maze:
        print("".join(row))


# ---------- Управление игроком ----------
def move(dx, dy):
    global player_x, player_y, player_stuck
    if player_stuck > 0:
        print("⛓ Игрок застрял в ловушке! Осталось ходов:", player_stuck)
        player_stuck -= 1
        return

    new_x, new_y = player_x + dx, player_y + dy
    if maze[new_y][new_x] == ".":  
        # проверка ловушки
        if (new_x, new_y) in traps:
            traps.remove((new_x, new_y))
            player_stuck = 2   # застревает на 2 хода
            print("💀 Игрок наступил в ловушку и застрял!")
        
        maze[player_y][player_x] = "."
        player_x, player_y = new_x, new_y
        maze[player_y][player_x] = "@"


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
    if abs(player_x - bot_x) <= 2 and abs(player_y - bot_y) <= 2:
        path = find_path((bot_x, bot_y), (player_x, player_y))
        if len(path) > 1:
            new_x, new_y = path[1]
        else:
            new_x, new_y = bot_x, bot_y
    else:
        moves = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(moves)
        new_x, new_y = bot_x, bot_y
        for dx, dy in moves:
            nx, ny = bot_x+dx, bot_y+dy
            if maze[ny][nx] == ".":
                new_x, new_y = nx, ny
                break

    if (new_x, new_y) == (player_x, player_y):
        clear()
        print_maze()
        print("Бот поймал игрока!")
        exit()

    maze[bot_y][bot_x] = "."
    bot_x, bot_y = new_x, new_y
    maze[bot_y][bot_x] = "B"


# ---------- Игра ----------
maze, traps = generate_maze(21, 15)

player_x, player_y = 1, 1
bot_x, bot_y = len(maze[0]) - 2, len(maze) - 2
player_stuck = 0  # счётчик "заморозки" игрока

maze[player_y][player_x] = "@"
maze[bot_y][bot_x] = "B"

while True:
    clear()
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
