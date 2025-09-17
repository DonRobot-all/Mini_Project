import os
import time
import random

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_maze(maze):
    for row in maze:
        print("".join(row))

def generate_maze(width, height, delay=0.05):
    # размеры должны быть нечётными
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    # сетка полностью из стен
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
                # ломаем стену
                maze[ny][nx] = "."
                maze[y + dy//2][x + dx//2] = "."
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()

        # визуализация
        clear()
        print_maze(maze)
        time.sleep(delay)

    return maze

if __name__ == "__main__":
    generate_maze(31, 21, delay=0.02)